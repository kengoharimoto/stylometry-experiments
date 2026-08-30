#!/usr/bin/env python3
"""B1 (axis-anatomy plan): variance anatomy of the classical MDS.

Eigenvalue spectrum (how much squared-distance variance axis 1 carries,
gap to axis 2), jackknife stability of axis 1 under single-unit deletion,
and grouped-deletion checks for the leverage suspects (Sivadharma pair,
sastra outgroup).

Usage: b1_variance.py w|c [--noreuse]
"""
import csv
import os
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(os.environ.get('STYLO_ROOT', '/mnt/kengo/stylometry-experiments'))
HERE = Path(__file__).parent
NOREUSE = '--noreuse' in sys.argv
argv = [a for a in sys.argv if a != '--noreuse']
FEAT = argv[1] if len(argv) > 1 else 'c'
W1 = FEAT == 'w'
MFW = 500
if W1 and NOREUSE:
    sys.exit('w + --noreuse refused: the no-reuse W1 axis is partly a '
             'length artifact (R1) — run c --noreuse instead')

if NOREUSE:
    BASE_CORPUS = ROOT / 'corpus/epic_puranas_sandhied_noreuse'
    MANIFEST = ROOT / 'manifests/noreuse2026_n126.txt'
else:
    BASE_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
    MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
STRATA = ROOT / 'materials/presentation_2026/chronology_strata.tsv'


def word_counts(path):
    return Counter(path.read_text(encoding='utf-8').lower().split())


def trigram_counts(path):
    txt = re.sub(r'\s+', '', path.read_text(encoding='utf-8').lower())
    return Counter(txt[i:i + 3] for i in range(len(txt) - 2))


count_fn = word_counts if W1 else trigram_counts

manifest = {l.strip().removesuffix('.txt') for l in
            MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}
names, counts = [], []
for p in sorted(BASE_CORPUS.glob('*.txt')):
    if p.stem in manifest:
        names.append(p.stem)
        counts.append(count_fn(p))
assert len(names) == len(manifest)

strata = {}
with open(STRATA, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        strata[row['text']] = int(row['stratum'])


def delta_D(counts_subset):
    raw = Counter()
    for c in counts_subset:
        raw.update(c)
    feats = [w for w, _ in raw.most_common(MFW)]
    totals = [sum(c.values()) for c in counts_subset]
    X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts_subset, totals)])
    Z = (X - X.mean(0)) / X.std(0)
    return np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)


def mds_axes(D, k=2):
    n = len(D)
    J = np.eye(n) - 1 / n
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1]
    return w[idx], V[:, idx[:k]] * np.sqrt(np.maximum(w[idx[:k]], 0))


D = delta_D(counts)
lam, Y = mds_axes(D)
pos = lam[lam > 0]
print(f'eigenvalue spectrum (positive part, {len(pos)} eigenvalues):')
shares = pos / pos.sum()
for i in range(8):
    print(f'  axis {i+1}: {100*shares[i]:.1f}%')
print(f'  axis-1/axis-2 ratio: {pos[0]/pos[1]:.2f}')

x_full = Y[:, 0]
# sign convention: epics (stratum 1) left
epic = np.array([strata[n] == 1 for n in names])
if x_full[epic].mean() > x_full[~epic].mean():
    x_full = -x_full

# jackknife: drop one unit, recompute (features refilled), correlate axis 1
rhos = np.empty(len(names))
l1shares = np.empty(len(names))
for i in range(len(names)):
    sub = [c for j, c in enumerate(counts) if j != i]
    lam_i, Y_i = mds_axes(delta_D(sub), k=1)
    p = lam_i[lam_i > 0]
    l1shares[i] = p[0] / p.sum()
    xi = Y_i[:, 0]
    keep = np.array([j for j in range(len(names)) if j != i])
    r = spearmanr(xi, x_full[keep]).statistic
    rhos[i] = abs(r)          # sign of an eigenvector is arbitrary
order = np.argsort(rhos)
print(f'\njackknife (drop 1 of {len(names)}, features refilled): '
      f'min rho {rhos.min():.4f}, median {np.median(rhos):.4f}')
print('least stable drops:')
for i in order[:5]:
    print(f'  -{names[i]:<46} rho {rhos[i]:.4f}  (axis-1 share {100*l1shares[i]:.1f}%)')
print(f'axis-1 share under jackknife: {100*l1shares.min():.1f}-{100*l1shares.max():.1f}%')

# grouped deletions: leverage suspects
SUSPECTS = {'sastra outgroup (stratum 9)': [n for n in names if strata[n] == 9],
            'Sivadharma pair (stratum 13)': [n for n in names if strata[n] == 13],
            'both': [n for n in names if strata[n] in (9, 13)]}
print('\ngrouped deletions:')
for label, drop in SUSPECTS.items():
    keep_idx = [j for j, n in enumerate(names) if n not in drop]
    sub = [counts[j] for j in keep_idx]
    lam_g, Y_g = mds_axes(delta_D(sub), k=1)
    p = lam_g[lam_g > 0]
    r = abs(spearmanr(Y_g[:, 0], x_full[keep_idx]).statistic)
    print(f'  drop {label:<32} ({len(drop)} units): rho {r:.4f}, '
          f'axis-1 share {100*p[0]/p.sum():.1f}%')

tag = ('W1' if W1 else 'C3') + ('_noreuse' if NOREUSE else '')
with open(HERE / f'b1_jackknife_{tag}_500.tsv', 'w', encoding='utf-8') as f:
    f.write('dropped_unit\trho_x\taxis1_share\n')
    for i in range(len(names)):
        f.write(f'{names[i]}\t{rhos[i]:.4f}\t{l1shares[i]:.4f}\n')
print(f'\nwrote b1_jackknife_{tag}_500.tsv')
