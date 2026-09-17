#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Podzial keycapa "Psyduck" (Bambu Studio 3MF, malowanie MMU) na osobne czesci,
po jednej na kolor - zeby kazda grupe wydrukowac jednym filamentem, bez
przezbrajania AMS i bez wiezy czyszczacej.

Zasada dzialania
----------------
Model zrodlowy ma malowanie MMU zapisane w atrybutach `paint_color` trojkatow.
Skrypt dekoduje je (kodowanie TriangleSelector z PrusaSlicer/BambuStudio),
grupuje trojkaty w obszary kolorow i zamienia kazdy obszar na osobna BRYLE:

  * obszar wypukly (dziob, oczy, wlosy) -> "czop": powierzchnia obszaru
    + scianki wyciagniete wzdluz kierunku d + plaska podstawa. Gniazdo w
    korpusie to ta sama bryla, tylko bez zbieznosci - dzieki temu krawedz
    na powierzchni trafia w siebie co do mikrona (szew niewidoczny),
    a czop ma LUZ mm zbieznosci w glab (latwy montaz + miejsce na klej).

  * stopy -> operacje boolowskie (obrys stopy w XY jest samoprzecinajacy
    sie w rzucie, wiec metoda czopa tu nie dziala).

  * baza keycapa (czarna) odcina sie plaszczyzna Z_SZWU - model ma tam
    gotowy, plaski szew (zero trojkatow przecinajacych plaszczyzne).

Jednostki: milimetry. Uruchomienie:  python3 podzial_kolorow.py [zrodlo.3mf]
"""
import sys, os, re, collections, zipfile
import numpy as np, trimesh
import mapbox_earcut as earcut
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

# ========================= PARAMETRY =========================
LUZ          = 0.10   # luz boczny czopa [mm] - pasowanie ciasne wg CLAUDE.md
GL_DZIOB     = 2.5    # glebokosc czopa dzioba [mm]
KIER_DZIOB   = (0.0, 0.87, -0.5)   # czop dzioba schodzi skosem w dol (30 st.):
                      # przy kierunku poziomym (0,1,0) gniazdo dzioba zachodzi
                      # na gniazda oczu i czesci nie daloby sie zlozyc
GL_OKO       = 1.4    # glebokosc czopa oka [mm]
GL_WLOSY     = 1.2    # glebokosc czopa kepki wlosow [mm]
GL_STOPA     = 0.6    # ile stopa wchodzi w czarna baze ponizej szwu [mm]
                      # (gorna scianka bazy ma 1.54 mm - zostaje >0.9 mm)
Z_SZWU       = -3.61904001   # plaski szew miedzy kaczka a baza keycapa [mm]
Z_STOPA_GORA = -2.80  # gorne ograniczenie bryly stopy [mm]
ODSTEP       = 6.0    # odstep miedzy czesciami na plycie [mm]
SRODEK       = (128.0, 128.0)  # srodek plyty A1 (256 x 256) [mm]

KOLORY = {'zolty':1, 'czarny':2, 'bialy':3, 'kremowy':4}   # numery slotow AMS
# =============================================================


# ---------- 1. wczytanie 3MF + dekodowanie malowania MMU ----------
def wczytaj_3mf(sciezka):
    """Zwraca (vertices, faces, state) - state to numer filamentu na trojkat
    (0 = domyslny filament obiektu, czyli slot 1)."""
    with zipfile.ZipFile(sciezka) as z:
        nazwa = [n for n in z.namelist() if n.endswith('.model') and 'Objects' in n]
        nazwa = nazwa[0] if nazwa else '3D/3dmodel.model'
        xml = z.read(nazwa).decode('utf-8')

    V = np.array([[float(a), float(b), float(c)] for a, b, c in re.findall(
        r'<vertex x="([-\d.eE+]+)" y="([-\d.eE+]+)" z="([-\d.eE+]+)"', xml)])

    tris, paints = [], []
    for m in re.finditer(r'<triangle ([^/]*?)/>', xml):
        at = m.group(1)
        tris.append([int(re.search(f'v{i}="(\\d+)"', at).group(1)) for i in (1, 2, 3)])
        pc = re.search(r'paint_color="([0-9A-Fa-f]+)"', at)
        paints.append(pc.group(1) if pc else None)
    F = np.array(tris)

    def bity(s):
        # znaki od konca, w kazdym pol-bajcie bity od najmlodszego
        return [(int(ch, 16) >> i) & 1 for ch in reversed(s) for i in range(4)]

    def dekoduj(s):
        """Zwraca liste (stan, glebokosc_podzialu) dla lisci drzewa podzialu."""
        b = bity(s); poz = [0]; out = []
        def rd(n):
            v = b[poz[0]:poz[0] + n]; poz[0] += n; return v
        def wezel(d):
            sp = rd(2); boki = sp[0] | (sp[1] << 1)
            if boki:                      # trojkat podzielony - schodzimy nizej
                rd(2)
                for _ in range(boki + 1): wezel(d + 1)
            else:                         # lisc - zapisany stan
                nb = rd(2); n = nb[0] | (nb[1] << 1)
                if n == 3:
                    e = rd(4); n = 3 + (e[0] | (e[1] << 1) | (e[2] << 2) | (e[3] << 3))
                out.append((n, d))
        wezel(0)
        return out

    S = np.zeros(len(F), dtype=int)
    for i, p in enumerate(paints):
        if p is None: continue
        w = collections.Counter()
        for n, d in dekoduj(p): w[n] += 0.25 ** d    # waga = udzial powierzchni
        S[i] = w.most_common(1)[0][0]
    return V, F, S


# ---------- 2. narzedzia geometryczne ----------
def skladowe(m, maska):
    """Spojne skladowe podzbioru scian."""
    import scipy.sparse as sp
    from scipy.sparse.csgraph import connected_components
    sel = np.where(maska)[0]; idx = {f: i for i, f in enumerate(sel)}
    a = m.face_adjacency
    pr = a[maska[a[:, 0]] & maska[a[:, 1]]]
    g = sp.coo_matrix((np.ones(len(pr)), ([idx[x] for x in pr[:, 0]],
                                          [idx[x] for x in pr[:, 1]])),
                      shape=(len(sel), len(sel)))
    n, lab = connected_components(g, directed=False)
    return [sel[lab == i] for i in range(n)]


def petle_brzegowe(F, fidx):
    """Skierowane petle brzegu obszaru (obszar po lewej stronie krawedzi)."""
    de = set()
    for f in F[fidx]:
        de |= {(int(f[0]), int(f[1])), (int(f[1]), int(f[2])), (int(f[2]), int(f[0]))}
    bd = [e for e in de if (e[1], e[0]) not in de]
    nxt = collections.defaultdict(list)
    for a, b in bd: nxt[a].append(b)
    uzyte, petle = set(), []
    for e0 in bd:
        if e0 in uzyte: continue
        petla = [e0[0]]; cur = e0; uzyte.add(e0)
        while True:
            kand = [x for x in nxt[cur[1]] if (cur[1], x) not in uzyte]
            if not kand: break
            petla.append(cur[1]); cur = (cur[1], kand[0]); uzyte.add(cur)
            if cur[1] == e0[0]: break
        petle.append(petla)
    return sorted([p for p in petle if len(p) >= 3], key=len, reverse=True)


def uklad(d):
    """Ortonormalny uklad (d, u, v)."""
    d = np.asarray(d, float); d = d / np.linalg.norm(d)
    a = np.array([0., 0., 1.]) if abs(d[2]) < 0.9 else np.array([1., 0., 0.])
    u = np.cross(d, a); u /= np.linalg.norm(u)
    return d, u, np.cross(d, u)


def kierunek_obszaru(m, fidx):
    """Usredniona normalna obszaru, zwrocona W GLAB bryly."""
    w = (m.face_normals[fidx] * m.area_faces[fidx][:, None]).sum(0)
    return -w / np.linalg.norm(w)


def odsun_do_srodka(P2, d):
    """Przesuniecie wierzcholkow wielokata do srodka o d [mm] (dwusieczne)."""
    n = len(P2)
    A = sum(P2[i, 0] * P2[(i + 1) % n, 1] - P2[(i + 1) % n, 0] * P2[i, 1] for i in range(n))
    zn = 1.0 if A > 0 else -1.0
    out = np.zeros_like(P2)
    for i in range(n):
        p, pm, pp = P2[i], P2[i - 1], P2[(i + 1) % n]
        def nrm(e):
            # normalna do wnetrza: dla obiegu CCW (pole > 0) wnetrze jest PO LEWEJ
            l = np.linalg.norm(e)
            return np.array([-e[1], e[0]]) / l * zn if l > 1e-12 else np.zeros(2)
        n1, n2 = nrm(p - pm), nrm(pp - p)
        # punkt odsuniety o d od OBU krawedzi lezy na dwusiecznej:
        # p + d*(n1+n2)/(1+n1.n2)  (dla n1==n2 wychodzi zwykle p + d*n)
        mian = 1.0 + float(n1 @ n2)
        out[i] = p + d * (n1 + n2) / mian if mian > 0.2 else p + d * n2
    return out


def czop(m, fidx, d, glebokosc, zbieznosc=0.0):
    """Bryla: powierzchnia obszaru + scianki wzdluz d + plaska podstawa.
    `zbieznosc` zwezaja podstawe (czop), 0 = gniazdo w korpusie."""
    V, F = m.vertices, m.faces
    d, u, v = uklad(d)
    petle = petle_brzegowe(F, fidx)
    t = V @ d
    t_cut = max(t[np.array(L)].max() for L in petle) + glebokosc

    wier, sci, poly = [V], [F[fidx]], []
    baza = len(V)
    for L in petle:
        Li = np.array(L)
        P2 = np.stack([V[Li] @ u, V[Li] @ v], 1)
        P2 = odsun_do_srodka(P2, zbieznosc) if zbieznosc > 0 else P2
        Q = P2[:, 0:1] * u + P2[:, 1:2] * v + t_cut * d
        b = baza + sum(len(x) for x in poly); n = len(Li)
        w = []
        for i in range(n):
            a, bb = Li[i], Li[(i + 1) % n]
            qa, qb = b + i, b + (i + 1) % n
            w += [[a, qa, qb], [a, qb, bb]]
        wier.append(Q); sci.append(np.array(w)); poly.append(P2)

    allp = np.concatenate(poly); rings = np.cumsum([len(p) for p in poly])
    sci.append(earcut.triangulate_float64(allp, rings).reshape(-1, 3) + baza)

    M = trimesh.Trimesh(vertices=np.concatenate(wier),
                        faces=np.concatenate(sci), process=True)
    trimesh.repair.fix_normals(M)
    if M.volume < 0: M.invert()
    return M


def pryzma_xy(P, z0, z1):
    """Pionowa pryzma z wielokata shapely."""
    pr = trimesh.creation.extrude_polygon(P, height=z1 - z0)
    pr.apply_translation([0, 0, z0])
    return pr


def obrys_xy(m, fidx, wygladz=0.02):
    """Czysty obrys obszaru w rzucie XY (suma rzutow trojkatow)."""
    tr = [Polygon(m.vertices[m.faces[f]][:, :2]) for f in fidx]
    P = unary_union([t for t in tr if t.is_valid and t.area > 1e-9])
    P = P.buffer(wygladz).buffer(-wygladz)
    if isinstance(P, MultiPolygon): P = max(P.geoms, key=lambda g: g.area)
    return Polygon(P.exterior)


def bool_op(op, meshes):
    return getattr(trimesh.boolean, op)(meshes, engine='manifold')


def polprzestrzen(z, gora):
    """Duzy szescian obcinajacy wszystko powyzej / ponizej plaszczyzny z."""
    b = trimesh.creation.box(extents=(300, 300, 300))
    b.apply_translation([0, 0, z + 150 if gora else z - 150])
    return b


def najwieksza_bryla(m):
    """Odrzuca okruchy (bryly < 1% objetosci) powstale przy erozji obrysu."""
    b = m.split(only_watertight=False)
    return m if len(b) <= 1 else max(b, key=lambda x: x.volume)


# ---------- 3. podzial modelu ----------
def podziel(zrodlo):
    V, F, S = wczytaj_3mf(zrodlo)
    m = trimesh.Trimesh(vertices=V, faces=F, process=False)
    assert m.is_watertight, 'model zrodlowy nie jest szczelny'
    print(f'model: {len(F)} trojkatow, {m.volume:.1f} mm3, '
          f'gabaryt {np.round(m.extents,2)}')

    sk = lambda st: skladowe(m, S == st)
    dziob  = [c for c in sk(4) if len(c) > 1000][0]
    stopy  = sorted([c for c in sk(4) if len(c) < 1000],
                    key=lambda c: V[F[c]].reshape(-1, 3)[:, 0].mean())
    oczy   = sorted(sk(3), key=lambda c: V[F[c]].reshape(-1, 3)[:, 0].mean())
    zrenice= sorted([c for c in sk(2) if len(c) == 7],
                    key=lambda c: V[F[c]].reshape(-1, 3)[:, 0].mean())
    wlosy  = [c for c in sk(2) if 600 < len(c) < 800][0]
    # nozdrza: dwie male zolte latki WEWNATRZ dzioba - za male na osobna czesc,
    # wchlaniamy je do dzioba (zostaja jako zaglebienia, tylko w kolorze dzioba)
    nozdrza = [c for c in sk(0) if 40 <= len(c) <= 45
               and V[F[c]].reshape(-1, 3)[:, 1].mean() < -3]

    # --- czesci wypukle (czop + gniazdo) ---
    OBSZARY = [
        ('dziob',  np.concatenate([dziob] + nozdrza), KIER_DZIOB,             GL_DZIOB, 'kremowy'),
        ('oko-L',  np.concatenate([oczy[0], zrenice[0]]), kierunek_obszaru(m, oczy[0]), GL_OKO, 'bialy'),
        ('oko-P',  np.concatenate([oczy[1], zrenice[1]]), kierunek_obszaru(m, oczy[1]), GL_OKO, 'bialy'),
        ('wlosy',  wlosy, (0, 0, -1),                                          GL_WLOSY, 'czarny'),
    ]
    czesci, gniazda = {}, []
    for nazwa, fidx, d, gl, kolor in OBSZARY:
        p = czop(m, fidx, d, gl, zbieznosc=LUZ)
        g = czop(m, fidx, d, gl, zbieznosc=0.0)
        assert p.is_watertight and g.is_watertight, f'{nazwa}: bryla nieszczelna'
        czesci[nazwa] = (p, kolor, np.asarray(uklad(d)[0]))
        gniazda.append(g)
        print(f'  {nazwa:8s} {p.volume:7.2f} mm3  gabaryt {np.round(p.extents,2)}')

    # --- stopy (boolean: obrys XY, od GL_STOPA pod szwem do Z_STOPA_GORA) ---
    for nazwa, fidx in (('stopa-L', stopy[0]), ('stopa-P', stopy[1])):
        P = obrys_xy(m, fidx)
        zb = Z_SZWU - GL_STOPA
        g = najwieksza_bryla(bool_op('intersection', [m, pryzma_xy(P, zb, Z_STOPA_GORA)]))
        p = najwieksza_bryla(bool_op('intersection', [m, pryzma_xy(P.buffer(-LUZ), zb, Z_STOPA_GORA)]))
        assert g.is_watertight and p.is_watertight, f'{nazwa}: bryla nieszczelna'
        czesci[nazwa] = (p, 'kremowy', np.array([0., 0., -1.]))
        gniazda.append(g)
        print(f'  {nazwa:8s} {p.volume:7.2f} mm3  gabaryt {np.round(p.extents,2)}')

    # --- korpus bez wszystkich wnek, rozciety na szwie ---
    korpus = bool_op('difference', [m] + gniazda)
    assert korpus.is_watertight, 'korpus po odjeciu wnek nie jest szczelny'
    gora = najwieksza_bryla(bool_op('intersection', [korpus, polprzestrzen(Z_SZWU, True)]))
    dol  = najwieksza_bryla(bool_op('intersection', [korpus, polprzestrzen(Z_SZWU, False)]))
    czesci['cialo']       = (gora, 'zolty',  np.array([0., 0., -1.]))
    czesci['baza-keycap'] = (dol,  'czarny', np.array([0., 0.,  1.]))
    print(f'  cialo    {gora.volume:8.2f} mm3   baza-keycap {dol.volume:7.2f} mm3')

    # --- kontrola: kazda czesc szczelna i jednolita, zadne dwie sie nie przenikaja ---
    import itertools
    for n, (p, k, d) in czesci.items():
        assert p.is_watertight,  f'{n}: bryla nieszczelna'
        assert p.body_count == 1, f'{n}: {p.body_count} rozlacznych bryl'
    for a, b in itertools.combinations(czesci, 2):
        pa, pb = czesci[a][0], czesci[b][0]
        if (pa.bounds[0] > pb.bounds[1]).any() or (pb.bounds[0] > pa.bounds[1]).any():
            continue
        v = bool_op('intersection', [pa, pb]).volume
        assert v < 1e-3, f'kolizja {a} x {b}: {v:.3f} mm3 - czesci nie zloza sie'
    print('  kontrola: wszystkie czesci szczelne, brak kolizji')
    return czesci


# ---------- 4. orientacja do druku + ulozenie na plycie ----------
def ustaw_do_druku(mesh, d):
    """Obraca bryle tak, by plaska podstawa (koniec kierunku d) legla na stole."""
    M = mesh.copy()
    R = trimesh.geometry.align_vectors(d, [0, 0, -1])
    M.apply_transform(R)
    M.apply_translation([-M.centroid[0], -M.centroid[1], -M.bounds[0][2]])
    return M


def ulozenie(czesci):
    """Grupuje czesci kolorami w kolumny i zwraca pozycje na plycie."""
    grupy = collections.OrderedDict()
    for n, (msh, kol, d) in czesci.items(): grupy.setdefault(kol, []).append(n)
    kol_szer = {}
    for kol, ns in grupy.items():
        kol_szer[kol] = max(czesci[n][0].extents[0] for n in ns)
    calosc = sum(kol_szer.values()) + ODSTEP * (len(grupy) - 1)
    x = SRODEK[0] - calosc / 2
    poz = {}
    for kol, ns in grupy.items():
        ns = sorted(ns, key=lambda n: -czesci[n][0].extents[1])
        wys = sum(czesci[n][0].extents[1] for n in ns) + ODSTEP * (len(ns) - 1)
        y = SRODEK[1] - wys / 2
        for n in ns:
            e = czesci[n][0].extents
            poz[n] = (x + kol_szer[kol] / 2, y + e[1] / 2)
            y += e[1] + ODSTEP
        x += kol_szer[kol] + ODSTEP
    return poz


# ---------- 5. zapis 3MF dla Bambu Studio ----------
SZABLON_CT = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
 <Default Extension="png" ContentType="image/png"/>
</Types>'''
SZABLON_RELS = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>'''


def zapisz_3mf(czesci, poz, cel, ustawienia=None):
    obj, itm, cfg = [], [], []
    for i, (nazwa, (msh, kolor, d)) in enumerate(czesci.items(), start=1):
        M = ustaw_do_druku(msh, d)
        vs = '\n'.join(f'     <vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>'
                       for x, y, z in M.vertices)
        ts = '\n'.join(f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>'
                       for a, b, c in M.faces)
        obj.append(f'  <object id="{i}" type="model">\n   <mesh>\n'
                   f'    <vertices>\n{vs}\n    </vertices>\n'
                   f'    <triangles>\n{ts}\n    </triangles>\n   </mesh>\n  </object>')
        px, py = poz[nazwa]
        itm.append(f'  <item objectid="{i}" transform="1 0 0 0 1 0 0 0 1 '
                   f'{px:.4f} {py:.4f} 0" printable="1"/>')
        cfg.append(f'  <object id="{i}">\n'
                   f'    <metadata key="name" value="{nazwa}"/>\n'
                   f'    <metadata key="extruder" value="{KOLORY[kolor]}"/>\n'
                   f'    <part id="1" subtype="normal_part">\n'
                   f'      <metadata key="name" value="{nazwa}"/>\n'
                   f'      <metadata key="matrix" value="1 0 0 0 1 0 0 0 1 0 0 0"/>\n'
                   f'    </part>\n  </object>')
    inst = '\n'.join(f'    <model_instance>\n'
                     f'      <metadata key="object_id" value="{i}"/>\n'
                     f'      <metadata key="instance_id" value="0"/>\n'
                     f'    </model_instance>' for i in range(1, len(czesci) + 1))
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
             'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021">\n'
             ' <metadata name="Application">skrypt podzial_kolorow.py</metadata>\n'
             ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
             ' <resources>\n' + '\n'.join(obj) + '\n </resources>\n'
             ' <build>\n' + '\n'.join(itm) + '\n </build>\n</model>')
    conf = ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n' + '\n'.join(cfg) +
            '\n  <plate>\n    <metadata key="plater_id" value="1"/>\n'
            '    <metadata key="plater_name" value="Psyduck - podzial na kolory"/>\n'
            '    <metadata key="locked" value="false"/>\n' + inst + '\n  </plate>\n</config>')
    with zipfile.ZipFile(cel, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', SZABLON_CT)
        z.writestr('_rels/.rels', SZABLON_RELS)
        z.writestr('3D/3dmodel.model', model)
        z.writestr('Metadata/model_settings.config', conf)
        if ustawienia: z.writestr('Metadata/project_settings.config', ustawienia)


# ---------- main ----------
if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    zrodlo = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'psyduck_keycap.3mf')
    czesci = podziel(zrodlo)
    poz = ulozenie(czesci)

    stl_dir = os.path.join(here, '..', 'stl'); os.makedirs(stl_dir, exist_ok=True)
    nry = {'zolty': '1', 'czarny': '2', 'bialy': '3', 'kremowy': '4'}
    for nazwa, (msh, kolor, d) in czesci.items():
        M = ustaw_do_druku(msh, d)
        M.export(os.path.join(stl_dir, f'{nry[kolor]}-{kolor}-{nazwa}.stl'))

    ust = None
    with zipfile.ZipFile(zrodlo) as z:
        if 'Metadata/project_settings.config' in z.namelist():
            ust = z.read('Metadata/project_settings.config').decode('utf-8')
    cel = os.path.join(here, '..', 'slicer', 'psyduck-plyta-podzielona.3mf')
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    zapisz_3mf(czesci, poz, cel, ust)

    print('\nulozenie na plycie (X, Y):')
    for n, (x, y) in sorted(poz.items()): print(f'  {n:12s} ({x:6.1f}, {y:6.1f})')
    print(f'\nzapisano: {len(czesci)} STL + {os.path.basename(cel)}')
