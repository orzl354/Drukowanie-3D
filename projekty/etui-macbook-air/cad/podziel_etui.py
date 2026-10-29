#!/usr/bin/env python3
"""
Podział etui MacBook Air 13" (ByteSlinger, MakerWorld) na części mieszczące się
na Bambu Lab A1 (256 × 256 mm).

Oryginał ma 315 × 241 mm, więc dno i pokrywa są przecinane płaszczyzną
prostopadłą do długiego boku. Złącze:
  * 4 "motylki" (klucze w kształcie muszki / bow-tie) wpuszczone od środka
    w dno i w pokrywę — zlicowane z powierzchnią, ciągną połówki do siebie
    i trzymają je w jednej płaszczyźnie,
  * kołki z filamentu 1,75 mm (kawałki szpuli) w dnie i w ściankach —
    ustawiają połówki względem siebie podczas klejenia,
  * mikrofaza 45° na zewnętrznych krawędziach cięcia — zamiast "prawie
    równego" styku powstaje cienka, równa linia (i znika problem stopy słonia).

Użycie:
    pip install numpy trimesh manifold3d shapely networkx
    python3 podziel_etui.py MacBookAirCase.3mf katalog_wyjsciowy/

Wszystkie wymiary w mm. Układ współrzędnych = układ siatek z pliku 3mf:
  X – długi bok (315), Y – wysokość (dno: +Y do środka, pokrywa: -Y do środka),
  Z – głębokość (241), zawiasy przy Z ≈ -115, zamek przy Z ≈ +118.
"""
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import trimesh
from shapely.affinity import translate
from shapely.geometry import Polygon

# ───────────────────────── PARAMETRY ─────────────────────────

# Położenie cięcia na osi X. Środek (0) odpada: tam jest środkowy zawias
# (|x| < 15) i zatrzask pokrywy. Kanał zamka w dnie zajmuje x ∈ [-35, 90].
# -52.5 → części 105 + 210 mm (proporcja 1/3 : 2/3) i 17 mm zapasu od kanału.
CIECIE_X = -52.5

# Mikrofaza na zewnętrznych krawędziach styku (0 = wyłączona)
FAZA_SZWU = 0.3

# ── Motylki (bow-tie) ──
MOTYL_DLUGOSC = 30.0      # w poprzek szwu (po 15 mm na każdą połówkę)
MOTYL_SZEROKOSC = 16.0    # szerokość końców
MOTYL_TALIA = 8.0         # szerokość w przewężeniu (na linii szwu)
MOTYL_PROMIEN = 0.6       # zaokrąglenie naroży klucza (gniazdo ma ostre naroża z dyszy)
LUZ_MOTYLA = 0.15         # luz na stronę: pasowanie pod klej (ciasne, 0.1–0.15)
MOTYL_POZYCJE_Z = (-80.0, -27.0, 27.0, 80.0)

# Głębokość gniazda i grubość klucza. Klucz o 0.1 cieńszy → nigdy nie wystaje
# ponad powierzchnię (wystający klucz dociskałby laptopa).
DNO_GNIAZDO = 2.6         # dno ma 5.3 mm → zostaje 2.7 mm pod gniazdem
POKRYWA_GNIAZDO = 2.4     # pokrywa ma 5.0 mm → zostaje 2.6 mm
ROZNICA_KLUCZA = 0.1

# ── Kołki z filamentu 1.75 ──
KOLEK_OTWOR = 2.0         # Ø otworu (poziomy otwór drukuje się lekko mniejszy — test!)
KOLEK_GLEBOKOSC = 8.0     # w każdą połówkę → kołek ok. 15.5 mm
DNO_KOLKI_Z = (-100.0, -53.5, 0.0, 53.5, 100.0)   # pomiędzy motylkami
DNO_KOLKI_Y = -8.35       # środek grubości dna (-11.0 … -5.7)
SCIANKA_KOLKI_Y = 1.5     # wysokość kołka w ściankach (ścianka: -5.7 … 6.0)
POKRYWA_KOLKI_Z = (-100.0, -53.5, 0.0, 53.5, 100.0)
POKRYWA_KOLKI_Y = 5.73    # środek płyty pokrywy (3.23 … 8.23)

# Stół A1 i odstępy przy układaniu płyt
STOL = 256.0
MARGINES = 3.0
ODSTEP = 4.0

# Geometria oryginału w miejscu cięcia (zmierzona z siatki)
DNO_SPOD_Y = -11.0        # zewnętrzna powierzchnia dna (na stole)
DNO_WNETRZE_Y = -5.7      # wewnętrzna powierzchnia dna
SCIANKA_GORA_Y = 6.0
SCIANKA_TYL_Z = (-110.5, -105.65)   # zewn., wewn.
SCIANKA_PRZOD_Z = (114.5, 109.65)
POKRYWA_ZEWN_Y = 8.23
POKRYWA_WEWN_Y = 3.23

# ───────────────────────── GEOMETRIA ─────────────────────────

def wczytaj_obiekty(sciezka_3mf):
    """Zwraca słownik nazwa_pliku_obiektu -> Trimesh.
    Plik obiektu może mieć kilka <object> (np. modyfikator-kostkę) — bierzemy
    największą siatkę, czyli właściwą część."""
    wynik = {}
    with zipfile.ZipFile(sciezka_3mf) as z:
        for nazwa in z.namelist():
            if not nazwa.startswith("3D/Objects/"):
                continue
            s = z.read(nazwa).decode()
            siatki = []
            for o in re.findall(r"<object .*?</object>", s, re.S):
                v = np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"', o), float)
                t = np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', o), int)
                siatki.append(trimesh.Trimesh(v, t, process=True))
            wynik[Path(nazwa).stem] = max(siatki, key=lambda m: len(m.faces))
    return wynik


def boole(a, b, op):
    return getattr(trimesh.boolean, op)([a, b], engine="manifold")


def pudlo(xmin, xmax, ymin, ymax, zmin, zmax):
    b = trimesh.creation.box(extents=[xmax - xmin, ymax - ymin, zmax - zmin])
    b.apply_translation([(xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2])
    return b


def wyciagnij(punkty_uv, w0, w1, osie):
    """Wielokąt w płaszczyźnie (u, v) wyciągnięty od w0 do w1.
    osie = np. "xyz": u→X, v→Y, w→Z;  "xzy": u→X, v→Z, w→Y."""
    poly = punkty_uv if isinstance(punkty_uv, Polygon) else Polygon(punkty_uv)
    m = trimesh.creation.extrude_polygon(poly, w1 - w0)
    m.apply_translation([0, 0, w0])
    perm = np.zeros((4, 4))
    perm[3, 3] = 1
    for src, os_ in enumerate(osie):
        perm["xyz".index(os_), src] = 1
    m.apply_transform(perm)
    if m.volume < 0:          # permutacja nieparzysta odwraca normalne
        m.invert()
    return m


def kontur_motyla(luz=0.0, promien=0.0):
    """Muszka w płaszczyźnie (x, z), środek w (0, 0), talia na x = 0 (linia szwu)."""
    d, s, t = MOTYL_DLUGOSC / 2, MOTYL_SZEROKOSC / 2, MOTYL_TALIA / 2
    p = Polygon([(-d, -s), (0, -t), (d, -s), (d, s), (0, t), (-d, s)])
    if promien:
        p = p.buffer(-promien, join_style=1).buffer(promien, join_style=1)
    if luz:
        p = p.buffer(luz, join_style=2, mitre_limit=5)
    return p


def bryla_motyla(cx, cz, y0, y1, luz=0.0):
    """Gniazdo muszki: kontur w (x, z), wyciągnięty po Y od y0 do y1."""
    return wyciagnij(translate(kontur_motyla(luz), cx, cz), y0, y1, "xzy")


def walec_x(cy, cz, srednica, x0, x1):
    w = trimesh.creation.cylinder(radius=srednica / 2, height=x1 - x0, sections=48)
    w.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    w.apply_translation([(x0 + x1) / 2, cy, cz])
    return w


def faza_wzdluz_z(c, y_krawedzi, kierunek, f):
    """Klin na krawędzi (x = c, y = y_krawedzi), biegnący wzdłuż Z.
    kierunek = +1: materiał nad krawędzią, -1: materiał pod nią."""
    return wyciagnij([(c - f, y_krawedzi - kierunek * 0.01), (c + f, y_krawedzi - kierunek * 0.01),
                      (c, y_krawedzi + kierunek * f)], -200, 200, "xyz")


def faza_wzdluz_y(c, z_krawedzi, kierunek, f, ymin, ymax):
    """Klin na krawędzi (x = c, z = z_krawedzi), biegnący wzdłuż Y."""
    return wyciagnij([(c - f, z_krawedzi - kierunek * 0.01), (c + f, z_krawedzi - kierunek * 0.01),
                      (c, z_krawedzi + kierunek * f)], ymin, ymax, "xzy")


def przetnij(m, c):
    lewa = boole(m, pudlo(-500, c, -500, 500, -500, 500), "intersection")
    prawa = boole(m, pudlo(c, 500, -500, 500, -500, 500), "intersection")
    return lewa, prawa


def odejmij_wszystko(m, narzedzia):
    if not narzedzia:
        return m
    return boole(m, trimesh.boolean.union(narzedzia, engine="manifold"), "difference")


def podziel_dno(dno):
    c = CIECIE_X
    narzedzia = []
    # gniazda motylków od środka (otwarte do góry przy druku → bez podpór)
    for z in MOTYL_POZYCJE_Z:
        narzedzia.append(bryla_motyla(c, z, DNO_WNETRZE_Y - DNO_GNIAZDO, DNO_WNETRZE_Y + 1.0, luz=LUZ_MOTYLA))
    # kołki: dno + obie ścianki
    for z in DNO_KOLKI_Z:
        narzedzia.append(walec_x(DNO_KOLKI_Y, z, KOLEK_OTWOR, c - KOLEK_GLEBOKOSC, c + KOLEK_GLEBOKOSC))
    for zz in (SCIANKA_TYL_Z, SCIANKA_PRZOD_Z):
        narzedzia.append(walec_x(SCIANKA_KOLKI_Y, sum(zz) / 2, KOLEK_OTWOR,
                                 c - KOLEK_GLEBOKOSC, c + KOLEK_GLEBOKOSC))
    if FAZA_SZWU:
        f = FAZA_SZWU
        narzedzia.append(faza_wzdluz_z(c, DNO_SPOD_Y, +1, f))          # spód (strona stołu)
        narzedzia.append(faza_wzdluz_z(c, SCIANKA_GORA_Y, -1, f))      # górna krawędź ścianek
        narzedzia.append(faza_wzdluz_y(c, SCIANKA_TYL_Z[0], +1, f, -20, 20))   # tył, zewn.
        narzedzia.append(faza_wzdluz_y(c, SCIANKA_PRZOD_Z[0], -1, f, -20, 20))  # przód, zewn.
    return przetnij(odejmij_wszystko(dno, narzedzia), c)


def podziel_pokrywe(pokrywa):
    c = CIECIE_X
    narzedzia = []
    # wnętrze pokrywy jest od strony -Y (tam są zawiasy i zatrzask)
    for z in MOTYL_POZYCJE_Z:
        narzedzia.append(bryla_motyla(c, z, POKRYWA_WEWN_Y - 1.0, POKRYWA_WEWN_Y + POKRYWA_GNIAZDO, luz=LUZ_MOTYLA))
    for z in POKRYWA_KOLKI_Z:
        narzedzia.append(walec_x(POKRYWA_KOLKI_Y, z, KOLEK_OTWOR, c - KOLEK_GLEBOKOSC, c + KOLEK_GLEBOKOSC))
    if FAZA_SZWU:
        narzedzia.append(faza_wzdluz_z(c, POKRYWA_ZEWN_Y, -1, FAZA_SZWU))  # strona zewnętrzna (stół)
    return przetnij(odejmij_wszystko(pokrywa, narzedzia), c)


def klucz(grubosc):
    return trimesh.creation.extrude_polygon(kontur_motyla(promien=MOTYL_PROMIEN), grubosc)


# ───────────── orientacja do druku (jak w oryginalnym projekcie) ─────────────

def na_stol_dno(m):
    m = m.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))   # +Y → +Z
    return na_zero(m)


def na_stol_pokrywa(m):
    m = m.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))  # -Y → +Z
    return na_zero(m)


def na_stol_zamek(m):
    # orientacja z oryginalnego projektu (obrót 180° wokół osi (1, 1, 0))
    m = m.copy()
    m.apply_transform(np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]], float))
    return na_zero(m)


def na_zero(m):
    m.apply_translation(-m.bounds[0])
    return m


def zapisz_3mf(sciezka, obiekty):
    """Prosty 3mf (rdzeń specyfikacji): lista (nazwa, siatka już ustawiona na stole)."""
    zasoby, budowa = [], []
    for i, (nazwa, m) in enumerate(obiekty, start=1):
        v = "".join(f'<vertex x="{x:.4f}" y="{y:.4f}" z="{z:.4f}"/>' for x, y, z in m.vertices)
        t = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in m.faces)
        zasoby.append(f'<object id="{i}" name="{nazwa}" type="model"><mesh><vertices>{v}</vertices>'
                      f'<triangles>{t}</triangles></mesh></object>')
        budowa.append(f'<item objectid="{i}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             f'<resources>{"".join(zasoby)}</resources><build>{"".join(budowa)}</build></model>')
    typy = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/'
            'package/2006/content-types"><Default Extension="rels" ContentType="application/'
            'vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" '
            'ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/'
            'package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" '
            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(sciezka, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", typy)
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", model)


def poloz(m, x, y, obrot_z=False):
    m = m.copy()
    if obrot_z:
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1]))
    m.apply_translation([x, y, 0] - m.bounds[0])
    assert m.bounds[1][0] <= STOL - MARGINES + 1e-6 and m.bounds[1][1] <= STOL - MARGINES + 1e-6, \
        "część wychodzi poza stół"
    return m


def plyty(cz):
    """Trzy płyty A1: duże połówki osobno, małe połówki razem; klucze i zamek w wolnym pasie."""
    M, O = MARGINES, ODSTEP
    duze_x = M + cz["dno_prawe"].extents[0] + O          # początek wolnego pasa obok dużej połówki
    p1 = [("dno_prawe", poloz(cz["dno_prawe"], M, M)),
          ("zamek", poloz(cz["zamek"], duze_x, M))]
    y = M + cz["zamek"].extents[1] + O
    for i in range(4):
        k = poloz(cz["motylek_dno_x4"], duze_x, y, obrot_z=True)
        p1.append((f"motylek_dno_{i + 1}", k))
        y = k.bounds[1][1] + O
    p2 = [("pokrywa_prawa", poloz(cz["pokrywa_prawa"], M, M))]
    y = M
    for i in range(4):
        k = poloz(cz["motylek_pokrywa_x4"], duze_x, y, obrot_z=True)
        p2.append((f"motylek_pokrywa_{i + 1}", k))
        y = k.bounds[1][1] + O
    p3 = [("dno_lewe", poloz(cz["dno_lewe"], M, M)),
          ("pokrywa_lewa", poloz(cz["pokrywa_lewa"], M + cz["dno_lewe"].extents[0] + 2 * O, M))]
    return {"plyta1_dno_prawe": p1, "plyta2_pokrywa_prawa": p2, "plyta3_lewe_polowki": p3}


def main():
    zrodlo, wyjscie = Path(sys.argv[1]), Path(sys.argv[2])
    wyjscie.mkdir(parents=True, exist_ok=True)
    obj = wczytaj_obiekty(zrodlo)
    dno, pokrywa, zamek = obj["object_1"], obj["object_2"], obj["object_3"]

    dno_l, dno_p = podziel_dno(dno)
    pok_l, pok_p = podziel_pokrywe(pokrywa)

    czesci = {
        "dno_lewe": na_stol_dno(dno_l),
        "dno_prawe": na_stol_dno(dno_p),
        "pokrywa_lewa": na_stol_pokrywa(pok_l),
        "pokrywa_prawa": na_stol_pokrywa(pok_p),
        "motylek_dno_x4": na_zero(klucz(DNO_GNIAZDO - ROZNICA_KLUCZA)),
        "motylek_pokrywa_x4": na_zero(klucz(POKRYWA_GNIAZDO - ROZNICA_KLUCZA)),
        "zamek": na_stol_zamek(zamek),
    }
    for nazwa, m in czesci.items():
        assert m.is_watertight, nazwa
        m.export(wyjscie / f"{nazwa}.stl")
        print(f"{nazwa:20s} {m.extents.round(1)} mm  {m.volume / 1000:6.1f} cm³")
    for nazwa, obiekty in plyty(czesci).items():
        zapisz_3mf(wyjscie / f"{nazwa}.3mf", obiekty)
        print(f"{nazwa}.3mf: {', '.join(n for n, _ in obiekty)}")
    # kontrola: suma połówek + gniazda = oryginał
    for n, orig, a, b in (("dno", dno, dno_l, dno_p), ("pokrywa", pokrywa, pok_l, pok_p)):
        print(f"{n}: oryginał {orig.volume/1000:.1f} cm³, po podziale {(a.volume+b.volume)/1000:.1f} cm³")


if __name__ == "__main__":
    main()
