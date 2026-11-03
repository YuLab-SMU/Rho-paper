#!/usr/bin/env python3
"""Build compact, non-screenshot evidence figures for the Rho manuscript.

Outputs (into both drafts/figures/print and drafts/arxiv/figures):
  figure-p1-anchor.png     small crop of the real P1 Notebook (agent cell + output)
  figure-p1-counts.pdf/png vector bar chart, P1 recomputed vs reported counts
  figure-p4-counts.pdf/png vector bar chart, P4 recomputed vs reported counts
  figure-casecards.pdf/png two vector case cards (P2, P5)
  figure-p3-pathway.png    crop of the already-redrawn P3 Hallmark plot panel

Only PIL (raster crops) and stdlib (SVG) are used; no matplotlib.
"""
from __future__ import annotations
import math
from html import escape
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PRINT = ROOT / "drafts" / "figures" / "print"
ARXIV = ROOT / "drafts" / "arxiv" / "figures"
PRINT.mkdir(parents=True, exist_ok=True)

DARK = "#173c32"; SECOND = "#4b625a"; ACCENT = "#3f7864"; PUB = "#c0875c"
GRID = "#dfe7e3"; RULE = "#cfddd7"; WHITE = "#ffffff"; FILL = "#eef3f1"; STROKE = "#b9c9c2"
FONT = "DejaVu Sans, Liberation Sans, Arial, sans-serif"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_svg: list[str] = []
def svg_reset(w, h):
    _svg.clear(); _svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')
    _svg.append(f'<rect width="{w}" height="{h}" fill="{WHITE}"/>')
def svg_text(x, y, s, size=20, color=SECOND, weight="400", anchor="start"):
    w = f' font-weight="{weight}"' if weight != "400" else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    _svg.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}"{w}{a} fill="{color}">{escape(s)}</text>')
def svg_rect(x, y, w, h, fill=FILL, stroke=STROKE, sw=2, rx=0):
    _svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def svg_line(x1, y1, x2, y2, color=GRID, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    _svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}/>')
def svg_save(name):
    _svg.append("</svg>")
    (PRINT / name).write_text("\n".join(_svg), encoding="utf-8")

def wrap(s, width):
    words = s.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= width: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

# ------------------------------------------------------------ bar charts
def nicemax(m):
    for step in (50, 100, 200, 250, 500, 1000):
        if math.ceil(m / step) <= 5:
            return step * math.ceil(m / step)
    return m

def bar_chart(stem, title, subtitle, cats, local, reported):
    W, H = 1000, 560
    svg_reset(W, H)
    svg_text(24, 46, title, 30, DARK, "700")
    svg_text(24, 80, subtitle, 18, SECOND)
    px0, py0, px1, py1 = 100, 128, 968, 430
    pw, ph = px1 - px0, py1 - py0
    base = py1
    mx = nicemax(max(local + reported))
    for i in range(0, mx + 1, mx // 4):
        y = base - i / mx * ph
        svg_line(px0, y, px1, y, GRID, 1.2)
        svg_text(px0 - 12, y + 6, f"{i:,}", 17, SECOND, "400", "end")
    svg_text(28, py0 - 8, "genes", 17, SECOND)
    n = len(cats); gw = pw / n; bw = gw * 0.30; gap = 6
    for i, (cat, lv, rv) in enumerate(zip(cats, local, reported)):
        cx = px0 + gw * (i + 0.5)
        pair = 2 * bw + gap
        lx = cx - pair / 2
        for x, v, col in ((lx, lv, ACCENT), (lx + bw + gap, rv, PUB)):
            h = v / mx * ph
            svg_rect(x, base - h, bw, h, fill=col, stroke="none", rx=2)
            svg_text(x + bw / 2, base - h - 8, f"{v:,}", 17, DARK, "700", "middle")
        for k, ln in enumerate(wrap(cat, 16)):
            svg_text(cx, base + 28 + k * 20, ln, 17, SECOND, "400", "middle")
    # legend
    lx0, ly = 640, 100
    svg_rect(lx0, ly - 12, 16, 16, fill=ACCENT, stroke="none", rx=2)
    svg_text(lx0 + 24, ly + 2, "this run", 17, SECOND)
    svg_rect(lx0 + 130, ly - 12, 16, 16, fill=PUB, stroke="none", rx=2)
    svg_text(lx0 + 154, ly + 2, "reported", 17, SECOND)
    svg_save(stem + ".svg")

# ------------------------------------------------------------ case cards
def case_cards(stem):
    W, H = 1100, 400
    svg_reset(W, H)
    cards = [
        ("P2 \u00b7 Single-nucleus RNA-seq (GSE221215)",
         "Is the biological replicate the sample or the cell?",
         "UMAP \u00b7 per-sample QC table \u00b7 cell-to-mouse map \u00b7 cell-level DE test",
         "A cell-level Wilcoxon test ignores mouse dependence; the cell classes stay working annotations."),
        ("P5 \u00b7 Blood transcriptome (GSE252990)",
         "What can a patient-paired comparison support?",
         "per-patient table \u00b7 three time points \u00b7 patient-plus-time model \u00b7 input-processing history",
         "Counts depend on input handling; a paired contrast is not prediction of response."),
    ]
    cw, ch, gap, x0, y0 = 520, 360, 40, 10, 20
    for idx, (title, q, mats, opened) in enumerate(cards):
        x = x0 + idx * (cw + gap)
        svg_rect(x, y0, cw, ch, fill=FILL, stroke=STROKE, sw=2, rx=14)
        svg_text(x + 22, y0 + 40, title, 21, DARK, "700")
        svg_line(x + 22, y0 + 56, x + cw - 22, y0 + 56, RULE, 1.5)
        yy = y0 + 86
        for label, body in (("Question", q), ("Materials organized", mats), ("What it opened", opened)):
            svg_text(x + 22, yy, label.upper(), 15, ACCENT, "700")
            yy += 24
            for ln in wrap(body, 46):
                svg_text(x + 22, yy, ln, 18, SECOND); yy += 23
            yy += 10
    svg_save(stem + ".svg")

# ------------------------------------------------------------ raster crops
def p1_anchor():
    src = Image.open(ROOT / "drafts" / "figures" / "p1-notebook.png").convert("RGB")
    cell = src.crop((382, 147, 382 + 735, 147 + 235))       # agent-attributed cell
    out = src.crop((430, 535, 430 + 680, 535 + 130))         # output + mapping warning
    pad = 18
    W = 735 + 2 * pad
    H = pad + 26 + cell.height + 20 + 26 + out.height + pad
    canvas = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(canvas)
    fb = ImageFont.truetype(FB, 20); fr = ImageFont.truetype(FR, 20)
    y = pad
    d.text((pad, y), "A  Agent-attributed R cell", font=fb, fill="#173c32"); y += 26
    canvas.paste(cell, (pad, y)); d.rectangle((pad - 1, y - 1, pad + cell.width, y + cell.height), outline="#d8e2de", width=2); y += cell.height + 20
    d.text((pad, y), "B  Reported counts and a gene-mapping warning", font=fb, fill="#173c32"); y += 26
    canvas.paste(out, (pad, y)); d.rectangle((pad - 1, y - 1, pad + out.width, y + out.height), outline="#d8e2de", width=2)
    canvas.save(PRINT / "figure-p1-anchor.png", optimize=True)

def p3_pathway():
    src = Image.open(ARXIV / "figure-5-p3.png").convert("RGB")  # composite 1696x2040
    crop = src.crop((48, 900, 1648, 2000))                     # panel B: redrawn Hallmark dot plot
    W = crop.width + 40
    canvas = Image.new("RGB", (W, crop.height + 30), "white")
    canvas.paste(crop, (20, 15))
    d = ImageDraw.Draw(canvas)
    d.rectangle((19, 14, 20 + crop.width, 15 + crop.height), outline="#d8e2de", width=2)
    canvas.save(PRINT / "figure-p3-pathway.png", optimize=True)

def convert(name):
    import subprocess
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(PRINT / (name + ".pdf")), str(PRINT / (name + ".svg"))], check=True)
    subprocess.run(["rsvg-convert", "-f", "png", "-d", "200", "-p", "200", "-o", str(PRINT / (name + ".png")), str(PRINT / (name + ".svg"))], check=True)

def main():
    p1_anchor()
    p3_pathway()
    bar_chart("figure-p1-counts",
              "P1 \u2014 recomputed vs reported counts",
              "Two DESeq2 contrasts, nominal P<0.01 and |log2FC|>0.5; counts are one run.",
              ["Up", "Down", "Reversal 1", "Reversal 2"],
              [1096, 1549, 334, 551], [1193, 869, 417, 293])
    bar_chart("figure-p4-counts",
              "P4 \u2014 recomputed vs reported counts",
              "Three old vs four young samples, BH-adjusted P<0.05 and |log2FC|>1.",
              ["Up", "Down", "Total"],
              [370, 234, 604], [406, 94, 500])
    case_cards("figure-casecards")
    for nm in ("figure-p1-counts", "figure-p4-counts", "figure-casecards"):
        convert(nm)
    # copy everything the manuscript includes into the arxiv figures dir
    for f in ["figure-p1-anchor.png", "figure-p1-counts.pdf", "figure-p1-counts.png",
              "figure-p4-counts.pdf", "figure-p4-counts.png",
              "figure-casecards.pdf", "figure-casecards.png", "figure-p3-pathway.png"]:
        (ARXIV / f).write_bytes((PRINT / f).read_bytes())
    print("done")

if __name__ == "__main__":
    main()
