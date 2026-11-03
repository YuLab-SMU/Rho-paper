#!/usr/bin/env python3
"""Overlay precise labels on the gpt-image visual base for Figure 1.

The base image is deliberately text-free (gpt-image cannot render reliable
lettering). This script adds the paper's exact labels at fixed positions and
writes the publication figure.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PRINT = ROOT / "drafts" / "figures" / "print"
ARXIV = ROOT / "drafts" / "arxiv" / "figures"
BASE = PRINT / "fig1-base.png"
OUT = PRINT / "figure-argument.png"

DARK = "#173c32"
ACCENT = "#3f7864"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def main():
    im = Image.open(BASE).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    f_badge = ImageFont.truetype(FB, 26)
    f_line = ImageFont.truetype(FR, 28)

    zones = [
        (W * 0.16, "A", ["A judgment,", "materials scattered"]),
        (W * 0.49, "B", ["Organized by", "the current purpose"]),
        (W * 0.81, "C", ["One shared state:", "read, revised, continued"]),
    ]
    y0 = H - 150
    for cx, badge, lines in zones:
        # badge disc
        r = 17
        d.ellipse((cx - r, y0 - r, cx + r, y0 + r), fill=DARK)
        bw = d.textbbox((0, 0), badge, font=f_badge)[2]
        d.text((cx - bw / 2, y0 - 17), badge, font=f_badge, fill="white")
        # two label lines, centred
        yy = y0 + 30
        for ln in lines:
            tw = d.textbbox((0, 0), ln, font=f_line)[2]
            d.text((cx - tw / 2, yy), ln, font=f_line, fill=DARK)
            yy += 36

    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, optimize=True)
    ARXIV.mkdir(parents=True, exist_ok=True)
    (ARXIV / "figure-argument.png").write_bytes(OUT.read_bytes())
    print("wrote", OUT, im.size)


if __name__ == "__main__":
    main()
