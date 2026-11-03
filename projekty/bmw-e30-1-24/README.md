# BMW E30 M3 w skali 1:24, z bodykitem jako osobnymi częściami

Projekt do kursu [`nauka/notatki/blender-bodykit.md`](../../nauka/notatki/blender-bodykit.md).

## Cel
Model wystawowy BMW E30 **M3** (coupe) w skali **1:24**, wymodelowany w Blenderze
z blueprintów. Bodykit to osobne części: dokładka/splitter, progi, skrzydło
oraz ewentualnie własne modyfikacje.

Wybrany blueprint przedstawia M3 (wymiary 4345 / 2565 / 1680 / 1370, poszerzone
nadkola, skrzydło), a nie zwykłe 320i coupe. To dobrze pasuje do kursu:
fabryczna aerodynamika M3 to gotowy zestaw części do lekcji 4 (każdą modelujesz
jako osobny obiekt na powierzchni karoserii).

## Wymiary

| | Rzeczywiste (miarka w Blenderze) | Na wydruku 1:24 |
|---|---|---|
| Długość (Y) | 4345 mm | 181,0 mm |
| Szerokość bez lusterek (X) | 1680 mm | 70,0 mm |
| Wysokość (Z) | 1370 mm | 57,1 mm |
| Rozstaw osi | 2565 mm | 106,9 mm |
| Rozstaw kół przód / tył | 1418 / 1430 mm | 59,1 / 59,6 mm |

Źródło: linie wymiarowe na blueprincie, zgodne z danymi katalogowymi M3 E30
(auto-data.net: 4345 × 1680 × 1370, rozstaw osi 2565).

- Eksport STL: `Scale = 1000 / 24 = 41.667`.
- Minimalna grubość części w Blenderze: `1,2 mm × 24 ≈ 29 mm` (`Thickness: 30mm`).

## Blueprinty (`cad/blueprinty/`)

`oryginaly/` to pliki w postaci, w jakiej je znalazłem (źródło: the-blueprints.com).
Pliki w `blueprinty/` są przygotowane do Blendera:

1. **Wyprostowane:** bok był obrócony o 0,33°, a widok z góry o 0,57°
   (linia ziemi i oś symetrii nie były poziome).
2. **Przycięte ciasno do karoserii:** od zderzaka do zderzaka, od ziemi do dachu,
   bez linii wymiarowych i bez lusterek.
3. **Przeskalowane do prawdziwych proporcji.** Skany były nierównomiernie
   rozciągnięte (o 3–4% w jednej osi). Przykładowo bok miał proporcje 3,09 : 1,
   a powinien mieć 4345 : 1370 = 3,17 : 1.
4. **Widok z góry obrócony o 90°**, żeby przód auta był na dole (oś −Y w Blenderze).

| Plik | Size w Blenderze | Proporcje |
|---|---|---|
| `bok.png` | 4.345 | 4345 × 1370 |
| `przod.png` | 1.68 | 1680 × 1370 |
| `tyl.png` | 1.68 | 1680 × 1370 |
| `gora.png` | 4.345 | 1680 × 4345 (pionowy) |

**Znana niespójność:** osie kół na rysunku boku wypadają w odstępie ≈ 2595 mm,
a katalogowy rozstaw osi to 2565 mm (różnica 30 mm, czyli 1,2 mm na wydruku 1:24).
Do decyzji przy modelowaniu nadkoli: trzymać się rysunku czy miarki rozstawu osi.

## Materiał
**PLA Matte**: model wystawowy, który nie trafia do auta, więc odporność
temperaturowa nie jest potrzebna, a mat ukrywa linie warstw. Karoseria i bodykit
drukowane osobno, w różnych kolorach, bez wieży czyszczącej.

## Ustawienia druku
| | |
|---|---|
| Warstwa | 0.12 mm (start, **do testu**) |
| Wypełnienie | do ustalenia |
| Ścianki (perymetry) | do ustalenia |
| Orientacja na stole | karoseria na płaskim dnie, części bodykitu osobno |
| Podpory | prawdopodobnie tylko w nadkolach (tree) |
| Uwagi | najpierw test: przednia ćwiartka + jedna część bodykitu (ćwiczenie 5) |

## Status
`szkic`. Etap: ćwiczenie 2 (blueprinty przygotowane, do ustawienia w Blenderze).

## Wnioski
- Blueprint z internetu trzeba **zmierzyć**, zanim mu zaufasz: wszystkie 4 rzuty
  miały inne proporcje niż wynika z ich własnych linii wymiarowych.
