# Stojak na LEGO Speed Champions — wersja „lekka”

Model: *Display Stand for LEGOs Speed Champion cars* (autor **Sebb3l**, MakerWorld,
licencja *Standard Digital File License*). Licencja nie pozwala na rozpowszechnianie
pliku, więc **samego modelu nie trzymam w repo** — tu tylko moje ustawienia.

## Cel
Ten sam stojak przy jak najmniejszym zużyciu filamentu: w środku prawie pusty,
w środku tylko kilka linii podpierających górną powierzchnię.

## Materiał
PLA Matte. To model wystawowy, nic go nie obciąża i nie stoi w aucie.

## Ustawienia druku
Zmiany zrobione jako **ustawienia per obiekt** (prawy klik na obiekt → nadpisane
parametry), więc zostają po zmianie profilu drukarki z P1S na A1.

| | Podstawa (110×70×18) | Tylna ścianka (100×220×8) | Wkład 2×4 |
|---|---|---|---|
| Ścianki | 3 → **2** | 3 → **2** | bez zmian (3) |
| Wypełnienie | gyroid 15% → **lightning 10%** | gyroid 15% → **lightning 10%** | bez zmian |
| Warstwy górne | 5 → **4** | 5 → **4** | bez zmian |
| Warstwy dolne | 3 → **2** | 3 (bez zmian) | bez zmian |
| Orientacja / podpory | jak w oryginale | jak w oryginale | jak w oryginale |

**Dlaczego tak:**
- **Lightning** to wypełnienie, które podpiera *tylko* górną powierzchnię, nie całą
  objętość: w środku zostaje kilka „gałązek”. Nie daje sztywności, ale w modelu
  wystawowym sztywność biorą na siebie ścianki i skóry góra/dół (jak w płycie warstwowej).
- **2 ścianki** (≈0,9 mm) wystarczą, bo boki nie przenoszą siły. Zewnętrzne wymiary
  się nie zmieniają, więc pasowania między częściami zostają takie same.
- **4 warstwy górne** (nie mniej): przy rzadkim wypełnieniu górna skóra musi „zamknąć”
  dziury, inaczej robi się *pillowing* (górna powierzchnia faluje albo ma dziurki).
- **Wkładu nie ruszam**: ma ~4 cm³, a w nim jest ciasne pasowanie pod LEGO.
  Oszczędność byłaby żadna, a ryzyko złego pasowania duże.

Szacunek (z objętości siatki, **do sprawdzenia w Bambu Studio**): z ~130 g do ~75 g
(około −40%). Najwięcej materiału idzie teraz w górną i dolną skórę dużej tylnej
ścianki (220×100 mm). Dalsza oszczędność wymaga zmiany geometrii, a nie ustawień.

## Status
`szkic` — ustawienia przygotowane, nie wydrukowane.

## Wnioski
- Do sprawdzenia: czy 4 warstwy górne wystarczą przy lightning (jeśli są dziurki
  na górze → 5 warstw).
- Do sprawdzenia: czy tylna ścianka z 2 ściankami nie ugina się przy wciskaniu
  wkładu (jeśli tak → 3 ścianki tylko dla niej).
