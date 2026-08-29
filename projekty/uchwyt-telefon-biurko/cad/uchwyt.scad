// ============================================================================
//  UCHWYT NA TELEFON NA BIURKO
//  Zacisk na krawedz blatu + obrot w dwoch osiach (pionowa 180 st. + pochylenie)
//
//  Telefon docelowy: Samsung Galaxy S22  (146.0 x 70.6 x 7.6 mm)
//  Material: PETG            Jednostki: mm
//
//  Eksport pojedynczej czesci:
//    openscad -D 'czesc="kolyska"' -o ../stl/kolyska.stl uchwyt.scad
// ============================================================================

// "plyta"  - wszystkie czesci obok siebie w orientacji druku (podglad)
// "zacisk" | "widelec" | "kolyska" | "stopka" | "pokretlo"
czesc = "plyta";

$fa = 2;
$fs = 0.4;

// ---------------------------------------------------------------------------
//  TELEFON - jedyne liczby, ktore trzeba zmienic przy innym modelu
// ---------------------------------------------------------------------------
tel_grub  = 7.6;    // grubosc S22
etui_grub = 3.5;    // naddatek na etui; bez etui wpisz 0

// ---------------------------------------------------------------------------
//  TOLERANCJE  (wartosci startowe z CLAUDE.md - DO WERYFIKACJI DRUKIEM)
// ---------------------------------------------------------------------------
luz_ruchomy = 0.35;

// ---------------------------------------------------------------------------
//  SRODKI ZLACZNE  (srednice otworow = nominal + luz)
// ---------------------------------------------------------------------------
m6_otw    = 6.6;    // otwor przelotowy M6
m6_nakr_d = 11.8;   // nakretka M6: rozstaw naroznikow 11.55 + luz
m6_nakr_h = 5.6;    // wysokosc nakretki M6
m6_leb_d  = 10.8;   // leb imbusowy M6
m4_otw    = 4.5;    // otwor przelotowy M4
m4_nakr_d = 8.4;    // nakretka M4: rozstaw naroznikow 8.08 + luz
m4_nakr_h = 5.4;    // nakretka samohamowna (nylock) M4 jest wyzsza od zwyklej

// ---------------------------------------------------------------------------
//  BLAT BIURKA
// ---------------------------------------------------------------------------
blat_max = 36;      // maks. grubosc blatu miedzy ramionami zacisku

// ---------------------------------------------------------------------------
//  KOLYSKA
// ---------------------------------------------------------------------------
kanal      = tel_grub + etui_grub + luz_ruchomy;  // szczelina na telefon
kol_szer   = 92;    // szerokosc (telefon poziomo ma 146 mm - wystaje po 27 mm)
plyta_gr   = 3.6;   // grubosc plyty oparcia
plyta_h    = 56;    // wysokosc plyty oparcia
polka_gr   = 5.0;   // grubosc polki (dna)
warga_gr   = 3.2;   // grubosc wargi przedniej
warga_h    = 12;    // wysokosc wargi ponad polke
kabel_szer = 30;    // wyciecie na kabel
polka_gl   = plyta_gr + kanal + warga_gr;

zaczep_szer = 16;   // szerokosc zaczepu osi pochylenia
zaczep_r    = 9;    // promien konca zaczepu
zaczep_y    = 15;   // jak daleko za plyte odsunieta jest os
zaczep_z    = 30;   // wysokosc osi pochylenia nad spodem polki

// ---------------------------------------------------------------------------
//  WIDELEC (tarcza obrotu pionowego + widly osi pochylenia)
// ---------------------------------------------------------------------------
tarcza_d  = 46;
tarcza_h  = 7;
ramie_gr  = 6;      // grubosc ramienia widelca
ramie_y   = 22;     // glebokosc ramienia
os_h      = 34;     // wysokosc osi pochylenia nad tarcza
stop_r    = 15;     // promien okregu, po ktorym chodzi ogranicznik
stop_d    = 6;      // srednica kolka ogranicznika (na zacisku)
stop_h    = 3;      // wysokosc kolka / glebokosc rowka
// kat, jaki kolek zajmuje na tym promieniu - rowek musi byc o tyle dluzszy,
// zeby SKOK wynosil dokladnie 180 st.
stop_kat_kolka = 2 * asin((stop_d/2) / stop_r);
stop_kat_rowka = 180 + stop_kat_kolka;

// ---------------------------------------------------------------------------
//  ZACISK
// ---------------------------------------------------------------------------
zac_szer = 44;      // szerokosc zacisku
krg_gr   = 18;      // grubosc grzbietu litery C (z rachunku naprezen, patrz README)
dol_gr   = 12;      // dolne ramie (musi pomiescic nakretke M6)
gora_gr  = 9;       // gorne ramie
ramie_dl = 48;      // zasieg ramion nad blatem
os_y     = 26;      // polozenie osi pionowej i sruby dociskowej wzdluz ramienia
faza     = 5;       // faza wzmacniajaca gardziel litery C

zac_h = dol_gr + blat_max + gora_gr;

// ---------------------------------------------------------------------------
//  POMOCNICZE
// ---------------------------------------------------------------------------

// prostopadloscian o zaokraglonych krawedziach pionowych, wysrodkowany w XY
module zpp(x, y, z, r) {
    hull() for (sx = [-1, 1], sy = [-1, 1])
        translate([sx * (x/2 - r), sy * (y/2 - r), 0])
            cylinder(h = z, r = r);
}

// wycinek pierscienia - ogranicznik obrotu
module luk(r_wew, r_zew, wys, kat) {
    rotate_extrude(angle = kat)
        translate([r_wew, 0]) square([r_zew - r_wew, wys]);
}

// ============================================================================
//  KOLYSKA
//  Uklad "jak w uzyciu": Y w glab, Z w gore, plyta oparcia z tylu (y = 0..gr).
//  Drukuje sie DOKLADNIE w tej orientacji - polka lezy na stole, zero podpor.
// ============================================================================
module kolyska() {
    difference() {
        union() {
            // --- polka + warga: profil 2D (z, y) wyciagniety wzdluz X
            translate([kol_szer/2, 0, 0]) rotate([0, -90, 0])
                linear_extrude(kol_szer)
                    offset(r = 1.2) offset(r = -1.2)
                        union() {
                            square([polka_gr, polka_gl]);
                            translate([0, plyta_gr + kanal])
                                square([polka_gr + warga_h, warga_gr]);
                        }

            // --- plyta oparcia, zaokraglone narozniki
            translate([0, plyta_gr, 0]) rotate([90, 0, 0])
                linear_extrude(plyta_gr)
                    offset(r = 6) offset(r = -6)
                        translate([-kol_szer/2, 0]) square([kol_szer, plyta_h]);

            // --- zaczep osi pochylenia; hull tworzy skarpe ~50 st. od poziomu,
            //     czyli 40 st. zwisu - drukuje sie bez podpor
            hull() {
                translate([-zaczep_szer/2, -zaczep_y, zaczep_z])
                    rotate([0, 90, 0]) cylinder(h = zaczep_szer, r = zaczep_r);
                translate([0, -0.6, zaczep_z - 2]) zpp(zaczep_szer, 1.2, 2, 0.5);
                // szerokosc skarpy = szerokosc zaczepu: musi zmiescic sie
                // miedzy ramionami widelca przez caly zakres obrotu
                translate([0, -0.6, 0.5])          zpp(zaczep_szer, 1.2, 2, 0.5);
            }
        }

        // --- otwor osi pochylenia (przelot)
        translate([-kol_szer, -zaczep_y, zaczep_z]) rotate([0, 90, 0])
            cylinder(h = 2 * kol_szer, d = m4_otw);

        // --- gniazdo nakretki nylock M4 W SRODKU zaczepu (otwarte na lewe ramie)
        translate([-zaczep_szer/2 - 0.01, -zaczep_y, zaczep_z]) rotate([0, 90, 0])
            cylinder(h = m4_nakr_h, d = m4_nakr_d, $fn = 6);

        // --- wyciecie na kabel: tylko przez polke i wargę.
        //     NIE tnie plyty oparcia - to tamtedy idzie obciazenie z telefonu
        //     do zaczepu, przerwanie tego pasa oslabiloby czesc w newralgicznym miejscu.
        translate([0, plyta_gr + (polka_gl - plyta_gr + 1)/2, -1])
            zpp(kabel_szer, polka_gl - plyta_gr + 1, polka_gr + warga_h + 2, 5);

        // --- podciecie ulgowe w narozniku polka/plyta: telefon ma przylegac
        //     do OBU plaszczyzn, a nie opierac sie na promieniu po dyszy
        translate([-kol_szer, plyta_gr, polka_gr]) rotate([0, 90, 0])
            cylinder(h = 3 * kol_szer, r = 1.4);
    }
}

// ============================================================================
//  WIDELEC - tarcza obrotu pionowego + widly osi pochylenia
//  Drukuje sie tarcza do stolu, zero podpor.
// ============================================================================
module widelec() {
    rozstaw = zaczep_szer + 2 * luz_ruchomy;   // swiatlo miedzy ramionami
    x_ram   = rozstaw/2 + ramie_gr/2;

    difference() {
        union() {
            cylinder(h = tarcza_h, d = tarcza_d);

            // Ramiona rozszerzone u podstawy - skarpa zamiast ostrego karbu.
            // Rozszerzenie idzie TYLKO NA ZEWNATRZ: wewnetrzna sciana ramienia
            // musi zostac plaska na calej wysokosci, bo w szczelinie miedzy
            // ramionami obraca sie zaczep kolyski razem ze swoja skarpa.
            for (s = [-1, 1]) hull() {
                translate([s * x_ram, 0, os_h + tarcza_h])
                    rotate([0, 90, 0])
                        cylinder(h = ramie_gr, d = 2 * zaczep_r, center = true);
                translate([s * x_ram, 0, tarcza_h - 0.01])
                    zpp(ramie_gr, ramie_y, 0.01, 1.5);
                translate([s * (x_ram + 3.5), 0, tarcza_h - 0.01])
                    zpp(ramie_gr + 7, ramie_y + 4, 0.01, 3);
            }

        }

        // rowek ogranicznika w SPODZIE tarczy. Celowo tutaj, a nie jako zabek
        // pod tarcza: zabek wystawalby ponizej plaszczyzny druku i tarcza
        // drukowalaby sie w powietrzu. Rowek to zwykla wneka w pierwszych
        // warstwach, zamostkowana po 3 mm.
        translate([0, 0, -0.01]) rotate([0, 0, -stop_kat_rowka/2])
            luk(stop_r - stop_d/2 - luz_ruchomy,
                stop_r + stop_d/2 + luz_ruchomy, stop_h + 0.01, stop_kat_rowka);

        // os pionowa: przelot + gniazdo lba imbusowego dostepne miedzy ramionami
        translate([0, 0, -1]) cylinder(h = tarcza_h + 2, d = m6_otw);
        translate([0, 0, tarcza_h - 4.5]) cylinder(h = 20, d = m6_leb_d);

        // os pochylenia
        translate([-tarcza_d, 0, os_h + tarcza_h]) rotate([0, 90, 0])
            cylinder(h = 2 * tarcza_d, d = m4_otw);
    }
}

// ============================================================================
//  ZACISK na krawedz blatu
//  Modelowany "jak w uzyciu", drukowany polozony na boku (patrz plyta()).
// ============================================================================
module zacisk() {
    difference() {
        union() {
            translate([0, -krg_gr/2, 0]) zpp(zac_szer, krg_gr, zac_h, 6);          // grzbiet
            // ramiona zachodza 1 mm na grzbiet - bryly do union() musza sie
            // PRZENIKAC; sam styk plaszczyzn zostawia rozlaczne bryly
            translate([0, (ramie_dl - 1)/2, 0])
                zpp(zac_szer, ramie_dl + 1, dol_gr, 6);                             // dolne ramie
            translate([0, (ramie_dl - 1)/2, zac_h - gora_gr])
                zpp(zac_szer, ramie_dl + 1, gora_gr, 6);                            // gorne ramie

            // fazy w gardzieli - tam jest maksimum naprezen zginajacych.
            // Celowo male (5 mm), zeby nie blokowac wsuniecia blatu.
            // kolek ogranicznika obrotu (wchodzi w rowek w spodzie tarczy)
            translate([stop_r, os_y, zac_h - 0.01]) cylinder(h = stop_h + 0.01, d = stop_d);

            for (i = [0, 1]) hull() {
                kier = (i == 0) ? 1 : -1;
                z0   = (i == 0) ? dol_gr - 0.5 : zac_h - gora_gr + 0.5;
                translate([0, 0,    z0])               zpp(zac_szer, 1, 0.01, 0.4);
                translate([0, 0,    z0 + kier * faza]) zpp(zac_szer, 1, 0.01, 0.4);
                translate([0, faza, z0])               zpp(zac_szer, 1, 0.01, 0.4);
            }
        }

        // --- os pionowa: przelot + gniazdo nakretki M6 od spodu gornego ramienia
        translate([0, os_y, zac_h - gora_gr - 1]) cylinder(h = gora_gr + 3, d = m6_otw);
        translate([0, os_y, zac_h - gora_gr - 0.01])
            cylinder(h = m6_nakr_h, d = m6_nakr_d, $fn = 6);

        // --- sruba dociskowa: przelot + gniazdo nakretki M6 od spodu
        translate([0, os_y, -1]) cylinder(h = dol_gr + 2, d = m6_otw);
        translate([0, os_y, -0.01]) cylinder(h = m6_nakr_h, d = m6_nakr_d, $fn = 6);
    }
}

// ============================================================================
//  STOPKA dociskowa - rozklada nacisk sruby na spod blatu
// ============================================================================
module stopka() {
    difference() {
        union() {
            cylinder(h = 5, d = 24);
            translate([0, 0, 5]) cylinder(h = 1.5, d1 = 24, d2 = 21);
        }
        translate([0, 0, -0.01]) cylinder(h = 3.5, d = m6_otw + 0.6);
        translate([0, 0, 3.4])   cylinder(h = 2, d1 = m6_otw + 0.6, d2 = 0);
    }
}

// ============================================================================
//  POKRETLO na leb sruby M6
// ============================================================================
module pokretlo() {
    difference() {
        union() {
            cylinder(h = 11, d = 34);
            for (a = [0 : 60 : 359])
                rotate([0, 0, a]) translate([19, 0, 0]) cylinder(h = 11, d = 11);
        }
        translate([0, 0, -0.01]) cylinder(h = 6, d = m6_nakr_d, $fn = 6);
        translate([0, 0, -0.01]) cylinder(h = 20, d = m6_otw);
    }
}

// ============================================================================
//  UKLAD NA STOLE - kazda czesc w swojej orientacji druku
// ============================================================================
module zacisk_do_druku() {
    // plaszczyzna litery C rownolegle do warstw = zginanie gardzieli
    // dziala W PLASZCZYZNIE warstw, a nie rozrywa ich w osi Z
    rotate([0, -90, 0]) translate([zac_szer/2, 0, 0]) zacisk();
}

module plyta() {
    translate([-60,  70, 0]) kolyska();           // 92 x 42
    translate([ 60,  85, 0]) widelec();           // 46 x 46
    translate([ 55, -10, 0]) zacisk_do_druku();   // 57 x 66
    translate([-70, -60, 0]) pokretlo();          // 49 x 44
    translate([-10, -70, 0]) stopka();            // 24 x 24
}


// ============================================================================
//  ZLOZENIE - tylko do sprawdzania pasowania i kolizji, NIE do druku
// ============================================================================
kat_pan  = 0;    // obrot pionowy   [-90 .. +90]
kat_tilt = 0;    // pochylenie      [ujemne = telefon klania sie do przodu]
blat_gr  = 25;   // grubosc blatu do podgladu

module zlozenie() {
    zacisk();

    // blat biurka (poglad)
    %translate([-70, -6, dol_gr]) cube([140, 90, blat_gr]);

    translate([0, os_y, zac_h]) rotate([0, 0, kat_pan]) {
        widelec();
        translate([0, 0, tarcza_h + os_h]) rotate([kat_tilt, 0, 0]) rotate([0, 0, 180])
            translate([0, zaczep_y, -zaczep_z]) {
                kolyska();
                // telefon (poglad): S22 pionowo
                %translate([-35.3, plyta_gr + luz_ruchomy/2, polka_gr])
                    cube([70.6, tel_grub + etui_grub, 146]);
            }
    }
    translate([0, os_y, -14]) stopka();
}

// ---------------------------------------------------------------------------
if      (czesc == "kolyska")  kolyska();
else if (czesc == "widelec")  widelec();
else if (czesc == "zacisk")   zacisk_do_druku();
else if (czesc == "stopka")   stopka();
else if (czesc == "pokretlo") pokretlo();
else if (czesc == "zlozenie") zlozenie();
else if (czesc == "plyta")    plyta();
// czesc = "nic"  -> nic nie rysuj (uzywane przez test kolizji)
