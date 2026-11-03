# Ćwiczenia: Blender, karoseria i bodykit

Teoria i instrukcje krok po kroku: [`../notatki/blender-bodykit.md`](../notatki/blender-bodykit.md).
Najpierw próbuj sam. Podpowiedzi są zwinięte, otwieraj je dopiero, gdy utkniesz.

---

## Ćwiczenie 1 — „resorak” z klocków (lekcja 1)

**Zadanie:** z prymitywów zbuduj zabawkowe auto: korpus z kostki, kabina
z drugiej kostki, 4 koła z walców. Wszystko w prawdziwej skali.

Wymagania:
- korpus: 4,2 × 1,8 × 0,8 m (długość wzdłuż **Y**), stoi nad ziemią
  na wysokości promienia kół,
- koła: walce o średnicy 0,65 m i szerokości 0,22 m, osie kół równoległe do **X**,
- rozstaw osi 2,6 m, koła symetrycznie po obu stronach.

**Kryteria sukcesu:**
- [ ] Żadna pozycja ani obrót nie są ustawione „na oko”: wszystko wpisane
      liczbą (GRS + liczba albo pola w panelu `N`).
- [ ] Koła mają `Rotation Y = 90°` (albo równoważnie) i ich `X` wynosi
      dokładnie ±(ta sama wartość).
- [ ] W widoku z boku (`Numpad 3`) przód auta jest po lewej.
- [ ] Przełączasz `1 / 3 / 7 / 5` i obracasz widok bez patrzenia w ściągę.
- [ ] Plik zapisany jako `nauka/cwiczenia/blender-01-resorak.blend`.

<details><summary>Podpowiedź 1: jak zrobić walec o konkretnym wymiarze</summary>

Po `Shift + A > Mesh > Cylinder` rozwiń panel Adjust Last Operation
(lewy dolny róg): są tam `Radius` i `Depth`. Albo wpisz wymiary w `Dimensions`
w panelu `N`.
</details>

<details><summary>Podpowiedź 2: jak szybko zrobić 4 koła</summary>

Zrób jedno, ustaw je dokładnie, potem `Shift + D` i od razu `X` (oś)
i liczbę, o ile przesunąć. Kopia porusza się tylko w osi X o zadaną wartość.
</details>

---

## Ćwiczenie 2 — blueprinty Twojego auta (lekcja 2)

**Zadanie:** dla wybranego auta ustaw w scenie miarkę i 4 rzuty
(bok, przód, tył, góra).

**Kryteria sukcesu:**
- [ ] Miarka ma wymiary katalogowe auta (wpisane w `Dimensions`) i stoi na Z = 0.
- [ ] Na boku i na górze zderzaki dotykają ścian miarki, a na przodzie i tyle
      boki karoserii (bez lusterek) dotykają jej ścian.
- [ ] Wysokość dachu bok vs przód: różnica ≤ 2 cm.
- [ ] Środki kół bok vs góra: różnica ≤ 2 cm, a rozstaw osi zgodny z katalogiem.
- [ ] Obracając widok w perspektywie, **nie widzisz** żadnego blueprintu
      (`Only Axis Aligned`).
- [ ] Kolekcji `Blueprinty` nie da się zaznaczyć kliknięciem.
- [ ] Po zamknięciu i ponownym otwarciu pliku obrazki są na miejscu
      (ścieżki względne działają).
- [ ] Zapisane w `projekty/<auto>/cad/`.

<details><summary>Podpowiedź: blueprint nie pasuje jednocześnie na boku i na górze</summary>

Najpierw sprawdź, czy przycięcie obrazków było ciasne (czy na krawędziach
nie ma marginesu). Jeśli tak, rysunki faktycznie się różnią. Ustaw je według
rozstawu osi, bo to wymiar, który najbardziej rzuca się w oczy na gotowym modelu.
Różnicę zapisz w README projektu.
</details>

---

## Ćwiczenie 3 — karoseria, wersja uproszczona (lekcja 3)

**Zadanie:** wymodeluj połowę nadwozia z Mirror + Subdivision Surface,
z otwartymi nadkolami. Bez detali (klamki, wycieraczki, szczeliny).

**Kryteria sukcesu:**
- [ ] Obiekt `karoseria` ma `Location`, `Rotation` = 0 i `Scale` = 1
      w panelu `N` (całe modelowanie w Edit Mode).
- [ ] Na środku maski, dachu i zderzaków **nie ma szpary**: Clipping działa.
- [ ] `Select All by Trait > Faces by Sides` (≠ 4) nie zaznacza nic albo tylko
      pojedyncze świadomie zostawione miejsca.
- [ ] Siatka bazowa (bez Subdivision): **poniżej ~600 ścian** na połowę.
- [ ] Sylwetka zgodna z blueprintami we wszystkich widokach `1 / 3 / 7`
      (odchyłki rzędu 1–2 cm).
- [ ] Przy obracaniu w perspektywie, w trybie Solid ze Shade Smooth, nie widać
      garbów ani wgnieceń.
- [ ] Face Orientation: wszystko na zewnątrz bez czerwonego.

<details><summary>Podpowiedź 1: od czego zacząć, gdy nie wiem, gdzie wyciągać</summary>

Zacznij od nadkoli. To najbardziej charakterystyczny kształt i od nich
„rozchodzi się” reszta siatki. Kafelki wokół łuku ustaw promieniście,
jak szprychy. Dopiero potem łącz je progiem.
</details>

<details><summary>Podpowiedź 2: dużo trójkątów w okolicy słupków</summary>

Zwykle znaczy to, że w jednym miejscu spotyka się nieparzysta liczba pasów
kafelków. Sprawdź, czy liczba krawędzi wzdłuż dolnej i górnej linii okna jest
taka sama. Jeśli nie, dodaj/usuń pętlę (`Ctrl + R` / `X > Dissolve Edges`)
z jednej strony.
</details>

---

## Ćwiczenie 4 — bodykit (lekcja 4)

**Zadanie:** zaprojektuj własny zestaw: **splitter przedni + progi** oraz
**jedno** do wyboru: spoiler, dyfuzor albo poszerzenia nadkoli.

**Kryteria sukcesu:**
- [ ] Każda część to osobny, nazwany obiekt (`splitter_przod`, `prog`, …).
- [ ] Wewnętrzna strona części leży na karoserii: w X-ray w widokach
      `1 / 3` nie widać szczeliny między częścią a nadwoziem.
- [ ] `Solidify` z `Offset = 1` i grubością ≥ **1,2 mm × mianownik skali**
      (zapisz w README, jaką skalę wybrałeś i jaką grubość to daje).
- [ ] Mirror działa na każdej części (symetria lewo-prawo).
- [ ] Kolejność modyfikatorów: Mirror → Subdivision → Solidify.

<details><summary>Podpowiedź: Solidify robi grubość do środka auta</summary>

Albo `Offset` jest −1, albo normalne części są odwrócone. Włącz Face
Orientation. Jeśli kopia ścian jest czerwona na zewnątrz, popraw ją `Shift + N`
w Edit Mode.
</details>

---

## Ćwiczenie 5 — pierwszy wydruk (lekcja 5)

**Zadanie:** wyeksportuj i wydrukuj **jedną** część bodykitu (najmniejszą)
oraz **przednią ćwiartkę** karoserii jako test pasowania. Nie całe auto:
najpierw sprawdzasz, czy grubości i pasowanie mają sens, a potem drukujesz
5 godzin.

**Kryteria sukcesu:**
- [ ] 3D Print Toolbox: `Non Manifold Edge = 0`, `Intersect Face = 0`.
- [ ] Wymiar w Bambu Studio = wymiar rzeczywisty / mianownik skali (± 0,5 mm).
- [ ] Część przylega do karoserii bez szczeliny widocznej gołym okiem.
- [ ] Najcieńsze miejsce części wydrukowało się w całości (bez dziur w ściankach).
- [ ] Ustawienia i orientacja zapisane w `projekty/<auto>/README.md`
      (sekcja Ustawienia druku), a wnioski w sekcji Wnioski.
- [ ] Wpis w `nauka/dziennik.md`.

<details><summary>Podpowiedź: jak wyciąć „ćwiartkę” karoserii do testu</summary>

Na kopii w kolekcji `Do_druku` dodaj modyfikator `Boolean` z kostką
ustawioną na przód auta (`Operation: Intersect`) i zatwierdź go
(`Object > Convert > Mesh`). Zostanie tylko część, którą obejmuje kostka.
</details>
