"""Lámina de calidad: locomotora, versión fantasma, dos vagones, pueblo en ruinas y reabierto.

Uso: python lamina.py -> ../cuadros/lamina.png (320x180 x6)
"""
import math, os
import numpy as np
from pxa import Art, RAMPS, hexrgb, save
import px  # letra 5x7

OUT = os.path.join(os.path.dirname(__file__), '..', 'cuadros')


# ------------------------------------------------------------------ locomotora 64x40
def locomotora():
    a = Art(64, 40)
    # rueda trasera y ruedas motrices
    for cx, r in ((10, 4), (24, 6), (37, 6), (50, 6)):
        a.disc_face(cx, 33, r, 'iron', bias=-0.08)
    a.box(5, 25, 60, 27, 'iron', bias=-0.05)                       # bastidor
    a.box(4, 4, 20, 25, 'red')                                       # cabina
    a.hcyl(2, 22, 3.5, 1.6, 'iron', bias=0.05)                       # techo curvo
    a.hcyl(20, 53, 18, 7, 'iron')                                    # caldera
    a.hcyl(52, 58, 18, 7.5, 'iron', bias=-0.12)                      # caja de humo
    a.vcyl(52.5, 2.6, 4, 11, 'iron')                                 # chimenea
    a.hcyl(48, 57, 3, 1.4, 'iron', bias=0.05)                        # boca de la chimenea
    a.sphere(38.5, 11.5, 4, 'iron', clip_y=12)                       # domo de vapor
    a.sphere(30.5, 11.8, 2.6, 'brass', clip_y=12)                    # arenero de bronce
    a.box(18, 24, 61, 24, 'iron', bevel=0, bias=0.12)                # estribo
    a.box(58, 24, 61, 29, 'red', bevel=1)                            # viga paragolpes
    for i in range(5):                                               # quitapiedras
        a.line(58 + i, 30, 60 + i, 37, 'iron', bias=0.05 * (i % 2))
    a.box(55, 10, 59, 14, 'brass')                                   # farol
    for x in (28, 44):                                               # bandas de bronce en la caldera
        for y in range(11, 26):
            d = (y + 0.5 - 18) / 7
            if abs(d) <= 1:
                a.put(x, y, 'brass', (0, d, math.sqrt(1 - d * d)))
    a.render()
    # detalles a mano
    for y in range(8, 15):                                           # ventana de cabina encendida
        for x in range(8, 16):
            k = 5 if (x < 10 and y < 10) else (4 if y < 12 else 3)
            a.rgb[(x, y)] = hexrgb(RAMPS['glass'][k])
    for x in range(7, 17):
        a.rgb[(x, 7)] = hexrgb(RAMPS['red'][0])
    for y in range(7, 16):
        a.rgb[(7, y)] = hexrgb(RAMPS['red'][0]); a.rgb[(16, y)] = hexrgb(RAMPS['red'][1])
    for x in range(7, 17):
        a.rgb[(x, 15)] = hexrgb(RAMPS['red'][1])
    for x in range(5, 20):                                           # filete dorado de la cabina
        a.rgb[(x, 20)] = hexrgb(RAMPS['brass'][3]); a.rgb[(x, 21)] = hexrgb(RAMPS['red'][1])
    for x in (6, 19):
        for y in range(5, 24, 3):
            a.rgb[(x, y)] = hexrgb(RAMPS['red'][4])                  # remaches
    for x in range(22, 52):                                          # pasamanos
        a.rgb[(x, 14)] = hexrgb(RAMPS['iron'][5] if x % 6 else RAMPS['iron'][3])
    for x in range(22, 52, 5):                                       # remaches en la caldera
        a.rgb[(x, 21)] = hexrgb(RAMPS['iron'][4]); a.rgb[(x, 22)] = hexrgb(RAMPS['iron'][1])
    a.rgb[(56, 11)] = hexrgb('fffbe4'); a.rgb[(57, 11)] = hexrgb('fffbe4'); a.rgb[(56, 12)] = hexrgb('ffe890'); a.rgb[(57, 12)] = hexrgb('ffc04a')
    a.rgb[(58, 12)] = hexrgb('ffe890'); a.rgb[(56, 13)] = hexrgb('ffc04a'); a.rgb[(57, 13)] = hexrgb('e8862a')
    for cx in (24, 37, 50):                                          # rayos y cubos de las ruedas
        for ang in range(0, 360, 45):
            for rr in (2, 3, 4):
                x = round(cx + rr * math.cos(math.radians(ang))); y = round(33 + rr * math.sin(math.radians(ang)))
                a.rgb[(x, y)] = hexrgb(RAMPS['iron'][2])
        a.rgb[(cx, 33)] = hexrgb(RAMPS['brass'][4]); a.rgb[(cx - 1, 33)] = hexrgb(RAMPS['brass'][2])
        for ang in range(200, 290, 15):                              # brillo del aro arriba a la izquierda
            x = round(cx + 5.4 * math.cos(math.radians(ang))); y = round(33 + 5.4 * math.sin(math.radians(ang)))
            a.rgb[(x, y)] = hexrgb(RAMPS['iron'][5])
    for x in range(24, 51):                                          # biela
        a.rgb[(x, 31)] = hexrgb(RAMPS['iron'][5] if x < 30 else RAMPS['iron'][4]); a.rgb[(x, 32)] = hexrgb(RAMPS['iron'][2])
    for x in (24, 37, 50):
        a.rgb[(x, 31)] = hexrgb(RAMPS['brass'][4])
    for x in range(54, 57):                                          # puerta de la caja de humo
        a.rgb[(x, 15)] = hexrgb(RAMPS['iron'][1]); a.rgb[(x, 21)] = hexrgb(RAMPS['iron'][1])
    a.rgb[(55, 18)] = hexrgb(RAMPS['brass'][4])
    a.rgb[(13, 2)] = hexrgb(RAMPS['brass'][3]); a.rgb[(13, 1)] = hexrgb(RAMPS['brass'][4])   # silbato
    return a


# ------------------------------------------------------------------ vagón caldera 46x36
def vagon_caldera():
    a = Art(46, 36)
    for cx in (8, 14, 32, 38):
        a.disc_face(cx, 32, 3, 'iron', bias=-0.05)
    a.box(1, 26, 44, 28, 'wood')
    a.box(0, 27, 1, 28, 'iron'); a.box(44, 27, 45, 28, 'iron')
    a.vcyl(23, 9, 6, 25, 'red')                                      # caldera parada
    a.hcyl(13, 33, 6, 1.6, 'iron', bias=0.05)                        # tapa
    a.vcyl(23, 2.5, 1, 5, 'iron')                                    # chimenea corta
    for y in (10, 19, 24):
        for x in range(14, 33):
            d = (x + 0.5 - 23) / 9
            if abs(d) <= 1:
                a.put(x, y, 'brass', (d, 0, math.sqrt(1 - d * d)), bias=-0.05)
    a.box(17, 12, 29, 18, 'iron', bias=-0.1)                         # boca del hogar
    a.render(warm=(23, 15, 22, 0.35))
    for y in range(13, 18):                                          # fuego
        for x in range(18, 29):
            k = 5 if (20 < x < 26 and 14 < y < 17) else (4 if 19 < x < 28 else 3)
            if y == 13 and x % 3 == 0:
                k = 2
            a.rgb[(x, y)] = hexrgb(RAMPS['glass'][k])
    for (x, y) in ((21, 0), (25, -1), (19, 1)):                     # chispas
        if a.inb(x, y + 1):
            a.rgb[(x, y + 1)] = hexrgb('ffe890')
    for x in range(2, 44, 4):                                        # tablas del piso
        a.rgb[(x, 27)] = hexrgb(RAMPS['wood'][2])
    return a


# ------------------------------------------------------------------ vagón cantina 46x36
def vagon_cantina():
    a = Art(46, 36)
    for cx in (8, 14, 32, 38):
        a.disc_face(cx, 32, 3, 'iron', bias=-0.05)
    a.box(1, 27, 44, 28, 'iron')
    a.box(1, 8, 44, 26, 'red')
    a.hcyl(0, 45, 6, 2.6, 'iron', bias=0.08)                          # techo redondeado
    a.box(15, 1, 30, 4, 'wood')                                       # cartel
    a.render(warm=(23, 17, 26, 0.18))
    for i in range(5):                                               # ventanas encendidas con siluetas
        x0 = 4 + i * 8
        for y in range(12, 19):
            for x in range(x0, x0 + 5):
                k = 5 if (x == x0 and y < 14) else (4 if y < 16 else 3)
                a.rgb[(x, y)] = hexrgb(RAMPS['glass'][k])
        for x in range(x0 - 1, x0 + 6):
            a.rgb[(x, 11)] = hexrgb(RAMPS['red'][0]); a.rgb[(x, 19)] = hexrgb(RAMPS['red'][4])
        a.rgb[(x0 - 1, 15)] = hexrgb(RAMPS['red'][0])
        if i in (1, 3):                                              # gente en la ventana
            for (dx, dy) in ((1, 14), (2, 14), (1, 15), (2, 15), (0, 17), (1, 17), (2, 17), (3, 17), (0, 18), (1, 18), (2, 18), (3, 18), (1, 16), (2, 16)):
                a.rgb[(x0 + dx, dy)] = hexrgb(RAMPS['red'][1])
    for x in range(2, 44):                                           # filete dorado y zócalo
        a.rgb[(x, 22)] = hexrgb(RAMPS['brass'][3]); a.rgb[(x, 23)] = hexrgb(RAMPS['red'][1])
    for x in range(16, 30):                                          # cartel: copa
        pass
    for (x, y) in ((22, 2), (23, 2), (24, 2), (22, 3), (23, 3), (24, 3)):
        a.rgb[(x, y)] = hexrgb(RAMPS['red'][3])
    a.rgb[(23, 4)] = hexrgb(RAMPS['cream'][4]); a.rgb[(22, 5)] = hexrgb(RAMPS['cream'][4]); a.rgb[(24, 5)] = hexrgb(RAMPS['cream'][3])
    for (x, y) in ((18, 2), (27, 2)):
        a.rgb[(x, y)] = hexrgb(RAMPS['glass'][4])
    return a


# ------------------------------------------------------------------ pueblo: andén en 3/4, ruina o reabierto 60x48
def anden(reabierto=True):
    a = Art(60, 48)
    wall = 'plaster' if reabierto else 'stone'
    roof = 'roof' if reabierto else 'stone'
    # andén: cara de arriba (luz) y frente
    a.plane([(2, 36), (58, 36), (54, 30), (6, 30)], 'stone', (0, -0.85, 0.5), bias=0.05)
    a.box(2, 37, 58, 41, 'stone', bevel=1, bias=-0.05)
    # edificio: frente y costado
    a.box(12, 16, 40, 31, wall)
    a.plane([(41, 16), (49, 12), (49, 27), (41, 31)], wall, (0.85, 0, 0.5))
    # techo a dos aguas: faldón de adelante y lateral
    if reabierto:
        a.plane([(9, 17), (43, 17), (37, 7), (15, 7)], roof, (0, -0.55, 0.83))
        a.plane([(43, 17), (52, 13), (46, 4), (37, 7)], roof, (0.55, -0.5, 0.67))
    else:
        a.plane([(9, 17), (26, 17), (24, 9), (15, 7)], roof, (0, -0.55, 0.83))
        a.plane([(30, 17), (43, 17), (37, 7), (33, 9)], roof, (0, -0.55, 0.83), bias=-0.1)
        a.plane([(43, 17), (52, 13), (46, 4), (37, 7)], roof, (0.55, -0.5, 0.67), bias=-0.15)
    # farol del andén
    a.vcyl(53.5, 1, 20, 35, 'iron')
    a.box(51, 17, 56, 20, 'iron')
    warm = (36, 26, 34, 0.4) if reabierto else None
    a.render(warm=warm)
    g = RAMPS['glass']
    # ventanas y puerta
    for (x0, y0) in ((15, 20), (32, 20)):
        for y in range(y0, y0 + 6):
            for x in range(x0, x0 + 5):
                if reabierto:
                    k = 5 if (x == x0 and y == y0) else (4 if y < y0 + 3 else 3)
                    a.rgb[(x, y)] = hexrgb(g[k])
                else:
                    a.rgb[(x, y)] = hexrgb(RAMPS['night'][1])
        for x in range(x0 - 1, x0 + 6):
            a.rgb[(x, y0 - 1)] = hexrgb(RAMPS[wall][1]); a.rgb[(x, y0 + 6)] = hexrgb(RAMPS[wall][4])
        if not reabierto:                                           # tablas cruzadas
            for t in range(6):
                a.rgb[(x0 + min(4, t), y0 + t)] = hexrgb(RAMPS['wood'][3])
    for y in range(22, 31):                                         # puerta
        for x in range(24, 29):
            a.rgb[(x, y)] = hexrgb(RAMPS['wood'][2] if reabierto else RAMPS['wood'][1])
        a.rgb[(23, y)] = hexrgb(RAMPS[wall][1])
    a.rgb[(27, 26)] = hexrgb(RAMPS['brass'][4])
    # cartel
    for x in range(18, 35):
        for y in range(11, 15):
            a.rgb[(x, y)] = hexrgb(RAMPS['cream'][4] if reabierto else RAMPS['stone'][3])
    for x in range(18, 35):
        a.rgb[(x, 15)] = hexrgb(RAMPS['cream'][1] if reabierto else RAMPS['stone'][0])
    if not reabierto:
        a.rgb[(30, 11)] = hexrgb(RAMPS['night'][2]); a.rgb[(31, 11)] = hexrgb(RAMPS['night'][2]); a.rgb[(31, 12)] = hexrgb(RAMPS['night'][2])
        for (x, y) in ((14, 31), (15, 30), (13, 30), (44, 30), (45, 29), (46, 30), (8, 35), (9, 34), (50, 35), (34, 31), (35, 30)):
            a.rgb[(x, y)] = hexrgb(RAMPS['green'][3])               # yuyos
            a.rgb[(x, y - 1)] = hexrgb(RAMPS['green'][4]) if (x + y) % 2 else a.rgb.get((x, y - 1), hexrgb(RAMPS['green'][2]))
        for (x, y) in ((20, 25), (21, 26), (21, 27), (22, 28), (36, 18), (37, 19)):
            a.rgb[(x, y)] = hexrgb(RAMPS['stone'][0])               # grietas
    # luz del farol
    for x in range(52, 56):
        a.rgb[(x, 18)] = hexrgb(g[5] if reabierto else RAMPS['night'][2]); a.rgb[(x, 19)] = hexrgb(g[4] if reabierto else RAMPS['night'][1])
    return a


# ------------------------------------------------------------------ lámina

def compose():
    W, H = 320, 180
    img = np.zeros((H, W, 3), dtype=np.int32)
    night = [hexrgb(c) for c in RAMPS['night']]
    for y in range(H):                                              # cielo en bandas con borde en tablero
        k = min(5, int(y / 22))
        img[y, :] = night[k]
        if k < 5 and y % 22 >= 20:
            for x in range(W):
                if (x + y) % 2 == 0:
                    img[y, x] = night[k + 1]
    for (x, y) in ((14, 8), (40, 20), (77, 5), (120, 14), (160, 9), (199, 22), (236, 6), (262, 17), (300, 11), (88, 30), (284, 30), (57, 36)):
        img[y, x] = hexrgb('b9c3cf')
    for (x, y) in ((140, 26), (250, 32), (20, 44)):
        img[y, x] = hexrgb('fff2b0'); img[y, x - 1] = img[y, x + 1] = img[y - 1, x] = img[y + 1, x] = hexrgb('4a5070')
    # luna
    for y in range(4, 22):
        for x in range(278, 300):
            d = math.hypot(x - 289, y - 13)
            if d <= 8:
                img[y, x] = hexrgb('fff6e0') if d < 6 or (x - 289) + (y - 13) < 0 else hexrgb('c8b89c')
            elif d <= 9.5:
                img[y, x] = hexrgb('30385c')
    for (x, y) in ((286, 11), (291, 15), (288, 16)):
        img[y, x] = hexrgb('d8c8aa')
    # campo y vía
    for y in range(84, H):
        img[y, :] = hexrgb(RAMPS['grass'][1] if y < 98 else RAMPS['grass'][0])
    for x in range(W):
        img[84, x] = hexrgb(RAMPS['grass'][2])
        if x % 5 == 0:
            img[83, x] = hexrgb(RAMPS['grass'][2])
    rail_y = 80
    img[rail_y + 1:rail_y + 5, :] = hexrgb(RAMPS['rust'][1])
    for x in range(0, W, 6):
        img[rail_y + 2:rail_y + 5, x:x + 4] = hexrgb(RAMPS['wood'][1])
        img[rail_y + 2, x:x + 4] = hexrgb(RAMPS['wood'][2])
    img[rail_y, :] = hexrgb(RAMPS['iron'][4]); img[rail_y + 1, :] = hexrgb(RAMPS['iron'][2])
    # tren vivo: cantina, caldera, locomotora
    can = vagon_cantina(); cal = vagon_caldera(); loc = locomotora()
    can.stamp(img, 8, rail_y - 35)
    cal.stamp(img, 57, rail_y - 35)
    for x in (54, 55, 56, 103, 104):
        img[rail_y - 8, x] = hexrgb(RAMPS['iron'][3])
    loc.stamp(img, 104, rail_y - 39)
    # haz del farol de la loco (bandas, sin ruido)
    for x in range(168, 214):
        d = (x - 168) / 46
        half = 2 + int(d * 9)
        for y in range(rail_y - 28 + 0, rail_y - 28 + 1 + half):
            if y < rail_y and (img[y, x] == night[min(5, int(y / 22))]).all():
                img[y, x] = hexrgb('2a2a46') if d > 0.6 else (hexrgb('3a3450') if d > 0.25 else hexrgb('544660'))
    # tren fantasma: la misma loco en materiales fantasma
    gh = locomotora()
    ghr = [hexrgb(c) for c in RAMPS['ghost']]
    def toghost(c, boost=0):
        lum = (0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]) / 255
        return ghr[max(0, min(5, int(lum * 6.5) + boost))]
    gh.rgb = {k: toghost(c, 1) for k, c in gh.rgb.items()}
    gh.out_px = {k: ghr[1] for k in gh.out_px}
    for (x, y) in list(gh.rgb):
        if y % 4 == 3 and (x // 2) % 3 != 0:
            gh.rgb[(x, y)] = ghr[1]
    # halo fantasma en bandas
    for y in range(rail_y - 50, rail_y + 6):
        for x in range(214, 300):
            d = math.hypot((x - 254) / 44, (y - (rail_y - 18)) / 24)
            if d < 1 and (img[y, x] == night[min(5, int(y / 22))]).all():
                img[y, x] = hexrgb('123236') if d < 0.5 else (hexrgb('0e1e2a') if d < 0.8 else img[y, x])
    gh.stamp(img, 222, rail_y - 39)
    # pueblos: ruina -> reabierto
    ru = anden(False); re = anden(True)
    base = 164
    for x in range(W):
        img[base - 4: base, x] = hexrgb(RAMPS['grass'][1])
    ru.stamp(img, 38, base - 52)
    re.stamp(img, 190, base - 52)
    # resplandor cálido del pueblo reabierto, en dos bandas
    for y in range(base - 30, base):
        for x in range(176, 266):
            d = math.hypot((x - 220) / 46, (y - (base - 10)) / 16)
            if d < 1 and tuple(img[y, x]) in (hexrgb(RAMPS['grass'][0]), hexrgb(RAMPS['grass'][1])):
                img[y, x] = hexrgb('3a2a1a') if d < 0.6 else hexrgb('22201a')
    re.stamp(img, 190, base - 52)
    # flecha y textos
    cv = px.Canvas(W, H)
    for y in range(H):
        pass
    arrow_y = base - 26
    for x in range(118, 170):
        img[arrow_y, x] = hexrgb('8ab486')
    for i in range(4):
        img[arrow_y - i, 169 - i] = img[arrow_y + i, 169 - i] = hexrgb('8ab486')
    _text(img, 124, arrow_y - 12, 'REABRIR', '8ab486')
    _text(img, 56, base + 4, 'RUINA', '625f76')
    _text(img, 204, base + 4, 'VILLA ALCIRA', 'ffc04a')
    g2, g3, g4 = (hexrgb(RAMPS['grass'][k]) for k in (2, 3, 4))
    for (x, y) in ((12, 100), (30, 112), (100, 104), (150, 118), (178, 100), (276, 108), (300, 122), (20, 140), (296, 146), (150, 150), (8, 160)):
        for (dx, dy, c) in ((0, 0, g3), (1, -1, g4), (-1, -1, g3), (2, 0, g2), (-2, 0, g2), (0, -2, g4)):
            img[y + dy, x + dx] = c
    for x in range(0, W, 16):                                       # alambrado
        img[101:108, x] = hexrgb(RAMPS['wood'][1]); img[101, x] = hexrgb(RAMPS['wood'][3])
    for x in range(W):
        img[103, x] = hexrgb(RAMPS['iron'][1]) if x % 16 else img[103, x]
    _text(img, 228, rail_y + 8, 'TREN FANTASMA', '6ad8b8')
    _text(img, 40, rail_y + 8, 'CANTINA  CALDERA  LOCOMOTORA', 'b49e86')
    return img


def _text(img, x, y, s, col):
    c = px.Canvas(img.shape[1], img.shape[0], fill='void')
    c.a[:] = 255
    px.text(c, x, y, s, 0)
    mask = c.a == 0
    img[mask] = hexrgb(col)


if __name__ == '__main__':
    img = compose()
    save(img, os.path.join(OUT, 'lamina.png'), 6)
    print('lamina.png', img.shape, 'colores:', len({tuple(p) for p in img.reshape(-1, 3)}))
