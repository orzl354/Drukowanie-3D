// ---------------------------------------------------------------------------
// Drabinka tolerancji: gniazdo krzyzowe pod trzpien MX
//
// Po co: otwory drukowane pionowo na FDM wychodza MNIEJSZE niz w modelu.
// O ile - zalezy od drukarki, filamentu, temperatury i predkosci. Ta plytka
// odpowiada na to pytanie jedna liczba, ktora potem wpisujemy do arkusza
// FreeCAD jako `krzyz_luz`.
//
// Kazde gniazdo ma wymiary nominalu MX powiekszone o `dodatek`. Cyfra obok
// gniazda to dodatek w setnych milimetra (5 = +0,05 mm).
//
// Drukuj TYMI SAMYMI ustawieniami, ktorymi bedziesz drukowal keycapa
// (ta sama wysokosc warstwy, ten sam filament, ta sama predkosc) - inaczej
// wynik nie przenosi sie na czesc docelowa.
// ---------------------------------------------------------------------------

/* [Nominal MX] */
krzyz_ramie   = 4.10;   // dlugosc ramienia krzyza
krzyz_grubosc = 1.17;   // grubosc ramienia krzyza

/* [Badane dodatki] */
dodatki       = [0.00, 0.05, 0.10, 0.15, 0.20];

/* [Geometria plytki] */
gniazdo_gleb  = 4.20;   // glebokosc gniazda
rozstaw       = 13.0;   // odstep miedzy srodkami gniazd
plyta_gr      = 6.0;    // grubosc plytki
plyta_y       = 20.0;   // glebokosc plytki
margines      = 3.0;    // margines po bokach
r_naroza      = 2.5;    // zaokraglenie narozy (DfAM: mniej naprezen, lepsza 1. warstwa)

/* [Opisy] */
tekst_rozmiar = 4.0;
tekst_wys     = 0.6;

$fn = 48;

// --- wielkosci pochodne ---------------------------------------------------
n        = len(dodatki);
plyta_x  = n * rozstaw + 2 * margines;
y_gniazd = plyta_y - 6.5;
y_tekstu = 4.5;
nadmiar  = 1.0;         // zeby ciecie wyszlo ponad gorna plaszczyzne

// --- moduly ---------------------------------------------------------------

// Krzyz jako dwa PRZENIKAJACE sie prostopadloscian.
// (Wniosek z projektu uchwyt-telefon-biurko: w CGAL bryly musza sie przenikac,
//  a nie stykac. Tu przenikaja sie w srodku, wiec union() da jedna bryle.)
module krzyz(ramie, grubosc, h) {
    union() {
        cube([ramie, grubosc, h], center = true);
        cube([grubosc, ramie, h], center = true);
    }
}

module plyta() {
    hull()
        for (x = [r_naroza, plyta_x - r_naroza])
            for (y = [r_naroza, plyta_y - r_naroza])
                translate([x, y, 0])
                    cylinder(r = r_naroza, h = plyta_gr);
}

module opisy() {
    // Cyfry wtapiaja sie w plyte o `zatopienie`, zeby NIE stykaly sie z nia
    // plaszczyzna o zerowej grubosci - inaczej CGAL zostawi je jako osobne bryly.
    zatopienie = 0.05;
    for (i = [0 : n - 1])
        translate([margines + rozstaw * (i + 0.5), y_tekstu, plyta_gr - zatopienie])
            linear_extrude(height = tekst_wys + zatopienie)
                text(str(round(dodatki[i] * 100)),
                     size = tekst_rozmiar,
                     halign = "center",
                     valign = "center");
}

module drabinka() {
    difference() {
        union() {
            plyta();
            opisy();
        }
        for (i = [0 : n - 1])
            translate([margines + rozstaw * (i + 0.5),
                       y_gniazd,
                       plyta_gr - gniazdo_gleb + (gniazdo_gleb + nadmiar) / 2])
                krzyz(krzyz_ramie   + dodatki[i],
                      krzyz_grubosc + dodatki[i],
                      gniazdo_gleb  + nadmiar);
    }
}

drabinka();

// Kontrola przed eksportem: w konsoli OpenSCAD po F6 (Render) ma byc
//   "Top level object is a 3D object:  Simple:  yes  Vertices: ...  Volumes: 1"
// Volumes wieksze niz 1 = plytka rozpadla sie na kawalki, cos jest zle.
