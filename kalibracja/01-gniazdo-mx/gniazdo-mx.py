#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator drabinki tolerancji gniazda krzyzowego MX -> gniazdo-mx.stl

Po co: otwory drukowane pionowo na FDM wychodza MNIEJSZE niz w modelu.
O ile - zalezy od drukarki, filamentu i predkosci. Ta plytka odpowiada na to
jedna liczba, ktora wpisujemy potem do arkusza FreeCAD jako `krzyz_luz`.

Kazda stacja ma jedno gniazdo krzyzowe (nominal MX powiekszony o `dodatek`)
oraz obok rzad malych kwadratowych otworkow - ich LICZBA to numer stacji.

Dlaczego Python, a nie OpenSCAD jak reszta przyrzadow w tym repo:
skrypt buduje siatke wprost z prostopadloscianow i sam sprawdza, czy wynik
jest szczelna, spojnie zorientowana bryla o oczekiwanej objetosci. Dzieki temu
STL w repo jest zweryfikowany, a Ty nie musisz instalowac niczego poza slicerem.

Uruchomienie (nic poza standardowym Pythonem nie jest potrzebne):
    python3 gniazdo-mx.py
"""

import struct
import sys

# --- parametry -------------------------------------------------------------
KRZYZ_RAMIE = 4.10      # nominal MX: dlugosc ramienia
KRZYZ_GRUB = 1.17       # nominal MX: grubosc ramienia
DODATKI = [0.00, 0.05, 0.10, 0.15, 0.20]   # badane naddatki [mm]

GLEBOKOSC = 4.20        # glebokosc gniazda i otworkow numerujacych
ROZSTAW = 13.0          # odstep miedzy srodkami stacji
MARGINES = 3.5          # margines po bokach plyty
PLYTA_GR = 6.0          # grubosc plyty
PLYTA_Y = 20.0          # glebokosc plyty

Y_GNIAZDA = 13.0        # os gniazd
Y_NUMERU = 4.5          # os otworkow numerujacych
KROPKA = 1.6            # bok otworka numerujacego
KROPKA_ODSTEP = 0.8     # odstep miedzy otworkami

PLIK = "gniazdo-mx.stl"


# --- budowa listy prostokatow do wyciecia ----------------------------------
def prostokaty():
    """Zwraca liste (x0, x1, y0, y1) - wszystkie kieszenie o glebokosci GLEBOKOSC."""
    out = []
    for i, d in enumerate(DODATKI):
        xc = MARGINES + ROZSTAW * (i + 0.5)
        a = (KRZYZ_RAMIE + d) / 2.0
        t = (KRZYZ_GRUB + d) / 2.0
        # krzyz = dwa przenikajace sie prostokaty
        out.append((xc - a, xc + a, Y_GNIAZDA - t, Y_GNIAZDA + t))
        out.append((xc - t, xc + t, Y_GNIAZDA - a, Y_GNIAZDA + a))
        # numer stacji: i+1 kwadratowych otworkow
        n = i + 1
        szer = n * KROPKA + (n - 1) * KROPKA_ODSTEP
        x0 = xc - szer / 2.0
        for k in range(n):
            lx = x0 + k * (KROPKA + KROPKA_ODSTEP)
            out.append((lx, lx + KROPKA, Y_NUMERU - KROPKA / 2.0, Y_NUMERU + KROPKA / 2.0))
    return out


# --- siatka ----------------------------------------------------------------
def unikalne(wartosci, eps=1e-9):
    w = sorted(wartosci)
    out = [w[0]]
    for v in w[1:]:
        if v - out[-1] > eps:
            out.append(v)
    return out


class Siatka:
    def __init__(self):
        self.tri = []

    def quad(self, p0, p1, p2, p3, n):
        """Czworokat o zadanej normalnej zewnetrznej; kolejnosc wierzcholkow
        poprawiana automatycznie, zeby nie robic tego w pamieci."""
        ux = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        vx = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
        cx = (ux[1] * vx[2] - ux[2] * vx[1],
              ux[2] * vx[0] - ux[0] * vx[2],
              ux[0] * vx[1] - ux[1] * vx[0])
        if cx[0] * n[0] + cx[1] * n[1] + cx[2] * n[2] < 0:
            p0, p1, p2, p3 = p0, p3, p2, p1
        self.tri.append((p0, p1, p2))
        self.tri.append((p0, p2, p3))


def zbuduj():
    kieszenie = prostokaty()

    xs = unikalne([0.0, MARGINES * 2 + ROZSTAW * len(DODATKI)]
                  + [r[0] for r in kieszenie] + [r[1] for r in kieszenie])
    ys = unikalne([0.0, PLYTA_Y]
                  + [r[2] for r in kieszenie] + [r[3] for r in kieszenie])

    L, W, H = xs[-1], ys[-1], PLYTA_GR
    z_dno = H - GLEBOKOSC

    def wyciete(i, j):
        cx = (xs[i] + xs[i + 1]) / 2.0
        cy = (ys[j] + ys[j + 1]) / 2.0
        for (x0, x1, y0, y1) in kieszenie:
            if x0 < cx < x1 and y0 < cy < y1:
                return True
        return False

    nx, ny = len(xs) - 1, len(ys) - 1
    maska = [[wyciete(i, j) for j in range(ny)] for i in range(nx)]

    s = Siatka()

    for i in range(nx):
        for j in range(ny):
            x0, x1, y0, y1 = xs[i], xs[i + 1], ys[j], ys[j + 1]
            # spod plyty
            s.quad((x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0), (0, 0, -1))
            # gora: pelna plaszczyzna albo dno kieszeni
            z = z_dno if maska[i][j] else H
            s.quad((x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z), (0, 0, 1))

    # scianki kieszeni - tam, gdzie sasiednie komorki roznia sie stanem
    for i in range(nx - 1):
        for j in range(ny):
            if maska[i][j] == maska[i + 1][j]:
                continue
            x, y0, y1 = xs[i + 1], ys[j], ys[j + 1]
            n = (1, 0, 0) if maska[i + 1][j] else (-1, 0, 0)
            s.quad((x, y0, z_dno), (x, y1, z_dno), (x, y1, H), (x, y0, H), n)
    for i in range(nx):
        for j in range(ny - 1):
            if maska[i][j] == maska[i][j + 1]:
                continue
            y, x0, x1 = ys[j + 1], xs[i], xs[i + 1]
            n = (0, 1, 0) if maska[i][j + 1] else (0, -1, 0)
            s.quad((x0, y, z_dno), (x1, y, z_dno), (x1, y, H), (x0, y, H), n)

    # boki plyty
    for i in range(nx):
        x0, x1 = xs[i], xs[i + 1]
        s.quad((x0, 0, 0), (x1, 0, 0), (x1, 0, H), (x0, 0, H), (0, -1, 0))
        s.quad((x0, W, 0), (x1, W, 0), (x1, W, H), (x0, W, H), (0, 1, 0))
    for j in range(ny):
        y0, y1 = ys[j], ys[j + 1]
        s.quad((0, y0, 0), (0, y1, 0), (0, y1, H), (0, y0, H), (-1, 0, 0))
        s.quad((L, y0, 0), (L, y1, 0), (L, y1, H), (L, y0, H), (1, 0, 0))

    pole_kieszeni = sum((xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
                        for i in range(nx) for j in range(ny) if maska[i][j])
    oczekiwana_v = L * W * H - pole_kieszeni * GLEBOKOSC
    return s.tri, (L, W, H), oczekiwana_v


# --- weryfikacja -----------------------------------------------------------
def sprawdz(tri, oczekiwana_v):
    kluczy = {}
    for t in tri:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            kluczy[(a, b)] = kluczy.get((a, b), 0) + 1

    bledy = []
    powtorzone = [k for k, v in kluczy.items() if v != 1]
    if powtorzone:
        bledy.append("krawedzie skierowane wystepujace wiecej niz raz: %d" % len(powtorzone))
    niesparowane = [k for k in kluczy if (k[1], k[0]) not in kluczy]
    if niesparowane:
        bledy.append("krawedzie bez pary (dziury w siatce): %d" % len(niesparowane))

    v = 0.0
    for (a, b, c) in tri:
        v += (a[0] * (b[1] * c[2] - b[2] * c[1])
              - a[1] * (b[0] * c[2] - b[2] * c[0])
              + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    if abs(v - oczekiwana_v) > 1e-6:
        bledy.append("objetosc siatki %.6f != oczekiwana %.6f" % (v, oczekiwana_v))
    return v, bledy


def zapisz(tri, sciezka):
    with open(sciezka, "wb") as f:
        f.write(b"drabinka tolerancji gniazda MX".ljust(80, b" "))
        f.write(struct.pack("<I", len(tri)))
        for (a, b, c) in tri:
            ux = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
            vx = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
            n = (ux[1] * vx[2] - ux[2] * vx[1],
                 ux[2] * vx[0] - ux[0] * vx[2],
                 ux[0] * vx[1] - ux[1] * vx[0])
            d = (n[0] ** 2 + n[1] ** 2 + n[2] ** 2) ** 0.5 or 1.0
            f.write(struct.pack("<3f", n[0] / d, n[1] / d, n[2] / d))
            for p in (a, b, c):
                f.write(struct.pack("<3f", *p))
            f.write(struct.pack("<H", 0))


if __name__ == "__main__":
    tri, (L, W, H), oczekiwana_v = zbuduj()
    v, bledy = sprawdz(tri, oczekiwana_v)

    print("Stacje (liczba otworkow = numer stacji):")
    for i, d in enumerate(DODATKI):
        print("  %d otw.  dodatek +%.2f mm  ->  gniazdo %.2f x %.2f mm"
              % (i + 1, d, KRZYZ_RAMIE + d, KRZYZ_GRUB + d))
    print("Gabaryt        : %.2f x %.2f x %.2f mm" % (L, W, H))
    print("Trojkatow      : %d" % len(tri))
    print("Objetosc       : %.3f cm3  (~%.2f g w PLA przy 100%%)" % (v / 1000.0, v / 1000.0 * 1.24))

    if bledy:
        print("SIATKA NIEPOPRAWNA:")
        for b in bledy:
            print("  - " + b)
        sys.exit(1)

    print("Siatka         : szczelna, spojnie zorientowana, objetosc zgodna z modelem")
    zapisz(tri, PLIK)
    print("Zapisano       : %s" % PLIK)
