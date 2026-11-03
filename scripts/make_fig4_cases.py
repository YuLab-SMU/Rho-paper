#!/usr/bin/env python3
"""Compose Figure 4: four further judgments as compact cards (P2-P5)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PRINT = ROOT / "drafts" / "figures" / "print"
ARXIV = ROOT / "drafts" / "arxiv" / "figures"

DARK = "#173c32"; SECOND = "#4b625a"; ACCENT = "#3f7864"
FILL = "#eef3f1"; STROKE = "#9fb8ae"; WHITE = "#ffffff"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, M, GAP = 2048, 36, 36
CW = (W - 2 * M - GAP) // 2
CH = 360


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


def card(d, x, y, title, fields):
    d.rounded_rectangle((x, y, x + CW, y + CH), radius=16, fill=FILL, outline=STROKE, width=2)
    f_t = ImageFont.truetype(FB, 24)
    f_l = ImageFont.truetype(FB, 15)
    f_b = ImageFont.truetype(FR, 20)
    d.text((x + 24, y + 24), title, font=f_t, fill=DARK)
    d.line((x + 24, y + 60, x + CW - 24, y + 60), fill="#c9d8d1", width=1)
    yy = y + 78
    for label, body in fields:
        d.text((x + 24, yy), label.upper(), font=f_l, fill=ACCENT)
        yy += 24
        for ln in wrap(d, body, f_b, CW - 48):
            d.text((x + 24, yy), ln, font=f_b, fill=SECOND); yy += 26
        yy += 12
    return yy


def main():
    cards = [
        ("P2 \u00b7 Single-nucleus RNA-seq (GSE221215)", [
            ("Question", "Is the biological replicate the sample or the cell?"),
            ("Materials it needed", "UMAP \u00b7 per-sample QC \u00b7 cell-to-mouse map \u00b7 cell-level DE test"),
            ("What the interface exposed", "A cell-level Wilcoxon test ignores mouse dependence; 8,364 nuclei stay unresolved."),
            ("What stayed open", "No revision landing; the class labels are unvalidated."),
        ]),
        ("P3 \u00b7 Spatial profiling (GSE232853)", [
            ("Question", "Which compartment drives the pathway?"),
            ("Materials it needed", "Hallmark table \u00b7 CD68/CD20 contrast \u00b7 paired and unpaired alternatives"),
            ("What the interface exposed", "1,111 DE genes; a pooled enrichment hides which side drives a term."),
            ("What stayed open", "No revision or continuation; not a replication of the study."),
        ]),
        ("P4 \u00b7 Ageing endothelium (GSE270697)", [
            ("Question", "Why do reported counts differ?"),
            ("Materials it needed", "counts \u00b7 Ensembl 102 map \u00b7 expression filter \u00b7 pathway tables"),
            ("What the interface exposed", "604 against 500 genes; one unmapped transcript is about 34% of counts."),
            ("What stayed open", "The cause is untested; the metabolomics arm was not analysed."),
        ]),
        ("P5 \u00b7 Blood transcriptome (GSE252990)", [
            ("Question", "What can a patient-paired comparison support?"),
            ("Materials it needed", "per-patient table \u00b7 three time points \u00b7 patient-plus-time model \u00b7 input history"),
            ("What the interface exposed", "2,596 against 4,532 genes depending on how the input was handled."),
            ("What stayed open", "Not response prediction; the processing history is unknown."),
        ]),
    ]
    rows = (len(cards) + 1) // 2
    H = M + rows * CH + (rows - 1) * GAP + M
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    for i, (title, fields) in enumerate(cards):
        x = M + (i % 2) * (CW + GAP)
        y = M + (i // 2) * (CH + GAP)
        card(d, x, y, title, fields)
    out = PRINT / "figure-case-judgments.png"
    im.save(out, optimize=True)
    ARXIV.mkdir(parents=True, exist_ok=True)
    (ARXIV / "figure-case-judgments.png").write_bytes(out.read_bytes())
    print("wrote", out, im.size)


if __name__ == "__main__":
    main()
