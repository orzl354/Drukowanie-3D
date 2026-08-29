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
