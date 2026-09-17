#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
biblioteka/podzial_mmu.py — narzędzia do rozbierania modeli malowanych MMU
(projekty Bambu Studio / PrusaSlicer .3mf) na osobne bryły, po jednej na kolor.

Po co: druk wielokolorowy na jednej dyszy = zmiana filamentu co warstwę
i wieża czyszcząca. Jak się model rozbierze na części jednokolorowe, drukuje
się je osobno (albo sekwencyjnie „wg obiektu") i skleja — zero odpadu.

Czego tu NIE ma: rozpoznawania, co jest dziobem a co okiem. To jest w skrypcie
konkretnego projektu — biblioteka daje tylko klocki.

Typowy przepływ w skrypcie projektu:

    V, F, S = wczytaj_3mf('model.3mf')          # S = numer filamentu na trójkąt
    m = trimesh.Trimesh(V, F, process=False)
    obszary = skladowe(m, S == 2)               # spójne łaty danego koloru
    czesci['dziob'] = (czop(m, idx, kier, 2.5, zbieznosc=LUZ), 'kremowy', kier)
    kontrola(czesci)                            # szczelność + brak kolizji
    zapisz_3mf(czesci, ulozenie(czesci), 'plyta.3mf', KOLORY)

Jednostki: milimetry.
"""
import os, re, collections, zipfile
import numpy as np, trimesh
import mapbox_earcut as earcut
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

SRODEK_A1 = (128.0, 128.0)   # środek stołu Bambu Lab A1 (256 x 256 mm)

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



# ---------- 4. orientacja do druku + ulozenie na plycie ----------
def ustaw_do_druku(mesh, d):
    """Obraca bryle tak, by plaska podstawa (koniec kierunku d) legla na stole."""
    M = mesh.copy()
    R = trimesh.geometry.align_vectors(d, [0, 0, -1])
    M.apply_transform(R)
    M.apply_translation([-M.centroid[0], -M.centroid[1], -M.bounds[0][2]])
    return M


def ulozenie(czesci, odstep=6.0, srodek=SRODEK_A1):
    """Grupuje czesci kolorami w kolumny i zwraca pozycje (x, y) na plycie."""
    grupy = collections.OrderedDict()
    for n, (msh, kol, d) in czesci.items(): grupy.setdefault(kol, []).append(n)
    kol_szer = {}
    for kol, ns in grupy.items():
        kol_szer[kol] = max(czesci[n][0].extents[0] for n in ns)
    calosc = sum(kol_szer.values()) + odstep * (len(grupy) - 1)
    x = srodek[0] - calosc / 2
    poz = {}
    for kol, ns in grupy.items():
        ns = sorted(ns, key=lambda n: -czesci[n][0].extents[1])
        wys = sum(czesci[n][0].extents[1] for n in ns) + odstep * (len(ns) - 1)
        y = srodek[1] - wys / 2
        for n in ns:
            e = czesci[n][0].extents
            poz[n] = (x + kol_szer[kol] / 2, y + e[1] / 2)
            y += e[1] + odstep
        x += kol_szer[kol] + odstep
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


def zapisz_3mf(czesci, poz, cel, kolory, ustawienia=None):
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
                   f'    <metadata key="extruder" value="{kolory[kolor]}"/>\n'
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




def kontrola(czesci):
    """Sprawdza to, czego sama szczelnosc nie wychwyci: czy kazda czesc jest
    w jednym kawalku i czy zadne dwie sie nie przenikaja. Przenikanie = zestawu
    fizycznie nie da sie zlozyc, a wyglada poprawnie na renderze."""
    import itertools
    for n, (p, k, d) in czesci.items():
        assert p.is_watertight,   f'{n}: bryla nieszczelna'
        assert p.body_count == 1, f'{n}: {p.body_count} rozlacznych bryl'
    for a, b in itertools.combinations(czesci, 2):
        pa, pb = czesci[a][0], czesci[b][0]
        if (pa.bounds[0] > pb.bounds[1]).any() or (pb.bounds[0] > pa.bounds[1]).any():
            continue
        v = bool_op('intersection', [pa, pb]).volume
        assert v < 1e-3, f'kolizja {a} x {b}: {v:.3f} mm3 - czesci nie zloza sie'
    print('  kontrola: wszystkie czesci szczelne, w jednym kawalku, brak kolizji')


def eksportuj_stl(czesci, katalog, kolory):
    """Zapisuje kazda czesc jako STL w orientacji druku, z prefiksem slotu AMS."""
    os.makedirs(katalog, exist_ok=True)
    for nazwa, (msh, kolor, d) in czesci.items():
        ustaw_do_druku(msh, d).export(
            os.path.join(katalog, f'{kolory[kolor]}-{kolor}-{nazwa}.stl'))


def ustawienia_zrodla(zrodlo):
    """Wyciaga project_settings.config ze zrodlowego 3MF (kolory filamentow,
    profil procesu), zeby przeniesc je do wynikowej plyty."""
    with zipfile.ZipFile(zrodlo) as z:
        n = 'Metadata/project_settings.config'
        return z.read(n).decode('utf-8') if n in z.namelist() else None
