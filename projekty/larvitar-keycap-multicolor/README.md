# Larvitar keycap — podział na kolory (druk bez zmiany filamentu)

Model źródłowy: **Larvitar – Pokémon Mechanical Keyboard Keycap**, autor
*MonsieurPierre* (MakerWorld, „Standard Digital File License”). Projekt Bambu
Studio z malowaniem MMU. Rozcięty na osobne bryły — po jednej na kolor — tak
jak `../psyduck-keycap-multicolor/`, tą samą biblioteką
(`../../biblioteka/podzial_mmu.py`).

## Cel

Ten sam co przy Psyducku: zamiast multicolor z wieżą czyszczącą — osobne
części, sklejane po wydruku. Tu wychodzi **5 części i tylko 3 kolory**.

## Materiał

PLA. Paleta z oryginalnego projektu, przy czym **slot 3 (czarny) jest nieużywany**
— ciemne detale przy oczach to nie czerń, tylko ciemna zieleń:

| AMS | Kolor | Części |
|-----|-------|--------|
| 1 | zielony `#00AE42` | `cialo` |
| 2 | ciemnozielony `#164B35` | `plyta-brzuch` |
| 3 | — | *(nieużywany)* |
| 4 | biały `#FFFFFF` | `baza-keycap`, `oko-L`, `oko-P` |

## Części

| Plik | Obj. | Gabaryt [mm] | Uwagi |
|------|------|--------------|-------|
| `1-zielony-cialo.stl` | 622 mm³ | 11,9 × 14,9 × 18,4 | figurka z cokołem i gniazdami |
| `4-bialy-baza-keycap.stl` | 1045 mm³ | 18,0 × 18,0 × 9,4 | keycap z trzpieniem MX |
| `2-ciemnozielony-plyta-brzuch.stl` | 31,9 mm³ | 5,4 × 4,1 × 2,8 | płyta na brzuchu |
| `4-bialy-oko-L/P.stl` | ~1,7 mm³ | 1,7 × 1,1 × 1,4 | **na granicy sensu — patrz niżej** |

## Czym ten model różni się od Psyducka

**1. Baza i figurka to już dwie osobne bryły.** `m.split()` zwraca 2 zamknięte
solidy — autor nie zrobił z nich unii. Rozdzielenie kosztowało zero cięcia.
U Psyducka trzeba było szukać płaskiego szwu; tu go po prostu nie ma, bo
i nie musi być.

**2. Figurka stykała się z bazą pięciopunktowo.** Wchodziła w jej górę tylko
0,33 mm, a przekrój styku to 3 wysepki po 6,6 / 6,6 / 3,1 mm². Za mało na klejenie
i beznadziejnie na przyczepność do stołu. Dlatego przekrój na płaszczyźnie góry
bazy jest **wyciągnięty w dół o 0,8 mm jako cokół**, a w bazie powstaje pasujące
gniazdo — złącze samo się pozycjonuje i ma sensowną powierzchnię klejenia.
Górna ścianka bazy ma 1,54 mm, więc po wybraniu 0,8 mm zostaje 0,74 mm.

**3. Ciemnozielonych obszarów jest 10, ale tylko jeden nadaje się na część.**

| Obszar | Gabaryt [mm] | Decyzja |
|---|---|---|
| płyta na brzuchu | 4,30 × 2,14 × 5,31 | **osobna część** |
| łuki nad oczami ×2 | 0,76 × 1,10 × 1,31 | malowanie |
| pyszczek | 1,80 × 0,52 × 0,40 | malowanie |
| romby na bokach ×2 | 0,95 × 1,04 × 1,59 | malowanie |
| detale przy oczach ×2 | 0,40 × 0,85 × 1,10 | malowanie |
| kropki ×2 | 0,24 × 0,79 × 0,61 | malowanie |

Dziewięć obszarów poniżej ~1,8 mm zostaje na zielonym ciele. Ciemnozielony
marker albo akryl cienkim pędzelkiem.

## Oczy — uczciwie: prawdopodobnie lepiej pomalować

Wygenerowane, ale widoczna część ma **1,07 × 1,71 mm**, a cała bryłka z czopem
1,7 × 1,1 × 1,4 mm i 1,7 mm³. To ziarnko. Do tego **tuż obok nich są
ciemnozielone łuki, których i tak nie da się wydzielić** — czyli okolica oka
i tak wymaga pędzelka. Malowanie białego owalu jest szybsze i pewniejsze niż
wklejanie pęsetą czegoś wielkości ziarnka maku.

Pliki są, więc możesz spróbować. Jak wolisz od razu bez nich — ustaw
`OCZY_OSOBNO = False` w skrypcie i przegeneruj; oczy zostaną częścią ciała.

## Ustawienia druku

Profil autora: **0,12 mm warstwa, 2 perymetry, 15% wypełnienia**.
Do **sprawdzenia na A1**:

* **`baza-keycap`** — płaską ścianką cięcia na stół, komora na switch do góry.
  Zwisy >45° są wtedy **wyłącznie na z = 0–3 mm** (pierwsza warstwa + dolny
  rant). Bez podpór.
* **`cialo`** — ⚠ **brim obowiązkowy.** Figurka ma 18,4 mm wysokości, a styka
  się ze stołem tylko **13,8 mm²** (cokół). W oryginale stała na całej,
  18 × 18 mm bazie keycapa — po rozdzieleniu tej stabilności już nie ma.
  Brim 5 mm, zewnętrzny.
* **`cialo` — zwisy.** 78,5 mm², z czego **58,3 mm² w paśmie z = 0–3 mm**:
  tuż nad cokołem tułów rozszerza się z 13,8 do 57 mm². To ten sam nawis co
  w oryginale (tam też brzuch wisiał nad płaską górą keycapa), więc powinien
  przejść bez podpór z lekkim obwiśnięciem od spodu. Jeśli wyjdzie brzydko —
  podpory drzewkowe tylko do wysokości 4 mm.
* **`plyta-brzuch`, `oczy`** — płaskim dnem na stół, brim, bez podpór.
* STL-e są **już obrócone do druku** i posadzone na `z = 0`.

## Druk bez zmiany filamentu

`slicer/larvitar-plyta-podzielona.3mf` — jedna płyta, 5 obiektów, każdy
z przypisanym slotem AMS.

Sprawdzony sposób (ten sam, który zadziałał przy Psyducku): **sekwencja druku
„Wg obiektu”**. Nazwy plików zaczynają się od numeru slotu, więc kolejność sama
grupuje kolory i wychodzą **2 zmiany filamentu na całe zadanie**
(`1 zielony → 2 ciemnozielony → 4 biały ×3`).

Alternatywa bez żadnej zmiany: 3 osobne zadania z tej samej płyty, ustawiając
obiekty pozostałych kolorów jako niedrukowalne.

## Montaż

`baza-keycap` → wciśnij i wklej `cialo` (cokół wchodzi w gniazdo, samo się
ustawia) → `plyta-brzuch` → ewentualnie oczy. Klej cyjanoakrylowy **żelowy**.

⚠ Jeśli drukujesz z brimem: **oczyść nożykiem krawędź dna cokołu i czopów**
przed klejeniem. Nadlew 0,2 mm sprawi, że część nie dosiądzie.

Detale ciemnozielone (9 sztuk) i ewentualnie oczy — malowanie po sklejeniu.

## Status

**Zaprojektowane i zweryfikowane geometrycznie — nie wydrukowane.**
Kontrola w bibliotece przechodzi: 5 brył szczelnych, każda w jednym kawałku,
zero kolizji między częściami.

## Wnioski

1. **Najpierw `m.split()`, potem cokolwiek innego.** Przy Psyducku szukałem
   płaskiego szwu; tu połowa roboty była już zrobiona — dwie osobne bryły
   w jednej siatce. Warto zawsze sprawdzić `body_count` przed cięciem.
2. **Rozdzielenie części potrafi popsuć drukowalność.** Figurka stojąca na
   bazie była stabilna; ta sama figurka osobno stoi na 13,8 mm² przy 18,4 mm
   wysokości. Podział to nie tylko geometria — trzeba policzyć, na czym każda
   część stanie na stole.
3. **Stosunek „ile kolorów da się wydzielić” bywa kiepski.** Tu 10 obszarów
   ciemnej zieleni, z czego użyteczny 1. Przy modelu z drobnym wzorem podział
   na części ma sens tylko dla dużych plam koloru — reszta to i tak pędzelek.
4. **Biblioteka się opłaciła.** Po wyniesieniu narzędzi do
   `biblioteka/podzial_mmu.py` skrypt tego projektu ma ~110 linii i opisuje
   tylko *co jest czym*. Refaktor zweryfikowany regresją: Psyduck po zmianie
   generuje STL-e bit w bit identyczne.

## Do sprawdzenia po pierwszym druku

* [ ] Czy `cialo` na 13,8 mm² cokołu trzyma się stołu przy brimie 5 mm.
* [ ] Czy nawis tułowia nad cokołem (z = 0–3 mm) wyszedł bez podpór.
* [ ] Czy luz 0,10 mm pasuje do cokołu (duże złącze — może wymagać innej
      wartości niż małe czopy).
* [ ] Czy oczy w ogóle da się sensownie wkleić, czy jednak pędzelek.

## Odtworzenie plików

```bash
python3 cad/podzial_kolorow.py cad/larvitar.3mf
```

## Licencja

Model źródłowy ma **Standard Digital File License** — bez prawa redystrybucji.
Repo jest publiczne, więc geometria (`.stl`, `.3mf`) jest w `.gitignore`;
wersjonowany jest tylko skrypt. Żeby odtworzyć części, potrzebna jest własna
kopia modelu z MakerWorld jako `cad/larvitar.3mf`.
