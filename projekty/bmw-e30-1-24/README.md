# BMW E30 coupe w skali 1:24 z własnym bodykitem

Projekt do kursu [`nauka/notatki/blender-bodykit.md`](../../nauka/notatki/blender-bodykit.md).

## Cel
Model wystawowy BMW E30 (2-drzwiowe coupe, polift 1988–91) w skali **1:24**,
wymodelowany w Blenderze z blueprintów, z **własnym bodykitem** jako osobnymi
częściami (splitter, progi, spoiler/ducktail).

Przy okazji to pierwszy projekt do nauki modelowania karoserii: E30 ma płaskie boki,
prostą linię okien i proste zderzaki, więc błędy siatki są mniej kłopotliwe
niż przy obłym nadwoziu.

**Dlaczego coupe, a nie sedan:** mniej słupków i szczelin drzwi, czyli prostsza
siatka. **Dlaczego polift:** plastikowe zderzaki to gładkie bryły, do których
łatwo dopasować dokładkę (przedlift ma chromowane listwy).
Jeśli wolisz inną wersję, zmień wymiary w tabeli poniżej przed ustawieniem blueprintów.

## Wymiary

| | Rzeczywiste (miarka w Blenderze) | Na wydruku 1:24 |
|---|---|---|
| Długość (Y) | 4325 mm | 180,2 mm |
| Szerokość bez lusterek (X) | 1645 mm | 68,5 mm |
| Wysokość (Z) | 1380 mm | 57,5 mm |
| Rozstaw osi | 2570 mm | 107,1 mm |
| Koło (opona 195/65 R14) | Ø ≈ 609 mm, szer. 195 mm | Ø ≈ 25,4 mm, szer. 8,1 mm |

Źródło: dane katalogowe 320i coupe (carsales.com.au). Bazy różnią się o kilka mm
w szerokości i wysokości, a ostatecznie **sprawdź je z wybranym blueprintem**.
Rozstaw osi 2570 mm zgadza się we wszystkich źródłach.

- Eksport STL: `Scale = 1000 / 24 = 41.667`.
- Minimalna grubość części w Blenderze: `1,2 mm × 24 ≈ 29 mm` (`Thickness: 30mm`).
- Mieści się na stole A1 (256 mm) z dużym zapasem.

## Materiał
**PLA Matte** to model wystawowy, który nie trafia do auta, więc odporność
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
`szkic`. Etap: lekcja 1 (interfejs). Blueprint jeszcze nie wybrany.

Kolejne kroki:
1. Ćwiczenie 1 (resorak z klocków).
2. Znaleźć blueprint E30 coupe (bok, przód, tył, góra), przyciąć i zapisać
   do `cad/blueprinty/`.
3. Ćwiczenie 2: ustawić blueprinty w `cad/bmw-e30.blend`.

## Wnioski
—
