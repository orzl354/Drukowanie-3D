# Drukowanie-3D

Osobiste repo do druku 3D i nauki projektowania CAD.
Sprzęt: **Bambu Lab A1 Combo + AMS Lite**, dysza 0.4 mm, pole 256³ mm.

Zasady pracy, sprzęt, tolerancje i konwencje — patrz [`CLAUDE.md`](CLAUDE.md).

## Struktura

| Katalog | Zawartość |
|---|---|
| `projekty/` | jeden folder = jeden projekt (`cad/`, `stl/`, `slicer/`, `zdjecia/`) |
| `projekty/_szablon/` | szablon `README.md` do kopiowania przy nowym projekcie |
| `nauka/` | `dziennik.md`, ćwiczenia, notatki |
| `profile/` | profile filamentów i procesów |
| `kalibracja/` | wyniki testów: tolerancje, temp tower, flow, bridging |
| `biblioteka/` | własne komponenty wielokrotnego użytku |

## Projekty

| Projekt | Co to | Status |
|---|---|---|
| [`uchwyt-telefon-biurko`](projekty/uchwyt-telefon-biurko/) | uchwyt na telefon z zaciskiem na blat, parametryczny OpenSCAD | szkic |
| [`pingwin-keycap-multicolor`](projekty/pingwin-keycap-multicolor/) | podział modelu malowanego kolorami na części jednokolorowe (druk bez zmian filamentu) | szkic |

## Status

Nic jeszcze nie wydrukowane i brak własnych pomiarów kalibracyjnych.
Tolerancje podane w `CLAUDE.md` są **wartościami startowymi**, do zweryfikowania
drukiem na tym konkretnym egzemplarzu drukarki.
