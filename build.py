#!/usr/bin/env python3
"""Build entry.png for news-image-20261124, account 2 (Orochim25).

Broadsheet newspaper, 9 hero scenes: 3 large heroes on top, 6 smaller
heroes below, each with its own bold flat-vector illustration. All 31
verified stories of Tuesday 24 November 2026. Drawn with PIL only.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 239, 220)
PANEL = (255, 253, 246)
INK = (26, 26, 26)
RED = (163, 31, 36)
NAVY = (31, 58, 95)
GOLD = (201, 162, 39)
GREY = (90, 86, 76)
SKY = (178, 214, 235)
SEA = (28, 78, 130)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def font(size, bold=False, serif=False):
    if serif:
        path = FD + ("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf")
    else:
        path = FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(path, size)


REGION_COLOR = {
    "N. AMERICA": (179, 32, 44),
    "EUROPE": (36, 86, 166),
    "MIDEAST": (201, 106, 18),
    "AFRICA": (46, 125, 50),
    "ASIA-PACIFIC": (106, 63, 160),
    "LATIN AM.": (15, 118, 110),
}

# ---------------------------------------------------------------- text utils


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def chip(d, x, y, text, fill, fg=(255, 255, 255), fnt=None):
    fnt = fnt or font(10, bold=True)
    w = d.textlength(text, font=fnt) + 12
    h = fnt.size + 8
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill)
    d.text((x + 6, y + 4), text, font=fnt, fill=fg)
    return x + w


def starburst(d, cx, cy, r_out, r_in, n, fill):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- hero art
# Each art function draws inside the box (x0, y0, x1, y1). Bold, simple,
# high-contrast shapes that read at ~300 px wide.


def art_hormuz(d, x0, y0, x1, y1):
    # Sky, sea, two big tankers, spiky mines, orange explosions.
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.rectangle([x0, y0 + (y1 - y0) * 0.55, x1, y1], fill=SEA)
    w = x1 - x0
    # sun
    d.ellipse([x1 - 52, y0 + 8, x1 - 14, y0 + 46], fill=(250, 205, 80))
    # tanker 1 (left, big)
    hx, hy = x0 + 18, y0 + (y1 - y0) * 0.62
    d.rectangle([hx, hy, hx + 130, hy + 26], fill=(20, 20, 20))
    d.rectangle([hx + 90, hy - 22, hx + 118, hy], fill=(240, 240, 235))
    d.rectangle([hx + 8, hy - 12, hx + 26, hy], fill=(200, 40, 40))
    # tanker 2 (right, smaller)
    hx2 = x0 + w - 150
    d.rectangle([hx2, hy + 6, hx2 + 120, hy + 30], fill=(30, 30, 30))
    d.rectangle([hx2 + 82, hy - 14, hx2 + 106, hy + 6], fill=(240, 240, 235))
    # mines: spiky black balls in the water
    for mx, my, mr in [(x0 + 70, y1 - 22, 12), (x0 + w // 2, y1 - 14, 10),
                       (x1 - 60, y1 - 26, 12)]:
        starburst(d, mx, my, mr + 7, mr - 2, 8, (15, 15, 15))
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(15, 15, 15))
    # explosions
    starburst(d, x0 + 96, hy - 26, 30, 14, 10, (255, 140, 20))
    starburst(d, x0 + 96, hy - 26, 18, 8, 10, (255, 220, 60))
    starburst(d, x1 - 96, hy - 18, 24, 11, 10, (255, 140, 20))
    starburst(d, x1 - 96, hy - 18, 13, 6, 10, (255, 220, 60))


def art_ulleung(d, x0, y0, x1, y1):
    # Sky, green island with lighthouse, two big jets, huge warning triangle.
    d.rectangle([x0, y0, x1, y1], fill=(196, 226, 240))
    w = x1 - x0
    d.ellipse([x0 + 14, y0 + 10, x0 + 54, y0 + 50], fill=(250, 205, 80))
    # island
    d.polygon([(x0 + 10, y1), (x0 + 120, y0 + 52), (x0 + 235, y1)],
              fill=(52, 130, 70))
    # lighthouse
    d.rectangle([x0 + 112, y0 + 30, x0 + 126, y0 + 56], fill=(240, 240, 235))
    d.rectangle([x0 + 110, y0 + 24, x0 + 128, y0 + 32], fill=(200, 40, 40))
    # sea
    d.rectangle([x0, y1 - 16, x1, y1], fill=(28, 78, 130))
    # jets: big dark delta silhouettes
    for jx, jy, s in [(x0 + w - 150, y0 + 22, 1.0), (x0 + w - 90, y0 + 52, 0.8)]:
        d.polygon([(jx, jy), (jx + 52 * s, jy + 10 * s), (jx, jy + 20 * s),
                   (jx + 10 * s, jy + 10 * s)], fill=(25, 25, 30))
        d.line([jx - 26, jy + 10, jx - 4, jy + 10], fill=(25, 25, 30), width=3)
    # huge warning triangle
    cx, cy = x0 + w - 62, y0 + 78
    d.polygon([(cx, cy - 34), (cx + 36, cy + 26), (cx - 36, cy + 26)],
              fill=(255, 200, 20), outline=(160, 30, 30), width=4)
    d.text((cx - 4, cy - 16), "!", font=font(30, bold=True), fill=(160, 30, 30))


def art_sanofi(d, x0, y0, x1, y1):
    # Giant capsule pill + big $41 BILLION banner.
    d.rectangle([x0, y0, x1, y1], fill=(232, 240, 248))
    w = x1 - x0
    # giant pill, diagonal
    cx, cy = x0 + w // 2, y0 + 52
    d.rounded_rectangle([cx - 130, cy - 26, cx + 130, cy + 26], radius=26,
                        fill=(255, 255, 255), outline=(200, 40, 40), width=3)
    d.rounded_rectangle([cx - 130, cy - 26, cx, cy + 26], radius=26,
                        fill=(200, 40, 40))
    d.rectangle([cx - 2, cy - 26, cx + 2, cy + 26], fill=(255, 255, 255))
    # banner
    d.rectangle([x0 + 16, y1 - 40, x1 - 16, y1 - 8], fill=NAVY)
    txt = "$41 BILLION"
    f = font(24, bold=True)
    tw = d.textlength(txt, font=f)
    d.text((x0 + (w - tw) / 2, y1 - 36), txt, font=f, fill=(255, 255, 255))


def art_chip(d, x0, y0, x1, y1):
    # Big chip + red prohibition circle/slash.
    d.rectangle([x0, y0, x1, y1], fill=(226, 232, 240))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = 52
    for i in range(-1, 2):
        for px in (cx - s - 14, cx + s + 2):
            d.rectangle([px, cy + i * 22 - 4, px + 12, cy + i * 22 + 4],
                        fill=(201, 162, 39))
        for py in (cy - s - 14, cy + s + 2):
            d.rectangle([cx + i * 22 - 4, py, cx + i * 22 + 4, py + 12],
                        fill=(201, 162, 39))
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(25, 25, 30))
    d.rectangle([cx - s + 14, cy - s + 14, cx + s - 14, cy + s - 14],
                outline=(201, 162, 39), width=3)
    d.text((cx - 22, cy - 16), "AI", font=font(26, bold=True),
           fill=(255, 255, 255))
    # prohibition ring
    r = 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 30, 30), width=9)
    d.line([cx - r * 0.7, cy + r * 0.7, cx + r * 0.7, cy - r * 0.7],
           fill=(200, 30, 30), width=9)


def art_eu(d, x0, y0, x1, y1):
    # EU circle of stars + big red X.
    d.rectangle([x0, y0, x1, y1], fill=(226, 232, 240))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=(30, 60, 140))
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = cx + 30 * math.cos(a), cy + 30 * math.sin(a)
        starburst(d, sx, sy, 6, 2.5, 5, (255, 215, 0))
    d.line([cx - 46, cy - 46, cx + 46, cy + 46], fill=(200, 30, 30), width=10)
    d.line([cx - 46, cy + 46, cx + 46, cy - 46], fill=(200, 30, 30), width=10)


def art_estonia(d, x0, y0, x1, y1):
    # Huge warning triangle + border barrier.
    d.rectangle([x0, y0, x1, y1], fill=(240, 228, 200))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - 6
    d.polygon([(cx, cy - 40), (cx + 44, cy + 32), (cx - 44, cy + 32)],
              fill=(255, 200, 20), outline=(160, 30, 30), width=5)
    d.text((cx - 5, cy - 20), "!", font=font(36, bold=True), fill=(160, 30, 30))
    # barrier stripes at the bottom
    for i in range(5):
        x = x0 + 8 + i * 20
        d.polygon([(x, y1 - 12), (x + 10, y1 - 12), (x + 20, y1 - 2),
                   (x + 10, y1 - 2)], fill=(25, 25, 30))


def art_court(d, x0, y0, x1, y1):
    # Big gavel + sound block, $290bn implied by the headline text.
    d.rectangle([x0, y0, x1, y1], fill=(232, 228, 214))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # gavel head
    d.rounded_rectangle([cx - 44, cy - 34, cx + 44, cy - 6], radius=8,
                        fill=(120, 72, 20))
    d.rectangle([cx - 44, cy - 34, cx - 30, cy - 6], fill=(90, 52, 12))
    # handle
    d.rectangle([cx - 6, cy - 6, cx + 6, cy + 34], fill=(150, 100, 40))
    # sound block
    d.rounded_rectangle([cx - 34, cy + 34, cx + 34, cy + 46], radius=4,
                        fill=(90, 52, 12))
    # motion ticks
    for dx in (-52, 52):
        d.line([cx + dx, cy - 26, cx + dx, cy - 6], fill=(90, 52, 12), width=4)


def art_gaza(d, x0, y0, x1, y1):
    # Big explosion starburst over a dark building silhouette.
    d.rectangle([x0, y0, x1, y1], fill=(40, 40, 48))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - 8
    starburst(d, cx, cy, 46, 20, 10, (255, 140, 20))
    starburst(d, cx, cy, 28, 12, 10, (255, 220, 60))
    # building silhouettes at the bottom
    d.rectangle([x0 + 8, y1 - 34, x0 + 40, y1], fill=(15, 15, 18))
    d.rectangle([x0 + 46, y1 - 22, x0 + 70, y1], fill=(15, 15, 18))
    d.rectangle([x1 - 40, y1 - 30, x1 - 8, y1], fill=(15, 15, 18))
    # cracked wall line
    d.line([x1 - 58, y1 - 40, x1 - 46, y1 - 24, x1 - 56, y1 - 10],
           fill=(255, 220, 60), width=3)


def art_quake(d, x0, y0, x1, y1):
    # Brown mountain with snow cap + huge red zigzag crack + 5.6.
    d.rectangle([x0, y0, x1, y1], fill=(214, 232, 240))
    cx = (x0 + x1) / 2
    d.polygon([(x0 + 6, y1 - 8), (cx, y0 + 12), (x1 - 6, y1 - 8)],
              fill=(120, 84, 50))
    d.polygon([(cx - 16, y0 + 30), (cx, y0 + 12), (cx + 16, y0 + 30),
               (cx + 8, y0 + 26), (cx, y0 + 32), (cx - 8, y0 + 26)],
              fill=(255, 255, 255))
    # crack
    pts = [(cx - 30, y0 + 40), (cx - 12, y0 + 56), (cx - 26, y0 + 70),
           (cx - 6, y0 + 86), (cx - 18, y1 - 12)]
    d.line(pts, fill=(160, 30, 30), width=5, joint="curve")
    f = font(22, bold=True)
    d.text((x1 - 52, y0 + 8), "5.6", font=f, fill=(160, 30, 30))


BIG_ART = {1: art_hormuz, 2: art_ulleung, 3: art_sanofi}
SMALL_ART = {4: art_chip, 6: art_eu, 7: art_estonia, 10: art_court,
             11: art_gaza, 20: art_quake}

# ---------------------------------------------------------------- map data

CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 73), (-105, 74),
     (-95, 80), (-85, 79), (-78, 73), (-70, 68), (-65, 60), (-58, 52),
     (-55, 47), (-60, 45), (-66, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 30), (-84, 30), (-88, 29), (-91, 22), (-94, 19),
     (-97, 16), (-94, 15), (-90, 14), (-86, 13), (-83, 9), (-79, 9),
     (-83, 10), (-87, 13), (-91, 15), (-95, 16), (-100, 18), (-105, 20),
     (-110, 23), (-114, 28), (-118, 32), (-122, 37), (-124, 43), (-125, 49),
     (-130, 55), (-140, 60), (-152, 58), (-162, 58), (-168, 66)],
    # South America
    [(-79, 9), (-76, 10), (-72, 12), (-66, 11), (-62, 9), (-58, 7), (-54, 5),
     (-51, 4), (-50, 0), (-46, -2), (-41, -3), (-37, -6), (-35, -9),
     (-38, -15), (-40, -21), (-46, -24), (-49, -28), (-54, -33), (-58, -38),
     (-63, -41), (-66, -46), (-68, -51), (-70, -54), (-73, -50), (-73, -44),
     (-72, -36), (-71, -28), (-70, -19), (-75, -15), (-79, -9), (-81, -4),
     (-80, 0), (-79, 4), (-79, 9)],
    # Africa
    [(-17, 15), (-16, 20), (-12, 27), (-9, 31), (-5, 35), (0, 36), (6, 37),
     (10, 37), (12, 34), (16, 32), (20, 32), (26, 32), (30, 31), (32, 31),
     (34, 28), (35, 24), (37, 20), (39, 16), (41, 13), (44, 11), (48, 11),
     (51, 11), (48, 6), (44, 2), (41, -2), (40, -8), (39, -13), (36, -18),
     (34, -23), (31, -28), (28, -33), (24, -34), (19, -35), (16, -30),
     (14, -24), (12, -17), (12, -12), (13, -8), (12, -5), (9, 3), (5, 5),
     (0, 6), (-5, 5), (-8, 5), (-12, 8), (-15, 11), (-17, 15)],
    # Eurasia
    [(-6, 36), (-9, 37), (-9, 39), (-8, 43), (-4, 44), (-2, 46), (-2, 48),
     (-1, 50), (1, 51), (3, 53), (5, 55), (8, 57), (8, 58), (5, 60), (7, 62),
     (10, 64), (14, 67), (18, 69), (24, 71), (30, 70), (36, 68), (44, 68),
     (52, 68), (60, 69), (68, 72), (76, 72), (84, 74), (92, 75), (100, 76),
     (108, 76), (116, 73), (124, 72), (132, 71), (142, 70), (152, 69),
     (162, 68), (170, 66), (178, 65), (172, 62), (166, 60), (162, 56),
     (158, 52), (156, 51), (150, 59), (144, 58), (142, 54), (140, 49),
     (138, 45), (134, 43), (131, 42), (128, 39), (126, 38), (122, 37),
     (121, 34), (120, 31), (121, 28), (118, 25), (114, 22), (110, 20),
     (108, 18), (106, 10), (104, 8), (101, 7), (99, 9), (97, 12), (95, 15),
     (93, 18), (91, 22), (89, 22), (87, 21), (84, 18), (81, 15), (80, 12),
     (77, 8), (76, 10), (75, 13), (73, 17), (72, 20), (70, 22), (68, 23),
     (66, 25), (63, 25), (60, 25), (58, 26), (56, 27), (54, 26), (52, 25),
     (50, 28), (48, 30), (49, 28), (51, 26), (54, 24), (57, 22), (58, 20),
     (55, 17), (52, 15), (49, 14), (46, 13), (44, 13), (42, 15), (40, 16),
     (39, 20), (37, 22), (35, 26), (34, 28), (33, 31), (31, 33), (29, 36),
     (27, 37), (24, 36), (22, 37), (20, 40), (19, 42), (16, 44), (14, 44),
     (12, 44), (10, 44), (8, 44), (6, 43), (3, 42), (0, 39), (-2, 37),
     (-6, 36)],
    # Australia
    [(113, -22), (114, -28), (115, -32), (115, -35), (119, -34), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (143, -39),
     (146, -39), (149, -37), (150, -35), (153, -32), (153, -27), (152, -24),
     (150, -22), (147, -19), (144, -15), (142, -11), (141, -13), (138, -15),
     (136, -12), (134, -12), (132, -11), (130, -13), (128, -14), (126, -14),
     (124, -16), (122, -17), (120, -19), (117, -20), (114, -21), (113, -22)],
    # UK
    [(-5, 50), (-4, 53), (-5, 56), (-4, 58), (-2, 58), (0, 57), (1, 54),
     (1, 51), (-1, 50), (-4, 50), (-5, 50)],
    # Japan
    [(130, 31), (131, 33), (133, 34), (135, 34), (137, 35), (139, 36),
     (140, 38), (141, 40), (141, 42), (140, 44), (142, 44), (144, 43),
     (142, 41), (140, 39), (139, 37), (137, 36), (135, 34), (133, 33),
     (131, 32), (130, 31)],
    # New Zealand
    [(167, -45), (169, -44), (171, -43), (173, -41), (175, -40), (176, -38),
     (175, -37), (174, -36), (173, -35), (171, -37), (169, -40), (167, -43),
     (167, -45)],
]

STORY_POINTS = [
    # (number, lon, lat, region)
    (1, 56.3, 26.6, "MIDEAST"), (2, 130.9, 37.5, "ASIA-PACIFIC"),
    (3, 2.35, 48.86, "EUROPE"), (4, -77.0, 38.9, "N. AMERICA"),
    (5, 2.35, 48.86, "EUROPE"), (6, 17.1, 48.1, "EUROPE"),
    (7, 24.7, 59.4, "EUROPE"), (8, 4.4, 50.8, "EUROPE"),
    (9, 6.1, 49.6, "EUROPE"), (10, 51.4, 35.7, "MIDEAST"),
    (11, 34.5, 31.5, "MIDEAST"), (12, 42.9, 14.8, "MIDEAST"),
    (13, 32.5, 0.0, "AFRICA"), (14, 12.5, 41.9, "AFRICA"),
    (15, 38.7, 9.0, "AFRICA"), (16, 38.7, 9.0, "AFRICA"),
    (17, 30.2, 1.6, "AFRICA"), (18, 32.5, 15.6, "AFRICA"),
    (19, 105.9, 21.0, "ASIA-PACIFIC"), (20, 87.9, 27.9, "ASIA-PACIFIC"),
    (21, 139.7, 35.7, "ASIA-PACIFIC"), (22, 149.1, -35.3, "ASIA-PACIFIC"),
    (23, 90.4, 23.8, "ASIA-PACIFIC"), (24, 100.3, 40.9, "ASIA-PACIFIC"),
    (25, 121.0, 14.6, "ASIA-PACIFIC"), (26, 139.7, 35.7, "ASIA-PACIFIC"),
    (27, -73.6, 4.1, "LATIN AM."), (28, -99.1, 19.4, "LATIN AM."),
    (29, -82.4, 23.1, "LATIN AM."), (30, -60.0, -3.1, "LATIN AM."),
    (31, -92.3, 14.9, "LATIN AM."),
]


def draw_map(d, mx0, my0, mx1, my1):
    d.rectangle([mx0, my0, mx1, my1], fill=(208, 224, 238))
    # graticule
    for lon in range(-150, 181, 30):
        x = mx0 + (lon + 180) / 360 * (mx1 - mx0)
        d.line([x, my0, x, my1], fill=(255, 255, 255), width=1)
    for lat in (-40, -20, 0, 20, 40, 60):
        y = my1 - (lat + 58) / 142 * (my1 - my0)
        d.line([mx0, y, mx1, y], fill=(255, 255, 255), width=1)
    lat_lo, lat_hi = -58.0, 84.0

    def proj(lon, lat):
        x = mx0 + (lon + 180) / 360 * (mx1 - mx0)
        y = my1 - (lat - lat_lo) / (lat_hi - lat_lo) * (my1 - my0)
        return x, y

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(214, 196, 152), outline=(150, 130, 100))
    # dot positions, spread so no two centres are closer than 20 px
    pts = []
    for num, lon, lat, region in STORY_POINTS:
        x, y = proj(lon, lat)
        pts.append([num, x, y, region])
    for _ in range(60):
        moved = False
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[j][1] - pts[i][1]
                dy = pts[j][2] - pts[i][2]
                dist = math.hypot(dx, dy)
                if dist < 20 and dist > 0.01:
                    push = (20 - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    pts[i][1] -= ux * push
                    pts[i][2] -= uy * push
                    pts[j][1] += ux * push
                    pts[j][2] += uy * push
                    moved = True
        if not moved:
            break
    # leader lines from true position to spread position
    for (num, lon, lat, region), (_, px, py, _) in zip(STORY_POINTS, pts):
        tx, ty = proj(lon, lat)
        if math.hypot(px - tx, py - ty) > 3:
            d.line([tx, ty, px, py], fill=(120, 110, 95), width=1)
    for num, px, py, region in pts:
        col = REGION_COLOR[region]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col,
                  outline=(255, 255, 255), width=2)
        f = font(10, bold=True)
        tw = d.textlength(str(num), font=f)
        d.text((px - tw / 2, py - 6), str(num), font=f, fill=(255, 255, 255))
    d.rectangle([mx0, my0, mx1, my1], outline=INK, width=1)


# ---------------------------------------------------------------- page

BIG_HEROES = [
    dict(num=1, region="MIDEAST", tag="REPORTED",
         title="Three tankers hit mines in Hormuz, IRGC claims",
         summary="Three tankers caught fire on naval mines under US escort; claim unverified.",
         source="Trends MENA / TBS News"),
    dict(num=2, region="ASIA-PACIFIC", tag="CONFIRMED",
         title="Russian jets trigger air-raid alert on Ulleung",
         summary="Jets entered Seoul's defence zone; residents sheltered at 7:52 a.m. F-15Ks scrambled.",
         source="Reuters / Korea JoongAng Daily"),
    dict(num=3, region="EUROPE", tag="CONFIRMED",
         title="Sanofi to buy Insmed in $41 billion deal",
         summary="Sanofi buys US biotech Insmed for $41bn in cash, its biggest pharma bet in years.",
         source="Reuters"),
]

SMALL_HEROES = [
    dict(num=4, region="N. AMERICA", tag="CONFIRMED",
         title="US blacklists Megaspeed, Alibaba unit in Nvidia scandal",
         summary="US firms barred from shipping.",
         source="Reuters / Spyglass"),
    dict(num=6, region="EUROPE", tag="REPORTED",
         title="Central European leaders reject new EU budget",
         summary="Visegrad + Austria reject it.",
         source="Reuters"),
    dict(num=7, region="EUROPE", tag="REPORTED",
         title="Russia warns Estonia its actions risk 'open war'",
         summary="Moscow summons Tallinn's envoy.",
         source="Reuters"),
    dict(num=10, region="MIDEAST", tag="REPORTED",
         title="Iran courts demand $290 billion from US",
         summary="Tehran: US must pay $290bn.",
         source="AFP"),
    dict(num=11, region="MIDEAST", tag="REPORTED",
         title="Israeli strikes in Gaza kill three, incl. UNRWA worker",
         summary="Three killed, incl. UNRWA worker.",
         source="Al Jazeera"),
    dict(num=20, region="ASIA-PACIFIC", tag="CONFIRMED",
         title="5.6 quake hits Nepal near Tibet",
         summary="Felt across Nepal and northern India.",
         source="Reuters"),
]

ALSO_ITEMS = [
    (5, "HLD Clariane takeover bid", "Reuters"),
    (8, "EU probes Coca-Cola bottler", "T.Briefings"),
    (9, "EU auditors fault aid oversight", "ECA"),
    (12, "Houthis: Saudi airstrike kills 17", "AFP"),
    (13, "Somalia-Uganda anti-Shabaab", "Shabelle"),
    (14, "WFP: 10m tons wheat at risk", "WFP"),
    (15, "AU maternal health roadmap", "TNA"),
    (16, "1 in 6 Africa pregnancies to teens", "CDC"),
    (17, "Fighting traps Ebola teams in Ituri", "WHO"),
    (18, "Qatar condemns Khartoum attacks", "MFA"),
    (19, "Hanoi blast kills 6, injures 10", "Reuters"),
    (21, "Japan speeds ICC funding", "Reuters"),
    (22, "Australia fines tech firms 5%", "Reuters"),
    (23, "Hasina plans return home", "Reuters"),
    (24, "China names Shenzhou-24 crew", "Reuters"),
    (25, "Manila court orders Ang arrest", "PNA"),
    (26, "Japan cuts spending view", "Reuters"),
    (27, "Villavicencio car bomb", "El Tiempo"),
    (28, "Mexico to try 'El Chapo Isidro'", "Reuters"),
    (29, "WHO chief visits Cuba", "Al Jazeera"),
    (30, "Man rescued after 11 Amazon days", "AP"),
    (31, "Caravan crosses into Mexico", "Al Jazeera"),
]

NUMBERS = [
    ("$41bn", "Sanofi buys Insmed"),
    ("$290bn", "Iran courts demand from US"),
    ("5.6", "Nepal quake magnitude"),
    ("6 killed", "Hanoi explosion"),
    ("23", "injured in Villavicencio blast"),
    ("10m tons", "wheat at risk, WFP warns"),
    ("5%", "max tech fine, Australia"),
]


def tag_color(tag):
    return (34, 120, 50) if tag == "CONFIRMED" else (176, 96, 10)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # top rule
    d.rectangle([0, 0, W, 5], fill=INK)
    # masthead
    f_mast = font(46, bold=True, serif=True)
    d.text((8, 10), "THE WORLD IN ONE DAY", font=f_mast, fill=INK)
    f_date = font(30, bold=True, serif=True)
    d.text((8, 58), "TUESDAY, 24 NOVEMBER 2026", font=f_date, fill=RED)
    f_meta = font(11)
    meta = "31 stories · 6 regions · Research cutoff 08:30 UTC"
    d.text((W - 8 - d.textlength(meta, font=f_meta), 74), meta,
           font=f_meta, fill=GREY)
    d.line([8, 92, W - 8, 92], fill=INK, width=2)
    # UTC strip
    d.rectangle([8, 98, W - 8, 136], fill=NAVY)
    f_lab = font(12, bold=True)
    d.text((16, 112), "THE DAY IN UTC · times as reported",
           font=f_lab, fill=(255, 255, 255))
    ax0, ax1, ay = 330, 995, 126
    d.line([ax0, ay, ax1, ay], fill=(255, 255, 255), width=2)
    for h in (0, 6, 12, 18, 24):
        x = ax0 + h / 24 * (ax1 - ax0)
        d.line([x, ay - 4, x, ay + 4], fill=(255, 255, 255), width=2)
        t = f"{h:02d}"
        d.text((x - 7, ay - 18), t, font=font(9), fill=(190, 205, 225))
    for frac in (1 / 24, 7.87 / 24):
        x = ax0 + frac * (ax1 - ax0)
        d.ellipse([x - 5, ay - 5, x + 5, ay + 5], fill=(250, 205, 80),
                  outline=(255, 255, 255), width=1)
    d.text((ax0 + 1 / 24 * (ax1 - ax0) + 9, ay - 18), "01:00 HANOI BLAST",
           font=font(9, bold=True), fill=(250, 205, 80))
    d.text((ax0 + 7.87 / 24 * (ax1 - ax0) + 9, ay - 18),
           "07:52 ULLEUNG", font=font(9, bold=True),
           fill=(250, 205, 80))
    # numbers strip
    d.text((8, 142), "THE DAY IN NUMBERS", font=font(13, bold=True), fill=INK)
    bw, gap = 141, 5
    for i, (num, lab) in enumerate(NUMBERS):
        x0 = 8 + i * (bw + gap)
        d.rectangle([x0, 158, x0 + bw, 200], fill=PANEL, outline=RED, width=1)
        d.line([x0, 158, x0 + bw, 158], fill=RED, width=3)
        f_num = font(20, bold=True)
        tw = d.textlength(num, font=f_num)
        d.text((x0 + (bw - tw) / 2, 164), num, font=f_num, fill=RED)
        f_lab2 = font(9)
        lines = wrap(d, lab, f_lab2, bw - 10)
        ly = 188
        for ln in lines[:1]:
            tw2 = d.textlength(ln, font=f_lab2)
            d.text((x0 + (bw - tw2) / 2, ly), ln, font=f_lab2, fill=INK)
    # section header
    d.text((8, 206), "THE NINE STORIES THAT LED THE DAY",
           font=font(14, bold=True), fill=INK)
    d.line([8, 222, W - 8, 222], fill=INK, width=1)
    # ---- 3 big heroes
    hx = [8, 348, 688]
    hw = 328
    hy0, hy1 = 228, 454
    for h, x0 in zip(BIG_HEROES, hx):
        x1 = x0 + hw
        d.rectangle([x0, hy0, x1, hy1], fill=PANEL, outline=INK, width=1)
        BIG_ART[h["num"]](d, x0 + 1, hy0 + 1, x1 - 1, hy0 + 106)
        d.line([x0, hy0 + 106, x1, hy0 + 106], fill=INK, width=1)
        ty = hy0 + 112
        rc = REGION_COLOR[h["region"]]
        d.ellipse([x0 + 10, ty + 1, x0 + 26, ty + 17], fill=RED)
        f_nb = font(11, bold=True)
        tw = d.textlength(str(h["num"]), font=f_nb)
        d.text((x0 + 18 - tw / 2, ty + 3), str(h["num"]), font=f_nb,
               fill=(255, 255, 255))
        d.text((x0 + 32, ty + 2), h["region"], font=font(11, bold=True),
               fill=rc)
        f_h = font(18, bold=True, serif=True)
        lines = wrap(d, h["title"], f_h, hw - 20)
        block(d, x0 + 10, ty + 22, lines[:2], f_h, leading=21)
        f_s = font(12)
        lines = wrap(d, h["summary"], f_s, hw - 20)
        block(d, x0 + 10, ty + 66, lines[:2], f_s, leading=14)
        cx = chip(d, x0 + 10, hy1 - 20, h["tag"], tag_color(h["tag"]))
        d.text((cx + 8, hy1 - 17), "Source: " + h["source"], font=font(10),
               fill=GREY)
    # ---- 6 small heroes, 2 rows x 3 cols
    sy = [462, 572]
    sh = 106
    for row, y0 in enumerate(sy):
        for col, x0 in enumerate(hx):
            h = SMALL_HEROES[row * 3 + col]
            x1 = x0 + hw
            y1 = y0 + sh
            d.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=1)
            d.rectangle([x0, y0, x0 + 5, y1], fill=RED)
            SMALL_ART[h["num"]](d, x0 + 6, y0 + 4, x0 + 104, y0 + 102)
            d.line([x0 + 104, y0, x0 + 104, y1], fill=INK, width=1)
            tx = x0 + 112
            rc = REGION_COLOR[h["region"]]
            d.text((tx, y0 + 6), f"{h['num']} · {h['region']}",
                   font=font(10, bold=True), fill=rc)
            f_h = font(13, bold=True)
            lines = wrap(d, h["title"], f_h, hw - 122)
            block(d, tx, y0 + 22, lines[:3], f_h, leading=15)
            f_s = font(11)
            lines = wrap(d, h["summary"], f_s, hw - 122)
            block(d, tx, y0 + 70, lines[:1], f_s, leading=13)
            cx = chip(d, tx, y0 + 88, h["tag"], tag_color(h["tag"]),
                      fnt=font(9, bold=True))
            d.text((cx + 6, y0 + 91), h["source"], font=font(9), fill=GREY)
    # ---- bottom: map + ALSO list
    d.text((8, 686), "WHERE IT HAPPENED", font=font(14, bold=True), fill=INK)
    d.text((516, 686), "ALSO ON TUESDAY 24 NOVEMBER",
           font=font(14, bold=True), fill=INK)
    d.line([8, 702, 500, 702], fill=INK, width=1)
    d.line([516, 702, W - 8, 702], fill=INK, width=1)
    draw_map(d, 8, 706, 500, 912)
    f_leg = font(10)
    leg = "N. AMERICA 1   ·   EUROPE 6   ·   MIDEAST 4   ·   AFRICA 6   ·   ASIA-PACIFIC 9   ·   LATIN AM. 5"
    d.text((8, 918), leg, font=f_leg, fill=INK)
    # ALSO list: 22 items, 2 columns x 11 rows
    f_a = font(10)
    for i, (num, title, src) in enumerate(ALSO_ITEMS):
        col = i // 11
        row = i % 11
        x = 516 + col * 250
        y = 708 + row * 20
        d.text((x, y), f"{num}.", font=font(10, bold=True), fill=RED)
        txt = f"{title} — {src}"
        while d.textlength(txt, font=f_a) > 218 and len(txt) > 20:
            txt = txt[:-4] + "…"
        d.text((x + 24, y), txt, font=f_a, fill=INK)
    # DATE CHECK bar
    d.rectangle([8, 934, W - 8, 966], fill=(250, 230, 210), outline=RED,
                width=1)
    f_dc = font(10, bold=True)
    d.text((16, 938), "DATE CHECK", font=f_dc, fill=RED)
    f_dct = font(10)
    dc = ("Left out, wrong date: Nvidia/Huang +31% (23 Nov) · COP31 collapse (23 Nov) · "
          "Merkury sinking (22–23 Nov) · SoftBank–Intel $2B (Aug 2025) · CAS Senegal ruling (not yet decided)")
    lines = wrap(d, dc, f_dct, W - 130)
    block(d, 110, 938, lines[:2], f_dct, leading=13)
    # footer
    f_f = font(10)
    foot = ("Every story above happened or was first reported on Tuesday 24 November 2026. "
            "CONFIRMED = the event happened that day; REPORTED = first reported that day. "
            "Sources: Reuters, AFP, Al Jazeera, El Tiempo, WFP, WHO, Africa CDC.")
    lines = wrap(d, foot, f_f, W - 16)
    block(d, 8, 972, lines[:2], f_f, leading=13)
    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
