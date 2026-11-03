#!/usr/bin/env python3
"""Generate the Rho architecture figure (two stacked panels, A and B).

Self-contained, standard library only, deterministic. Writes one vector SVG
that converts to PDF/PNG with rsvg-convert.

Canvas is 1400 px wide so that, at the manuscript's text width, figure text
stays legible (~7 pt). Two stacked panels: A system architecture, B round-trip.

Truth preserved (see Rho / Rho-plugins / Rho-core docs/ARCHITECTURE.md):
  * Three layers: Rho = application container (select & assemble, layout,
    shared interaction routing, presentation). Rho-plugins = functional
    capability providers that own semantics, native state, provenance and
    results. Rho-core = OPTIONAL managed execution, not on every path.
  * Four shared interaction concepts: Action, Resource, Selection, View.
  * Human and Agent reach the SAME actions and resources (two entrances,
    one set of material). A displayed relationship is not proof of a claim.
"""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

DARK = "#173c32"
SECOND = "#4b625a"
FILL = "#e7f2ec"
FILL2 = "#dcefe4"
STROKE = "#7ba596"
ACCENT = "#3f7864"
RULE = "#cfddd7"
GREY = "#9eaba5"
WHITE = "#ffffff"
FONT = "DejaVu Sans, Liberation Sans, Arial, sans-serif"

W = 1400
M = 24
PANEL_A_Y, PANEL_A_H = 20, 660
PANEL_B_Y, PANEL_B_H = 700, 800
H = PANEL_B_Y + PANEL_B_H + M  # 1524

OUT_DIR = Path(__file__).resolve().parents[1] / "drafts" / "figures" / "print"
OUT_SVG = OUT_DIR / "figure-architecture.svg"

_svg: list[str] = []


def rect(x, y, w, h, rx=12, fill=FILL, stroke=STROKE, sw=2):
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


def line(x1, y1, x2, y2, color=ACCENT, sw=3.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    _svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{color}" stroke-width="{sw}"{d} stroke-linecap="round"/>')


def arrowhead(x, y, ux, uy, head=11, color=ACCENT):
    px, py = -uy, ux
    bx, by = x - head * ux, y - head * uy
    p1 = (bx + head * 0.5 * px, by + head * 0.5 * py)
    p2 = (bx - head * 0.5 * px, by - head * 0.5 * py)
    _svg.append(f'<polygon points="{x:.1f},{y:.1f} {p1[0]:.1f},{p1[1]:.1f} '
                f'{p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>')


def arrow(x1, y1, x2, y2, color=ACCENT, w=3.2, head=11, double=False):
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy) or 1
    ux, uy = dx / dist, dy / dist
    sx, sy = (x1 + head * 0.9 * ux, y1 + head * 0.9 * uy) if double else (x1, y1)
    ex, ey = x2 - head * 0.9 * ux, y2 - head * 0.9 * uy
    line(sx, sy, ex, ey, color, w)
    arrowhead(x2, y2, ux, uy, head, color)
    if double:
        arrowhead(x1, y1, -ux, -uy, head, color)


def badge(cx, cy, num, r=14):
    _svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{DARK}"/>')
    text(cx, cy + 6, str(num), 17, WHITE, "700", "middle")


def panel(x, y, w, h, letter, title, subtitle):
    rect(x, y, w, h, rx=18, fill=WHITE, stroke=RULE, sw=2)
    text(x + 32, y + 54, letter, 40, DARK, "700")
    text(x + 96, y + 54, title, 40, DARK, "700")
    text(x + 32, y + 94, subtitle, 20, SECOND)
    line(x + 32, y + 112, x + w - 32, y + 112, RULE, 2)


def edge_point(box, toward):
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2
    dx, dy = toward[0] - cx, toward[1] - cy
    if dx == 0 and dy == 0:
        return cx, cy
    tx = (w / 2) / abs(dx) if dx else float("inf")
    ty = (h / 2) / abs(dy) if dy else float("inf")
    t = min(tx, ty)
    return cx + dx * t, cy + dy * t


# --------------------------------------------------------------- PANEL A
def panel_a():
    y0 = PANEL_A_Y
    panel(M, y0, W - 2 * M, PANEL_A_H, "A", "System architecture",
          "Semantics belong to plugins; composition and routing to the application; "
          "one execution's lifetime to Core")

    bw, bh, by = 400, 200, y0 + 130
    plug = (56, by, bw, bh)
    app = (500, by, bw, bh)
    core = (944, by, bw, bh)

    def layer(box, title, role, body):
        x, y, w, h = box
        cx = x + w / 2
        rect(x, y, w, h)
        text(cx, y + 42, title, 26, DARK, "700", "middle")
        clines(cx, y + 74, role, 21, ACCENT, "600", 25)
        clines(cx, y + 108, body, 20, SECOND, "400", 25)

    layer(plug, "Rho-plugins", ["capability providers"],
          ["R analysis \u00b7 Agent bridge", "tables & plots \u00b7 editor & files",
           "own semantics, native state,", "provenance and results"])
    layer(app, "Rho application", ["organizer"],
          ["select & assemble \u00b7 layout", "shared interaction routing",
           "and presentation"])
    layer(core, "Rho-core", ["optional managed execution"],
          ["request identity \u00b7 retained", "execution facts \u00b7 resident Host",
           "not on every path"])

    mid_y = by + bh / 2
    arrow(plug[0] + plug[2], mid_y, app[0], mid_y, double=True, w=3, head=10)
    arrow(app[0] + app[2], mid_y, core[0], mid_y, double=True, w=3, head=10)

    ss = (56, y0 + 380, W - 2 * M - 64, 128)
    rect(*ss)
    text(ss[0] + 26, ss[1] + 40, "Shared state", 26, DARK, "700")
    text(ss[0] + 26, ss[1] + 72,
         "actions \u00b7 resources \u00b7 selections \u00b7 views \u2014 each with owner, "
         "version and provenance", 20, SECOND)
    text(ss[0] + 26, ss[1] + 96,
         "observed computation fact    |    agent interpretation    |    human judgment",
         20, SECOND)
    text(ss[0] + 26, ss[1] + 120,
         "local service on the machine  \u00b7  no Rho server  \u00b7  the browser has no "
         "shell, filesystem or Core access", 18, ACCENT)

    for box in (plug, app, core):
        cx = box[0] + box[2] / 2
        arrow(cx, by + bh, cx, ss[1], color=STROKE, w=2.3, head=9)

    ent_y, ent_w, ent_h = y0 + 540, 240, 84
    res = (56, ent_y, ent_w, ent_h)
    agn = (W - 56 - ent_w, ent_y, ent_w, ent_h)
    rect(*res)
    rect(*agn)
    text(res[0] + ent_w / 2, ent_y + ent_h / 2 + 9, "Researcher", 25, DARK, "700", "middle")
    text(agn[0] + ent_w / 2, ent_y + ent_h / 2 + 9, "Agent", 25, DARK, "700", "middle")
    arrow(res[0] + ent_w / 2, ent_y, res[0] + ent_w / 2, ss[1] + ss[3], w=3.2, head=11)
    arrow(agn[0] + ent_w / 2, ent_y, agn[0] + ent_w / 2, ss[1] + ss[3], w=3.2, head=11)
    text(W / 2, 545,
         "two entrances read and write the same actions and resources",
         20, ACCENT, "600", "middle")


# --------------------------------------------------------------- PANEL B
def panel_b():
    y0 = PANEL_B_Y
    panel(M, y0, W - 2 * M, PANEL_B_H, "B", "The analysis round-trip",
          "The interface and the Agent's context are two presentations of one shared "
          "state; versions are per object, not global")

    cx = 700

    def node(box, num, title, body):
        x, y, w, h = box
        rect(x, y, w, h)
        badge(x + 16, y + 16, num, r=13)
        clines(x + w / 2, y + 46, title, 23, DARK, "700", 27)
        by_ = y + 46 + 27 * len(title) + 4
        clines(x + w / 2, by_, body, 20, SECOND, "400", 24)

    n1 = (570, 840, 260, 120)
    n2 = (972, 960, 270, 130)
    n3 = (972, 1210, 270, 130)
    n4 = (560, 1335, 280, 130)
    n5 = (158, 1210, 270, 130)
    n6 = (158, 960, 270, 130)
    hub = (525, 1085, 350, 172)

    rect(*hub, rx=14, fill=FILL2, stroke=STROKE, sw=2.5)
    text(cx, hub[1] + 42, "Shared state", 25, DARK, "700", "middle")
    clines(cx, hub[1] + 74, ["three sources; per-object versions",
                             "(no global revision)"], 20, SECOND, "400", 24)
    clines(cx, hub[1] + 128, ["checkable invariants:", "identity \u00b7 version \u00b7 protection"],
           19, ACCENT, "600", 23)

    def C(b):
        return (b[0] + b[2] / 2, b[1] + b[3] / 2)

    order = [n1, n2, n3, n4, n5, n6]
    for i in range(6):
        a, b = order[i], order[(i + 1) % 6]
        p, q = edge_point(a, C(b)), edge_point(b, C(a))
        arrow(p[0], p[1], q[0], q[1], head=11)
    p, q = edge_point(n6, C(n1)), edge_point(n1, C(n6))
    text((p[0] + q[0]) / 2 - 4, (p[1] + q[1]) / 2 - 10, "re-organize",
         19, ACCENT, "600", "middle")

    for b in (n4, n5):
        p, q = edge_point(hub, C(b)), edge_point(b, C(hub))
        line(p[0], p[1], q[0], q[1], GREY, 2, dash="6 6")

    node(n1, 1, ["Scientific purpose"], ["what am I deciding?"])
    node(n2, 2, ["Organization plan"], ["which materials, why,", "which relations,",
                                       "what is missing"])
    node(n3, 3, ["Operable working", "interface"], ["views + actions +", "explicit gaps"])
    node(n4, 4, ["Human reading", "& revision"],
         ["layout \u2260 focus", "\u2260 analysis scope"])
    node(n5, 5, ["Agent continuation"],
         ["bounded context:", "prepared / provided / read"])
    node(n6, 6, ["New results", "& progress"], ["next purpose \u2192 plan"])


def build():
    _svg.clear()
    _svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                f'viewBox="0 0 {W} {H}">')
    _svg.append(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')
    panel_a()
    panel_b()
    _svg.append("</svg>")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_SVG.write_text("\n".join(_svg), encoding="utf-8")
    print(f"wrote {OUT_SVG}  ({W}x{H})")


if __name__ == "__main__":
    build()
