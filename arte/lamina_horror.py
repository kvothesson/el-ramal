"""Lámina de horror: el mismo tren y pueblo, pero muerto.

Uso: python lamina_horror.py -> ../cuadros/lamina-horror.png (320x180 x6)
"""
import math, os
import numpy as np
from pxa import RAMPS, hexrgb, save
from lamina import locomotora, vagon_caldera, vagon_cantina, anden, _text

OUT = os.path.join(os.path.dirname(__file__), '..', 'cuadros')
R = {k: [hexrgb(c) for c in v] for k, v in RAMPS.items()}
WHITE = hexrgb('f4fff8')


def remap(a, pairs):
    table = {}
    for src, dst in pairs:
        for k, c in enumerate(R[src]):
            table[c] = R[dst][min(k, len(R[dst]) - 1)]
    a.rgb = {p: table.get(c, c) for p, c in a.rgb.items()}
    a.out_px = {p: table.get(c, c) for p, c in a.out_px.items()}


def rust_patches(a, spots):
    for (x, y, r) in spots:
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r - 1, x + r + 2):
                d = math.hypot((xx - x) / 1.4, yy - y)
                if d <= r and (xx, yy) in a.rgb:
                    a.rgb[(xx, yy)] = R['rust'][2 if d > r - 1 else 3]
                    if d < 0.8:
                        a.rgb[(xx, yy)] = R['rust'][1]


def face(a, x, y, skin='pale', eyes=WHITE):
    """Cara chica: óvalo pálido 4x5, cuencas negras, boca abierta."""
    for (dx, dy) in ((1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (1, 3), (2, 3), (3, 3), (1, 4), (2, 4), (1, 5), (2, 5)):
        a.rgb[(x + dx, y + dy)] = R[skin][4]
    a.rgb[(x, y + 2)] = R[skin][0]; a.rgb[(x + 3, y + 2)] = R[skin][0]
    a.rgb[(x, y + 1)] = eyes; a.rgb[(x + 3, y + 1)] = eyes
    for dy in (3, 4, 5):
        a.rgb[(x + 1, y + dy)] = R[skin][0]; a.rgb[(x + 2, y + dy)] = R[skin][0]
    return
    for (dx, dy) in ((1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (3, 2), (0, 3), (1, 3), (2, 3), (3, 3), (1, 4), (2, 4)):
        a.rgb[(x + dx, y + dy)] = R[skin][4]
    a.rgb[(x + 1, y + 2)] = eyes; a.rgb[(x + 2, y + 2)] = R[skin][0]
    a.rgb[(x + 3, y + 2)] = R[skin][0]
    a.rgb[(x + 1, y + 1)] = R[skin][5]
    a.rgb[(x + 1, y + 4)] = R[skin][2]; a.rgb[(x + 2, y + 4)] = R[skin][2]


def loco_muerta():
    a = locomotora()
    remap(a, [('red', 'oxblood'), ('brass', 'rust'), ('glass', 'pale')])
    rust_patches(a, [(26, 23, 2), (40, 24, 2), (47, 22, 1), (12, 23, 2), (33, 16, 1), (56, 20, 1), (8, 6, 1)])
    for y in range(8, 15):                       # cabina oscura con el maquinista
        for x in range(8, 16):
            a.rgb[(x, y)] = R['dread'][3] if y < 12 else R['dread'][2]
    face(a, 10, 9)
    a.rgb[(15, 8)] = R['pale'][3]; a.rgb[(14, 9)] = R['pale'][3]; a.rgb[(15, 10)] = R['pale'][2]   # vidrio roto
    for (x, y) in ((56, 11), (57, 11), (58, 12), (56, 12), (57, 12), (56, 13), (57, 13)):           # farol: ojo rojo
        a.rgb[(x, y)] = R['blood'][5] if (x, y) == (57, 12) else R['blood'][4]
    a.rgb[(57, 12)] = WHITE
    return a


def cantina_muerta():
    a = vagon_cantina()
    remap(a, [('red', 'oxblood'), ('brass', 'rust'), ('glass', 'sick')])
    for i in range(5):
        x0 = 4 + i * 8
        for y in range(12, 19):
            for x in range(x0, x0 + 5):
                a.rgb[(x, y)] = R['sick'][2] if y < 15 else R['sick'][1]
        if i in (1, 2, 4):                       # pasajeros que miran
            for (dx, dy) in ((1, 14), (2, 14), (3, 14), (1, 15), (2, 15), (3, 15), (0, 17), (1, 17), (2, 17), (3, 17), (4, 17), (0, 18), (1, 18), (2, 18), (3, 18), (4, 18), (1, 16), (2, 16), (3, 16), (2, 13)):
                a.rgb[(x0 + dx, dy)] = R['dread'][0]
            a.rgb[(x0 + 1, 15)] = WHITE; a.rgb[(x0 + 3, 15)] = WHITE
    for (dx, dy) in ((1, 15), (2, 15), (3, 15), (1, 16), (2, 16), (3, 16), (0, 13), (1, 12), (2, 12), (3, 12), (4, 13), (2, 17), (3, 18)):
        a.rgb[(4 + dx, dy)] = R['blood'][3] if dy > 13 else R['blood'][4]   # mano de sangre en la primera ventana
    for (x, y) in ((6, 19), (6, 20), (7, 21)):
        a.rgb[(x, y)] = R['blood'][2]            # chorreado
    return a


def caldera_muerta():
    a = vagon_caldera()
    remap(a, [('red', 'oxblood'), ('brass', 'rust'), ('glass', 'blood')])
    for (x, y) in ((20, 14), (21, 14), (25, 14), (26, 14), (21, 15), (25, 15), (22, 16), (23, 16), (24, 16), (23, 17)):
        a.rgb[(x, y)] = R['blood'][0]            # cara en las brasas
    a.rgb[(20, 14)] = R['blood'][1]; a.rgb[(26, 14)] = R['blood'][1]
    rust_patches(a, [(15, 22, 1), (31, 9, 1)])
    return a


def fantasma():
    a = locomotora()
    pale = R['pale']
    def tog(c, boost=0):
        lum = (0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]) / 255
        return pale[max(0, min(5, int(lum * 7) + boost))]
    a.rgb = {k: tog(c, 1) for k, c in a.rgb.items()}
    a.out_px = {k: pale[1] for k in a.out_px}
    for y in range(8, 15):
        for x in range(8, 16):
            a.rgb[(x, y)] = pale[0]
    for y in range(9, 15):                       # calavera en la cabina
        for x in range(9, 15):
            if not ((x in (9, 14)) and y in (9, 14)):
                a.rgb[(x, y)] = pale[4]
    for (x, y) in ((10, 10), (11, 10), (10, 11), (11, 11), (13, 10), (13, 11)):
        a.rgb[(x, y)] = pale[0]
    a.rgb[(10, 11)] = WHITE; a.rgb[(13, 11)] = WHITE
    for y in range(12, 15):
        a.rgb[(11, y)] = pale[0]; a.rgb[(12, y)] = pale[0]
    for (x, y) in list(a.rgb):                   # se deshace hacia abajo
        if y > 30 and (x + y) % 3 == 0:
            del a.rgb[(x, y)]
        elif y % 4 == 3 and (x // 2) % 3 != 0:
            a.rgb[(x, y)] = pale[1]
    return a


def compose():
    W, H = 320, 180
    img = np.zeros((H, W, 3), dtype=np.int32)
    sky = R['dread'] + [R['blood'][1]]
    bands = [0, 18, 34, 48, 60, 70, 78]
    for y in range(H):
        k = max(i for i, b in enumerate(bands) if y >= b) if y < 84 else 6
        img[y, :] = sky[min(k, 6)]
        if k < 6 and y < 84 and y >= bands[k + 1] - 2 and (y + 0) % 1 == 0:
            for x in range(W):
                if (x + y) % 2 == 0:
                    img[y, x] = sky[k + 1]
    # luna de sangre con nubes que la cortan
    mx, my, mr = 286, 20, 13
    for y in range(my - mr - 3, my + mr + 4):
        for x in range(mx - mr - 3, mx + mr + 4):
            d = math.hypot(x - mx, y - my)
            if d <= mr:
                lit = (x - mx) * -0.6 + (y - my) * -0.5
                k = 5 if lit > mr * 0.45 else (4 if lit > 0 else (3 if lit > -mr * 0.5 else 2))
                img[y, x] = R['blood'][k]
            elif d <= mr + 2 and (x + y) % 2 == 0:
                img[y, x] = R['blood'][1]
    for (x, y, r) in ((281, 16, 2), (290, 25, 2), (279, 26, 1), (293, 14, 1)):
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                if math.hypot(xx - x, yy - y) <= r:
                    img[yy, xx] = R['blood'][2] if tuple(img[yy, xx]) != R['blood'][5] else R['blood'][3]
    for (cy, x0, x1) in ((17, 262, 320), (26, 250, 306)):   # nubes en tiras
        for x in range(x0, x1):
            img[cy, x] = R['dread'][4]; img[cy + 1, x] = R['dread'][3]
            if x % 7 == 0:
                img[cy - 1, x] = R['dread'][4]
    # horizonte: árboles secos, cruces, poste torcido con cuervos
    hor = 78
    for x in range(W):
        h = int(3 + 2 * math.sin(x / 19) + math.sin(x / 7))
        img[hor - h:hor + 1, x] = R['dread'][0]
    def tree(x, h):
        for y in range(hor - h, hor):
            img[y, x] = R['dread'][0]; img[y, x + 1] = R['dread'][0]
        for (dx, dy, l) in ((-1, -h + 4, 6), (1, -h + 7, 7), (-1, -h + 10, 5), (1, -h + 2, 4)):
            for i in range(l):
                xx = x + dx * i + (1 if dx > 0 else 0); yy = hor + dy - i // 2
                img[yy, xx] = R['dread'][0]
                if i == l - 1:
                    img[yy - 1, xx + dx] = R['dread'][0]
    tree(28, 26); tree(118, 20); tree(304, 30)
    for cx in (60, 70, 77, 180, 190):
        img[hor - 9:hor, cx] = R['dread'][0]; img[hor - 7, cx - 2:cx + 3] = R['dread'][0]
    # poste torcido y alambre con cuervos
    for i in range(44):
        img[hor - 44 + i, 2 + i // 9] = R['dread'][0]; img[hor - 44 + i, 3 + i // 9] = R['dread'][0]
    img[hor - 42, 0:10] = R['dread'][0]
    for x in range(4, 104):
        y = hor - 41 + int(6 * math.sin(math.pi * (x - 4) / 100))
        img[y, x] = R['dread'][3]
    for cx in (34, 41, 48, 76):
        y = hor - 41 + int(6 * math.sin(math.pi * (cx - 4) / 100))
        for (dx, dy) in ((0, -1), (1, -1), (-1, -1), (0, -2), (1, -2), (2, -3), (-1, -2)):
            img[y + dy, cx + dx] = R['dread'][0]
        img[y - 2, cx + 1] = R['blood'][4]
    # campo y vía
    for y in range(hor + 1, H):
        img[y, :] = R['grass'][1] if y < 96 else R['grass'][0]
    rail_y = 82
    img[rail_y + 1:rail_y + 5, :] = R['rust'][1]
    for x in range(0, W, 6):
        if x % 30 != 18:                          # durmientes que faltan
            img[rail_y + 2:rail_y + 5, x:x + 4] = R['wood'][1]
            img[rail_y + 2, x:x + 4] = R['wood'][2]
    img[rail_y, :] = R['rust'][3]; img[rail_y + 1, :] = R['rust'][2]
    for x in range(0, W, 3):
        img[rail_y, x] = R['iron'][3]
    # niebla baja en tablero
    for y in range(rail_y - 4, rail_y + 9):
        for x in range(W):
            if (x + y) % 2 == 0 and (math.sin(x / 13 + y) > 0.2):
                img[y, x] = R['pale'][1] if y > rail_y else img[y, x]
    # tren muerto
    can, cal, loc = cantina_muerta(), caldera_muerta(), loco_muerta()
    # humo negro
    for (x, y, r) in ((158, 34, 4), (152, 26, 6), (142, 17, 8), (128, 10, 9)):
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                d = math.hypot(xx - x, yy - y)
                if d <= r:
                    lit = (xx - x) + (yy - y) < -r * 0.6
                    img[yy, xx] = R['dread'][5] if lit else (R['dread'][4] if d < r - 1 else R['dread'][3])
    for (x, y) in ((124, 9), (125, 9), (131, 9), (132, 9)):        # una cara en el humo
        img[y, x] = R['dread'][0]
    img[10, 124] = R['pale'][4]; img[10, 132] = R['pale'][4]
    img[14:18, 127:130] = R['dread'][0]
    can.stamp(img, 8, rail_y - 35)
    cal.stamp(img, 57, rail_y - 35)
    loc.stamp(img, 104, rail_y - 39)
    # haz rojo
    for x in range(168, 212):
        d = (x - 168) / 44
        half = 2 + int(d * 8)
        for y in range(rail_y - 28, rail_y - 27 + half):
            if y < rail_y - 1:
                img[y, x] = R['blood'][1] if d > 0.5 else R['blood'][2]
    # fantasma con jirones hacia atrás
    gh = fantasma()
    for i in range(12):
        y = rail_y - 34 + i * 3
        length = 14 + (i * 7) % 11
        for x in range(214 - length, 222):
            if (x + i) % 2 == 0 or x > 216:
                img[y, x] = R['pale'][1] if x < 214 - length // 2 else R['pale'][2]
    gh.stamp(img, 222, rail_y - 39)
    # animita con velas y banderas rojas
    ax, ay = 150, 160
    for y in range(ay - 12, ay):
        for x in range(ax, ax + 12):
            img[y, x] = R['blood'][2] if x > ax + 1 else R['blood'][3]
    for i in range(7):
        img[ay - 13 - i, ax - 1 + i:ax + 13 - i] = R['blood'][3] if i < 6 else R['blood'][4]
    img[ay - 8:ay - 2, ax + 3:ax + 9] = R['dread'][1]
    for (x, y) in ((ax + 4, ay - 4), (ax + 7, ay - 4)):
        img[y, x] = R['sick'][4]; img[y - 1, x] = R['glass'][4] if 'glass' in R else R['sick'][5]
        img[y - 2, x] = R['sick'][5]
    for (fx, h) in ((ax - 8, 26), (ax + 19, 22)):
        img[ay - h:ay, fx] = R['wood'][2]
        for yy in range(ay - h, ay - h + 6):
            for xx in range(fx + 1, fx + 9 - (yy - (ay - h)) // 2):
                img[yy, xx] = R['blood'][4] if (xx + yy) % 5 else R['blood'][5]
    for (x, y) in ((ax - 3, ay - 1), (ax + 14, ay - 1), (ax + 16, ay - 2)):
        img[y - 3:y + 1, x] = R['green'][2]; img[y - 4, x] = R['green'][4]   # botellas
    for x in range(ax - 6, ax + 22):
        if (x * 7) % 5 < 2:
            img[ay - 1, x] = R['sick'][3]                                     # cera derramada
    # pueblos: ruina y reabierto (luz enferma, alguien en la puerta)
    base = 166
    ru = anden(False)
    re = anden(True)
    remap(re, [('glass', 'sick'), ('roof', 'oxblood'), ('plaster', 'stone')])
    for y in range(22, 31):
        for x in range(24, 29):
            re.rgb[(x, y)] = R['dread'][0]
    for (dx, dy) in ((1, 0), (2, 0), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (1, 4), (2, 4), (1, 5), (2, 5), (1, 6), (2, 6)):
        re.rgb[(25 + dx, 23 + dy)] = R['pale'][1]
    re.rgb[(26, 24)] = WHITE; re.rgb[(27, 24)] = WHITE
    for x in range(52, 56):
        re.rgb[(x, 18)] = R['sick'][5]; re.rgb[(x, 19)] = R['sick'][4]
    for y in range(base - 30, base):
        for x in range(176, 266):
            d = math.hypot((x - 220) / 46, (y - (base - 10)) / 15)
            if d < 1 and tuple(img[y, x]) in (R['grass'][0], R['grass'][1]):
                img[y, x] = R['sick'][1] if d < 0.55 else R['sick'][0]
    for i in range(40):                                                       # sombra larga de la figura
        img[base - 15 + i // 8, 228 - i] = R['dread'][0]; img[base - 14 + i // 8, 228 - i] = R['dread'][0]
    ru.stamp(img, 38, base - 52)
    re.stamp(img, 190, base - 52)
    fx, fy = 229, base - 34                                                   # el que espera en el andén
    for y in range(fy, fy + 19):
        w = 1 if y < fy + 4 else (2 if y < fy + 16 else 1)
        for x in range(fx - w, fx + w + 1):
            img[y, x] = R['dread'][0]
    img[fy + 1, fx - 1] = img[fy + 1, fx + 1] = R['dread'][0]
    img[fy + 2, fx - 1] = np.array(WHITE); img[fy + 2, fx + 1] = np.array(WHITE)
    for y in range(fy + 6, fy + 15):                                          # brazos largos
        img[y, fx - 3] = R['dread'][0]; img[y, fx + 3] = R['dread'][0]
    # cruces y yuyos en el campo de abajo
    for (x, y, h) in ((14, 132, 9), (96, 150, 7), (122, 112, 6), (284, 124, 8), (300, 150, 10), (176, 104, 6)):
        img[y - h:y, x] = R['stone'][2]; img[y - h + 2, x - 2:x + 3] = R['stone'][2]; img[y - h, x] = R['stone'][3]
        img[y, x - 2:x + 3] = R['grass'][2]
    for (x, y) in ((40, 110), (70, 128), (110, 168), (260, 112), (310, 136), (20, 160), (140, 128)):
        for (dx, dy, c) in ((0, 0, R['grass'][3]), (1, -1, R['rust'][3]), (-1, -1, R['grass'][3]), (0, -2, R['rust'][4]), (2, 0, R['grass'][2])):
            img[y + dy, x + dx] = c
    # viñeta en dos escalones
    cx, cy = W / 2, H / 2
    for y in range(H):
        for x in range(W):
            d = math.hypot((x - cx) / (W * 0.62), (y - cy) / (H * 0.62))
            if d > 0.92:
                img[y, x] = (img[y, x] * (0.45 if d > 1.02 else 0.7)).astype(np.int32) if ((x + y) % 2 == 0 or d > 1.02) else img[y, x]
    _text(img, 112, 120, 'REABRIR', 'c0242a')
    for x in range(110, 142):
        img[131, x] = R['blood'][3]
    for i in range(4):
        img[131 - i, 141 - i] = img[131 + i, 141 - i] = R['blood'][3]
    _text(img, 52, base + 2, 'RUINA', '46445a')
    _text(img, 196, base + 2, 'VILLA ALCIRA', 'c0242a')
    _text(img, 212, 92, 'NO VOLVIÓ NADIE', '6e8a8e')
    return img


def apagar(img):
    """Oscurece todo con luces puntuales en escalones; lo que brilla solo queda intacto."""
    H, W = img.shape[:2]
    glow = {WHITE, R['blood'][4], R['blood'][5], R['sick'][3], R['sick'][4], R['sick'][5], R['pale'][4], R['pale'][5],
            R['glass'][3], R['glass'][4], R['glass'][5], R['blood'][3]}
    luces = [  # x, y, radio, fuerza
        (286, 20, 60, 0.55),    # luna
        (168, 44, 70, 0.75),    # ojo rojo de la loco
        (155, 154, 34, 0.8),    # velas de la animita
        (220, 140, 52, 0.75),   # pueblo reabierto, luz enferma
        (254, 60, 46, 0.55),    # resplandor del fantasma
        (36, 64, 30, 0.35),     # ventanas de la cantina
        (80, 60, 22, 0.4),      # brasas de la caldera
    ]
    pasos = [0.18, 0.3, 0.45, 0.65, 0.9]
    out = img.copy()
    for y in range(H):
        for x in range(W):
            c = tuple(int(v) for v in img[y, x])
            if c in glow:
                continue
            f = 0.0
            for (lx, ly, r, st) in luces:
                d = math.hypot(x - lx, (y - ly) * 1.25) / r
                if d < 1:
                    f = max(f, st * (1 - d) ** 1.5)
            v = 0.18 + f
            k = 0
            for i, p in enumerate(pasos):
                if v >= p:
                    k = i
            # borde en damero entre escalones
            if k + 1 < len(pasos) and v > pasos[k] + (pasos[k + 1] - pasos[k]) * 0.6 and (x + y) % 2 == 0:
                k += 1
            m = pasos[k]
            out[y, x] = (np.array(c) * m).astype(np.int32)
    return out


if __name__ == '__main__':
    img = apagar(compose())
    from PIL import Image
    q = Image.fromarray(img.astype(np.uint8), 'RGB').quantize(96, method=Image.Quantize.MAXCOVERAGE, dither=Image.Dither.NONE).convert('RGB')
    img = np.array(q).astype(np.int32)
    save(img, os.path.join(OUT, 'lamina-horror-oscura.png'), 6)
    print('lamina-horror-oscura.png colores:', len({tuple(p) for p in img.reshape(-1, 3)}))
