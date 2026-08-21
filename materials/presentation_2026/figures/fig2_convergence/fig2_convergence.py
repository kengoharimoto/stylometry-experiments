#!/usr/bin/env python3
"""Article Figure 2: W1 x C3 axis-1 agreement across the joint sweep (§3.1).

Heatmap of Spearman rho between the W1 drift axis at each MFW setting
(30-5000, 11 settings) and the no-space C3 axis at each feature-count
setting (250-12,000, 8 settings), with-reuse build, 127 units. The
adopted 500x500 cell (rho = 0.953) is outlined.

Inputs are the committed sweep coordinate TSVs, NOT recomputation:
`mfw_sweep/coords_W1_mfw*.tsv` (each setting's own axis, sign-oriented
epics-left — so the W1 failure regimes at 30 and >=1500 MFW show as
the honest fading of the grid's edges) and
`c3_nospace/coords_nospace_mfw*.tsv` (each Procrustes-aligned onto the
W1 hero layout by hero_mds — the article C3 frame convention).

Writes fig2_convergence.png / .pdf, the grid as
fig2_convergence_grid.tsv, and the within-lens stability columns
(each setting's axis vs the adopted 500 setting of its own lens) as
fig2_within_lens.tsv — the citable sources for §3.1's sweep sentences
(these post-clean no-space values supersede the 2026-08-14 note's
pre-clean spaced-C3 sweep, whose W1 decay was quoted vs the 80-MFW
deck hero).
"""
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

import sys
ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts/presentation'))
import figcommon  # noqa: E402  (font setup)

W1_DIR = ROOT / 'materials/presentation_2026/figures/mfw_sweep'
C3_DIR = ROOT / 'materials/presentation_2026/figures/c3_nospace'
W1_MFWS = [30, 50, 80, 120, 200, 300, 500, 800, 1500, 3000, 5000]
C3_MFWS = [250, 500, 1000, 2000, 3000, 5000, 8000, 12000]
ADOPTED = (500, 500)


def load_x(path):
    with open(path, encoding='utf-8') as f:
        return {r['text']: float(r['x']) for r in csv.DictReader(f, delimiter='\t')}


w1 = {m: load_x(W1_DIR / f'coords_W1_mfw{m}.tsv') for m in W1_MFWS}
c3 = {m: load_x(C3_DIR / f'coords_nospace_mfw{m}.tsv') for m in C3_MFWS}
names = sorted(set(w1[500]) & set(c3[500]))
assert len(names) == 127, len(names)

G = np.zeros((len(W1_MFWS), len(C3_MFWS)))
for i, mw in enumerate(W1_MFWS):
    a = np.array([w1[mw][n] for n in names])
    for j, mc in enumerate(C3_MFWS):
        b = np.array([c3[mc][n] for n in names])
        G[i, j] = spearmanr(a, b).statistic

with open(HERE / 'fig2_convergence_grid.tsv', 'w', encoding='utf-8') as f:
    f.write('w1_mfw\\c3_feats\t' + '\t'.join(map(str, C3_MFWS)) + '\n')
    for i, mw in enumerate(W1_MFWS):
        f.write(str(mw) + '\t' + '\t'.join(f'{v:.4f}' for v in G[i]) + '\n')

with open(HERE / 'fig2_within_lens.tsv', 'w', encoding='utf-8') as f:
    f.write('lens\tsetting\trho_vs_adopted_500\n')
    ref = np.array([w1[500][n] for n in names])
    for m in W1_MFWS:
        r = spearmanr(np.array([w1[m][n] for n in names]), ref).statistic
        f.write(f'W1\t{m}\t{r:.4f}\n')
    ref = np.array([c3[500][n] for n in names])
    for m in C3_MFWS:
        r = spearmanr(np.array([c3[m][n] for n in names]), ref).statistic
        f.write(f'C3\t{m}\t{r:.4f}\n')

i0, j0 = W1_MFWS.index(ADOPTED[0]), C3_MFWS.index(ADOPTED[1])
print(f'adopted {ADOPTED}: rho = {G[i0, j0]:.4f}; grid max = {G.max():.4f} '
      f'at W1 {W1_MFWS[int(np.argmax(G) // len(C3_MFWS))]} x '
      f'C3 {C3_MFWS[int(np.argmax(G) % len(C3_MFWS))]}')

fig, ax = plt.subplots(figsize=(8.4, 7.2))
im = ax.imshow(G, cmap='viridis', vmin=0, vmax=1, aspect='auto',
               origin='upper')
for i in range(len(W1_MFWS)):
    for j in range(len(C3_MFWS)):
        v = G[i, j]
        ax.text(j, i, f'{v:.2f}'.lstrip('0') if v >= 0 else f'{v:.2f}',
                ha='center', va='center', fontsize=8.5,
                color='white' if v < 0.6 else 'black')
ax.add_patch(plt.Rectangle((j0 - 0.5, i0 - 0.5), 1, 1, fill=False,
                           edgecolor='#c2185b', lw=2.4))
ax.set_xticks(range(len(C3_MFWS)), [str(m) for m in C3_MFWS], fontsize=9)
ax.set_yticks(range(len(W1_MFWS)), [str(m) for m in W1_MFWS], fontsize=9)
ax.set_xlabel('C3 feature count (character trigrams, no-space)', fontsize=10.5)
ax.set_ylabel('W1 feature count (most frequent words)', fontsize=10.5)
ax.set_title('Cross-lens axis-1 agreement (Spearman ρ), 127 units\n'
             'adopted setting 500 × 500 outlined', fontsize=11, pad=10)
cbar = fig.colorbar(im, ax=ax, shrink=0.85)
cbar.set_label('ρ (W1 axis 1, C3 axis 1)', fontsize=9.5)
fig.tight_layout()
for ext in ('png', 'pdf'):
    fig.savefig(HERE / f'fig2_convergence.{ext}',
                dpi=180 if ext == 'png' else None, facecolor='white')
print('wrote fig2_convergence.png / .pdf / _grid.tsv')
