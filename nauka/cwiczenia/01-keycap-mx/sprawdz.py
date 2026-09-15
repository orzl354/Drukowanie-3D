# -*- coding: utf-8 -*-
"""
sprawdz.py - kontrola modelu keycapa przed eksportem do STL.

JAK URUCHOMIC (tak samo na Linuksie i na macOS):
  1. Otworz swoj dokument .FCStd we FreeCAD.
  2. View -> Panels -> Python console  (macOS tak samo).
  3. W konsoli wklej:
         exec(open("/pelna/sciezka/do/sprawdz.py").read())

     Na macOS sciezka bedzie w stylu:
         /Users/<ty>/Drukowanie-3D/nauka/cwiczenia/01-keycap-mx/sprawdz.py
     Na Linuksie:
         /home/<ty>/Drukowanie-3D/nauka/cwiczenia/01-keycap-mx/sprawdz.py

Skrypt nic nie zmienia w modelu - tylko czyta i wypisuje.
"""

import FreeCAD

GESTOSC = {"PLA": 1.24, "PETG": 1.27, "ASA": 1.07}  # g/cm3


def _znajdz_body(doc):
    ciala = [o for o in doc.Objects if o.isDerivedFrom("PartDesign::Body")]
    if not ciala:
        ciala = [o for o in doc.Objects
                 if hasattr(o, "Shape") and o.Shape.Solids and o.TypeId != "App::Part"]
    return ciala


def _arkusz(doc):
    for o in doc.Objects:
        if o.isDerivedFrom("Spreadsheet::Sheet"):
            return o
    return None


def _alias(sheet, nazwa):
    try:
        wartosc = sheet.get(nazwa)
    except Exception:
        return None
    return float(getattr(wartosc, "Value", wartosc))


def sprawdz():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        print("BLAD: nie ma otwartego dokumentu.")
        return

    print("=" * 62)
    print("Dokument: %s" % doc.Name)

    ciala = _znajdz_body(doc)
    if not ciala:
        print("BLAD: nie znalazlem zadnego Body ani bryly.")
        return

    for body in ciala:
        ksztalt = body.Shape
        print("-" * 62)
        print("Body: %s" % body.Label)

        # 1. Poprawnosc geometrii
        poprawny = ksztalt.isValid()
        print("  Geometria poprawna : %s" % ("TAK" if poprawny else "NIE  <-- NAPRAW"))

        # 2. Liczba rozlacznych bryl - odpowiednik "Volumes:" z OpenSCAD
        n = len(ksztalt.Solids)
        print("  Liczba bryl        : %d %s" % (n, "" if n == 1 else " <-- model jest rozerwany"))

        # 3. Gabaryt
        bb = ksztalt.BoundBox
        print("  Gabaryt (X/Y/Z)    : %.3f x %.3f x %.3f mm" % (bb.XLength, bb.YLength, bb.ZLength))

        # 4. Objetosc i masa
        v_cm3 = ksztalt.Volume / 1000.0
        print("  Objetosc           : %.3f cm3" % v_cm3)
        masy = ", ".join("%s %.2f g" % (m, v_cm3 * g) for m, g in sorted(GESTOSC.items()))
        print("  Masa (100%% wypelnienia): %s" % masy)

        # 5. Porownanie z arkuszem
        sheet = _arkusz(doc)
        if sheet is None:
            print("  Arkusz             : brak - pomijam porownanie wymiarow")
            continue

        oczekiwane = [
            ("X", "szer_podstawy", bb.XLength),
            ("Y", "szer_podstawy", bb.YLength),
            ("Z", "wys_calk", bb.ZLength),
        ]
        print("  Porownanie z arkuszem '%s':" % sheet.Name)
        for os_, alias, zmierzone in oczekiwane:
            cel = _alias(sheet, alias)
            if cel is None:
                print("    %s: brak aliasu '%s' w arkuszu" % (os_, alias))
                continue
            delta = zmierzone - cel
            status = "OK" if abs(delta) < 0.01 else "ROZNICA %+.3f mm  <-- sprawdz" % delta
            print("    %s: model %.3f  vs  %s = %.3f   %s" % (os_, zmierzone, alias, cel, status))

        # 6. Przypomnienie o placeholderach
        luz = _alias(sheet, "krzyz_luz")
        gleb = _alias(sheet, "gleb_wew")
        if luz is not None and abs(luz - 0.10) < 1e-6:
            print("  UWAGA: krzyz_luz = 0.100 mm to wartosc startowa z lekcji.")
            print("         Zrob kalibracja/01-gniazdo-mx zanim wydrukujesz keycapa na serio.")
        if gleb is not None and abs(gleb - 7.80) < 1e-6:
            print("  UWAGA: gleb_wew = 7.800 mm to wartosc startowa z lekcji.")
            print("         Wpisz tu pomiar B1 z pomiary.md, inaczej klawisz moze miec skrocony skok.")

    print("=" * 62)


sprawdz()
