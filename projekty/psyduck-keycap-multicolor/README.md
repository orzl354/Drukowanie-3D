# Psyduck keycap — podział na kolory (druk bez zmiany filamentu)

Model źródłowy: **Psyduck Pokemon Keyboard Keycap MX**, autor *MonsieurPierre*
(MakerWorld, „Standard Digital File License”). Plik przyszedł jako projekt Bambu
Studio z **malowaniem MMU na 4 kolory**. Tu został rozcięty na osobne bryły — po
jednej na kolor — żeby każdą grupę wydrukować jednym filamentem, **bez zmian
koloru w trakcie druku i bez wieży czyszczącej**.

## Cel

Zamiast drukować multicolor (4 filamenty, zmiana koloru co warstwę, ~15–20 g
odpadu na wieżę przy 2,6 cm³ modelu) — 8 osobnych części, 4 zadania druku,
sklejane po wydruku. Zero odpadu na przepłukiwanie.

## Materiał

PLA / PLA Matte (model wystawowy, keycap nie jest obciążony mechanicznie ani
nie jedzie do samochodu — PETG/ASA niepotrzebne). Kolory jak w oryginalnym
projekcie:

| AMS | Kolor | Części |
|-----|-------|--------|
| 1 | żółty `#F4EE2A` | `cialo` |
| 2 | czarny `#000000` | `baza-keycap`, `wlosy` |
| 3 | biały `#FFFFFF` | `oko-L`, `oko-P` |
| 4 | kremowy `#F7E6DE` | `dziob`, `stopa-L`, `stopa-P` |

## Części

| Plik | Obj. | Gabaryt [mm] | Uwagi |
|------|------|--------------|-------|
| `1-zolty-cialo.stl` | 1366 mm³ | 15,3 × 15,8 × 14,4 | korpus kaczki z gniazdami |
| `2-czarny-baza-keycap.stl` | 1050 mm³ | 18,0 × 18,0 × 9,4 | baza keycapa z trzpieniem MX |
| `2-czarny-wlosy.stl` | 7,2 mm³ | 4,9 × 2,2 × 3,6 | kępka 3 włosków na wspólnej stopce |
| `3-bialy-oko-L/P.stl` | 9,2 mm³ | 3,0 × 2,8 × 2,8 | czop wciskany w oczodół |
| `4-kremowy-dziob.stl` | 161 mm³ | 7,8 × 10,1 × 5,5 | czop wchodzi skosem 30° w dół |
| `4-kremowy-stopa-L/P.stl` | 4,3 mm³ | 4,0 × 3,1 × 1,3 | wchodzi 0,6 mm w czarną bazę |

Suma = objętość oryginału (2619,5 mm³) minus luzy. Skrypt sam sprawdza, że każda
bryła jest szczelna, jednolita i że **żadne dwie części się nie przenikają** —
bez tego zestawu nie dałoby się złożyć.

## Jak to jest pocięte

* **Baza keycapa / kaczka** — model ma w tym miejscu gotowy, **płaski szew**
  na `z = -3,619 mm` (zero trójkątów przecinających tę płaszczyznę). Rozcięcie
  tam jest darmowe i idealnie gładkie.
* **Dziób, oczy, włosy** — „czop + gniazdo”. Powierzchnia obszaru zostaje
  nietknięta, ścianki są wyciągnięte w głąb bryły, dno płaskie. Gniazdo to ta
  sama bryła bez zbieżności, więc **krawędź na powierzchni trafia w siebie
  dokładnie** — szew jest niewidoczny, a luz 0,10 mm siedzi dopiero w głębi
  czopa (zbieżność), gdzie i tak potrzeba miejsca na klej.
* **Stopy** — obrys stopy w rzucie z góry sam się przecina, więc metoda czopa
  tu nie działa; użyte są operacje boolowskie na pionowej pryzmie obrysu.

### Dlaczego dziób wchodzi skosem

Przy czopie poziomym `(0,1,0)` gniazdo dzioba **zachodziło na gniazda oczu**
(0,5 mm³ przenikania) — dziobu i oczu nie dałoby się włożyć jednocześnie.
Kierunek `(0, 0,87, −0,5)` (30° w dół) prowadzi czop pod oczami i kolizja znika
przy dowolnej głębokości. To jest ten przypadek, gdzie o konstrukcji decyduje
montaż, a nie wygląd.

## Czego NIE dało się rozdzielić

Trzy detale są poniżej granicy sensu na dyszy 0,4 mm — zostały wtopione
w większą część, do pomalowania po sklejeniu:

* **Źrenice** (0,5 × 0,25 mm, płaskie — leżą dokładnie na kuli oka, odchyłka
  −0,02 mm) → zostają na białym oku. **Cienkopis / marker olejny, czarny.**
* **Nozdrza** (0,5 × 0,9 mm, żółte latki wewnątrz dzioba) → wtopione w dziób.
  Są zagłębione, więc czytają się kształtem; kolor pomijalny.
* Gdyby uprzeć się na osobne źrenice — 0,5 mm kulka do wklejenia w 0,5 mm
  otwór. Nie warto.

## Ustawienia druku

Punkt wyjścia = profil autora modelu: **0,12 mm warstwa, 2 perymetry, 15%
wypełnienia**. Do **sprawdzenia na moim A1**, nie brać jako pewnik:

* **`baza-keycap`** — drukować **odwrotnie niż w modelu**: płaską ścianką cięcia
  na stół, komora na switch otwarta do góry. Wtedy zwisy >45° są **tylko na
  `z = 0…0,6 mm`** (czyli pierwsza warstwa) — zero podpór. W drugą stronę
  wychodzi 219 mm² zwisów rozrzuconych po całej wysokości.
* **`cialo`** — płaską ścianką na stół (tak jak w oryginale, autor deklaruje
  „no supports”). Gniazdo dzioba jest skośną kieszenią 2,5 mm — jej strop to
  zwis ~30° od poziomu na głębokości 2,5 mm. Trochę obwiśnie, ale to wnętrze
  gniazda, zasłonięte przez dziób. **Bez podpór.**
* **`wlosy`** — stopką na stół, włoski do góry (jak w oryginale). Włoski mają
  ~0,5 mm — 1 perymetr. **Wolniej + chłodzenie na max**, inaczej się rozjadą.
* **`dziob`, `oczy`, `stopy`** — płaskim dnem na stół, bez podpór.
* Wszystko w **STL-ach jest już obrócone do druku** i posadzone na `z = 0`.

## Druk bez zmiany filamentu

Wszystkie 8 części jest na **jednej płycie** (`slicer/psyduck-plyta-podzielona.3mf`),
pogrupowane kolorami w kolumny, każdy obiekt ma już przypisany slot AMS.

⚠️ **Jedna płyta ≠ jedno zadanie.** Na jednej dyszy 4 kolory naraz to i tak
zmiany filamentu co warstwę. Żeby ich nie było, drukuj **4 razy z tej samej
płyty**:

1. Otwórz płytę w Bambu Studio.
2. Zaznacz obiekty **jednego** koloru → reszta: PPM → **„Ustaw jako
   niedrukowalne”** (albo po prostu je ukryj).
3. Potnij i wydrukuj. Powtórz dla pozostałych 3 kolorów.

Kolejność bez znaczenia; najwięcej czasu zajmie `cialo` i `baza-keycap`,
reszta to minuty.

Alternatywa: zaimportować pojedyncze STL-e z `stl/` — nazwy mają prefiks
numeru slotu AMS (`1-zolty-…`, `2-czarny-…`, …).

## Montaż

Kolejność: `baza-keycap` → wklej `stopa-L/P` (siedzą w kieszeniach w bazie)
→ nasadź `cialo` na bazę (płaski szew, duża powierzchnia klejenia)
→ `dziob` (wsuwać **skosem w dół i do tyłu**, zgodnie z osią czopa)
→ `oczy` → `wlosy`.

Klej: **cyjanoakryl żelowy** (płynny ucieknie przez 0,1 mm luz) albo klej do
modeli PLA. Źrenice markerem **po** sklejeniu oczu.

## Status

**Zaprojektowane i zweryfikowane geometrycznie — nie wydrukowane.**
Automatyczna kontrola w skrypcie przechodzi: 8 brył szczelnych, każda w jednym
kawałku, zero kolizji między częściami, złożenie odtwarza oryginał.

## Wnioski

1. **Malowanie MMU to gotowa mapa cięcia.** `paint_color` w 3MF to zserializowane
   drzewo podziału trójkąta (kodowanie z PrusaSlicer). Dekodowanie dało
   4402 pomalowane trójkąty bez ani jednego błędu — nie trzeba zgadywać, gdzie
   są granice kolorów.
2. **Modele bywają już „prepodzielone”.** Płaski szew na `z = -3,619` z zerem
   trójkątów przecinających płaszczyznę to ślad po tym, że autor złożył model
   z kaczki i keycapa. Warto takich szwów szukać, zanim zacznie się ciąć na siłę.
3. **Kierunek czopa to decyzja montażowa, nie estetyczna.** Dziób poziomo
   wyglądał sensownie i był nie do złożenia. Test przenikania par brył wyłapał
   to od razu — i powinien być w każdym takim skrypcie.
4. **Odsunięcie wielokąta do środka ma dwie pułapki**: znak normalnej (liczony
   z pola ze znakiem) i to, że na narożniku trzeba iść po dwusiecznej
   `d·(n₁+n₂)/(1+n₁·n₂)`, a nie po znormalizowanej sumie — inaczej na rogu
   wychodzi 0,07 zamiast 0,10 mm. Pomyliłem znak i czopy wyszły **większe** od
   gniazd; złapał to dopiero test „czop minus gniazdo = 0”.
5. **Nie każdy kolor da się rozdzielić.** 0,5 mm źrenica to nie jest część —
   to malowanie. Granica użyteczności ≈ 1,5–2 mm najmniejszego wymiaru.

## Do sprawdzenia po pierwszym druku

* [ ] Czy luz **0,10 mm** to dobra wartość dla wciskanych czopów (`kalibracja/`).
      Za ciasno → przeszlifować czop; za luźno → podnieść `LUZ` w skrypcie.
* [ ] Czy strop gniazda dzioba nie obwisł tak, że dziób nie dochodzi do końca.
* [ ] Czy włoski 0,5 mm wyszły na wolniejszym profilu.
* [ ] Czy 0,6 mm kieszeni w bazie nie prześwituje (ścianka zostaje ~0,94 mm).

## Odtworzenie plików

```bash
python3 cad/podzial_kolorow.py cad/psyduck_keycap.3mf
```

Generuje `stl/*.stl` + `slicer/psyduck-plyta-podzielona.3mf`. Parametry (luz,
głębokości czopów, odstępy na płycie) są nazwanymi stałymi na górze skryptu.

## Licencja

Model źródłowy ma **Standard Digital File License** — nie wolno go
redystrybuować ani udostępniać prac pochodnych. To repo jest publiczne, więc
**geometria (`.stl`, `.3mf`) jest w `.gitignore`** — wersjonowany jest tylko
mój skrypt. Żeby odtworzyć części, trzeba mieć własną kopię modelu z MakerWorld
i wrzucić ją jako `cad/psyduck_keycap.3mf`.
