"""Pixel art con volumen: materiales con rampas de color, luz por normales y contorno selectivo.

Cada píxel guarda material + normal (o un color fijo). El sombreado cuantiza la luz a
la rampa del material, así el volumen sale con bandas limpias, sin ruido. Después se
pasa el contorno selectivo (del color del material, más claro del lado de la luz).
"""
import math
import numpy as np
from PIL import Image


def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# rampas de oscuro a claro, con cambio de tono (sombras a violeta, luces a cálido)
RAMPS = {
    'iron':   ['15131f', '262536', '3b3c52', '585d75', '828aa0', 'b9c3cf'],
    'red':    ['2a0e1e', '561628', '8a2230', 'bb3a34', 'e0663c', 'f6a466'],
    'brass':  ['2c1a16', '5e3a1c', '9a6420', 'd09a32', 'f0d062', 'fff2b0'],
    'wood':   ['231420', '44262a', '6c3e30', '9a603a', 'c48a50', 'e8bc7c'],
    'coal':   ['0c0b12', '1a1822', '2c2836', '423c4e', '5e566a'],
    'plaster': ['3a2a34', '5e4848', '8a7062', 'b49e86', 'd8c8aa', 'f4ead2'],
    'roof':   ['2a0e1a', '4e1622', '7a2228', 'a8382e', 'cc5a3a', 'e88a58'],
    'stone':  ['1c1a26', '2e2c3a', '46445a', '625f76', '86839a', 'b0aec0'],
    'rust':   ['1e1014', '3a1a18', '5e2c1e', '864424', 'aa6432', 'c88a50'],
    'grass':  ['0e1410', '16221a', '223322', '33482c', '4c6232'],
    'green':  ['0f1c1a', '1c3330', '2a4f45', '3f6e58', '5c8e6a', '8ab486'],
    'cream':  ['3c3036', '6a5a56', '9a8a78', 'c8b89c', 'e8dcc0', 'fff6e0'],
    'glass':  ['5a2010', 'a8481a', 'e8862a', 'ffc04a', 'ffe890', 'fffbe4'],   # emisivo cálido
    'ghost':  ['0c2226', '14403e', '1f6a60', '36a088', '6ad8b8', 'c4fff0'],
    'night':  ['07070e', '0c0d1a', '121428', '1a1e38', '242a4a', '30385c'],
    'blood':  ['14040a', '2e0812', '560c18', '8a1420', 'c0242a', 'e85440'],
    'sick':   ['1a1a10', '34361c', '5a5c2a', '8a8a3a', 'c4bc5a', 'f0e8a0'],   # luz enferma
    'pale':   ['10161a', '22303a', '3e5660', '6e8a8e', 'a8c4c0', 'e4f4ee'],   # piel muerta / fantasma
    'oxblood': ['1a060e', '360a16', '5a1220', '7e1c26', 'a02c2c', 'c04a3a'],
    'dread':  ['040306', '08060c', '0e0a14', '160e1c', '1e1226', '2a1630'],  # cielo
}
L = np.array([-0.55, -0.68, 0.48]); L = L / np.linalg.norm(L)


class Art:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.mat = np.full((h, w), '', dtype=object)
        self.n = np.zeros((h, w, 3)); self.n[..., 2] = 1
        self.fixed = {}          # (x,y) -> rgb
        self.bias = np.zeros((h, w))   # ajuste fino de luz por píxel
        self.emit = np.zeros((h, w), dtype=bool)
        self.no_outline = set()

    def inb(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def put(self, x, y, mat, n=(0, 0, 1), bias=0.0, emit=False):
        x, y = int(x), int(y)
        if not self.inb(x, y):
            return
        self.mat[y, x] = mat; self.n[y, x] = n; self.bias[y, x] = bias; self.emit[y, x] = emit
        self.fixed.pop((x, y), None)

    def fix(self, x, y, rgb):
        x, y = int(x), int(y)
        if self.inb(x, y):
            if not self.mat[y, x]:
                self.mat[y, x] = '_fixed'
            self.fixed[(x, y)] = hexrgb(rgb) if isinstance(rgb, str) else rgb

    def ramp_px(self, x, y, mat, k):
        """Pone un color exacto de una rampa (para detalles a mano)."""
        r = RAMPS[mat]; self.fix(x, y, r[max(0, min(len(r) - 1, k))])
        if self.inb(int(x), int(y)):
            self.mat[int(y), int(x)] = mat

    # --------- primitivas con normal
    def box(self, x0, y0, x1, y1, mat, bevel=1, bias=0.0):
        """Caja vista de frente: cara plana con bisel arriba/izquierda claros y abajo/derecha oscuros."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                n = (0, 0, 1)
                if y - y0 < bevel:
                    n = (0, -0.8, 0.6)
                elif y1 - y < bevel:
                    n = (0, 0.8, 0.6)
                elif x - x0 < bevel:
                    n = (-0.7, 0, 0.7)
                elif x1 - x < bevel:
                    n = (0.7, 0, 0.7)
                self.put(x, y, mat, n, bias)

    def hcyl(self, x0, x1, cy, r, mat, bias=0.0, taper=0):
        for x in range(x0, x1 + 1):
            for y in range(int(cy - r), int(cy + r) + 1):
                d = (y + 0.5 - cy) / r
                if abs(d) <= 1:
                    self.put(x, y, mat, (0, d, math.sqrt(max(0, 1 - d * d))), bias)

    def vcyl(self, cx, r, y0, y1, mat, bias=0.0):
        for y in range(y0, y1 + 1):
            for x in range(int(cx - r), int(cx + r) + 1):
                d = (x + 0.5 - cx) / r
                if abs(d) <= 1:
                    self.put(x, y, mat, (d, 0, math.sqrt(max(0, 1 - d * d))), bias)

    def sphere(self, cx, cy, r, mat, clip_y=None, bias=0.0):
        for y in range(int(cy - r), int(cy + r) + 1):
            if clip_y is not None and y > clip_y:
                continue
            for x in range(int(cx - r), int(cx + r) + 1):
                dx, dy = (x + 0.5 - cx) / r, (y + 0.5 - cy) / r
                q = dx * dx + dy * dy
                if q <= 1:
                    self.put(x, y, mat, (dx, dy, math.sqrt(1 - q)), bias)

    def disc_face(self, cx, cy, r, mat, bias=0.0):
        """Disco plano (rueda) con aro: el borde se trata como tubo."""
        for y in range(int(cy - r), int(cy + r) + 1):
            for x in range(int(cx - r), int(cx + r) + 1):
                dx, dy = x + 0.5 - cx, y + 0.5 - cy
                d = math.hypot(dx, dy)
                if d <= r:
                    if d > r - 1.3:
                        n = (dx / d * 0.8, dy / d * 0.8, 0.6)
                    else:
                        n = (0, 0, 1)
                    self.put(x, y, mat, n, bias)

    def plane(self, pts, mat, n, bias=0.0):
        """Polígono relleno con una sola normal (techos, caras de cajas en 3/4)."""
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            for x in range(int(min(xs)), int(max(xs)) + 1):
                if _inside(x + 0.5, y + 0.5, pts):
                    self.put(x, y, mat, n, bias)

    def line(self, x0, y0, x1, y1, mat, k=None, n=(0, 0, 1), bias=0.0):
        steps = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(steps):
            t = i / max(1, steps - 1)
            x, y = round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
            if k is None:
                self.put(x, y, mat, n, bias)
            else:
                self.ramp_px(x, y, mat, k)

    # --------- sombreado
    def shade(self, warm=None, ambient=0.18):
        """warm: (x, y, radio, fuerza) luz puntual cálida que levanta la rampa."""
        out = {}
        for y in range(self.h):
            for x in range(self.w):
                m = self.mat[y, x]
                if not m:
                    continue
                if (x, y) in self.fixed:
                    out[(x, y)] = self.fixed[(x, y)]; continue
                r = RAMPS[m]
                if self.emit[y, x]:
                    i = 0.75 + self.bias[y, x]
                else:
                    i = ambient + (1 - ambient) * max(0.0, float(np.dot(self.n[y, x], L))) + self.bias[y, x]
                    if warm:
                        wx, wy, wr, ws = warm
                        d = math.hypot(x - wx, y - wy)
                        if d < wr:
                            i += ws * (1 - d / wr) ** 2
                k = int(round(max(0, min(1, i)) * (len(r) - 1)))
                out[(x, y)] = hexrgb(r[k])
        self.rgb = out
        return out

    def outline(self, darken_only=False):
        """Contorno selectivo: color más oscuro del material vecino; un paso más claro del lado de la luz."""
        add = {}
        for y in range(-1, self.h + 1):
            for x in range(-1, self.w + 1):
                if self.inb(x, y) and self.mat[y, x]:
                    continue
                best = None
                for dx, dy, lit in ((1, 0, True), (0, 1, True), (-1, 0, False), (0, -1, False)):
                    xx, yy = x + dx, y + dy
                    if self.inb(xx, yy) and self.mat[yy, xx] and self.mat[yy, xx] != '_fixed':
                        if (xx, yy) in self.no_outline:
                            continue
                        r = RAMPS[self.mat[yy, xx]]
                        c = r[1] if (lit and not darken_only) else r[0]
                        if best is None or not lit:
                            best = c
                if best:
                    add[(x, y)] = hexrgb(best)
        self.out_px = add
        return add

    def stamp(self, dst, ox, oy):
        """Pega el sprite sombreado + contorno en un lienzo RGB (numpy HxWx3)."""
        H, W = dst.shape[:2]
        for (x, y), c in self.out_px.items():
            X, Y = ox + x, oy + y
            if 0 <= X < W and 0 <= Y < H:
                dst[Y, X] = c
        for (x, y), c in self.rgb.items():
            X, Y = ox + x, oy + y
            if 0 <= X < W and 0 <= Y < H:
                dst[Y, X] = c

    def render(self, warm=None):
        self.shade(warm); self.outline(); return self

    def recolor(self, mapping):
        """Cambia materiales (por ejemplo a 'ghost') manteniendo normales: versión fantasma."""
        for y in range(self.h):
            for x in range(self.w):
                m = self.mat[y, x]
                if m in mapping:
                    self.mat[y, x] = mapping[m]
        for (x, y), c in list(self.fixed.items()):
            pass


def _inside(x, y, pts):
    c = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]; xj, yj = pts[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
            c = not c
        j = i
    return c


def save(arr, path, scale):
    img = Image.fromarray(arr.astype(np.uint8), 'RGB')
    img.resize((arr.shape[1] * scale, arr.shape[0] * scale), Image.NEAREST).save(path)
