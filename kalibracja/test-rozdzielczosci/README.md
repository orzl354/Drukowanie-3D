# Test rozdzielczości małych detali

Odpowiada na jedno pytanie: **jak cienki detal wychodzi jeszcze używalny
na A1 z dyszą 0.4?** Potrzebne, zanim zaczniemy cokolwiek projektować
w skali modelarskiej (1:64 / 1:43 / 1:24), bo tam większość elementów
ląduje poniżej 1 mm.

Model: [`cad/test-mini.py`](cad/test-mini.py) → [`cad/test-mini.FCStd`](cad/test-mini.FCStd)

## Cel

Płytka 56 × 30 × 1.6 mm z trzema strefami:

| strefa | co | wymiary | odpowiada elementowi |
|---|---|---|---|
| **A** — 8 żeber pionowych | ścianka stojąca, wys. 6 mm | 1.6 / 1.2 / 1.0 / 0.8 / 0.6 / 0.5 / 0.4 / 0.3 | statywy skrzydła, żebra dyfuzora, canardy |
| **B** — 6 kołków | walec, wys. 4 mm | Ø 1.6 / 1.2 / 1.0 / 0.8 / 0.6 / 0.4 | kołki pozycjonujące, łączenie części |
| **C** — 6 otworów | na wylot przez bazę | Ø 1.6 / 1.2 / 1.0 / 0.8 / 0.6 / 0.4 | gniazda pod te kołki |

Żebra i kołki idą **od najgrubszego (lewa) do najcieńszego (prawa)** —
na wydruku nie ma opisów, bo tekst w tej skali i tak by nie wyszedł.

Kołki i otwory mają **te same nominalne średnice** — po wydruku sprawdzasz,
który kołek wchodzi w który otwór. To daje realny luz pasowania na Twojej
maszynie, przy tej wielkości detalu.

## Materiał

**PLA** — najlepiej odwzorowuje drobne detale ze wszystkiego, co masz
(najniższa lepkość w temperaturze druku, najmniejsze puchnięcie strugi na wyjściu
z dyszy). Nawet jeśli docelowa część ma być z PETG, ten test rób na PLA:
chodzi o wyznaczenie granicy możliwości, nie o wytrzymałość.

## Ustawienia druku

> Punkt wyjścia, nie pewnik — po to jest ten wydruk.

| | |
|---|---|
| Warstwa | **0.12 mm** (niżej niż zwykle — detal, nie prędkość) |
| Ścianki | 2 |
| Wypełnienie | 15 % (baza i tak jest cienka) |
| Prędkość ścianek zewn. | **obniż do ~40 mm/s** — cienkie żebra mają małą podstawę i wibrują |
| Chłodzenie | 100 % |
| Orientacja | płasko, żebra i kołki do góry |
| Podpory | nie |
| Brim | nie |

### Zanim wyślesz na drukarkę — obejrzyj podgląd w Bambu Studio

Slicer potrafi **całkowicie pominąć** detal cieńszy niż szerokość ścieżki.
Jeśli w podglądzie żebra 0.4 i 0.3 nie mają żadnych linii — one się nie
wydrukują i to też jest wynik testu. Zanotuj, od której grubości slicer
przestaje cokolwiek generować, *zanim* zobaczysz, co wyszło z drukarki.

W Bambu Studio szukaj opcji **„Detect thin walls" / „Wykrywanie cienkich ścianek"** —
włączona zmienia wynik, więc zanotuj, w jakim stanie była.

## Jak ocenić wynik

Dla każdego żebra (od najgrubszego) zapisz:

- **jest / nie ma** — czy w ogóle się wydrukowało
- **stoi / faluje** — czy jest proste, czy pofalowane od nadmiaru ciepła
- **wytrzymuje paznokieć** — czy odłamie się przy lekkim nacisku z boku

Pierwsza grubość idąc od lewej, która przechodzi wszystkie trzy, to
**Twoje realne minimum dla pionowej ścianki** — ta liczba trafia potem
do `CLAUDE.md` obok obecnego 1.2 mm i decyduje, w jakiej skali w ogóle
opłaca się projektować.

Kołki: który najcieńszy nie ułamał się przy zdejmowaniu ze stołu.
Pasowanie: który kołek wchodzi w który otwór (opór / suwliwie / luźno).

## Status

**Wygenerowane, nie wydrukowane.**

Weryfikacja geometrii (FreeCAD, headless):

```
Baza     zwiazany=True   DOF=0
Zebra    zwiazany=True   DOF=0
Kolki    zwiazany=True   DOF=0
bryla valid  : True
bryl w czesci: 1
bbox [mm]    : 56.0 x 30.0 x 7.6
objetosc     : 3006.8 mm3
```

Przekrój na wysokości z = 4 mm potwierdza, że żebra mają dokładnie
1.600 / 1.200 / 1.000 / 0.800 / 0.600 / 0.500 / 0.400 / 0.300 mm,
a kołki Ø 1.600 / 1.200 / 1.000 / 0.800 / 0.600 / 0.400 mm.

Zużycie: ~3 cm³, czyli **poniżej 4 g** — test kosztuje tyle co nic.

## Wnioski

*(do uzupełnienia po wydruku)*

| żebro | grubość | wydrukowane? | proste? | wytrzymałe? |
|---|---|---|---|---|
| 1 | 1.6 | | | |
| 2 | 1.2 | | | |
| 3 | 1.0 | | | |
| 4 | 0.8 | | | |
| 5 | 0.6 | | | |
| 6 | 0.5 | | | |
| 7 | 0.4 | | | |
| 8 | 0.3 | | | |

**Realne minimum ścianki pionowej: ______ mm**

| kołek Ø | ocalał? | w który otwór wchodzi? |
|---|---|---|
| 1.6 | | |
| 1.2 | | |
| 1.0 | | |
| 0.8 | | |
| 0.6 | | |
| 0.4 | | |

## Edycja

Wszystkie wymiary siedzą w arkuszu `Parametry` w pliku `.FCStd` — otwórz
we FreeCAD, zmień liczbę, odśwież. Regeneracja od zera:

```bash
OUT_DIR=. freecadcmd cad/test-mini.py
```
