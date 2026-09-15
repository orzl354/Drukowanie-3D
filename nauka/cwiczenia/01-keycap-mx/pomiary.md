# Pomiary oryginalnego keycapa — GK630K Onyx White (pudding)

> Wypełnij suwmiarką **przed** modelowaniem. Liczby stąd wpisujesz do arkusza we FreeCAD.
> Nie kopiuj wartości „typowych z internetu" — profile keycapów różnią się między producentami,
> a my robimy zamiennik do **tej** klawiatury.

**Data pomiaru:** ____________
**Mierzony klawisz:** **Esc** (górny rząd) — ten sam, który zastępujemy
**Suwmiarka:** ____________ (elektroniczna / zegarowa, rozdzielczość)

> Jeśli nie masz suwmiarki: zmierz przynajmniej **B1** (głębokość wewnętrzna) —
> da się to zrobić wykałaczką i linijką z dokładnością ~0,5 mm, wkładając ją do środka
> keycapa aż do oporu i zaznaczając paznokciem poziom krawędzi. To gorsze niż suwmiarka,
> ale nadal lepsze niż liczba wzięta z internetu. Resztę wymiarów zewnętrznych da się
> odrysować ołówkiem na kartce w kratkę. Powiedz mi, jeśli tak wychodzi — przestawię
> kolejność tak, żeby drabinka kalibracyjna poszła pierwsza.

---

## A. Wymiary zewnętrzne

| # | Co mierzysz | Jak | Wartość | Trafia do aliasu |
|---|---|---|---|---|
| A1 | szerokość podstawy (lewo–prawo) | najszersze miejsce dolnej krawędzi | ______ mm | `szer_podstawy` |
| A2 | głębokość podstawy (przód–tył) | j.w., w drugiej osi | ______ mm | — (jeśli ≠ A1, powiedz mi) |
| A3 | szerokość wierzchu | górna płaszczyzna, lewo–prawo | ______ mm | `szer_gory` |
| A4 | wysokość całkowita z przodu | od dolnej krawędzi do najniższego punktu wierzchu | ______ mm | kontrola `wys_calk` |
| A5 | wysokość całkowita z tyłu | j.w., z tyłu | ______ mm | → różnica A5−A4 = **pochylenie rzędu**; w górnym rzędzie jest największa, patrz niżej |
| A6 | głębokość wgłębienia (dish) | linijka w poprzek wierzchu, szczelina w środku | ______ mm | lekcja 2 |

> **A4 i A5 na klawiszu Esc.** Esc jest w górnym rzędzie, więc spodziewaj się największej
> różnicy A5 − A4 z całej klawiatury. Zanotuj ją — to jest dokładnie ta wartość, o którą
> płaska v1 będzie z tyłu niższa od sąsiadów, i to jest pierwszy parametr lekcji 2.
> Jeśli A5 − A4 wyjdzie poniżej ~0,5 mm, to znaczy, że Twoje keycapy mają rzędy o płaskim
> wierzchu (profil w typie DSA/XDA) — wtedy v1 będzie **od razu** pasowała do reszty
> i lekcja 2 zmienia zakres. Napisz mi, ile wyszło.

## B. Wymiary wewnętrzne — te decydują, czy klawisz zadziała

| # | Co mierzysz | Jak | Wartość | Trafia do aliasu |
|---|---|---|---|---|
| B1 | **głębokość wewnętrzna** | głębokościomierz suwmiarki: od dolnej krawędzi do wewnętrznego sufitu | ______ mm | **`gleb_wew`** |
| B2 | grubość ścianki bocznej | szczęki suwmiarki na krawędzi spódnicy | ______ mm | porównaj z `gr_scianki` = 1.2 |
| B3 | wysokość bossa (słupka z krzyżem) | od sufitu w dół do dolnej krawędzi bossa | ______ mm | kontrola `boss_wys` |
| B4 | średnica / szerokość bossa | ______ mm | kontrola `boss_srednica` |

> **B1 jest najważniejszą liczbą w całej tabeli.** Jeśli ją zaniżysz, klawisz będzie miał
> skrócony skok — spódnica usiądzie na obudowie przełącznika przed końcem ruchu.
> Jeśli zawyżysz, keycap będzie „pływał" wyżej niż sąsiedzi.
> Zmierz dwa razy, w dwóch miejscach.

## C. Przełącznik (keycap zdjęty)

| # | Co sprawdzasz | Wartość / odpowiedź |
|---|---|---|
| C1 | Kształt trzpienia | krzyż (MX) / dwa kołki (Choc) / inny: ______ |
| C2 | Marka na obudowie przełącznika | ______ |
| C3 | Wysokość trzpienia nad obudową (stan spoczynku) | ______ mm |
| C4 | Ramię krzyża — długość | ______ mm (nominał 4,10) |
| C5 | Ramię krzyża — grubość | ______ mm (nominał 1,17) |
| C6 | Prześwit pod krawędzią keycapa do płytki (stan spoczynku) | ______ mm — musi być **> 4 mm** (skok) |

> C4 i C5 mierzy się trudno, bo szczęki suwmiarki ślizgają się po ukosach trzpienia.
> Jeśli wyjdzie coś w granicach 4,0–4,2 i 1,1–1,3 — nominał jest w porządku, jedziemy dalej.
> Liczy się i tak wynik **drabinki kalibracyjnej**, nie ten pomiar.

## D. Kontrola sąsiedztwa

| # | Co | Wartość |
|---|---|---|
| D1 | rozstaw środków dwóch sąsiednich klawiszy | ______ mm (spodziewane 19,05) |
| D2 | szczelina między sąsiednimi keycapami | ______ mm |

---

## Wnioski z pomiarów

Które wartości startowe z lekcji okazały się nietrafione i o ile:

```
```
