# Rho preprint working draft

`main.tex` is the editable manuscript; `references.bib` is its bibliography and
`figures/` contains the four figures used by the manuscript: the argument figure
(`figure-argument.png`), the system figure (`figure-system.pdf`), the P1 judgment
figure (`figure-p1-judgment.png`) and the case-judgment figure
(`figure-case-judgments.png`). The original interface captures and the data
redraws are in `supplementary.tex` / `supplementary.pdf` (Supplementary Figures
S1--S10). The article uses
standard LaTeX packages and a single-column layout. `main.bbl` is the generated
bibliography included in the source archive when available. The preview is a
working draft, not a completed submission. Generated PDFs and the ZIP archive
are kept locally and excluded from version control; the source, bibliography and
figures needed to compile are tracked.

Compile from this directory with a current TeX distribution (for example,
`pdflatex main; bibtex main; pdflatex main; pdflatex main`) or with
`tectonic --keep-intermediates main.tex`. arXiv processes submissions with the
chosen TeX processor, and the generated PDF must be checked during submission;
see [arXiv's TeX submission guidance](https://info.arxiv.org/help/submit_tex.html).

Before submission, publish a stable, versioned record of the five analyses and
reference it in the manuscript; obtain
scientific review of the case claims; and inspect the final arXiv-produced PDF.
The external-agent figure shows the Rho-side view of an external session and a
labelled schematic; an actual capture of the external client's own window remains
a possible addition. No submission is implied by this working draft.

The five source datasets are publicly available from GEO. The local run records
are not yet archived publicly. The figures derived from the P2--P5 project views
were captured after reopening those projects; the P1 live-variable image and the
external ACP screenshot come from earlier recorded episodes. See the manuscript
captions and `docs/PAPER.md` for the evidence boundaries.
