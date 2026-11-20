#!/usr/bin/env python3
"""Draw the one-image summary of Friday 20 November 2026 world news.

A newspaper-style front page at 2x, downscaled to 1024x1024
(entry.png, beside this file). Pure PIL, no network, no external
assets: every picture is a simple shape drawn here, and all text is
set in real system fonts so nothing can come out garbled.
"""

import math

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor
W = 1024 * S

PAPER = (247, 243, 234)
INK = (24, 26, 34)
RED = (178, 34, 40)
GREY = (96, 96, 100)
DARK = (22, 24, 30)
BLUE = (28, 52, 110)
GOLD = (232, 184, 64)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, px):
    return ImageFont.truetype(path, px * S)


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, W), PAPER)
d = ImageDraw.Draw(img)


def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x * S, y * S), s, font=fnt, fill=fill, anchor=anchor)


def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill,
                outline=outline, width=width * S)


def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append(((cx + rr * math.cos(ang)) * S,
                    (cy + rr * math.sin(ang)) * S))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- masthead
text(24, 16, "THE WORLD IN ONE DAY", font(SERIF_B, 30))
text(1000, 24, "ONE DAY · ONE PICTURE", font(SANSB, 16), fill=GREY, anchor="ra")
text(512, 52, "FRIDAY 20 NOVEMBER 2026", font(SANS_B, 50), anchor="ma")
rect(24, 116, 1000, 119, fill=RED)
rect(24, 123, 1000, 124, fill=INK)

# ---------------------------------------------------------------- lead story
rect(24, 136, 1000, 386, fill=(238, 240, 248), outline=INK, width=2)
# illustration: a circle of twelve gold stars (Europe) over a bridge
d.ellipse([52 * S, 168 * S, 208 * S, 324 * S], fill=BLUE, outline=INK, width=2 * S)
for i in range(12):
    ang = -math.pi / 2 + i * math.pi / 6
    star(130 + 58 * math.cos(ang), 246 + 58 * math.sin(ang), 11, GOLD)
# a small bridge arch under the circle, the Channel crossed
d.arc([40 * S, 300 * S, 220 * S, 380 * S], 180, 360, fill=RED, width=6 * S)
d.line([(40 * S, 342 * S), (220 * S, 342 * S)], fill=INK, width=3 * S)
text(130, 356, "UK · EU", font(SANS_B, 15), anchor="ma")
LX = 236
text(LX, 150, "EUROPE — UK-EU SUMMIT, BRUSSELS", font(SANS_B, 19), fill=RED)
ly = 178
for line in wrap(d, "BRITAIN AND THE EU AGREE A 100,000-A-YEAR YOUTH DEAL",
                 font(SANS_B, 35), (1000 - LX - 20) * S):
    text(LX, ly, line, font(SANS_B, 35))
    ly += 43
ly += 4
for line in wrap(d, "Up to 100,000 young people a year will be able to live, work "
                    "and study on each side of the Channel for up to three years, "
                    "at the heart of a post-Brexit reset also easing food trade "
                    "and linking carbon markets. Leaders sign off in Brussels today.",
                 font(SANS, 20), (1000 - LX - 20) * S):
    text(LX, ly, line, font(SANS, 20))
    ly += 26

# ---------------------------------------------------------------- panels
def panel(x0, y0, x1, y1, tint, kicker, kcol, headline, body, icon):
    rect(x0, y0, x1, y1, fill=tint, outline=INK, width=2)
    rect(x0, y0, x0 + 7, y1, fill=kcol)
    text(x0 + 20, y0 + 10, kicker, font(SANS_B, 15), fill=kcol)
    icon(x0 + 20, y0 + 44)
    tx = x0 + 96
    hy = y0 + 40
    for line in wrap(d, headline, font(SANS_B, 25), (x1 - tx - 14) * S):
        text(tx, hy, line, font(SANS_B, 25))
        hy += 31
    hy += 4
    for line in wrap(d, body, font(SANS, 17), (x1 - x0 - 34) * S):
        if hy + 22 > y1 - 6:
            break
        text(x0 + 20, hy, line, font(SANS, 17))
        hy += 22


def icon_sun(x, y):
    d.ellipse([x * S, y * S, (x + 62) * S, (y + 62) * S],
              fill=(240, 176, 48), outline=INK, width=2 * S)
    d.line([(x + 8) * S, (y + 46) * S, (x + 54) * S, (y + 46) * S],
           fill=(46, 125, 79), width=4 * S)
    d.arc([x * S, (y + 18) * S, (x + 62) * S, (y + 62) * S], 200, 340,
          fill=(46, 125, 79), width=4 * S)


def icon_ball(x, y):
    d.ellipse([x * S, y * S, (x + 62) * S, (y + 62) * S],
              fill=(250, 250, 248), outline=INK, width=2 * S)
    d.arc([(x - 6) * S, (y + 8) * S, (x + 26) * S, (y + 54) * S], 270, 90,
          fill=RED, width=3 * S)
    d.arc([(x + 36) * S, (y + 8) * S, (x + 68) * S, (y + 54) * S], 90, 270,
          fill=RED, width=3 * S)


def icon_shield(x, y):
    pts = [(x + 31, y), (x + 62, y + 12), (x + 62, y + 34),
           (x + 31, y + 62), (x, y + 34), (x, y + 12)]
    d.polygon([(px * S, py * S) for px, py in pts], fill=(70, 90, 140),
              outline=INK, width=2 * S)
    d.ellipse([(x + 23) * S, (y + 20) * S, (x + 39) * S, (y + 36) * S],
              fill=GOLD, outline=INK, width=2 * S)
    d.rectangle([(x + 28) * S, (y + 34) * S, (x + 34) * S, (y + 46) * S],
                fill=GOLD)


def icon_football(x, y):
    d.ellipse([x * S, y * S, (x + 62) * S, (y + 62) * S],
              fill=(250, 250, 248), outline=INK, width=2 * S)
    cx, cy = x + 31, y + 31
    pts = []
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append(((cx + 13 * math.cos(ang)) * S,
                    (cy + 13 * math.sin(ang)) * S))
    d.polygon(pts, fill=INK)


panel(24, 398, 506, 606, (236, 244, 232), "CLIMATE — COP31, ANTALYA", (46, 125, 79),
      "COP31'S FINAL DAY OPENS WITH NO DEAL",
      "A revised draft drops every mention of fossil fuels, angering "
      "campaigners, as nearly 200 nations race to agree by Friday. "
      "Talks look set to spill into the weekend.",
      icon_sun)

panel(518, 398, 1000, 606, (250, 238, 232), "SPORT — BASEBALL, USA", RED,
      "TRUMP PARDONS HIT KING PETE ROSE",
      "A posthumous pardon for the late legend's 1990 tax case, announced "
      "on the flight home from Asia. Rose's 4,256 career hits still stand.",
      icon_ball)

panel(24, 618, 506, 826, (238, 240, 250), "CYBER — FINANCE, WORLDWIDE", BLUE,
      "JPMORGAN, VISA, MASTERCARD HIT IN BREACH",
      "Hackers got customer names and e-mails via outside service "
      "providers. Card numbers were untouched.",
      icon_shield)

panel(518, 618, 1000, 826, (243, 240, 228), "FOOTBALL — FIFA", (122, 96, 20),
      "TASHIMA: A RED-CARD ROW PUSHED ME TO RUN FOR FIFA",
      "Japan's Kozo Tashima says the Balogun affair drove his challenge to "
      "Gianni Infantino. It is FIFA's first contested presidential vote "
      "since 2016, set for March 2027.",
      icon_football)

# ---------------------------------------------------------------- bottom row
rect(24, 838, 1000, 922, fill=(250, 233, 238), outline=INK, width=2)
d.polygon([(60 * S, 848 * S), (96 * S, 848 * S), (96 * S, 912 * S),
           (60 * S, 912 * S)], fill=(250, 250, 248), outline=INK, width=2 * S)
d.ellipse([(70 * S, 866 * S), (86 * S, 882 * S)], fill=RED)
d.line([(96 * S, 848 * S), (96 * S, 912 * S)], fill=INK, width=2 * S)
text(116, 846, "JAPAN — TOKYO", font(SANS_B, 15), fill=(160, 40, 90))
text(116, 866, "10,000 MARCH ON THE DIET OVER TAKAICHI'S MILITARY PLANS",
     font(SANS_B, 22))
text(116, 896, "Protesters oppose revising the pacifist constitution and expanding "
               "the armed forces.", font(SANS, 17))

# ---------------------------------------------------------------- ticker
rect(0, 934, 1024, 1024, fill=DARK)
text(24, 944, "ALSO TODAY", font(SANS_B, 16), fill=(240, 180, 60))
ticker = ("California subpoenas Nvidia over China chips  ·  25 killed in Israeli "
          "strikes across Gaza  ·  Iraq's PM takes on pro-Iran militias  ·  Europe "
          "ready for talks with Russia  ·  US sanctions Comancheros and 'Ndrangheta")
ty = 966
for line in wrap(d, ticker, font(SANS, 16), (1000 - 24) * S):
    text(24, ty, line, font(SANS, 16), fill=PAPER)
    ty += 21

img = img.resize((1024, 1024), Image.LANCZOS)
img.save("entry.png")
print("wrote entry.png", img.size)
