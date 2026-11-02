#!/usr/bin/env python3
"""Make lossless crops of reopened Rho views and an external-agent evidence figure."""
from pathlib import Path
from html import escape
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import cairosvg
import csv
import math
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / 'work/english-draft/captures'
OUT = ROOT / 'drafts/figures/print'
RHO = ROOT.parent / 'Rho'
OUT.mkdir(parents=True, exist_ok=True)
font = '/System/Library/Fonts/Supplemental/Arial.ttf'
bold = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'

def case(filename, title, subtitle, box, output):
    source = Image.open(CAPTURES / filename).convert('RGB').crop(box)
    width = source.width + 96
    canvas = Image.new('RGB', (width, source.height + 188), 'white')
    d = ImageDraw.Draw(canvas)
    d.text((48, 22), title, font=ImageFont.truetype(bold, 38), fill='#173c32')
    d.text((48, 79), subtitle, font=ImageFont.truetype(font, 25), fill='#60746d')
    d.line((48, 128, width - 48, 128), fill='#cfddd7', width=2)
    canvas.paste(source, (48, 150))
    d.rectangle((47, 149, width - 48, 150 + source.height), outline='#d8e2de', width=2)
    canvas.save(OUT / output, optimize=True)

case('p2-studio-4k.png', 'Single-nucleus analysis', 'P2 | Cell classes and sample-level QC', (2120, 250, 3720, 1910), 'figure-4-p2.png')
case('p5-studio-4k.png', 'A paired patient comparison', 'P5 | The on-treatment result table in a workspace', (880, 250, 2730, 1720), 'figure-7-p5.png')

# Redraw P3's local table as a separate plot: labels in the saved plot overlap.
# The screenshot is retained as an unaltered, separately labelled panel.
table = RHO / 'work/literature-repro/projects/P3-dlbcl-dsp/results/hallmark_ora.csv'
with table.open(newline='') as f:
    rows = [r for r in csv.DictReader(f) if r['p.adjust'] and float(r['p.adjust']) < .05]
rows.sort(key=lambda r: float(r['p.adjust']), reverse=True)
names = ['\n'.join(textwrap.wrap(r['Description'].removeprefix('HALLMARK_').replace('_', ' '), 30)) for r in rows]
ratio = [int(r['GeneRatio'].split('/')[0]) / int(r['GeneRatio'].split('/')[1]) for r in rows]
fig, ax = plt.subplots(figsize=(16, 11), dpi=100)
points = ax.scatter(ratio, range(len(rows)), s=[float(r['Count'])*7 for r in rows],
                    c=[-math.log10(float(r['p.adjust'])) for r in rows], cmap='viridis', edgecolor='#26483e', linewidth=.5)
ax.set_yticks(range(len(rows)), names, fontsize=16)
ax.tick_params(axis='x', labelsize=15)
ax.set_xlabel('Gene ratio among mapped Hallmark-set genes', fontsize=17, labelpad=12)
ax.grid(axis='x', color='#e1e9e5'); ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
bar = fig.colorbar(points, ax=ax, pad=.04, shrink=.75)
bar.set_label('−log10 adjusted P', fontsize=16)
bar.ax.tick_params(labelsize=13)
handles = [ax.scatter([], [], s=n*7, facecolor='#8ca99c', edgecolor='#26483e', linewidth=.5, label=str(n)) for n in (20, 35, 50)]
fig.legend(handles=handles, title='Genes', loc='lower right', bbox_to_anchor=(.98, .02), frameon=False, fontsize=12, title_fontsize=13)
fig.subplots_adjust(left=.33, right=.91, top=.97, bottom=.09)
buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=100); plt.close(fig); buf.seek(0)
plot = Image.open(buf).convert('RGB')
shot = Image.open(CAPTURES / 'p3-studio-4k.png').convert('RGB').crop((2120, 1210, 3720, 1850))
canvas = Image.new('RGB', (1696, 2040), 'white'); draw = ImageDraw.Draw(canvas)
draw.text((48, 22), 'Spatial compartment analysis', font=ImageFont.truetype(bold, 38), fill='#173c32')
draw.text((48, 79), 'P3 | Local table in Rho and a readable redraw of its significant terms', font=ImageFont.truetype(font, 25), fill='#60746d')
draw.line((48, 128, 1648, 128), fill='#cfddd7', width=2)
draw.text((48, 151), 'A  Enrichment table in Studio', font=ImageFont.truetype(bold, 27), fill='#173c32')
canvas.paste(shot, (48, 195))
draw.text((48, 865), 'B  Redrawn from the local result table (BH-adjusted P < 0.05)', font=ImageFont.truetype(bold, 27), fill='#173c32')
canvas.paste(plot, (48, 900))
canvas.save(OUT / 'figure-5-p3.png', optimize=True)

# P4: the original Rho answer is shown above a fresh, labelled redraw of
# selected GSEA rows. This does not change or rerun the source analysis.
data_dir = RHO / 'work/literature-repro/projects/P4-muscle-ec-bulk/results'
rows4 = []
for prefix, filename in [('GO BP', 'gsea_go.csv'), ('KEGG', 'gsea_kegg.csv')]:
    with (data_dir / filename).open(newline='') as f:
        values = [r for r in csv.DictReader(f) if r['p.adjust'] and r['NES'] and r['p.adjust'] != 'NA' and r['NES'] != 'NA']
    values.sort(key=lambda r: float(r['p.adjust']))
    rows4 += [(prefix, r) for r in values[:5]]
rows4.reverse()
labels4 = [p + ' | ' + r['Description'] for p, r in rows4]
fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
ax.scatter([float(r['NES']) for _, r in rows4], range(len(rows4)),
           s=125, color='#3e7e9a', edgecolor='#244f64', linewidth=.8)
ax.set_yticks(range(len(rows4)), labels4, fontsize=15)
ax.set_xlabel('Normalized enrichment score (old vs young)', fontsize=17, labelpad=12)
ax.tick_params(axis='x', labelsize=15); ax.grid(axis='x', color='#e1e9e5'); ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
fig.subplots_adjust(left=.42, right=.97, top=.97, bottom=.12)
buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=100); plt.close(fig); buf.seek(0)
plot4 = Image.open(buf).convert('RGB')
shot4 = Image.open(CAPTURES / 'p4-overview-4k.png').convert('RGB').crop((1530, 200, 3130, 800))
canvas = Image.new('RGB', (1696, 1880), 'white'); draw = ImageDraw.Draw(canvas)
draw.text((48, 22), 'Comparing a published result', font=ImageFont.truetype(bold, 38), fill='#173c32')
draw.text((48, 79), 'P4 | Reported counts and selected pathway results', font=ImageFont.truetype(font, 25), fill='#60746d')
draw.line((48, 128, 1648, 128), fill='#cfddd7', width=2)
draw.text((48, 151), 'A  The agent’s answer in Rho', font=ImageFont.truetype(bold, 27), fill='#173c32')
canvas.paste(shot4, (48, 195))
draw.text((48, 830), 'B  Selected pathways, redrawn from the local result tables', font=ImageFont.truetype(bold, 27), fill='#173c32')
canvas.paste(plot4, (48, 890))
canvas.save(OUT / 'figure-6-p4.png', optimize=True)

# The diagram is explanatory; the lower image is an unaltered crop of a
# separate installed external-Codex acceptance capture, originally 1440x900.
external = Image.open(RHO / 'work/acp-installed-external/2-live-external-plan.png').convert('RGB').crop((300, 200, 1370, 610))
buffer = io.BytesIO()
external.save(buffer, format='PNG')
encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1080" viewBox="0 0 1800 1080">
<rect width="1800" height="1080" fill="white"/>
<g font-family="Arial, sans-serif" fill="#173c32">
<text x="55" y="65" font-size="40" font-weight="700">An Agent can work outside Rho</text>
<text x="55" y="108" font-size="25" fill="#60746d">External Codex ACP episode | explanatory diagram and observed Rho view</text>
<line x1="55" y1="133" x2="1745" y2="133" stroke="#cfddd7" stroke-width="2"/>
<text x="55" y="190" font-size="27" font-weight="700">A  Explicit connection (diagram)</text>
<rect x="55" y="225" width="490" height="173" rx="12" fill="#e7f2ec" stroke="#7ba596" stroke-width="2"/>
<text x="85" y="278" font-size="31" font-weight="700">External Codex client</text>
<text x="85" y="320" font-size="23">Input, permissions and runtime</text><text x="85" y="352" font-size="23">remain in the original client</text>
<rect x="655" y="225" width="425" height="173" rx="12" fill="#f3f7f5" stroke="#aabdb4" stroke-width="2"/>
<text x="685" y="278" font-size="31" font-weight="700">ACP relay</text><text x="685" y="320" font-size="23">Explicitly configured</text><text x="685" y="352" font-size="23">project-scoped observation</text>
<rect x="1190" y="225" width="555" height="173" rx="12" fill="#e7f2ec" stroke="#7ba596" stroke-width="2"/>
<text x="1220" y="278" font-size="31" font-weight="700">Rho project view</text><text x="1220" y="320" font-size="23">Observed plan and file references</text><text x="1220" y="352" font-size="23">without taking over the client</text>
<path d="M565 310 H635 M615 299 L635 310 L615 321 M1100 310 H1170 M1150 299 L1170 310 L1150 321" fill="none" stroke="#3f7864" stroke-width="4"/>
<text x="55" y="467" font-size="27" font-weight="700">B  Rho's view of the live external session (actual capture)</text>
<image x="55" y="500" width="1070" height="410" href="data:image/png;base64,{encoded}"/>
<rect x="54" y="499" width="1072" height="412" fill="none" stroke="#d8e2de" stroke-width="2"/>
<text x="1190" y="560" font-size="26" font-weight="700">What the screenshot shows</text>
<text x="1190" y="604" font-size="23">An external ACP session,</text><text x="1190" y="637" font-size="23">its reported plan, and the</text><text x="1190" y="670" font-size="23">original client's ownership.</text>
<text x="1190" y="750" font-size="23" fill="#60746d">This is Rho's observation,</text><text x="1190" y="783" font-size="23" fill="#60746d">not the external client window.</text>
<text x="55" y="1010" font-size="22" fill="#60746d">The screenshot is a crop of the original 1440 × 900 acceptance capture; the diagram is explanatory.</text>
</g></svg>'''
(OUT / 'figure-8-external-agent.svg').write_text(svg, encoding='utf-8')
cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT / 'figure-8-external-agent.png'))
