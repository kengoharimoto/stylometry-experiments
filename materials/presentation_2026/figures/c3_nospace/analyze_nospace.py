#!/usr/bin/env python3
"""Does word division drive the C3 map? No-space (scriptio continua) check.

Spaces in the romanized sandhied text are editorial (manuscripts have no
word division; recitation pauses need not match). hero_mds.py --strip-spaces
recomputes the C3 maps on the continuous character stream; all coordinate
sets are Procrustes-aligned onto the same W1-delta reference, so x is
directly comparable with the standard (space-bearing) mfw_sweep coords.
"""
import csv
import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).parent
SWEEP = HERE.parent / 'mfw_sweep'
ROOT = Path('/mnt/kengo/stylometry-experiments')
CORPUS = ROOT / 'corpus/epic_puranas_sandhied'
MANIFEST = {l.strip().removesuffix('.txt') for l in
            (ROOT / 'manifests/dicsep2026_n127_ppl.txt').read_text().splitlines()
            if l.strip() and not l.startswith('#')}
MFWS = [250, 500, 1000, 5000]


def load(path):
    with open(path, encoding='utf-8') as f:
        return {r['text']: (float(r['x']), float(r['y']))
                for r in csv.DictReader(f, delimiter='\t')}


std = {n: load(SWEEP / f'coords_mfw{n}.tsv') for n in MFWS}
nsp = {n: load(HERE / f'coords_nospace_mfw{n}.tsv') for n in MFWS}
w1 = load(SWEEP / 'coords_W1_delta.tsv')       # W1-80 hero reference
w1_500 = load(SWEEP / 'coords_W1_mfw500.tsv')  # W1 sweet spot
names = sorted(w1)
assert all(sorted(c) == names for c in std.values())
assert all(sorted(c) == names for c in nsp.values())

sx = {n: np.array([std[n][t][0] for t in names]) for n in MFWS}
nx = {n: np.array([nsp[n][t][0] for t in names]) for n in MFWS}
ny = {n: np.array([nsp[n][t][1] for t in names]) for n in MFWS}
sy = {n: np.array([std[n][t][1] for t in names]) for n in MFWS}
w1x = np.array([w1[t][0] for t in names])

print('MFW    rho_x(nospace,std)  rho_x(nospace,W1)  rho_x(std,W1)  rho_y(nospace,std)')
for n in MFWS:
    a = spearmanr(nx[n], sx[n]).statistic
    b = spearmanr(nx[n], w1x).statistic
    c = spearmanr(sx[n], w1x).statistic
    d = spearmanr(ny[n], sy[n]).statistic
    print(f'{n:<6} {a:>18.4f} {b:>17.4f} {c:>13.4f} {d:>18.4f}')

w5x = np.array([w1_500[t][0] for t in names])
print('\nsweet-spot convergence vs W1-500: '
      f'std C3-500 rho {spearmanr(sx[500], w5x).statistic:.4f}, '
      f'nospace C3-500 rho {spearmanr(nx[500], w5x).statistic:.4f}')

# stratum ordering on x
strata = {}
with open(ROOT / 'materials/presentation_2026/chronology_strata.tsv',
          encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        strata[row['text']] = int(row['stratum'])
groups = sorted(set(strata[t] for t in names))
print('\nmean x per stratum (500): std | nospace')
for s in groups:
    idx = [i for i, t in enumerate(names) if strata[t] == s]
    print(f'  {s:>2}  {sx[500][idx].mean():>7.3f}  {nx[500][idx].mean():>7.3f}')

# biggest movers in x-rank at the sweet spot
r_std = np.argsort(np.argsort(sx[500]))
r_nsp = np.argsort(np.argsort(nx[500]))
dr = r_nsp - r_std
order = np.argsort(-np.abs(dr))
print('\nbiggest x-rank movers, std -> nospace (MFW 500):')
for i in order[:12]:
    print(f'  {names[i]:<40} {r_std[i]:>3} -> {r_nsp[i]:>3}  ({dr[i]:+d})')

# feature-list anatomy: how space-bound is the standard top-500?
texts = {}
for p in sorted(CORPUS.glob('*.txt')):
    if p.stem in MANIFEST:
        texts[p.stem] = p.read_text(encoding='utf-8').lower()
raw_std, raw_nsp = Counter(), Counter()
for t in texts.values():
    s = re.sub(r'\s+', ' ', t).strip()
    raw_std.update(s[i:i + 3] for i in range(len(s) - 2))
    c = re.sub(r'\s+', '', t)
    raw_nsp.update(c[i:i + 3] for i in range(len(c) - 2))
for n in [500]:
    top_std = [g for g, _ in raw_std.most_common(n)]
    top_nsp = [g for g, _ in raw_nsp.most_common(n)]
    spaced = [g for g in top_std if ' ' in g]
    shared = set(g for g in top_std if ' ' not in g) & set(top_nsp)
    print(f'\ntop-{n} anatomy: {len(spaced)} of the standard top-{n} contain a '
          f'space ({len(spaced)/n:.0%});')
    print(f'  space-free overlap std∩nospace: {len(shared)}')
    print(f'  examples of space-bearing top features: '
          f'{[repr(g) for g in spaced[:12]]}')
