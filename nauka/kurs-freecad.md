# Kurs FreeCAD — plan

Uczę się modelowania parametrycznego w **FreeCAD**, wzorując się na kanale
[CAD CAM Lessons](https://www.youtube.com/@CADCAMLessons) (FreeCAD dla początkujących,
Part Design krok po kroku; ten sam autor prowadzi `cadcamlessons.com`).

Pracuję na dwóch maszynach: **Linux/PC** i **MacBook**. Wszystko, co robimy, ma działać
tak samo na obu — różnice w skrótach i nawigacji są w
[`notatki/freecad-02-skroty.md`](notatki/freecad-02-skroty.md).

---

## Zasada kursu

Każda lekcja = **jeden gotowy przedmiot**, nie ćwiczenie „na sucho".
Kolejność: krótka teoria → ćwiczenie → kryteria sukcesu → wpis do `dziennik.md`.

Każdy model robię **parametrycznie przez arkusz (Spreadsheet)**, nie przez wpisywanie
liczb do szkiców. To jest odpowiednik zmiennych na górze pliku `.scad` — bez tego
FreeCAD jest tylko klikaniem.

---

## Moduł 0 — start (do zrobienia raz, na obu maszynach)

| | |
|---|---|
| 0.1 | Instalacja i ustawienia — [`notatki/freecad-01-instalacja-i-ustawienia.md`](notatki/freecad-01-instalacja-i-ustawienia.md) |
| 0.2 | Nawigacja i skróty, w tym macOS — [`notatki/freecad-02-skroty.md`](notatki/freecad-02-skroty.md) |
| 0.3 | Jak myśleć w Part Design — [`notatki/freecad-03-part-design.md`](notatki/freecad-03-part-design.md) |

## Moduł 1 — keycap (tu zaczynamy)

➡️ **[Lista kroków na teraz: `cwiczenia/01-keycap-mx/START.md`](cwiczenia/01-keycap-mx/START.md)**

| Lekcja | Temat | Nowe umiejętności | Status |
|---|---|---|---|
| **1** | [Keycap 1u na Esc, płaski wierzch](cwiczenia/01-keycap-mx/) | arkusz parametrów, szkic w pełni związany, Pad, Loft, Thickness, gniazdo MX | **do zrobienia** |
| 2 | Keycap v2: wgłębienie (dish), **pochylenie górnego rzędu** (Esc go potrzebuje), fazy i zaokrąglenia | Pocket przez bryłę obrotową, Chamfer/Fillet, płaszczyzny odniesienia | — |
| 3 | Rodzina keycapów z jednego modelu (R1–R4, 1u / 1.25u / 2u) | jeden arkusz → wiele konfiguracji, eksport wsadowy | — |
| 4 | Keycap z legendą „ESC” w drugim kolorze (AMS Lite) | modelowanie pod multicolor, podział na obiekty, 3MF wielobryłowy | — |

## Moduł 2 — dalej (szkic, do doprecyzowania po module 1)

- Szkicownik na serio: więzy geometryczne vs wymiarowe, dlaczego „w pełni związany" to nie fanaberia.
- Rewolucja (Revolution) i profile obrotowe — pokrętła, tuleje, dystanse.
- Zaokrąglenia, fazy, pochylenia (Draft) — czyli DfAM w praktyce.
- Złożenia i sprawdzanie kolizji (Assembly w FreeCAD 1.0+).
- TechDraw: rysunek wykonawczy do pomiaru suwmiarką po wydruku.

---

## Czego pilnuję w każdej lekcji

1. **Milimetry.** Zawsze. Jednostki ustawione tak samo na PC i na MacBooku.
2. **Szkic musi być zielony** (w pełni związany). Żółty szkic = model, który sam się zepsuje.
3. **Parametry w arkuszu**, nazwy bez polskich znaków (`szer_podstawy`, nie `szer_podstawy_ą`).
4. **Orientacja druku ustalona przed modelowaniem**, nie po. Patrz wnioski z `uchwyt-telefon-biurko`.
5. Po każdej sesji: wpis do [`dziennik.md`](dziennik.md) i `git push`.
