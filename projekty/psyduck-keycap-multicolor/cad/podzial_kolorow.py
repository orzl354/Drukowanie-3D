#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Podzial keycapa "Psyduck" (Bambu Studio 3MF, malowanie MMU) na osobne czesci,
po jednej na kolor - zeby kazda grupe wydrukowac jednym filamentem, bez
przezbrajania AMS i bez wiezy czyszczacej.

Narzedzia geometryczne siedza w ../../../biblioteka/podzial_mmu.py - tutaj jest
tylko to, co specyficzne dla tego modelu: ktory obszar koloru jest czym
i jak glęboko wchodzi jego czop.

Jak model jest pociety
----------------------
  * baza keycapa  - model ma gotowy PLASKI SZEW na Z_SZWU (zero trojkatow
    przecinajacych te plaszczyzne), wiec ciecie tam jest darmowe.
  * dziob, oczy, wlosy - "czop + gniazdo" z tej samej powierzchni: krawedz na
    zewnatrz trafia w siebie co do mikrona (szew niewidoczny), a luz siedzi
    dopiero w glebi czopa jako zbieznosc - tam, gdzie i tak trzeba miejsca
    na klej.
  * stopy - operacje boolowskie, bo obrys stopy w rzucie z gory sam sie
    przecina i metoda czopa tu nie dziala.

Uruchomienie:  python3 podzial_kolorow.py [zrodlo.3mf]
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', '..', 'biblioteka'))
import numpy as np, trimesh
from podzial_mmu import *

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

KOLORY = {'zolty': 1, 'czarny': 2, 'bialy': 3, 'kremowy': 4}   # sloty AMS
# =============================================================


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

    kontrola(czesci)
    return czesci



if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    zrodlo = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'psyduck_keycap.3mf')
    czesci = podziel(zrodlo)
    poz = ulozenie(czesci, odstep=ODSTEP)

    eksportuj_stl(czesci, os.path.join(here, '..', 'stl'), KOLORY)
    cel = os.path.join(here, '..', 'slicer', 'psyduck-plyta-podzielona.3mf')
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    zapisz_3mf(czesci, poz, cel, KOLORY, ustawienia_zrodla(zrodlo))

    print('\nulozenie na plycie (X, Y):')
    for n, (x, y) in sorted(poz.items()): print(f'  {n:12s} ({x:6.1f}, {y:6.1f})')
    print(f'\nzapisano: {len(czesci)} STL + {os.path.basename(cel)}')
