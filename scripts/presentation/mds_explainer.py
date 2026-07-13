#!/usr/bin/env python3
"""F4: the "mileage chart -> map" MDS explainer for the chronology presentation.

Left: the actual Burrows's-Delta distances between six landmark texts,
displayed like a road atlas's mileage chart (lower triangle, shaded by
distance). Right: those six numbers flattened into a map by classical MDS,
Procrustes-rotated onto the hero orientation. The full 101x101 analysis is
exactly this, only bigger.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import figcommon as fc

LANDMARKS = [
    ('mahabharata_06-bhismaparvan', 'MBh 6 (Bhīṣma)'),
    ('ramayana_02-ayodhyakanda_a', 'Rām 2 (Ayodhyā)'),
    ('vayupurana', 'Vāyu'),
    ('visnupurana_u', 'Viṣṇu'),
    ('agnipurana_u', 'Agni'),
    ('bhagavatapurana_skandha-10_u', 'BhP 10'),
]

strata, _, _ = fc.load_strata()
names, Yref_full, Dfull = fc.hero_layout()
idx = [names.index(n) for n, _ in LANDMARKS]
D = Dfull[np.ix_(idx, idx)]
labels = [lab for _, lab in LANDMARKS]
cols = [fc.PALETTE[strata[n]] for n, _ in LANDMARKS]

# MDS on just the six texts, oriented like the hero map
Y = fc.cmdscale(D)
Y, _ = fc.procrustes_align(Y, Yref_full[idx])

fig = plt.figure(figsize=(13.33, 7.5))
axt = fig.add_axes([0.055, 0.09, 0.38, 0.65])
axm = fig.add_axes([0.56, 0.12, 0.42, 0.68])

# ── Left: the mileage chart ───────────────────────────────────────────────────
n = len(labels)
axt.set_xlim(-0.5, n - 0.5); axt.set_ylim(n - 0.5, -0.5)
axt.axis('off')
dmin, dmax = D[np.triu_indices(n, 1)].min(), D[np.triu_indices(n, 1)].max()
for i in range(n):
    for j in range(i):
        f = (D[i, j] - dmin) / (dmax - dmin)
        shade = 0.97 - 0.55 * f           # light = near, dark = far
        axt.add_patch(plt.Rectangle((j - 0.47, i - 0.47), 0.94, 0.94,
                                    facecolor=(shade * 0.92, shade * 0.96, shade),
                                    edgecolor='#cccccc', lw=0.6))
        axt.text(j, i, f'{D[i, j]:.2f}', ha='center', va='center',
                 fontsize=13, color='#111111' if f > 0.55 else '#333333')
# names run along the diagonal, road-atlas style
for i, (lab, c) in enumerate(zip(labels, cols)):
    axt.scatter([i], [i], s=80, c=c, edgecolors='white', linewidths=0.8,
                clip_on=False, zorder=3)
    axt.text(i + 0.22, i - 0.10, lab, ha='left', va='bottom', fontsize=12,
             rotation=35, rotation_mode='anchor', color='#222222')
fig.text(0.25, 0.865, 'stylistic distance between six texts\n'
         '(Burrows’s Delta — like a mileage chart)',
         ha='center', va='center', fontsize=12.5)

# ── Middle: the arrow ─────────────────────────────────────────────────────────
fig.text(0.505, 0.47, 'MDS', ha='center', fontsize=15, color='#555555',
         fontweight='bold')
arr = plt.annotate('', xy=(0.555, 0.44), xytext=(0.455, 0.44),
                   xycoords='figure fraction',
                   arrowprops=dict(arrowstyle='-|>', color='#555555', lw=2.2))
fig.text(0.505, 0.40, 'flatten the table\ninto a picture', ha='center',
         fontsize=9.5, color='#777777', style='italic')

# ── Right: the map ────────────────────────────────────────────────────────────
axm.scatter(Y[:, 0], Y[:, 1], s=180, c=cols, edgecolors='white', linewidths=1.2,
            zorder=3)
off = {'MBh 6 (Bhīṣma)': (0, -22), 'Rām 2 (Ayodhyā)': (0, 14),
       'Vāyu': (0, 14), 'Viṣṇu': (0, -22), 'Agni': (0, 14), 'BhP 10': (0, -22)}
for (x, y), lab in zip(Y, labels):
    axm.annotate(lab, (x, y), xytext=off[lab], textcoords='offset points',
                 ha='center', fontsize=12, fontweight='bold', color='#333333')
pad = 0.35
axm.set_xlim(Y[:, 0].min() - pad, Y[:, 0].max() + pad)
axm.set_ylim(Y[:, 1].min() - pad, Y[:, 1].max() + pad)
axm.set_xticks([]); axm.set_yticks([])
for sp in axm.spines.values():
    sp.set_color('#cccccc')
axm.set_title('the map that best honours those distances\n'
              '(near in the table = near on the map)', fontsize=12.5, pad=12)

fig.suptitle('From a table of distances to a map: multidimensional scaling (MDS)',
             fontsize=15, y=0.95)
fig.text(0.5, 0.035, 'the opening map is exactly this, with the full 101 × 101 table',
         ha='center', fontsize=11.5, color='#555555', style='italic')

out = fc.FIGDIR / 'mds_explainer'
fig.savefig(f'{out}.png', dpi=200)
fig.savefig(f'{out}.pdf')
print('wrote', out.with_suffix('.png'))
