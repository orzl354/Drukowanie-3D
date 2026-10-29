# Etui MacBook Air 13" (2024) — podział pod Bambu A1

Model: *MacBook Air Hard Case* (autor **ByteSlinger**, MakerWorld, licencja
*Standard Digital File License*). Licencja nie pozwala rozpowszechniać pliku, więc
w repo jest **tylko mój skrypt podziału** (`cad/podziel_etui.py`), bez siatek.
STL-e i 3mf generuję lokalnie z oryginalnego pliku.

## Cel
Oryginał ma 315 × 241 mm i był projektowany pod H2D. Na A1 (256 × 256) trzeba
przeciąć dno i pokrywę tak, żeby po sklejeniu szew był prawie niewidoczny,
powierzchnie się licowały i nic nie wystawało do środka (MacBook siedzi na wcisk).

## Decyzje projektowe (dlaczego tak)
**Gdzie ciąć: x = −52.5 mm (części 105 + 210 mm), nie na środku.**
Środek odpada, bo tam jest środkowy zawias (|x| < 15) i zatrzask pokrywy,
a w dnie kanał zamka zajmuje x ∈ [−35, 90]. W x = −52.5 przekrój jest „czysty”:
dno 5,3 mm, ścianki 4,85 mm, pokrywa to płaska płyta 5 mm. Podział 1/3 : 2/3
wygląda na zamierzoną linię podziału. Szew dna i pokrywy wypada w tym samym
miejscu, więc po zamknięciu wygląda jak jedna linia dookoła etui.

**Złącze: motylki wpuszczane od środka + kołki z filamentu + klej.**
- *Motylek (bow-tie, „jaskółka podwójna”)*: klucz w kształcie muszki wklejony w gniazdo
  przechodzące przez szew. Przewężenie na linii szwu sprawia, że połówek nie da się
  rozciągnąć nawet przed związaniem kleju. Klucz drukuje się **płasko**, więc jego
  warstwy biegną *w poprzek* szwu i to on przenosi zginanie, a nie słabe sklejenie
  czołowe. Gniazda są otwarte do góry przy druku, więc nie potrzebują podpór.
- *Dlaczego nie pióro-wpust albo zakładka?* Przy druku dnem do stołu pióro wystające
  z powierzchni cięcia byłoby poziomym nawisem na całej długości 241 mm. Motylek nie ma
  tego problemu.
- *Kołki z filamentu 1,75* (kawałki ze szpuli, Ø otworu 2,0, po 8 mm w każdą stronę):
  ustawiają połówki w osi Y/Z podczas klejenia, także w ściankach, gdzie nie ma miejsca
  na motylka.
- *Klucz jest 0,1 mm cieńszy niż gniazdo*, więc nigdy nie wystaje do środka.
  Zagłębienie 0,1 mm jest niewidoczne, a wystający klucz dociskałby laptopa.

**Mikrofaza 0,3 mm × 45° na zewnętrznych krawędziach szwu.**
Dwie powierzchnie stykane „na zero” nigdy nie wyjdą idealnie: 0,1 mm różnicy daje
ząbek, który widać i czuć palcem. Faza zmienia to w cienką, równą linię, która wygląda
na zamierzoną (tak robi się szczeliny w obudowach elektroniki). Przy okazji usuwa
problem stopy słonia, czyli rozlanej pierwszej warstwy, która blokuje dokładny styk
przy stole. `FAZA_SZWU = 0` w skrypcie ją wyłącza.

## Materiał
Do wyboru PLA (jak w oryginale) albo PETG. **PETG jest lepszy na etui**, bo jest mniej
kruchy przy upadku. Klej: CA (cyjanoakrylowy, „kropelka”) w żelu. Daje czas na ustawienie
i wypełnia drobne szczeliny. Przy PETG CA trzyma słabiej, więc tam motylki są ważniejsze.

## Ustawienia druku
| | |
|---|---|
| Warstwa | 0,2 mm (jak w oryginale) |
| Ścianki | 2 (oryginał); **3 przy dnie i pokrywie**, żeby kołki i gniazda miały „mięso” — do decyzji |
| Wypełnienie | 15% (oryginał); klucze **100%** |
| Orientacja | dno i pokrywa zewnętrzną stroną na stole, klucze płasko (pliki są już tak ułożone) |
| Podpory | jak w oryginale: normal(auto), *tylko od stołu*. Otwory na kołki nie potrzebują podpór |
| Płyty | 3 pliki `plytaN_*.3mf`, każdy mieści się na A1 z marginesem 3 mm |
| Uwagi | stopa słonia: zostaw domyślną kompensację w Bambu Studio |

Modyfikator z oryginału (kostka 30% wypełnienia przy zatrzasku pokrywy) **nie został
przeniesiony**. Jeśli chcesz go zachować, dodaj w Bambu Studio modyfikator „Kostka” na
`pokrywa_prawa` przy zatrzasku i ustaw 30%.

## Montaż
1. **Na sucho**: wsadź kołki (filament 1,75 przycięty na ~15 mm), złóż połówki i włóż
   motylki. Sprawdź, czy szew się zamyka, a klucze siedzą równo.
2. Połóż obie połówki **zewnętrzną stroną na szybie / lustrze / blacie** (płaska
   powierzchnia wymusza zlicowanie od zewnątrz).
3. Cienka warstwa CA na powierzchnię cięcia, kołki w otwory, dociśnij połówki.
4. Klej w gniazda, wciśnij motylki, dociśnij płaskim klockiem. Nadmiar kleju zetrzyj od razu.
5. Tak samo pokrywa. Na koniec montaż wg instrukcji oryginału (wkładki gwintowane, śruby, zamek).

## Regeneracja plików
```bash
pip install numpy trimesh manifold3d shapely networkx
python3 cad/podziel_etui.py MacBookAirCase.3mf wyjscie/
```
Wszystkie wymiary (miejsce cięcia, luzy, kształt motylka, kołki, faza) są na górze skryptu.

## Status
`szkic` — pliki wygenerowane i sprawdzone numerycznie (brak kolizji, klucz 0,1 mm pod
powierzchnią, objętości się zgadzają), nic jeszcze nie wydrukowane.

## Wnioski
Do sprawdzenia na A1 **przed** drukiem całości: wytnij w Bambu Studio pasek ~40 mm wokół
szwu (oba fragmenty + 1 motylek) i wydrukuj test.
- luz motylka 0,15 / stronę: za ciasno → 0,2, za luźno → 0,1,
- otwór 2,0 pod filament 1,75: poziome otwory wychodzą mniejsze, więc jeśli kołek nie wchodzi, daj 2,1,
- czy faza 0,3 daje ładną linię, czy wolę 0,2.
