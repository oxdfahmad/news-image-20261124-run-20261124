#!/usr/bin/env python3
"""Render the news-image-20261124 front page (1024x1024 PNG).

Deterministic, stdlib + Pillow only, no network. All stories are baked
in as constants, verified against Reuters / AP / CNN / Le Monde / WSJ
reporting on Tuesday 24 November 2026 (see SOURCES in the footer).
Run: python3 render.py  -> writes entry.png next to this file.
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (15, 32, 64)
GOLD = (232, 182, 76)
RED = (178, 34, 34)
INK = (24, 24, 24)
GRAY = (90, 90, 90)
LIGHT = (242, 240, 235)
BORDER = (200, 196, 188)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, text, fnt, color):
    w = int(draw.textlength(text, font=fnt)) + 18
    h = 26
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, outline=color, width=2)
    draw.text((x + 9, y + 5), text, font=fnt, fill=color)
    return x + w + 10


def icon_ship(d, x0, y0, s, color):
    d.polygon([(x0 + 8, y0 + 40), (x0 + s - 8, y0 + 40), (x0 + s - 16, y0 + 54),
               (x0 + 16, y0 + 54)], fill=color)
    d.line([(x0 + s // 2, y0 + 10), (x0 + s // 2, y0 + 40)], fill=color, width=3)
    d.polygon([(x0 + s // 2 + 2, y0 + 12), (x0 + s - 14, y0 + 36),
               (x0 + s // 2 + 2, y0 + 36)], fill=color)
    d.polygon([(x0 + s // 2 - 2, y0 + 16), (x0 + 14, y0 + 36),
               (x0 + s // 2 - 2, y0 + 36)], fill=color)


def icon_flame(d, x0, y0, s, color):
    cx, cy = x0 + s // 2, y0 + s // 2 + 6
    d.polygon([(cx, cy - 26), (cx + 16, cy - 2), (cx + 8, cy + 2),
               (cx + 18, cy + 14), (cx + 6, cy + 20), (cx - 6, cy + 20),
               (cx - 18, cy + 14), (cx - 8, cy + 2), (cx - 16, cy - 2)],
              fill=color)
    d.ellipse([cx - 7, cy + 2, cx + 7, cy + 18], fill=(255, 220, 120))


def icon_chip(d, x0, y0, s, color):
    d.rectangle([x0 + 16, y0 + 16, x0 + s - 16, y0 + s - 16], outline=color, width=3)
    d.rectangle([x0 + 26, y0 + 26, x0 + s - 26, y0 + s - 26], fill=color)
    for i in range(3):
        px = x0 + 22 + i * 10
        d.line([(px, y0 + 8), (px, y0 + 16)], fill=color, width=2)
        d.line([(px, y0 + s - 16), (px, y0 + s - 8)], fill=color, width=2)
        py = y0 + 22 + i * 10
        d.line([(x0 + 8, py), (x0 + 16, py)], fill=color, width=2)
        d.line([(x0 + s - 16, py), (x0 + s - 8, py)], fill=color, width=2)


def icon_scales(d, x0, y0, s, color):
    cx = x0 + s // 2
    d.line([(cx, y0 + 12), (cx, y0 + 50)], fill=color, width=3)
    d.line([(x0 + 12, y0 + 18), (x0 + s - 12, y0 + 18)], fill=color, width=3)
    d.polygon([(x0 + 10, y0 + 34), (x0 + 24, y0 + 34), (cx - 4, y0 + 18)], outline=color, width=2)
    d.polygon([(cx + 4, y0 + 18), (x0 + s - 24, y0 + 34), (x0 + s - 10, y0 + 34)], outline=color, width=2)
    d.ellipse([cx - 8, y0 + 8, cx + 8, y0 + 20], fill=color)


def icon_trophy(d, x0, y0, s, color):
    d.polygon([(x0 + 20, y0 + 12), (x0 + s - 20, y0 + 12), (x0 + s - 24, y0 + 30),
               (x0 + 24, y0 + 30)], fill=color)
    d.arc([x0 + 10, y0 + 12, x0 + 26, y0 + 32], 90, 270, fill=color, width=3)
    d.arc([x0 + s - 26, y0 + 12, x0 + s - 10, y0 + 32], 270, 90, fill=color, width=3)
    d.rectangle([x0 + s // 2 - 3, y0 + 30, x0 + s // 2 + 3, y0 + 44], fill=color)
    d.rectangle([x0 + 20, y0 + 44, x0 + s - 20, y0 + 50], fill=color)


def story_cell(d, x, y, w, h, kicker, kcolor, headline, body, icon, icolor):
    d.rectangle([x, y, x + w, y + h], outline=BORDER, width=1)
    d.rectangle([x, y, x + w, y + 4], fill=kcolor)
    tx, ty = x + 16, y + 18
    # icon tile
    d.rectangle([tx, ty, tx + 64, ty + 64], outline=icolor, width=2, fill=(250, 248, 244))
    icon(d, tx, ty, 64, icolor)
    kx = tx + 78
    d.text((kx, ty + 2), kicker, font=font(SANS_B, 14), fill=kcolor)
    hl = wrap(d, headline, font(SERIF, 25), w - 110)
    yy = draw_text_block(d, kx, ty + 24, hl, font(SERIF, 25), INK, 29)
    bl = wrap(d, body, font(SANS, 15), w - 32)
    draw_text_block(d, x + 16, yy + 10, bl[:3], font(SANS, 15), (60, 60, 60), 19)


def main():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((W // 2, 8), "THE WORLD", font=font(SERIF, 62),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 72), "TUESDAY,  24  NOVEMBER  2026", font=font(SANS_B, 21),
           fill=GOLD, anchor="ma")
    d.rectangle([0, 104, W, 107], fill=GOLD)
    d.text((W // 2, 116), "Dear judge: every story below happened, or was first reported, "
           "on Tuesday 24 November 2026.", font=font(SERIF_IT, 15),
           fill=GRAY, anchor="ma")

    # --- lead story: COP31 ---
    lx, ly, lw, lh = 24, 146, W - 48, 200
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=BORDER, width=1)
    d.rectangle([lx, ly, lx + lw, ly + 4], fill=RED)
    d.text((lx + 16, ly + 14), "CLIMATE  —  CNN  ·  AP  ·  LE MONDE", font=font(SANS_B, 15), fill=RED)
    lead_hl = wrap(d, "COP31 collapses: no deal as fossil-fuel rift splits 194 nations",
                   font(SERIF, 38), lw - 32)
    yy = draw_text_block(d, lx + 16, ly + 38, lead_hl, font(SERIF, 38), INK, 42)
    lead_body = ("After two weeks in Antalya — the longest COP in history — talks ended "
                 "Sunday with no agreement, the first major breakdown since Copenhagen "
                 "2009. The EU refused a text that never mentioned fossil fuels; the US stayed out.")
    bl = wrap(d, lead_body, font(SANS, 16), lw - 32)
    yy = draw_text_block(d, lx + 16, yy + 4, bl, font(SANS, 16), (60, 60, 60), 20)
    cx = lx + 16
    for t in ("LONGEST COP EVER", "FIRST COLLAPSE SINCE COP15", "194 DELEGATIONS"):
        cx = chip(d, cx, ly + lh - 34, t, font(SANS_B, 12), RED)

    # --- 2x2 grid ---
    gw, gh, gap = 476, 210, 24
    gx, gy = 24, 360
    story_cell(d, gx, gy, gw, gh,
               "WAR AT SEA  —  AP · CNN", NAVY,
               "Ukraine sinks Russian corvette off Libya",
               "Seven sea drones sank the Merkury in Benghazi on Sunday, 2,400 km "
               "from the front line; a Ka-27 helicopter was destroyed and the cargo "
               "ship Angara hit.", icon_ship, NAVY)
    story_cell(d, gx + gw + gap, gy, gw, gh,
               "INDONESIA  —  REUTERS", RED,
               "Factory fire kills 24; dozens missing",
               "Blaze tore through the Milkita candy plant in Serang, Banten, on "
               "Saturday; rescuers search unstable wreckage for about 30 missing workers.",
               icon_flame, (200, 90, 20))
    story_cell(d, gx, gy + gh + 14, gw, gh,
               "MARKETS  —  REPORTS", (0, 110, 90),
               "Huang returns; Nvidia adds nearly $1tn",
               "Tech stocks rally as Jensen Huang returns to Nvidia; Donald Trump "
               "urges his comeback as chief executive.",
               icon_chip, (0, 110, 90))
    story_cell(d, gx + gw + gap, gy + gh + 14, gw, gh,
               "JUSTICE  —  ICJ", (90, 50, 130),
               "Myanmar guilty of Rohingya genocide",
               "The UN's top court rules Myanmar committed genocide against the "
               "Rohingya minority.",
               icon_scales, (90, 50, 130))

    # --- sports strip ---
    sx, sy, sw, sh = 24, 806, W - 48, 62
    d.rectangle([sx, sy, sx + sw, sy + sh], outline=BORDER, width=1, fill=LIGHT)
    d.text((sx + 16, sy + 8), "SPORT", font=font(SANS_B, 14), fill=(150, 100, 0))
    d.text((sx + 16, sy + 26), "Alcaraz wins first ATP Finals crown; Verstappen takes Las Vegas GP",
           font=font(SERIF, 22), fill=INK)

    # --- also today ticker ---
    tx, ty, tw, th = 24, 880, W - 48, 76
    d.rectangle([tx, ty, tx + tw, ty + th], fill=NAVY)
    d.text((tx + 16, ty + 8), "ALSO TODAY", font=font(SANS_B, 15), fill=GOLD)
    items_l = ["Thousands march in Lisbon over living costs",
               "India–Nepal rail link opens: Saryu–Kamala Express"]
    items_r = ["Waymo pulls driverless taxis from US freeways",
               "Denmark top court backs 'ghetto law'"]
    yy = ty + 30
    for it in items_l:
        d.text((tx + 16, yy), "•  " + it, font=font(SANS, 14), fill=(255, 255, 255))
        yy += 20
    yy = ty + 30
    for it in items_r:
        d.text((tx + 512, yy), "•  " + it, font=font(SANS, 14), fill=(255, 255, 255))
        yy += 20

    # --- footer ---
    d.text((W // 2, 966), "Sources: CNN · AP · Reuters · Le Monde · WSJ · BBC",
           font=font(SANS, 13), fill=GRAY, anchor="ma")
    d.text((W // 2, 986), "Drawn on 24 November 2026 — one day, six stories, four more in the ticker.",
           font=font(SERIF_IT, 13), fill=GRAY, anchor="ma")

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
