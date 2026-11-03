# Blender od zera: karoseria z blueprintów i bodykit do druku

Kurs dla Blendera 5.2, od kompletnego zera. Ćwiczenia z kryteriami sukcesu są
w [`../cwiczenia/blender-bodykit.md`](../cwiczenia/blender-bodykit.md).

## Mapa kursu

| Lekcja | Temat | Po co |
|---|---|---|
| 1 | Interfejs, nawigacja, podstawowe operacje | bez tego każdy dalszy krok to walka z programem |
| 2 | Blueprinty: tło z rysunków technicznych | daje proporcje, wtedy nie rzeźbisz „na oko” |
| 3 | Karoseria: modelowanie od płaszczyzny („rozciąganie”) | bodykit musi do czegoś przylegać |
| 4 | Bodykit: splitter, progi, spoiler, poszerzenia | właściwy cel |
| 5 | Przygotowanie do druku na A1 | skala, grubość ścianek, eksport STL |

**Dlaczego w tej kolejności:** to, co widziałeś na filmikach, to trzy osobne
umiejętności sklejone w jeden proces: (1) ustawienie rysunków w tle,
(2) obrysowanie ich siatką i wyciąganie jej w 3D, (3) budowanie części
na powierzchni karoserii. Bodykit robi się na końcu, bo jego wewnętrzna
powierzchnia jest **kopią powierzchni nadwozia**, więc nadwozie musi już istnieć.

---

## Lekcja 1 — interfejs i nawigacja

### Teoria (5 minut)

Okno Blendera składa się z **edytorów**, czyli prostokątnych obszarów. Każdy
ma własne menu i własne skróty. Najważniejsza zasada:

> **Skrót klawiszowy działa w tym edytorze, nad którym jest kursor myszy.**
> Jeśli naciśniesz `G`, a kursor stoi nad listą obiektów, nic się nie
> przesunie. To najczęstszy powód „Blender nie reaguje”.

Domyślny układ (zakładka **Layout** na górnym pasku):

```
┌──────────────────────────── górny pasek: File Edit Render Window Help | Layout Modeling ... ┐
│ ┌──────┐                                                      ┌──────────────────┐ │
│ │Tool- │              3D VIEWPORT                             │ OUTLINER         │ │
│ │bar   │       (tu modelujesz: duży środek)                   │ (lista obiektów) │ │
│ │ (T)  │                                       [gizmo osi XYZ]├──────────────────┤ │
│ │      │                                                      │ PROPERTIES       │ │
│ └──────┘                                        [panel N →]   │ (pionowy pasek   │ │
│                                                               │  ikon = zakładki)│ │
├──────────────────────────── TIMELINE (animacja, na razie ignoruj) ─┴──────────────┘ │
```

- **3D Viewport** — główny widok. Na jego górnym pasku (header), od lewej:
  lista trybu (`Object Mode` / `Edit Mode`), menu `View`, `Select`, `Add`,
  `Object`. Po prawej stronie headera: przycisk **X-ray** (dwa nachodzące na
  siebie kwadraty) i cztery kulki trybów cieniowania (Wireframe / **Solid** /
  Material Preview / Rendered). Pracujesz w **Solid**.
- **Gizmo nawigacji** (prawy górny róg viewportu): kolorowa kulka osi
  (czerwony X, zielony Y, niebieski Z). Kliknięcie w kółko osi ustawia widok
  z tej strony. Pod nią: rączka (przesuwanie widoku), lupa (zoom),
  kratka (przełącza widok perspektywiczny ↔ ortogonalny).
- **Toolbar** (lewa krawędź viewportu, `T` chowa/pokazuje) — narzędzia.
  Na razie wystarczą skróty, toolbar zostaw.
- **Sidebar / panel N** (prawa krawędź viewportu, `N` chowa/pokazuje) —
  zakładka **Item** pokazuje `Location`, `Rotation`, `Scale` i **`Dimensions`**
  zaznaczonego obiektu. Tu wpisujesz dokładne liczby.
- **Outliner** — drzewo obiektów i kolekcji (kolekcja to folder na obiekty).
  Ikona oka chowa obiekt.
- **Properties** — pionowy pasek ikon po lewej stronie tego edytora to
  zakładki. Ważne dla nas:
  - stożek z kulką → **Scene** (jednostki),
  - pomarańczowy kwadrat → **Object** (sposób wyświetlania obiektu),
  - niebieski klucz → **Modifiers** (Mirror, Subdivision, Solidify),
  - zielony trójkąt (dla siatki) albo ikona obrazka/osi (dla obrazka) →
    **Object Data**.
- **Panel „Adjust Last Operation”** — po prawie każdej operacji w lewym dolnym
  rogu viewportu pojawia się zwinięty panel z jej parametrami (np. po dodaniu
  walca: liczba boków). Kliknij, żeby rozwinąć. Znika po kolejnej operacji;
  `F9` otwiera go ponownie.

### Ustawienia na start (raz, zapisują się na stałe)

1. **Język → angielski.** `Edit > Preferences > Interface > Translation`
   i ustaw `Language: English`, jeśli Blender startuje po polsku.
   *Dlaczego:* 99% tutoriali i forów używa angielskich nazw, a w tych
   notatkach też podaję nazwy angielskie.
2. **Brak klawiatury numerycznej (laptop)?** `Edit > Preferences > Input`
   i zaznacz **Emulate Numpad**. Wtedy cyfry z górnego rzędu przełączają widoki.
   Koszt: w Edit Mode cyfry `1/2/3` przestają zmieniać tryb zaznaczania,
   więc używasz ikon w headerze (patrz lekcja 3).
3. **Brak myszy z kółkiem?** Tamże **Emulate 3 Button Mouse** (`Alt` + lewy
   przycisk zastępuje środkowy). Ale szczerze: do modelowania kup mysz z kółkiem.
   Emulacja koliduje ze skrótami zaznaczania pętli krawędzi.
4. Ustawienia zapisują się automatycznie: w oknie Preferences w lewym dolnym
   rogu jest ikona trzech kresek, sprawdź, czy `Auto-Save Preferences` jest
   zaznaczone.

### Nawigacja w widoku

| Akcja | Mysz / klawisz |
|---|---|
| Obrót widoku | przytrzymaj **środkowy przycisk** (kółko) i ruszaj |
| Przesuwanie widoku | `Shift` + środkowy przycisk |
| Zoom | kółko myszy |
| Widok z przodu / tyłu | `Numpad 1` / `Ctrl + Numpad 1` |
| Widok z prawej / lewej | `Numpad 3` / `Ctrl + Numpad 3` |
| Widok z góry / dołu | `Numpad 7` / `Ctrl + Numpad 7` |
| Perspektywa ↔ ortogonalny | `Numpad 5` |
| Wycentruj na zaznaczonym | `Numpad .` (kropka) |
| Pokaż wszystko | `Home` |
| Menu kołowe widoków | `` ` `` (klawisz pod `Esc`, z tyldą) |

**Widok ortogonalny** nie ma perspektywy: równoległe linie zostają
równoległe, a odległe rzeczy nie maleją. Rysunki techniczne (blueprinty)
są właśnie w rzucie ortogonalnym, dlatego modelując według nich zawsze
pracujesz w widokach `1/3/7`. Blender sam włącza ortogonalny, gdy wybierzesz
taki widok.

**Osie w Blenderze (zapamiętaj, przyda się w lekcji 2):**
- `Z` w górę, `X` w prawo (patrząc z przodu), `Y` w głąb.
- Samochód ustawiamy tak: **długość wzdłuż Y, szerokość wzdłuż X,
  przód auta skierowany w −Y**. Wtedy `Numpad 1` (Front) pokazuje przód auta,
  a `Numpad 3` (Right) jego prawy bok.

### Zaznaczanie i podstawowe operacje (Object Mode)

| Akcja | Skrót |
|---|---|
| Zaznacz | lewy klik |
| Dodaj do zaznaczenia | `Shift` + lewy klik |
| Zaznacz wszystko / odznacz | `A` / `Alt + A` |
| Zaznaczenie prostokątem | przeciągnij lewym przyciskiem po pustym miejscu |
| Dodaj obiekt | `Shift + A` |
| Usuń | `X` → `Delete` (albo klawisz `Delete`) |
| Duplikuj | `Shift + D` (potem ruch myszą; prawy klik zostawia kopię w miejscu) |
| Zmień nazwę | `F2` |
| Cofnij / ponów | `Ctrl + Z` / `Ctrl + Shift + Z` |
| Zapisz | `Ctrl + S` |

**Przesuwanie, obrót i skala to „GRS”:**

1. Naciśnij `G` (grab = przesuń), `R` (rotate) albo `S` (scale).
2. *(opcjonalnie)* naciśnij `X`, `Y` lub `Z`, żeby zablokować ruch do jednej
   osi. Pojawi się kolorowa linia osi.
3. *(opcjonalnie)* wpisz liczbę z klawiatury, np. `R` `Y` `90` obraca
   o dokładnie 90° wokół Y.
4. Lewy klik albo `Enter` zatwierdza, a prawy klik albo `Esc` anuluje.

Przykłady: `G Z 0.5` podnosi o 0,5 m. `S 2` powiększa dwa razy.
`G Shift+Z` przesuwa wszędzie **poza** osią Z, czyli po podłodze.

**Liczby z jednostką:** w każdym polu i przy GRS możesz wpisać `30mm`
albo `4.255m`, a Blender sam przeliczy. Domyślnie 1 jednostka Blendera = 1 m.

**3D Cursor** to biało-czerwone kółko w środku sceny. **Nowe obiekty pojawiają
się w miejscu kursora.** `Shift` + prawy klik przestawia kursor, a `Shift + C`
wraca nim do środka świata (i pokazuje całą scenę). Jeśli nowy obiekt
„pojawia się gdzieś w kosmosie”, to przez kursor.

### Object Mode a Edit Mode

`Tab` przełącza między nimi.

- **Object Mode** operuje na **całym obiekcie**: przesuwasz go razem z jego
  własnymi osiami i punktem środka (origin, mała pomarańczowa kropka).
- **Edit Mode** operuje na **geometrii wewnątrz obiektu**: wierzchołkach,
  krawędziach i ścianach. Origin i osie obiektu zostają tam, gdzie były.

Ta różnica jest kluczowa w lekcji 3: modyfikator Mirror odbija geometrię
względem **osi obiektu**. Jeśli obrócisz obiekt w Object Mode, obrócisz też oś
lustra.

➡️ **Ćwiczenie 1** w pliku z ćwiczeniami.

---

## Lekcja 2 — blueprinty w tle

### Teoria

Blueprint to rysunek auta w rzutach: bok, przód, tył, góra. Ustawiamy każdy
rzut jako obrazek w odpowiednim widoku Blendera, w **prawdziwej skali**
(1 m w Blenderze = 1 m auta). Potem wierzchołki siatki ustawiasz tak, żeby
pokrywały się z liniami rysunku we wszystkich widokach naraz.

**Dlaczego prawdziwa skala, skoro i tak drukujesz model?**
- Wymiary producenta (długość, rozstaw osi) wpisujesz wprost, bez przeliczania.
- Skalę druku (1:24, 1:18…) wybierasz dopiero przy eksporcie, jedną liczbą.
  Możesz wydrukować ten sam model w dwóch skalach.

**Ostrzeżenie:** blueprinty z internetu często **nie zgadzają się same ze
sobą**: dach na boku jest o 2 cm wyżej niż na przodzie albo rozstaw osi
różni się od katalogowego. To normalne. Zasada kompromisu:
- **długość, rozstaw osi, wysokość** bierz z widoku z boku,
- **szerokość** z widoku z przodu lub z góry,
- przy sprzecznościach wygrywają **wymiary katalogowe** (Wikipedia, dane
  producenta), a szczegóły kształtu weryfikujesz na **zdjęciach**.

### Krok 1 — przygotuj obrazki (poza Blenderem)

1. Znajdź blueprint: wyszukaj `<marka model rocznik> blueprint`
   (np. the-blueprints.com, drawingdatabase.com; dokładniejsze, płatne:
   getoutlines.com). Szukaj takiego, w którym wszystkie rzuty mają tę samą skalę.
2. Zapisz wymiary katalogowe: **długość, szerokość (bez lusterek), wysokość,
   rozstaw osi**.
3. W darmowym edytorze (Photopea w przeglądarce albo GIMP) wytnij każdy rzut
   do osobnego pliku: `bok.png`, `przod.png`, `tyl.png`, `gora.png`.
   **Przycinaj ciasno do obrysu auta** (od zderzaka do zderzaka, od ziemi
   do dachu). *Dlaczego:* wtedy krawędź obrazka = krawędź auta, a dopasowanie
   skali w Blenderze sprowadza się do zrównania dwóch krawędzi.
4. Sprawdź kierunki: na `bok.png` **przód auta ma być po lewej**, a na
   `gora.png` **przód auta ma być na dole**. Jeśli jest odwrotnie, odbij obrazek
   w edytorze (`Image > Flip Horizontal` / `Vertical`).
   *Dlaczego:* w widoku Right (`Numpad 3`) oś −Y jest po lewej, a w widoku Top
   (`Numpad 7`) na dole. Tam patrzy przód auta (ustaliliśmy: przód = −Y).
5. Zapisz obrazki w folderze projektu: `projekty/<auto>/cad/blueprinty/`.

### Krok 2 — nowa scena i jednostki

1. `File > New > General`.
2. Kursor nad viewportem, kliknij kostkę i naciśnij `X` → `Delete`.
3. `File > Save As` i zapisz jako `projekty/<auto>/cad/<auto>.blend`.
   *Dlaczego od razu:* Blender zapisuje ścieżki do obrazków **względnie**
   do pliku `.blend`. Jeśli zapiszesz go przed wczytaniem obrazków, cały folder
   da się przenieść (albo sklonować z gita) bez gubienia tła.
4. Properties → zakładka **Scene** (stożek z kulką) → panel `Units`:
   `Unit System: Metric`, `Unit Scale: 1.0`, `Length: Meters`.
   To ustawienia domyślne, tylko sprawdź.

### Krok 3 — „miarka”, czyli pudełko o wymiarach auta

To jest trik, który sprawia, że wszystkie rzuty zgrają się ze sobą.

1. `Shift + A > Mesh > Cube`.
2. `N` otwiera sidebar → zakładka `Item` → w polach **Dimensions** wpisz:
   `X` = szerokość auta, `Y` = długość, `Z` = wysokość
   (np. `1.75m`, `4.255m`, `1.45m`).
3. W polu `Location Z` wpisz **połowę wysokości** (np. `0.725m`), żeby spód
   pudełka leżał na ziemi (Z = 0). `Location X` i `Y` zostaw 0.
   *Dlaczego Z = połowa:* origin kostki jest w jej środku.
4. `F2` i nazwij ją `miarka`.
5. Properties → zakładka **Object** (pomarańczowy kwadrat) → panel
   `Viewport Display` → `Display As: Wire`. Kostka staje się przezroczystym
   szkieletem i nie zasłania rysunku.
6. *(opcjonalnie)* Druga, płaska miarka do rozstawu osi: kolejna kostka
   o wymiarach `X 0.05`, `Y = rozstaw osi`, `Z 0.05`, też jako Wire.
   Później posłuży do ustawienia środków kół.

Teraz każdy rzut ma do czego się „przyłożyć”: zderzaki dotykają ścian
pudełka, opony dotykają spodu, a dach dotyka góry.

### Krok 4 — widok z boku

1. Kursor nad viewportem: `Numpad 3` (Right).
2. `Shift + A > Image > Reference` i wybierz `bok.png`. Obrazek pojawia się
   ustawiony przodem do aktualnego widoku. Dlatego najpierw ustawiasz widok,
   a dopiero potem dodajesz obrazek.
3. `F2` → `bp_bok`.
4. Properties → ostatnia zakładka **Object Data** (dla obrazka ma ikonę
   obrazka/osi). Ustaw:
   - `Opacity` ✓, wartość **0.5**: rysunek półprzezroczysty, siatka widoczna.
   - `Depth: Front`: rysunek zawsze nad modelem, więc go nie zasłonisz.
     Instrukcja Blendera zaleca to przy modelowaniu z referencji: Front
     + niskie Opacity.
   - `Show In`: `Orthographic` ✓, `Perspective` ✗, **`Only Axis Aligned`** ✓.
     *Dlaczego:* rysunek boku jest widoczny tylko, gdy patrzysz dokładnie
     z boku. W innych widokach i przy obracaniu nie zaśmieca ekranu.
5. Dopasuj do miarki (kursor nad viewportem, zaznaczony `bp_bok`):
   - `S` i ruszaj myszą, aż długość auta na rysunku = długość pudełka,
   - `G Y` przesuwa poziomo, aż zderzaki stykają się ze ścianami pudełka,
   - `G Z` przesuwa w pionie, aż opony stoją na spodzie pudełka.
   - Dla precyzji przybliż widok (kółko) na zderzak. `Shift` podczas ruchu
     myszą daje wolniejszy, dokładniejszy ruch.
6. Sprawdź środki kół z miarką rozstawu osi. Jeśli się nie zgadzają
   (blueprint jest „krzywy”), ustal kompromis według zasad z teorii.

### Krok 5 — przód, tył, góra

Powtarzasz krok 4 dla każdego rzutu, zmieniając tylko widok przed dodaniem obrazka:

| Obrazek | Widok przed `Shift+A > Image > Reference` | Dopasuj do pudełka |
|---|---|---|
| `przod.png` | `Numpad 1` (Front) | szerokość X i wysokość Z, środek auta w X = 0 |
| `tyl.png` | `Ctrl + Numpad 1` (Back) | jak wyżej |
| `gora.png` | `Numpad 7` (Top) | szerokość X i długość Y |

Dla `bp_przod` i `bp_tyl` ustaw dodatkowo **`Side: Front`**. *Dlaczego:* oba
leżą w tej samej osi, więc bez tego w widoku z przodu prześwitywałby też tył.
`Side: Front` pokazuje obrazek tylko od strony, w którą jest zwrócony.

**Kontrola krzyżowa:** wysokość dachu na boku = wysokość dachu na przodzie,
a oś przedniego koła na boku = oś przedniego koła na górze. Jeśli różnica jest
większa niż 1–2 cm, coś jest źle przeskalowane.

### Krok 6 — uporządkuj i zablokuj

1. Zaznacz wszystkie `bp_*` (`Shift` + klik w Outlinerze), kursor nad
   viewportem, `M` → `+ New Collection` → nazwa `Blueprinty`.
2. W Outlinerze kliknij ikonę lejka (Filter) u góry → w `Restriction Toggles`
   włącz **strzałkę** (Selectable). Pojawi się kolumna strzałek: kliknij
   strzałkę przy kolekcji `Blueprinty`, żeby ją wyszarzyć.
   *Dlaczego:* obrazka nie da się już zaznaczyć, więc nie przesuniesz go
   przypadkiem podczas modelowania. To najczęstsza katastrofa w tym procesie.
3. `Ctrl + S`.

➡️ **Ćwiczenie 2.**

---

## Lekcja 3 — karoseria: modelowanie od płaszczyzny

### Teoria

To jest „rozciąganie”, które widziałeś: zaczynasz od małej płaszczyzny
i **wyciągasz (extrude, `E`) jej krawędzie** wzdłuż linii rysunku, jakbyś
obrysowywał auto kawałkami taśmy. Potem w innych widokach przesuwasz
wierzchołki w głąb, aż płaski obrys stanie się bryłą.

Trzy zasady, które decydują, czy wyjdzie gładko:

1. **Tylko czworokąty (quads).** Każda ściana ma 4 wierzchołki. Trójkąty
   i wielokąty (n-gony) robią wgniecenia, gdy siatkę wygładzasz.
2. **Mało wierzchołków, wygładzanie robi modyfikator.** Siatka bazowa ma kilkaset
   ścian, a modyfikator **Subdivision Surface** dzieli je i zaokrągla.
   *Dlaczego:* łatwiej kontrolować 300 punktów niż 30 000. Każdy dodatkowy
   wierzchołek to kolejne miejsce, gdzie może powstać garb.
3. **Krawędzie biegną wzdłuż linii auta**, czyli szpar drzwi, linii
   bocznego przetłoczenia, krawędzi maski i łuku nadkola. To się nazywa
   *edge flow*. Gdy siatka idzie zgodnie z kształtem, łatwo go uzyskać,
   a gdy w poprzek, walczysz z każdym wierzchołkiem.

**Modelujesz tylko połowę auta.** Modyfikator **Mirror** dorysowuje drugą
połowę na bieżąco. Połowa pracy, a symetria gwarantowana.

**Pierwsze auto: zrób wersję uproszczoną.** Bez klamek, wycieraczek,
szczelin drzwi. Okna jako część powierzchni (możesz je później wydrukować
innym kolorem). Celem jest poprawna bryła, na której zbudujesz bodykit.

### Krok 1 — płaszczyzna startowa (w Edit Mode!)

1. `Numpad 3` (bok). Upewnij się, że 3D Cursor jest w środku (`Shift + C`).
2. `Shift + A > Mesh > Plane`. `F2` → `karoseria`.
3. **`Tab`** wchodzi w Edit Mode. Wszystko jest zaznaczone (pomarańczowe).
4. `R Y 90`, `Enter`. Płaszczyzna staje pionowo, przodem do widoku z boku.
5. `S 0.15`: zmniejsz ją do rozmiaru jednego „kafelka”.
6. `G` i przesuń ją nad przednie nadkole, a potem `G X 0.85` (mniej więcej
   połowa szerokości auta, czyli bok karoserii).

**Dlaczego obrót i ruch w Edit Mode, a nie w Object Mode:** origin obiektu
zostaje w środku świata (X = 0), a jego osie nie są obrócone. Mirror odbija
względem osi X **obiektu**, więc lustro wypada dokładnie na środku auta.
Gdybyś obrócił obiekt o 90° w Object Mode, „oś X lustra” wskazywałaby w dół
i odbicie poszłoby pod podłogę.

### Krok 2 — Mirror od razu

1. `Tab` wraca do Object Mode.
2. Properties → **Modifiers** (niebieski klucz) → `Add Modifier > Generate >
   Mirror`.
3. `Axis: X` (domyślnie). Zaznacz **`Clipping`**.
   *Dlaczego Clipping:* wierzchołek, który dociągniesz do środka (X = 0),
   „przykleja się” do płaszczyzny lustra i nie przejdzie na drugą stronę.
   Bez tego na środku maski i dachu zostaje szpara.
4. W widoku z przodu (`Numpad 1`) zobaczysz dwie płaszczyzny po obu stronach.

### Krok 3 — obrys boku (widok `Numpad 3`)

Narzędzia Edit Mode, których tu użyjesz:

| Akcja | Skrót |
|---|---|
| Tryb: wierzchołki / krawędzie / ściany | `1` / `2` / `3` (z Emulate Numpad: ikony w headerze obok `Edit Mode`) |
| Wyciągnij (extrude) | `E` |
| Zaznacz pętlę krawędzi | `Alt` + lewy klik na krawędzi |
| Dodaj pętlę cięcia | `Ctrl + R`, kółkiem zmień liczbę, lewy klik, potem prawy klik (zostaje na środku) |
| Wypełnij między krawędziami | `F` |
| Edycja proporcjonalna (miękki ruch) | `O`, promień zmieniasz kółkiem podczas ruchu |
| X-ray (widać i zaznaczasz przez model) | `Alt + Z` |

Kolejność:

1. **Tryb krawędzi** (`2`). Włącz X-ray (`Alt + Z`).
2. **Nadkola.** Zaznacz górną krawędź kafelka, `E` i ciągnij wzdłuż łuku
   nadkola. Powtarzaj, aż obejdziesz łuk (wystarczy 6–8 kroków). Każdy kafelek
   ustaw tak, by jedna krawędź leżała na łuku, a druga trochę dalej od koła.
   Powstaje pierścień kafelków wokół koła. To samo zrób dla tylnego nadkola.
   - *Alternatywa:* `Shift + A > Circle` (w Edit Mode doda się do tego samego
     obiektu), w panelu Adjust Last Operation ustaw `Vertices: 16`
     i `Align: View`, przeskaluj do łuku, usuń dolną połowę wierzchołków
     (`X > Vertices`), zaznacz resztę, `E`, `S 1.2`, i pierścień gotowy.
3. **Próg.** Połącz dolne końce obu pierścieni: zaznacz dwie naprzeciwległe
   krawędzie, `F` utworzy między nimi ścianę. Potem `Ctrl + R` dodaj na niej
   pętle cięcia, żeby kafelki miały podobny rozmiar.
4. **Do linii okien.** Zaznacz górne krawędzie pasa nad nadkolami i progiem
   (`Shift` + klik po kolei), `E`, `Z` i wyciągnij do linii pod szybami.
5. **Przód i tył.** Wyciągaj skrajne krawędzie do przodu (do zderzaka)
   i do tyłu tak samo.
6. **Kabina.** Wyciągnij górną krawędź w górę wzdłuż słupków i szyb do dachu.

Masz płaski „wycinek” boku auta, z dziurami na koła.

### Krok 4 — nadaj kształt w 3D (widoki `Numpad 1` i `Numpad 7`)

1. `Numpad 7` (góra): zaznaczaj kolumny wierzchołków (prostokątem, z X-ray)
   i przesuwaj `G X` tak, by obrys pokrywał się z widokiem z góry. Przód
   i tył auta zwężają się, a kabina jest węższa od nadwozia.
2. `Numpad 1` (przód): to samo dla przekroju. Boki są lekko wypukłe, a szyby
   pochylone do środka.
3. **Maska, dach, klapa:** zaznacz górną krawędź (np. przy masce), `E X`
   i wyciągnij do środka, aż Clipping ją zatrzyma na X = 0. Potem `Ctrl + R`
   dodaj 1–2 pętle wzdłuż, żeby maska mogła się zaokrąglić.
4. Na bieżąco obracaj widok w perspektywie (środkowy przycisk) i szukaj garbów.
   Jeśli wierzchołek odstaje, przesuń go z `O` (proporcjonalnie), wtedy
   sąsiedzi pójdą miękko za nim.

### Krok 5 — wygładzenie

1. `Tab` do Object Mode.
2. `Add Modifier > Generate > Subdivision Surface`, `Levels Viewport: 2`.
   Na liście modyfikatorów Mirror musi być **nad** Subdivision, czyli najpierw
   odbicie, potem wygładzenie. Inaczej środek auta będzie miał bruzdę.
   Kolejność zmieniasz, przeciągając modyfikator za kropki po prawej stronie
   jego nagłówka.
3. Prawy klik na modelu → `Shade Smooth`.
4. Gdy krawędź ma być ostra (np. kant progu), dodaj blisko niej pętlę
   (`Ctrl + R`). Im bliżej, tym ostrzej. To *support loop*.

### Kontrola jakości siatki

- **Statystyki:** strzałka obok ikony Overlays (dwa kółka w headerze) →
  `Statistics`. Pokazuje liczbę ścian i wierzchołków.
- **Nie-czworokąty:** w Edit Mode `Select > Select All by Trait > Faces by Sides`,
  potem w panelu Adjust Last Operation `Number of Vertices: 4`,
  `Type: Not Equal To`. Zaznaczy się wszystko, co nie jest quadem.
- **Zdublowane wierzchołki:** `A`, potem `M > By Distance`.
- **Odwrócone ściany:** Overlays → `Face Orientation`. Czerwony = tył ściany
  na zewnątrz (źle). Napraw: `A`, `Shift + N`. To ważne przy druku i przy
  Solidify w lekcji 4.

➡️ **Ćwiczenie 3.**

---

## Lekcja 4 — bodykit

### Teoria

Elementy bodykitu: **dokładka przednia / splitter**, **progi (side skirts)**,
**dyfuzor tylny**, **spoiler / skrzydło**, **poszerzenia nadkoli**.

Główna technika: **powierzchnia montażowa części to kopia ścian karoserii.**
1. Kopiujesz ściany nadwozia w miejscu, gdzie część przylega.
2. Odłączasz je jako osobny obiekt.
3. Od tej kopii wyciągasz kształt części na zewnątrz.
4. Nadajesz grubość modyfikatorem **Solidify**.

*Dlaczego tak, a nie od zera:* wewnętrzna strona części jest z definicji
identyczna z powierzchnią auta, więc nie ma szczelin. Przy druku to znaczy,
że część przylega na całej długości, a nie tylko na trzech punktach.

*Dlaczego osobne obiekty:* każdą część drukujesz w innej orientacji (najlepszej
dla niej) i innym kolorem **bez wieży czyszczącej** AMS (czarny splitter,
karoseria w kolorze nadwozia). Druk całości w multicolor zmarnowałby
dużo filamentu na zmiany koloru.

### Splitter / dokładka przednia (krok po kroku)

1. Zaznacz `karoseria`, `Tab`, tryb ścian (`3`).
2. Zaznacz rząd ścian na dole przedniego zderzaka: `Alt` + klik zaznacza
   całą pętlę, `Shift + Alt` + klik dodaje kolejną.
3. `Shift + D`, a potem od razu **prawy klik**. Kopia zostaje dokładnie
   w miejscu oryginału.
4. `P > Selection`: kopia staje się osobnym obiektem. Modyfikatory (Mirror,
   Subdivision) przechodzą na nowy obiekt razem z nią.
5. `Tab` (Object Mode), kliknij nowy obiekt, `F2` → `splitter_przod`.
6. Zaznacz tylko `splitter_przod`, `Tab`, tryb krawędzi. Zaznacz dolną pętlę
   krawędzi (`Alt` + klik).
7. `E Z` i ciągnij w dół o kilka cm, potem znów `E` i `G Y` do przodu.
   Powstaje „półka” wystająca przed zderzak. W widoku z boku dopasuj ją
   do własnego projektu albo zdjęcia referencyjnego.
8. `Tab`, `Add Modifier > Generate > Solidify`:
   - `Thickness`: patrz ramka o skali poniżej,
   - `Offset: 1` (zamiast domyślnego −1): grubość narasta **na zewnątrz**
     od karoserii, a wewnętrzna strona zostaje na jej powierzchni,
   - `Even Thickness` ✓: równa grubość na zakrętach.
   - Kolejność: Mirror → Subdivision → **Solidify** (grubość na końcu,
     z już gładkiej powierzchni).

> **Grubość w modelu skali, czyli najważniejsza pułapka DfAM w tym kursie.**
> Prawdziwy splitter ma ~4 mm grubości. W skali 1:24 to **0,17 mm**, czyli
> mniej niż pół szerokości ścieżki dyszy 0.4. Nie wydrukuje się.
> Minimalna ścianka to 1,2 mm **na wydruku**, więc w modelu w prawdziwej skali:
>
> `grubość w Blenderze = 1,2 mm × mianownik skali`
>
> 1:24 → **29 mm**, 1:18 → **22 mm**. Elementy bodykitu w modelach skali
> są więc zawsze **pogrubione** względem oryginału. Robią to też fabryczne
> modele diecast. Wpisuj w `Thickness` np. `30mm`.

### Progi (side skirts)

Ta sama technika: kopiujesz pas ścian pod drzwiami, między nadkolami
(`Shift + D`, prawy klik, `P`), wyciągasz dolną krawędź w dół i na zewnątrz
(`E Z`, potem `E` + `G X`), a na koniec Solidify jak wyżej.

### Poszerzenia nadkoli

Kopiujesz pierścień ścian wokół nadkola. Potem w trybie ścian
`Alt + E > Extrude Faces Along Normals` wyciąga je równo „od karoserii”,
a skalowaniem (`S`) poszerzasz łuk na zewnątrz.

### Spoiler / skrzydło

Tu nie ma powierzchni do skopiowania, bo to osobna bryła:
1. `Numpad 3`, `Shift + A > Mesh > Plane`, w Edit Mode `R Y 90`
   (jak w lekcji 3), a potem zbuduj **profil skrzydła** (przekrój jak kropla
   łezki, spłaszczona) z 8–12 wierzchołków. Wierzchołki przesuwasz `G`.
2. Wyciągnij profil na szerokość: zaznacz wszystko, `E X` do połowy
   szerokości auta. Druga połowa dorysuje się z Mirror (dodaj go).
3. Stójki (mocowania) zrób z kostek. Pamiętaj, że w skali też muszą mieć
   ≥ 1,2 mm na wydruku. W praktyce będą grubsze niż w oryginale.

➡️ **Ćwiczenie 4.**

---

## Lekcja 5 — przygotowanie do druku na A1

### Teoria: STL nie ma jednostek

Plik STL to same liczby. Bambu Studio czyta je jako **milimetry**. Blender
zapisuje swoje jednostki, czyli **metry**. Auto o długości 4,255 m bez
przeliczenia wczyta się jako kostka 4,255 **mm**.
Dlatego skalę ustawiasz w eksporcie:

`Scale w eksporcie = 1000 / mianownik skali`

| Skala druku | Scale w eksporcie | Auto 4,255 m na wydruku | Mieści się w 256 mm? |
|---|---|---|---|
| 1:24 | `41.667` | 177 mm | tak |
| 1:18 | `55.556` | 236 mm | tak, ale ciasno (po przekątnej jest zapas) |
| 1:12 | `83.333` | 355 mm | **nie**, trzeba by dzielić karoserię |

### Krok 1 — wtyczka 3D Print Toolbox

1. `Edit > Preferences > Get Extensions`. Jeśli prosi, zezwól na dostęp online
   (`Allow Online Access`).
2. Wyszukaj `3D Print Toolbox` → `Install`.
3. W viewporcie, w sidebarze (`N`), pojawi się zakładka **3D-Print**.

### Krok 2 — wersja „do druku” (oryginał zostaje edytowalny)

1. Zaznacz część, `Shift + D`, prawy klik (kopia w miejscu), `M` → nowa
   kolekcja `Do_druku`. Ukryj kolekcję z oryginałami (oko w Outlinerze).
2. Na kopii: `Object > Convert > Mesh`. To **zatwierdza (apply) wszystkie
   modyfikatory**: lustro, wygładzenie i grubość stają się prawdziwą geometrią.
3. **Karoseria musi być zamkniętą bryłą.** Siatka z lekcji 3 to powłoka bez dna.
   Najprostsze rozwiązanie dla modelu wystawowego: w Edit Mode zaznacz dolną
   pętlę krawędzi, `E Z` w dół do wysokości podłogi, a potem `F` (albo
   `Face > Grid Fill`) zamyka dno płaską ścianą. Płaskie dno = idealna
   pierwsza warstwa na stole.
4. Zakładka **3D-Print** → `Check All`. Wymagane:
   - `Non Manifold Edge: 0`: bryła szczelna (slicer nie zgaduje, co jest środkiem),
   - `Intersect Face: 0`: nic nie przenika samo siebie.
   - `Thickness` ustaw na **29 mm** (dla 1:24, z ramki w lekcji 4) i sprawdź,
     czy nic nie jest za cienkie.

### Krok 3 — eksport

1. Zaznacz jedną część (np. `splitter_przod` z kolekcji `Do_druku`).
2. `File > Export > STL (.stl)`. Po prawej stronie okna:
   - `Selection Only` ✓,
   - `Scale`: `41.667` (dla 1:24),
   - `Forward` / `Up` zostaw domyślne (Z w górę, tak samo jak w Bambu Studio).
3. Zapisz jako `projekty/<auto>/stl/splitter_przod.stl`.
4. W Bambu Studio po imporcie **sprawdź wymiar** (narzędzie skalowania pokazuje
   rozmiar w mm). Auto 1:24 ma mieć długość = prawdziwa długość / 24.

### Orientacja na stole — punkt wyjścia (do weryfikacji wydrukiem)

| Część | Orientacja | Podpory |
|---|---|---|
| Karoseria | na płaskim dnie | prawdopodobnie tylko w nadkolach (górna część łuku to zwis > 45°); drzewiaste (`tree`) |
| Splitter / progi | najczęściej płaską, montażową stroną do stołu, długością wzdłuż stołu | zależnie od kształtu; sprawdź podgląd zwisów w slicerze |
| Spoiler | na tylnej krawędzi albo płasko na spodzie, do przetestowania | w zależności od profilu |

Materiał: **PLA Matte**, bo to model wystawowy (nie ASA: nie jedzie
w samochodzie). Warstwa: profil `0.12mm Fine` w Bambu Studio jako start, bo
w modelu skali widać schodki na zaokrągleniach. **Do sprawdzenia testem
na A1.**

➡️ **Ćwiczenie 5.**

---

## Ściąga skrótów

| Skrót | Co robi | Gdzie |
|---|---|---|
| środkowy / `Shift`+środkowy / kółko | obrót / przesuw / zoom widoku | wszędzie |
| `Numpad 1 / 3 / 7` (+`Ctrl` = przeciwna strona) | przód / prawy bok / góra | wszędzie |
| `Numpad 5` | perspektywa ↔ ortogonalny | wszędzie |
| `Numpad .` / `Home` | centruj na zaznaczonym / pokaż wszystko | wszędzie |
| `N` / `T` | sidebar (wymiary) / toolbar | wszędzie |
| `Tab` | Object ↔ Edit Mode | wszędzie |
| `Shift + A` | dodaj | wszędzie |
| `G` / `R` / `S` + `X/Y/Z` + liczba | przesuń / obróć / skaluj | wszędzie |
| `Shift + D`, potem prawy klik | duplikat w miejscu | wszędzie |
| `F2` | zmień nazwę | wszędzie |
| `Alt + Z` | X-ray | wszędzie |
| `Shift + C` | kursor do środka + pokaż wszystko | wszędzie |
| `1 / 2 / 3` | wierzchołki / krawędzie / ściany | Edit |
| `E` | extrude | Edit |
| `Alt` + klik | zaznacz pętlę | Edit |
| `Ctrl + R` | pętla cięcia | Edit |
| `F` | wypełnij ścianę | Edit |
| `O` | edycja proporcjonalna | Edit |
| `P` | odłącz do osobnego obiektu | Edit |
| `M > By Distance` | scal zdublowane wierzchołki | Edit |
| `Shift + N` | popraw kierunek ścian (normalne) | Edit |
| `F9` | panel ostatniej operacji | wszędzie |
| `Ctrl + Z` | cofnij | wszędzie |

## Pułapki początkującego

- **Skrót nie działa:** kursor nie jest nad viewportem albo jesteś w złym
  trybie (sprawdź listę `Object Mode` / `Edit Mode` w headerze).
- **Obiekt „zniknął”:** ukryty przez przypadkowe `H` (`Alt + H` pokazuje
  wszystko) albo jesteś daleko od niego (`Home`).
- **Skalowałeś w Object Mode, a Solidify / zaokrąglenia są krzywe:** skala
  obiektu różna od 1. Napraw: Object Mode, `Ctrl + A > Scale`.
- **Mirror odbija w złą stronę:** obiekt obrócony w Object Mode albo origin
  nie jest w X = 0. Patrz lekcja 3, krok 1.
- **Przesunąłeś blueprint:** `Ctrl + Z`, a potem zablokuj kolekcję
  (lekcja 2, krok 6).
- **Plik `.blend1`:** to automatyczna kopia zapasowa poprzedniego zapisu.
  Przydaje się, gdy coś zepsujesz i zapiszesz, ale nie trafia do gita.
