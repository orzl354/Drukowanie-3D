// Test skoku osi pionowej: kolek na zacisku w rowku w spodzie tarczy widelca.
// Uruchomienie:  openscad -D kat_pan=91 -o /tmp/p.stl test-obrotu.scad
// UWAGA: tarcza LEZY na zacisku, wiec przeciecie zawsze zawiera plaszczyzne
// styku o zerowej grubosci. Kolizja = wynik o niezerowej rozpietosci w Z.
include <uchwyt.scad>
czesc = "nic";
$fa = 6; $fs = 1.0;
kat_pan = 0;
intersection() {
    translate([0, os_y, zac_h]) rotate([0, 0, kat_pan]) widelec();
    zacisk();
}
