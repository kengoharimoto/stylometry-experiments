#!/usr/bin/env python3
"""Article Figure 1: the two hero maps side by side (§3.1).

C3-500 no-space (char trigrams, whitespace-stripped sandhied stream)
and W1-500 (word unigrams, ByT5-unsandhied), CLEANED build (reuse
stripped, colophon-free), manifest noreuse2026_n126 — the convergence
exhibit: two feature systems with almost no shared linguistic
material, one ordering (axis-1 Spearman rho = 0.93, quoted in the
caption/text, not drawn). C3 is panel (a): the cleaned chronology is
trigram-led (art. §3.4). Units whose residues fall below the ~3k-word
floor are faded (art. §3.4 discipline).

Coordinates come from the committed article-frame coords TSVs (the
frame of record — NOT recomputed here):
`mds3d/coords_C3-500ns_noreuse_n126.tsv` and
`mds3d/coords_W1-500_noreuse_n126.tsv`. Codes and strata colors from
figcommon. Greedy label placement (above/below/right/left, first
non-colliding slot). Print styling: white ground, equal aspect, shared
legend, per-panel "earlier -> later" arrow.

Writes fig1_map_pair.png / .pdf next to this script.
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os
ROOT = Path(os.environ.get('STYLO_ROOT', '/mnt/kengo/stylometry-experiments'))
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts/presentation'))
import figcommon  # noqa: E402

PANELS = [
    ('(a)  C3-500 — character trigrams on the undivided sandhied stream',
     ROOT / 'materials/presentation_2026/figures/mds3d/coords_C3-500ns_noreuse_n126.tsv'),
    ('(b)  W1-500 — word unigrams on unsandhied text',
     ROOT / 'materials/presentation_2026/figures/mds3d/coords_W1-500_noreuse_n126.tsv'),
]
# sub-floor residues (art. §3.4): faded markers/labels
FLOOR = 3000
subfloor = set()
with open(ROOT / 'materials/presentation_2026/figures/noreuse_reframe/unit_ci_W1_noreuse.tsv',
          encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        if float(r['tokens']) < FLOOR:
            subfloor.add(r['unit'])
LEGEND = [
    (1, 'Mahābhārata'), (2, 'Rāmāyaṇa'), (3, 'old purāṇic core'),
    (4, 'old Skandapurāṇa'), (5, 'sectarian & encyclopedic'),
    (6, 'Śivapurāṇa'), (7, 'Bhāgavata'), (8, 'BhP + commentary'),
    (9, 'śāstra'), (10, 'Skāndamahāpurāṇa'), (11, 'epic Appendix I'),
    (12, 'Harivaṃśa'), (13, 'Śivadharma'), (14, 'Purāṇapañcalakṣaṇa'),
]

strata = {}
with open(ROOT / 'materials/presentation_2026/chronology_strata.tsv',
          encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        strata[r['text']] = int(r['stratum'])

fig, axes = plt.subplots(1, 2, figsize=(14, 8))
for ax, (title, coords) in zip(axes, PANELS):
    pts = []
    with open(coords, encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            pts.append((r['text'], float(r['x']), float(r['y'])))
    xs = [p[1] for p in pts]
    ys = [p[2] for p in pts]
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    CH_W, CH_H = 0.0105 * span, 0.019 * span    # per-char width, line height
    # occupied boxes: seed with every marker so labels avoid points too
    placed = [(x - CH_W, y - CH_H * 0.6, x + CH_W, y + CH_H * 0.6)
              for _, x, y in pts]
    OFFSETS = [(0, 1.0), (0, -1.0), (1, 0.35), (-1, 0.35),
               (1, -0.35), (-1, -0.35), (0, 1.9), (0, -1.9),
               (1, 1.0), (-1, 1.0), (1, -1.0), (-1, -1.0),
               (0, 2.8), (0, -2.8)]

    def collides(box):
        x0, y0, x1, y1 = box
        return any(x0 < b[2] and x1 > b[0] and y0 < b[3] and y1 > b[1]
                   for b in placed)

    for name, x, y in pts:
        col = figcommon.PALETTE.get(strata.get(name, 0), '#999999')
        code = figcommon.code(name)
        faded = name in subfloor
        ax.plot(x, y, 'o', ms=5.5, color=col, zorder=3,
                alpha=0.25 if faded else 1.0,
                markeredgecolor='white', markeredgewidth=0.5)
        w = len(code) * CH_W
        for k, (dx, dy) in enumerate(OFFSETS):
            lx = x + dx * (w / 2 + CH_W * 1.6)
            ly = y + dy * CH_H * 1.15
            box = (lx - w / 2, ly - CH_H / 2, lx + w / 2, ly + CH_H / 2)
            if not collides(box) or k == len(OFFSETS) - 1:
                placed.append(box)
                ax.annotate(code, (x, y), xytext=(lx, ly),
                            textcoords='data', ha='center', va='center',
                            fontsize=5.4, fontweight='bold', color=col,
                            alpha=0.35 if faded else 1.0, zorder=4)
                break
    ax.set_title(title, fontsize=10.5, loc='left', pad=8)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.margins(0.04)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.annotate('', xy=(0.63, 0.015), xytext=(0.37, 0.015),
                xycoords='axes fraction',
                arrowprops=dict(arrowstyle='->', color='#666666', lw=1.0))
    ax.text(0.5, 0.033, 'earlier → later', transform=ax.transAxes,
            ha='center', fontsize=9, color='#666666', style='italic')

handles = [plt.Line2D([], [], marker='o', ls='', ms=6,
                      color=figcommon.PALETTE[s], label=lab)
           for s, lab in LEGEND]
fig.legend(handles=handles, loc='lower center', ncol=5, fontsize=8.5,
           frameon=False, handletextpad=0.25, columnspacing=1.2,
           bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(rect=(0, 0.09, 1, 0.98))
for ext in ('png', 'pdf'):
    fig.savefig(HERE / f'fig1_map_pair.{ext}',
                dpi=180 if ext == 'png' else None, facecolor='white')
print('wrote fig1_map_pair.png / .pdf')
