# keycap-mx-1u

Zamiennik keycapa 1u na przełącznik MX do klawiatury **Skyloong GK630K Onyx White**
(oryginalne klawisze: pudding). Pierwszy projekt robiony we **FreeCAD**, nie w OpenSCAD.

**Klawisz docelowy: Escape.** Przełączniki potwierdzone — trzpień **krzyżowy MX**
(sprawdzone po zdjęciu klawisza, 2026-09-15).

Prowadzenie krok po kroku: [`nauka/cwiczenia/01-keycap-mx/`](../../nauka/cwiczenia/01-keycap-mx/)
Lista kroków na teraz: [`START.md`](../../nauka/cwiczenia/01-keycap-mx/START.md)

## Cel

Nauczyć się Part Design na przedmiocie, który ma twarde, weryfikowalne kryterium sukcesu:
albo klawisz wchodzi na przełącznik i ma pełny skok, albo nie. Docelowo — własny zestaw
klawiszy akcentowych (Esc, strzałki) w innym kolorze niż reszta.

**Dlaczego akurat Esc:** leży w narożniku, ma jednego sąsiada, jest naturalnym klawiszem
akcentowym (wydruk w innym kolorze wygląda na zamysł, nie na protezę) i nie bierze udziału
w pisaniu na ślepo — różnica w profilu nie przeszkadza w pracy.

**Czym za to płacimy:** Esc siedzi w górnym rzędzie, a ten ma największe pochylenie wierzchu.
Płaska v1 wyjdzie mniej więcej na wysokości przedniej krawędzi oryginału, czyli z tyłu będzie
niższa od sąsiadów o różnicę `A5 − A4` z pomiarów. Świadomy kompromis na jeden wydruk —
lekcja 2 to naprawia.

Wersjonowanie:

| Wersja | Zakres | Status |
|---|---|---|
| **v1** | 1u, **płaski wierzch**, bez pochylenia rzędu, bez zaokrągleń, **bez legendy** | modelowanie |
| v2 | wgłębienie pod palec (dish), **pochylenie górnego rzędu**, fazy | — |
| v3 | rodzina: rzędy R1–R4, rozmiary 1.25u / 2u | — |
| v4 | legenda „ESC” w drugim kolorze (AMS Lite) | — |

## Materiał

| Zastosowanie | Filament | Dlaczego |
|---|---|---|
| Egzemplarze testowe (pasowanie) | **PLA Matte** | tani, stabilny wymiarowo, matowa faktura dobrze udaje keycapa; do sprawdzenia pasowania w zupełności wystarczy |
| Wersja akcentowa | **PLA Matte, kolor kontrastowy** | Esc to klawisz akcentowy — na białej klawiaturze wydruk w wyraźnym kolorze czyta się jako zamysł, a nie jako niedoróbka profilu |
| Wersja „na klawiaturę" | **PETG (czarny)** | lepsza odporność na ścieranie i na tłuszcz z palców niż PLA — **do zweryfikowania w praktyce, nie mam jeszcze przebiegu** |

**ASA nie ma tu sensu** — klawiatura stoi na biurku, nie w aucie. Odporność na 60 °C
nie jest potrzebna, a ASA na otwartej A1 tylko dołoży warpingu przy podstawie 18 × 18 mm.

Uwaga o oryginałach: klawisze pudding są dwuskładnikowe (przezroczysta spódnica + kryjący
wierzch) i wtryskiwane — wydruk FDM nie odtworzy ani przezierności, ani gładzi wtrysku.
Efekt „pudding" wraca dopiero w v4, przez druk dwukolorowy z AMS Lite.

## Ustawienia druku

> Wartości startowe. Oznaczone **[T]** wymagają potwierdzenia testem na mojej A1.

| | |
|---|---|
| Warstwa | 0.12–0.16 mm **[T]** — niżej = czystsze gniazdo, ale dłużej |
| Wypełnienie | 15% (ścianki i tak się schodzą, wypełnienie prawie nie występuje) |
| Ścianki (perymetry) | **3** — przy dyszy 0.4 daje ok. 1.2 mm, czyli minimum z `CLAUDE.md` |
| Orientacja na stole | **wierzchem do stołu, trzpieniem do góry** |
| Podpory | **brak** — ścianki rozchylają się ok. 14° od pionu, boss rośnie ku górze |
| Brim | niepotrzebny; jeśli odrywa, 5 mm **[T]** |
| Chłodzenie | **min. czas warstwy 8–10 s albo 4+ sztuk naraz [T]** — warstwa ma tu ok. 2 cm², bez tego warstwy nakładają się na gorące i gniazdo „pływa" |
| Uwagi | pierwsza warstwa to wierzch klawisza — teksturowany PEI odciśnie się jako matowa faktura pod palcem |

Dlaczego taka orientacja i dlaczego v1 ma płaski wierzch — uzasadnienie w sekcji
„Orientacja druku" w [lekcji 1](../../nauka/cwiczenia/01-keycap-mx/README.md).

## Zależności

| Co | Skąd | Bez tego |
|---|---|---|
| `krzyz_luz` | [`kalibracja/01-gniazdo-mx/`](../../kalibracja/01-gniazdo-mx/) — pasowanie, bez pomiaru | keycap nie wejdzie albo pęknie |
| `wys_calk` | porównanie z oryginałem na stole — [`pomiary.md`](../../nauka/cwiczenia/01-keycap-mx/pomiary.md) | keycap wyższy/niższy od sąsiadów |
| `gniazdo_od_dolu` | porównanie na klawiaturze — [`pomiary.md`](../../nauka/cwiczenia/01-keycap-mx/pomiary.md) | klawisz siedzi za wysoko albo ma skrócony skok |

Brak suwmiarki nie blokuje projektu: `krzyz_luz` wynika z pasowania drabinki,
a pozostałe dwa parametry z porównania wydruku z oryginałem. Iterujemy wydrukami —
jeden keycap to ok. 10 minut i grama filamentu.

## Status

`szkic` — model jeszcze nie zbudowany, kalibracja niewykonana, nic nie wydrukowane.
Wartości w arkuszu to placeholdery z lekcji.

Ustalone: klawisz docelowy **Esc**, przełącznik **MX (krzyż)**, orientacja druku
**wierzchem do stołu**, v1 **bez legendy** — napis dopiero w v4, drukiem dwukolorowym.
Tłoczenie albo grawer przy tej wysokości warstwy wyjdzie chropowate i będzie zbierać brud.

## Wnioski

_(uzupełniać po każdym wydruku)_

| Data | Wersja | Co wyszło | Co poprawić |
|---|---|---|---|
| | | | |
