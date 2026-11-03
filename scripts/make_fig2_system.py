#!/usr/bin/env python3
"""Standalone Figure 2: system and deployment (three layers + shared state)."""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

DARK = "#173c32"; SECOND = "#4b625a"; FILL = "#e7f2ec"; FILL2 = "#dcefe4"
STROKE = "#7ba596"; ACCENT = "#3f7864"; RULE = "#cfddd7"; WHITE = "#ffffff"
FONT = "DejaVu Sans, Liberation Sans, Arial, sans-serif"

W, H = 1400, 640
OUT = Path(__file__).resolve().parents[1] / "drafts" / "figures" / "print" / "figure-system.svg"

_svg: list[str] = []


def rect(x, y, w, h, fill=FILL, stroke=STROKE, sw=2, rx=12):
    _svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def text(x, y, s, size=21, color=SECOND, weight="400", anchor="start"):
    w = f' font-weight="{weight}"' if weight != "400" else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    _svg.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}"'
                f'{w}{a} fill="{color}">{escape(s)}</text>')


def clines(cx, y0, lines, size, color, weight, lh):
    for i, s in enumerate(lines):
        text(cx, y0 + i * lh, s, size, color, weight, "middle")


def line(x1, y1, x2, y2, color=ACCENT, sw=3.2):
    _svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')


def arrowhead(x, y, ux, uy, head=11, color=ACCENT):
    px, py = -uy, ux
    bx, by = x - head * ux, y - head * uy
    _svg.append(f'<polygon points="{x:.1f},{y:.1f} {bx + head*0.5*px:.1f},{by + head*0.5*py:.1f} '
                f'{bx - head*0.5*px:.1f},{by - head*0.5*py:.1f}" fill="{color}"/>')


def arrow(x1, y1, x2, y2, color=ACCENT, w=3.2, head=11, double=False):
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy) or 1
    ux, uy = dx / d, dy / d
    sx, sy = (x1 + head * 0.9 * ux, y1 + head * 0.9 * uy) if double else (x1, y1)
    ex, ey = x2 - head * 0.9 * ux, y2 - head * 0.9 * uy
    line(sx, sy, ex, ey, color, w)
    arrowhead(x2, y2, ux, uy, head, color)
    if double:
        arrowhead(x1, y1, -ux, -uy, head, color)


def build():
    _svg.clear()
    _svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    _svg.append(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')
    text(32, 52, "System and deployment", 38, DARK, "700")
    text(32, 90, "Semantics belong to plugins; composition and routing to the application; "
                 "one execution's lifetime to Core", 19, SECOND)
    line(32, 108, W - 32, 108, RULE, 2)

    bw, bh, by = 400, 200, 134
    plug = (56, by, bw, bh); app = (500, by, bw, bh); core = (944, by, bw, bh)

    def layer(box, title, role, body):
        x, y, w, h = box; cx = x + w / 2
        rect(x, y, w, h)
        text(cx, y + 42, title, 26, DARK, "700", "middle")
        clines(cx, y + 74, role, 21, ACCENT, "600", 25)
        clines(cx, y + 108, body, 20, SECOND, "400", 25)

    layer(plug, "Rho-plugins", ["capability providers"],
          ["R analysis \u00b7 Agent bridge", "tables & plots \u00b7 editor & files",
           "own semantics, native state,", "provenance and results"])
    layer(app, "Rho application", ["organizer"],
          ["select & assemble \u00b7 layout", "shared interaction routing", "and presentation"])
    layer(core, "Rho-core", ["optional managed execution"],
          ["request identity \u00b7 retained", "execution facts \u00b7 resident Host",
           "not on every path"])

    my = by + bh / 2
    arrow(plug[0] + plug[2], my, app[0], my, double=True, w=3, head=10)
    arrow(app[0] + app[2], my, core[0], my, double=True, w=3, head=10)

    ss = (56, 382, W - 2 * 24 - 64, 128)
    rect(*ss)
    text(ss[0] + 26, ss[1] + 40, "Shared state", 26, DARK, "700")
    text(ss[0] + 26, ss[1] + 72,
         "actions \u00b7 resources \u00b7 selections \u00b7 views \u2014 each with owner, "
         "version and provenance", 20, SECOND)
    text(ss[0] + 26, ss[1] + 96,
         "observed computation fact    |    agent interpretation    |    human judgment", 20, SECOND)
    text(ss[0] + 26, ss[1] + 120,
         "local service on the machine  \u00b7  no Rho server  \u00b7  the browser has no "
         "shell, filesystem or Core access", 18, ACCENT)
    for box in (plug, app, core):
        cx = box[0] + box[2] / 2
        arrow(cx, by + bh, cx, ss[1], color=STROKE, w=2.3, head=9)

    ent_y, ent_w, ent_h = 548, 240, 84
    res = (56, ent_y, ent_w, ent_h); agn = (W - 56 - ent_w, ent_y, ent_w, ent_h)
    for b, label in ((res, "Researcher"), (agn, "Agent")):
        rect(*b)
        text(b[0] + ent_w / 2, ent_y + ent_h / 2 + 9, label, 25, DARK, "700", "middle")
    arrow(res[0] + ent_w / 2, ent_y, res[0] + ent_w / 2, ss[1] + ss[3], w=3.2, head=11)
    arrow(agn[0] + ent_w / 2, ent_y, agn[0] + ent_w / 2, ss[1] + ss[3], w=3.2, head=11)
    text(W / 2, 532, "two entrances read and write the same actions and resources",
         20, ACCENT, "600", "middle")

    _svg.append("</svg>")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(_svg), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    build()
