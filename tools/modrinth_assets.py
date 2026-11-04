#!/usr/bin/env python3
"""Builds the Modrinth listing images into modrinth/ (logo + catalogue gallery images).

    python3 tools/generate.py && python3 tools/modrinth_assets.py

In-game screenshots come from the showcase client test:
    WORLDFOODS_SHOWCASE=1 xvfb-run -a -s "-screen 0 1920x1080x24" ./gradlew runClientGameTest -PclientTests
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from content import CROPS, CUISINES, FOODS  # noqa: E402
import textures  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", "worldfoods")
OUT = os.path.join(ROOT, "modrinth")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

LANG_EN = json.load(open(f"{ASSETS}/lang/en_us.json", encoding="utf-8"))
LANG_TR = json.load(open(f"{ASSETS}/lang/tr_tr.json", encoding="utf-8"))


def tex(name):
    return Image.open(f"{ASSETS}/textures/item/{name}.png").convert("RGBA")


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def background(w, h):
    img = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(img)
    top, bottom = (58, 36, 24), (28, 18, 12)
    for y in range(h):
        t = y / (h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)) + (255,))
    return img


def header(img, title, subtitle):
    d = ImageDraw.Draw(img)
    logo = textures.logo(96, tex)
    img.alpha_composite(logo, (48, 36))
    d.text((168, 40), title, font=font(54, True), fill=(255, 236, 200))
    d.text((170, 104), subtitle, font=font(26), fill=(240, 190, 140))


def card(img, x, y, w, h, item, line1, line2, badge=None):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rounded_rectangle([x, y, x + w, y + h], radius=14, fill=(255, 255, 255, 20),
                                              outline=(255, 220, 170, 70), width=2)
    img.alpha_composite(overlay)
    d = ImageDraw.Draw(img)
    icon = tex(item).resize((64, 64), Image.NEAREST)
    img.alpha_composite(icon, (x + 12, y + (h - 64) // 2))
    tw = w - 100
    d.text((x + 88, y + 10), line1, font=fit_font(line1, 21, tw, True), fill=(255, 240, 215))
    d.text((x + 88, y + 38), line2, font=fit_font(line2, 16, tw, False), fill=(225, 195, 155))
    if badge:
        bf = font(14, True)
        bw = d.textlength(badge, font=bf) + 14
        d.rounded_rectangle([x + 88, y + h - 28, x + 88 + bw, y + h - 8], radius=7, fill=(217, 67, 43))
        d.text((x + 95, y + h - 26), badge, font=bf, fill=(255, 255, 255))


def fit_font(text, size, width, bold):
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    while size > 11 and probe.textlength(text, font=font(size, bold)) > width:
        size -= 1
    return font(size, bold)


def catalogue(items, title, subtitle, path, cols=5, card_h=92):
    w = 1920
    rows = (len(items) + cols - 1) // cols
    h = max(1080, 180 + rows * (card_h + 14) + 30)
    img = background(w, h)
    header(img, title, subtitle)
    cw = (w - 96 - (cols - 1) * 16) // cols
    for i, (item, l1, l2, badge) in enumerate(items):
        x = 48 + (i % cols) * (cw + 16)
        y = 180 + (i // cols) * (card_h + 14)
        card(img, x, y, cw, card_h, item, l1, l2, badge)
    img.convert("RGB").save(path, optimize=True)
    return img.size


def crops_image(path):
    """Each crop with its seeds and all four growth stages."""
    w, h = 1920, 1080
    img = background(w, h)
    header(img, "17 new crops", "Seeds drop from grass · plant on farmland · 4 growth stages  ·  17 yeni ekin")
    cols, card_h, cw = 3, 132, (1920 - 96 - 32) // 3
    for i, c in enumerate(CROPS):
        x = 48 + (i % cols) * (cw + 16)
        y = 176 + (i // cols) * (card_h + 12)
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(overlay).rounded_rectangle([x, y, x + cw, y + card_h], radius=14, fill=(255, 255, 255, 20),
                                                  outline=(255, 220, 170, 70), width=2)
        img.alpha_composite(overlay)
        d = ImageDraw.Draw(img)
        img.alpha_composite(tex(c["produce"]).resize((64, 64), Image.NEAREST), (x + 12, y + 12))
        img.alpha_composite(tex(c["id"] + "_seeds").resize((32, 32), Image.NEAREST), (x + 28, y + 84))
        d.text((x + 88, y + 12), c["en"], font=font(22, True), fill=(255, 240, 215))
        d.text((x + 88, y + 42), c["tr"], font=font(17), fill=(225, 195, 155))
        for st in range(4):
            stage = Image.open(f"{ASSETS}/textures/block/{c['id']}_crop_stage{st}.png").convert("RGBA")
            sx = x + 88 + st * 92
            ImageDraw.Draw(img).rectangle([sx, y + 70, sx + 79, y + 120], fill=(92, 60, 38))
            img.alpha_composite(stage.resize((80, 80), Image.NEAREST).crop((0, 30, 80, 80)), (sx, y + 70))
    img.convert("RGB").save(path, optimize=True)
    return img.size


def main():
    os.makedirs(f"{OUT}/gallery", exist_ok=True)

    textures.logo(512, tex).save(f"{OUT}/icon.png")

    dishes = [f for f in FOODS if "cuisine" in f or f["id"] in
              ("fruit_salad", "cheesecake", "strawberry_ice_cream", "hot_chocolate", "strawberry_milkshake", "latte")]
    order = list(CUISINES)
    dishes.sort(key=lambda f: order.index(f["cuisine"]) if "cuisine" in f else len(order))

    def dish_row(f):
        cu = CUISINES.get(f.get("cuisine"), ("Desserts & drinks", "Tatlı & içecek"))
        return (f["id"], f["en"], f"{f['tr']}  ·  {cu[0]}", f"+{f['food'][0]} hunger")

    half = 40
    print("dishes-1", catalogue([dish_row(f) for f in dishes[:half]], "World Foods",
                                f"{len(dishes)} real-world dishes  ·  Dünya mutfağından {len(dishes)} yemek",
                                f"{OUT}/gallery/08-dishes-1.png"))
    print("dishes-2", catalogue([dish_row(f) for f in dishes[half:]], "World Foods",
                                "Turkish, Italian, Japanese, Mexican, Indian, French, Spanish and more",
                                f"{OUT}/gallery/09-dishes-2.png"))

    print("crops", crops_image(f"{OUT}/gallery/10-crops.png"))

    ingredients = [f for f in FOODS if "cuisine" not in f and f["id"] not in
                   ("fruit_salad", "cheesecake", "strawberry_ice_cream", "hot_chocolate", "strawberry_milkshake", "latte")]
    ing = [(f["id"], f["en"], f["tr"], None) for f in ingredients]
    print("ingredients", catalogue(ing, "Ingredients", "Flour, dough, cheese, yogurt, minced meat...  ·  Malzemeler",
                                   f"{OUT}/gallery/11-ingredients.png", cols=3, card_h=104))


if __name__ == "__main__":
    main()
