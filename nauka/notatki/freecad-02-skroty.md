# FreeCAD — nawigacja i skróty, PC ↔ MacBook

> FreeCAD pokazuje aktualny skrót **obok pozycji w menu**. Jeśli coś tu nie zgadza się
> z Twoją wersją — wierz menu, nie tej tabelce, i popraw ją. Część skrótów Sketchera
> zmieniła się w okolicach 1.0.

---

## Zasada ogólna dla macOS

| Na PC | Na MacBooku |
|---|---|
| `Ctrl` + litera (zapis, cofnij, kopiuj) | **`Cmd`** + litera |
| `Ctrl` jako modyfikator zaznaczania w 3D | **`Cmd`** |
| pojedyncze litery (`H`, `V`, `C`, `E`…) | **tak samo**, bez modyfikatora |
| `Edit → Preferences` | **`FreeCAD → Settings…`** (`Cmd+,`) |
| `Alt` | **`Option ⌥`** |
| prawy przycisk myszy | **dwa palce na gładziku** lub `Ctrl`+klik |
| środkowy przycisk myszy | **nie istnieje** → patrz „Nawigacja" niżej |

Dodatkowo na Macu:
- **Cmd+Q zamyka FreeCAD natychmiast.** Leży obok Cmd+W i Cmd+S. Włączony autozapis to nie luksus.
- Jeśli masz **„naturalne" przewijanie** włączone w systemie, zoom kółkiem/gładzikiem będzie
  odwrotny niż na PC. Albo przyzwyczaj się, albo odwróć w FreeCAD:
  Settings → Display → Navigation → **Invert zoom**.

---

## Nawigacja w widoku 3D

| Czynność | PC (tryb **CAD**, mysz) | MacBook (tryb **Gesture**, gładzik) |
|---|---|---|
| Obrót | środkowy + lewy przycisk | przeciągnięcie **prawym** (dwa palce z `Ctrl`) |
| Przesunięcie (pan) | środkowy przycisk | przeciągnięcie **lewym po pustym tle** |
| Zoom | kółko | szczypanie / dwa palce w pionie |
| Dopasuj widok do modelu | `View → Fit All` (ikona lupy) | tak samo |
| Widok izometryczny | `0` | `0` |
| Widoki znormalizowane (przód/góra/bok…) | `1`–`6` | `1`–`6` |

**Kostka nawigacyjna** (prawy górny róg) działa identycznie na obu maszynach i jest
najszybszym sposobem na wyjście z zagubionego widoku. Klikasz ściankę — dostajesz ten rzut.

W trybie **Gesture** lewy przycisk na pustym tle **obraca widok, a nie zaznacza ramką**.
Jeśli na Macu „widok ucieka bez powodu" — to jest to.

---

## Sketcher — skróty, których używamy najczęściej

Wszystkie działają tak samo na PC i na Macu (to zwykłe litery).
Skróty dwuklawiszowe czyta się jako „naciśnij `G`, puść, naciśnij `L`".

### Geometria

| Narzędzie | Skrót |
|---|---|
| Linia | `G`, `L` |
| Łamana (polyline) | `G`, `M` |
| Prostokąt | `G`, `R` |
| Okrąg | `G`, `C` |
| Łuk | `G`, `A` |
| Przełącz na geometrię konstrukcyjną | `G`, `N` |
| Geometria zewnętrzna (rzut krawędzi z modelu) | `G`, `X` |

### Więzy

| Więz | Skrót | Po co |
|---|---|---|
| Pokrycie (coincident) | `C` | sklejenie dwóch punktów |
| Poziomo | `H` | |
| Pionowo | `V` | |
| Równolegle | `P` | |
| Prostopadle | `N` | |
| Styczne | `T` | |
| Równe | `E` | dwa wymiary jedną liczbą — mniej parametrów do pilnowania |
| Symetria | `S` | zaznacz 2 punkty **i** oś, dopiero potem `S` |
| Wymiar (uniwersalny) | `K`, `D` | |
| Wymiar poziomy / pionowy | `K`, `L` / `K`, `I` | |
| Promień / średnica | `K`, `R` / `K`, `O` | |

### Poza szkicem

| Czynność | PC | Mac |
|---|---|---|
| Zapisz | `Ctrl+S` | `Cmd+S` |
| Cofnij / ponów | `Ctrl+Z` / `Ctrl+Shift+Z` | `Cmd+Z` / `Cmd+Shift+Z` |
| Przelicz model na siłę | zaznacz dokument → prawy → **Mark to recompute**, potem `Refresh` | tak samo |
| Usuń operację z drzewa | `Del` | `Fn+Delete` albo `Del` |

---

## Miejsce na moje poprawki

Jeśli któryś skrót u mnie jest inny, wpisuję tutaj (i na której maszynie):

| Czynność | Co jest naprawdę | Maszyna |
|---|---|---|
| | | |
