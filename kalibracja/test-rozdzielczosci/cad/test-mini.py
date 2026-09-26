# -*- coding: utf-8 -*-
"""
TEST ROZDZIELCZOSCI MALYCH DETALI - Bambu Lab A1, dysza 0.4
Odpowiada na pytanie: jak cienki detal wychodzi jeszcze uzywalny?

  strefa A: 8 zeber pionowych  1.6 -> 0.3 mm  (statywy skrzydla, zebra dyfuzora)
  strefa B: 6 kolkow           1.6 -> 0.4 mm  (kolki montazowe)
  strefa C: 6 otworow          1.6 -> 0.4 mm  (gniazda pod te kolki)

Kazdy detal ma obok WYPUKLY opis z wlasnym wymiarem, zeby po wydruku
dalo sie odczytac, ktory jest ktory.

Uruchomienie:   OUT_DIR=. freecadcmd test-mini.py
"""
import os
import FreeCAD as App
import Part, Sketcher, Mesh, MeshPart, Draft

OUT = os.environ.get('OUT_DIR', os.getcwd())
V = App.Vector
C = Sketcher.Constraint
CZCIONKA = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'

# --- co testujemy ---------------------------------------------------------
ZEBRA = [1.6, 1.2, 1.0, 0.8, 0.6, 0.5, 0.4, 0.3]   # grubosci zeber
SREDN = [1.6, 1.2, 1.0, 0.8, 0.6, 0.4]             # srednice kolkow i otworow

# --- geometria plytki -----------------------------------------------------
BAZA_X, BAZA_Y, BAZA_Z = 62.0, 44.0, 1.6
ZEB_H, ZEB_L, ZEB_ROZ, ZEB_Y = 6.0, 8.0, 7.0, 9.0   # wys / dlug / rozstaw / y poczatku
KOL_H, KOL_ROZ = 4.0, 8.0
Y_KOLKI, Y_OTWORY = 1.0, -9.0
Y_OPIS_ZEB, Y_OPIS_KOL, Y_OPIS_OTW = 4.5, -4.0, -15.0
OPIS_WYS, OPIS_WYPUKLOSC = 3.0, 0.5

doc = App.newDocument("test_mini")

# --- arkusz parametrow ----------------------------------------------------
ark = doc.addObject('Spreadsheet::Sheet', 'Parametry')
ark.set('A1', 'parametr'); ark.set('B1', 'wartosc'); ark.set('C1', 'opis')
_w = [2]
def par(nazwa, wart, opis):
    ark.set('A%d' % _w[0], nazwa); ark.set('B%d' % _w[0], str(wart))
    ark.set('C%d' % _w[0], opis);  ark.setAlias('B%d' % _w[0], nazwa)
    _w[0] += 1
par('baza_x', BAZA_X, 'dlugosc plytki bazowej [mm]')
par('baza_y', BAZA_Y, 'szerokosc plytki bazowej [mm]')
par('baza_z', BAZA_Z, 'grubosc plytki bazowej [mm]')
par('zebro_h', ZEB_H, 'wysokosc zeber nad baza [mm]')
par('kolek_h', KOL_H, 'wysokosc kolkow nad baza [mm]')
for i, t in enumerate(ZEBRA, 1):
    par('zebro_%d' % i, t, 'grubosc zebra nr %d [mm]' % i)
for i, d in enumerate(SREDN, 1):
    par('kolek_%d' % i, d, 'srednica kolka nr %d [mm]' % i)
for i, d in enumerate(SREDN, 1):
    par('otwor_%d' % i, d, 'srednica otworu nr %d [mm]' % i)
doc.recompute()

body = doc.addObject('PartDesign::Body', 'Body')

# --- pomocnicze: w pelni zwiazany prostokat i okrag -----------------------
def prostokat(szkic, x0, y0, w, h, tag):
    n = szkic.GeometryCount
    p = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    for a, b in zip(p, p[1:] + p[:1]):
        szkic.addGeometry(Part.LineSegment(V(a[0], a[1], 0), V(b[0], b[1], 0)), False)
    szkic.addConstraint([
        C('Coincident', n, 2, n+1, 1), C('Coincident', n+1, 2, n+2, 1),
        C('Coincident', n+2, 2, n+3, 1), C('Coincident', n+3, 2, n, 1),
        C('Horizontal', n), C('Horizontal', n+2),
        C('Vertical', n+1), C('Vertical', n+3)])
    for typ, args, suf in (('DistanceX', (n, 1, n, 2, w), '_w'),
                           ('DistanceY', (n+1, 1, n+1, 2, h), '_h'),
                           ('DistanceX', (-1, 1, n, 1, x0), '_x'),
                           ('DistanceY', (-1, 1, n, 1, y0), '_y')):
        i = szkic.addConstraint(C(typ, *args)); szkic.renameConstraint(i, tag + suf)

def okrag(szkic, cx, cy, d, tag):
    n = szkic.GeometryCount
    szkic.addGeometry(Part.Circle(V(cx, cy, 0), V(0, 0, 1), d / 2.0), False)
    for typ, args, suf in (('Diameter', (n, d), '_d'),
                           ('DistanceX', (-1, 1, n, 3, cx), '_x'),
                           ('DistanceY', (-1, 1, n, 3, cy), '_y')):
        i = szkic.addConstraint(C(typ, *args)); szkic.renameConstraint(i, tag + suf)

def nowy_szkic(nazwa):
    s = body.newObject('Sketcher::SketchObject', nazwa)
    s.AttachmentSupport = [(doc.getObject('XY_Plane'), '')]
    s.MapMode = 'FlatFace'
    return s

def rozstaw(n, krok):
    return [(i - (n - 1) / 2.0) * krok for i in range(n)]

x_zeb = rozstaw(len(ZEBRA), ZEB_ROZ)
x_kol = rozstaw(len(SREDN), KOL_ROZ)

# --- szkic 1: baza + otwory ----------------------------------------------
s1 = nowy_szkic('Baza')
prostokat(s1, -BAZA_X/2, -BAZA_Y/2, BAZA_X, BAZA_Y, 'baza')
for i, (cx, d) in enumerate(zip(x_kol, SREDN), 1):
    okrag(s1, cx, Y_OTWORY, d, 'otw%d' % i)
s1.setExpression('Constraints.baza_w', 'Parametry.baza_x')
s1.setExpression('Constraints.baza_h', 'Parametry.baza_y')
s1.setExpression('Constraints.baza_x', '-Parametry.baza_x / 2')
s1.setExpression('Constraints.baza_y', '-Parametry.baza_y / 2')
for i in range(1, len(SREDN) + 1):
    s1.setExpression('Constraints.otw%d_d' % i, 'Parametry.otwor_%d' % i)
p1 = body.newObject('PartDesign::Pad', 'PadBaza')
p1.Profile = s1; p1.Length = BAZA_Z
p1.setExpression('Length', 'Parametry.baza_z')
doc.recompute()

# --- szkic 2: zebra -------------------------------------------------------
s2 = nowy_szkic('Zebra')
for i, (cx, t) in enumerate(zip(x_zeb, ZEBRA), 1):
    prostokat(s2, cx - t/2, ZEB_Y, t, ZEB_L, 'zeb%d' % i)
    s2.setExpression('Constraints.zeb%d_w' % i, 'Parametry.zebro_%d' % i)
    s2.setExpression('Constraints.zeb%d_x' % i, '%.4f - Parametry.zebro_%d / 2' % (cx, i))
p2 = body.newObject('PartDesign::Pad', 'PadZebra')
p2.Profile = s2; p2.Length = BAZA_Z + ZEB_H
p2.setExpression('Length', 'Parametry.baza_z + Parametry.zebro_h')
doc.recompute()

# --- szkic 3: kolki -------------------------------------------------------
s3 = nowy_szkic('Kolki')
for i, (cx, d) in enumerate(zip(x_kol, SREDN), 1):
    okrag(s3, cx, Y_KOLKI, d, 'kol%d' % i)
    s3.setExpression('Constraints.kol%d_d' % i, 'Parametry.kolek_%d' % i)
p3 = body.newObject('PartDesign::Pad', 'PadKolki')
p3.Profile = s3; p3.Length = BAZA_Z + KOL_H
p3.setExpression('Length', 'Parametry.baza_z + Parametry.kolek_h')
doc.recompute()

# --- opisy (wypukle, wysrodkowane pod kazdym detalem) ---------------------
# Tekst nie jest sterowany arkuszem - powstaje z tych samych list na gorze
# pliku. Zmiana wymiaru w arkuszu NIE przerysuje opisu; zeby zgadzaly sie
# oba, zmieniaj listy ZEBRA / SREDN i uruchom skrypt ponownie.
def opis(tekst, cx, y_dol):
    fn = getattr(Draft, 'make_shapestring', None) or Draft.makeShapeString
    ss = fn(String=tekst, FontFile=CZCIONKA, Size=OPIS_WYS, Tracking=0)
    doc.recompute()
    ksztalt = ss.Shape.copy()
    doc.removeObject(ss.Name)
    if not ksztalt.Faces:                      # gdyby wyszly same kontury
        ksztalt = Part.makeFace(ksztalt.Wires, 'Part::FaceMakerBullseye')
    bb = ksztalt.BoundBox
    ksztalt.translate(V(cx - bb.Center.x, y_dol - bb.YMin, 0))
    return ksztalt.extrude(V(0, 0, BAZA_Z + OPIS_WYPUKLOSC))

napisy = []
for cx, t in zip(x_zeb, ZEBRA):
    napisy.append(opis('%.1f' % t, cx, Y_OPIS_ZEB))
for cx, d in zip(x_kol, SREDN):
    napisy.append(opis('%.1f' % d, cx, Y_OPIS_KOL))
    napisy.append(opis('%.1f' % d, cx, Y_OPIS_OTW))
doc.recompute()

wynik = body.Shape.fuse(napisy).removeSplitter()
eksport = doc.addObject('Part::Feature', 'DoDruku')
eksport.Shape = wynik
doc.recompute()

# --- raport ---------------------------------------------------------------
print('--- DIAGNOSTYKA ---')
for s in (s1, s2, s3):
    print('%-8s zwiazany=%-5s  DOF=%s' % (s.Name, s.FullyConstrained, s.solve()))
print('bryla valid  :', wynik.isValid())
print('bryl w czesci:', len(wynik.Solids))
bb = wynik.BoundBox
print('bbox [mm]    : %.1f x %.1f x %.1f' % (bb.XLength, bb.YLength, bb.ZLength))
print('objetosc     : %.1f mm3  (~%.1f g PLA)' % (wynik.Volume, wynik.Volume * 1.24e-3))

doc.saveAs(os.path.join(OUT, 'test-mini.FCStd'))

# Siatka z jawnie zadana dokladnoscia. Domyslna tesselacja rozbija sie
# na krzywych liter i daje plik kilkanascie razy wiekszy bez zadnego
# zysku - 0.02 mm to i tak dziesiec razy mniej niz warstwa druku.
siatka = MeshPart.meshFromShape(Shape=wynik, LinearDeflection=0.02,
                                AngularDeflection=0.6, Relative=False)
siatka.write(os.path.join(OUT, 'test-mini.stl'))
print('trojkatow w siatce: %d' % siatka.CountFacets)
print('zapisano FCStd / stl')
