#!/usr/bin/env python3
"""Compose the P1 evidence screenshots as editable, self-contained SVG figures.

Only spatial crops and vector labels are added; screenshot pixels are not retouched.
All crops on a figure are from the same source capture.
"""
from __future__ import annotations

import base64
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "drafts" / "figures"
OUT = FIGURES / "print"
OUT.mkdir(parents=True, exist_ok=True)

def label(x: int, y: int, text: str, size: int = 25, color: str = "#1d3731", weight: int = 600) -> str:
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(text)}</text>'

def image_data(name: str) -> str:
    return "data:image/png;base64," + base64.b64encode((FIGURES / name).read_bytes()).decode("ascii")

def crop(src: str, x: int, y: int, w: int, h: int, view: tuple[int, int, int, int]) -> str:
    vx, vy, vw, vh = view
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" '
            f'viewBox="{vx} {vy} {vw} {vh}" preserveAspectRatio="xMinYMin meet" overflow="hidden">'
            f'<image x="0" y="0" width="1440" height="900" href="{src}"/></svg>')

def panel(x: int, y: int, w: int, h: int) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff" stroke="#d9e2df" stroke-width="2"/>'

def canvas(height: int, content: list[str]) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{height}" '
            f'viewBox="0 0 1600 {height}"><rect width="1600" height="{height}" fill="#fff"/>'
            + "".join(content) + '</svg>')

def heading(title: str, subtitle: str) -> list[str]:
    return [label(48, 55, title, 36, "#173c32", 700),
            label(48, 91, subtitle, 22, "#5b706a", 400),
            '<line x1="48" y1="112" x2="1552" y2="112" stroke="#cddbd5" stroke-width="2"/>']

def main() -> None:
    nb = image_data("p1-notebook.png")
    p = heading("A shared R session", "P1 · Agent execution and live analysis objects")
    p += [label(48, 157, "A  Agent-attributed cell", 25), panel(48, 175, 1504, 484),
          crop(nb, 50, 177, 1500, 480, (382, 147, 735, 235)),
          label(48, 705, "B  Output and warning", 25), panel(48, 724, 1504, 292),
          crop(nb, 50, 727, 1500, 286, (430, 535, 680, 130)),
          label(48, 1063, "C  Live variables", 25), panel(48, 1082, 728, 335), panel(824, 1082, 728, 335),
          crop(nb, 50, 1084, 724, 282, (1132, 145, 308, 120)),
          crop(nb, 826, 1084, 724, 331, (1132, 605, 308, 141)),
          label(48, 1458, "Selected regions from one Notebook capture; source pixels unchanged.", 19, "#71827d", 400)]
    (OUT / "figure-1-notebook.svg").write_text(canvas(1484, p), encoding="utf-8")

    studio = image_data("p1-studio.png")
    p = heading("One analysis, multiple materials", "P1 · Studio brings project notes, work views and the answer together")
    p += [label(48, 157, "A  Project notes", 25), label(824, 157, "B  Files in the answer", 25),
          panel(48, 176, 728, 660), panel(824, 176, 728, 660),
          crop(studio, 50, 178, 724, 656, (302, 108, 296, 267)),
          crop(studio, 826, 210, 724, 582, (1102, 338, 336, 270)),
          label(48, 879, "C  Workspace context", 25), panel(48, 898, 1504, 315),
          crop(studio, 50, 900, 720, 297, (300, 60, 800, 330)),
          label(830, 965, "Studio overview", 30, "#173c32", 700),
          label(830, 1022, "Project notes", 25, "#354e46", 400),
          label(830, 1072, "Conversation views and timeline", 25, "#354e46", 400),
          label(830, 1122, "Answer files shown above", 25, "#354e46", 400),
          label(48, 1254, "A–C are selected regions of the same Studio capture.", 19, "#71827d", 400)]
    (OUT / "figure-2-studio.svg").write_text(canvas(1276, p), encoding="utf-8")

    graph = image_data("p1-graph.png")
    p = heading("Following findings to their sources", "P1 · Graph distinguishes several kinds of recorded relationship")
    p += [label(48, 157, "A  Question, findings and related materials", 25), panel(48, 176, 1504, 786),
          crop(graph, 50, 178, 1500, 782, (320, 190, 780, 407)),
          label(48, 1007, "B  Finding detail", 25), label(822, 1007, "C  Relationship legend", 25),
          panel(48, 1025, 740, 306), panel(822, 1025, 730, 306),
          crop(graph, 50, 1027, 736, 302, (650, 377, 245, 100)),
          '<line x1="856" y1="1078" x2="916" y2="1078" stroke="#9eaba5" stroke-width="3"/>',
          label(934, 1086, "The Agent reported it", 24, "#354e46", 400),
          '<line x1="856" y1="1131" x2="916" y2="1131" stroke="#9eaba5" stroke-width="3" stroke-dasharray="9 6"/>',
          label(934, 1139, "Named in a command", 24, "#354e46", 400),
          '<line x1="856" y1="1184" x2="916" y2="1184" stroke="#27936b" stroke-width="4" stroke-dasharray="2 6"/>',
          label(934, 1192, "Seen changing on disk", 24, "#354e46", 400),
          '<line x1="856" y1="1237" x2="916" y2="1237" stroke="#d88959" stroke-width="3"/>',
          label(934, 1245, "Written in the notes", 24, "#354e46", 400),
          label(48, 1373, "A and B show the same capture; C redraws its legend for legibility.", 19, "#71827d", 400)]
    (OUT / "figure-3-graph.svg").write_text(canvas(1399, p), encoding="utf-8")

if __name__ == "__main__":
    main()
