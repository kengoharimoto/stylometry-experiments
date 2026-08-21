#!/usr/bin/env python3
"""The chronology as a single line: all units on MDS axis 1, with CIs.

One panel per build (C3-500 no-space lens only — the chronology is
trigram-led, and W1-noreuse per-unit positions are R1-gated). Points sit
at their TRUE axis-1 coordinates, so crowding and gaps are real
distances, not rank artifacts: the epic shelf at the far left, the
crowded purāṇic middle, the long sparse late tail.

Uncertainty: the R2 instrument's per-unit 95% line-bootstrap CIs
(`noreuse_reframe/unit_ci_C3_{noreuse,withreuse}.tsv`, fixed-map Gower
projection, B=500, seed 20260814) are native to the percentile scale;
each CI is mapped into coordinate space through the map's own empirical
percentile->coordinate function (monotone interpolation over the sorted
unit coordinates) and drawn as a whisker in a staggered lane below the
line. Sub-3k-word residues are greyed: their whiskers are shown (often
wide) but their positions are not citable (length floor, §3.4).

Sources: axis-1 coordinates from the committed coords TSVs
(`mds3d/coords_C3-500ns_*.tsv`) — the article frame every CI
instrument uses. NOT from the viewer PTS arrays: on the C3 maps the
viewers' in-plane frame is rotated ~22-28 deg from the article's drift
axis (near-degenerate top eigenpair; discovered 2026-08-21 — pairwise
distances are unaffected, axis-1 readings are). Viewer PTS supply only
unit codes and colors here. CIs from the unit_ci TSVs; word counts
from the build's unsandhied corpus. The script asserts the Gower est
percentiles agree with the map ranks.

Writes one_line_C3.png / .pdf next to this script.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts/presentation'))
import figcommon  # noqa: E402  (font setup on import)

MDS3D = ROOT / 'materials/presentation_2026/figures/mds3d'
CIDIR = ROOT / 'materials/presentation_2026/figures/noreuse_reframe'
PANELS = [
    ('article_C3-500ns_noreuse_n126.html', 'coords_C3-500ns_noreuse_n126.tsv',
     'unit_ci_C3_noreuse.tsv', 'corpus/epic_puranas_unsandhied_noreuse',
     'no-reuse build (the chronology of record) — n=126'),
    ('article_C3-500ns_n127.html', 'coords_C3-500ns_n127.tsv',
     'unit_ci_C3_withreuse.tsv', 'corpus/epic_puranas_unsandhied',
     'with-reuse build — n=127'),
]
LABEL_LANES = 7
WHISKER_LANES = 7
GREY = '#c4c4c4'
GREY_TEXT = '#a0a0a0'

fig, axes = plt.subplots(2, 1, figsize=(24, 11))
for ax, (viewer, coord_file, ci_file, corpus, title) in zip(axes, PANELS):
    style = {p['name']: p for p in json.loads(
        re.search(r'const PTS = (\[.*?\]);',
                  (MDS3D / viewer).read_text(encoding='utf-8'),
                  re.S).group(1))}
    pts = []
    for ln in (MDS3D / coord_file).read_text(encoding='utf-8').splitlines()[1:]:
        f = ln.split('\t')
        pts.append({'name': f[0], 'x': float(f[1]),
                    'code': style[f[0]]['code'], 'color': style[f[0]]['color']})
    pts.sort(key=lambda p: p['x'])
    n = len(pts)
    xs = np.array([p['x'] for p in pts])
    pct_grid = np.arange(n) / (n - 1) * 100      # rank pct -> coordinate
    ci = {}
    for ln in (CIDIR / ci_file).read_text(encoding='utf-8').splitlines()[1:]:
        f = ln.split('\t')
        ci[f[0]] = (float(f[1]), float(f[2]), float(f[3]))
    words = {p['name']: len((ROOT / corpus / (p['name'] + '.txt'))
                            .read_text(encoding='utf-8').split()) for p in pts}
    # sanity: the Gower est percentile must agree with the map rank
    est_pct = np.array([ci[p['name']][0] for p in pts])
    drift = np.abs(est_pct - pct_grid).max()
    print(f'{coord_file}: max |Gower est pct - map rank pct| = {drift:.1f}')
    assert drift < 3, 'CI percentiles disagree with map ranks - wrong frame?'

    for i, p in enumerate(pts):
        small = words[p['name']] < 3000
        col = GREY if small else p['color']
        lo, hi = ci[p['name']][1], ci[p['name']][2]
        xlo, xhi = np.interp([lo, hi], pct_grid, xs)
        # label lane above the line
        y_lab = 0.07 + (i % LABEL_LANES) * 0.125
        ax.annotate(p['code'], (p['x'], 0), xytext=(p['x'], y_lab),
                    textcoords='data', rotation=90, ha='center', va='bottom',
                    fontsize=6.4, color=GREY_TEXT if small else '#1a1a1a',
                    arrowprops=dict(arrowstyle='-', lw=0.3, color='#d8d8d8'))
        # CI whisker lane below the line
        y_ci = -0.07 - (i % WHISKER_LANES) * 0.055
        ax.plot([xlo, xhi], [y_ci, y_ci], '-', lw=1.1,
                color=GREY if small else p['color'],
                alpha=0.55 if small else 0.9, solid_capstyle='butt')
        ax.plot([p['x'], p['x']], [0, y_ci], '-', lw=0.25,
                color='#e0e0e0', zorder=0)
        ax.plot(p['x'], y_ci, marker='|', ms=3.5,
                color=GREY if small else p['color'])
        ax.plot(p['x'], 0, 'o', ms=5, color=col, zorder=4,
                markeredgecolor='white', markeredgewidth=0.4)
    ax.axhline(0, color='#3a3a3a', lw=0.9, zorder=1)
    ax.set_ylim(-0.5, 1.02)
    ax.set_yticks([])
    for s in ('left', 'right', 'top'):
        ax.spines[s].set_visible(False)
    ax.set_title(f'C3-500 no-space, {title}', fontsize=12, loc='left',
                 fontweight='bold')
    ax.text(0.0, -0.085, 'early ←', transform=ax.transAxes, fontsize=9.5,
            color='#666666')
    ax.text(1.0, -0.085, '→ late', transform=ax.transAxes, fontsize=9.5,
            color='#666666', ha='right')

fig.suptitle('The chronology as one line: MDS axis 1 (Burrows’s Delta), '
             'true coordinates', fontsize=14, fontweight='bold')
fig.text(0.5, 0.005,
         'Whiskers: 95% line-bootstrap CIs (fixed-map Gower projection, '
         'B=500, seed 20260814), mapped from the percentile scale into '
         'coordinate space through the map’s own rank–coordinate '
         'function.  Grey: sub-3k-word units/residues — shown with their '
         'intervals, positions not citable (length floor).',
         fontsize=8.5, color='#777777', ha='center')
fig.tight_layout(rect=(0, 0.015, 1, 0.965))
for ext in ('png', 'pdf'):
    fig.savefig(HERE / f'one_line_C3.{ext}',
                dpi=170 if ext == 'png' else None)
print('wrote one_line_C3.png / .pdf')
