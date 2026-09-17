#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rozbicie malowanego wielokolorowo modelu 3MF (Bambu Studio) na osobne czesci,
z ktorych kazda jest jednolita kolorystycznie - zeby drukowac bez zmian filamentu
i bez wiezy czyszczacej.

Model wejsciowy: "Penguin keycap" (Melodybox, MakerWorld) - pingwin na trzonku MX,
malowany 3 kolorami (czarny / bialy / zolty) przez `paint_color` w 3MF.

IDEA CIECIA
-----------
Kolory w 3MF to malowanie POWIERZCHNI, nie bryly. Zeby z tego zrobic czesci do
druku, kazda plama koloru zamieniam na "wtopke" (plug): bryle ograniczona z przodu
oryginalna powierzchnia modelu, a z tylu plaska plaszczyzna. Korpus dostaje
dokladnie dopasowane gniazdo.

Realizacja: dla kazdej plamy licze jej CIEN (rzut na plaszczyzne XZ, wzdluz osi Y
- pingwin patrzy w -Y). Cien wyciagniety w rure wzdluz Y i przeciety polprzestrzenia
{y <= -s0} daje obszar ciecia. Dalej wystarcza boolean:
    korpus  = bryla - suma(obszarow ciecia)
    wtopka  = obszar ciecia (zmniejszony o luz) * bryla
Taki podzial jest DOKLADNY (suma objetosci czesci = objetosc bryly minus luzy),
bo obszary ciecia nie zachodza na siebie.

Dlaczego rzut wzdluz Y: wszystkie kolorowe plamy sa na przodzie modelu. Dla bialej
plamy tylko 3% powierzchni ma normalna odchylona od -Y bardziej niz 84 stopnie, wiec
rzut jest praktycznie jednoznaczny. Dla stop i dzioba jest gorzej (zawijaja sie),
ale cien liczony jako SUMA rzutow trojkatow (a nie z konturu brzegu) radzi sobie
i z tym - obejmuje cala "sylwetke" plamy.

WYNIK: 7 czesci (5 obowiazkowych + 2 opcjonalne oczy), wszystkie na jednej plycie.

Uruchomienie:
    python3 podziel_na_kolory.py <plik.3mf> <katalog_wyjsciowy>

Wymaga: numpy, scipy, manifold3d
"""

import collections
import os
import sys
import time
import zipfile

import numpy as np

# ----------------------------------------------------------------------------
# PARAMETRY  (wszystko w mm)
# ----------------------------------------------------------------------------
GRUB_MIN        = 0.9    # min. grubosc wtopki w najplytszym miejscu plamy
GRUB_MIN_OKO    = 1.2    # to samo dla oczu (osobne, plytsze gniazda w bialym froncie)
LUZ             = 0.10   # luz boczny wtopki wzgledem gniazda (na strone)
LUZ_DNO         = 0.15   # szczelina na klej na dnie gniazda
Z_NAD_BAZA      = 0.10   # ile ponad gorna plaszczyzna bazy keycapa zaczyna sie ciecie
MIN_POLE_PLAMY  = 1.0    # mm2 - mniejsze plamy malowania scalam z otoczeniem (szum)
MIN_OBJ_BRYLY   = 0.05   # mm3 - mniejsze bryly (odpryski z booleanow) wyrzucam
PLYTA           = (256.0, 256.0)   # pole robocze Bambu Lab A1
# Tryb "kolejnosc druku: po obiekcie" wymaga rozsuniecia czesci - glowica objezdza
# to, co juz wydrukowane. Dla A1: extruder_clearance_max_radius = 73 mm,
# extruder_clearance_height_to_rod = 25 mm (powyzej tej wysokosci grozi zahaczenie
# belka). Dlatego siatka z duzym skokiem, a najwyzsza czesc drukowana na koniec.
SKOK_SIATKI     = 80.0   # odstep osi czesci na plycie (tryb "po obiekcie")
KOLUMNY         = 3      # ile czesci w rzedzie (od lewej do prawej)
# Kolejnosc druku = kolejnosc na tej liscie = kolejnosc obiektow w 3MF.
# Pogrupowana kolorami (zolty -> bialy -> czarny), wiec tylko 2 zmiany filamentu,
# a korpus (najwyzszy, 34 mm) jest ostatni.
KOLEJNOSC_DRUKU = ["dziob", "stopa-L", "stopa-P", "front", "oko-L", "oko-P", "korpus"]
UPROSZCZ_KONTUR = 0.01   # uproszczenie konturu cienia (Douglas-Peucker)
UPROSZCZ_SIATKE = 0.01   # mm - dopuszczalne odchylenie przy upraszczaniu siatki (0 = bez)
# mapowanie kodu paint_color -> numer filamentu w Bambu Studio
KOD_NA_FILAMENT = {"": 1, "4": 1, "8": 2, "0C": 3}
FILAMENT_OPIS   = {1: ("czarny", "#000000"), 2: ("bialy", "#FFFFFF"), 3: ("zolty", "#F4EE2A")}
FAR             = 60.0   # dlugosc rury ciecia (musi przekroczyc gabaryt modelu)


# ----------------------------------------------------------------------------
# 1. WCZYTANIE 3MF
# ----------------------------------------------------------------------------
def macierz_3mf(txt):
    """3MF trzyma transformacje jako 12 liczb wierszowo; punkt mnozony z lewej: p' = p*M + t."""
    v = [float(x) for x in txt.split()]
    M = np.eye(4)
    M[:3, :3] = np.array(v[:9]).reshape(3, 3)
    M[3, :3] = v[9:]
    return M


def zastosuj(P, M):
    return P @ M[:3, :3] + M[3, :3]


def czytaj_model(strumien):
    """Szybki parser liniowy - lxml na pliku 150 MB jest o dwa rzedy wielkosci wolniejszy."""
    obiekty, cur, V, F, C = {}, None, [], [], []
    for raw in strumien:
        s = raw.decode("utf-8", "replace").lstrip() if isinstance(raw, bytes) else raw.lstrip()
        if s.startswith("<vertex "):
            p = s.split('"')
            V.append((float(p[1]), float(p[3]), float(p[5])))
        elif s.startswith("<triangle "):
            p = s.split('"')
            F.append((int(p[1]), int(p[3]), int(p[5])))
            C.append(p[7] if len(p) > 8 else "")
        elif s.startswith("<object "):
            cur, V, F, C = s.split('"')[1], [], [], []
        elif s.startswith("</object>"):
            obiekty[cur] = (np.array(V), np.array(F, dtype=np.int64), np.array(C))
    return obiekty


def czytaj_3mf(sciezka):
    """Zwraca (P_model, F_model, filament_na_twarz, P_baza, F_baza) w ukladzie plyty."""
    with zipfile.ZipFile(sciezka) as z:
        glowny = z.read("3D/3dmodel.model").decode("utf-8", "replace")
        sub = [n for n in z.namelist() if n.startswith("3D/Objects/") and n.endswith(".model")]
        if not sub:
            raise SystemExit("3MF bez 3D/Objects/*.model - nieobslugiwany wariant")
        with z.open(sub[0]) as fh:
            obiekty = czytaj_model(fh)

    # komponenty i transformacje z glownego 3dmodel.model
    komp = []
    for linia in glowny.splitlines():
        s = linia.strip()
        if s.startswith("<component "):
            oid = s.split('objectid="')[1].split('"')[0]
            tr = s.split('transform="')[1].split('"')[0] if 'transform="' in s else None
            komp.append((oid, macierz_3mf(tr) if tr else np.eye(4)))
        elif s.startswith("<item "):
            tr = s.split('transform="')[1].split('"')[0] if 'transform="' in s else None
            budowa = macierz_3mf(tr) if tr else np.eye(4)
    if len(komp) < 2:
        raise SystemExit("oczekiwano 2 komponentow (pingwin + baza keycapa)")

    czesci = []
    for oid, M in komp:
        V, F, C = obiekty[oid]
        czesci.append((zastosuj(zastosuj(V, M), budowa), F, C))
    # wieksza siatka = model malowany, mniejsza = baza keycapa
    czesci.sort(key=lambda t: -len(t[1]))
    (Pm, Fm, Cm), (Pb, Fb, _) = czesci[0], czesci[1]

    fil = np.array([KOD_NA_FILAMENT.get(c, 1) for c in Cm], dtype=np.int64)

    # obrot 180 stopni wokol X - w pliku model stoi glowa w dol (tak byl ciety na plyte)
    R = np.diag([1.0, -1.0, -1.0])
    Pm, Pb = Pm @ R, Pb @ R
    # przod modelu na -Y: kierunek = od srodka bryly do srodka bialej plamy
    fd = Pm[Fm[fil == 2].ravel()].mean(0)[:2] - Pm.mean(0)[:2]
    fd /= np.linalg.norm(fd)
    ang = np.arctan2(fd[1], fd[0]) + np.pi / 2
    c, s = np.cos(-ang), np.sin(-ang)
    Rz = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1.0]])
    Pm, Pb = Pm @ Rz, Pb @ Rz
    # baza na z=0, calosc wysrodkowana w XY
    A = np.vstack([Pm, Pb])
    off = np.array([(A[:, 0].min() + A[:, 0].max()) / 2,
                    (A[:, 1].min() + A[:, 1].max()) / 2, A[:, 2].min()])
    return Pm - off, Fm, fil, Pb - off, Fb


# ----------------------------------------------------------------------------
# 2. NAPRAWA SIATKI  (Image-to-3D zostawia mikroskopijne platki i dziury)
# ----------------------------------------------------------------------------
def kraw_skierowane(F):
    return np.stack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]], 1).reshape(-1, 2)


def licznik_kraw(F, nv):
    D = kraw_skierowane(F)
    k = np.minimum(D[:, 0], D[:, 1]).astype(np.int64) * nv + np.maximum(D[:, 0], D[:, 1])
    uk, inv, cnt = np.unique(k, return_inverse=True, return_counts=True)
    return D, uk, inv, cnt


def napraw(P, F, lab):
    """Usuwa twarze przy krawedziach uzywanych != 2 razy i lata powstale petle wachlarzem."""
    F = F.astype(np.int64)
    lab = lab.copy()
    nv = len(P)
    for it in range(15):
        D, uk, inv, cnt = licznik_kraw(F, nv)
        zle = (cnt[inv].reshape(-1, 3) != 2).any(1)
        if not zle.any():
            break
        F, lab = F[~zle], lab[~zle]
        D, uk, inv, cnt = licznik_kraw(F, nv)
        brzeg = cnt[inv] == 1
        if not brzeg.any():
            continue
        de, dface = D[brzeg], (np.arange(len(D)) // 3)[brzeg]
        nastepnik, twarz_kraw = {}, {}
        for (a, b), fi in zip(de, dface):
            nastepnik.setdefault(int(a), []).append(int(b))
            twarz_kraw[(int(a), int(b))] = int(fi)
        petle = []
        for a0 in list(nastepnik):
            while nastepnik.get(a0):
                petla, a, ok = [a0], a0, True
                while True:
                    if not nastepnik.get(a):
                        ok = False
                        break
                    b = nastepnik[a].pop()
                    if b == a0:
                        break
                    if b in petla:
                        ok = False
                        break
                    petla.append(b)
                    a = b
                if ok and len(petla) >= 3:
                    petle.append(petla)
        nowe_F, nowe_L, nowe_P = [], [], []
        for petla in petle:
            ci = nv + len(nowe_P)
            nowe_P.append(P[petla].mean(0))
            gl = [lab[twarz_kraw[(petla[i], petla[(i + 1) % len(petla)])]]
                  for i in range(len(petla)) if (petla[i], petla[(i + 1) % len(petla)]) in twarz_kraw]
            L = collections.Counter(gl).most_common(1)[0][0] if gl else 1
            for i in range(len(petla)):
                a, b = petla[i], petla[(i + 1) % len(petla)]
                nowe_F.append((b, a, ci))      # przeciwnie do krawedzi brzegowej
                nowe_L.append(L)
        if nowe_P:
            P = np.vstack([P, np.array(nowe_P)])
            nv = len(P)
            F = np.vstack([F, np.array(nowe_F, dtype=np.int64)])
            lab = np.concatenate([lab, np.array(nowe_L, dtype=lab.dtype)])
    # zostaw tylko najwieksza skorupe (przez krawedzie) i przenumeruj wierzcholki
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    D, uk, inv, cnt = licznik_kraw(F, len(P))
    o = np.argsort(inv, kind="stable")
    fi = (np.arange(len(D)) // 3)[o]
    A = coo_matrix((np.ones(len(fi) // 2), (fi[0::2], fi[1::2])), shape=(len(F), len(F)))
    nc, fc = connected_components(A, directed=False)
    tri = P[F]
    obj = np.einsum("ij,ij->i", tri[:, 0], np.cross(tri[:, 1], tri[:, 2])) / 6
    naj = np.argmax(np.abs(np.bincount(fc, weights=obj, minlength=nc)))
    m = fc == naj
    uzyte, inv2 = np.unique(F[m], return_inverse=True)
    return P[uzyte], inv2.reshape(-1, 3), lab[m]


# ----------------------------------------------------------------------------
# 3. PLAMY KOLORU: scalenie szumu + skladowe spojne
# ----------------------------------------------------------------------------
def plamy(P, F, lab):
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    nv = len(P)
    D = kraw_skierowane(F)
    k = np.minimum(D[:, 0], D[:, 1]).astype(np.int64) * nv + np.maximum(D[:, 0], D[:, 1])
    o = np.argsort(k, kind="stable")
    fi = (np.arange(len(D)) // 3)[o]
    fa, fb = fi[0::2], fi[1::2]
    n = np.cross(P[F][:, 1] - P[F][:, 0], P[F][:, 2] - P[F][:, 0])
    pole = 0.5 * np.linalg.norm(n, axis=1)

    def skladowe(lab):
        rowne = lab[fa] == lab[fb]
        A = coo_matrix((np.ones(rowne.sum()), (fa[rowne], fb[rowne])), shape=(len(F), len(F)))
        nc, cid = connected_components(A, directed=False)
        return cid, np.bincount(cid, weights=pole, minlength=nc)

    lab = lab.copy()
    for _ in range(8):
        cid, pola = skladowe(lab)
        male = set(np.where(pola < MIN_POLE_PLAMY)[0].tolist())
        if not male:
            break
        m = np.isin(cid, list(male))
        sel = m[fa] ^ m[fb]
        glosy = collections.defaultdict(collections.Counter)
        for x, y in zip(fa[sel], fb[sel]):
            a, b = (x, y) if m[x] else (y, x)
            glosy[cid[a]][lab[b]] += 1
        if not glosy:
            break
        for c, v in glosy.items():
            lab[cid == c] = v.most_common(1)[0][0]
    cid, pola = skladowe(lab)
    return lab, cid, pola


# ----------------------------------------------------------------------------
# 4. CIECIE
# ----------------------------------------------------------------------------
def buduj_czesci(P, F, lab, cid, pola, Pb, Fb, log=print):
    import manifold3d as m3

    def man(V, T):
        return m3.Manifold(m3.Mesh(vert_properties=V.astype(np.float32), tri_verts=T.astype(np.uint32)))

    bryla = man(P, F) + man(Pb, Fb)
    if bryla.status() != m3.Error.NoError:
        raise SystemExit("bryla nie jest manifoldowa: %s" % bryla.status())
    log("bryla: objetosc %.2f mm3, trojkatow %d" % (bryla.volume(), bryla.num_tri()))

    duze = sorted([c for c in range(len(pola)) if pola[c] >= MIN_POLE_PLAMY], key=lambda c: -pola[c])
    # rozpoznanie plam po kolorze, wielkosci i polozeniu
    srodek = {c: P[F[cid == c].ravel()].mean(0) for c in duze}
    czarne = [c for c in duze if lab[cid == c][0] == 1]
    biale = [c for c in duze if lab[cid == c][0] == 2]
    zolte = [c for c in duze if lab[cid == c][0] == 3]
    if not biale or len(zolte) < 3:
        raise SystemExit("nieoczekiwana struktura kolorow: %d bialych, %d zoltych" % (len(biale), len(zolte)))
    front = biale[0]
    zolte.sort(key=lambda c: -pola[c])
    stopy = sorted(zolte[:2], key=lambda c: srodek[c][0])          # po X: lewa, prawa
    dziob = zolte[2]
    oczy = sorted([c for c in czarne[1:]][:2], key=lambda c: srodek[c][0])
    plamy_map = {"front": front, "dziob": dziob,
                 "stopa-L": stopy[0], "stopa-P": stopy[1]}
    if len(oczy) == 2:
        plamy_map["oko-L"], plamy_map["oko-P"] = oczy[0], oczy[1]

    z_min = Pb[:, 2].max() + Z_NAD_BAZA          # nie tnij w baze keycapa

    def cien(sel):
        """Suma rzutow trojkatow plamy na plaszczyzne (x,z); NonZero + orientacja CCW."""
        T = P[F[sel]][:, :, [0, 2]]
        a, b = T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]
        s = a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]
        T[s < 0] = T[s < 0][:, ::-1]
        cs = m3.CrossSection([t for t in T[np.abs(s) > 1e-12]], m3.FillRule.NonZero)
        return cs.simplify(UPROSZCZ_KONTUR) if UPROSZCZ_KONTUR else cs

    def rura(cs, s0):
        """Obszar {y <= -s0} nad cieniem cs, przyciety do z >= z_min."""
        return (cs.extrude(FAR).rotate([90, 0, 0]).translate([0, -s0, 0])
                  .trim_by_plane([0, 0, 1], z_min))

    sh, s0 = {}, {}
    for nm, c in plamy_map.items():
        sh[nm] = cien(cid == c)
        s_min = (-P[F[cid == c].ravel()][:, 1]).min()
        s0[nm] = s_min - (GRUB_MIN_OKO if nm.startswith("oko") else GRUB_MIN)
        log("  %-7s pole plamy %7.2f mm2, cien %7.2f mm2, dno gniazda y=%6.2f"
            % (nm, pola[c], sh[nm].area(), -s0[nm]))

    # cien frontu: oczy to jego czesc (dostana wlasne, plytsze gniazda),
    # dziob wycinamy - siedzi we wlasnym gniezdzie w korpusie
    if "oko-L" in sh:
        sh["front"] = sh["front"] + sh["oko-L"] + sh["oko-P"]
    sh["front"] = sh["front"] - sh["dziob"]

    gniazdo = {nm: rura(sh[nm], s0[nm]) for nm in sh}
    wtopka = {nm: rura(sh[nm].offset(-LUZ, m3.JoinType.Miter, 2.0, 0), s0[nm] + LUZ_DNO) for nm in sh}

    def oczysc(mf, nazwa):
        """Wyrzuca odpryski booleanow (paperowe bryly z prawie stycznych ciec)."""
        bryly = [b for b in mf.decompose() if b.volume() >= MIN_OBJ_BRYLY]
        if not bryly:
            raise SystemExit("czesc %s wyszla pusta" % nazwa)
        odrzucone = mf.num_tri() - sum(b.num_tri() for b in bryly)
        out = bryly[0]
        for b in bryly[1:]:
            out = out + b
        if len(bryly) > 1 or odrzucone:
            log("  %-7s bryl: %d (odrzucono odpryskow: %d trojkatow)" % (nazwa, len(bryly), odrzucone))
        return out

    wyc = gniazdo["front"] + gniazdo["dziob"] + gniazdo["stopa-L"] + gniazdo["stopa-P"]
    czesci = {"korpus": oczysc(bryla - wyc, "korpus")}
    f = wtopka["front"] ^ bryla
    if "oko-L" in gniazdo:
        f = f - gniazdo["oko-L"] - gniazdo["oko-P"]
    czesci["front"] = oczysc(f, "front")
    for nm in ("dziob", "stopa-L", "stopa-P", "oko-L", "oko-P"):
        if nm in wtopka:
            czesci[nm] = oczysc(wtopka[nm] ^ bryla, nm)

    suma = sum(p.volume() for p in czesci.values())
    log("kontrola: suma czesci %.2f mm3, bryla %.2f mm3, luzy %.2f mm3 (%.2f%%)"
        % (suma, bryla.volume(), bryla.volume() - suma, 100 * (bryla.volume() - suma) / bryla.volume()))
    return czesci, bryla


# ----------------------------------------------------------------------------
# 5. UPROSZCZENIE SIATEK + EKSPORT
# ----------------------------------------------------------------------------
def na_siatke(mf):
    m = mf.to_mesh()
    return np.asarray(m.vert_properties[:, :3], dtype=np.float64), np.asarray(m.tri_verts, dtype=np.int64)


def objetosc(P, F):
    t = P[F]
    return np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6


def uprosc(mf, nazwa, log=print):
    """Upraszczanie siatki w granicach zadanej tolerancji. Model z Image-to-3D ma
       ~0.02 mm na trojkat - przy dyszy 0.4 mm to czysty narzut na pliki i slicer.
       manifold3d.simplify() w przeciwienstwie do zwyklej decymacji kwadrykowej
       gwarantuje, ze wynik zostaje szczelna bryla manifoldowa."""
    if not UPROSZCZ_SIATKE:
        return mf
    s = mf.simplify(UPROSZCZ_SIATKE)
    blad = 100 * abs(s.volume() - mf.volume()) / abs(mf.volume())
    if s.status().name != "NoError" or blad > 1.0:
        log("  %-7s uproszczenie odrzucone (status %s, blad objetosci %.2f%%)" % (nazwa, s.status(), blad))
        return mf
    log("  %-7s siatka %7d -> %6d trojkatow, blad objetosci %.3f%%"
        % (nazwa, mf.num_tri(), s.num_tri(), blad))
    return s


def czysc_siatke(P, F, nazwa, log=print):
    """Domkniecie pliku: zgrzanie wierzcholkow w precyzji float32 (taka ma binarny STL),
       usuniecie trojkatow zdegenerowanych i zdublowanych, zalatanie dziur po nich.
       Bez tego upraszczanie zostawia mikroskopijne drzazgi, ktore slicer widzi jako
       bledy siatki."""
    P32 = P.astype(np.float32).astype(np.float64)
    uq, inv = np.unique(P32, axis=0, return_inverse=True)
    F = inv[F]
    zdeg = (F[:, 0] == F[:, 1]) | (F[:, 1] == F[:, 2]) | (F[:, 0] == F[:, 2])
    klucz = np.sort(F, axis=1)
    _, pierwszy, ile = np.unique(klucz, axis=0, return_index=True, return_counts=True)
    dubel = np.zeros(len(F), dtype=bool)
    if (ile > 1).any():
        powt = np.zeros(len(klucz), dtype=bool)
        _, odw = np.unique(klucz, axis=0, return_inverse=True)
        powt = (ile > 1)[odw]
        dubel = powt                       # cale grupy duplikatow do usuniecia (fin/plewa)
    usun = zdeg | dubel
    if usun.any():
        log("  %-7s czyszczenie: %d zdegenerowanych, %d zdublowanych trojkatow"
            % (nazwa, int(zdeg.sum()), int(dubel.sum())))
    F = F[~usun]
    P, F, _ = napraw(uq, F, np.zeros(len(F), dtype=np.int64))
    return P, F


def domknij(P, F, nazwa, log=print):
    """Powtarza czyszczenie, az siatka jest szczelna w tej samej precyzji, w jakiej
       trafi do pliku (binarny STL to float32)."""
    for _ in range(4):
        P, F = czysc_siatke(P, F, nazwa, log=log)
        if szczelna(P.astype(np.float32).astype(np.float64), F):
            return P.astype(np.float32).astype(np.float64), F
    log("  %-7s UWAGA: nie udalo sie domknac siatki" % nazwa)
    return P, F


def szczelna(P, F):
    """Kazda krawedz uzyta dokladnie 2 razy i w przeciwnych kierunkach.
       Wierzcholki zgrzewane po polozeniu - slicer robi tak samo, wiec dwa osobne
       indeksy w tym samym punkcie to dla niego krawedz niemanifoldowa."""
    uq, inv0 = np.unique(P, axis=0, return_inverse=True)
    P, F = uq, inv0[F]
    if ((F[:, 0] == F[:, 1]) | (F[:, 1] == F[:, 2]) | (F[:, 0] == F[:, 2])).any():
        return False
    D, uk, inv, cnt = licznik_kraw(F, len(P))
    if not (cnt == 2).all():
        return False
    o = np.argsort(inv, kind="stable")
    a, b = D[o][0::2], D[o][1::2]
    return bool(((a[:, 0] == b[:, 1]) & (a[:, 1] == b[:, 0])).all())


def zapisz_stl(sciezka, P, F, nazwa="czesc"):
    t = P[F].astype(np.float32)
    n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    ln = np.linalg.norm(n, axis=1)
    ln[ln == 0] = 1
    n = (n / ln[:, None]).astype(np.float32)
    rek = np.zeros(len(F), dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
    rek["n"], rek["v"] = n, t
    with open(sciezka, "wb") as fh:
        fh.write(("%-80s" % ("wygenerowane: " + nazwa)).encode()[:80])
        fh.write(np.uint32(len(F)).tobytes())
        fh.write(rek.tobytes())


# orientacja druku: "stojaco" = jak w zlozeniu, "tylem" = plaskim tylem wtopki na stol
ORIENTACJA = {"korpus": "stojaco", "stopa-L": "stojaco", "stopa-P": "stojaco",
              "front": "tylem", "dziob": "tylem", "oko-L": "tylem", "oko-P": "tylem"}


def obroc_do_druku(P, nazwa):
    """Korpus i stopy maja plaski spod (baza keycapa / polka pod stopa) - stawiamy je jak
       w zlozeniu. Front, dziob i oczy maja plaski TYL (dno gniazda) - kladziemy je na nim,
       obrot -90 stopni wokol X przenosi +Y (normalna tylu) na -Z. Zadna z czesci nie
       potrzebuje wtedy podpor."""
    if ORIENTACJA.get(nazwa, "tylem") == "stojaco":
        Q = P.copy()
    else:
        Q = np.stack([P[:, 0], P[:, 2], -P[:, 1]], 1)
    Q[:, 2] -= Q[:, 2].min()
    return Q


def kolejnosc(czesci):
    """Kolejnosc druku: wg KOLEJNOSC_DRUKU, reszta (jesli jakas) na koniec."""
    znane = [nm for nm in KOLEJNOSC_DRUKU if nm in czesci]
    return znane + sorted(set(czesci) - set(znane))


def rozmiesc(czesci, log=print):
    """Uklada czesci w rzedach od lewej do prawej, w kolejnosci druku: pierwsza
       czesc lewy-przedni naroznik, potem w prawo, potem rzad dalej od operatora.
       Zwraca {nazwa: (dx, dy)} - samo przesuniecie, bo siatki zostaja przy poczatku
       ukladu (float32 w STL/3MF ma przy x~128 mm osiem razy grubszy krok niz przy
       x~0 i potrafi skleic sasiednie wierzcholki w niemanifoldowa krawedz)."""
    kol = kolejnosc(czesci)
    wiersze = (len(kol) + KOLUMNY - 1) // KOLUMNY
    szer_c = (KOLUMNY - 1) * SKOK_SIATKI
    wys_c = (wiersze - 1) * SKOK_SIATKI
    x0, y0 = (PLYTA[0] - szer_c) / 2, (PLYTA[1] - wys_c) / 2

    przes = {}
    for i, nm in enumerate(kol):
        P = czesci[nm][0]
        cx = x0 + (i % KOLUMNY) * SKOK_SIATKI
        cy = y0 + (i // KOLUMNY) * SKOK_SIATKI
        przes[nm] = (cx - (P[:, 0].min() + P[:, 0].max()) / 2,
                     cy - (P[:, 1].min() + P[:, 1].max()) / 2)
        log("    %d. %-8s -> X %6.1f  Y %6.1f  (filament %d, %s)"
            % (i + 1, nm, cx, cy, FILAMENT_CZESCI.get(nm, 1),
               FILAMENT_OPIS[FILAMENT_CZESCI.get(nm, 1)][0]))
    zajete_x = max(P[:, 0].max() - P[:, 0].min() for P, _ in czesci.values()) + szer_c
    zajete_y = max(P[:, 1].max() - P[:, 1].min() for P, _ in czesci.values()) + wys_c
    if zajete_x > PLYTA[0] - 10 or zajete_y > PLYTA[1] - 10:
        log("UWAGA: uklad %.0f x %.0f mm nie miesci sie na plycie - zmniejsz SKOK_SIATKI"
            % (zajete_x, zajete_y))
    log("uklad: %d kolumn x %d rzedow, skok %.0f mm, zajete ~%.0f x %.0f mm"
        % (KOLUMNY, wiersze, SKOK_SIATKI, zajete_x, zajete_y))
    return przes


FILAMENT_CZESCI = {"korpus": 1, "front": 2, "dziob": 3, "stopa-L": 3, "stopa-P": 3,
                   "oko-L": 1, "oko-P": 1}


def zapisz_3mf(sciezka, czesci, przes):
    """Plyta jako 3MF: siatki lokalne, pozycja w <item transform>, filament na obiekt
       w model_settings.config (rozszerzenie Bambu Studio / Orca).

       Kolejnosc obiektow w pliku = kolejnosc na liscie obiektow w slicerze =
       kolejnosc druku w trybie "po obiekcie". Dlatego obiekty ida w KOLEJNOSC_DRUKU,
       a nie alfabetycznie - inaczej trzeba je potem przeciagac recznie."""
    obj_xml, item_xml, cfg = [], [], []
    for i, nm in enumerate(kolejnosc(czesci), start=1):
        P, F = czesci[nm]
        v = "\n".join('     <vertex x="%.6f" y="%.6f" z="%.6f"/>' % tuple(p) for p in P)
        t = "\n".join('     <triangle v1="%d" v2="%d" v3="%d"/>' % tuple(f) for f in F)
        obj_xml.append('  <object id="%d" type="model">\n   <mesh>\n    <vertices>\n%s\n    </vertices>\n'
                       '    <triangles>\n%s\n    </triangles>\n   </mesh>\n  </object>' % (i, v, t))
        dx, dy = przes[nm]
        item_xml.append('  <item objectid="%d" transform="1 0 0 0 1 0 0 0 1 %.6f %.6f 0" printable="1"/>'
                        % (i, dx, dy))
        cfg.append('  <object id="%d">\n    <metadata key="name" value="%s"/>\n'
                   '    <metadata key="extruder" value="%d"/>\n  </object>'
                   % (i, nm, FILAMENT_CZESCI.get(nm, 1)))
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n'
             ' <metadata name="Application">podziel_na_kolory.py</metadata>\n'
             ' <resources>\n%s\n </resources>\n <build>\n%s\n </build>\n</model>\n'
             % ("\n".join(obj_xml), "\n".join(item_xml)))
    settings = '<?xml version="1.0" encoding="UTF-8"?>\n<config>\n%s\n</config>\n' % "\n".join(cfg)
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
          ' <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
          ' <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
          '</Types>\n')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            ' <Relationship Target="/3D/3dmodel.model" Id="rel-1" '
            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n</Relationships>\n')
    with zipfile.ZipFile(sciezka, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", model)
        z.writestr("Metadata/model_settings.config", settings)


# ----------------------------------------------------------------------------
def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    zrodlo, wyj = sys.argv[1], sys.argv[2]
    os.makedirs(wyj, exist_ok=True)
    t0 = time.time()

    print("1/5 wczytywanie %s" % zrodlo)
    P, F, fil, Pb, Fb = czytaj_3mf(zrodlo)
    print("    model: %d wierzcholkow, %d trojkatow; baza: %d trojkatow" % (len(P), len(F), len(Fb)))
    print("    gabaryt zlozenia: %s mm" % np.round(np.vstack([P, Pb]).max(0) - np.vstack([P, Pb]).min(0), 2))

    print("2/5 naprawa siatki")
    P, F, fil = napraw(P, F, fil)
    print("    po naprawie: %d wierzcholkow, %d trojkatow" % (len(P), len(F)))

    print("3/5 plamy koloru")
    fil, cid, pola = plamy(P, F, fil)
    duze = sorted([c for c in range(len(pola)) if pola[c] >= MIN_POLE_PLAMY], key=lambda c: -pola[c])
    for c in duze:
        print("    plama #%-4d %-7s pole %8.2f mm2" % (c, FILAMENT_OPIS[fil[cid == c][0]][0], pola[c]))

    print("4/5 ciecie na czesci")
    czesci, bryla = buduj_czesci(P, F, fil, cid, pola, Pb, Fb)

    print("5/5 upraszczanie siatek, orientacja, plyta, eksport")
    gotowe = {}
    for nm, mf in czesci.items():
        Pp, Fp = na_siatke(uprosc(mf, nm))
        Pp = obroc_do_druku(Pp, nm)
        Pp[:, 0] -= (Pp[:, 0].min() + Pp[:, 0].max()) / 2      # wysrodkuj w XY,
        Pp[:, 1] -= (Pp[:, 1].min() + Pp[:, 1].max()) / 2      # spodem na z=0
        gotowe[nm] = domknij(Pp, Fp, nm)                       # domykanie na koncu:
                                                               # kazde przesuniecie po
                                                               # nim moze znow skleic
                                                               # wierzcholki w float32
    przes = rozmiesc(gotowe)
    for i, nm in enumerate(kolejnosc(gotowe), start=1):
        Pp, Fp = gotowe[nm]
        nazwa = "%d-%s-%s.stl" % (i, nm, FILAMENT_OPIS[FILAMENT_CZESCI[nm]][0])
        zapisz_stl(os.path.join(wyj, nazwa), Pp, Fp, nazwa)
        print("    %-26s %6d trojkatow  gabaryt %s mm  szczelna=%s"
              % (nazwa, len(Fp), np.round(Pp.max(0) - Pp.min(0), 2), szczelna(Pp, Fp)))
    zapisz_3mf(os.path.join(wyj, "plyta-pingwin-keycap.3mf"), gotowe, przes)
    print("    plyta-pingwin-keycap.3mf  (wszystkie czesci rozstawione na jednej plycie)")
    print("gotowe w %.0f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
