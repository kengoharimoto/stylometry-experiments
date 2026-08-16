#!/usr/bin/env python3
"""A1 (axis-anatomy plan): per-feature loading table for the drift axis.

For each of the 500 features, Spearman-correlate its relative rate with
axis-1 (and axis-2) position across the 127 manifest units. Axis positions
are the saved sweet-spot coordinates (W1-500; no-space C3-500), so the
loadings describe exactly the maps the article uses.

Usage: a1_loadings.py w|c
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
FEAT = sys.argv[1] if len(sys.argv) > 1 else 'c'
W1 = FEAT == 'w'
MFW = 500

BASE_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
COORDS = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                 if W1 else 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv')


def word_counts(path):
    return Counter(path.read_text(encoding='utf-8').lower().split())


def trigram_counts(path):
    # article C3 convention: scriptio continua (see c3_nospace note)
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
        coords[row['text']] = (float(row['x']), float(row['y']))
x = np.array([coords[n][0] for n in names])
y = np.array([coords[n][1] for n in names])

# early/late reference groups: bottom and top quartile of x
qx = np.argsort(x)
q1 = qx[:len(names) // 4]           # early pole
q4 = qx[-(len(names) // 4):]        # late pole

rows = []
for j, f in enumerate(feats):
    rx = spearmanr(X[:, j], x).statistic
    ry = spearmanr(X[:, j], y).statistic
    rows.append({'feature': f,
                 'rho_x': rx, 'rho_y': ry,
                 'mean_permille': 1000 * X[:, j].mean(),
                 'early_q_permille': 1000 * X[q1, j].mean(),
                 'late_q_permille': 1000 * X[q4, j].mean()})
rows.sort(key=lambda r: r['rho_x'])

tag = 'W1' if W1 else 'C3'
out = HERE / f'loadings_{tag}_500.tsv'
with open(out, 'w', encoding='utf-8') as f:
    f.write('feature\trho_x\trho_y\tmean_permille\tearly_q_permille\tlate_q_permille\n')
    for r in rows:
        f.write(f"{r['feature']}\t{r['rho_x']:.4f}\t{r['rho_y']:.4f}\t"
                f"{r['mean_permille']:.3f}\t{r['early_q_permille']:.3f}\t"
                f"{r['late_q_permille']:.3f}\n")
print(f'wrote {out.name} ({len(rows)} features)')

absr = np.array([abs(r['rho_x']) for r in rows])
print(f'|rho_x| distribution: median {np.median(absr):.3f}, '
      f'>=0.5: {(absr >= .5).sum()}, >=0.7: {(absr >= .7).sum()}')

print(f'\ntop 25 EARLY-pole features (rate falls with x; early-q vs late-q per-mille):')
for r in rows[:25]:
    print(f"  {r['feature']!r:<10} rho {r['rho_x']:+.3f}   "
          f"{r['early_q_permille']:>8.2f} -> {r['late_q_permille']:>8.2f}")
print(f'\ntop 25 LATE-pole features (rate rises with x):')
for r in rows[-25:][::-1]:
    print(f"  {r['feature']!r:<10} rho {r['rho_x']:+.3f}   "
          f"{r['early_q_permille']:>8.2f} -> {r['late_q_permille']:>8.2f}")
