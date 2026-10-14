# -*- coding: utf-8 -*-
"""
ZOLW - figurka do malowania, jeden kolor, dwie czesci na kolkach.

Proporcje zdjete z klatek serialu (nie z opisu gatunku - pierwsza wersja
byla robiona "na miekkoskorupowca z wiki" i wyszla plaska, a postac ma
pancerz-babel). Cechy, ktore trzymaja podobienstwo:
  - pancerz bardzo wypukly, w rzucie prawie okragly
  - plaski SWINSKI RYJEK z dwiema dziurkami - znak rozpoznawczy
  - duze oczy z ciezkimi powiekami, szeroka glowa
  - krotkie przysadziste nogi z wyraznymi pazurami
  - kolce na rancie pancerza

Wszystkie wymiary licze jako ulamek PANCERZ_DL, wiec zmiana tej jednej
liczby przeskalowuje cala figurke z zachowaniem proporcji.

Poza: ryjek oparty o plyte. To drugi punkt podparcia - dzieki niemu szyja
drukuje sie bez podpor mimo wysiegu.

Jednostki: milimetry (1 jednostka Blendera = 1 mm).
Uruchomienie:  OUT_DIR=. python3 -I zolw.py
"""
import os, math
import bpy, bmesh
from mathutils import Vector

OUT = os.environ.get('OUT_DIR', os.getcwd())
V = Vector

# ===========================================================================
#  JEDYNY WYMIAR, KTORY USTAWIASZ RECZNIE
# ===========================================================================
PANCERZ_DL = 70.0        # dlugosc pancerza [mm]; cala reszta skaluje sie z tego
S = PANCERZ_DL

# ---- proporcje (ulamki S), odczytane z klatek ----------------------------
P_SZER_F   = 0.88        # pancerz w rzucie prawie okragly
P_WYS_F    = 0.52        # BABEL, nie nalesnik - to glowna poprawka wzgl. v1
P_RANT_F   = 0.030       # grubosc wywinietego rantu
KOLEC_N    = 14          # ile kolcow na rancie
KOLEC_DL_F = 0.070
KOLEC_R_F  = 0.030

CIALO_Z0_F = 0.145       # PRZESWIT POD BRZUCHEM - tulow wisi nad ziemia
                         #   na nogach. Uwaga: od ok. 0.10 w gore brzuch
                         #   przestaje byc samonosny i chce podpor.
CIALO_WYS_F= 0.17
CIALO_DL_F = 0.86
CIALO_SZER_F = 0.74      # wzgledem szerokosci pancerza

SZYJA_R_F  = 0.078       # gruba szyja
GLOWA_Z_F     = 0.60     # na jakiej wysokosci siedzi glowa (leb w gorze)
SZYJA_KAT_DOL = 58.0     # kat szyi przy pancerzu [st.] - stromo
SZYJA_KAT_GORA= 46.0     # kat szyi pod glowa [st.] - lagodniej = widoczny luk
                         #   Oba musza zostac >= 45, inaczej spod szyi staje
                         #   sie zwisem. Wysieg do przodu wychodzi z nich
                         #   i z GLOWA_Z_F, nie zadaje sie go osobno.
GLOWA_POCHYL  = 24.0     # odgiecie lba do gory [st.]
PYSK_ROZWARCIE= 40.0     # rozwarcie paszczy [st.] - 0 = pysk zamkniety
PYSK_GLEB_F   = 0.74     # jak gleboko paszcza wchodzi w glowe (x GLOWA_DL)

GLOWA_DL_F = 0.30
GLOWA_SZER_F = 0.235
GLOWA_WYS_F  = 0.205
OKO_R_F    = 0.050       # duze oczy
POWIEKA_F  = 0.030       # walek nad okiem = ciezka powieka
RYJEK_D_F  = 0.135       # srednica swinskiego dysku
RYJEK_GR_F = 0.038       # grubosc dysku
DZIURKA_D_F= 0.028       # nozdrza

NOGA_WYSUW_F = 0.24      # krotkie nogi
NOGA_R_F     = 0.105
STOPA_DL_F   = 0.22
STOPA_SZER_F = 0.20
STOPA_H_F    = 0.090
PAZUR_DL_F   = 0.080     # duze, wyrazne pazury
PAZUR_R_F    = 0.030
OGON_DL_F    = 0.22

KOLEK_D    = 4.0
KOLEK_H    = 5.0
KOLEK_LUZ  = 0.4
VOXEL      = 0.35
CEL_TROJKATOW = 60000

# ---- wymiary wynikowe ----------------------------------------------------
P_SZER   = S * P_SZER_F
P_WYS    = S * P_WYS_F
CIALO_Z0 = S * CIALO_Z0_F
CIALO_WYS= S * CIALO_WYS_F
C_DL     = S * CIALO_DL_F
C_SZER   = P_SZER * CIALO_SZER_F
CIALO_GORA = CIALO_Z0 + CIALO_WYS

SZYJA_R  = S * SZYJA_R_F
GLOWA_DL = S * GLOWA_DL_F
GLOWA_SZER = S * GLOWA_SZER_F
GLOWA_WYS  = S * GLOWA_WYS_F
OKO_R    = S * OKO_R_F
RYJEK_D  = S * RYJEK_D_F
RYJEK_GR = S * RYJEK_GR_F
NOGA_WYSUW = S * NOGA_WYSUW_F
NOGA_R   = S * NOGA_R_F
STOPA_DL = S * STOPA_DL_F
STOPA_SZER = S * STOPA_SZER_F
STOPA_H  = S * STOPA_H_F
PAZUR_DL = S * PAZUR_DL_F
OGON_DL  = S * OGON_DL_F

# ===========================================================================
#  NARZEDZIA
# ===========================================================================
def wyczysc():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def kula(poz, promien, segs=28):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=promien, location=poz,
                                         segments=segs, ring_count=segs // 2)
    return bpy.context.object

def elipsoida(poz, polosie, segs=28):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=poz,
                                         segments=segs, ring_count=segs // 2)
    o = bpy.context.object
    o.scale = polosie
    bpy.ops.object.transform_apply(scale=True)
    return o

def pudlo(srodek, wymiary):
    bpy.ops.mesh.primitive_cube_add(size=1, location=srodek)
    o = bpy.context.object
    o.scale = V(wymiary)          # szescian size=1 ma bok 1, wiec skala = wymiar
    bpy.ops.object.transform_apply(scale=True)
    return o

def walec(poz, promien, wysokosc, obrot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=promien, depth=wysokosc,
                                        location=poz, rotation=obrot, vertices=40)
    return bpy.context.object

def stozek(poz, r1, r2, wysokosc, obrot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=wysokosc,
                                    location=poz, rotation=obrot, vertices=24)
    return bpy.context.object

def polacz(obiekty, nazwa):
    for o in bpy.context.selected_objects:
        o.select_set(False)
    for o in obiekty:
        o.select_set(True)
    bpy.context.view_layer.objects.active = obiekty[0]
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = nazwa
    return o

def boolean(cel, narzedzie, operacja='DIFFERENCE'):
    m = cel.modifiers.new(name='bool', type='BOOLEAN')
    m.operation = operacja
    m.object = narzedzie
    m.solver = 'EXACT'
    bpy.context.view_layer.objects.active = cel
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(narzedzie, do_unlink=True)
    return cel

def remesh(obiekt, voxel=VOXEL):
    m = obiekt.modifiers.new(name='remesh', type='REMESH')
    m.mode = 'VOXEL'
    m.voxel_size = voxel
    m.use_smooth_shade = True
    bpy.context.view_layer.objects.active = obiekt
    bpy.ops.object.modifier_apply(modifier=m.name)
    return obiekt

def wygladz(obiekt, moc=0.5, ile=3):
    m = obiekt.modifiers.new(name='smooth', type='SMOOTH')
    m.factor = moc
    m.iterations = ile
    bpy.context.view_layer.objects.active = obiekt
    bpy.ops.object.modifier_apply(modifier=m.name)
    return obiekt

def decymuj(obiekt, cel):
    n = len(obiekt.data.polygons)
    if n <= cel:
        return obiekt
    m = obiekt.modifiers.new(name='dec', type='DECIMATE')
    m.ratio = cel / n
    bpy.context.view_layer.objects.active = obiekt
    bpy.ops.object.modifier_apply(modifier=m.name)
    return obiekt

def klin(wierzcholek, kier_gora, kier_dol, dlugosc, polszer, nazwa='Klin'):
    """Klin do wyciecia paszczy: ostrze w 'wierzcholek', rozwiera sie
    do przodu miedzy kierunkiem gornej i dolnej szczeki."""
    wx, wy, wz = wierzcholek
    gx, gz = kier_gora
    dx_, dz_ = kier_dol
    w = [(wx, wy - polszer, wz), (wx, wy + polszer, wz),
         (wx + gx * dlugosc, wy - polszer, wz + gz * dlugosc),
         (wx + gx * dlugosc, wy + polszer, wz + gz * dlugosc),
         (wx + dx_ * dlugosc, wy - polszer, wz + dz_ * dlugosc),
         (wx + dx_ * dlugosc, wy + polszer, wz + dz_ * dlugosc)]
    f = [(0, 2, 4), (1, 5, 3), (0, 1, 3, 2), (0, 4, 5, 1), (2, 3, 5, 4)]
    me = bpy.data.meshes.new(nazwa)
    me.from_pydata(w, [], f)
    me.update()
    ob = bpy.data.objects.new(nazwa, me)
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    return ob

def diagnostyka(obiekt, etykieta):
    bm = bmesh.new()
    bm.from_mesh(obiekt.data)
    nonmanifold = [e for e in bm.edges if not e.is_manifold]
    objetosc = bm.calc_volume(signed=True)
    # Liczba ROZLACZNYCH bryl. Szczelnosc tego nie wykrywa: model moze miec
    # zero krawedzi niemanifoldowych i dalej byc kilkoma luznymi kawalkami.
    widziane, bryly = set(), 0
    for f0 in bm.faces:
        if f0.index in widziane:
            continue
        bryly += 1
        stos = [f0]; widziane.add(f0.index)
        while stos:
            f = stos.pop()
            for e in f.edges:
                for s2 in e.link_faces:
                    if s2.index not in widziane:
                        widziane.add(s2.index); stos.append(s2)
    bm.free()
    bb = [obiekt.matrix_world @ V(c) for c in obiekt.bound_box]
    xs=[v.x for v in bb]; ys=[v.y for v in bb]; zs=[v.z for v in bb]
    print('%-9s trojk=%-6d nonmanifold=%-3d ROZLACZNYCH=%-3d bbox=%.1f x %.1f x %.1f mm  V=%.1f cm3'
          % (etykieta, len(obiekt.data.polygons), len(nonmanifold), bryly,
             max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs), objetosc/1000.0))
    if bryly != 1:
        print('   !!! %s rozpada sie na %d bryl' % (etykieta, bryly))
    return len(nonmanifold), bryly, objetosc

# ===========================================================================
#  CIALO
# ===========================================================================
wyczysc()
bryly = []
def bryla(poz, polosie):
    bryly.append(elipsoida(poz, polosie))

# --- tulow ---------------------------------------------------------------
for i in range(9):
    t = (i / 8.0 - 0.5) * 2.0
    zwez = math.sqrt(max(0.14, 1.0 - 0.70 * t * t))
    bryla((t * C_DL * 0.40, 0, CIALO_Z0 + CIALO_WYS * 0.46),
          (C_DL * 0.12, C_SZER * 0.5 * zwez, CIALO_WYS * 0.52))

# --- szyja: luk, stromo przy pancerzu, lagodniej pod glowa --------------
#     Nachylenie maleje liniowo z tan(SZYJA_KAT_DOL) do tan(SZYJA_KAT_GORA),
#     co daje widoczne wygiecie zamiast prostego skosu. Wysieg do przodu
#     wyliczam z calki tego nachylenia, zeby trafic w zadana wysokosc glowy.
a_dol  = math.tan(math.radians(SZYJA_KAT_DOL))
a_gora = math.tan(math.radians(SZYJA_KAT_GORA))
x0, z0 = C_DL * 0.50, CIALO_Z0 + CIALO_WYS * 0.25
dz = S * GLOWA_Z_F - z0
dx = 2.0 * dz / (a_dol + a_gora)          # z warunku: pole pod wykresem = dz
print('   szyja: luk %.0f -> %.0f st., wysieg %.1f mm (samonosna gdy >= 45)'
      % (SZYJA_KAT_DOL, SZYJA_KAT_GORA, dx))

SZ_PKT = 20
kolizja = 0.0
for i in range(SZ_PKT):
    t = i / (SZ_PKT - 1.0)
    x = dx * t
    z = z0 + a_dol * x - (a_dol - a_gora) * x * x / (2.0 * dx)
    r = SZYJA_R * (1.0 - 0.16 * t)
    # Punkt szyi lezacy JEDNOCZESNIE w obrysie pancerza i powyzej plaszczyzny
    # jego posadowienia zostanie scięty przez noz splaszczajacy wierzch ciala.
    # Tak wlasnie urwalo kiedys glowe, a kontrola szczelnosci tego nie widziala.
    if (x0 + x) < PANCERZ_DL * 0.5 and (z - r * 0.35) > CIALO_GORA:
        kolizja = max(kolizja, (z - r * 0.35) - CIALO_GORA)
    bryla((x0 + x, 0, z), (r, r, r * 0.95))
if kolizja > 0:
    print('   !!! SZYJA PRZECIETA: noz splaszczajacy siega %.1f mm ponad jej os.'
          % kolizja)
    print('       Grozi urwaniem glowy. Obniz SZYJA_KAT_DOL albo nasade szyi.')
else:
    print('   szyja: os przechodzi pod plaszczyzna posadowienia pancerza - ok')

# --- glowa: odgieta do gory, budowana wzdluz wlasnej osi ----------------
tilt = math.radians(GLOWA_POCHYL)
FX, FZ = math.cos(tilt), math.sin(tilt)         # "do przodu" glowy
UX, UZ = -math.sin(tilt), math.cos(tilt)        # "do gory" glowy
NX, NZ = x0 + dx, z0 + a_dol * dx - (a_dol - a_gora) * dx / 2.0   # koniec szyi

def pkt_glowy(wzdluz, wzwyz=0.0):
    return (NX + FX * wzdluz + UX * wzwyz, 0.0, NZ + FZ * wzdluz + UZ * wzwyz)

for i in range(6):
    t = i / 5.0
    px, _, pz = pkt_glowy(GLOWA_DL * (0.10 + 0.72 * t))
    bryla((px, 0, pz), (GLOWA_DL * 0.20,
                        GLOWA_SZER * 0.50 * (1.0 - 0.42 * t),
                        GLOWA_WYS * 0.50 * (1.0 - 0.34 * t)))

# --- policzki -----------------------------------------------------------
for strona in (1, -1):
    cx_, _, cz_ = pkt_glowy(GLOWA_DL * 0.28, -GLOWA_WYS * 0.08)
    bryla((cx_, strona * GLOWA_SZER * 0.22, cz_),
          (GLOWA_DL * 0.26, GLOWA_SZER * 0.26, GLOWA_WYS * 0.30))

# --- nogi: krotkie slupki ze stopa --------------------------------------
NOGI = [( C_DL * 0.30,  1,  42),
        ( C_DL * 0.30, -1,  42),
        (-C_DL * 0.30,  1, -44),
        (-C_DL * 0.30, -1, -44)]
STOPY = []
for bx, strona, kat in NOGI:
    a = math.radians(kat)
    z_biodro = CIALO_Z0 + CIALO_WYS * 0.40
    x_st = bx + math.sin(a) * NOGA_WYSUW
    y_st = strona * (C_SZER * 0.34 + math.cos(a) * NOGA_WYSUW)
    STOPY.append((x_st, y_st, a, strona))
    for i in range(10):
        t = i / 9.0
        x = bx + math.sin(a) * NOGA_WYSUW * t
        y = strona * (C_SZER * 0.34 + math.cos(a) * NOGA_WYSUW * t)
        z = z_biodro - (z_biodro - STOPA_H * 0.55) * t
        r = NOGA_R * (1.0 - 0.22 * t)
        bryla((x, y, z), (r, r, r * 0.95))
    bryla((x_st, y_st, STOPA_H * 0.34),
          (STOPA_DL * 0.5, STOPA_SZER * 0.5, STOPA_H * 0.78))

# --- ogon ----------------------------------------------------------------
for i in range(8):
    t = i / 7.0
    r = S * 0.055 * (1.0 - 0.60 * t)
    bryla((-C_DL * 0.44 - OGON_DL * t, 0, CIALO_Z0 + CIALO_WYS * 0.30 - S * 0.02 * t),
          (r, r * 0.9, r * 0.8))

cialo = polacz(bryly, 'Cialo')
remesh(cialo)
wygladz(cialo, 0.5, 3)

# spod plaski (stopy i ryjek na plycie)
boolean(cialo, pudlo((0, 0, -200), (600, 600, 400)), 'DIFFERENCE')
# plaski wierzch pod obrysem pancerza
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=200, location=(0, 0, CIALO_GORA + 100),
                                    vertices=64)
ob = bpy.context.object
ob.scale = (PANCERZ_DL * 0.5 * 0.99, P_SZER * 0.5 * 0.99, 1.0)
bpy.ops.object.transform_apply(scale=True)
boolean(cialo, ob, 'DIFFERENCE')

# ===========================================================================
#  DETALE GLOWY: swinski ryjek, nozdrza, oczy, powieki
# ===========================================================================
dodatki = []
# ryjek - splaszczona elipsoida na koncu pyska
RPX, _, RPZ = pkt_glowy(GLOWA_DL * 0.86)
dodatki.append(elipsoida((RPX, 0, RPZ),
                         (RYJEK_GR * 1.10, RYJEK_D * 0.44, RYJEK_D * 0.40)))

# oczy - wysoko i blisko czola, jak na rysunku
for strona in (1, -1):
    ox_, _, oz_ = pkt_glowy(GLOWA_DL * 0.30, GLOWA_WYS * 0.30)
    dodatki.append(elipsoida((ox_, strona * GLOWA_SZER * 0.26, oz_),
                             (OKO_R * 0.95, OKO_R * 1.05, OKO_R * 1.05), segs=24))

# --- pazury: po 3 na stope ----------------------------------------------
for x_lapa, y_lapa, a, strona in STOPY:
    for k in (-1, 0, 1):
        ox, oy = math.sin(a), strona * math.cos(a)
        bx_, by_ = -oy, ox
        kx = x_lapa + ox * (STOPA_DL * 0.5 - S * 0.02) + bx_ * k * STOPA_SZER * 0.30
        ky = y_lapa + oy * (STOPA_DL * 0.5 - S * 0.02) + by_ * k * STOPA_SZER * 0.30
        dodatki.append(stozek((kx, ky, STOPA_H * 0.45), S * PAZUR_R_F, S * 0.004, PAZUR_DL,
                              obrot=(0, math.radians(90), math.atan2(oy, ox))))

# --- kolki laczace -------------------------------------------------------
POZ_KOLKOW = [(PANCERZ_DL * 0.20, 0), (-PANCERZ_DL * 0.20, 0)]
for kx, ky in POZ_KOLKOW:
    dodatki.append(walec((kx, ky, CIALO_GORA + KOLEK_H / 2 - 0.5), KOLEK_D / 2, KOLEK_H))

cialo = polacz([cialo] + dodatki, 'Cialo')
remesh(cialo)

# PASZCZA - wycinana PO remeshu. Przed remeshem voxel zalalby szczeline,
# a boolean na samoprzecinajacej sie siatce (patrz pancerz) jest nieokreslony.
g = math.radians(PYSK_ROZWARCIE) * 0.5
gx, gz = FX * math.cos(g) - UX * math.sin(g), FZ * math.cos(g) - UZ * math.sin(g)
dx_, dz_ = FX * math.cos(g) + UX * math.sin(g), FZ * math.cos(g) + UZ * math.sin(g)
wx, _, wz = pkt_glowy(GLOWA_DL * 0.10, -GLOWA_WYS * 0.06)
boolean(cialo, klin((wx, 0.0, wz), (gx, gz), (dx_, dz_),
                    GLOWA_DL * PYSK_GLEB_F, GLOWA_SZER * 0.44), 'DIFFERENCE')

# nozdrza - wiercone wzdluz osi glowy
for strona in (1, -1):
    nx_, _, nz_ = pkt_glowy(GLOWA_DL * 0.84, GLOWA_WYS * 0.02)
    d = walec((nx_, strona * RYJEK_D * 0.18, nz_), S * DZIURKA_D_F * 0.5,
              RYJEK_GR * 2.2, obrot=(0, math.radians(90.0 - GLOWA_POCHYL), 0))
    boolean(cialo, d, 'DIFFERENCE')
decymuj(cialo, CEL_TROJKATOW)

# ===========================================================================
#  PANCERZ - wypukly babel z rantem i kolcami
# ===========================================================================
pancerz = elipsoida((0, 0, 0), (PANCERZ_DL * 0.5, P_SZER * 0.5, P_WYS), segs=56)
pancerz.name = 'Pancerz'
boolean(pancerz, pudlo((0, 0, -200), (600, 600, 400)), 'DIFFERENCE')

rant = walec((0, 0, S * P_RANT_F * 0.5), 1, S * P_RANT_F, obrot=(0, 0, 0))
rant.scale = (PANCERZ_DL * 0.5 * 1.035, P_SZER * 0.5 * 1.045, 1.0)
bpy.ops.object.transform_apply(scale=True)
czesci_p = [pancerz, rant]

# kolce na rancie - jak na klatkach
for i in range(KOLEC_N):
    fi = 2 * math.pi * (i + 0.5) / KOLEC_N
    px = math.cos(fi) * PANCERZ_DL * 0.5 * 1.00
    py = math.sin(fi) * P_SZER * 0.5 * 1.01
    kier = math.atan2(math.sin(fi) * P_SZER, math.cos(fi) * PANCERZ_DL)
    czesci_p.append(stozek((px, py, S * P_RANT_F * 0.9 + S * KOLEC_R_F * 1.5),
                           S * KOLEC_R_F, S * 0.003, S * KOLEC_DL_F,
                           obrot=(0, math.radians(58), kier)))
pancerz = polacz(czesci_p, 'Pancerz')

# KOLEJNOSC MA ZNACZENIE: najpierw remesh, potem boolean.
# Po join() pancerz to kilkanascie przenikajacych sie powlok (kopula, rant,
# kolce). Boolean na samoprzecinajacej sie siatce jest nieokreslony - przy
# odwrotnej kolejnosci solver skasowal cala kopule i zostawil same kolce.
remesh(pancerz)
# bezpiecznik: nic nie moze wystawac ponizej plaszczyzny posadowienia,
# inaczej pancerz stanie na czubkach kolcow zamiast na plaskim spodzie
boolean(pancerz, pudlo((0, 0, -200), (600, 600, 400)), 'DIFFERENCE')
for kx, ky in POZ_KOLKOW:
    boolean(pancerz, walec((kx, ky, KOLEK_H / 2 - 0.6),
                           (KOLEK_D + KOLEK_LUZ) / 2, KOLEK_H + 1.0), 'DIFFERENCE')
decymuj(pancerz, CEL_TROJKATOW // 2)

# ===========================================================================
#  RAPORT + EKSPORT
# ===========================================================================
print('\n--- DIAGNOSTYKA  (PANCERZ_DL = %.0f mm) ---' % S)
nm_c, br_c, v_c = diagnostyka(cialo, 'cialo')
nm_p, br_p, v_p = diagnostyka(pancerz, 'pancerz')
print('objetosc razem: %.1f cm3' % ((v_c + v_p) / 1000.0))


def eksport(obiekt, nazwa):
    for o in bpy.data.objects:
        o.select_set(False)
    obiekt.select_set(True)
    bpy.context.view_layer.objects.active = obiekt
    bpy.ops.wm.stl_export(filepath=os.path.join(OUT, nazwa),
                          export_selected_objects=True, global_scale=1.0)
    print('zapisano %s' % nazwa)

eksport(cialo, 'zolw-cialo.stl')
eksport(pancerz, 'zolw-pancerz.stl')
pancerz.location = (0, 0, CIALO_GORA)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.wm.stl_export(filepath=os.path.join(OUT, 'zolw-zlozenie.stl'),
                      export_selected_objects=False, global_scale=1.0)
print('zapisano zolw-zlozenie.stl')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'zolw.blend'))
