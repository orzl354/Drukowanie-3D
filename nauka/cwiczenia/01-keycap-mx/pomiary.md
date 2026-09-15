# Dopasowanie keycapa — metoda bez suwmiarki

Nie mam suwmiarki, więc **przyrządami pomiarowymi są: oryginalny keycap, klawiatura
i sama drukarka.** To nie jest gorszy zastępnik — dla tej części jest wręcz trafniejszy,
bo interesuje nas nie „ile ma milimetrów", tylko „czy pasuje do sąsiadów".

> Suwmiarkę i tak warto kupić — elektroniczna 150 mm to wydatek rzędu 40–70 zł
> i najbardziej przydatne narzędzie w druku 3D po samej drukarce. Ale nie czekamy na nią.

---

## Skąd bierzemy trzy potrzebne liczby

| Parametr | Skąd | Kiedy |
|---|---|---|
| `krzyz_luz` | drabinka [`kalibracja/01-gniazdo-mx`](../../../kalibracja/01-gniazdo-mx/) — pasowanie, nie pomiar | **przed** modelowaniem |
| `wys_calk` | porównanie 1: keycap obok keycapa na stole | po pierwszym wydruku |
| `gniazdo_od_dolu` | porównanie 2: keycap na klawiaturze obok sąsiada | po pierwszym wydruku |

`szer_podstawy` i `szer_gory` zostawiamy bez zmian — 18 mm przy rozstawie 19,05 mm
daje właściwą szczelinę, a szerokość wierzchu to czysta estetyka. Nie ma tu czego mierzyć.

---

## Jak zobaczyć dziesiąte części milimetra bez narzędzi

**Sztuczka z warstwą.** Drukujesz warstwą 0,12 mm. Boczna ścianka wydruku ma widoczne
prążki co dokładnie tę wartość. Jeśli Twój keycap jest niższy od oryginału o cztery prążki —
różnica wynosi 0,48 mm. Masz linijkę z podziałką 0,12 mm wbudowaną w każdy wydruk.

**Sztuczka ze światłem.** Połóż obie części na czymś płaskim (szkło, blat, okładka książki)
i przyłóż w poprzek wierzchów sztywną prostą krawędź — plastikową kartę, grzbiet linijki,
brzeg pudełka. Szczelina poniżej 0,1 mm jest widoczna pod światło jako jasny pasek.
Oko wyłapuje tu znacznie mniej, niż zmierzyłoby się linijką.

---

## Porównanie 1 — `wys_calk` (na stole)

Postaw obok siebie **oryginalny Esc** i **wydrukowany keycap**, oba dolną krawędzią do blatu.
Przyłóż prostą krawędź w poprzek.

Oryginał ma wierzch pochylony, więc porównuj z jego **przednią** krawędzią — to ten punkt,
któremu odpowiada nasz płaski wierzch.

| Co widzisz | Co zrobić w arkuszu |
|---|---|
| wydruk niższy o `x` | `wys_calk` + `x` |
| wydruk wyższy o `x` | `wys_calk` − `x` |
| równo | nie ruszaj |

## Porównanie 2 — `gniazdo_od_dolu` (na klawiaturze)

Załóż wydrukowany keycap na przełącznik Esc. Obok, na swoim miejscu, zostaw **oryginalną
jedynkę** — jest z tego samego rzędu, więc jest uczciwym punktem odniesienia.
Przyłóż prostą krawędź w poprzek obu.

Robisz to **po** wyrównaniu `wys_calk`, inaczej zmieszasz dwa błędy w jeden.

| Co widzisz | Co to znaczy | Co zrobić w arkuszu |
|---|---|---|
| wydruk **sterczy** o `x` | gniazdo za płytkie, keycap nie nasuwa się dość głęboko | `gniazdo_od_dolu` + `x` |
| wydruk **wsiąka** o `x` | gniazdo za głębokie | `gniazdo_od_dolu` − `x` |
| równo | gotowe | — |

## Test skoku — ważniejszy niż wygląd

Naciskaj na przemian wydrukowany Esc i sąsiednią jedynkę. Szukasz różnicy w **głębokości
i charakterze** ruchu.

- Klawisz zatrzymuje się wyżej, kończy „twardo", jakby uderzał w coś sztywnego →
  **dolna krawędź siada na obudowie przełącznika przed końcem skoku.**
  Zmniejsz `gniazdo_od_dolu` o 0,5 mm i drukuj ponownie.
- Skok taki sam jak u sąsiada → w porządku.

Ten objaw ma pierwszeństwo przed wyglądem. Klawisz o skróconym skoku jest wadliwy,
klawisz stojący 0,3 mm za wysoko jest tylko brzydki.

---

## Dziennik dopasowania

| Wydruk | `wys_calk` | `gniazdo_od_dolu` | `krzyz_luz` | Co zaobserwowałem | Poprawka |
|---|---|---|---|---|---|
| v1-a | 9.5 | 7.0 | | | |
| v1-b | | | | | |
| v1-c | | | | | |

Gotowe, gdy: keycap trzyma się po odwróceniu klawiatury, ma taki sam skok jak sąsiad,
a wierzch stoi równo z jedynką.

---

## Gdy kupisz suwmiarkę

Wtedy warto zmierzyć oryginał wprost i wpisać liczby od razu, zamiast iterować.
Tabela do wypełnienia:

**Data:** ____________ **Mierzony klawisz:** Esc

| # | Co mierzysz | Wartość | Alias |
|---|---|---|---|
| A1 | szerokość podstawy | ______ mm | `szer_podstawy` |
| A3 | szerokość wierzchu | ______ mm | `szer_gory` |
| A4 | wysokość całkowita **z przodu** | ______ mm | `wys_calk` |
| A5 | wysokość całkowita **z tyłu** | ______ mm | → A5 − A4 = pochylenie rzędu, lekcja 2 |
| A6 | głębokość wgłębienia (dish) | ______ mm | lekcja 2 |
| B1 | głębokość wewnętrzna (do sufitu) | ______ mm | kontrola: ≈ `wys_calk` − `gr_scianki` |
| B2 | grubość ścianki bocznej | ______ mm | porównanie z `gr_scianki` = 1,2 |
| B3 | od dolnej krawędzi do dna gniazda | ______ mm | **`gniazdo_od_dolu`** |
| D1 | rozstaw środków sąsiednich klawiszy | ______ mm | spodziewane 19,05 |

> **A5 − A4** to jest ta wartość, o którą płaska v1 jest z tyłu niższa od sąsiadów,
> i pierwszy parametr lekcji 2. Jeśli wyjdzie poniżej ~0,5 mm — Twoje keycapy mają rzędy
> o płaskim wierzchu (profil w typie DSA/XDA), v1 pasuje od razu, a lekcja 2 zmienia zakres.
