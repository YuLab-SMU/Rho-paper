#!/usr/bin/env python3
"""Compose Figure 3: one P1 judgment, made inspectable.

Panel A: the claim and the materials it rests on (drawn).
Panel B: the recomputed-versus-reported counts (existing redrawn chart).
Panel C: the real Notebook crops (agent cell + reported counts), neutral labels.

Precise numbers and wording are drawn here rather than generated.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PRINT = ROOT / "drafts" / "figures" / "print"
ARXIV = ROOT / "drafts" / "arxiv" / "figures"
SRC = ROOT / "drafts" / "figures"

DARK = "#173c32"; SECOND = "#4b625a"; ACCENT = "#3f7864"
FILL = "#eef3f1"; STROKE = "#9fb8ae"; WHITE = "#ffffff"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else FR, sz)


def wrap(d, text, f, width):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textbbox((0, 0), t, font=f)[2] <= width: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def neutral_anchor():
    src = Image.open(SRC / "p1-notebook.png").convert("RGB")
    cell = src.crop((382, 147, 382 + 735, 147 + 235))
    out = src.crop((430, 535, 430 + 680, 535 + 130))
    w = max(cell.width, out.width) + 16
    h = cell.height + out.height + 12 + 16
    c = Image.new("RGB", (w, h), "white")
    c.paste(cell, (8, 8))
    c.paste(out, (8, 8 + cell.height + 12))
    d = ImageDraw.Draw(c)
    d.rectangle((8, 8, 8 + cell.width, 8 + cell.height), outline="#d8e2de", width=2)
    d.rectangle((8, 8 + cell.height + 12, 8 + out.width, 8 + cell.height + 12 + out.height),
                outline="#d8e2de", width=2)
    return c


def badge(d, x, y, letter):
    r = 18
    d.ellipse((x - r, y - r, x + r, y + r), fill=DARK)
    f = font(24, True)
    tw = d.textbbox((0, 0), letter, font=f)[2]
    d.text((x - tw / 2, y - 15), letter, font=f, fill="white")


def main():
    W = 2048
    counts = Image.open(PRINT / "figure-p1-counts.png").convert("RGB")
    anchor = neutral_anchor()

    # canvas
    A_h = 470
    counts_w = 940
    counts = counts.resize((counts_w, round(counts.height * counts_w / counts.width)), Image.LANCZOS)
    anchor_w = 900
    anchor = anchor.resize((anchor_w, round(anchor.height * anchor_w / anchor.width)), Image.LANCZOS)
    B_y = A_h + 70
    H = B_y + max(counts.height, anchor.height) + 50
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)

    # ---- Panel A: claim -> materials
    badge(d, 26, 26, "A")
    claim_w, claim_h = 860, 128
    cx = W // 2
    d.rounded_rectangle((cx - claim_w // 2, 34, cx + claim_w // 2, 34 + claim_h),
                        radius=16, fill=FILL, outline=STROKE, width=2)
    f_t = font(28, True); f_b = font(22)
    title = "Claim"
    tw = d.textbbox((0, 0), title, font=f_t)[2]
    d.text((cx - tw / 2, 48), title, font=f_t, fill=DARK)
    body = "The recomputation reproduces the published counts and reversal counts."
    lines = wrap(d, body, f_b, claim_w - 60)
    yy = 86
    for ln in lines:
        tw = d.textbbox((0, 0), ln, font=f_b)[2]
        d.text((cx - tw / 2, yy), ln, font=f_b, fill=SECOND); yy += 27

    cards = [
        ("Contrast", ["two pairwise", "DESeq2 contrasts"]),
        ("Samples", ["5 WT, 6 hTau,", "6 CgA-KO/hTau"]),
        ("Model", ["nominal P<0.01,", "|log2FC|>0.5"]),
        ("Run", ["one shared", "Notebook session"]),
        ("Version", ["script and", "input versions"]),
    ]
    cw, ch, gap = 360, 176, 40
    total = len(cards) * cw + (len(cards) - 1) * gap
    x0 = (W - total) // 2
    cy = 250
    f_ct = font(25, True); f_cb = font(20)
    claim_bottom = 34 + claim_h
    centers = []
    for i, (t, subl) in enumerate(cards):
        x = x0 + i * (cw + gap)
        cxx = x + cw // 2
        centers.append(cxx)
        d.rounded_rectangle((x, cy, x + cw, cy + ch), radius=14, fill=WHITE, outline=STROKE, width=2)
        tw = d.textbbox((0, 0), t, font=f_ct)[2]
        d.text((cxx - tw / 2, cy + 26), t, font=f_ct, fill=DARK)
        yy = cy + 68
        for ln in subl:
            tw = d.textbbox((0, 0), ln, font=f_cb)[2]
            d.text((cxx - tw / 2, yy), ln, font=f_cb, fill=SECOND); yy += 27
    # arrows claim -> cards
    for cxx in centers:
        d.line((cx, claim_bottom, cxx, cy), fill=ACCENT, width=3)
        ax, ay = cxx, cy
        d.polygon([(ax, ay), (ax - 8, ay - 12), (ax + 8, ay - 12)], fill=ACCENT)

    # ---- Panel B: counts
    badge(d, 34, B_y - 28, "B")
    im.paste(counts, (44, B_y))
    d.rectangle((43, B_y - 1, 44 + counts.width, B_y + counts.height), outline="#d8e2de", width=2)

    # ---- Panel C: real Notebook crops
    C_x = 1080
    badge(d, C_x - 10, B_y - 28, "C")
    im.paste(anchor, (C_x, B_y))
    d.rectangle((C_x - 1, B_y - 1, C_x + anchor.width, B_y + anchor.height), outline="#d8e2de", width=2)

    out = PRINT / "figure-p1-judgment.png"
    im.save(out, optimize=True)
    ARXIV.mkdir(parents=True, exist_ok=True)
    (ARXIV / "figure-p1-judgment.png").write_bytes(out.read_bytes())
    print("wrote", out, im.size)


if __name__ == "__main__":
    main()
