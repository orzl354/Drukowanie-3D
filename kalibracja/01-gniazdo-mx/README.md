# 01 — gniazdo krzyżowe MX: drabinka tolerancji

## Po co to jest

Keycap trzyma się na przełączniku **jednym** pasowaniem: krzyżem 4,10 × 1,17 mm.
Otwory drukowane pionowo na FDM wychodzą mniejsze od modelu — o ile, tego nie da się
wyczytać z tabelki, bo zależy to od konkretnej drukarki, filamentu i prędkości.

Ta płytka zamienia to pytanie w **jedną liczbę**, która idzie potem do arkusza FreeCAD
jako `krzyz_luz` (lekcja [`01-keycap-mx`](../../nauka/cwiczenia/01-keycap-mx/)).

To nie jest ćwiczenie modelarskie — to przyrząd pomiarowy, dlatego jest generowany kodem,
a nie klikany we FreeCAD. Pięć wariantów jednej geometrii to w kodzie jedna pętla,
a we FreeCAD pół godziny klikania.

**Bez suwmiarki ta płytka działa tak samo dobrze** — odpowiedź daje pasowanie, nie pomiar.
Dlatego to jest pierwsza rzecz do wydrukowania w całym projekcie.

## Co zawiera

**`gniazdo-mx.stl` — gotowy plik do druku, leży w tym folderze.** Nie potrzebujesz
do niego OpenSCAD-a ani FreeCAD-a, tylko slicera.

Płytka 72 × 20 × 6 mm z pięcioma gniazdami. **Liczba małych otworków obok gniazda = numer
stacji**, a numer mówi, o ile powiększony jest krzyż względem nominału MX:

| Otworków | Dodatek | Wymiary gniazda |
|---|---|---|
| ● | +0,00 mm | 4,10 × 1,17 mm (czysty nominał) |
| ●● | +0,05 mm | 4,15 × 1,22 mm |
| ●●● | +0,10 mm | 4,20 × 1,27 mm |
| ●●●● | +0,15 mm | 4,25 × 1,32 mm |
| ●●●●● | +0,20 mm | 4,30 × 1,37 mm |

`gniazdo-mx.py` to źródło, z którego ten STL powstał — czysty Python, bez bibliotek.
Jeśli zechcesz zmienić zakres badanych dodatków, popraw `DODATKI` na górze pliku i uruchom:

```bash
python3 gniazdo-mx.py
```

Skrypt przed zapisem sprawdza sam siebie: czy siatka jest szczelna, czy jest spójnie
zorientowana i czy jej objętość zgadza się z modelem. Jeśli coś nie gra — nie zapisze pliku.

> Reszta przyrządów w tym repo jest w OpenSCAD i tak zostaje. Ten jeden jest w Pythonie,
> bo dzięki temu STL w repo jest **zweryfikowany**, a Ty startujesz bez instalowania
> czegokolwiek poza slicerem.

## Jak wydrukować

Otwórz `gniazdo-mx.stl` w Bambu Studio. Ustawienia — **identyczne z tymi, którymi będziesz
drukował keycapa**, inaczej wynik nie przenosi się na część docelową:

| | |
|---|---|
| Materiał | ten sam, co na keycapa (proponuję PLA Matte na start) |
| Warstwa | **0,12 mm** — i zapamiętaj tę wartość, keycap musi iść tak samo |
| Ścianki | 3 |
| Wypełnienie | 15% |
| Orientacja | płasko, gniazdami do góry (tak jak się wczytuje) |
| Podpory | brak |
| Czas / materiał | ok. 30–40 min, ~5 g |

## Jak zmierzyć wynik

> **Wyjmij jeden przełącznik z klawiatury ściągaczem** (GK630K jest hot-swap) i testuj na nim,
> trzymając go w palcach. Nie wciskaj płytki na przełącznik osadzony w PCB — za ciasne gniazdo
> potrafi wyrwać przełącznik razem z gniazdem hot-swap albo urwać ścieżkę. To jest jedyny
> krok w całym projekcie, w którym da się uszkodzić klawiaturę.

1. Wciskaj trzpień kolejno w gniazda **od największego (●●●●●) w dół**.
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

| Stacja | Wchodzi? | Opór | Trzyma po odwróceniu? | Uwagi |
|---|---|---|---|---|
| ● +0,00 | | | | |
| ●● +0,05 | | | | |
| ●●● +0,10 | | | | |
| ●●●● +0,15 | | | | |
| ●●●●● +0,20 | | | | |

**Wybrany `krzyz_luz` = ______ mm**

**Rzeczywisty skurcz otworu:** wybrany dodatek *jest* Twoim skurczem. Jeśli pasuje stacja
●●● (+0,10), to znaczy, że Twoja A1 przy tych ustawieniach zawęża pionowe otwory o ok.
0,10 mm na wymiar. Ta liczba przydaje się we **wszystkich** kolejnych projektach —
otwory pod śruby, kołki, zatrzaski — nie tylko w keycapie.

**Wnioski:**

```
```
