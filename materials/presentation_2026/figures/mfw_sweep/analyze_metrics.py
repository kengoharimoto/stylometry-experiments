#!/usr/bin/env python3
"""Effect of distance measure on the MDS x-axis, at fixed MFW.

Baselines: the delta runs from the MFW sweeps (W1-500, C3-500, C3-12000).
All layouts were oriented/Procrustes-aligned by hero_mds.py onto the same
W1-delta hero reference, so x is comparable across metrics and runs.
"""
import csv
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).parent
MET = HERE / 'metrics'
METRICS = ['wurzburg', 'argamon', 'eder', 'cosine', 'euclidean',
           'manhattan', 'canberra', 'minmax']

def load_x(path, names=None):
    d = {}
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            d[row['text']] = float(row['x'])
    if names is None:
        names = sorted(d)
    return names, np.array([d[t] for t in names])

names, w1_delta_80 = load_x(HERE / 'coords_W1_delta.tsv')          # deck hero axis
_, w1_delta_500 = load_x(HERE / 'coords_W1_mfw500.tsv', names)
_, c3_delta_500 = load_x(HERE / 'coords_mfw500.tsv', names)
_, c3_delta_12000 = load_x(HERE / 'coords_mfw12000.tsv', names)

CASES = [
    ('W1-500', 'W1_500_{m}.tsv', w1_delta_500),
    ('C3-500', 'C3_500_{m}.tsv', c3_delta_500),
    ('C3-12000', 'C3_12000_{m}.tsv', c3_delta_12000),
]

print('Spearman rho of x: each metric vs delta at same settings | vs W1-80-delta hero')
print(f'{"metric":<11}' + ''.join(f'{c:>22}' for c, _, _ in CASES))
for m in METRICS:
    cells = []
    for _, pat, base in CASES:
        _, x = load_x(MET / pat.format(m=m), names)
        cells.append(f'{spearmanr(x, base).statistic:>10.3f} |{spearmanr(x, w1_delta_80).statistic:>8.3f}')
    print(f'{m:<11}' + ''.join(f'{c:>22}' for c in cells))

print(f'{"delta":<11}' + ''.join(
    f'{"1.000":>10} |{spearmanr(b, w1_delta_80).statistic:>8.3f}'.rjust(22)
    for _, _, b in CASES))

# how much does each metric's C3 axis move when MFW goes 500 -> 12000?
print('\nrho of x, C3-500 vs C3-12000 (same metric) — MFW robustness per metric:')
for m in ['delta'] + METRICS:
    if m == 'delta':
        a, b = c3_delta_500, c3_delta_12000
    else:
        _, a = load_x(MET / f'C3_500_{m}.tsv', names)
        _, b = load_x(MET / f'C3_12000_{m}.tsv', names)
    print(f'  {m:<11} {spearmanr(a, b).statistic:.3f}')
