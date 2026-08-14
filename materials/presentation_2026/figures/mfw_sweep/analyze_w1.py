#!/usr/bin/env python3
"""W1 MFW sweep stability + W1xC3 convergence matrix (dim-1 Spearman)."""
import csv
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).parent
ROOT = Path('/mnt/kengo/stylometry-experiments')
W1S = [30, 50, 80, 120, 200, 300, 500, 800, 1500, 3000, 5000]
C3S = [250, 500, 1000, 2000, 3000, 5000, 8000, 12000]

def load(path):
    d = {}
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            d[row['text']] = (float(row['x']), float(row['y']))
    return d

w1 = {n: load(HERE / f'coords_W1_mfw{n}.tsv') for n in W1S}
c3 = {n: load(HERE / f'coords_mfw{n}.tsv') for n in C3S}
names = sorted(w1[80])
assert all(sorted(v) == names for v in list(w1.values()) + list(c3.values()))

WX = {n: np.array([w1[n][t][0] for t in names]) for n in W1S}
WY = {n: np.array([w1[n][t][1] for t in names]) for n in W1S}
CX = {n: np.array([c3[n][t][0] for t in names]) for n in C3S}

print('W1 stability (x = dim 1):')
print('MFW    rho_x(vs80)  rho_y(vs80)')
for n in W1S:
    sx = spearmanr(WX[n], WX[80]).statistic
    sy = spearmanr(WY[n], WY[80]).statistic
    print(f'{n:<6} {sx:>10.4f} {sy:>12.4f}')

print('\nadjacent steps, rho_x:')
for a, b in zip(W1S, W1S[1:]):
    print(f'  {a:>5} -> {b:<5} {spearmanr(WX[a], WX[b]).statistic:.4f}')

print('\nW1 x C3 convergence, Spearman rho of x (rows = W1 MFW, cols = C3 MFW):')
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
print(f'\nmax convergence: rho = {best[0]:.4f} at W1 mfw={best[1]}, C3 mfw={best[2]}')

# stratum means along x for the W1 sweep
strata = {}
with open(ROOT / 'materials/presentation_2026/chronology_strata.tsv', encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        strata[row['text']] = int(row['stratum'])
print('\nmean x per stratum (columns = W1 MFW):')
print('stratum ' + ''.join(f'{n:>8}' for n in W1S))
for s in sorted(set(strata[t] for t in names)):
    idx = [i for i, t in enumerate(names) if strata[t] == s]
    print(f'{s:>7} ' + ''.join(f'{WX[n][idx].mean():>8.3f}' for n in W1S))

# biggest movers between W1 80 and W1 1500
def ranks(v):
    r = np.empty(len(v)); r[np.argsort(v)] = np.arange(len(v)); return r
r80, r1500 = ranks(WX[80]), ranks(WX[1500])
moves = sorted(zip(np.abs(r80 - r1500), names, r80, r1500), reverse=True)[:10]
print('\nbiggest x-rank movers, W1 80 vs 1500:')
for d, t, ra, rb in moves:
    print(f'  {t:<45} rank {int(ra):>3} -> {int(rb):>3}  (moved {int(d)})')
