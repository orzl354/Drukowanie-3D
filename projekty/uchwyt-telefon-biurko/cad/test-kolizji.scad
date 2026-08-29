// Test przenikania kolyski z reszta uchwytu i blatem.
// Uruchomienie:  openscad -D kat_tilt=-40 -D kat_pan=45 -o /tmp/k.stl test-kolizji.scad
// Jesli openscad NIE zapisze pliku ("Current top level object is empty")
// -> brak kolizji. Jesli zapisze -> czesci sie przenikaja.
include <uchwyt.scad>
czesc = "nic";          // wylacza geometrie najwyzszego poziomu z uchwyt.scad
$fa = 8; $fs = 1.5;     // zgrubnie - test nie potrzebuje gladkich walcow
kat_pan = 0; kat_tilt = 0; blat_gr = 25;

module kolyska_w_pozycji() {
    translate([0, os_y, zac_h]) rotate([0, 0, kat_pan])
        translate([0, 0, tarcza_h + os_h]) rotate([kat_tilt, 0, 0]) rotate([0, 0, 180])
            translate([0, zaczep_y, -zaczep_z]) kolyska();
}
intersection() {
    kolyska_w_pozycji();
    union() {
        zacisk();
        translate([-70, -6, dol_gr]) cube([140, 90, blat_gr]);
        translate([0, os_y, zac_h]) rotate([0, 0, kat_pan]) widelec();
    }
}
