# Żółw — figurka do malowania

Postać z kreskówki, modelowana proceduralnie w Blenderze (skrypt, nie rzeźbienie
ręczne). Jeden kolor, dwie części łączone na kołki, druk bez podpór.

![render 3/4](zdjecia/render-34.png)

Model: [`cad/zolw.py`](cad/zolw.py)

## Cel

Figurka na półkę, malowana ręcznie po wydruku. Dlatego **jeden kolor** — żadnego
multicolor z AMS Lite, bo wieża czyszcząca przy takim detalu kosztowałaby więcej
filamentu niż sama figurka, a i tak wszystko idzie pod farbę.

## Proporcje — skąd się wzięły

Pierwsza wersja była robiona z opisu gatunku („żółw miękkoskorupowy = płaski")
i wyszła naleśnikiem. **Proporcje są teraz zdjęte z klatek serialu**, i to
zmieniło cztery rzeczy:

| cecha | z opisu gatunku | z klatek |
|---|---|---|
| wysokość pancerza | 0.26 długości (płaski) | **0.52 — bąbel** |
| ryjek | zwężający się stożek | **płaski dysk z dwiema dziurkami** |
| nogi | długie słupki | **krótkie, przysadziste, z dużymi pazurami** |
| rant pancerza | gładki | **kolce dookoła** |

Oczy są samymi wypukłymi gałkami. Ciężkie powieki, które postać ma na rysunku,
to kreska — łatwiej je domalować niż wydrukować, a próba zrobienia ich
geometrią dawała efekt guzika z kapeluszem.

## Skalowanie

W skrypcie jest **jedna liczba do zmiany**:

```python
PANCERZ_DL = 70.0        # dlugosc pancerza [mm]
```

Wszystkie pozostałe wymiary to ułamki tej liczby, więc zmiana przeskalowuje
całość z zachowaniem proporcji. Przy 70 mm figurka ma **112 × 75 × 52 mm**
po złożeniu. Chcesz mniejszą — wpisz 50 i uruchom skrypt ponownie.

Uwaga przy zmniejszaniu: pazury mają `0.080 × PANCERZ_DL`, więc przy 50 mm
schodzą do ~4 mm, a przy 35 mm do ~2.8 mm. Poniżej tego warto najpierw
sprawdzić, co wychodzi, testem z [`kalibracja/test-rozdzielczosci/`](../../kalibracja/test-rozdzielczosci/).

## Materiał

**PLA** — figurka wystawowa, zero obciążeń, a PLA najlepiej trzyma drobny detal
i najłatwiej się maluje (PETG trzeba odtłuścić i gorzej trzyma podkład).

## Części i druk

| część | gabaryty [mm] | orientacja | podpory |
|---|---|---|---|
| `zolw-cialo` | 112 × 75 × 20 | jak stoi, brzuchem do góry stołu | **nie** |
| `zolw-pancerz` | 72 × 67 × 37 | kopułą do góry, płaską podstawą na stół | **nie** |

**Dlaczego bez podpór** — to był warunek projektowy, nie przypadek:

- Ciało stoi na czterech stopach **i ryjku**. Ryjek opiera się o płytę i jest
  drugim punktem podparcia, dzięki czemu szyja o wysięgu 28 mm nie wisi
  w powietrzu. Gdyby łeb był podniesiony (parametr `SZYJA_KONIEC_Z`), szyja
  schodziłaby pod ~20° od poziomu — daleko poza to, co drukarka zmostkuje.
- Pancerz to kopuła z płaską podstawą, czyli zero zwisów.

### Ustawienia

> Wartości startowe, nie zmierzone na moim egzemplarzu A1.

| | |
|---|---|
| Warstwa | 0.12 mm (detal głowy i pazurów) |
| Ścianki | 2 |
| Wypełnienie | 10–15 % |
| Chłodzenie | 100 % |
| Brim | niepotrzebny — obie części mają dużą stopę |
| Zużycie | bryła 117 cm³ → szacunkowo **45–60 g PLA** przy 15 % |

### Montaż

Pancerz wchodzi na **dwa kołki Ø4 mm** (gniazda Ø4.4, luz 0.4 na klej).
Kropla kleju i gotowe. Podział na dwie części jest też po to, żeby malować
deseń na skorupie osobno, bez obchodzenia nóg i głowy.

## Status

**Wygenerowane, nie wydrukowane.**

```
cialo     trojk=83381  nonmanifold=0  ROZLACZNYCH=1  bbox=111.7 x 75.1 x 19.6 mm  V=35.0 cm3
pancerz   trojk=42483  nonmanifold=0  ROZLACZNYCH=1  bbox=72.4 x 66.6 x 37.2 mm   V=82.2 cm3
```

`ROZLACZNYCH=1` to kontrola, która tu zarabia na siebie: **szczelność nie
oznacza spójności.** Wcześniejsza wersja miała `nonmanifold=0` i składała się
z pięciu osobnych brył — korpusu i czterech odłączonych nóg. Samo sprawdzenie
szczelności by tego nie wykryło.

## Wnioski

*(do uzupełnienia po wydruku)*

Rzeczy, które wiem, że są niedokończone:

- **Tułów pod pancerzem jest żebrowany** — widać dziewięć elipsoid, z których
  jest złożony. W złożeniu zakrywa go pancerz, więc to kosmetyka, ale gdyby
  ktoś zdjął skorupę, widać.
- **Pancerz jest gładki** — na rysunku ma delikatną kreskę wzdłuż i poprzeczne
  fałdy nad głową. Do domalowania albo do dorobienia w modelu.
- Kolce na rancie są drobne (ok. 5 mm przy `PANCERZ_DL = 70`); przy
  zmniejszaniu figurki zejdą poniżej sensownej granicy.

### Pułapka techniczna, warto zapamiętać

Boolean na siatce, która sama się przecina, jest nieokreślony. Po `join()`
pancerz był kilkunastoma przenikającymi się powłokami (kopuła + rant + kolce);
wiercenie w tym gniazd na kołki **skasowało całą kopułę** i zostawiło same
kolce. Kolejność musi być: `join → remesh → boolean`, nigdy odwrotnie.
