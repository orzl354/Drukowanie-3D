# 01 — gniazdo krzyżowe MX: drabinka tolerancji

## Po co to jest

Keycap trzyma się na przełączniku **jednym** pasowaniem: krzyżem 4,10 × 1,17 mm.
Otwory drukowane pionowo na FDM wychodzą mniejsze od modelu — o ile, tego nie da się
wyczytać z tabelki, bo zależy to od konkretnej drukarki, filamentu i prędkości.

Ta płytka zamienia to pytanie w **jedną liczbę**, która idzie potem do arkusza FreeCAD
jako `krzyz_luz` (lekcja [`01-keycap-mx`](../../nauka/cwiczenia/01-keycap-mx/)).

To nie jest ćwiczenie modelarskie — to przyrząd pomiarowy, dlatego jest w OpenSCAD,
a nie we FreeCAD. Pięć wariantów jednej geometrii to w OpenSCAD jedna pętla,
a we FreeCAD pół godziny klikania.

## Co zawiera

`gniazdo-mx.scad` — płytka z pięcioma gniazdami. Cyfra przy gnieździe = **dodatek w setnych
milimetra**, dodany do obu wymiarów krzyża:

| Cyfra na płytce | Wymiary gniazda |
|---|---|
| `0` | 4,10 × 1,17 mm (czysty nominał) |
| `5` | 4,15 × 1,22 mm |
| `10` | 4,20 × 1,27 mm |
| `15` | 4,25 × 1,32 mm |
| `20` | 4,30 × 1,37 mm |

## Jak wydrukować

```bash
openscad -o gniazdo-mx.stl gniazdo-mx.scad
# macOS, jeśli nie ma w PATH:
# /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD -o gniazdo-mx.stl gniazdo-mx.scad
```

> Ten plik **nie był u mnie wyrenderowany** (nie mam OpenSCAD w środowisku). Przed eksportem
> zerknij na podgląd i na konsolę po `F6` — ma być `Volumes: 1`.

Ustawienia — **identyczne z tymi, którymi będziesz drukował keycapa**, inaczej wynik nie przenosi się na część docelową:

| | |
|---|---|
| Materiał | ten sam, co na keycapa (proponuję PLA Matte na start) |
| Warstwa | 0.12–0.16 mm |
| Ścianki | 3 |
| Wypełnienie | 15% |
| Orientacja | płasko, gniazdami do góry |
| Podpory | brak |
| Czas | ~15–20 min |

## Jak zmierzyć wynik

> **Wyjmij jeden przełącznik z klawiatury ściągaczem** (GK630K jest hot-swap) i testuj na nim,
> trzymając go w palcach. Nie wciskaj płytki na przełącznik osadzony w PCB — za ciasne gniazdo
> potrafi wyrwać przełącznik razem z gniazdem hot-swap albo urwać ścieżkę. To jest jedyny
> krok w całym projekcie, w którym da się uszkodzić klawiaturę.

1. Wciskaj trzpień kolejno w gniazda **od największego (`20`) w dół**.
2. Dla każdego zanotuj: wchodzi / z jakim oporem / czy trzyma po odwróceniu / czy coś trzeszczy.
3. Szukasz **najciaśniejszego gniazda, które wchodzi bez użycia siły i trzyma po odwróceniu.**
4. Zrób kontrolę: wyjmij i włóż 5 razy. Jeśli po 5 cyklach zaczyna luzować — weź o jeden stopień ciaśniej.

Uwaga na kierunek błędu: keycap ma być **zdejmowalny**. Pasowanie wciskane z `CLAUDE.md`
(0,10–0,15 mm) jest tu punktem wyjścia, ale keycap zdejmuje się dziesiątki razy, a ścianka
gniazda ma ~1,5 mm — celuj raczej w górną połowę tego zakresu niż w dolną.

---

## Wynik (uzupełnić po druku)

**Data:** ____________
**Drukarka:** Bambu Lab A1 · **Dysza:** 0.4 · **Warstwa:** ______ mm
**Filament:** ____________________

| Gniazdo | Wchodzi? | Opór | Trzyma po odwróceniu? | Uwagi |
|---|---|---|---|---|
| `0` (4.10 × 1.17) | | | | |
| `5` (4.15 × 1.22) | | | | |
| `10` (4.20 × 1.27) | | | | |
| `15` (4.25 × 1.32) | | | | |
| `20` (4.30 × 1.37) | | | | |

**Wybrany `krzyz_luz` = ______ mm**

**Rzeczywisty skurcz otworu:** zmierz suwmiarką któreś z gniazd i porównaj z modelem —
różnica to Twoja poprawka dla wszystkich pionowych otworów, nie tylko tego jednego:

```
model ______ mm  −  wydruk ______ mm  =  skurcz ______ mm
```

**Wnioski:**

```
```
