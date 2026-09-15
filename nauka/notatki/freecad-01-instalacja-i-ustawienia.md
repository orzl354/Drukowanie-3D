# FreeCAD — instalacja i ustawienia startowe (PC + MacBook)

> Cel: po przejściu tej notatki FreeCAD na obu maszynach zachowuje się **identycznie**,
> a pliki `.FCStd` otwierają się w obie strony bez niespodzianek.

---

## 1. Wersja — to jest ważniejsze, niż wygląda

Używaj **tej samej wersji na PC i na MacBooku**. FreeCAD zapisuje do pliku strukturę
modelu zależną od wersji: plik zapisany w nowszej wersji potrafi się w starszej nie otworzyć
albo otworzyć z błędami przeliczenia. Przy pracy na dwóch maszynach to jest najczęstsze
źródło „u mnie działało".

Minimum: **FreeCAD 1.0**. To wydanie naprawiło *toponaming* — historyczny problem, przez który
zmiana wymiaru potrafiła rozsypać cały model, bo FreeCAD gubił, do której ścianki był
przypięty fillet. Poradniki nagrane na 0.19/0.20 (a takich jest w sieci większość) pokazują
obejścia tego problemu, które od 1.0 są już niepotrzebne — nie dziw się różnicom w menu.

Sprawdź swoją wersję: **Help → About FreeCAD** (macOS: **FreeCAD → About FreeCAD**).
Zapisz obie w tabelce na dole tej notatki.

## 2. Instalacja

**Linux / PC**

Preferuj AppImage albo pakiet z freecad.org — wersje z repozytoriów dystrybucji potrafią być
o dwa wydania w tyle, a to nas wywraca na punkcie 1.

**macOS (MacBook)**

1. `.dmg` z [freecad.org](https://www.freecad.org/downloads.php) — **wybierz build pod swój procesor**:
   `arm64` dla Apple Silicon (M1/M2/M3/M4), `x86_64` dla starszych Intelowych.
   Na Apple Silicon build Intelowy odpali się przez Rosettę, ale będzie zauważalnie wolniejszy
   przy przeliczaniu modelu.
2. Alternatywnie Homebrew: `brew install --cask freecad`.
3. Przy pierwszym uruchomieniu macOS może zablokować aplikację jako „od niezidentyfikowanego
   dewelopera". Nie klikaj w kółko „OK" — **kliknij prawym (Ctrl+klik) na FreeCAD.app → Open**,
   i dopiero w tym oknie potwierdź. To jednorazowe.

## 3. Ustawienia do zmiany od razu (na obu maszynach tak samo)

**Edit → Preferences** (macOS: **FreeCAD → Settings…**, `Cmd+,`)

| Gdzie | Ustaw | Dlaczego |
|---|---|---|
| General → Units → Unit system | **Standard (mm, kg, s, degree)** | całe repo jest w mm; inny system = liczby w arkuszu znaczą co innego |
| General → Units → Number of decimals | **3** | tolerancje 0.05 mm muszą być widoczne, przy domyślnych 2 miejscach 1.175 pokaże się jako 1.18 |
| General → Document → Auto save | **włączone, co 5 min** | FreeCAD potrafi wysypać się przy skomplikowanym filletcie |
| General → Document → Storage → „Save thumbnail into project file" | włączone | miniatura w GitHubie/Finderze |
| Display → Navigation → 3D Navigation | PC: **CAD**, MacBook: **Gesture** | patrz niżej |
| Part Design → General → „Auto remove redundant constraints" | wg uznania | na start zostaw domyślnie i ucz się czytać komunikaty o nadmiarowych więzach |

### Nawigacja — tu PC i Mac naprawdę się różnią

Domyślny tryb **CAD** wymaga **środkowego przycisku myszy** (obrót = MMB + lewy).
Na gładziku MacBooka nie ma czego nacisnąć. Dlatego:

- **MacBook, gładzik:** Preferences → Display → Navigation → 3D Navigation = **Gesture**.
  Wtedy: obrót = przeciągnięcie **prawym** (dwa palce z Ctrl), przesuwanie = przeciągnięcie
  **lewym po pustym tle**, zoom = szczypanie / dwa palce w pionie.
  Uwaga: w trybie Gesture **lewy przycisk na pustym tle obraca widok, a nie zaznacza ramką** —
  to najczęstsze „dlaczego mi ucieka widok" na Macu.
- **MacBook, mysz z rolką:** możesz zostawić **CAD** i mieć identycznie jak na PC.
  To jest wygodniejsze, jeśli często przeskakujesz między maszynami — jeden zestaw odruchów.
- Niezależnie od trybu: w prawym górnym rogu jest **kostka nawigacyjna** (Navigation Cube).
  Klikanie w jej ścianki i narożniki działa tak samo wszędzie i ratuje, gdy widok się zgubi.
  Skrót do widoku izometrycznego: **`0`–`6`** to widoki znormalizowane, **`0`** = izometria.

## 4. Warsztaty (workbenches), których będziemy używać

FreeCAD dzieli narzędzia na „warsztaty" — to lista rozwijana na górnym pasku.
Przełączanie warsztatu **nie** zmienia modelu, zmienia tylko dostępne przyciski.

| Warsztat | Do czego |
|---|---|
| **Part Design** | 99% naszej pracy: bryły budowane z operacji na szkicach |
| **Sketcher** | szkice (wchodzi się w niego automatycznie z Part Design) |
| **Spreadsheet** | arkusz parametrów — nasze „zmienne na górze pliku" |
| **Mesh / Import-Export** | eksport do STL na druk |

Nie mieszaj **Part** z **Part Design**. `Part` to operacje logiczne na gotowych bryłach
(jak OpenSCAD: `union`, `difference`). `Part Design` to modelowanie oparte na historii operacji
i szkicach — i to jest ta droga, którą chcemy, bo pozwala wrócić i zmienić wymiar.

## 5. Praca na dwóch maszynach + git

Plik `.FCStd` to **zzipowane archiwum XML** — dla gita to plik binarny.
Konsekwencja jest jedna i twarda:

> **Gita nie da się użyć do scalenia dwóch wersji tego samego `.FCStd`.**
> Jeśli zmodyfikujesz model na PC i na MacBooku bez `pull` pomiędzy, jedna wersja przepada.

Dlatego rytuał na start i koniec każdej sesji, niezależnie od maszyny:

```bash
# START sesji
git pull origin <galaz>

# KONIEC sesji
git add -A
git commit -m "opis po polsku w trybie rozkazującym"
git push -u origin <galaz>
```

Repo ma `.gitattributes`, który oznacza `*.FCStd` i `*.stl` jako binarne — dzięki temu
`git diff` nie wypluwa ściany śmieci, a `git status` nie próbuje konwertować końców linii.

Pliki `*.FCStd1` (automatyczna kopia poprzedniego zapisu) i `*.FCBak` są już w `.gitignore` —
nie commituj ich, to tylko kopie zapasowe FreeCAD-a.

### Homebrew na MacBooku — reszta narzędzi

```bash
brew install --cask freecad openscad bambu-studio
brew install git
```

---

## Moje wersje (uzupełnić)

| Maszyna | System | FreeCAD | Tryb nawigacji |
|---|---|---|---|
| PC | | | CAD |
| MacBook | | | |
