"""Lienzo de pixel art por código para El Ramal.

Reglas del taller (pixelfilm/AGENTS.md): paleta cerrada, dithering Bayer,
alfa binario, upscale entero con NEAREST. Todo se dibuja en índices de paleta.
"""
import numpy as np
from PIL import Image

PAL_HEX = {
    'void': '06070d', 'sky0': '0b0d1c', 'sky1': '121733', 'sky2': '1b2348', 'sky3': '283363', 'sky4': '3a4680', 'haze': '55609a',
    'star': 'e8e6f2', 'g0': '090c08', 'g1': '121a0e', 'g2': '1c2914', 'g3': '2b3b1d', 'g4': '44562a',
    'w0': '24170f', 'w1': '3f2a1a', 'w2': '63432a', 'w3': '8d6640', 'w4': 'b88d5c',
    'm0': '1d2029', 'm1': '353a48', 'm2': '585f74', 'm3': '8a93a8', 'm4': 'c8cfdc',
    'l0': 'fff4c8', 'l1': 'ffd25a', 'l2': 'f09a30', 'l3': 'b85a22', 'l4': '6e2c18',
    'r0': '4a1018', 'r1': '8c1c24', 'r2': 'd0343a', 'b1': '2a6fb0', 'b2': '58b4ff', 'b0': '173a63',
    'gr1': '2d6b3a', 'gr2': '7fe08c', 'p1': '4a4290', 'p2': '8f86e6', 'cream': 'ece6d6',
    'u0': '0f121a', 'u1': '1a1f2c', 'u2': '2a3144', 'u3': '3c4660', 'mr': 'ff5a6a', 'brick': '7a3a2a', 'brick2': 'a4553a',
    'teal': '1d9e75', 'milk': 'd8d4c4', 'pink': 'd4537e', 'gold': 'd4af37',
    'gh0': '163a3c', 'gh1': '2f7f78', 'gh2': '7fe0cf', 'gh3': 'd2fff4',
    'ru1': '4e2618', 'ru2': '8a4a2a', 'dg': '343520', 'dg2': '55522e', 'fog': '262c3e',
    'clear': 'ff00ff',
}
NAMES = list(PAL_HEX)
IDX = {n: i for i, n in enumerate(NAMES)}
RGB = np.array([[int(h[i:i + 2], 16) for i in (0, 2, 4)] for h in PAL_HEX.values()], dtype=np.uint8)
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0 + 1 / 32


class Canvas:
    def __init__(self, w=480, h=270, fill='void'):
        self.w, self.h = w, h
        self.a = np.full((h, w), IDX[fill], dtype=np.uint8)
        self.clip = (0, 0, w, h)

    def ok(self, x, y):
        c = self.clip
        return c[0] <= x < c[2] and c[1] <= y < c[3]

    def c(self, n):
        return IDX[n] if isinstance(n, str) else n

    def px(self, x, y, col):
        x, y = int(x), int(y)
        if self.ok(x, y):
            self.a[y, x] = self.c(col)

    def get(self, x, y):
        return NAMES[self.a[y, x]]

    def rect(self, x, y, w, h, col):
        c = self.clip
        x0, y0, x1, y1 = max(c[0], int(x)), max(c[1], int(y)), min(c[2], int(x + w)), min(c[3], int(y + h))
        if x1 > x0 and y1 > y0:
            self.a[y0:y1, x0:x1] = self.c(col)

    def hline(self, x0, x1, y, col):
        self.rect(min(x0, x1), y, abs(x1 - x0) + 1, 1, col)

    def vline(self, x, y0, y1, col):
        self.rect(x, min(y0, y1), 1, abs(y1 - y0) + 1, col)

    def line(self, x0, y0, x1, y1, col):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.px(x0, y0, col)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def disc(self, cx, cy, r, col):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + 0.3:
                    self.px(x, y, col)

    def ring(self, cx, cy, r, col):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if r - 0.6 <= d <= r + 0.4:
                    self.px(x, y, col)

    def ellipse_fill(self, cx, cy, rx, ry, col):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    self.px(x, y, col)

    def dith(self, x, y, t, col):
        """Pinta col si la trama Bayer lo deja pasar con intensidad t (0..1)."""
        x, y = int(x), int(y)
        if self.ok(x, y) and t > BAYER[y % 4, x % 4]:
            self.a[y, x] = self.c(col)

    def vgrad(self, x0, y0, x1, y1, cols):
        """Degradé vertical con trama entre una lista de colores."""
        n = len(cols) - 1
        for y in range(y0, y1):
            f = (y - y0) / max(1, (y1 - y0 - 1)) * n
            i = min(n - 1, int(f)); t = f - i
            for x in range(x0, x1):
                self.a[y, x] = self.c(cols[i + 1] if t > BAYER[y % 4, x % 4] else cols[i])

    def glow(self, cx, cy, r, cols, only=None, squash=1.0, power=1.0):
        """Halo por capas: cols de adentro hacia afuera. only: set de colores sobre los que se puede pintar."""
        n = len(cols)
        oki = None if only is None else {self.c(o) for o in only}
        for y in range(int(cy - r * squash - 1), int(cy + r * squash + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if not self.ok(x, y):
                    continue
                d = (((x - cx) ** 2 + ((y - cy) / squash) ** 2) ** 0.5) / r
                if d >= 1:
                    continue
                if oki is not None and self.a[y, x] not in oki:
                    continue
                f = (1 - d) ** power * n
                k = int(f); t = f - k
                k = min(k, n - 1)
                col = cols[n - 1 - k]
                if k == 0 and t <= BAYER[y % 4, x % 4]:
                    continue
                if k > 0 and t <= BAYER[y % 4, x % 4]:
                    col = cols[n - k]
                self.a[y, x] = self.c(col)

    def save(self, path, scale=4):
        img = Image.fromarray(RGB[self.a], 'RGB')
        img.resize((self.w * scale, self.h * scale), Image.NEAREST).save(path)
        return img


# ---------------- letra 5x7 ----------------
G = {
 'A': '01110 10001 10001 11111 10001 10001 10001', 'B': '11110 10001 10001 11110 10001 10001 11110',
 'C': '01110 10001 10000 10000 10000 10001 01110', 'D': '11110 10001 10001 10001 10001 10001 11110',
 'E': '11111 10000 10000 11110 10000 10000 11111', 'F': '11111 10000 10000 11110 10000 10000 10000',
 'G': '01110 10001 10000 10111 10001 10001 01111', 'H': '10001 10001 10001 11111 10001 10001 10001',
 'I': '01110 00100 00100 00100 00100 00100 01110', 'J': '00111 00010 00010 00010 00010 10010 01100',
 'K': '10001 10010 10100 11000 10100 10010 10001', 'L': '10000 10000 10000 10000 10000 10000 11111',
 'M': '10001 11011 10101 10101 10001 10001 10001', 'N': '10001 10001 11001 10101 10011 10001 10001',
 'O': '01110 10001 10001 10001 10001 10001 01110', 'P': '11110 10001 10001 11110 10000 10000 10000',
 'Q': '01110 10001 10001 10001 10101 10010 01101', 'R': '11110 10001 10001 11110 10100 10010 10001',
 'S': '01111 10000 10000 01110 00001 00001 11110', 'T': '11111 00100 00100 00100 00100 00100 00100',
 'U': '10001 10001 10001 10001 10001 10001 01110', 'V': '10001 10001 10001 10001 10001 01010 00100',
 'W': '10001 10001 10001 10101 10101 10101 01010', 'X': '10001 10001 01010 00100 01010 10001 10001',
 'Y': '10001 10001 01010 00100 00100 00100 00100', 'Z': '11111 00001 00010 00100 01000 10000 11111',
 '0': '01110 10001 10011 10101 11001 10001 01110', '1': '00100 01100 00100 00100 00100 00100 01110',
 '2': '01110 10001 00001 00010 00100 01000 11111', '3': '11110 00001 00001 01110 00001 00001 11110',
 '4': '00010 00110 01010 10010 11111 00010 00010', '5': '11111 10000 11110 00001 00001 10001 01110',
 '6': '00110 01000 10000 11110 10001 10001 01110', '7': '11111 00001 00010 00100 01000 01000 01000',
 '8': '01110 10001 10001 01110 10001 10001 01110', '9': '01110 10001 10001 01111 00001 00010 01100',
 '.': '00000 00000 00000 00000 00000 01100 01100', ',': '00000 00000 00000 00000 01100 00100 01000',
 '!': '00100 00100 00100 00100 00100 00000 00100', '¡': '00100 00000 00100 00100 00100 00100 00100',
 '+': '00000 00100 00100 11111 00100 00100 00000', '-': '00000 00000 00000 11111 00000 00000 00000',
 '×': '00000 10001 01010 00100 01010 10001 00000', '/': '00001 00010 00010 00100 01000 01000 10000',
 '%': '11001 11010 00010 00100 01000 01011 10011', ':': '00000 01100 01100 00000 01100 01100 00000',
 '·': '00000 00000 00000 01100 01100 00000 00000', '?': '01110 10001 00001 00010 00100 00000 00100',
 '*': '00100 01110 11111 01110 01010 10001 00000', ' ': '00000 00000 00000 00000 00000 00000 00000',
 '>': '01000 00100 00010 00001 00010 00100 01000', '"': '01010 01010 01010 00000 00000 00000 00000', '<': '00010 00100 01000 10000 01000 00100 00010',
}
ACC = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ñ': 'N'}


def text_w(s, scale=1):
    return (len(s) * 6 - 1) * scale


def text(cv, x, y, s, col, scale=1, outline=None, shadow=None):
    s = s.upper()
    if outline is not None:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
            _text(cv, x + dx, y + dy, s, outline, scale)
        if scale > 1:
            for dx, dy in ((2, 0), (0, 2), (2, 2), (1, 2), (2, 1)):
                _text(cv, x + dx, y + dy, s, outline, scale)
    if shadow is not None:
        _text(cv, x + scale, y + scale, s, shadow, scale)
    _text(cv, x, y, s, col, scale)


def _text(cv, x, y, s, col, scale):
    cx = x
    for ch in s:
        base = ACC.get(ch, ch)
        rows = G.get(base, G['?']).split()
        for j, row in enumerate(rows):
            for i, b in enumerate(row):
                if b == '1':
                    cv.rect(cx + i * scale, y + j * scale, scale, scale, col)
        if ch in ACC:
            if ch == 'Ñ':
                for i, j in ((1, -2), (2, -3), (3, -2), (4, -3)):
                    cv.rect(cx + i * scale, y + j * scale, scale, scale, col)
            else:
                for i, j in ((2, -2), (3, -2)):
                    cv.rect(cx + i * scale, y + j * scale, scale, scale, col)
        cx += 6 * scale


def panel(cv, x, y, w, h, fill='u1', hi='u3', lo='u0', border='void'):
    cv.rect(x, y, w, h, border)
    cv.rect(x + 1, y + 1, w - 2, h - 2, fill)
    cv.hline(x + 1, x + w - 2, y + 1, hi)
    cv.vline(x + 1, y + 1, y + h - 2, hi)
    cv.hline(x + 1, x + w - 2, y + h - 2, lo)
    cv.vline(x + w - 2, y + 1, y + h - 2, lo)


def star(cv, x, y, col='gold', hi='l1'):
    for dx, dy in ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (0, 3), (2, 3)):
        cv.px(x + dx, y + dy, col)
    cv.px(x + 1, y + 1, hi)


class Sprite:
    """Capa chica con transparencia ('clear'): se dibuja con las mismas primitivas y se pega con contorno."""
    def __init__(self, w, h):
        self.cv = Canvas(w, h, fill='clear')

    def blit(self, dst, x, y, outline='void'):
        a = self.cv.a
        h, w = a.shape
        clear = IDX['clear']
        if outline:
            for j in range(-1, h + 1):
                for i in range(-1, w + 1):
                    inside = 0 <= i < w and 0 <= j < h and a[j, i] != clear
                    if inside:
                        continue
                    near = False
                    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ii, jj = i + di, j + dj
                        if 0 <= ii < w and 0 <= jj < h and a[jj, ii] != clear:
                            near = True; break
                    if near:
                        dst.px(x + i, y + j, outline)
        for j in range(h):
            for i in range(w):
                if a[j, i] != clear:
                    dst.px(x + i, y + j, int(a[j, i]))
