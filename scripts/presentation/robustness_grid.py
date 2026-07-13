#!/usr/bin/env python3
"""F2: small-multiples robustness grid for the chronology presentation.

Six MDS panels — words (W1, unsandhied) and character 3-grams (C3, sandhied)
crossed with three distance metrics per row — all stratum-colored with the
hero palette and Procrustes-aligned to the committed hero layout, so the eye
can verify that the seriation axis survives every change of lens.

Metrics chosen to span families (z-scored Delta variants vs. raw-frequency
metrics), not to cherry-pick agreement; each panel reports its Procrustes
similarity to the hero layout.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

import figcommon as fc

PANELS = [                       # (features, metric)
    ('w', 'delta'), ('w', 'wurzburg'), ('w', 'minmax'),
    ('c', 'manhattan'), ('c', 'minmax'), ('c', 'wurzburg'),
]
ROW_DESC = {'w': 'words (unsandhied text, top 80)',
            'c': 'character 3-grams (sandhied text, top 5000)'}

strata, labels_map, _ = fc.load_strata()
names_ref, Yref, _ = fc.hero_layout()

profiles = {f: fc.load_profiles(f) for f in ('w', 'c')}

fig = plt.figure(figsize=(13.33, 7.5))
axes = fig.subplots(2, 3)
fig.subplots_adjust(left=0.045, right=0.995, top=0.90, bottom=0.115,
                    hspace=0.22, wspace=0.06)

for ax, (feats, metric) in zip(axes.flat, PANELS):
    names, _, X, Z = profiles[feats]
    order = [names.index(n) for n in names_ref]
    D = fc.distance_matrix(X, Z, metric)
    Y = fc.cmdscale(D)[order]
    Y, sim = fc.procrustes_align(Y, Yref)
    for s in fc.GROUP_ORDER:
        sel = [i for i, n in enumerate(names_ref) if strata[n] == s]
        ax.scatter(Y[sel, 0], Y[sel, 1], s=26, c=fc.PALETTE[s], alpha=0.9,
                   edgecolors='white', linewidths=0.4, zorder=3)
    hero = feats == 'w' and metric == 'delta'
    ax.set_title(('W1 · ' if feats == 'w' else 'C3 · ') +
                 fc.METRIC_NAMES[metric] + ('   (= the opening map)' if hero else ''),
                 fontsize=10.5, pad=4)
    if not hero:
        ax.text(0.985, 0.02, f'layout agreement with W1 Delta: {sim:.2f}',
                transform=ax.transAxes, ha='right', fontsize=7.5,
                color='#777777')
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color('#cccccc')

for row, feats in enumerate(('w', 'c')):
    axes[row, 0].set_ylabel(ROW_DESC[feats], fontsize=10.5)

fig.suptitle('The same map from six different measurements\n', fontsize=14,
             y=0.985)
fig.text(0.5, 0.925, 'each panel: independent distance table → MDS, '
         'rotated onto the opening map · colors as in the opening map',
         ha='center', fontsize=10, color='#555555')
fig.text(0.5, 0.075, 'horizontal axis in every panel:  earlier  →  later',
         ha='center', fontsize=10.5, style='italic', color='#555555')

group_label = {s: labels_map[next(n for n in names_ref if strata[n] == s)]
               for s in fc.GROUP_ORDER}
handles = [Line2D([], [], marker='o', linestyle='', markersize=6,
                  markerfacecolor=fc.PALETTE[s], markeredgecolor='white',
                  label=group_label[s]) for s in fc.GROUP_ORDER]
fig.legend(handles=handles, loc='lower center', ncol=5, fontsize=8,
           frameon=False, bbox_to_anchor=(0.5, 0.0),
           columnspacing=1.2, handletextpad=0.3)

out = fc.FIGDIR / 'robustness_grid'
fig.savefig(f'{out}.png', dpi=200)
fig.savefig(f'{out}.pdf')
print('wrote', out.with_suffix('.png'))
