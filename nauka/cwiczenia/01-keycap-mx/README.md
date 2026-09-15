# Lekcja 1 — keycap 1u na przełącznik MX (FreeCAD, Part Design)

**Cel:** zbudować w pełni parametryczny keycap, który wejdzie na przełącznik w GK630K,
i przy okazji nauczyć się szkieletu pracy w Part Design: arkusz → szkic → Loft → Thickness → Pocket.

**Czego jeszcze NIE robimy w tej lekcji:** wgłębienia pod palec (dish), pochylenia rzędu,
zaokrągleń. Wierzch będzie **płaski**. To nie jest uproszczenie „bo trudne" — to decyzja
konstrukcyjna, którą uzasadniam w sekcji „Orientacja druku". Dish dokładamy w lekcji 2.

Projekt zapisujemy w [`projekty/keycap-mx-1u/`](../../../projekty/keycap-mx-1u/).

---

## 1. Teoria — co w keycapie jest naprawdę krytyczne

Keycap to wydrążona, ścięta piramida z krzyżowym gniazdem pod spodem. Z wymiarów,
które go opisują, **tylko trzy decydują o tym, czy w ogóle zadziała**:

1. **Krzyż gniazda.** Trzpień MX to krzyż o nominale **4,10 × 1,17 mm**. Za ciasno — rozerwiesz
   keycapa albo wyrwiesz przełącznik z gniazda hot-swap. Za luźno — klawisz chodzi i spada.
   Otwory drukowane pionowo wychodzą **mniejsze niż w modelu** (skurcz + naddatek ścieżki),
   więc luzu nie zgadujemy — mierzymy go wydrukiem. To jest zadanie z
   [`kalibracja/01-gniazdo-mx/`](../../../kalibracja/01-gniazdo-mx/).

2. **Głębokość wewnętrzna** (od dolnej krawędzi do wewnętrznego sufitu). Klawisz ma **4 mm skoku**.
   Jeśli spódnica keycapa jest za długa, przy wciśnięciu usiądzie na obudowie przełącznika,
   zanim przełącznik dojdzie do końca — klawisz będzie „twardy" i płytki.
   Dlatego tę jedną liczbę **przepisujemy z oryginalnego keycapa**, nie wymyślamy.

3. **Szerokość podstawy.** Rozstaw klawiszy to 19,05 mm. Podstawa ~18 mm zostawia ok. 1 mm
   szczeliny. Zrób 18,6 i sąsiednie klawisze zaczną się ocierać.

Cała reszta (wysokość, szerokość wierzchu, kąt ścianek) to **estetyka i ergonomia** —
tu masz wolną rękę, byle profil pasował do sąsiadów w rzędzie.

### Zanim usiądziesz do FreeCAD

Wypełnij [`pomiary.md`](pomiary.md). Potrzebujesz suwmiarki i **jednego zdjętego keycapa**
(najlepiej z rzędu, w którym chcesz mieć zamiennik — np. `F` albo `J`).
Bez tych liczb będziesz modelował cudzy klawisz, nie swój.

> **Sprawdź od razu jedną rzecz:** po zdjęciu keycapa zobacz, czy trzpień przełącznika to
> **krzyż** (MX: Gateron / Outemu / Cherry). Jeśli to co innego (np. Kailh Choc — dwa prostokątne
> kołki), cała geometria gniazda z tej lekcji jest nieaktualna i musimy ją przeliczyć.
> Napisz mi, co zobaczyłeś.

---

## 2. Orientacja druku — ustalamy ją TERAZ, nie po modelowaniu

To wniosek z uchwytu na telefon: orientacja potrafi wymusić zmianę konstrukcji, więc
decydujemy na początku.

Keycap drukujemy **wierzchem do stołu, trzpieniem do góry**. Wtedy:

| | |
|---|---|
| Ścianki | rozchylają się ku górze o ok. **14° od pionu** (przy podstawie 18 i wierzchu 13,5 na wysokości 9) — daleko od limitu 45°, zero podpór |
| Trzpień/gniazdo | boss stoi na stole jak słupek i rośnie do góry — **drukuje się sam, bez mostków** |
| Otwarty spód | ląduje na samej górze wydruku — nie ma czego podpierać |
| Wierzch klawisza | to **pierwsza warstwa** na teksturowanym PEI → wychodzi matowy, lekko szorstki. Pod palcem jest to zaleta |

I tu jest powód, dla którego v1 ma płaski wierzch: **wklęsły dish nie ma jak leżeć na stole.**
Dotykałby blatu tylko obrzeżem, pierwsza warstwa byłaby cienką ramką. Płaski wierzch daje
pełny kontakt 13,5 × 13,5 mm. W lekcji 2, gdy dołożymy dish, będziemy musieli świadomie
wybrać między brimem, obróceniem modelu a podporami — i wtedy będziesz już wiedział, o co gramy.

---

## 3. Ćwiczenie

### Krok 0 — nowy dokument

`File → New`, zapisz od razu jako `projekty/keycap-mx-1u/cad/keycap-1u.FCStd`.
Warsztat **Part Design** → **Create body**.

### Krok 1 — arkusz parametrów

Warsztat **Spreadsheet** → **Create spreadsheet**. W drzewie zmień jego nazwę na `Arkusz`
(F2 na nazwie).

Wypełnij tak — opis w kolumnie A, wartość w B, alias na komórce B:

| Wiersz | A (opis) | B (wartość) | alias |
|---|---|---|---|
| 1 | szerokość podstawy | `18 mm` | `szer_podstawy` |
| 2 | szerokość wierzchu | `13.5 mm` | `szer_gory` |
| 3 | grubość ścianki | `1.2 mm` | `gr_scianki` |
| 4 | głębokość wewnętrzna (Z POMIARU!) | `7.8 mm` | `gleb_wew` |
| 5 | wysokość całkowita | `=gleb_wew + gr_scianki` | `wys_calk` |
| 6 | ramię krzyża MX (nominał) | `4.1 mm` | `krzyz_ramie` |
| 7 | grubość ramienia MX (nominał) | `1.17 mm` | `krzyz_grubosc` |
| 8 | luz gniazda (Z KALIBRACJI!) | `0.1 mm` | `krzyz_luz` |
| 9 | głębokość gniazda | `4 mm` | `gniazdo_gleb` |
| 10 | wysokość bossa | `=gniazdo_gleb + 0.2 mm` | `boss_wys` |
| 11 | średnica bossa | `7 mm` | `boss_srednica` |

Alias ustawiasz tak: klikasz komórkę B1 → pole **Alias** nad arkuszem → wpisujesz `szer_podstawy`
→ Enter. Komórka zrobi się żółta. **Tylko ASCII, bez polskich znaków.**

Zwróć uwagę na wiersze 5 i 10 — to **formuły**, nie liczby. Wysokość całkowita nie jest
niezależnym parametrem: wynika z tego, ile miejsca musi być w środku, plus grubość wierzchu.
Jeśli zmienisz `gleb_wew`, wysokość poprawi się sama. O to chodzi w parametryzacji:
opisujesz **zależności**, nie wyniki.

> Wartości w wierszach 4 i 8 zastąp swoimi, gdy tylko je zdobędziesz.
> Do tego czasu model będzie się liczył, ale **nie drukuj go na produkcję** — to placeholdery.

### Krok 2 — bryła zewnętrzna (Loft)

Potrzebujesz dwóch kwadratów na dwóch różnych wysokościach.

1. **Szkic dolny:** zaznacz płaszczyznę **XY** w drzewie → **Create sketch**.
   Narysuj prostokąt (`G`, `R`) mniej więcej wokół środka.
   Zwiąż go: dwa więzy **symetrii** (`S`) — po jednym względem osi X i osi Y — sprawiają,
   że prostokąt jest wyśrodkowany na origin. Potem jeden wymiar poziomy (`K`, `L`)
   i jeden pionowy (`K`, `I`), oba przez `fx` → `Arkusz.szer_podstawy`.
   **Szkic musi być zielony.** Zamknij.

   > Podpowiedź do symetrii: zaznacz **dwa przeciwległe narożniki prostokąta**, potem
   > (z Ctrl / Cmd) **oś**, dopiero wtedy `S`. Kolejność zaznaczania ma znaczenie — oś ostatnia.

2. **Płaszczyzna dla szkicu górnego:** zaznacz **XY** → **Create a datum plane**,
   Attachment offset → **Z** → `fx` → `Arkusz.wys_calk`.

3. **Szkic górny:** na tej płaszczyźnie, dokładnie tak samo, ale wymiar = `Arkusz.szer_gory`.

4. **Loft:** w Part Design → **Additive loft**. Jako profil bazowy wskaż szkic dolny,
   dodaj szkic górny do listy sekcji. `Create solid` zaznaczone. OK.

   Jeśli bryła wyjdzie poskręcana jak śruba — Loft połączył narożniki „na krzyż".
   Naprawa: upewnij się, że oba prostokąty mają narożniki w tych samych ćwiartkach
   (obie symetrie na miejscu), albo w oknie Loft odwróć kolejność sekcji.

### Krok 3 — wydrążenie (Thickness)

Obróć model tak, żeby widzieć **spód** (płaszczyzna Z=0). Kliknij tę ściankę — musi się podświetlić
jako jedna ścianka, nie krawędź.

Part Design → **Thickness**. Wartość → `fx` → `Arkusz.gr_scianki`.
Mode: **Skin**, Join type: **Intersection**, zaznacz **Make thickness inwards**.

Efekt: skorupa o stałej grubości, otwarta od spodu. Jedno kliknięcie zamiast liczenia,
o ile mniejszy ma być wewnętrzny Loft — i, co ważniejsze, grubość **zostaje stała**,
gdy zmienisz kąt ścianek.

Sprawdź w widoku przekroju (`View → Clipping plane`), czy w środku faktycznie jest pusto
i czy sufit jest na wysokości `gleb_wew`.

### Krok 4 — boss pod gniazdo

1. **Płaszczyzna bossa:** zaznacz **XY** → **Create a datum plane**, offset Z → `fx`:
   ```
   Arkusz.gleb_wew - Arkusz.boss_wys
   ```
   To jest **dolna** płaszczyzna bossa. Wysokość sufitu wewnętrznego wynosi `gleb_wew`,
   więc boss o wysokości `boss_wys` dosunie się do niego dokładnie.

2. Na tej płaszczyźnie: szkic z **okręgiem** (`G`, `C`) wyśrodkowanym na origin
   (więz pokrycia `C` środka z punktem origin), średnica (`K`, `O`) → `Arkusz.boss_srednica`.

3. **Pad** w górę, długość → `Arkusz.boss_wys`.

   > W OpenSCAD stykające się bryły w `union()` to był problem (pamiętasz `Volumes: 3`).
   > FreeCAD używa innego jądra geometrycznego (OCC) i sklejanie „ścianka do ścianki" jest tu
   > poprawne — nie musisz robić naddatku. Jeśli mimo to Pad zgłosi błąd, dodaj `+ 0.01 mm`
   > do długości i jedź dalej.

### Krok 5 — gniazdo krzyżowe

Robimy je **dwoma prostokątnymi Pocketami**, nie jednym szkicem krzyża.
Dwa nachodzące na siebie zarysy w jednym szkicu to najczęstsza przyczyna „Invalid sketch"
u początkujących, a wynik jest identyczny.

1. Szkic na **płaszczyźnie bossa** (tej samej co w kroku 4), prostokąt wyśrodkowany
   (dwie symetrie), wymiary przez `fx`:
   - poziomy: `Arkusz.krzyz_ramie + Arkusz.krzyz_luz`
   - pionowy: `Arkusz.krzyz_grubosc + Arkusz.krzyz_luz`
2. **Pocket**, długość → `Arkusz.gniazdo_gleb`, zaznacz **Reversed** (ma ciąć w górę, w boss).
3. Drugi szkic na tej samej płaszczyźnie, ten sam prostokąt **obrócony o 90°** —
   czyli poziomy = `krzyz_grubosc + krzyz_luz`, pionowy = `krzyz_ramie + krzyz_luz`.
4. Drugi **Pocket**, te same ustawienia.

Gniazdo ma teraz 4 mm głębokości w bossie wysokim na 4,2 mm — zostaje 0,2 mm „sufitu",
żeby trzpień nie przebił się na wylot.

> **Wyzwanie (opcjonalne, na potem):** zrób ten krzyż jako **jeden** szkic — łamana
> (`G`, `M`) o 12 odcinkach, związana przez symetrie i więzy **równości** (`E`).
> Wtedy potrzebujesz tylko dwóch wymiarów na całą figurę. Ładniejsze, ale nie szybsze.

### Krok 6 — sprawdzenie i eksport

1. Uruchom makro [`sprawdz.py`](sprawdz.py) (patrz nagłówek pliku — jak je odpalić).
2. Zaznacz **Body** → `File → Export` → STL → `projekty/keycap-mx-1u/stl/keycap-1u-v1.stl`.
3. Commit + push.

---

## 4. Kryteria sukcesu

Zaliczone, gdy **wszystkie** są spełnione:

- [ ] Każdy szkic w drzewie jest **zielony** (fully constrained).
- [ ] Żadna liczba wymiarowa nie jest wpisana ręcznie — wszystkie pola są **niebieskie** (`fx` → `Arkusz`).
- [ ] Zmiana `szer_podstawy` w arkuszu na `19 mm` przelicza cały model **bez ani jednego błędu**
      w drzewie. Wróć potem na `18 mm`. (To jest prawdziwy test parametryczności — model,
      który nie przeżywa zmiany wymiaru, nie jest parametryczny, tylko narysowany.)
- [ ] `sprawdz.py` zgłasza: bryła poprawna, **1 solid**, bounding box zgodny z arkuszem.
- [ ] STL otwiera się w Bambu Studio bez ostrzeżenia o błędach siatki.
- [ ] **Po druku:** keycap wchodzi na przełącznik z wyczuwalnym oporem, nie spada przy odwróceniu
      klawiatury, klawisz ma pełny skok (nie siada wcześniej na obudowie).

## 5. Pułapki, na które uważaj

| Objaw | Przyczyna |
|---|---|
| Loft wychodzi skręcony | prostokąty nie są tak samo zorientowane — brakuje symetrii w jednym ze szkiców |
| Thickness zgłasza błąd | zaznaczona krawędź zamiast ścianki, albo grubość > połowa najmniejszego wymiaru |
| „Invalid sketch" przy Pocket | dwa nachodzące zarysy w jednym szkicu |
| Pole wymiaru nie przyjmuje `Arkusz.x` | arkusz nazywa się inaczej (sprawdź **Name** w drzewie, nie Label), albo alias ma polski znak |
| Model się rozsypuje po zmianie w arkuszu | szkic był narysowany po **ściance modelu** zamiast po płaszczyźnie odniesienia |
| Keycap nie wchodzi na przełącznik | `krzyz_luz` wciąż jest placeholderem 0,1 — zrób kalibrację |

## 6. Co dalej

1. Wydrukuj drabinkę z [`kalibracja/01-gniazdo-mx/`](../../../kalibracja/01-gniazdo-mx/)
   i wstaw prawdziwy `krzyz_luz` do arkusza.
2. Wydrukuj keycapa i wpisz wnioski do [`projekty/keycap-mx-1u/README.md`](../../../projekty/keycap-mx-1u/README.md).
3. Wpis do [`nauka/dziennik.md`](../../dziennik.md).
4. Lekcja 2: dish, pochylenie rzędu, fazy — i decyzja, jak to wydrukować bez podpór.
