# Dlaczego tu nie ma plików

Model źródłowy („Penguin keycap", Melodybox, MakerWorld) jest na licencji
*Standard Digital File License*, która nie pozwala udostępniać plików ani ich
pochodnych. To repo jest publiczne, więc STL-e i 3MF z podziałem **zostają
lokalnie** — katalogi `stl/` i `slicer/` są w `.gitignore`.

Pliki do druku generujesz u siebie ze swojego 3MF:

```bash
python3 ../cad/podziel_na_kolory.py <twoj-plik.3mf> .
```
