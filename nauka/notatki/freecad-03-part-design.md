# Jak myśleć w Part Design (i czym to się różni od OpenSCAD)

Znam już OpenSCAD, więc najkrótsza droga to porównanie.

| OpenSCAD | Part Design | Różnica, która boli na starcie |
|---|---|---|
| zmienne na górze pliku | **Spreadsheet** z aliasami | w FreeCAD trzeba je świadomie założyć, inaczej liczby wsiąkną w szkice |
| `linear_extrude(h)` | **Pad** (na szkicu) | |
| `difference()` z bryłą | **Pocket** (na szkicu) | Pocket zawsze wycina, nie da się nim dodać |
| `hull()` między profilami | **Loft** (na ≥2 szkicach) | Loft potrzebuje szkiców na **różnych płaszczyznach** |
| ręczne odjęcie mniejszej bryły | **Thickness** (wydrążenie) | jedno kliknięcie zamiast liczenia offsetów |
| `rotate_extrude()` | **Revolution** | |
| brak — fazy robiło się ręcznie | **Fillet / Chamfer** | działają na **krawędziach gotowej bryły**, nie na szkicu |
| kolejność w kodzie | **kolejność w drzewie** | drzewo to jest Twój kod, tylko klikalny |

---

## Trzy pojęcia, bez których nic nie zagra

**Body (Ciało).** Jedna spójna bryła i jej historia operacji. Jeden plik może mieć wiele Body,
ale **jedno Body = jedna bryła**. Jeśli operacja rozerwie model na dwie rozłączne części,
FreeCAD krzyknie błędem — i dobrze, bo to ten sam problem, co `Volumes: 3` w OpenSCAD
przy stykających się (a nie przenikających) bryłach.

**Tip (Wierzchołek).** Ostatnia operacja w drzewie — to, co widać jako aktualny kształt.
Można go cofnąć („Set tip") i wstawić coś w środek historii. To jest cała siła Part Design:
zmieniasz wymiar sprzed dziesięciu kroków i reszta się przelicza.

**Sketch (Szkic).** Płaski rysunek 2D przypięty do płaszczyzny. Szkic ma stan:
- **żółto-biały** = niedookreślony, ma stopnie swobody,
- **zielony** = **w pełni związany** (fully constrained) — każdy punkt ma wymuszone położenie.

Zasada: **nie wychodzisz ze szkicu, dopóki nie jest zielony.** Niedookreślony szkic wygląda
identycznie, a po zmianie dowolnego wymiaru potrafi się złożyć w harmonijkę, bo FreeCAD
sam wybierze, co przesunąć. Licznik stopni swobody jest na dole okna Sketchera
(„Fully constrained" albo „X degrees of freedom").

---

## Ile wymiarów potrzebuje kształt — i co się dzieje, gdy dasz o jeden za dużo

To jest najczęstsza pułapka Sketchera i **zielony szkic wcale przed nią nie chroni**.
Zielony znaczy tylko „nie ma stopni swobody", a nie „kształt jest taki, jak chciałeś".

### Jak to policzyć

Zamknięty czworokąt (4 linie) ma na starcie **8 stopni swobody**. Każdy więz je odbiera:

| Więz | Ile odbiera |
|---|---|
| punkt na osi | 1 |
| symetria dwóch punktów względem osi | 2 |
| poziomo / pionowo | 1 |
| każdy wymiar (długość, kąt) | 1 |

### Trapez keycapa — komplet więzów

Profil boku keycapa: podstawa na osi poziomej, symetryczny względem osi pionowej.

```
punkt lewy dolny na osi X                 -1   ->  7
symetria dolnych punktów wzgl. osi Y      -2   ->  5
symetria górnych punktów wzgl. osi Y      -2   ->  3
```

Zostają **dokładnie 3 stopnie swobody = dokładnie 3 wymiary**: szerokość podstawy,
szerokość góry, wysokość.

Uwaga na dwie pokusy, które po symetrii są już **nadmiarowe**:
- „poziomo" na górnej krawędzi — symetria górnych punktów już ją wymusza,
- drugi punkt dolny na osi X — symetria dolnych punktów już go tam trzyma.

FreeCAD zgłosi je jako *redundant constraints*.

### Dlaczego kąt boku to ten jeden za dużo

Podstawa, góra i wysokość **wyznaczają kąt boku**. Nie da się go dołożyć jako czwartej
niezależnej liczby, bo on już wynika z tamtych trzech:

| Podstawa | Góra | Wysokość | Kąt boku do poziomu |
|---|---|---|---|
| 18 | 13 | 11 | **77,2°** |
| 18 | 15,3 | 11 | 83° |

Jeśli mimo to wymusisz 83° **po jednej stronie**, a szerokość góry po drugiej, szkic da się
w pełni związać — tylko wyjdzie **niesymetryczny**: górna krawędź ucieknie w bok, bo nic
nie każe jej stać na środku. Będzie zielony i będzie zły.

Sygnał ostrzegawczy: figura, która miała być symetryczna, nie jest.
Nie przyglądaj się liczbom — przyglądaj się kształtowi.

### Reguła na przyszłość

> Najpierw **symetrie i więzy geometryczne**, dopiero potem wymiary.
> Wymiarów dokładaj tyle, ile zostało stopni swobody — licznik na dole okna Sketchera
> odlicza Ci to na bieżąco. Kiedy dojdzie do zera, **przestań**.

Wymiary wybieraj takie, które umiesz porównać z rzeczywistością. Szerokość podstawy
i wysokość przyłożysz do prawdziwego keycapa. Kąta boku nie przyłożysz do niczego —
niech będzie wynikiem, nie założeniem.

## Płaszczyzny i po czym szkicować

Nowe Body ma trzy płaszczyzny bazowe: **XY**, **XZ**, **YZ**. Szkicuj po nich zawsze, gdy się da.

**Nie szkicuj po ściankach modelu**, jeśli nie musisz. Ścianka to wynik poprzednich operacji —
gdy zmienisz wymiar, ścianka może zmienić numer albo zniknąć, a szkic zostanie bez podparcia.
FreeCAD 1.0 naprawił to w dużej mierze (to jest ten słynny *toponaming*) i dziś jest to
znacznie bezpieczniejsze niż w 0.19, ale nawyk zostaje: **płaszczyzna odniesienia
(Datum Plane) jest stabilna, ścianka nie.**

Kiedy potrzebujesz szkicu „5 mm nad czymś" — zrób **Datum Plane** z offsetem od płaszczyzny
bazowej i szkicuj po niej. Offset też może pochodzić z arkusza.

---

## Arkusz parametrów — jak to podpiąć

1. Warsztat **Spreadsheet** → **Create spreadsheet**. Nazwij go `Arkusz`.
2. W kolumnie A wpisuj opis, w kolumnie B wartość **z jednostką**: `18 mm`, `1.17 mm`, `9 deg`.
3. Zaznacz komórkę B → pole **Alias** (nad arkuszem) → wpisz nazwę, np. `szer_podstawy`.
   Komórka z aliasem robi się żółta.
4. W dowolnym polu wymiaru w FreeCAD kliknij małą **niebieską ikonę `fx`** (wyrażenie) i wpisz:
   `Arkusz.szer_podstawy`
5. Pole wymiaru zmieni się na niebieskie — to znaczy „sterowane wyrażeniem".

**Nazwy aliasów: tylko ASCII, bez spacji, bez polskich znaków.** `szer_gory`, nie `szer_góry`.
Diakrytyki w aliasie potrafią przejść przy wpisywaniu i wysypać się przy przeliczaniu.

Wyrażenia liczą: `Arkusz.szer_podstawy - 2 * Arkusz.gr_scianki` jest legalne.
To jest dokładnie to samo, co robisz w `.scad`.

---

## Kolejność operacji, która nie sprawia bólu

1. **Bryła główna** (Pad / Loft / Revolution) — surowy kształt zewnętrzny.
2. **Wydrążenie** (Thickness) albo duże ubytki (Pocket).
3. **Detale wewnętrzne** (gniazda, otwory, żeberka).
4. **Fillet / Chamfer na samym końcu.**

Punkt 4 jest nienegocjowalny. Zaokrąglenie zjada krawędź, której późniejsza operacja
mogła potrzebować jako odniesienia. Jeśli zrobisz fillet za wcześnie, a potem dołożysz otwór —
przy każdej zmianie wymiaru model będzie się sypał w tym jednym miejscu i nie będziesz wiedział, czemu.

---

## Eksport do druku

Zaznacz **Body** (nie Pad, nie szkic) → **File → Export** → `STL Mesh (*.stl)`.

W Preferences → Import-Export → Mesh Formats ustaw **maksymalne odchyłki siatki**
(„Maximum deviation") na mniej niż domyślne, np. **0.01 mm** — inaczej okrągłe kształty
wyjdą widocznie kanciaste. To jest odpowiednik `$fn` w OpenSCAD.

Plik źródłowy `.FCStd` idzie do `cad/`, eksport do `stl/`. Oba commitujemy.
