#!/usr/bin/env python3
"""Colophon-stripped C3 check: how much of the map do chapter colophons carry?

The A2 bridge (2026-08-16) showed several strong late-pole C3 trigrams feed
on chapter-colophon formulas (adhyāyaḥ, mahāpurāṇe...). Colophons are
transmission paratext, not composition language. Here every colophon line
is dropped in memory (patterns validated against the corpus: iti-initial
lines with genre markers; fused itiśrī...; bare chapter-number lines ending
in (')dhyāyaḥ; samāpta-type enders), the no-space C3-500 map is rebuilt on
the stripped text, Procrustes-oriented onto the adopted no-space frame, and
compared.
"""
import csv
import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
MFW = 500
CORPUS = ROOT / 'corpus/epic_puranas_sandhied'
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
REF_COORDS = ROOT / 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv'
W1_COORDS = ROOT / 'materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'

STRICT = re.compile(r'^\s*iti\b.*(purāṇ|adhyāy|dhyāyaḥ|sarga|parva|kāṇḍ|'
                    r'saṃhitā|khaṇḍ|māhātmy|śāstre|samāpt|prakaraṇ|paṭal)', re.I)
FUSED = re.compile(r'^\s*itiśrī', re.I)
LOOSE = re.compile(r"(adhyāyaḥ|'dhyāyaḥ)\s*$")
ENDER = re.compile(r'(sargaḥ|paṭalaḥ|samāptaḥ|samāptam|prakaraṇam)\s*$')


def is_colophon(line):
    return bool(STRICT.search(line) or FUSED.search(line)
                or LOOSE.search(line) or ENDER.search(line))


def trigrams(txt):
    txt = re.sub(r'\s+', '', txt.lower())
    return Counter(txt[i:i + 3] for i in range(len(txt) - 2))


manifest = {l.strip().removesuffix('.txt') for l in
            MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}

names, counts, colofrac = [], [], {}
for p in sorted(CORPUS.glob('*.txt')):
    if p.stem not in manifest:
        continue
    lines = p.read_text(encoding='utf-8').splitlines()
    keep, dropped = [], []
    for l in lines:
        (dropped if is_colophon(l) else keep).append(l)
    nk = sum(len(l.split()) for l in keep)
    nd = sum(len(l.split()) for l in dropped)
    colofrac[p.stem] = nd / (nk + nd) if nk + nd else 0.0
    names.append(p.stem)
    counts.append(trigrams('\n'.join(keep)))
assert len(names) == len(manifest)

raw = Counter()
for c in counts:
    raw.update(c)
feats = [w for w, _ in raw.most_common(MFW)]
totals = [sum(c.values()) for c in counts]
X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])
Z = (X - X.mean(0)) / X.std(0)
N = len(names)
D = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)
J = np.eye(N) - 1 / N
B = -0.5 * J @ (D ** 2) @ J
w, V = np.linalg.eigh(B)
idx = np.argsort(w)[::-1][:2]
Y = V[:, idx] * np.sqrt(np.maximum(w[idx], 0))


def load(p):
    with open(p, encoding='utf-8') as f:
        return {r['text']: (float(r['x']), float(r['y']))
                for r in csv.DictReader(f, delimiter='\t')}


ref = load(REF_COORDS)
w1 = load(W1_COORDS)
R = np.array([ref[n] for n in names])
A, Bm = R - R.mean(0), Y - Y.mean(0)
U_, _, Vt_ = np.linalg.svd(Bm.T @ A)
Y = Bm @ (U_ @ Vt_) + R.mean(0)

x_new = Y[:, 0]
x_old = np.array([ref[n][0] for n in names])
x_w1 = np.array([w1[n][0] for n in names])

print(f'colophon fraction: corpus-wide '
      f'{np.mean([colofrac[n] for n in names]):.2%} of words; '
      f'{sum(1 for n in names if colofrac[n] > 0)} units affected, max '
      f'{max(colofrac, key=colofrac.get)} {max(colofrac.values()):.1%}')
print(f'rho_x(stripped, adopted C3): {spearmanr(x_new, x_old).statistic:.4f}')
print(f'rho_x(stripped, W1-500):     {spearmanr(x_new, x_w1).statistic:.4f}')
print(f'rho_x(adopted,  W1-500):     {spearmanr(x_old, x_w1).statistic:.4f}')


def pct(v, i):
    return 100 * (v < v[i]).sum() / (len(v) - 1)


shift = np.array([pct(x_new, i) - pct(x_old, i) for i in range(N)])
cf = np.array([colofrac[n] for n in names])
print(f'rho(colophon fraction, x-percentile shift): '
      f'{spearmanr(cf, shift).statistic:.3f}')
order = np.argsort(-np.abs(shift))
print('\nbiggest percentile movers (adopted -> stripped; colophon frac):')
for i in order[:12]:
    print(f'  {names[i]:<48} {pct(x_old,i):>4.0f} -> {pct(x_new,i):>4.0f}  '
          f'({shift[i]:+.0f})   colo {100*cf[i]:.1f}%')

with open(HERE / 'coords_nocolophon_mfw500.tsv', 'w', encoding='utf-8') as f:
    f.write('text\tx\ty\tcolophon_frac\n')
    for n, (x, yy) in zip(names, Y):
        f.write(f'{n}\t{x:.6f}\t{yy:.6f}\t{colofrac[n]:.4f}\n')
print('\nwrote coords_nocolophon_mfw500.tsv')
