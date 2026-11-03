#!/usr/bin/env python3
"""Post-process the pandoc DOCX: restore author superscripts and arrows.

Pandoc drops LaTeX superscripts in \\author blocks and swallows $\\rightarrow$,
so this script rebuilds the author paragraph and restores the arrow glyphs.
"""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.shared import Pt

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "drafts" / "arxiv" / "main.docx"

AUTHORS = [
    ("Yonghe Xia", "1,2"),
    ("   Guangchuang Yu", "1,*"),
]
AFFIL = [
    "1 Department of Bioinformatics, School of Basic Medical Sciences,",
    "   Southern Medical University, Guangzhou, China",
    "2 School of Medicine, Westlake University, Hangzhou, China",
]
CONTACT = [
    "Yonghe Xia: xiayonghe@westlake.edu.cn",
    "* Corresponding author: gcyu1@smuedu.cn",
]


def clear(paragraph):
    """Remove every child element except the paragraph properties.

    Pandoc emits e-mail addresses as w:hyperlink elements, which are not runs,
    so removing runs alone leaves the addresses behind.
    """
    p = paragraph._p
    for child in list(p):
        if child.tag.endswith('}pPr'):
            continue
        p.remove(child)


def main() -> None:
    doc = Document(DOCX)

    # ---- author block (paragraph index 1 in the pandoc output)
    p = doc.paragraphs[1]
    clear(p)
    for name, mark in AUTHORS:
        r = p.add_run(name)
        r.font.size = Pt(12)
        s = p.add_run(mark)
        s.font.superscript = True
        s.font.size = Pt(12)
    for line in AFFIL:
        p.add_run("\n")
        r = p.add_run(line)
        r.font.size = Pt(9)
    for line in CONTACT:
        p.add_run("\n")
        r = p.add_run(line.replace("smuedu", "smu.edu"))
        r.font.size = Pt(9)

    # ---- restore arrows swallowed from $\\rightarrow$
    arrow = "\u2192"
    replacements = {
        "purpose  organization plan  operable interface  sourced shared state  "
        "agent continuation":
            f"purpose {arrow} organization plan {arrow} operable interface {arrow} "
            f"sourced shared state {arrow} agent continuation",
    }
    for para in doc.paragraphs:
        for old, new in replacements.items():
            if old in para.text:
                for run in para.runs:
                    if old in run.text:
                        run.text = run.text.replace(old, new)
                        break
                else:
                    # text is split across runs: flatten this paragraph
                    new_text = para.text.replace(old, new)
                    clear(para)
                    para.add_run(new_text)

    doc.save(DOCX)
    print("post-processed", DOCX)

    # ---- number captions so they agree with the in-text cross references
    doc = Document(DOCX)
    for style, word in (("Image Caption", "Figure"), ("Table Caption", "Table")):
        n = 0
        for para in doc.paragraphs:
            if para.style.name != style or not para.runs:
                continue
            n += 1
            first = para.runs[0]
            first.text = f"{word} {n}. " + first.text
    doc.save(DOCX)
    print("numbered captions")


if __name__ == "__main__":
    main()