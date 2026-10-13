# Organizer na biurko

Gotowy model z MakerWorld: *Office Desk Organizer* (autor: sebmar22, licencja
Standard Digital File License — Community Use). Nie projektuję go od nowa —
tu chodzi o **ustawienia druku pod wygląd**: gładkie boki, niewidoczny szew.

Plik do otwarcia w Bambu Studio: [`slicer/organizer_biurko_jakosc.3mf`](slicer/organizer_biurko_jakosc.3mf)

## Cel

Organizer stoi na widoku, więc liczy się wygląd ścian bocznych, a nie czas druku.
Gabaryty po imporcie: **164 × 72 × 85 mm** (oryginał był w calach, Bambu przeskalował ×6,43).

## Materiał

**PLA** (w projekcie: Bambu PLA Basic, czarny, slot 1 AMS).

**Sugestia: PLA Matte zamiast PLA Basic.** Matowa powierzchnia rozprasza światło,
więc linie warstw i szew są dużo mniej widoczne niż na błyszczącym PLA Basic —
to daje więcej „gładkości” niż jakakolwiek zmiana w procesie. Jeśli masz czarne
PLA Matte, wybierz je w slocie 1 (profil `Bambu PLA Matte @BBL A1`).

## Ustawienia druku

Bazą jest `0.20mm Standard @BBL A1`, zmienione parametry poniżej (w Bambu Studio
widać je jako zmodyfikowane, z gwiazdką).

| parametr | było | jest | dlaczego |
|---|---|---|---|
| Wysokość warstwy | 0,20 | **0,12** | Cieńsze warstwy = płytsze „schodki” na bokach. Pierwsza warstwa zostaje 0,2 dla przyczepności. |
| Ścianki | 2 | **3** | Wzór wypełnienia nie przebija na zewnątrz (tzw. *infill print-through*), sztywniejsze ścianki. |
| Prędkość ściany zewnętrznej | 200 mm/s | **60 mm/s** | Najważniejsza zmiana: wolna ściana zewnętrzna = równa ekstruzja, brak *ringingu* (falowania za narożnikami) i VFA (pionowe prążki od silników). |
| Przyspieszenie ściany zewnętrznej | 5000 | **2000** | Mniej szarpnięć na narożnikach = mniej ech/falowania. |
| Ściany wewnętrzne | 300 mm/s, accel 0 | **150 mm/s, 4000** | Spokojniejsza ściana wewnętrzna daje równe podparcie dla zewnętrznej. |
| Wypełnianie szczelin | 250 | **100 mm/s** | Mniej zgrubień w wąskich miejscach. |
| Precyzyjna ściana zewn. | wył. | **wł.** | Lepsza dokładność wymiarowa ściany zewnętrznej. |
| Pozycja szwu | wyrównany | **z tyłu** | Szew ląduje na tylnej ścianie — od frontu go nie widać. |
| Szew scarf | wył. | **wł. (zewnętrzny, inteligentny)** | Zamiast „kreski” szwu początek i koniec pętli zachodzą na siebie ukośnie — szew prawie znika. |
| Prasowanie (ironing) | brak | **górne powierzchnie** | Dna przegródek i górne krawędzie widać z góry — prasowanie robi z nich gładką taflę. |
| Górne powierzchnie | 200 mm/s | **100 mm/s, accel 1500** | Równiejsze linie na powierzchniach widocznych z góry. |
| Warstwy dolne | 3 | **5 (min. 0,8 mm)** | Przy warstwie 0,12 trzy warstwy to tylko 0,36 mm — za cienko. |
| Unikaj przejazdów przez ściany | wył. | **wł.** | Dysza nie przecina ścian zewnętrznych w ruchu jałowym — brak śladów i „włosków”. |
| Wypełnienie (obiekt) | 10 % zig-zag | **15 % gyroid** | Gyroid równomiernie podpiera ścianki we wszystkich kierunkach. |
| Podpory | wł. | **wył.** | Sprawdziłem siatkę: nawisów >45° jest ~85 mm² rozsianych po krawędziach — podpory tylko zostawiłyby ślady. |
| Brim | auto | **brak** | Duża, płaska podstawa na PEI trzyma się sama; brim zostawia nierówną krawędź na dole. |
| Kompensacja stopy słonia | 0,075 | **0,10 mm** | Mniej rozlanej pierwszej warstwy na dolnej krawędzi. |
| Wieża czyszcząca | wł. | **wył.** | Drukujesz jednym kolorem — wieża niepotrzebna. |
| Mnożnik płukania | 0 | **1** | Usuwa ostrzeżenie „objętość płukania = 0” (dotyczy tylko druku wielokolorowego). |

| | |
|---|---|
| Orientacja na stole | jak w pliku — podstawą do stołu |
| Podpory | nie |
| Szacowany czas | ok. 7–9 h (dokładny pokaże slicer; było 3 h 46 min) — **do sprawdzenia** |

### Zanim klikniesz „Drukuj”

1. **Obróć model tak, żeby ładny front patrzył do przodu stołu (w stronę −Y).** Szew
   jest ustawiony „z tyłu”, czyli na stronie od tyłu drukarki.
2. W podglądzie po pocięciu włącz „Szwy” i sprawdź, czy białe kreski są na tylnej ścianie.
3. Ostrzeżenie o siatce >1 mln trójkątów można zignorować (wolniej się tnie, druk się nie zmienia).
   Uproszczenie siatki potrafi „ściąć” zaokrąglenia, więc nie upraszczałem.

### Wymaga testu na mojej A1

- **Prasowanie**: przepływ 10 % / 30 mm/s to wartości domyślne. Jeśli na dnie
  przegródek widać rowki — podnieś przepływ do 15 %; jeśli nadlewki — obniż do 8 %.
- **60 mm/s ściany zewnętrznej**: przy wyraźnych pionowych prążkach (VFA) spróbuj 50 lub 80 mm/s —
  VFA zależą od konkretnej prędkości silników.
- **Stopa słonia 0,10**: jeśli dolna krawędź nadal odstaje, zwiększ do 0,15.

## Status

`szkic` — ustawienia przygotowane, czeka na wydruk.

## Wnioski

_(do uzupełnienia po wydruku: zdjęcie boku pod światło, widoczność szwu, czas rzeczywisty)_
