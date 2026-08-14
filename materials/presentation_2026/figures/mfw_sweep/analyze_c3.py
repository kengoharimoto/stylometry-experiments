#!/usr/bin/env python3
"""Stability of the C3-delta MDS across MFW settings.

All coordinate sets were Procrustes-aligned by hero_mds.py onto the same
W1-delta reference layout, so x is directly comparable across runs.
"""
import csv
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).parent
ROOT = Path('/mnt/kengo/stylometry-experiments')
MFWS = [250, 500, 1000, 2000, 3000, 5000, 8000, 12000]

def load(path):
    d = {}
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            d[row['text']] = (float(row['x']), float(row['y']))
    return d

coords = {n: load(HERE / f'coords_mfw{n}.tsv') for n in MFWS}
w1 = load(HERE / 'coords_W1_delta.tsv')
names = sorted(coords[5000])
assert all(sorted(c) == names for c in coords.values()) and sorted(w1) == names

X = {n: np.array([coords[n][t][0] for t in names]) for n in MFWS}
Y = {n: np.array([coords[n][t][1] for t in names]) for n in MFWS}
w1x = np.array([w1[t][0] for t in names])

strata = {}
with open(ROOT / 'materials/presentation_2026/chronology_strata.tsv', encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        strata[row['text']] = int(row['stratum'])

print('MFW    r_x(vs5000)  rho_x(vs5000)  rho_x(vsW1)  rho_y(vs5000)')
for n in MFWS:
    rx = np.corrcoef(X[n], X[5000])[0, 1]
    sx = spearmanr(X[n], X[5000]).statistic
    sw = spearmanr(X[n], w1x).statistic
    sy = spearmanr(Y[n], Y[5000]).statistic
    print(f'{n:<6} {rx:>10.4f} {sx:>13.4f} {sw:>12.4f} {sy:>14.4f}')

print('\nadjacent steps, rho_x:')
for a, b in zip(MFWS, MFWS[1:]):
    print(f'  {a:>5} -> {b:<5} {spearmanr(X[a], X[b]).statistic:.4f}')

# mean x per stratum: does the left-to-right stratum ordering hold?
print('\nmean x per stratum (columns = MFW):')
groups = sorted(set(strata[t] for t in names))
hdr = 'stratum ' + ''.join(f'{n:>9}' for n in MFWS) + '      W1'
print(hdr)
for s in groups:
    idx = [i for i, t in enumerate(names) if strata[t] == s]
    row = ''.join(f'{X[n][idx].mean():>9.3f}' for n in MFWS)
    print(f'{s:>7} {row}{w1x[idx].mean():>8.3f}')

# biggest movers in x-rank between 250 and 5000
def ranks(v):
    r = np.empty(len(v)); r[np.argsort(v)] = np.arange(len(v)); return r
r250, r5000 = ranks(X[250]), ranks(X[5000])
moves = sorted(zip(np.abs(r250 - r5000), names, r250, r5000), reverse=True)[:12]
print('\nbiggest x-rank movers, MFW 250 vs 5000 (of %d texts):' % len(names))
for d, t, ra, rb in moves:
    print(f'  {t:<45} rank {int(ra):>3} -> {int(rb):>3}  (moved {int(d)})')
