# Dziennik nauki

Jeden wpis = jedna sesja. Od najnowszych na górze.

Format wpisu:

```
## RRRR-MM-DD — temat

**Co robiłem:**
**Czego się nauczyłem:**
**Co nie wyszło / do sprawdzenia:**
**Następny krok:**
```

---

## 2026-09-17 — podział modelu malowanego kolorami na części jednokolorowe

**Co robiłem:** rozbiłem gotowy, malowany wielokolorowo model 3MF (pingwin-keycap
z MakerWorld) na 7 części jednokolorowych, żeby wydrukować go bez zmian filamentu
i bez wieży czyszczącej, wszystko na jednej płycie.
Projekt: `projekty/pingwin-keycap-multicolor/`.

**Czego się nauczyłem:**

1. **Kolor w 3MF to malowanie POWIERZCHNI, nie bryły.** Atrybut `paint_color` siedzi
   na pojedynczym trójkącie. Żadna płaszczyzna nie rozdzieli takich plam — sposób,
   który działa, to zamiana plamy na bryłę: powierzchnia modelu z przodu, płaska
   ściana z tyłu. Ta płaska ściana rozwiązuje przy okazji drugi problem: daje
   każdej części naturalną płaszczyznę do położenia na stole, więc podpory
   potrzebuje tylko korpus.

2. **Kierunek rzutowania musi być wspólny dla wszystkich plam.** Kuszące było
   rzutować każdą plamę wzdłuż jej własnej normalnej, ale wtedy obszary cięcia
   sąsiednich plam albo zachodzą na siebie, albo zostawiają papierowe wióry.
   Jeden wspólny kierunek jest lokalnie gorszy, za to daje podział dokładny —
   kontrola „suma objętości części = objętość bryły minus luzy" wychodzi co do mm³.

3. **Sylwetkę plamy licz jako sumę rzutów trójkątów, nie z konturu brzegu.**
   Stopy zawijają się do tyłu (42 % ich pola patrzy w bok albo do tyłu) i rzut
   konturu brzegu sam się przecina. Suma rzutów trójkątów z regułą NonZero jest
   na to odporna.

4. **Orientacja druku znowu wymusiła zmianę konstrukcji** — tak jak przy uchwycie.
   Chciałem zostawić oczy jako czopki na czarnym korpusie i zrobić dziury w białym
   froncie. Ale gniazdo frontu ma 6 mm głębokości, więc czopek oka wyszedłby
   1,9 × 1,0 × 3,8 mm sterczący **poziomo w powietrzu** w środku wnęki. Nie do
   wydrukowania. Oczy musiały zostać osobnymi wtopkami.

5. **Modele z „Image to 3D" mają ukryte śmieci w siatce.** 1,49 mln trójkątów
   (0,02 mm na trójkąt), 323 krawędzie brzegowe, 320 krawędzi użytych 3 razy —
   mikroskopijne płatki 0,02 mm. Slicer tego nie pokazuje, ale żaden boolean
   takiej siatki nie ruszy. Plus 463 plamki malowania < 1 mm² — szum po malowaniu.

6. **`float32` w STL potrafi rozszczelnić poprawną siatkę.** Części wychodziły
   szczelne, a po zapisie do STL już nie. Przy x ≈ 128 mm (środek płyty) krok
   `float32` jest osiem razy grubszy niż przy zerze i skleja sąsiednie wierzchołki
   w krawędź niemanifoldową. Wniosek na przyszłość: **siatkę domykaj na samym
   końcu, po wszystkich przesunięciach**, a pozycję na płycie nieś transformacją
   w 3MF, nie wpisuj jej w współrzędne wierzchołków.

7. **Podział na części to dopiero połowa roboty.** Same jednokolorowe obiekty na
   jednej płycie nadal powodują zmianę filamentu w każdej warstwie — dopiero
   kolejność druku „po obiekcie" schodzi z setek zmian do dwóch.

8. **Tryb „po obiekcie" dyktuje układ płyty, nie odwrotnie.** Upakowałem części
   ciasno (81 × 21 mm), a w tym trybie głowica objeżdża to, co już stoi, i wg
   profilu A1 potrzebuje wokół siebie **73 mm** (`extruder_clearance_max_radius`).
   Do tego `extruder_clearance_height_to_rod` = **25 mm** — powyżej tego belka
   portalu może zahaczyć o gotowy wydruk. Korpus ma 34 mm, więc musi być ostatni;
   wtedy nic już nad nim nie przejeżdża.

9. **Kolejność druku „po obiekcie" bierze się z listy obiektów, nie z położenia.**
   A lista to po prostu kolejność `<object>` w `3dmodel.model` — więc kolejność da
   się zapiec w pliku 3MF i nie trzeba nic przeciągać. W slicerze przeciąga się
   wiersze w `Proces` → `Obiekty`, a Ctrl+E pokazuje podpisy `Sekwencja#`.
   Uwaga: „od lewej do prawej" i „mało zmian filamentu" to dwa różne wymagania —
   pokrywają się tylko wtedy, gdy części ustawi się na płycie grupami kolorów.

**Co nie wyszło / do sprawdzenia:** nic jeszcze nie wydrukowane. Największy znak
zapytania to trzonek MX przy dyszy 0,4 mm (oryginał robiony pod 0,2 mm) — ścianki
krzyża ~1,2 mm i luzy ~1,3 mm są na granicy tego, co 0,4 trafia wymiarowo.
Drugi: luz wtopek 0,10 mm — wciąż liczba z `CLAUDE.md`, nie z pomiaru.

**Następny krok:** wydrukować sam `korpus` i przymierzyć do przełącznika, zanim
pójdzie reszta. To jeden druk i rozstrzyga, czy cała reszta ma sens.

## 2026-08-29 — uchwyt na telefon: pierwszy projekt parametryczny

**Co robiłem:** zaprojektowałem uchwyt na telefon na biurko (zacisk na krawędź
blatu, obrót w dwóch osiach) w OpenSCAD, w pełni parametrycznie.
Projekt: `projekty/uchwyt-telefon-biurko/`.

**Czego się nauczyłem:**

1. **Bryły w `union()` muszą się przenikać, nie stykać.** Grzbiet zacisku i jego
   ramiona miały wspólną płaszczyznę o zerowej grubości — CGAL zostawił z tego
   trzy rozłączne bryły zamiast jednej. Nachodzenie o 0,5–1 mm rozwiązuje sprawę.
   Sygnał ostrzegawczy: `Volumes:` większe niż 2 przy pojedynczej części.

2. **Kąt zwisu trzeba policzyć, nie ocenić okiem.** Skarpa pod zaczepem osi
   wyglądała dobrze na renderze, a wychodziła 46° — ponad limit. Liczy się
   styczna od podstawy skarpy do walca, nie linia między ich środkami.

3. **Orientacja druku potrafi wymusić zmianę konstrukcji.** Ogranicznik obrotu
   zrobiłem najpierw jako ząbek pod tarczą — a wtedy tarcza nie ma na czym leżeć
   na stole. Zamiana na rowek w tarczy + kołek na zacisku daje ten sam ruch
   i drukuje się bez podpór.

4. **Kinematykę da się przetestować przed drukiem**: przecięcie brył w różnych
   pozycjach. Gdy część wspólna jest pusta, OpenSCAD nie zapisuje pliku —
   to gotowy test „tak/nie”. Trzeba tylko sprawdzić kontrolą pozytywną, że
   detektor w ogóle działa; dwa razy dałem się nabrać na fałszywe „brak kolizji”
   (raz odczyt starego pliku, raz zepsuta ścieżka `include`).

5. **Render pokazał błąd, którego liczby nie pokazały**: telefon patrzył w głąb
   biurka, a skok ±90° nie pozwalał obrócić go do siebie. Geometria była poprawna,
   sens użytkowy nie.

**Co nie wyszło / do sprawdzenia:** nic jeszcze nie wydrukowane. Tolerancje
(`luz_ruchomy = 0,35`) wciąż z literatury, nie z pomiaru na mojej A1.

**Następny krok:** test tolerancji pasowań w `kalibracja/`, a potem druk uchwytu —
w tej kolejności, bo zaczep w widelcu i kołek w rowku stoją na tej jednej liczbie.

---

## 2026-08-29 — założenie repozytorium

**Co robiłem:** utworzyłem strukturę repo, `.gitignore` i szablon projektu.

**Czego się nauczyłem:** —

**Co nie wyszło / do sprawdzenia:** brak jeszcze jakichkolwiek pomiarów
z mojej A1 — wszystkie tolerancje w `CLAUDE.md` to na razie wartości
startowe z literatury, nie zmierzone na moim sprzęcie.

**Następny krok:** pierwszy druk kalibracyjny (test tolerancji pasowań),
żeby liczby w `kalibracja/` przestały być teoretyczne.
