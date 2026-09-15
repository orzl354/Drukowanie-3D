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

## 2026-09-15 — start kursu FreeCAD, projekt: keycap MX

**Co robiłem:** ustawiliśmy kurs FreeCAD (plan w `nauka/kurs-freecad.md`, wzorzec: kanał
CAD CAM Lessons), notatki modułu 0 i lekcję 1 — keycap 1u na przełącznik MX do GK630K.
Doszedł projekt `projekty/keycap-mx-1u/` i drabinka tolerancji `kalibracja/01-gniazdo-mx/`.
Samego modelu jeszcze nie zbudowałem — to jest zadanie na następną sesję.

**Czego się nauczyłem:** _(uzupełnić po zrobieniu lekcji 1)_

Do rozstrzygnięcia przy modelowaniu:

1. Czy arkusz (Spreadsheet) faktycznie daje mi to samo, co zmienne na górze pliku `.scad` —
   szczególnie: czy zmiana jednej wartości przelicza model bez błędów w drzewie.
2. Czy `Thickness` jest wygodniejszy od ręcznego liczenia wewnętrznego Loftu.
3. Ile realnie kosztuje pilnowanie, żeby każdy szkic był zielony.

**Co nie wyszło / do sprawdzenia:**

- **Nie mam suwmiarki.** Zmieniło to sposób pracy: zamiast mierzyć oryginał, dobieram
  dwa parametry porównując wydruk z sąsiednim klawiszem. Model dostał w związku z tym inną
  parametryzację — `wys_calk` i `gniazdo_od_dolu` zamiast głębokości wewnętrznej, bo każdy
  z nich ma własny, niezależny objaw przy oględzinach. Metoda: `pomiary.md`.
- Wartości startowe `wys_calk = 9.5` i `gniazdo_od_dolu = 7.0` to świadome zgadywanie
  w bezpieczną stronę (za nisko osadzony keycap jest brzydki, za głęboko osadzony ma
  skrócony skok). Poprawka po pierwszym wydruku.
- `krzyz_luz = 0.1` to placeholder do czasu odczytania drabinki.
- ~~Nie potwierdziłem, czy przełączniki mają trzpień krzyżowy MX~~ — **sprawdzone: krzyż MX**.
  Geometria gniazda 4,10 × 1,17 mm zostaje. Klawisz docelowy: **Esc**.
  Wybrany świadomie: narożnik, jeden sąsiad, klawisz akcentowy. Kosztem jest to, że górny
  rząd ma największe pochylenie wierzchu, a v1 jest płaska — z tyłu wyjdzie niżej niż sąsiad
  o różnicę A5 − A4 z pomiarów.
- Nadal brak jakichkolwiek własnych pomiarów kalibracyjnych z A1. Drabinka gniazda MX
  będzie pierwszym — i przy okazji da mi liczbę skurczu otworów pionowych,
  przydatną we wszystkich kolejnych projektach.

**Następny krok:** pomiary suwmiarką (`nauka/cwiczenia/01-keycap-mx/pomiary.md`),
druk drabinki `kalibracja/01-gniazdo-mx/`, dopiero potem FreeCAD.
W tej kolejności, bo cała lekcja 1 stoi na tych dwóch liczbach.

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
