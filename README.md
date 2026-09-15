# Drukowanie-3D

Osobiste repo do druku 3D i nauki projektowania CAD.
Sprzęt: **Bambu Lab A1 Combo + AMS Lite**, dysza 0.4 mm, pole 256³ mm.

Zasady pracy, sprzęt, tolerancje i konwencje — patrz [`CLAUDE.md`](CLAUDE.md).

## Struktura

| Katalog | Zawartość |
|---|---|
| `projekty/` | jeden folder = jeden projekt (`cad/`, `stl/`, `slicer/`, `zdjecia/`) |
| `projekty/_szablon/` | szablon `README.md` do kopiowania przy nowym projekcie |
| `nauka/` | `kurs-freecad.md` (plan nauki), `dziennik.md`, ćwiczenia, notatki |
| `profile/` | profile filamentów i procesów |
| `kalibracja/` | wyniki testów: tolerancje, temp tower, flow, bridging |
| `biblioteka/` | własne komponenty wielokrotnego użytku |

## Nauka

Uczę się modelowania parametrycznego w **FreeCAD** — plan i kolejność lekcji:
[`nauka/kurs-freecad.md`](nauka/kurs-freecad.md).
Wcześniejsze projekty powstawały w OpenSCAD i tak zostaje: OpenSCAD do rzeczy
generowanych pętlą (przyrządy, drabinki tolerancji), FreeCAD do przedmiotów.

Pracuję na dwóch maszynach (PC + MacBook). Różnice w konfiguracji, nawigacji
i skrótach są opisane w [`nauka/notatki/`](nauka/notatki/).

## Projekty

| Projekt | Narzędzie | Status |
|---|---|---|
| [`uchwyt-telefon-biurko`](projekty/uchwyt-telefon-biurko/) | OpenSCAD | zaprojektowany, niewydrukowany |
| [`keycap-mx-1u`](projekty/keycap-mx-1u/) | FreeCAD | szkic |

## Status

Brak własnych pomiarów kalibracyjnych — pierwszy zaplanowany to
[`kalibracja/01-gniazdo-mx`](kalibracja/01-gniazdo-mx/).
Tolerancje podane w `CLAUDE.md` są **wartościami startowymi**, do zweryfikowania
drukiem na tym konkretnym egzemplarzu drukarki.
