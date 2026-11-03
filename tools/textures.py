"""Procedural 16x16 pixel-art texture generator for World Foods."""
import math
import random
from PIL import Image, ImageDraw

S = 16


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(c, f):
    """f < 1 darkens, f > 1 lightens."""
    if f >= 1:
        return tuple(min(255, int(v + (255 - v) * (f - 1))) for v in c)
    return tuple(max(0, int(v * f)) for v in c)


class Canvas:
    def __init__(self):
        self.img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        self.px = self.img.load()

    def set(self, x, y, c, a=255):
        if 0 <= x < S and 0 <= y < S:
            self.px[x, y] = (*c, a)

    def get(self, x, y):
        if 0 <= x < S and 0 <= y < S:
            return self.px[x, y]
        return (0, 0, 0, 0)

    def opaque(self, x, y):
        return self.get(x, y)[3] > 0

    def ellipse(self, x0, y0, x1, y1, c):
        layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse([x0, y0, x1, y1], fill=(*c, 255))
        self.img.alpha_composite(layer)
        self.px = self.img.load()

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, c)

    def poly(self, pts, c):
        layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ImageDraw.Draw(layer).polygon(pts, fill=(*c, 255))
        self.img.alpha_composite(layer)
        self.px = self.img.load()

    def line(self, pts, c, w=1):
        layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ImageDraw.Draw(layer).line(pts, fill=(*c, 255), width=w)
        self.img.alpha_composite(layer)
        self.px = self.img.load()

    def finish(self, outline=True, highlight=True):
        """Pixel-art finishing: darken edge pixels and add a top-left highlight."""
        src = self.img.copy()
        sp = src.load()
        if outline or highlight:
            for y in range(S):
                for x in range(S):
                    r, g, b, a = sp[x, y]
                    if a == 0:
                        continue
                    c = (r, g, b)

                    def tr(dx, dy):
                        xx, yy = x + dx, y + dy
                        return not (0 <= xx < S and 0 <= yy < S) or sp[xx, yy][3] == 0

                    if outline and (tr(1, 0) or tr(0, 1) or tr(-1, 0) or tr(0, -1)):
                        if tr(1, 0) or tr(0, 1):
                            self.px[x, y] = (*shade(c, 0.55), 255)
                        else:
                            self.px[x, y] = (*shade(c, 0.7), 255)
                    elif highlight and (tr(-1, -1) or tr(-2, -2)) and not (tr(1, 1)):
                        self.px[x, y] = (*shade(c, 1.25), 255)
        return self.img


def speckle(cv, region, colours, n, seed):
    rnd = random.Random(seed)
    pts = [(x, y) for (x, y) in region if cv.opaque(x, y)]
    for _ in range(n):
        if not pts:
            break
        x, y = rnd.choice(pts)
        cv.set(x, y, rnd.choice(colours))


def box(x0, y0, x1, y1):
    return [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]


# ---------------------------------------------------------------------------
# item styles
# ---------------------------------------------------------------------------

def t_round(cv, c, seed):
    a, leaf = c[0], c[1]
    cv.ellipse(2, 4, 13, 14, a)
    cv.finish()
    cv.rect(7, 2, 8, 4, shade(leaf, 0.8))
    cv.poly([(4, 4), (7, 3), (8, 5), (5, 5)], leaf)
    cv.poly([(8, 4), (11, 3), (11, 5), (8, 5)], leaf)
    cv.set(5, 7, shade(a, 1.6)); cv.set(4, 8, shade(a, 1.4))


def t_berry(cv, c, seed):
    a, leaf = c[0], c[1]
    cv.poly([(2, 6), (13, 6), (12, 10), (8, 15), (7, 15), (3, 10)], a)
    cv.ellipse(2, 4, 13, 10, a)
    cv.finish()
    for (x, y) in [(5, 7), (8, 6), (11, 8), (6, 10), (9, 9), (8, 12), (4, 9), (10, 11)]:
        cv.set(x, y, hex2rgb("#f7e27a"))
    cv.poly([(4, 4), (7, 2), (8, 2), (11, 4), (8, 5), (7, 5)], leaf)
    cv.rect(7, 1, 8, 2, shade(leaf, 0.7))


def t_leafy(cv, c, seed):
    a, b = c[0], c[1]
    cv.ellipse(1, 3, 14, 14, a)
    cv.finish()
    cv.line([(8, 13), (8, 5)], shade(b, 1.2))
    cv.line([(8, 10), (4, 6)], shade(b, 1.2))
    cv.line([(8, 9), (12, 5)], shade(b, 1.2))
    cv.line([(8, 12), (3, 10)], b)
    cv.line([(8, 12), (13, 10)], b)


def t_bulb(cv, c, seed):
    a, b = c[0], c[1]
    cv.ellipse(3, 6, 12, 15, a)
    cv.poly([(5, 8), (10, 8), (8, 3), (7, 3)], a)
    cv.finish()
    cv.line([(7, 7), (6, 13)], b)
    cv.line([(9, 7), (10, 13)], b)
    cv.rect(7, 1, 8, 3, hex2rgb("#7fae4f"))
    cv.set(6, 0, hex2rgb("#7fae4f")); cv.set(9, 0, hex2rgb("#7fae4f"))
    cv.rect(6, 15, 9, 15, shade(a, 0.6))


def t_grains(cv, c, seed):
    a, b = c[0], c[1]
    rnd = random.Random(seed)
    spots = []
    for _ in range(40):
        x = rnd.randint(2, 12); y = rnd.randint(4, 12)
        if (x - 7.5) ** 2 / 36 + (y - 9) ** 2 / 16 > 1:
            continue
        spots.append((x, y))
    for (x, y) in spots[:16]:
        cv.rect(x, y, x + 1, y, a)
        cv.set(x, y + 1, b)
    cv.finish(outline=False)
    for (x, y) in spots[:16]:
        cv.set(x + 1, y + 1, shade(b, 0.7))


def t_cob(cv, c, seed):
    a, husk = c[0], c[1]
    cv.poly([(3, 13), (5, 15), (13, 6), (12, 2), (9, 3)], a)
    cv.finish()
    for i in range(0, 12, 2):
        for j in range(-2, 3, 2):
            x = 5 + i * 0.6 + j * 0.5; y = 12 - i * 0.8 + j * 0.5
            cv.set(int(x), int(y), shade(a, 0.75))
    cv.poly([(1, 15), (3, 9), (6, 12), (5, 15)], husk)
    cv.poly([(1, 15), (8, 15), (6, 12)], shade(husk, 0.8))


def t_pepper(cv, c, seed):
    a, stem = c[0], c[1]
    cv.ellipse(2, 4, 13, 15, a)
    cv.finish()
    cv.line([(8, 6), (8, 14)], shade(a, 0.75))
    cv.set(5, 7, shade(a, 1.5)); cv.set(5, 8, shade(a, 1.3))
    if len(c) > 2:  # stuffed pepper: show filling on top
        cv.ellipse(4, 3, 11, 6, c[1])
        speckle(cv, box(4, 3, 11, 6), [c[2], shade(c[1], 0.8)], 6, seed)
        cv.rect(7, 1, 8, 3, hex2rgb("#2e6b22"))
    else:
        cv.rect(7, 1, 8, 4, stem)
        cv.rect(6, 4, 9, 4, shade(stem, 0.8))


def t_chili(cv, c, seed):
    a, stem = c[0], c[1]
    cv.poly([(2, 14), (3, 15), (9, 11), (12, 6), (11, 4), (8, 5), (5, 10)], a)
    cv.finish()
    cv.line([(10, 4), (12, 1)], stem, 2)
    cv.set(8, 7, shade(a, 1.5)); cv.set(7, 8, shade(a, 1.4))


def t_long(cv, c, seed):
    a, b = c[0], c[1]
    cv.poly([(2, 12), (4, 15), (14, 5), (12, 2)], a)
    cv.ellipse(1, 10, 6, 15, a)
    cv.ellipse(10, 1, 14, 6, a)
    cv.finish()
    speckle(cv, box(3, 4, 12, 13), [shade(a, 1.3)], 6, seed)
    cv.poly([(11, 1), (14, 0), (15, 3), (13, 3)], b)


def t_leaves(cv, c, seed):
    a, b = c[0], c[1]
    cv.ellipse(1, 6, 9, 15, a)
    cv.ellipse(6, 1, 14, 10, b)
    cv.finish()
    cv.line([(2, 14), (8, 7)], shade(a, 1.3))
    cv.line([(7, 9), (13, 2)], shade(b, 1.3))


def t_seeds(cv, c, seed):
    a = c[0]
    pts = [(3, 3), (9, 2), (12, 6), (6, 7), (10, 10), (2, 10), (6, 12), (12, 13)]
    for (x, y) in pts:
        cv.set(x, y, shade(a, 1.35))
        cv.set(x + 1, y, a)
        cv.set(x, y + 1, a)
        cv.set(x + 1, y + 1, shade(a, 0.55))
        cv.set(x + 2, y + 1, shade(a, 0.4))
        cv.set(x + 1, y + 2, shade(a, 0.4))


def t_sack(cv, c, seed):
    a, b = c[0], c[1]
    cv.ellipse(2, 5, 13, 15, a)
    cv.poly([(5, 6), (10, 6), (11, 2), (4, 2)], a)
    cv.finish()
    cv.rect(5, 5, 10, 5, hex2rgb("#8b5a2b"))
    speckle(cv, box(4, 8, 11, 13), [b], 5, seed)


def t_blob(cv, c, seed):
    a, b = c[0], c[1]
    cv.ellipse(1, 5, 14, 14, a)
    cv.finish()
    speckle(cv, box(3, 7, 12, 12), [b], 6, seed)


def t_noodles(cv, c, seed):
    a, b = c[0], c[1]
    for i in range(6):
        cv.line([(2 + i, 14), (8 + i, 1)], a if i % 2 == 0 else b)
    cv.finish()
    cv.rect(4, 7, 12, 8, hex2rgb("#c8281c"))


def t_wedge(cv, c, seed):
    a, b = c[0], c[1]
    cv.poly([(1, 13), (14, 13), (14, 7), (6, 3)], a)
    cv.finish()
    cv.poly([(2, 12), (13, 12), (13, 8), (6, 5)], a)
    for (x, y) in [(5, 10), (9, 9), (11, 11), (8, 11)]:
        cv.set(x, y, b); cv.set(x + 1, y, shade(b, 0.8))
    cv.rect(1, 13, 14, 14, shade(a, 0.6))


def t_mince(cv, c, seed):
    a, b = c[0], c[1]
    cv.ellipse(1, 4, 14, 14, a)
    cv.finish()
    speckle(cv, box(2, 5, 13, 13), [b, shade(a, 0.8), hex2rgb("#f2e6e0")], 30, seed)


def t_flat(cv, c, seed):
    a, b, d = c[0], c[1], c[2]
    cv.ellipse(0, 3, 15, 14, a)
    cv.finish()
    cv.ellipse(2, 5, 13, 12, b)
    speckle(cv, box(3, 5, 12, 12), [d, shade(b, 0.8), a], 14, seed)


def t_pizza(cv, c, seed):
    a, b, d = c[0], c[1], c[2]
    cv.ellipse(0, 1, 15, 15, a)
    cv.finish()
    cv.ellipse(2, 3, 13, 13, b)
    speckle(cv, box(3, 4, 12, 12), [d, d, shade(d, 0.9)], 18, seed)
    speckle(cv, box(3, 4, 12, 12), [hex2rgb("#3f8f2f")], 5, seed + 1)


def t_cube(cv, c, seed):
    a, b = c[0], c[1]
    cv.poly([(2, 6), (8, 3), (14, 6), (14, 12), (8, 15), (2, 12)], a)
    cv.finish()
    cv.poly([(8, 9), (14, 6), (14, 12), (8, 15)], shade(a, 0.85))
    cv.poly([(2, 6), (8, 9), (8, 15), (2, 12)], b)
    cv.line([(2, 6), (8, 9), (14, 6)], shade(a, 0.7))


def t_bar(cv, c, seed):
    a, b = c[0], c[1]
    cv.rect(3, 1, 12, 14, a)
    cv.finish()
    for y in (5, 9):
        cv.line([(4, y), (11, y)], b)
    cv.line([(7, 2), (7, 13)], b)
    cv.rect(3, 10, 12, 14, hex2rgb("#c8281c"))
    cv.line([(3, 10), (12, 10)], hex2rgb("#f2e6e0"))


def t_sausage(cv, c, seed):
    a, b = c[0], c[1]
    cv.line([(3, 12), (12, 3)], a, 5)
    cv.ellipse(1, 9, 6, 14, a)
    cv.ellipse(9, 1, 14, 6, a)
    cv.finish()
    cv.line([(5, 9), (9, 5)], shade(a, 1.3))
    cv.set(1, 14, b); cv.set(14, 1, b)


def t_patty(cv, c, seed):
    a, b = c[0], c[1]
    cv.ellipse(1, 4, 14, 12, a)
    cv.rect(1, 8, 14, 10, shade(a, 0.8))
    cv.ellipse(1, 6, 14, 14, shade(a, 0.8))
    cv.ellipse(1, 3, 14, 11, a)
    cv.finish()
    speckle(cv, box(3, 4, 12, 9), [b, shade(a, 1.2)], 10, seed)


def t_fries(cv, c, seed):
    fry, box_c = c[0], c[1]
    for i, x in enumerate(range(3, 13, 2)):
        top = 1 + (i * 3) % 4
        cv.rect(x, top, x, 9, fry)
        cv.rect(x + 1, top + 1, x + 1, 9, shade(fry, 0.85))
    cv.poly([(2, 7), (13, 7), (12, 15), (3, 15)], box_c)
    cv.finish()
    cv.rect(6, 10, 9, 12, hex2rgb("#f5d14a"))


def t_wrap(cv, c, seed):
    a, f1, f2 = c[0], c[1], c[2]
    cv.line([(3, 13), (11, 5)], a, 7)
    cv.ellipse(8, 1, 15, 8, a)
    cv.ellipse(0, 9, 6, 15, a)
    cv.finish()
    cv.ellipse(9, 2, 14, 7, f1)
    speckle(cv, box(9, 2, 14, 7), [f2, shade(f1, 0.8), hex2rgb("#e0412f")], 8, seed)
    cv.line([(4, 11), (10, 5)], shade(a, 0.8))


def t_taco(cv, c, seed):
    a, f1, f2 = c[0], c[1], c[2]
    cv.ellipse(2, 3, 13, 11, f2)
    for y in range(8, 16):
        for x in range(16):
            cv.set(x, y, (0, 0, 0), 0)
    shell = Canvas()
    shell.ellipse(0, 0, 15, 15, a)
    for y in range(0, 7):
        for x in range(16):
            shell.set(x, y, (0, 0, 0), 0)
    cv.img.alpha_composite(shell.img)
    cv.px = cv.img.load()
    cv.finish()
    speckle(cv, box(2, 3, 13, 7), [f1, f2, hex2rgb("#e0412f"), hex2rgb("#f5c842")], 14, seed)


def t_burger(cv, c, seed):
    bun, patty, mid = c[0], c[1], c[2]
    cv.ellipse(1, 1, 14, 9, bun)
    cv.rect(1, 6, 14, 7, hex2rgb("#5fae45"))
    cv.rect(1, 7, 14, 8, mid)
    cv.rect(1, 9, 14, 10, patty)
    cv.rect(2, 11, 13, 11, hex2rgb("#e0412f"))
    cv.ellipse(1, 9, 14, 14, bun)
    cv.rect(1, 9, 14, 10, patty)
    cv.finish()
    for (x, y) in [(4, 3), (7, 2), (10, 3), (6, 4), (9, 4)]:
        cv.set(x, y, hex2rgb("#fff3d0"))


def t_hotdog(cv, c, seed):
    bun, saus, mus = c[0], c[1], c[2]
    cv.line([(2, 12), (12, 3)], saus, 4)
    cv.ellipse(0, 10, 4, 14, saus); cv.ellipse(11, 1, 15, 5, saus)
    cv.line([(4, 13), (13, 5)], bun, 5)
    cv.finish()
    for i in range(0, 9, 2):
        cv.set(4 + i, 10 - i, mus); cv.set(5 + i, 10 - i, mus)


def t_skewer(cv, c, seed):
    stick = hex2rgb("#8b5a2b")
    cv.line([(1, 14), (14, 1)], stick, 1)
    cols = [c[0], c[1], c[0], c[2], c[0]]
    for i, col in enumerate(cols):
        x = 3 + i * 2; y = 12 - i * 2
        cv.ellipse(x - 2, y - 2, x + 1, y + 1, col)
    cv.finish()


def t_balls(cv, c, seed):
    a, b = c[0], c[1]
    for (x, y) in [(1, 7), (7, 8), (4, 2)]:
        cv.ellipse(x, y, x + 7, y + 6, a)
    cv.finish()
    speckle(cv, box(1, 2, 14, 14), [b, shade(a, 1.3)], 12, seed)


def t_bowl(cv, c, seed):
    bowl = hex2rgb("#8b5a2b")
    a, b, d = c[0], c[1], c[2]
    cv.ellipse(1, 4, 14, 10, a)
    cv.poly([(1, 8), (14, 8), (12, 13), (10, 14), (5, 14), (3, 13)], bowl)
    cv.finish()
    cv.ellipse(2, 5, 13, 9, a)
    speckle(cv, box(3, 5, 12, 8), [b, b, d, shade(a, 0.85)], 16, seed)
    cv.line([(2, 9), (13, 9)], shade(bowl, 1.3))
    cv.line([(4, 11), (11, 11)], shade(bowl, 0.8))


def t_bottle(cv, c, seed):
    glass = hex2rgb("#cfe6f0")
    liq = c[0]
    cv.rect(6, 1, 9, 2, hex2rgb("#8b5a2b"))
    cv.rect(6, 3, 9, 5, glass)
    cv.ellipse(2, 5, 13, 15, glass)
    cv.finish()
    cv.ellipse(3, 8, 12, 14, liq)
    cv.rect(4, 8, 11, 9, liq)
    cv.set(4, 7, (255, 255, 255)); cv.set(4, 6, (255, 255, 255))


def t_tea_glass(cv, c, seed):
    glass = hex2rgb("#e6f2f6")
    liq = c[0]
    cv.ellipse(1, 12, 14, 15, hex2rgb("#d9d9d9"))
    cv.poly([(4, 2), (11, 2), (10, 6), (11, 11), (9, 13), (6, 13), (4, 11), (5, 6)], glass)
    cv.finish()
    cv.poly([(5, 4), (10, 4), (9, 6), (10, 11), (9, 12), (6, 12), (5, 11), (6, 6)], liq)
    cv.set(6, 5, shade(liq, 1.6))


def t_cup(cv, c, seed):
    cup = hex2rgb("#f4f4f4")
    liq = c[0]
    cv.ellipse(0, 11, 15, 15, hex2rgb("#d8d8d8"))
    cv.poly([(3, 4), (12, 4), (11, 12), (4, 12)], cup)
    cv.ellipse(11, 6, 15, 10, cup)
    cv.finish()
    cv.set(13, 8, (0, 0, 0), 0)
    cv.rect(4, 4, 11, 5, liq)
    cv.line([(5, 2), (6, 0)], hex2rgb("#e8e8e8"))
    cv.line([(9, 2), (10, 0)], hex2rgb("#e8e8e8"))


def t_boat(cv, c, seed):
    a, b, d = c[0], c[1], c[2]
    cv.poly([(0, 15), (4, 11), (11, 4), (15, 0), (13, 6), (6, 13)], a)
    cv.ellipse(3, 3, 12, 12, a)
    cv.finish()
    cv.ellipse(5, 5, 10, 10, b)
    speckle(cv, box(5, 5, 10, 10), [d, shade(b, 0.8)], 7, seed)


def t_rolls(cv, c, seed):
    a, b, d = c[0], c[1], c[2]
    for (x, y) in [(1, 8), (5, 3)]:
        cv.line([(x, y + 4), (x + 8, y)], a, 5)
    cv.finish()
    for (x, y) in [(10, 3), (6, 8)]:
        cv.ellipse(x - 1, y - 2, x + 3, y + 2, b)
        cv.set(x + 1, y, d)


def t_pastry(cv, c, seed):
    a, b, d = c[0], c[1], c[2]
    cv.poly([(1, 8), (8, 3), (15, 8), (8, 13)], a)
    cv.rect(1, 8, 15, 10, shade(a, 0.75))
    cv.poly([(1, 10), (8, 15), (15, 10), (8, 13)], shade(a, 0.75))
    cv.poly([(1, 8), (8, 3), (15, 8), (8, 13)], a)
    cv.finish()
    cv.line([(4, 8), (8, 5), (12, 8)], b)
    speckle(cv, box(5, 6, 11, 10), [d], 5, seed)


def t_ring(cv, c, seed):
    a, sesame = c[0], c[1]
    cv.ellipse(1, 1, 14, 14, a)
    cv.finish()
    for y in range(5, 11):
        for x in range(5, 11):
            if (x - 7.5) ** 2 + (y - 7.5) ** 2 <= 7:
                cv.set(x, y, (0, 0, 0), 0)
    speckle(cv, box(1, 1, 14, 14), [sesame], 16, seed)


def t_kumpir(cv, c, seed):
    a, b, d = c[0], c[1], c[2]
    cv.ellipse(1, 5, 14, 15, a)
    cv.finish()
    cv.ellipse(3, 3, 12, 10, b)
    speckle(cv, box(3, 3, 12, 10), [d, hex2rgb("#f2c62e"), hex2rgb("#3f8f2f"), shade(b, 0.8)], 16, seed)


def t_slice(cv, c, seed):
    a, b, d = c[0], c[1], c[2]
    cv.poly([(1, 9), (11, 3), (15, 6), (15, 11), (5, 15), (1, 13)], a)
    cv.finish()
    cv.line([(1, 11), (15, 8)], b, 1)
    cv.line([(2, 13), (15, 10)], d, 1)
    cv.poly([(2, 9), (11, 4), (14, 6), (5, 11)], shade(b, 1.1))


def t_popcorn(cv, c, seed):
    pop, red = c[0], c[1]
    cv.poly([(2, 6), (13, 6), (11, 15), (4, 15)], (255, 255, 255))
    for x in (4, 7, 10):
        cv.line([(x, 6), (x + (1 if x < 7 else (0 if x == 7 else -1)), 15)], red, 2)
    for (x, y) in [(3, 3), (6, 1), (9, 2), (11, 4), (5, 4), (8, 4)]:
        cv.ellipse(x, y, x + 3, y + 3, pop)
    cv.finish()


def t_stack(cv, c, seed):
    a, b, syrup = c[0], c[1], c[2]
    for i, y in enumerate((10, 7, 4)):
        cv.ellipse(1, y, 14, y + 5, b)
        cv.ellipse(1, y - 1, 14, y + 3, a)
    cv.finish()
    cv.ellipse(5, 3, 10, 5, hex2rgb("#fff2b0"))
    cv.poly([(3, 5), (12, 5), (11, 9), (9, 7), (6, 9)], syrup)


def t_pie(cv, c, seed):
    crust, dark, fill = c[0], c[1], c[2]
    cv.ellipse(0, 3, 15, 14, crust)
    cv.finish()
    cv.ellipse(2, 5, 13, 12, fill)
    for x in (4, 7, 10):
        cv.line([(x, 5), (x, 12)], crust)
    for y in (7, 10):
        cv.line([(2, y), (13, y)], crust)


def t_nachos(cv, c, seed):
    a, b, d = c[0], c[1], c[2]
    for (pts) in [[(1, 13), (6, 4), (9, 13)], [(5, 14), (11, 6), (14, 14)], [(3, 10), (10, 2), (12, 10)]]:
        cv.poly(pts, a)
    cv.finish()
    speckle(cv, box(2, 4, 13, 13), [b, b, d], 12, seed)


def t_sushi(cv, c, seed):
    rice, fish, nori = c[0], c[1], c[2]
    for (x, y) in [(0, 6), (7, 1)]:
        cv.ellipse(x, y, x + 8, y + 8, nori)
        cv.ellipse(x + 1, y + 1, x + 7, y + 7, rice)
        cv.ellipse(x + 3, y + 3, x + 5, y + 5, fish)
    cv.finish(outline=False)


def t_onigiri(cv, c, seed):
    rice, nori = c[0], c[1]
    cv.poly([(8, 1), (15, 13), (14, 15), (1, 15), (0, 13)], rice)
    cv.finish()
    cv.rect(5, 10, 10, 15, nori)


def t_dumplings(cv, c, seed):
    a, b = c[0], c[1]
    for (x, y) in [(0, 7), (7, 8), (4, 2)]:
        cv.ellipse(x, y, x + 8, y + 7, a)
        for yy in range(y + 5, y + 8):
            for xx in range(x, x + 9):
                cv.set(xx, yy, (0, 0, 0), 0)
        cv.rect(x + 1, y + 4, x + 7, y + 5, a)
    cv.finish()
    for (x, y) in [(0, 7), (7, 8), (4, 2)]:
        for i in range(2, 7, 2):
            cv.set(x + i, y + 1, b)


def t_triangle(cv, c, seed):
    a, b = c[0], c[1]
    cv.poly([(8, 1), (15, 14), (1, 14)], a)
    cv.finish()
    cv.line([(8, 3), (8, 12)], b)
    speckle(cv, box(4, 6, 12, 12), [shade(a, 1.2)], 6, seed)


def t_crescent(cv, c, seed):
    a, b = c[0], c[1]
    cv.ellipse(0, 3, 15, 14, a)
    cv.finish()
    for y in range(9, 16):
        for x in range(4, 12):
            if (x - 7.5) ** 2 / 16 + (y - 14) ** 2 / 9 <= 1:
                cv.set(x, y, (0, 0, 0), 0)
    for x in (4, 7, 10):
        cv.line([(x, 4), (x + 1, 10)], b)


def t_loaf(cv, c, seed):
    a, b = c[0], c[1]
    cv.line([(2, 13), (13, 2)], a, 6)
    cv.ellipse(0, 9, 6, 15, a); cv.ellipse(9, 0, 15, 6, a)
    cv.finish()
    for i in range(3):
        x = 4 + i * 3; y = 10 - i * 3
        cv.line([(x, y), (x + 2, y - 1)], b)


def t_crepe(cv, c, seed):
    a, choc = c[0], c[1]
    cv.poly([(1, 14), (14, 14), (14, 3)], a)
    cv.finish()
    cv.line([(4, 13), (13, 5)], choc, 2)
    cv.line([(8, 14), (14, 9)], choc, 1)


def t_sticks(cv, c, seed):
    a, b = c[0], c[1]
    for (x0, y0, x1, y1) in [(2, 14, 9, 1), (5, 15, 12, 2), (8, 15, 14, 4)]:
        cv.line([(x0, y0), (x1, y1)], a, 2)
    cv.finish()
    speckle(cv, box(1, 1, 14, 15), [hex2rgb("#ffffff"), b], 10, seed)


def t_plate(cv, c, seed):
    main, side, plate = c[0], c[1], c[2]
    cv.ellipse(0, 4, 15, 15, plate)
    cv.finish()
    cv.ellipse(1, 6, 9, 12, main)
    for x in (10, 11, 12, 13):
        cv.line([(x, 6), (x - 1, 12)], side)
    speckle(cv, box(2, 7, 8, 11), [shade(main, 1.2), hex2rgb("#f5c842")], 6, seed)


def t_waffle(cv, c, seed):
    a, b = c[0], c[1]
    cv.rect(1, 2, 14, 14, a)
    cv.finish()
    for i in range(3, 14, 3):
        cv.line([(i, 3), (i, 13)], b)
        cv.line([(2, i), (13, i)], b)


STYLES = {k[2:]: v for k, v in globals().items() if k.startswith("t_")}


def item_texture(style, colours, seed=0):
    cv = Canvas()
    STYLES[style](cv, [hex2rgb(x) for x in colours], seed)
    return cv.img


# ---------------------------------------------------------------------------
# crop stage textures (4 stages)
# ---------------------------------------------------------------------------

def crop_texture(plant, fruit, stage, seed=0):
    cv = Canvas()
    stem = hex2rgb("#4f9a35")
    dark = hex2rgb("#3a7a26")
    fruit = hex2rgb(fruit)
    rnd = random.Random(seed * 10 + stage)
    h = [4, 7, 11, 14][stage]
    if plant == "grass":
        for x in (2, 5, 8, 11, 14):
            hh = h - rnd.randint(0, 2)
            cv.line([(x, 15), (x + rnd.choice((-1, 0, 1)), 15 - hh)], stem if x % 2 else dark)
        if stage == 3:
            for x in (2, 8, 14):
                cv.rect(x - 1, 3, x, 6, fruit)
    elif plant == "head":
        if stage < 2:
            for x in (4, 8, 12):
                cv.line([(x, 15), (x - 1, 15 - h)], stem)
                cv.set(x - 2, 15 - h, stem); cv.set(x, 15 - h, stem)
        else:
            r = 3 if stage == 2 else 5
            for cx in (4, 11):
                cv.ellipse(cx - r, 15 - 2 * r, cx + r, 15, dark)
                cv.ellipse(cx - r + 1, 15 - 2 * r + 1, cx + r - 1, 15, fruit if stage == 3 else stem)
    elif plant == "bulb":
        for x in (3, 6, 9, 12):
            cv.line([(x, 15), (x + rnd.choice((-1, 1)), 15 - h)], stem)
        if stage == 3:
            for x in (3, 9):
                cv.ellipse(x - 1, 12, x + 3, 15, fruit)
    else:  # bush
        for x in (3, 8, 13):
            cv.line([(x, 15), (x, 15 - h)], dark)
            for y in range(15 - h, 16, 2):
                cv.set(x - 1, y, stem); cv.set(x + 1, y - 1, stem)
        if stage >= 2:
            for x in (3, 8, 13):
                cv.ellipse(x - 2, 15 - h, x + 2, 15 - h + 4, stem)
        if stage == 3:
            for (x, y) in [(2, 6), (7, 4), (12, 7), (4, 10), (10, 11), (13, 3)]:
                cv.rect(x, y, x + 1, y + 1, fruit)
    return cv.img


def icon_texture():
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    big = item_texture("bowl", ["#e88a2f", "#f0a24a", "#3f8f2f"], 3).resize((96, 96), Image.NEAREST)
    pizza = item_texture("pizza", ["#d9a55e", "#c8281c", "#f5e08a"], 4).resize((64, 64), Image.NEAREST)
    img.alpha_composite(big, (0, 32))
    img.alpha_composite(pizza, (64, 0))
    return img
