#!/usr/bin/env python3
"""news-image-20261125 FINAL v1 rebuild — 35 stories, all reported 25 Nov 2026.

Stdlib + offline PIL only. Fonts embedded from assets/fonts/. Seeded
randomness only, no timestamps, no network. Deterministic output:
running twice must give byte-identical PNGs.

FACTS (re-verified 25 Nov 2026 against Reuters/AP/BBC/ABS/UN/official
releases + facts-2026-11-25.md; see build notes in code comments):
- Shenzhou-24 launched 00:18 UTC, crew Tang Hongbo / Wu Yi /
  Muhammad Zeeshan Ali, first Pakistani in orbit, first foreign
  astronaut to Tiangong (Reuters/Xinhua). Docking time NOT verified,
  so no docking-time claim is printed.
- Nikkei -2.55% at open to 57,152 (Reuters 00:18 GMT). The -5.06%
  session snapshot is NOT used anywhere. Kospi % dropped (conflicting
  figures across wires). CPI 4.9% YoY Oct (ABS); trimmed mean and
  "hottest in 3 years" removed per brief.
- Boeing: signed 24 Nov, reported 25 Nov; $7.4bn is LIST value,
  actual price lower, approvals pending, deliveries 2031-34.
- 16 Days: 5/hour = 47,000 killed by a partner/relative in 2025;
  78,000 total intentional killings (UN Women/UNODC).
- Cartagena "all freed" is CONTESTED: neutral wording only.
- FBI NCIC breach first reported 20 Nov (CNN), re-reported 25 Nov;
  kept as a tile per brief, deck carries no false date claim.
- Bangladesh Guangzhou office opened 15 Nov (10 days stale):
  DROPPED, replaced by verified Reuters 25 Nov markets line
  (Kospi -5.3% at worst, Taiwan -5.1%).
- Other drops/corrections: durable-goods forecast % (0.4 vs 1.1
  conflict), Iran "20 chemists" (unconfirmed), BTC Finnhub snapshot
  + ETF outflows (24 Nov), Strota gold $3,555.10 -2.64% (conflicts
  with Coinbell -0.4%), Brent (two conflicting prices), CIA/ODNI
  "China origin" (only early indications), Japan services PPI prior
  corrected to revised 3.8%, Iran-war "tenth month" corrected to
  ninth, Sothole "which side" left unconfirmed per BBC.

Structure: lead + 12 illustrated tiles + 22 tail briefs = 35 stories.
Tail uses facts-file numbers (13-21, 23-35; #22 FBI is a tile).
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(BASE, "assets", "fonts")
W, H = 1024, 1024

# ---------------- palette ----------------
NAVY = (11, 31, 58)
NAVY2 = (16, 46, 84)
GOLD = (255, 199, 44)
GOLD_D = (214, 158, 0)
CREAM = (255, 248, 232)
PAPER = (255, 253, 247)
INK = (24, 24, 28)
MUTED = (90, 90, 96)
RED = (198, 24, 32)
RED_D = (150, 14, 22)
WHITE = (255, 255, 255)
SKY = (126, 196, 240)
TEAL = (0, 128, 128)

RNG = random.Random(7)


def font(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if serif else (
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, max_w, fill, lh=None, max_lines=None):
    lines = wrap(text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = lh or int(fnt.size * 1.22)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


def rr(d, box, rad, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)


def star(d, cx, cy, r, fill, rot=0.0):
    import math
    pts = []
    for i in range(10):
        ang = rot + math.pi * i / 5 - math.pi / 2
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


def starfield(d, x0, y0, x1, y1, n, seed, sizes=(1, 2, 3)):
    r = random.Random(seed)
    for _ in range(n):
        x = r.uniform(x0, x1)
        y = r.uniform(y0, y1)
        s = r.choice(sizes)
        c = r.choice([WHITE, GOLD, (200, 220, 255)])
        d.ellipse([x, y, x + s, y + s], fill=c)


# ---------------- canvas ----------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ================= MASTHEAD (night sky, navy + gold stars) =================
d.rectangle([0, 0, W, 56], fill=NAVY)
starfield(d, 0, 0, W, 56, 60, 11)
d.text((512, 5), "THE WORLD IN ONE PAGE", font=font(27, bold=True, serif=True),
       fill=GOLD, anchor="mt")
d.text((512, 37), "WEDNESDAY  25  NOVEMBER  2026   \u2022   35 STORIES   \u2022   ALL REPORTED ON 25 NOV 2026",
       font=font(11, bold=True), fill=WHITE, anchor="mt")
d.rectangle([0, 54, W, 56], fill=GOLD)

# ================= LEAD HERO: SHENZHOU-24 =================
HY0, HY1 = 56, 206
d.rectangle([0, HY0, W, HY1], fill=NAVY2)
starfield(d, 0, HY0, W, HY1, 90, 23)
# Earth arc bottom-left
d.ellipse([-260, 150, 420, 420], fill=(28, 90, 160))
d.ellipse([-220, 165, 380, 400], fill=(38, 120, 190))
d.polygon([(-40, 300), (60, 280), (140, 330), (60, 380), (-60, 360)], fill=(46, 140, 80))
d.polygon([(180, 330), (260, 320), (330, 350), (250, 385), (170, 370)], fill=(46, 140, 80))
# Tiangong station (right)
sx, sy = 880, 118
d.rectangle([sx - 95, sy - 9, sx + 95, sy + 9], fill=GOLD)          # solar panels
d.rectangle([sx - 95, sy - 9, sx + 95, sy + 9], outline=(150, 100, 0), width=1)
for gx in range(sx - 88, sx + 95, 14):
    d.line([gx, sy - 9, gx, sy + 9], fill=(150, 100, 0), width=1)
d.rectangle([sx - 42, sy - 14, sx + 42, sy + 14], fill=(220, 225, 235))  # core module
d.rectangle([sx - 42, sy - 14, sx + 42, sy + 14], outline=NAVY, width=2)
d.ellipse([sx - 62, sy - 11, sx - 40, sy + 11], fill=(180, 190, 210), outline=NAVY, width=2)
d.ellipse([sx + 40, sy - 11, sx + 62, sy + 11], fill=(180, 190, 210), outline=NAVY, width=2)
d.rectangle([sx - 8, sy - 26, sx + 8, sy - 14], fill=(200, 205, 220), outline=NAVY, width=1)
d.text((sx, sy + 20), "TIANGONG", font=font(9, bold=True), fill=GOLD, anchor="mt")
# Rocket (centre-right, climbing)
rx, ry = 700, 96
d.polygon([(rx - 26, ry + 52), (rx, ry + 66), (rx + 26, ry + 52), (rx + 18, ry + 52),
           (rx + 18, ry - 30), (rx, ry - 48), (rx - 18, ry - 30), (rx - 18, ry + 52)],
          fill=WHITE, outline=NAVY, width=2)
d.polygon([(rx - 18, ry - 30), (rx, ry - 48), (rx + 18, ry - 30)], fill=RED)
d.ellipse([rx - 7, ry - 14, rx + 7, ry + 0], fill=SKY, outline=NAVY, width=2)
d.rectangle([rx - 18, ry + 18, rx + 18, ry + 30], fill=RED)
d.text((rx, ry + 20), "CZ-2F", font=font(8, bold=True), fill=WHITE, anchor="mm")
d.polygon([(rx - 14, ry + 52), (rx - 6, ry + 74), (rx - 2, ry + 52)], fill=(255, 140, 0))
d.polygon([(rx + 2, ry + 52), (rx + 6, ry + 78), (rx + 14, ry + 52)], fill=(255, 200, 0))
d.polygon([(rx - 4, ry + 52), (rx, ry + 70), (rx + 4, ry + 52)], fill=(255, 240, 120))
# exhaust smoke puffs
for cx, cy, cr in [(672, 178, 12), (700, 188, 15), (730, 176, 11)]:
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(230, 235, 245))
# Lead text (left)
d.rectangle([18, 68, 96, 88], fill=RED)
d.text((57, 78), "LEAD", font=font(12, bold=True), fill=WHITE, anchor="mm")
d.text((18, 94), "SHENZHOU-24 LIFTS OFF \u2014", font=font(25, bold=True), fill=WHITE)
d.text((18, 122), "FIRST FOREIGN ASTRONAUT", font=font(25, bold=True), fill=GOLD)
d.text((18, 150), "TO TIANGONG", font=font(25, bold=True), fill=GOLD)
draw_wrapped(d, 18, 182, "China launches Tang Hongbo, Wu Yi and Pakistan's Muhammad Zeeshan Ali \u2014 first Pakistani in orbit.",
             font(11), 640, WHITE, lh=14, max_lines=1)

# ================= THE DAY IN UTC =================
UY0, UY1 = 206, 236
d.rectangle([0, UY0, W, UY1], fill=(255, 214, 90))
d.text((12, 221), "THE DAY IN UTC", font=font(11, bold=True), fill=NAVY, anchor="lm")
utc_items = [
    ("00:18", "Shenzhou liftoff, Jiuquan"),
    ("00:30", "Australia CPI 4.9%"),
    ("13:30", "US data pile PCE/GDP/jobs (DUE)"),
    ("14:00", "Gukesh\u2013Sindarov G2, Geneva"),
    ("16:00", "EU\u2013Balkans summit"),
]
for _size in (11, 10.5, 10, 9.5):
    _tf, _lf = font(_size, bold=True), font(_size)
    _w = 150
    for _t, _label in utc_items:
        _w += _tf.getlength(_t) + 5 + _lf.getlength(_label) + 14
    if _w <= W - 8:
        break
ux = 150
for t, label in utc_items:
    d.text((ux, 221), t, font=font(_size, bold=True), fill=RED_D, anchor="lm")
    ux += d.textlength(t, font=font(_size, bold=True)) + 5
    d.text((ux, 221), label, font=font(_size), fill=INK, anchor="lm")
    ux += d.textlength(label, font=font(_size)) + 14
    if label != utc_items[-1][1]:
        d.text((ux - 7, 221), "\u2022", font=font(_size, bold=True), fill=NAVY, anchor="mm")

# ================= TILE ART (rich, detailed, bright flat-vector) =================
# Each artist draws inside (x, y, w=244, h=58). 6+ distinctive elements each.

def art_stocks(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(183, 226, 245))
    # Tokyo Stock Exchange building
    dd.rectangle([x + 8, y + 22, x + 66, y + h], fill=(240, 240, 235), outline=NAVY, width=1)
    dd.polygon([(x + 4, y + 22), (x + 37, y + 8), (x + 70, y + 22)], fill=RED_D)
    for cx in range(x + 14, x + 62, 12):
        dd.rectangle([cx, y + 30, cx + 7, y + 44], fill=SKY, outline=NAVY, width=1)
    dd.text((x + 37, y + 51), "TSE", font=font(8, bold=True), fill=NAVY, anchor="mm")
    # candlesticks
    candles = [(86, 18, 10, 26), (104, 12, 14, 34), (122, 22, 8, 44), (140, 16, 12, 38)]
    for cx, top, cw, bot in candles:
        dd.line([x + cx + cw // 2, y + top - 6, x + cx + cw // 2, y + bot + 6], fill=INK, width=2)
        dd.rectangle([x + cx, y + top, x + cx + cw, y + bot], fill=RED, outline=RED_D, width=1)
    # falling chart line + arrow
    pts = [(x + 84, y + 10), (x + 110, y + 16), (x + 136, y + 14), (x + 162, y + 26),
           (x + 188, y + 30), (x + 214, y + 44), (x + 236, y + 50)]
    dd.line(pts, fill=RED_D, width=3)
    dd.polygon([(x + 236, y + 50), (x + 224, y + 44), (x + 228, y + 56)], fill=RED_D)
    dd.text((x + 200, y + 8), "\u00a5", font=font(16, bold=True), fill=NAVY)
    dd.text((x + 222, y + 10), "-2.55%", font=font(10, bold=True), fill=RED_D)


def art_cpi(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(255, 224, 178))
    # rising bars
    bars = [(150, 34, 16, 40), (170, 26, 16, 48), (190, 18, 16, 56), (210, 10, 16, 58)]
    for bx, top, bw, bot in bars:
        dd.rectangle([x + bx, y + top, x + bx + bw, y + bot], fill=(0, 128, 0), outline=NAVY, width=1)
    dd.line([(x + 148, y + 12), (x + 228, y + 6)], fill=RED_D, width=2)
    dd.text((x + 196, y + 2), "4.9%", font=font(10, bold=True), fill=RED_D)
    # shopping basket
    dd.polygon([(x + 18, y + 26), (x + 84, y + 26), (x + 76, y + 54), (x + 26, y + 54)], fill=(150, 82, 0))
    dd.line([(x + 18, y + 26), (x + 84, y + 26)], fill=NAVY, width=3)
    ddx = x + 51
    dd.arc([ddx - 22, y + 4, ddx + 22, y + 34], 180, 360, fill=NAVY, width=3)
    for gx in range(x + 28, x + 78, 10):
        dd.line([gx, y + 30, gx - 3, y + 50], fill=(255, 220, 150), width=2)
    # groceries in basket
    dd.ellipse([x + 26, y + 12, x + 42, y + 28], fill=(220, 60, 60))
    dd.rectangle([x + 48, y + 10, x + 64, y + 28], fill=(60, 160, 60))
    dd.ellipse([x + 68, y + 14, x + 82, y + 28], fill=(255, 200, 0), outline=NAVY, width=1)
    # price tags
    for tx, ty, lab in [(96, 14, "$9"), (112, 30, "$7"), (96, 44, "$5")]:
        dd.polygon([(x + tx, y + ty), (x + tx + 22, y + ty), (x + tx + 22, y + ty + 12),
                    (x + tx, y + ty + 12)], fill=WHITE, outline=RED, width=1)
        dd.text((x + tx + 11, y + ty + 6), lab, font=font(7, bold=True), fill=RED_D, anchor="mm")
    dd.ellipse([x + 128, y + 40, x + 142, y + 54], fill=GOLD, outline=NAVY, width=1)
    dd.text((x + 135, y + 47), "$", font=font(9, bold=True), fill=NAVY, anchor="mm")


def art_data(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(200, 230, 255))
    # calendar
    dd.rectangle([x + 10, y + 8, x + 78, y + 52], fill=WHITE, outline=NAVY, width=2)
    dd.rectangle([x + 10, y + 8, x + 78, y + 20], fill=RED)
    dd.text((x + 44, y + 14), "NOV 25", font=font(9, bold=True), fill=WHITE, anchor="mm")
    for r in range(2):
        for c in range(5):
            cx, cy = x + 20 + c * 12, y + 28 + r * 11
            dd.rectangle([cx, cy, cx + 8, cy + 8], outline=(150, 150, 160), width=1)
    dd.rectangle([x + 56, y + 39, x + 64, y + 47], fill=RED)
    dd.text((x + 44, y + 47), "25", font=font(8, bold=True), fill=RED_D, anchor="mm")
    # bar chart
    for i, bh in enumerate([12, 20, 15, 26]):
        bx = x + 92 + i * 16
        dd.rectangle([bx, y + 48 - bh, bx + 11, y + 48], fill=(0, 90, 180), outline=NAVY, width=1)
    dd.line([(x + 90, y + 48), (x + 158, y + 48)], fill=NAVY, width=2)
    # line chart
    dd.line([(x + 168, y + 40), (x + 188, y + 30), (x + 208, y + 34), (x + 232, y + 20)],
            fill=(0, 150, 0), width=3)
    dd.ellipse([x + 228, y + 16, x + 236, y + 24], fill=(0, 150, 0))
    # clock
    dd.ellipse([x + 196, y + 2, x + 236, y + 18], fill=WHITE, outline=NAVY, width=2)
    dd.line([x + 216, y + 10, x + 216, y + 5], fill=NAVY, width=2)
    dd.line([x + 216, y + 10, x + 224, y + 12], fill=RED, width=2)
    dd.text((x + 126, y + 54), "8:30 ET", font=font(9, bold=True), fill=RED_D, anchor="mm")


def art_trump(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(255, 226, 150))
    # sun + palms
    dd.ellipse([x + 196, y + 2, x + 238, y + 44], fill=(255, 180, 0), outline=(220, 120, 0), width=2)
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        dd.line([x + 217 + 24 * math.cos(a), y + 23 + 24 * math.sin(a),
                 x + 217 + 30 * math.cos(a), y + 23 + 30 * math.sin(a)], fill=(220, 120, 0), width=2)
    for px, flip in [(14, 1), (222, -1)]:
        dd.line([x + px + 12, y + 56, x + px + 12, y + 18], fill=(120, 70, 0), width=3)
        for a2 in range(-50, 51, 25):
            import math
            a = math.radians(a2 - 90)
            dd.line([x + px + 12, y + 20, x + px + 12 + flip * 16 * math.cos(a),
                     y + 20 + 14 * math.sin(a)], fill=(0, 140, 60), width=3)
    # US flag
    dd.rectangle([x + 52, y + 8, x + 96, y + 30], fill=WHITE, outline=NAVY, width=1)
    for s in range(4):
        dd.rectangle([x + 52, y + 8 + s * 6, x + 96, y + 11 + s * 6], fill=RED)
    dd.rectangle([x + 52, y + 8, x + 70, y + 20], fill=NAVY)
    for sy2 in range(3):
        for sx2 in range(3):
            dd.ellipse([x + 55 + sx2 * 5, y + 10 + sy2 * 4, x + 57 + sx2 * 5, y + 12 + sy2 * 4], fill=WHITE)
    # NATO flag
    dd.rectangle([x + 148, y + 8, x + 192, y + 30], fill=(0, 60, 160), outline=NAVY, width=1)
    star(dd, x + 170, y + 19, 9, WHITE)
    # two figures shaking hands
    dd.ellipse([x + 96, y + 34, x + 114, y + 50], fill=(240, 200, 160), outline=NAVY, width=1)
    dd.polygon([(x + 92, y + 52), (x + 118, y + 52), (x + 122, y + 58), (x + 88, y + 58)], fill=NAVY)
    dd.ellipse([x + 128, y + 34, x + 146, y + 50], fill=(240, 200, 160), outline=NAVY, width=1)
    dd.polygon([(x + 124, y + 52), (x + 150, y + 52), (x + 154, y + 58), (x + 120, y + 58)], fill=(0, 60, 120))
    dd.ellipse([x + 114, y + 50, x + 128, y + 58], fill=(240, 200, 160), outline=NAVY, width=1)
    dd.text((x + 121, y + 14), "PALM BEACH", font=font(8, bold=True), fill=NAVY, anchor="mm")


def art_eu(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(190, 210, 245))
    # Berlaymont building
    dd.rectangle([x + 10, y + 14, x + 92, y + 56], fill=(235, 235, 230), outline=NAVY, width=1)
    for r in range(3):
        for c in range(6):
            dd.rectangle([x + 16 + c * 12, y + 20 + r * 11, x + 24 + c * 12, y + 28 + r * 11],
                         fill=SKY, outline=NAVY, width=1)
    dd.rectangle([x + 40, y + 46, x + 62, y + 56], fill=NAVY)
    dd.text((x + 51, y + 12), "BRUSSELS", font=font(8, bold=True), fill=NAVY, anchor="mm")
    # gold star circle
    cx, cy = x + 150, y + 30
    dd.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(0, 40, 130))
    import math
    for k in range(12):
        a = math.radians(k * 30 - 90)
        star(dd, cx + 19 * math.cos(a), cy + 19 * math.sin(a), 3.2, GOLD)
    # empty chair with red ring
    chx, chy = x + 208, y + 30
    dd.ellipse([chx - 20, chy - 20, chx + 20, chy + 20], outline=RED, width=4)
    dd.line([chx - 14, chy - 14, chx + 14, chy + 14], fill=RED, width=3)
    dd.rectangle([chx - 11, y + 22, chx + 11, y + 34], fill=(120, 70, 20), outline=NAVY, width=1)
    dd.line([chx - 11, y + 34, chx - 11, y + 50], fill=NAVY, width=2)
    dd.line([chx + 11, y + 34, chx + 11, y + 50], fill=NAVY, width=2)
    dd.text((x + 208, y + 54), "SERBIA ABSENT", font=font(8, bold=True), fill=RED_D, anchor="mm")


def art_fire(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(255, 200, 130))
    # pine trees
    for tx, th in [(16, 34), (40, 42), (64, 30)]:
        dd.polygon([(x + tx, y + 56 - th), (x + tx - 11, y + 56), (x + tx + 11, y + 56)], fill=(0, 110, 50))
        dd.polygon([(x + tx, y + 56 - th - 10), (x + tx - 8, y + 56 - th + 4), (x + tx + 8, y + 56 - th + 4)], fill=(0, 140, 60))
        dd.rectangle([x + tx - 2, y + 52, x + tx + 2, y + 56], fill=(120, 70, 0))
    # flames
    for fx, fy, fs in [(96, 44, 16), (122, 48, 20), (150, 44, 14), (176, 48, 18)]:
        dd.polygon([(x + fx - fs, y + fy + 8), (x + fx - fs * 0.5, y + fy - fs),
                    (x + fx, y + fy - fs * 0.4), (x + fx + fs * 0.5, y + fy - fs),
                    (x + fx + fs, y + fy + 8)], fill=(255, 90, 0))
        dd.polygon([(x + fx - fs * 0.5, y + fy + 8), (x + fx, y + fy - fs * 0.3),
                    (x + fx + fs * 0.5, y + fy + 8)], fill=(255, 210, 0))
    # smoke
    for sx2, sy2, sr in [(100, 14, 8), (118, 8, 10), (140, 14, 8), (160, 8, 9), (180, 14, 7)]:
        dd.ellipse([x + sx2 - sr, y + sy2 - sr, x + sx2 + sr, y + sy2 + sr], fill=(120, 120, 125))
    # warning sign
    dd.polygon([(x + 208, y + 12), (x + 234, y + 12), (x + 221, y + 38)], fill=(255, 220, 0), outline=NAVY, width=2)
    dd.text((x + 221, y + 24), "!", font=font(14, bold=True), fill=RED_D, anchor="mm")
    dd.text((x + 221, y + 48), "3,000+ ha", font=font(9, bold=True), fill=RED_D, anchor="mm")


def art_16days(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(232, 214, 248))
    # purple ribbon
    rx, ry = x + 40, y + 28
    dd.polygon([(rx - 14, ry - 18), (rx - 2, ry - 18), (rx - 2, ry + 6), (rx - 14, ry + 22),
                (rx - 20, ry + 8)], fill=(110, 40, 160))
    dd.polygon([(rx + 14, ry - 18), (rx + 2, ry - 18), (rx + 2, ry + 6), (rx + 14, ry + 22),
                (rx + 20, ry + 8)], fill=(140, 60, 190))
    dd.ellipse([rx - 6, ry - 20, rx + 6, ry - 8], fill=(110, 40, 160))
    # candles
    for cx in [86, 108, 130]:
        dd.rectangle([x + cx, y + 22, x + cx + 10, y + 52], fill=WHITE, outline=NAVY, width=1)
        dd.ellipse([x + cx + 2, y + 12, x + cx + 8, y + 22], fill=(255, 180, 0))
        dd.ellipse([x + cx + 4, y + 15, x + cx + 6, y + 20], fill=(255, 240, 150))
    # flowers
    for fx, fy in [(160, 44), (182, 38), (204, 46), (222, 40)]:
        for k in range(5):
            import math
            a = math.radians(k * 72 - 90)
            dd.ellipse([x + fx + 6 * math.cos(a) - 3, y + fy + 6 * math.sin(a) - 3,
                        x + fx + 6 * math.cos(a) + 3, y + fy + 6 * math.sin(a) + 3], fill=(255, 120, 180))
        dd.ellipse([x + fx - 3, y + fy - 3, x + fx + 3, y + fy + 3], fill=GOLD)
    # 16-day calendar strip
    dd.rectangle([x + 152, y + 6, x + 232, y + 20], fill=WHITE, outline=(110, 40, 160), width=1)
    dd.text((x + 192, y + 13), "25 NOV \u2013 10 DEC", font=font(8, bold=True), fill=(110, 40, 160), anchor="mm")
    dd.text((x + 40, y + 54), "5 AN HOUR", font=font(9, bold=True), fill=(110, 40, 160), anchor="mm")


def art_congo(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(205, 235, 200))
    # map of DR Congo (rough)
    dd.polygon([(x + 14, y + 14), (x + 44, y + 8), (x + 66, y + 14), (x + 70, y + 30),
                (x + 56, y + 48), (x + 30, y + 50), (x + 12, y + 34)], fill=(90, 160, 90),
               outline=NAVY, width=1)
    dd.ellipse([x + 52, y + 16, x + 58, y + 22], fill=RED)
    dd.text((x + 42, y + 30), "BUNIA", font=font(8, bold=True), fill=NAVY, anchor="mm")
    # 3-truck convoy
    for i, tx in enumerate([92, 128, 164]):
        dd.rectangle([x + tx, y + 30, x + tx + 28, y + 46], fill=(200, 60, 40), outline=NAVY, width=1)
        dd.rectangle([x + tx + 20, y + 22, x + tx + 30, y + 32], fill=(200, 60, 40), outline=NAVY, width=1)
        dd.ellipse([x + tx + 4, y + 46, x + tx + 11, y + 53], fill=INK)
        dd.ellipse([x + tx + 18, y + 46, x + tx + 25, y + 53], fill=INK)
    # U-turn arrow
    dd.arc([x + 196, y + 8, x + 238, y + 40], 270, 90, fill=RED_D, width=4)
    dd.polygon([(x + 238, y + 24), (x + 228, y + 18), (x + 228, y + 30)], fill=RED_D)
    dd.text((x + 140, y + 12), "PULL BACK", font=font(9, bold=True), fill=RED_D, anchor="mm")
    dd.text((x + 42, y + 54), "UGANDA TALKS", font=font(8, bold=True), fill=NAVY, anchor="mm")


def art_iran(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(190, 225, 230))
    # pharmacy building
    dd.rectangle([x + 10, y + 10, x + 110, y + 56], fill=WHITE, outline=NAVY, width=2)
    dd.rectangle([x + 10, y + 10, x + 110, y + 24], fill=(0, 130, 130))
    dd.text((x + 60, y + 17), "+ PHARMACY", font=font(9, bold=True), fill=WHITE, anchor="mm")
    # empty shelves
    for sy2 in [30, 42, 54]:
        dd.line([x + 16, y + sy2, x + 104, y + sy2], fill=NAVY, width=2)
    dd.rectangle([x + 20, y + 32, x + 30, y + 41], fill=(200, 60, 60))
    dd.rectangle([x + 84, y + 44, x + 94, y + 53], fill=(60, 120, 200))
    dd.text((x + 60, y + 36), "EMPTY", font=font(8, bold=True), fill=RED_D, anchor="mm")
    # magnifier over pills
    dd.ellipse([x + 150, y + 8, x + 196, y + 54], outline=NAVY, width=4)
    dd.ellipse([x + 150, y + 8, x + 196, y + 54], fill=(255, 255, 255, 0))
    dd.line([x + 190, y + 48, x + 208, y + 56], fill=NAVY, width=4)
    dd.ellipse([x + 164, y + 26, x + 180, y + 36], fill=RED)
    dd.ellipse([x + 168, y + 38, x + 184, y + 48], fill=WHITE, outline=RED, width=1)
    # pill blister + cross
    dd.rectangle([x + 212, y + 12, x + 236, y + 34], fill=WHITE, outline=NAVY, width=1)
    for px in [216, 224, 232]:
        dd.ellipse([px, y + 16, px + 5, y + 21], fill=RED)
        dd.ellipse([px, y + 25, px + 5, y + 30], fill=(255, 200, 0))
    dd.text((x + 224, y + 50), "SHORTAGE", font=font(8, bold=True), fill=RED_D, anchor="mm")


def art_boeing(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(180, 220, 250))
    # sky + clouds
    for cx, cy in [(30, 10), (120, 6), (200, 12)]:
        dd.ellipse([x + cx, y + cy, x + cx + 26, y + cy + 10], fill=WHITE)
    # hangar
    dd.rectangle([x + 8, y + 30, x + 78, y + 56], fill=(200, 205, 215), outline=NAVY, width=1)
    dd.arc([x + 16, y + 30, x + 70, y + 52], 180, 360, fill=NAVY, width=2)
    dd.text((x + 43, y + 52), "HANGAR", font=font(7, bold=True), fill=NAVY, anchor="mm")
    # 737 jet
    jx, jy = x + 150, y + 30
    dd.polygon([(jx - 62, jy), (jx + 58, jy - 6), (jx + 70, jy), (jx + 58, jy + 6), (jx - 62, jy + 4)],
               fill=WHITE, outline=NAVY, width=2)
    dd.polygon([(jx + 30, jy - 6), (jx + 52, jy - 22), (jx + 58, jy - 6)], fill=WHITE, outline=NAVY, width=1)
    dd.polygon([(jx - 10, jy + 4), (jx + 6, jy + 18), (jx + 14, jy + 4)], fill=WHITE, outline=NAVY, width=1)
    dd.polygon([(jx - 62, jy - 2), (jx - 74, jy - 10), (jx - 74, jy + 6)], fill=WHITE, outline=NAVY, width=1)
    for wx in range(jx - 50, jx + 50, 10):
        dd.rectangle([wx, jy - 3, wx + 4, jy + 1], fill=SKY)
    dd.rectangle([jx - 58, jy - 1, jx + 40, jy + 2], fill=RED)
    dd.text((jx + 8, jy + 26), "737-8", font=font(9, bold=True), fill=NAVY, anchor="mm")
    # runway
    dd.rectangle([x + 84, y + 50, x + 236, y + 56], fill=(90, 90, 95))
    for dx in range(x + 92, x + 232, 18):
        dd.rectangle([dx, y + 52, dx + 9, y + 54], fill=WHITE)
    dd.text((x + 210, y + 44), "x50", font=font(11, bold=True), fill=RED_D)


def art_seki(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(225, 210, 235))
    # parliament building
    dd.rectangle([x + 10, y + 24, x + 96, y + 56], fill=(235, 235, 230), outline=NAVY, width=1)
    dd.polygon([(x + 8, y + 24), (x + 53, y + 8), (x + 98, y + 24)], fill=NAVY)
    for cx in range(x + 18, x + 90, 12):
        dd.rectangle([cx, y + 32, cx + 7, y + 46], fill=SKY, outline=NAVY, width=1)
    dd.rectangle([x + 48, y + 46, x + 58, y + 56], fill=NAVY)
    # gavel
    dd.line([x + 130, y + 44, x + 168, y + 16], fill=(120, 70, 0), width=5)
    dd.rectangle([x + 128, y + 10, x + 152, y + 24], fill=(120, 70, 0), outline=NAVY, width=1)
    dd.rectangle([x + 148, y + 14, x + 172, y + 28], fill=(150, 90, 20), outline=NAVY, width=1)
    dd.ellipse([x + 168, y + 40, x + 190, y + 52], fill=(120, 70, 0), outline=NAVY, width=1)
    # motion paper
    dd.polygon([(x + 186, y + 10), (x + 232, y + 10), (x + 232, y + 50), (x + 186, y + 50)], fill=WHITE, outline=NAVY, width=1)
    dd.line([(x + 192, y + 18), (x + 226, y + 18)], fill=RED, width=2)
    for ly in [26, 32, 38, 44]:
        dd.line([(x + 192, y + ly), (x + 226, y + ly)], fill=(120, 120, 130), width=1)
    dd.text((x + 209, y + 54), "CENSURE", font=font(8, bold=True), fill=RED_D, anchor="mm")
    dd.text((x + 130, y + 54), "6 PARTIES", font=font(8, bold=True), fill=NAVY, anchor="mm")


def art_fbi(dd, x, y, w, h):
    dd.rectangle([x, y, x + w, y + h], fill=(200, 205, 220))
    # server racks
    for sx in [12, 52, 92]:
        dd.rectangle([x + sx, y + 8, x + sx + 34, y + 54], fill=(40, 45, 60), outline=NAVY, width=1)
        for ry2 in range(y + 14, y + 52, 10):
            dd.rectangle([x + sx + 4, ry2, x + sx + 24, ry2 + 5], fill=(0, 200, 120))
            dd.ellipse([x + sx + 28, ry2 + 1, x + sx + 31, ry2 + 4], fill=RED)
    # shield
    shx, shy = x + 160, y + 28
    dd.polygon([(shx, shy - 20), (shx + 16, shy - 14), (shx + 16, shy + 4), (shx, shy + 20),
                (shx - 16, shy + 4), (shx - 16, shy - 14)], fill=(0, 60, 160), outline=GOLD, width=2)
    dd.text((shx, shy), "FBI", font=font(9, bold=True), fill=WHITE, anchor="mm")
    # breach crack
    dd.line([(x + 196, y + 6), (x + 206, y + 18), (x + 198, y + 30), (x + 210, y + 42), (x + 202, y + 54)],
            fill=RED, width=3)
    dd.line([(x + 206, y + 18), (x + 216, y + 14)], fill=RED, width=2)
    dd.line([(x + 198, y + 30), (x + 188, y + 34)], fill=RED, width=2)
    # warning triangle
    dd.polygon([(x + 222, y + 34), (x + 238, y + 34), (x + 230, y + 50)], fill=(255, 220, 0), outline=NAVY, width=1)
    dd.text((x + 230, y + 43), "!", font=font(10, bold=True), fill=RED_D, anchor="mm")
    dd.text((x + 160, y + 54), "NCIC", font=font(9, bold=True), fill=NAVY, anchor="mm")

# ================= 12 ILLUSTRATED TILES (3 rows x 4) =================
# (category, headline, deck, artist)
TILES = [
    ("MARKETS", "ASIAN STOCKS FALL",
     "Nikkei \u22122.55% at open to 57,152 as tech tracks US falls; Advantest \u221212%.",
     art_stocks),
    ("ECONOMY", "CPI JUMPS",
     "Australia Oct CPI 4.9% YoY, up from 4.3%; RBA hike bets revive (ABS).",
     art_cpi),
    ("ECONOMY", "DATA DUE",
     "US PCE, GDP, jobs due 13:30 UTC; core PCE seen +3.2%, GDP +3.4\u20133.6%.",
     art_data),
    ("POLITICS", "TRUMP\u2013RUTTE",
     "Trump meets NATO chief Rutte late afternoon in Palm Beach (DUE).",
     art_trump),
    ("EUROPE", "EU SUMMIT",
     "EU\u2013Balkans summit opens Brussels 16:00 UTC; Serbia absent (DUE).",
     art_eu),
    ("DISASTER", "ISLAND FIRE",
     "Flinders Island fire ~3,000+ ha; \u2018too late to leave\u2019 warning (Tasmania).",
     art_fire),
    ("UN", "16 DAYS",
     "UN: 5 women an hour killed by a partner or relative; 78,000 killed in 2025.",
     art_16days),
    ("AFRICA", "CONGO PULLBACK",
     "DR Congo rebels halt Bunia advance, pull back after Uganda-mediated talks.",
     art_congo),
    ("HEALTH", "MEDICINE HUNT",
     "Iran pharmacies shutting; patients cut doses or buy on informal markets (DW).",
     art_iran),
    ("BUSINESS", "BOEING ORDER",
     "Xiamen Airlines agrees 50 Boeing 737-8s, ~$7.4bn list value; 2031\u201334.",
     art_boeing),
    ("JAPAN", "SEKI CENSURE",
     "Japan opposition to file censure motion vs minister Seki over funds row (DUE).",
     art_seki),
    ("USA", "FBI BREACH",
     "FBI probes suspected breach of NCIC crime database; scope unclear (CNN/AP).",
     art_fbi),
]
TILE_W, TILE_H = 244, 118
for i, (cat, head, deck, artist) in enumerate(TILES):
    tx = 12 + (i % 4) * (TILE_W + 8)
    ty = 236 + (i // 4) * (TILE_H + 4)
    d.rectangle([tx, ty, tx + TILE_W, ty + TILE_H], fill=WHITE, outline=(200, 195, 185), width=1)
    artist(d, tx + 1, ty + 1, TILE_W - 2, 58)
    d.rectangle([tx + 1, ty + 1, tx + 108, ty + 17], fill=RED)
    d.text((tx + 6, ty + 9), cat, font=font(9, bold=True), fill=WHITE, anchor="lm")
    d.text((tx + 6, ty + 66), head, font=font(13, bold=True), fill=INK)
    draw_wrapped(d, tx + 6, ty + 84, deck, font(10), TILE_W - 12, MUTED, lh=12, max_lines=2)

# ================= BY THE NUMBERS =================
NY0, NY1 = 598, 646
d.rectangle([0, NY0, W, NY1], fill=NAVY)
d.text((12, NY0 + 4), "BY THE NUMBERS", font=font(10, bold=True), fill=GOLD)
NUMBERS = [
    ("4.9%", "AUSTRALIA CPI, OCT YOY"),
    ("\u22122.55%", "NIKKEI AT OPEN"),
    ("$7.4bn", "BOEING LIST VALUE"),
    ("78,000", "WOMEN & GIRLS KILLED, 2025"),
    ("3,000+ ha", "FLINDERS FIRE AREA"),
]
cell_w = (W - 150) // 5
for i, (num, lab) in enumerate(NUMBERS):
    cx = 150 + i * cell_w + cell_w // 2
    d.text((cx, NY0 + 22), num, font=font(19, bold=True), fill=WHITE, anchor="mm")
    d.text((cx, NY0 + 39), lab, font=font(8, bold=True), fill=(170, 190, 215), anchor="mm")

# ================= WORLD MAP =================
MY0, MY1 = 646, 758
d.rectangle([0, MY0, W, MY1], fill=(214, 232, 245))
d.text((12, MY0 + 10), "WHERE IT HAPPENED \u2014 WORLD MAP", font=font(11, bold=True), fill=NAVY, anchor="lm")
d.text((1012, MY0 + 10), "\u2605 LEAD  \u2022  1\u201312 TILES", font=font(9, bold=True), fill=MUTED, anchor="rm")
MAP_TOP, MAP_BOT = MY0 + 18, MY1 - 2


def proj(lon, lat):
    return (12 + (lon + 170) / 360.0 * 1000, MAP_TOP + (75 - lat) / 130.0 * (MAP_BOT - MAP_TOP))


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80), (-75, 72), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-22, 70), (-30, 76), (-55, 76), (-60, 74)],
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-40, -5), (-35, -9), (-40, -20),
     (-48, -28), (-58, -35), (-65, -40), (-70, -52), (-73, -50), (-73, -37), (-70, -20),
     (-77, -12), (-80, -3)],
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
     (43, 11), (48, 11), (51, 12), (44, 0), (40, -10), (35, -18), (32, -28), (26, -34),
     (19, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (30, 70), (25, 71), (18, 69),
     (12, 65), (5, 60), (5, 58), (-2, 55), (-10, 52), (-10, 43)],
    [(30, 36), (35, 36), (40, 38), (44, 39), (48, 38), (50, 42), (52, 46), (55, 50),
     (60, 55), (65, 60), (70, 68), (75, 72), (85, 74), (95, 76), (105, 77), (115, 76),
     (130, 72), (140, 72), (155, 70), (162, 66), (170, 66), (178, 65), (170, 60), (162, 58),
     (156, 52), (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38), (120, 32),
     (115, 25), (110, 20), (108, 15), (105, 10), (100, 8), (98, 12), (95, 16), (92, 21),
     (88, 22), (85, 19), (80, 13), (77, 8), (75, 12), (72, 20), (66, 25), (62, 25),
     (58, 26), (55, 26), (52, 28), (50, 29), (48, 30), (44, 29), (40, 30), (36, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32), (132, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -11), (140, -17), (136, -12), (132, -11), (130, -13),
     (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38), (141, 40), (142, 42),
     (144, 44), (142, 45), (140, 42), (138, 38), (135, 36), (132, 33)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10)],
    [(167, -45), (170, -42), (174, -38), (177, -38), (175, -41), (172, -43)],
]
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=(52, 130, 86),
              outline=(20, 80, 50), width=1)

# pins: (label, lon, lat, is_lead)
PINS = [
    ("\u2605", 100, 40, True),
    ("1", 140, 36, False), ("2", 149, -35, False), ("3", -77, 39, False),
    ("4", -80, 27, False), ("5", 4, 51, False), ("6", 148, -40, False),
    ("7", -74, 41, False), ("8", 30, 2, False), ("9", 51, 36, False),
    ("10", 118, 24, False), ("11", 134, 35, False), ("12", -77, 39, False),
]
# nudge overlapping US pins apart (3 = data/Washington, 12 = FBI/Washington)
PINS[3] = ("3", -84, 39, False)
PINS[12] = ("12", -70, 39, False)
for label, lon, lat, is_lead in PINS:
    px, py = proj(lon, lat)
    if is_lead:
        star(d, px, py, 11, GOLD)
        d.ellipse([px - 11, py - 11, px + 11, py + 11], outline=NAVY, width=1)
    else:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=2)
        d.text((px, py), label, font=font(8, bold=True), fill=WHITE, anchor="mm")

# ================= MORE OF THE DAY: 22 MORE STORIES =================
TY0 = 758
d.text((12, TY0 + 10), "MORE OF THE DAY \u2014 22 MORE STORIES", font=font(11, bold=True), fill=NAVY, anchor="lm")
d.rectangle([12, TY0 + 20, W - 12, TY0 + 21], fill=GOLD)
# (facts-file number, one-line brief). #23 Bangladesh (15 Nov, stale) dropped,
# replaced by verified Reuters 25 Nov markets line. #22 FBI is a tile.
TAIL = [
    (13, "10 freed in Cartagena standoff; police give no final count \u2014 \u2018all out\u2019 reports differ."),
    (14, "US Army to detonate ~4,300 kg unstable lead azide in Iowa Wed, 9am local."),
    (15, "Trump team split over targeting Iran\u2019s leaders to end war; no decision (NBC)."),
    (16, "Around 175 migrants unaccounted for after boat from Senegal vanishes (Reuters)."),
    (17, "Erdogan ally Yazici quits AKP post as fund probe reaches his son (Reuters)."),
    (18, "Mosque loudspeaker seizures draw \u2018religious war\u2019 charge vs Ben-Gvir (Al Jazeera)."),
    (19, "Libya\u2019s Haftar makes first known visit to T\u00fcrkiye after Ukraine hit Russian ship."),
    (20, "House counsel denies backing Oct raid on Rep. Omar\u2019s home; DOJ apologises (CNN)."),
    (21, "Nigeria\u2019s Emir of Daura, 92, suspended after assault allegation (BBC)."),
    (23, "Kospi \u22125.3% at worst, Taiwan \u22125.1% as AI sell-off spreads (Reuters)."),
    (24, "Zimbabwean, 24, convicted in S. Africa over Ukraine-war plan; suspended term (BBC)."),
    (25, "Prabowo\u2019s VP nominees Amran, Sugiono sent to MPR 23 Nov; vote 11 Dec."),
    (26, "Gukesh\u2013Sindarov Game 2, Geneva, 14:00 UTC; Game 1 drawn, 0.5\u20130.5."),
    (27, "CAS restores Senegal\u2019s 2025 AFCON title; Morocco to appeal (Reuters)."),
    (28, "Japan services PPI +4.2% YoY, fastest since 1990; Sept revised 3.8% (BOJ)."),
    (29, "Gold slips toward $3,560 ahead of US PCE data."),
    (30, "Bitcoin below $60,000, giving back rally toward $64,000 (CoinDesk)."),
    (31, "US last close: S&P 7,201 \u22120.5%, Nasdaq \u22121.5%, Dow 50,018 +0.85%."),
    (32, "Aussie dollar jumps to ~0.6657 after hot CPI print (FXStreet)."),
    (33, "US markets closed Thu for Thanksgiving; early close Fri 13:00 ET."),
    (34, "Trump: \u2018probably not too late\u2019 for US stake in Nvidia (NY Post)."),
    (35, "CIA, ODNI hit by breach of unclassified network; no classified hit (NYT)."),
]
assert len(TAIL) == 22
for i, (num, text) in enumerate(TAIL):
    col = 0 if i < 11 else 1
    row = i % 11
    lx = 12 if col == 0 else 518
    ly = TY0 + 24 + row * 13.5
    d.text((lx, ly), str(num), font=font(10, bold=True), fill=RED_D)
    d.text((lx + 24, ly), text, font=font(10), fill=INK)

# ================= MARKETS TICKER =================
KY0, KY1 = 928, 954
d.rectangle([0, KY0, W, KY1], fill=(12, 12, 14))
ticker = ("NIKKEI \u22122.55% AT OPEN  \u2022  S&P 7,201 \u22120.5%  \u2022  NASDAQ \u22121.5%  \u2022  "
          "DOW 50,018 +0.85%  \u2022  GOLD $3,548 \u22120.4%  \u2022  BTC $59,693 \u22122.4%  \u2022  "
          "ETH $1,676 \u22121.8%  \u2022  10-YR 4.90%  \u2022  AUD/USD 0.6657")
for _ts in (11, 10.5, 10, 9.5, 9, 8.5):
    if font(_ts, bold=True).getlength(ticker) <= W - 16:
        break
print("ticker font", _ts, "width", round(font(_ts, bold=True).getlength(ticker), 1))
d.text((512, (KY0 + KY1) // 2), ticker, font=font(_ts, bold=True), fill=GOLD, anchor="mm")

# ================= DATE CHECK + SOURCES =================
DY0 = 954
d.rectangle([12, DY0 + 4, W - 12, DY0 + 46], outline=RED, width=2)
d.text((20, DY0 + 11), "DATE CHECK", font=font(10, bold=True), fill=RED_D)
draw_wrapped(d, 20, DY0 + 25,
             "All 35 stories reported 25 Nov 2026. NOT USED (24 Nov or earlier): Huawei verdict \u00b7 Sparta II hit \u00b7 Riyadh tower strike \u00b7 Hormuz tanker claims \u00b7 ICJ Myanmar ruling (19 Nov) \u00b7 Turkish helicopter crash. No war-death tallies. DUE = scheduled. Boeing signed 24 Nov; FBI breach first reported 20 Nov.",
             font(9), W - 40, INK, lh=11, max_lines=2)
d.text((512, 1014), "SOURCES: REUTERS \u00b7 AP \u00b7 BBC \u00b7 ABS \u00b7 UN NEWS / UN WOMEN \u00b7 XINHUA \u00b7 EUROPEAN COUNCIL \u00b7 FIDE \u00b7 BEA \u00b7 TASMANIA FIRE SERVICE \u00b7 DW \u00b7 CNN \u00b7 NY POST \u00b7 COINDESK \u00b7 FXSTREET \u00b7 SKY NEWS \u00b7 AFP \u00b7 AL JAZEERA \u00b7 NBC NEWS",
       font=font(8), fill=MUTED, anchor="mm")

# ================= SAVE =================
OUT = os.path.join(BASE, "entry-v1final.png")
img.save(OUT, format="PNG", optimize=True)
print("saved", OUT, img.size)
PREV = os.path.join(BASE, "preview-300-v1final.png")
img.resize((300, 300), Image.LANCZOS).save(PREV, format="PNG", optimize=True)
print("saved", PREV)
