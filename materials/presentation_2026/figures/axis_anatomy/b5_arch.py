#!/usr/bin/env python3
"""B5 (axis-anatomy plan): the Guttman-arch check.

Classical MDS bends a single strong gradient into axis 2 (horseshoe
effect). Fit y ~ quadratic(x) across the manifest units, both lenses: the
R^2 of that fit is the fraction of the y-axis that is the x-axis folded
over, and must be measured before interpreting y at all. Gates all of Q3.
"""
import csv
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

import os
ROOT = Path(os.environ.get('STYLO_ROOT', '/mnt/kengo/stylometry-experiments'))
HERE = Path(__file__).parent
COORDS = {
    'W1-500': ROOT / 'materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv',
    'C3-500 (no-space)': ROOT / 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv',
}


def load(p):
    with open(p, encoding='utf-8') as f:
        return {r['text']: (float(r['x']), float(r['y']))
                for r in csv.DictReader(f, delimiter='\t')}


maps = {k: load(p) for k, p in COORDS.items()}
names = sorted(next(iter(maps.values())))
assert all(sorted(m) == names for m in maps.values())

resid = {}
print(f'{"lens":<20} {"R2 quad":>8} {"R2 lin":>8} {"quad coeff sign":>16}')
for k, m in maps.items():
    x = np.array([m[n][0] for n in names])
    y = np.array([m[n][1] for n in names])
    cq = np.polyfit(x, y, 2)
    yq = np.polyval(cq, x)
    r2q = 1 - ((y - yq) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    cl = np.polyfit(x, y, 1)
    r2l = 1 - ((y - np.polyval(cl, x)) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    resid[k] = y - yq
    print(f'{k:<20} {r2q:>8.3f} {r2l:>8.3f} {"+" if cq[0] > 0 else "-":>16}')

# cross-lens agreement of y, raw and arch-detrended (preview of C2)
k1, k2 = list(maps)
y1 = np.array([maps[k1][n][1] for n in names])
y2 = np.array([maps[k2][n][1] for n in names])
print(f'\ncross-lens rho_y raw:       {spearmanr(y1, y2).statistic:.4f}')
print(f'cross-lens rho_y detrended: {spearmanr(resid[k1], resid[k2]).statistic:.4f}')

with open(HERE / 'b5_arch_residuals.tsv', 'w', encoding='utf-8') as f:
    f.write('text\ty_detrended_W1\ty_detrended_C3\n')
    for i, n in enumerate(names):
        f.write(f'{n}\t{resid[k1][i]:.6f}\t{resid[k2][i]:.6f}\n')
print('wrote b5_arch_residuals.tsv')
