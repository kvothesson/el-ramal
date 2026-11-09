"""Hoja de sprites de El Ramal en pixel art de horror.

Genera ../sprites.png (base), ../sprites_brillo.png (solo lo que brilla en la oscuridad)
y ../sprites.json (índice). Uso: python sprites.py
"""
import json, math, os
import numpy as np
from PIL import Image
from pxa import Art, RAMPS, hexrgb
from lamina import locomotora, vagon_caldera, vagon_cantina, anden
from lamina_horror import remap, rust_patches, face, WHITE, R, cantina_muerta, caldera_muerta, loco_muerta

ROOT = os.path.join(os.path.dirname(__file__), '..')
GLOW = {WHITE} | {R['blood'][k] for k in (4, 5)} | {R['sick'][k] for k in (3, 4, 5)} | {R['glass'][k] for k in (3, 4, 5)} | {R['pale'][5]}


# ------------------------------------------------------------------ bases de vagón (46x36)
def ruedas(a):
    for cx in (8, 14, 32, 38):
        a.disc_face(cx, 32, 3, 'iron', bias=-0.05)


def plataforma(a):
    ruedas(a); a.box(1, 26, 44, 28, 'wood'); a.box(0, 27, 1, 28, 'iron'); a.box(44, 27, 45, 28, 'iron')


def coche(a, body):
    ruedas(a); a.box(1, 27, 44, 28, 'iron'); a.box(1, 8, 44, 26, body); a.hcyl(0, 45, 6, 2.6, 'iron', bias=0.08)


def ventanas(a, body, modo='enferma', cuales=range(5)):
    for i in cuales:
        x0 = 4 + i * 8
        for y in range(12, 19):
            for x in range(x0, x0 + 5):
                if modo == 'enferma':
                    a.rgb[(x, y)] = R['sick'][3] if y < 14 else (R['sick'][2] if y < 17 else R['sick'][1])
                elif modo == 'oscura':
                    a.rgb[(x, y)] = R['dread'][2]
                elif modo == 'espejo':
                    a.rgb[(x, y)] = R['pale'][4] if (x - x0) + (y - 12) < 3 else R['pale'][2]
        for x in range(x0 - 1, x0 + 6):
            a.rgb[(x, 11)] = R[body][0]; a.rgb[(x, 19)] = R[body][4]


def ojos_en(a, x0, y=15):
    for (dx, dy) in ((1, -1), (2, -1), (3, -1), (1, 0), (2, 0), (3, 0), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (1, 1), (2, 1), (3, 1), (2, -2)):
        a.rgb[(x0 + dx, y + dy)] = R['dread'][0]
    a.rgb[(x0 + 1, y)] = WHITE; a.rgb[(x0 + 3, y)] = WHITE


def filete(a, body, y=22):
    for x in range(2, 44):
        a.rgb[(x, y)] = R['rust'][3]; a.rgb[(x, y + 1)] = R[body][1]


def vagon(kind):
    a = Art(46, 36)
    if kind == 'caldera':
        return caldera_muerta()
    if kind == 'cantina':
        return cantina_muerta()
    if kind in ('pasajeros', 'espejo', 'postal', 'comedor', 'presidencial', 'guarda'):
        body = {'pasajeros': 'green', 'espejo': 'stone', 'postal': 'cream', 'comedor': 'wood', 'presidencial': 'green', 'guarda': 'oxblood'}[kind]
        coche(a, body)
        if kind == 'guarda':
            a.box(16, 0, 30, 5, 'oxblood')
        if kind == 'comedor':
            a.vcyl(36.5, 1.5, 0, 4, 'iron')
        if kind == 'presidencial':
            a.vcyl(41.5, 0.8, 0, 4, 'iron')
        a.render()
        modo = {'espejo': 'espejo', 'postal': 'oscura'}.get(kind, 'enferma')
        ventanas(a, body, modo)
        filete(a, body)
        if kind == 'pasajeros':
            for i in (0, 1, 3, 4):
                ojos_en(a, 4 + i * 8)
        if kind == 'espejo':
            for k in range(3):
                for t in range(10):
                    p = (6 + k * 13 + t // 2, 25 - t)
                    if p in a.rgb:
                        a.rgb[p] = R['pale'][4]
            ojos_en(a, 20)                       # alguien atrás tuyo en el reflejo
        if kind == 'postal':
            for x in range(17, 29):
                for y in range(12, 19):
                    a.rgb[(x, y)] = R['cream'][4]
            for t in range(6):
                a.rgb[(17 + t, 12 + t // 1 if t < 4 else 15)] = R['blood'][3]
                a.rgb[(28 - t, 12 + t // 1 if t < 4 else 15)] = R['blood'][3]
            a.rgb[(22, 16)] = R['blood'][4]; a.rgb[(23, 16)] = R['blood'][4]
        if kind == 'comedor':
            for (x, y) in ((35, 1), (37, 0), (36, 2)):
                pass
        if kind == 'presidencial':
            for x in range(2, 44):
                a.rgb[(x, 22)] = R['brass'][3]
            for y in range(0, 3):
                for x in range(42, 46):
                    a.rgb[(x, y)] = R['blood'][4] if (x + y) % 2 else R['blood'][3]
        if kind == 'guarda':
            for x in range(19, 28):
                a.rgb[(x, 2)] = R['sick'][4]; a.rgb[(x, 3)] = R['sick'][3]
            ojos_en(a, 21, 2) if False else None
        remap(a, [('red', 'oxblood'), ('glass', 'sick')])
        rust_patches(a, [(10, 24, 1), (38, 25, 1)])
        return a
    if kind in ('furgon', 'descarrilado'):
        ruedas(a); a.box(1, 27, 44, 28, 'iron')
        a.box(1, 6, 44, 26, 'wood' if kind == 'furgon' else 'sick')
        a.box(0, 4, 45, 6, 'iron')
        a.render()
        if kind == 'furgon':
            for x in range(3, 44, 3):
                for y in range(8, 26):
                    a.rgb[(x, y)] = R['wood'][1]
            for y in range(10, 26):
                for x in range(16, 30):
                    a.rgb[(x, y)] = R['wood'][2]
            for t in range(15):
                a.rgb[(16 + t * 13 // 14, 10 + t)] = R['wood'][4]; a.rgb[(29 - t * 13 // 14, 10 + t)] = R['wood'][4]
            for (x, y) in ((22, 17), (23, 17), (22, 18), (23, 18)):
                a.rgb[(x, y)] = R['dread'][0]
            a.rgb[(22, 17)] = WHITE                    # algo mira por la rendija
        else:
            for x in range(1, 45):
                for y in range(7, 26):
                    if (x + y) // 4 % 2 == 0:
                        a.rgb[(x, y)] = R['dread'][1]
        rust_patches(a, [(9, 22, 2), (36, 12, 1)])
        return a
    if kind in ('tolva', 'carbonera'):
        ruedas(a); a.box(1, 27, 44, 28, 'iron')
        if kind == 'tolva':
            a.plane([(2, 9), (43, 9), (36, 26), (9, 26)], 'iron', (0, 0, 1))
            a.box(2, 8, 43, 10, 'iron', bevel=1, bias=0.1)
        else:
            a.box(1, 16, 44, 26, 'iron', bias=-0.05)
        top = 8 if kind == 'tolva' else 16
        for x in range(4, 42):
            h = int(5 * math.sin((x - 4) / 37 * math.pi)) + (1 if x % 5 == 0 else 0)
            for y in range(top - h, top):
                a.put(x, y, 'coal', (0, -0.6 + 0.08 * (y - top + h), 0.8))
        a.render()
        for x in range(8, 40, 6):
            if (x, top - 3) in a.rgb:
                a.rgb[(x, top - 3)] = R['coal'][4]
        rust_patches(a, [(14, 20, 2), (30, 22, 1)])
        if kind == 'carbonera':
            for (x, y) in ((20, top - 2), (21, top - 2), (26, top - 3)):
                a.rgb[(x, y)] = R['blood'][4]           # brasas como ojos en el carbón
        return a
    if kind == 'tanque':
        plataforma(a)
        a.hcyl(4, 41, 17, 8, 'iron')
        a.sphere(22.5, 9.5, 3, 'iron', clip_y=10)
        for x in (10, 34):
            for y in range(9, 26):
                d = (y + 0.5 - 17) / 8
                if abs(d) <= 1:
                    a.put(x, y, 'rust', (0, d, math.sqrt(1 - d * d)))
        a.render()
        rust_patches(a, [(18, 22, 2), (28, 13, 1)])
        for y in range(24, 31):                          # gotea
            a.rgb[(26, y)] = R['blood'][3] if y < 28 else R['blood'][2]
        return a
    if kind == 'tambo':
        plataforma(a)
        for i in range(5):
            a.vcyl(5.5 + i * 8.5, 3, 15, 25, 'cream')
            a.vcyl(5.5 + i * 8.5, 1.6, 12, 14, 'cream', bias=-0.1)
        a.render()
        for i in (1, 3):
            x = int(5 + i * 8.5)
            for y in range(18, 26):
                a.rgb[(x, y)] = R['blood'][3] if y < 22 else R['blood'][2]
        return a
    if kind == 'dinamita':
        plataforma(a)
        for (x, y) in ((2, 18), (15, 18), (28, 18), (8, 10), (21, 10)):
            a.box(x, y, x + 12, y + 8, 'blood')
        a.render()
        for (x, y) in ((2, 18), (15, 18), (28, 18), (8, 10), (21, 10)):
            for t in range(5):
                a.rgb[(x + 4 + t, y + 2 + t // 1 if t < 5 else y)] = R['cream'][4]
                a.rgb[(x + 8 - t, y + 2 + t)] = R['cream'][4]
        a.rgb[(30, 8)] = R['wood'][3]; a.rgb[(31, 7)] = R['wood'][3]; a.rgb[(32, 6)] = R['sick'][5]; a.rgb[(33, 5)] = WHITE
        return a
    if kind == 'senal':
        plataforma(a)
        a.vcyl(22.5, 1.2, 4, 25, 'iron')
        a.box(18, 0, 27, 11, 'iron', bias=-0.1)
        a.render()
        for (cy, col) in ((3, 'blood'), (8, 'green')):
            for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (2, 0), (0, -1), (1, -1), (0, 2), (1, 2)):
                a.rgb[(22 + dx, cy + dy)] = R[col][5] if (dx, dy) in ((0, 0),) else R[col][4]
        return a
    if kind == 'farol':
        plataforma(a)
        a.vcyl(22.5, 1.2, 8, 25, 'iron')
        a.box(18, 1, 27, 8, 'iron')
        a.render()
        for y in range(2, 8):
            for x in range(19, 27):
                a.rgb[(x, y)] = R['sick'][5] if y < 5 else R['sick'][4]
        return a
    if kind == 'chatarrero':
        plataforma(a)
        for (x, y, r) in ((11, 18, 6), (27, 17, 7), (38, 21, 4)):
            a.disc_face(x, y, r, 'rust')
        a.line(3, 24, 41, 10, 'iron', bias=0.1)
        a.render()
        for (x, y, r) in ((11, 18, 6), (27, 17, 7), (38, 21, 4)):
            for ang in range(0, 360, 30):
                xx = round(x + (r - 0.5) * math.cos(math.radians(ang))); yy = round(y + (r - 0.5) * math.sin(math.radians(ang)))
                a.rgb[(xx, yy)] = R['rust'][1]
            a.rgb[(x, y)] = R['iron'][4]
        return a
    raise ValueError(kind)


# ------------------------------------------------------------------ pueblos (60x48, en 3/4)
def edificio(a, wall, roof, roto=False):
    a.plane([(2, 36), (58, 36), (54, 30), (6, 30)], 'stone', (0, -0.85, 0.5), bias=0.05)
    a.box(2, 37, 58, 41, 'stone', bevel=1, bias=-0.05)
    a.box(12, 16, 40, 31, wall)
    a.plane([(41, 16), (49, 12), (49, 27), (41, 31)], wall, (0.85, 0, 0.5))
    if roof:
        a.plane([(9, 17), (43, 17), (37, 7), (15, 7)], roof, (0, -0.55, 0.83))
        a.plane([(43, 17), (52, 13), (46, 4), (37, 7)], roof, (0.55, -0.5, 0.67))


def ventana_casa(a, x0, y0, modo, wall):
    for y in range(y0, y0 + 6):
        for x in range(x0, x0 + 5):
            a.rgb[(x, y)] = (R['sick'][4] if y < y0 + 2 else R['sick'][3]) if modo == 'luz' else R['dread'][1]
    for x in range(x0 - 1, x0 + 6):
        a.rgb[(x, y0 - 1)] = R[wall][1]; a.rgb[(x, y0 + 6)] = R[wall][4]


def puerta(a, figura=False):
    for y in range(22, 31):
        for x in range(24, 29):
            a.rgb[(x, y)] = R['dread'][0]
    if figura:
        for (dx, dy) in ((1, 0), (2, 0), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (1, 4), (2, 4), (1, 5), (2, 5), (1, 6), (2, 6)):
            a.rgb[(25 + dx, 23 + dy)] = R['pale'][1]
        a.rgb[(26, 24)] = WHITE; a.rgb[(27, 24)] = WHITE


def pueblo(kind):
    if kind == 'ruina':
        return anden(False)
    a = Art(60, 48)
    if kind == 'anden':
        a = anden(True)
        remap(a, [('glass', 'sick'), ('roof', 'oxblood'), ('plaster', 'stone')])
        puerta(a, True)
        return a
    if kind in ('lecheria', 'deposito', 'capilla', 'galpon', 'fantasma', 'quiniela'):
        wall, roof = {'lecheria': ('cream', 'green'), 'deposito': ('oxblood', 'iron'), 'capilla': ('plaster', 'iron'),
                      'galpon': ('wood', 'rust'), 'fantasma': ('pale', 'pale'), 'quiniela': ('brass', 'oxblood')}[kind]
        edificio(a, wall, roof)
        if kind == 'capilla':
            a.box(24, 0, 30, 9, wall)
            a.plane([(23, 1), (31, 1), (27, -4)], roof, (0, -0.6, 0.8))
        if kind == 'lecheria':
            for i in range(3):
                a.vcyl(44 + i * 4.5, 1.6, 30, 35, 'cream')
        a.render(warm=(26, 26, 30, 0.25) if kind != 'fantasma' else None)
        luz = 'luz' if kind not in ('galpon',) else 'oscura'
        ventana_casa(a, 15, 20, luz, wall); ventana_casa(a, 32, 20, luz, wall)
        puerta(a, kind in ('capilla', 'fantasma'))
        if kind == 'deposito':
            for y in range(17, 31, 2):
                for x in range(12 + (y % 4), 41, 4):
                    if (x, y) in a.rgb and a.rgb[(x, y)] not in (R['sick'][3], R['sick'][4], R['dread'][0]):
                        a.rgb[(x, y)] = R['oxblood'][1]
        if kind == 'capilla':
            a.rgb[(27, -1 + 2)] = R['brass'][4]
            for y in range(-3 + 4, 4):
                pass
            for (x, y) in ((27, 3), (27, 4), (27, 5), (27, 6), (26, 4), (28, 4)):
                a.rgb[(x, y)] = R['blood'][4]
        if kind == 'galpon':
            for y in range(19, 31):
                for x in range(18, 35):
                    a.rgb[(x, y)] = R['dread'][0]
            a.rgb[(23, 24)] = WHITE; a.rgb[(28, 24)] = WHITE
        if kind == 'quiniela':
            for i, d in enumerate((7, 3, 9)):
                for y in range(11, 15):
                    for x in range(18 + i * 6, 22 + i * 6):
                        a.rgb[(x, y)] = R['blood'][4] if (x + y + d) % 3 else R['blood'][5]
        if kind == 'fantasma':
            for (x, y) in list(a.rgb):
                if y % 3 == 0 and (x // 2) % 2 == 0:
                    a.rgb[(x, y)] = R['pale'][1]
        return a
    if kind == 'mina':
        a.sphere(26, 40, 22, 'rust', bias=-0.05)
        a.sphere(22, 36, 14, 'stone', bias=-0.1)
        for t in range(24):
            a.put(42 + t // 6, 38 - t, 'wood', (-0.6, 0, 0.8)); a.put(54 - t // 6, 38 - t, 'wood', (0.6, 0, 0.8))
        for y in (32, 26, 20):
            a.line(43, y, 53, y, 'wood')
        a.disc_face(48, 13, 4, 'iron')
        a.render(warm=(22, 36, 20, 0.3))
        for y in range(30, 41):
            for x in range(16, 27):
                if (x - 21.5) ** 2 / 30 + (y - 41) ** 2 / 110 < 1:
                    a.rgb[(x, y)] = R['dread'][0]
        a.rgb[(19, 35)] = WHITE; a.rgb[(23, 35)] = WHITE
        a.rgb[(20, 34)] = R['blood'][4]
        return a
    if kind == 'farol':
        a.plane([(10, 40), (50, 40), (46, 36), (14, 36)], 'stone', (0, -0.85, 0.5))
        a.vcyl(30, 1.6, 8, 39, 'iron')
        a.box(25, 0, 35, 9, 'iron')
        a.render()
        for y in range(1, 8):
            for x in range(26, 35):
                a.rgb[(x, y)] = R['sick'][5] if y < 4 else R['sick'][4]
        return a
    if kind == 'cruce':
        a.plane([(2, 40), (58, 40), (52, 34), (8, 34)], 'stone', (0, -0.85, 0.5))
        a.vcyl(30, 1.3, 6, 39, 'iron')
        a.render()
        for t in range(-9, 10):
            for (x, y) in ((30 + t, 6 + t // 2), (30 + t, 6 - t // 2)):
                a.rgb[(x, y)] = R['cream'][4] if (t // 3) % 2 else R['blood'][4]
                a.rgb[(x, y + 1)] = R['cream'][2] if (t // 3) % 2 else R['blood'][3]
        return a
    if kind == 'feria':
        for i in range(14):
            y = 12 + i
            a.plane([(30 - i * 1.6, y), (30 + i * 1.6, y), (30 + i * 1.6, y + 1), (30 - i * 1.6, y + 1)], 'blood' if (i // 3) % 2 == 0 else 'cream', (0, -0.3, 0.9))
        a.box(9, 26, 51, 39, 'oxblood')
        a.vcyl(30, 0.8, 4, 12, 'iron')
        a.render()
        for y in range(29, 39):
            for x in range(24, 37):
                a.rgb[(x, y)] = R['dread'][0]
        for x in range(10, 51, 5):
            a.rgb[(x, 27)] = R['sick'][5]
        a.rgb[(28, 32)] = WHITE; a.rgb[(32, 32)] = WHITE
        for y in range(34, 38):
            a.rgb[(30, y)] = R['blood'][4]
        return a
    raise ValueError(kind)


WAGONS = ['loco', 'caldera', 'tanque', 'tambo', 'furgon', 'tolva', 'cantina', 'pasajeros', 'guarda', 'carbonera', 'espejo', 'dinamita',
          'senal', 'postal', 'farol', 'chatarrero', 'comedor', 'descarrilado', 'presidencial', 'fantasma_loco']
TOWNS = ['ruina', 'anden', 'mina', 'lecheria', 'deposito', 'farol', 'cruce', 'feria', 'capilla', 'galpon', 'fantasma', 'quiniela']


def build():
    from lamina_horror import fantasma
    items = []
    for k in WAGONS:
        if k == 'loco':
            a = loco_muerta()
        elif k == 'fantasma_loco':
            a = fantasma()
        else:
            a = vagon(k)
        items.append(('w_' + k, a))
    for k in TOWNS:
        items.append(('t_' + k, pueblo(k)))
    CW, CH, COLS = 64, 52, 8
    rows = (len(items) + COLS - 1) // COLS
    base = np.zeros((rows * CH, COLS * CW, 4), dtype=np.uint8)
    brillo = np.zeros_like(base)
    index = {}
    for n, (name, a) in enumerate(items):
        ox, oy = (n % COLS) * CW + 1, (n // COLS) * CH + 2
        pix = {}
        pix.update({p: c for p, c in a.out_px.items()})
        pix.update(a.rgb)
        xs = [p[0] for p in pix]; ys = [p[1] for p in pix]
        x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
        for (x, y), c in pix.items():
            X, Y = ox + x - x0, oy + y - y0
            base[Y, X] = (*c, 255)
            if tuple(c) in GLOW:
                brillo[Y, X] = (*c, 255)
        index[name] = [ox, oy, x1 - x0 + 1, y1 - y0 + 1, -x0, -y0]
    Image.fromarray(base, 'RGBA').save(os.path.join(ROOT, 'sprites.png'))
    Image.fromarray(brillo, 'RGBA').save(os.path.join(ROOT, 'sprites_brillo.png'))
    json.dump(index, open(os.path.join(ROOT, 'sprites.json'), 'w'), indent=0)
    # lámina de control a x4
    prev = Image.fromarray(base, 'RGBA')
    bg = Image.new('RGBA', prev.size, (12, 10, 20, 255)); bg.alpha_composite(prev)
    os.makedirs(os.path.join(ROOT, 'cuadros'), exist_ok=True)
    bg.resize((prev.width * 3, prev.height * 3), Image.NEAREST).save(os.path.join(ROOT, 'cuadros', 'hoja-sprites.png'))
    print(len(items), 'sprites', base.shape)


if __name__ == '__main__':
    build()
