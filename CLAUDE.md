# CLAUDE.md — repozytorium `Drukowanie-3D`

## O czym jest to repo

To moje osobiste repozytorium do druku 3D i **nauki projektowania 3D**. Trzymam tu modele,
profile druku, notatki z nauki CAD, checklisty i dokumentację projektów.

Dwa równoległe cele:
1. **Projekty** — modele samochodów, figurki, akcesoria samochodowe (uchwyty, mocowania), części funkcjonalne.
2. **Nauka** — systematyczne opanowanie modelowania parametrycznego i dobrych praktyk DfAM (Design for Additive Manufacturing).

Traktuj mnie jak osobę uczącą się: **tłumacz "dlaczego", nie tylko "jak"**. Przy każdej decyzji
projektowej krótko uzasadnij wybór, żebym mógł go powtórzyć samodzielnie.

---

## Mój sprzęt

| | |
|---|---|
| Drukarka | **Bambu Lab A1 Combo** (bedslinger, otwarta konstrukcja) |
| Pole robocze | 256 × 256 × 256 mm |
| Dysza | 0.4 mm stalowa (standard), hotend do ~300 °C |
| Stół | Textured PEI, do 100 °C |
| Podajnik | **AMS Lite** — 4 szpule, druk wielokolorowy |
| Slicer | Bambu Studio (ewentualnie Orca Slicer) |

### Ograniczenia, o których musisz pamiętać
- **Brak komory zamkniętej** — ABS/ASA da się drukować, ale trzeba liczyć się z warpingiem
  i skurczem; projektuj z zaokrąglonymi narożnikami, brimem i unikaj dużych płaskich podstaw.
- **AMS Lite**: szpule o średnicy wewnętrznej 53–58 mm i szerokości 40–68 mm.
- **TPU i filamenty z włóknem (CF/GF) muszą być podawane zewnętrznie**, nie przez AMS Lite.
- Zmiana koloru w AMS Lite = **odpad na wieżę czyszczącą**. Przy projektach wielokolorowych
  proponuj podział na części drukowane osobno, jeśli to sensowniejsze niż multicolor.

### Moje filamenty i ich role
- **PLA / PLA Matte** → figurki, modele wystawowe, elementy dekoracyjne.
- **PETG (czarny)** → części funkcjonalne, obciążone mechanicznie.
- **ASA (szary)** → wszystko, co ląduje **w samochodzie** (PLA mięknie ~60 °C, deska rozdzielcza latem to za dużo).

Domyślnie zakładaj filamenty Bambu Lab (RFID + rozpoznawanie w AMS Lite).

---

## Struktura repozytorium

```
Drukowanie-3D/
├── projekty/              # jeden folder = jeden projekt
│   └── <nazwa-projektu>/
│       ├── README.md      # cel, status, wnioski, zdjęcia
│       ├── cad/           # pliki źródłowe (.f3d, .step, .scad, .FCStd)
│       ├── stl/           # eksporty do druku (.stl / .3mf)
│       ├── slicer/        # projekty .3mf z Bambu Studio
│       └── zdjecia/
├── nauka/
│   ├── dziennik.md        # co przerobiłem którego dnia
│   ├── cwiczenia/         # zadania modelarskie
│   └── notatki/           # skróty klawiszowe, techniki, teoria
├── profile/               # profile filamentów i procesów
├── kalibracja/            # testy tolerancji, temp tower, flow, bridging
└── biblioteka/            # własne komponenty do wielokrotnego użycia
```

---

## Jak masz mi pomagać

### Projektowanie
- Preferuję **modelowanie parametryczne**. Kod (OpenSCAD, CadQuery/build123d) generuj gotowy do
  uruchomienia, z nazwanymi zmiennymi na górze pliku i komentarzami po polsku.
- Jednostki zawsze w **milimetrach**.
- Zanim zaproponujesz model, ustal: przeznaczenie, materiał, obciążenia, wymiary krytyczne.
  Jeśli czegoś brakuje — dopytaj zamiast zgadywać.
- Przy każdym modelu podaj **zalecaną orientację na stole** i czy potrzebne są podpory.

### Domyślne tolerancje (weryfikuję je testami w `kalibracja/`)
- Pasowanie ruchome / luźne: **0.3–0.4 mm** luzu
- Pasowanie ciasne (wciskane): **0.1–0.15 mm**
- Otwory pod śruby M3: **3.2–3.4 mm**
- Minimalna grubość ścianki: **1.2 mm** (3 perymetry przy dyszy 0.4)

### DfAM — pilnuj tego przy każdym projekcie
- Zwisy powyżej ~45° → podpory albo przeprojektowanie (fazy, mostki).
- Warstwy dzielą się w osi Z — **układaj model tak, żeby siła nie rozrywała warstw**.
- Zaokrąglenia i fazy zamiast ostrych naroży (mniej naprężeń, lepsze pierwsze warstwy).
- Otwory drukowane pionowo wychodzą mniejsze — kompensuj lub rozwierć.

### Nauka
- Gdy proszę o naukę tematu: krótka teoria → ćwiczenie do wykonania → kryteria sukcesu.
- Proponuj wpisy do `nauka/dziennik.md` po każdej sesji.
- Nie rozwiązuj za mnie ćwiczeń, dopóki nie poproszę — najpierw podpowiedź.

### Praca z repo
- Commity po polsku, w trybie rozkazującym: `dodaj uchwyt na telefon w2`, `popraw tolerancje zatrzasku`.
- Nowy projekt = zawsze `README.md` z sekcjami: **Cel / Materiał / Ustawienia druku / Status / Wnioski**.
- Nie dodawaj do gita plików `.gcode` i `.3mf` z wynikami slicingu, jeśli są duże — dopisz do `.gitignore`.

---

## Czego nie robić
- Nie podawaj ustawień druku "z sufitu" jako pewników — oznaczaj, co wymaga testu na moim sprzęcie.
- Nie zakładaj, że mam komorę zamkniętą, drugą dyszę albo suszarkę do filamentu.
- Nie generuj gigantycznych plików STL w tekście — dawaj kod parametryczny albo instrukcję w CAD.
- Nie tłumacz podstaw od zera przy każdej odpowiedzi, chyba że temat jest dla mnie nowy.

---

## Jak zaczynamy sesję

Na start: sprawdź `nauka/dziennik.md` i `projekty/`, powiedz krótko gdzie skończyliśmy
i zaproponuj 2–3 sensowne kolejne kroki. Potem czekaj na mój wybór.
