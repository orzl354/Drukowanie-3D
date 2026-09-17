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

## 2026-09-17 — podział modelu malowanego MMU na osobne części kolorystyczne

**Co robiłem:** wziąłem gotowy keycap „Psyduck" z MakerWorld (projekt Bambu
Studio z malowaniem MMU na 4 kolory) i rozciąłem go na 8 osobnych brył — po
jednej na kolor — żeby drukować bez zmian filamentu i bez wieży czyszczącej.
Projekt: `projekty/psyduck-keycap-multicolor/`.

**Czego się nauczyłem:**

1. **Malowanie MMU w 3MF to gotowa mapa cięcia.** Atrybut `paint_color` przy
   trójkącie to zserializowane drzewo podziału (kodowanie `TriangleSelector`
   z PrusaSlicer): 2 bity „ile boków podzielonych", potem albo rekurencja,
   albo 2 bity stanu, a przy stanie ≥3 jeszcze 4 bity. Bity czyta się od
   **ostatniego znaku** stringa, w każdym półbajcie od najmłodszego. 4402
   pomalowane trójkąty zdekodowały się bez błędu — sprawdzian poprawności to
   „czy po zdekodowaniu zostały same zera dopełnienia".

2. **Zanim zacznę ciąć, warto poszukać gotowego szwu.** Model miał płaską
   granicę kaczka/baza keycapa na `z = -3,619` i **zero trójkątów przecinających
   tę płaszczyznę** — ślad po tym, że autor złożył go z dwóch brył. Cięcie tam
   jest darmowe i idealne. Szukanie takich miejsc = policzyć, ile ścian przecina
   kandydującą płaszczyznę.

3. **Czop i gniazdo z tej samej powierzchni.** Zamiast robić gniazdo osobno:
   buduję bryłę „powierzchnia obszaru + ścianki wzdłuż kierunku + płaskie dno"
   dwa razy — raz ze zbieżnością (czop), raz bez (gniazdo). Krawędź na
   powierzchni jest w obu identyczna, więc **szew jest niewidoczny**, a luz
   siedzi dopiero w głębi, gdzie i tak potrzeba miejsca na klej. Lepsze niż
   równomierny luz, który daje widoczną szczelinę dookoła.

4. **Kierunek czopa to decyzja montażowa.** Dziób wyciągnięty poziomo w głąb
   głowy wyglądał poprawnie, a jego gniazdo **zachodziło na gniazda oczu** —
   nie dałoby się włożyć obu. Przechylenie czopa o 30° w dół rozwiązało sprawę.
   Wniosek: test „czy któreś dwie części się przenikają" (boolean intersection
   każdej pary) musi być w skrypcie na stałe, bo okiem tego nie widać.

5. **Odsunięcie wielokąta do środka — dwie pułapki naraz.** Znak normalnej
   trzeba wziąć z pola ze znakiem (CCW → wnętrze po lewej, `[-ey, ex]`),
   a na narożniku iść po dwusiecznej `d·(n₁+n₂)/(1+n₁·n₂)`, nie po
   znormalizowanej sumie. Pomyliłem znak i **czopy wyszły większe od gniazd** —
   wszystkie testy „czy bryła szczelna" przechodziły, bo szczelna była.
   Złapał to dopiero test **„czop minus gniazdo = 0 mm³"**. Morał: sprawdzać
   relację między częściami, nie tylko poprawność każdej z osobna.

6. **`is_watertight` nie wystarcza.** Po cięciu płaszczyzną `slice_mesh_plane`
   zostawiło 56 zdegenerowanych ścian o zerowym polu — bryła „prawie" szczelna,
   ale boolean ją odrzucał („Not all meshes are volumes"). Cięcie tą samą
   płaszczyzną, ale jako **boolean z dużym prostopadłościanem** (manifold3d),
   dało czysty wynik. Do kompletu: po erozji obrysu zostają okruchy 0,02 mm³
   jako osobne bryły — stąd kontrola `body_count == 1`.

7. **Nie każdy kolor nadaje się na osobną część.** Źrenice mają 0,5 × 0,25 mm
   i leżą **płasko** na kule oka (odchyłka −0,02 mm — czyli to czyste malowanie,
   nie geometria). Nozdrza 0,5 × 0,9 mm. Granica sensu przy dyszy 0,4 to
   mniej więcej 1,5–2 mm najmniejszego wymiaru — poniżej tego marker, nie klej.

8. **Jedna płyta ≠ jedno zadanie.** Rozmieszczenie 4 kolorów na jednej płycie
   samo z siebie nie eliminuje zmian filamentu — na jednej dyszy i tak byłyby
   co warstwę. Bez zmian = 4 osobne zadania z tej samej płyty, przełączając
   obiekty na „niedrukowalne".

**Co nie wyszło / do sprawdzenia:** nic jeszcze nie wydrukowane. Do weryfikacji
na A1: czy luz 0,10 mm jest dobry dla wciskanych czopów, czy skośny strop
gniazda dzioba nie obwiśnie za bardzo, czy włoski 0,5 mm wyjdą.

**Następny krok:** wydrukować 4 zadania i złożyć; wynik luzu przenieść do
`kalibracja/` jako punkt odniesienia dla wklejanych wkładek kolorystycznych.

---

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
