#!/usr/bin/env python3
"""A3 (axis-anatomy plan): minimal sufficient feature set.

Greedy forward selection: how few of the 500 features reproduce the
drift axis at rho >= 0.95? Overfitting guard per the plan note: features
are selected to maximize axis agreement on a random half of the units
(seed 20260814) and the stopping criterion is evaluated on the held-out
half; the full-corpus rho for the selected set is reported alongside.
The axis for a candidate set is built exactly as the article's maps are
(z-scored rates, Burrows's Delta, classical MDS, axis 1), on the
evaluation units only, and compared against the committed article-frame
coordinates.

Usage: a3_minimal_set.py w|c   ->  a3_minimal_set_{W1,C3}.tsv

2026-08-29, run for the Indological companion (Kengo's call): the DH
draft stands on A2's redundancy result and does not cite this.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
FEAT = sys.argv[1] if len(sys.argv) > 1 else 'w'
W1 = FEAT == 'w'
MFW = 500
TARGET = 0.95
CAP = 60
SEED = 20260814

BASE_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
COORDS = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                 if W1 else 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv')


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

raw = Counter()
for c in counts:
    raw.update(c)
feats = [w for w, _ in raw.most_common(MFW)]
totals = [sum(c.values()) for c in counts]
X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])

coords = {}
with open(COORDS, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        coords[row['text']] = float(row['x'])
xref = np.array([coords[n] for n in names])

rng = np.random.default_rng(SEED)
perm = rng.permutation(len(names))
A, B = perm[:len(names) // 2], perm[len(names) // 2:]


def axis_rho(unit_idx, feat_idx):
    """Delta+MDS axis 1 on the given units/features vs the reference."""
    Xs = X[np.ix_(unit_idx, feat_idx)]
    mu, sd = Xs.mean(0), Xs.std(0)
    sd[sd == 0] = 1.0
    Z = (Xs - mu) / sd
    D = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)
    n = len(unit_idx)
    J = np.eye(n) - np.ones((n, n)) / n
    Bm = -0.5 * J @ (D ** 2) @ J
    vals, vecs = np.linalg.eigh(Bm)
    ax = vecs[:, -1]
    r = spearmanr(ax, xref[unit_idx]).statistic
    return abs(r)


selected = []
pool = list(range(MFW))
rows = []
print(f'[{ "W1" if W1 else "C3" }] greedy on {len(A)} units, holdout {len(B)}, '
      f'target holdout rho >= {TARGET}')
while len(selected) < CAP:
    best_f, best_r = None, -1.0
    for f in pool:
        r = axis_rho(A, selected + [f])
        if r > best_r:
            best_f, best_r = f, r
    selected.append(best_f)
    pool.remove(best_f)
    r_hold = axis_rho(B, selected)
    r_full = axis_rho(np.arange(len(names)), selected)
    rows.append((len(selected), feats[best_f], best_r, r_hold, r_full))
    print(f'  {len(selected):>2} +{feats[best_f]!r:<12} select-half {best_r:.4f}  '
          f'holdout {r_hold:.4f}  full {r_full:.4f}')
    if r_hold >= TARGET:
        break

tag = 'W1' if W1 else 'C3'
out = HERE / f'a3_minimal_set_{tag}.tsv'
with open(out, 'w', encoding='utf-8') as f:
    f.write('k\tfeature\trho_selecthalf\trho_holdout\trho_full\n')
    for k, feat, ra, rb, rf in rows:
        f.write(f'{k}\t{feat}\t{ra:.4f}\t{rb:.4f}\t{rf:.4f}\n')
print(f'wrote {out.name}: {len(selected)} features reach holdout '
      f'{rows[-1][3]:.4f} (full-corpus {rows[-1][4]:.4f})')
print('the set:', ' '.join(feats[i] for i in selected))
