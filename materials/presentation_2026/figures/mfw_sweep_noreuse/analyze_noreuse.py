#!/usr/bin/env python3
"""Noreuse-build MFW sweeps: stability, W1xC3 convergence, and comparison
with the reuse-in (dicsep2026_n127_ppl) sweeps on the 126 shared texts."""
import csv
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).parent                     # noreuse coords
MAIN = HERE.parent / 'mfw_sweep'                 # reuse-in coords
C3S = [250, 500, 1000, 2000, 3000, 5000, 8000, 12000]
W1S = [30, 50, 80, 120, 200, 300, 500, 800, 1500, 3000, 5000]

def load(path):
    d = {}
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            d[row['text']] = (float(row['x']), float(row['y']))
    return d

c3 = {n: load(HERE / f'coords_mfw{n}.tsv') for n in C3S}
w1 = {n: load(HERE / f'coords_W1_mfw{n}.tsv') for n in W1S}
names = sorted(w1[80])
assert all(sorted(v) == names for v in list(w1.values()) + list(c3.values()))
CX = {n: np.array([c3[n][t][0] for t in names]) for n in C3S}
CY = {n: np.array([c3[n][t][1] for t in names]) for n in C3S}
WX = {n: np.array([w1[n][t][0] for t in names]) for n in W1S}
w1hero = WX[80]

print(f'{len(names)} texts (noreuse2026_n126)\n')
print('C3 noreuse stability:')
print('MFW    rho_x(vs5000)  rho_x(vsW1-80)  rho_y(vs5000)')
for n in C3S:
    print(f'{n:<6} {spearmanr(CX[n], CX[5000]).statistic:>10.4f}'
          f' {spearmanr(CX[n], w1hero).statistic:>14.4f}'
          f' {spearmanr(CY[n], CY[5000]).statistic:>14.4f}')

print('\nW1 noreuse stability:')
print('MFW    rho_x(vs80)')
for n in W1S:
    print(f'{n:<6} {spearmanr(WX[n], WX[80]).statistic:>10.4f}')

print('\nW1 x C3 convergence (noreuse), Spearman rho of x:')
print('        ' + ''.join(f'{c:>8}' for c in C3S))
best = (0, None, None)
for m in W1S:
    row = []
    for c in C3S:
        r = spearmanr(WX[m], CX[c]).statistic
        row.append(r)
        if r > best[0]:
            best = (r, m, c)
    print(f'{m:>6}  ' + ''.join(f'{r:>8.3f}' for r in row))
print(f'max convergence: rho = {best[0]:.4f} at W1 mfw={best[1]}, C3 mfw={best[2]}')

# cross-build: noreuse vs reuse-in x at matched MFW, 126 shared texts
mc3 = {n: load(MAIN / f'coords_mfw{n}.tsv') for n in C3S}
mw1 = {n: load(MAIN / f'coords_W1_mfw{n}.tsv') for n in W1S}
shared = [t for t in names if t in mc3[5000]]
print(f'\ncross-build (noreuse vs reuse-in), {len(shared)} shared texts, rho of x:')
print('C3:  ' + '  '.join(
    f'{n}:{spearmanr([c3[n][t][0] for t in shared], [mc3[n][t][0] for t in shared]).statistic:.3f}'
    for n in C3S))
print('W1:  ' + '  '.join(
    f'{n}:{spearmanr([w1[n][t][0] for t in shared], [mw1[n][t][0] for t in shared]).statistic:.3f}'
    for n in W1S))
