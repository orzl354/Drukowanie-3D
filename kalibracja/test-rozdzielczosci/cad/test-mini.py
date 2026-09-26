# -*- coding: utf-8 -*-
"""
TEST ROZDZIELCZOSCI MALYCH DETALI - A1, dysza 0.4
Odpowiada na pytanie: jak cienki detal wychodzi jeszcze uzywalny?
  strefa A: 8 zeber pionowych  1.6 -> 0.3 mm  (statywy skrzydla, zebra dyfuzora)
  strefa B: 6 kolkow           1.6 -> 0.4 mm  (kolki montazowe)
  strefa C: 6 otworow          1.6 -> 0.4 mm  (gniazda pod kolki)
"""
import os, sys
import FreeCAD as App
import Part, Sketcher, Mesh

OUT = os.environ.get('OUT_DIR', os.getcwd())
V = App.Vector
C = Sketcher.Constraint

ZEBRA  = [1.6, 1.2, 1.0, 0.8, 0.6, 0.5, 0.4, 0.3]   # grubosci zeber
SREDN  = [1.6, 1.2, 1.0, 0.8, 0.6, 0.4]             # srednice kolkow i otworow
BAZA_X, BAZA_Y, BAZA_Z = 56.0, 30.0, 1.6
ZEB_H, ZEB_L, ZEB_ROZ, ZEB_Y = 6.0, 8.0, 6.0, 5.0   # wys / dlug / rozstaw / y poczatku
KOL_H, KOL_ROZ = 4.0, 7.0
Y_KOLKI, Y_OTWORY = -3.0, -11.0

doc = App.newDocument("test_mini")

# --- arkusz ---------------------------------------------------------------
ark = doc.addObject('Spreadsheet::Sheet', 'Parametry')
ark.set('A1', 'parametr'); ark.set('B1', 'wartosc'); ark.set('C1', 'opis')
wiersz = 2
def par(nazwa, wart, opis):
    global wiersz
    ark.set('A%d' % wiersz, nazwa); ark.set('B%d' % wiersz, str(wart))
    ark.set('C%d' % wiersz, opis);  ark.setAlias('B%d' % wiersz, nazwa)
    wiersz += 1
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

def prostokat(szkic, x0, y0, w, h, tag, wyr_w=None):
    """Dodaje w pelni zwiazany prostokat; zwraca indeks pierwszej linii."""
    n = szkic.GeometryCount
    p = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    for a, b in zip(p, p[1:] + p[:1]):
        szkic.addGeometry(Part.LineSegment(V(a[0], a[1], 0), V(b[0], b[1], 0)), False)
    szkic.addConstraint([
        C('Coincident', n, 2, n+1, 1), C('Coincident', n+1, 2, n+2, 1),
        C('Coincident', n+2, 2, n+3, 1), C('Coincident', n+3, 2, n, 1),
        C('Horizontal', n), C('Horizontal', n+2),
        C('Vertical', n+1), C('Vertical', n+3)])
    i = szkic.addConstraint(C('DistanceX', n, 1, n, 2, w));     szkic.renameConstraint(i, tag + '_w')
    i = szkic.addConstraint(C('DistanceY', n+1, 1, n+1, 2, h)); szkic.renameConstraint(i, tag + '_h')
    i = szkic.addConstraint(C('DistanceX', -1, 1, n, 1, x0));   szkic.renameConstraint(i, tag + '_x')
    i = szkic.addConstraint(C('DistanceY', -1, 1, n, 1, y0));   szkic.renameConstraint(i, tag + '_y')
    return n

def okrag(szkic, cx, cy, d, tag):
    n = szkic.GeometryCount
    szkic.addGeometry(Part.Circle(V(cx, cy, 0), V(0, 0, 1), d / 2.0), False)
    i = szkic.addConstraint(C('Diameter', n, d));              szkic.renameConstraint(i, tag + '_d')
    i = szkic.addConstraint(C('DistanceX', -1, 1, n, 3, cx));  szkic.renameConstraint(i, tag + '_x')
    i = szkic.addConstraint(C('DistanceY', -1, 1, n, 3, cy));  szkic.renameConstraint(i, tag + '_y')
    return n

def nowy_szkic(nazwa):
    s = body.newObject('Sketcher::SketchObject', nazwa)
    s.AttachmentSupport = [(doc.getObject('XY_Plane'), '')]
    s.MapMode = 'FlatFace'
    return s

# --- szkic 1: baza + otwory ----------------------------------------------
s1 = nowy_szkic('Baza')
prostokat(s1, -BAZA_X/2, -BAZA_Y/2, BAZA_X, BAZA_Y, 'baza')
x_otw = [(i - (len(SREDN)-1)/2.0) * KOL_ROZ for i in range(len(SREDN))]
for i, (cx, d) in enumerate(zip(x_otw, SREDN), 1):
    okrag(s1, cx, Y_OTWORY, d, 'otw%d' % i)
s1.setExpression('Constraints.baza_w', 'Parametry.baza_x')
s1.setExpression('Constraints.baza_h', 'Parametry.baza_y')
s1.setExpression('Constraints.baza_x', '-Parametry.baza_x / 2')
s1.setExpression('Constraints.baza_y', '-Parametry.baza_y / 2')
for i in range(1, len(SREDN)+1):
    s1.setExpression('Constraints.otw%d_d' % i, 'Parametry.otwor_%d' % i)
p1 = body.newObject('PartDesign::Pad', 'PadBaza')
p1.Profile = s1; p1.Length = BAZA_Z
p1.setExpression('Length', 'Parametry.baza_z')
doc.recompute()

# --- szkic 2: zebra -------------------------------------------------------
s2 = nowy_szkic('Zebra')
x_zeb = [(i - (len(ZEBRA)-1)/2.0) * ZEB_ROZ for i in range(len(ZEBRA))]
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
for i, (cx, d) in enumerate(zip(x_otw, SREDN), 1):
    okrag(s3, cx, Y_KOLKI, d, 'kol%d' % i)
    s3.setExpression('Constraints.kol%d_d' % i, 'Parametry.kolek_%d' % i)
p3 = body.newObject('PartDesign::Pad', 'PadKolki')
p3.Profile = s3; p3.Length = BAZA_Z + KOL_H
p3.setExpression('Length', 'Parametry.baza_z + Parametry.kolek_h')
doc.recompute()

# --- raport ---------------------------------------------------------------
print('--- DIAGNOSTYKA ---')
for s in (s1, s2, s3):
    print('%-8s zwiazany=%-5s  DOF=%s' % (s.Name, s.FullyConstrained, s.solve()))
print('bryla valid  :', body.Shape.isValid())
print('bryl w czesci:', len(body.Shape.Solids))
bb = body.Shape.BoundBox
print('bbox [mm]    : %.1f x %.1f x %.1f' % (bb.XLength, bb.YLength, bb.ZLength))
print('objetosc     : %.1f mm3' % body.Shape.Volume)

doc.saveAs(os.path.join(OUT, 'test-mini.FCStd'))
Part.export([body], os.path.join(OUT, 'test-mini.step'))
Mesh.export([body], os.path.join(OUT, 'test-mini.stl'))
print('zapisano FCStd / step / stl')
