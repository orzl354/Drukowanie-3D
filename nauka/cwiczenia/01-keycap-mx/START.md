# Od czego zacząć — lista kroków

Lista do odhaczania. Robisz po kolei, nie przeskakujesz.
Całość to ok. **3 godziny**, z czego połowa to czekanie na drukarkę — te fragmenty
są tak ułożone, żeby druk szedł w tle, kiedy Ty robisz coś innego.

Maszyna nie ma znaczenia — PC czy MacBook, byle na start zrobić `git pull`,
a na koniec `git push` (dlaczego to takie ważne: [notatka o ustawieniach](../../notatki/freecad-01-instalacja-i-ustawienia.md#5-praca-na-dwóch-maszynach--git)).

---

## Etap 0 — pobierz repo na maszynę (5 min)

Jeśli jeszcze nie masz go lokalnie:

```bash
git clone https://github.com/orzl354/Drukowanie-3D.git
cd Drukowanie-3D
git checkout claude/intelligent-franklin-1fiboy
```

Jeśli masz:

```bash
cd Drukowanie-3D
git fetch origin
git checkout claude/intelligent-franklin-1fiboy
git pull origin claude/intelligent-franklin-1fiboy
```

- [ ] Widzisz plik `kalibracja/01-gniazdo-mx/gniazdo-mx.stl`

---

## Etap 1 — wystartuj druk drabinki (10 min pracy + 40 min druku)

**To jest pierwsza rzecz, jaką robisz — druk idzie w tle przez cały etap 2.**

1. Otwórz `kalibracja/01-gniazdo-mx/gniazdo-mx.stl` w Bambu Studio.
2. Filament: **PLA Matte** (ten sam, którym potem wydrukujesz keycapa).
3. Ustaw i **zapisz w pamięci**, bo keycap musi iść identycznie:

   | | |
   |---|---|
   | Wysokość warstwy | **0,12 mm** |
   | Ścianki | 3 |
   | Wypełnienie | 15% |
   | Podpory | brak |

4. Slice → wyślij na drukarkę. Płytka leży płasko, gniazdami do góry — nic nie obracaj.

- [ ] Druk ruszył

**Nie czekaj przy drukarce.** Przejdź od razu do etapu 2.

---

## Etap 2 — FreeCAD: instalacja i ustawienia (30 min, w czasie druku)

Prowadzi Cię [`notatki/freecad-01-instalacja-i-ustawienia.md`](../../notatki/freecad-01-instalacja-i-ustawienia.md).

- [ ] FreeCAD **1.0 lub nowszy** zainstalowany (macOS: uważaj na arm64 vs x86_64 i na
      pierwsze uruchomienie przez prawy klik → Open)
- [ ] Jednostki: **Standard (mm, kg, s, degree)**
- [ ] Liczba miejsc po przecinku: **3** — bez tego nie zobaczysz różnicy 0,05 mm
- [ ] Autozapis co 5 min
- [ ] Nawigacja: PC → **CAD**, MacBook na gładziku → **Gesture**
- [ ] Wersję FreeCAD wpisaną do tabelki na końcu notatki

Potem **przeczytaj** (nie klikaj jeszcze nic w modelu):
[`notatki/freecad-03-part-design.md`](../../notatki/freecad-03-part-design.md) — 10 minut,
głównie porównanie z OpenSCAD, który już znasz.

- [ ] Wiesz, czym różni się **Part** od **Part Design** i dlaczego szkic ma być zielony

---

## Etap 3 — odczytaj drabinkę (15 min, po wydruku)

Instrukcja: [`kalibracja/01-gniazdo-mx/README.md`](../../../kalibracja/01-gniazdo-mx/)

> ⚠️ **Wyjmij jeden przełącznik z klawiatury ściągaczem i testuj na nim, trzymając go
> w palcach.** Nie wciskaj płytki na przełącznik osadzony w PCB — za ciasne gniazdo potrafi
> wyrwać przełącznik razem z gniazdem hot-swap. To jedyny moment w całym projekcie,
> w którym da się uszkodzić klawiaturę.

1. Wciskaj trzpień kolejno od największego gniazda (●●●●●) w dół.
2. Szukasz **najciaśniejszego, które wchodzi bez siły i trzyma po odwróceniu**.
3. Włóż i wyjmij 5 razy — jeśli zaczyna luzować, weź o stopień ciaśniej.

- [ ] Tabela wyników w `kalibracja/01-gniazdo-mx/README.md` wypełniona
- [ ] Znasz swoją wartość **`krzyz_luz` = ______ mm**
- [ ] Przełącznik wrócił na miejsce w klawiaturze

---

## Etap 4 — zbuduj model (60–90 min)

Prowadzi Cię [`README.md`](README.md) tej lekcji, krok po kroku.

- [ ] Nowy dokument zapisany jako `projekty/keycap-mx-1u/cad/keycap-1u.FCStd`
- [ ] Arkusz `Arkusz` z 13 parametrami, wszystkie aliasy ustawione
- [ ] W wierszu 9 wpisany **Twój** `krzyz_luz` z etapu 3
- [ ] Loft (dwa szkice, oba zielone)
- [ ] Thickness
- [ ] Boss + dwa Pockety gniazda
- [ ] `sprawdz.py` przechodzi: bryła poprawna, 1 solid, gabaryt zgodny, zapas ≥ 0,4 mm
- [ ] Test parametryczności: zmiana `szer_podstawy` na 19 mm przelicza model **bez błędów**
      (potem wróć na 18)
- [ ] Eksport do `projekty/keycap-mx-1u/stl/keycap-1u-v1.stl`

---

## Etap 5 — wydrukuj v1 (10 min pracy + ~15 min druku)

- [ ] Te same ustawienia co drabinka (0,12 mm, 3 ścianki, 15%, bez podpór)
- [ ] Orientacja: **wierzchem do stołu, trzpieniem do góry** — Bambu Studio wczyta model
      podstawą do dołu, więc **obróć go o 180° wokół osi X**
- [ ] Ustaw **4 sztuki naraz** albo minimalny czas warstwy 8–10 s (warstwa ma tu ok. 2 cm²;
      bez tego kolejne warstwy kładą się na gorące i gniazdo się rozjedzie)

---

## Etap 6 — dopasuj (30 min + kolejne wydruki)

Prowadzi Cię [`pomiary.md`](pomiary.md).

- [ ] Porównanie 1 na stole → poprawka `wys_calk`
- [ ] Porównanie 2 na klawiaturze → poprawka `gniazdo_od_dolu`
- [ ] Test skoku — czy klawisz nie siada wcześniej niż sąsiad
- [ ] Dziennik dopasowania w `pomiary.md` wypełniony

Nie licz na trafienie za pierwszym razem. Dwie–trzy iteracje to normalny wynik,
a jeden keycap to ok. 15 minut i gram filamentu.

---

## Etap 7 — zamknij sesję (10 min)

- [ ] Wnioski w [`projekty/keycap-mx-1u/README.md`](../../../projekty/keycap-mx-1u/README.md) (tabela na dole)
- [ ] Wpis w [`nauka/dziennik.md`](../../dziennik.md) — wpis na 2026-09-15 czeka z pustym
      „Czego się nauczyłem"
- [ ] `git add -A && git commit -m "..." && git push -u origin claude/intelligent-franklin-1fiboy`

---

## Gdzie jestem

Zaznacz, na czym stanąłeś — następnym razem zaczynamy stąd:

```
Etap: ____
Utknąłem na: ____________________________________
```
