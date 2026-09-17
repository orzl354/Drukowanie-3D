#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Podzial keycapa "Larvitar" (Bambu Studio 3MF, malowanie MMU) na osobne czesci
kolorystyczne. Narzedzia siedza w biblioteka/podzial_mmu.py - tutaj jest tylko
to, co specyficzne dla tego modelu.

Czym ten model rozni sie od Psyducka
------------------------------------
1. Baza keycapa i figurka to JUZ DWIE OSOBNE, zamkniete bryly w jednej siatce
   (m.split() daje 2 elementy). Nic nie trzeba ciac - wystarczy je rozdzielic.
2. Figurka wchodzi w gore bazy tylko 0.33 mm i styka sie z nia pieciopunktowo
   (3 wysepki, razem 16.3 mm2). Sam taki styk to slaba baza do klejenia
   i fatalna przyczepnosc do stolu przy druku, wiec przekroj na plaszczyznie
   gory bazy jest wyciagany w dol jako COKOL, a w bazie powstaje pasujace
   gniazdo - zlacze samo sie pozycjonuje.
3. Ciemnozielonych obszarow jest 10, ale tylko plyta na brzuchu ma sensowny
   rozmiar (4.3 x 2.1 x 5.3 mm). Pozostale 9 ma 0.24-1.8 mm i zostaje na ciele
   do pomalowania - patrz README.

Uruchomienie:  python3 podzial_kolorow.py [zrodlo.3mf]
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', '..', 'biblioteka'))
import numpy as np, trimesh
from podzial_mmu import *

# ========================= PARAMETRY =========================
LUZ         = 0.10   # luz boczny czopa [mm] - pasowanie ciasne wg CLAUDE.md
GL_BRZUCH   = 1.5    # glebokosc czopa plyty brzusznej [mm]
GL_OKO      = 1.2    # glebokosc czopa oka [mm]
GL_COKOL    = 0.8    # ile cokol figurki wchodzi w baze [mm]
                     # (gorna scianka bazy ma 1.54 mm - zostaje 0.74 mm)
ODSTEP      = 6.0    # odstep miedzy czesciami na plycie [mm]

OCZY_OSOBNO = True   # False = oczy zostaja na ciele (do pomalowania).
                     # Sa na granicy sensu: widoczna czesc to 1.1 x 1.7 mm.

KOLORY = {'zielony': 1, 'ciemnozielony': 2, 'czarny': 3, 'bialy': 4}  # sloty AMS
# =============================================================


def przekroj_xy(mesh, z):
    """Wielokaty przekroju bryly plaszczyzna z = const, we wspolrzednych XY."""
    sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    p2, _ = sec.to_planar(to_2D=np.eye(4))     # eye(4) => 2D to po prostu XY
    return list(p2.polygons_full)


def podziel(zrodlo):
    V, F, S = wczytaj_3mf(zrodlo)
    m = trimesh.Trimesh(vertices=V, faces=F, process=False)
    assert m.is_watertight, 'model zrodlowy nie jest szczelny'

    bryly = m.split(only_watertight=False)
    assert len(bryly) == 2, f'spodziewane 2 bryly, jest {len(bryly)}'
    # baza to ta lezaca nizej (keycap), figurka siedzi na niej
    baza, figurka = sorted(bryly, key=lambda b: b.bounds[0][2])
    ZB = baza.bounds[1][2]                      # plaska gora bazy
    print(f'model: {len(F)} trojkatow, {m.volume:.1f} mm3, gabaryt {np.round(m.extents,2)}')
    print(f'  baza {baza.volume:7.2f} mm3 (z do {ZB:.3f}),  figurka {figurka.volume:7.2f} mm3')

    # --- obszary kolorow ---
    brzuch = max((c for c in skladowe(m, S == 2)), key=len)
    male_biale = sorted([c for c in skladowe(m, S == 4) if len(c) < 100],
                        key=lambda c: V[F[c]].reshape(-1, 3)[:, 0].mean())

    OBSZARY = [('plyta-brzuch', brzuch, GL_BRZUCH, 'ciemnozielony')]
    if OCZY_OSOBNO and len(male_biale) == 2:
        OBSZARY += [('oko-L', male_biale[0], GL_OKO, 'bialy'),
                    ('oko-P', male_biale[1], GL_OKO, 'bialy')]

    czesci, gniazda = {}, []
    for nazwa, fidx, gl, kolor in OBSZARY:
        k = kierunek_obszaru(m, fidx)
        p, g = czop(m, fidx, k, gl, LUZ), czop(m, fidx, k, gl, 0.0)
        czesci[nazwa] = (p, kolor, np.asarray(uklad(k)[0]))
        gniazda.append(g)
        print(f'  {nazwa:13s} {p.volume:7.2f} mm3  gabaryt {np.round(p.extents,2)}')

    # --- cialo: minus gniazda, obciete na gorze bazy, plus cokol ---
    c = bool_op('difference', [figurka] + gniazda) if gniazda else figurka
    gora = najwieksza_bryla(bool_op('intersection', [c, polprzestrzen(ZB, True)]))
    wyspy = przekroj_xy(figurka, ZB)
    print(f'  cokol: {len(wyspy)} wysp o polu {[round(w.area,2) for w in wyspy]} mm2')
    cok_cz = [pryzma_xy(w.buffer(-LUZ), ZB - GL_COKOL, ZB) for w in wyspy]
    cok_gn = [pryzma_xy(w,               ZB - GL_COKOL, ZB) for w in wyspy]

    cialo = bool_op('union', [gora] + cok_cz)
    baza_n = bool_op('difference', [baza] + cok_gn)
    czesci['cialo']       = (cialo,  'zielony', np.array([0., 0., -1.]))
    czesci['baza-keycap'] = (baza_n, 'bialy',   np.array([0., 0.,  1.]))
    print(f'  cialo    {cialo.volume:8.2f} mm3   baza-keycap {baza_n.volume:7.2f} mm3')

    kontrola(czesci)
    return czesci


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    zrodlo = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'larvitar.3mf')
    czesci = podziel(zrodlo)
    poz = ulozenie(czesci, odstep=ODSTEP)

    eksportuj_stl(czesci, os.path.join(here, '..', 'stl'), KOLORY)
    cel = os.path.join(here, '..', 'slicer', 'larvitar-plyta-podzielona.3mf')
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    zapisz_3mf(czesci, poz, cel, KOLORY, ustawienia_zrodla(zrodlo))

    print('\nulozenie na plycie (X, Y):')
    for n, (x, y) in sorted(poz.items()): print(f'  {n:13s} ({x:6.1f}, {y:6.1f})')
    print(f'\nzapisano: {len(czesci)} STL + {os.path.basename(cel)}')
