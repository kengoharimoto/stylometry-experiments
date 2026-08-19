#!/usr/bin/env python3
"""R2 (no-reuse reframe): per-unit line-bootstrap CIs of drift-axis
percentile, on the fixed map of a given build.

For every unit of the build's manifest: B line-resamples of the unit's own
lines -> profile -> z-score with the build's base stats -> Gower projection
into the build's fixed map -> axis-1 percentile. Same instrument as
complement_halves/bootstrap_cis.py (seed 20260814, pivot shift onto the
exact whole-text estimate), generalized to whole units on either build.
Output feeds the movers table of notes/2026-08-19_noreuse_precedence_
reframe.md: with-reuse vs no-reuse percentile per unit, both CI-grade.

Units with > BLOCK_CAP lines are resampled in blocks of consecutive lines
(ceil(L/BLOCK_CAP) lines per block) — for units that large the CI is tight
regardless and per-line granularity only costs time.

Usage: unit_bootstrap_cis.py w|c withreuse|noreuse [B]
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
FEAT = sys.argv[1] if len(sys.argv) > 1 else 'w'
BUILD = sys.argv[2] if len(sys.argv) > 2 else 'noreuse'
B = int(sys.argv[3]) if len(sys.argv) > 3 else 500
W1 = FEAT == 'w'
MFW = 500
BLOCK_CAP = 2000
RNG = np.random.default_rng(20260814)

if BUILD == 'noreuse':
    CORPUS = ROOT / ('corpus/epic_puranas_unsandhied_noreuse' if W1
                     else 'corpus/epic_puranas_sandhied_noreuse')
    MANIFEST = ROOT / 'manifests/noreuse2026_n126.txt'
    REF = ROOT / ('materials/presentation_2026/figures/mds3d/coords_W1-500_noreuse_n126.tsv'
                  if W1 else 'materials/presentation_2026/figures/mds3d/coords_C3-500ns_noreuse_n126.tsv')
else:
    CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
    MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
    REF = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                  if W1 else 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv')


def word_counts_text(txt):
    return Counter(txt.lower().split())


def trigram_counts_text(txt):
    # article C3 convention: scriptio continua (all whitespace removed)
    txt = re.sub(r'\s+', '', txt.lower())
    return Counter(txt[i:i + 3] for i in range(len(txt) - 2))


count_text = word_counts_text if W1 else trigram_counts_text

manifest = {l.strip().removesuffix('.txt')
            for l in MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}
names, counts, paths = [], [], []
for p in sorted(CORPUS.glob('*.txt')):
    if p.stem in manifest:
        names.append(p.stem)
        counts.append(count_text(p.read_text(encoding='utf-8')))
        paths.append(p)
assert len(names) == len(manifest), sorted(manifest - set(names))

raw = Counter()
for c in counts:
    raw.update(c)
feats = [w for w, _ in raw.most_common(MFW)]
fidx = {f: i for i, f in enumerate(feats)}
totals = [sum(c.values()) for c in counts]
X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])
mu, sd = X.mean(0), X.std(0)
Z = (X - mu) / sd

N = len(names)
D = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)
J = np.eye(N) - 1 / N
Bmat = -0.5 * J @ (D ** 2) @ J
w, V = np.linalg.eigh(Bmat)
idx = np.argsort(w)[::-1][:2]
lam = w[idx]
Y0 = V[:, idx] * np.sqrt(np.maximum(lam, 0))

ref = {}
with open(REF, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        ref[row['text']] = (float(row['x']), float(row['y']))
R = np.array([ref[n] for n in names])
A, Bm = R - R.mean(0), Y0 - Y0.mean(0)
U_, _, Vt_ = np.linalg.svd(Bm.T @ A)
rot = U_ @ Vt_
Y = Bm @ rot + R.mean(0)

D2 = D ** 2
rowm = D2.mean(1)
grand = D2.mean()
base_mean_unrot = Y0.mean(0)
xs = np.sort(Y[:, 0])
Vk = V[:, idx]
sqrt_lam = np.sqrt(np.maximum(lam, 1e-12))


def place_x_many(FV, TOT):
    """axis-1 coords for a batch of profiles: FV (B, MFW) counts, TOT (B,)."""
    Zq = (FV / TOT[:, None] - mu) / sd
    d2 = np.abs(Zq[:, None, :] - Z[None, :, :]).mean(2) ** 2   # (B, N)
    b = -0.5 * (d2 - rowm[None, :] - d2.mean(1, keepdims=True) + grand)
    y = ((b @ Vk) / sqrt_lam - base_mean_unrot) @ rot + R.mean(0)
    return y[:, 0]


def pctile(x):
    return np.minimum(100.0, 100.0 * np.searchsorted(xs, x) / (N - 1))


def get_lines(path):
    lines = [l for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]
    if len(lines) == 1 and W1:      # single-line noreuse unsandhied files
        toks = lines[0].split()
        lines = [' '.join(toks[i:i + 16]) for i in range(0, len(toks), 16)]
    if len(lines) > BLOCK_CAP:
        per = -(-len(lines) // BLOCK_CAP)
        lines = [' '.join(lines[i:i + per]) if W1 else '\n'.join(lines[i:i + per])
                 for i in range(0, len(lines), per)]
    return lines


tag = ('W1' if W1 else 'C3') + '_' + BUILD
out = open(HERE / f'unit_ci_{tag}.tsv', 'w', encoding='utf-8')
out.write('unit\test\tlo\thi\ttokens\tlines\n')
print(f'{tag}, B={B}, {N} units on fixed map of {CORPUS.name}')

for name, path, cfull, tot in zip(names, paths, counts, totals):
    lines = get_lines(path)
    L = len(lines)
    F = np.zeros((L, MFW))
    T = np.zeros(L)
    for i, l in enumerate(lines):
        c = count_text(l)
        T[i] = sum(c.values())
        for k, v in c.items():
            j = fidx.get(k)
            if j is not None:
                F[i, j] = v
    keep = T > 0
    F, T = F[keep], T[keep]
    L = len(T)
    fv = np.zeros(MFW)
    for k, v in cfull.items():
        j = fidx.get(k)
        if j is not None:
            fv[j] = v
    est = pctile(place_x_many(fv[None, :], np.array([float(tot)])))[0]
    est_pad = pctile(place_x_many(F.sum(0)[None, :], np.array([T.sum()])))[0]
    II = RNG.integers(0, L, (B, L))
    FV = np.stack([F[ii].sum(0) for ii in II])
    TT = np.array([T[ii].sum() for ii in II])
    ps = pctile(place_x_many(FV, TT))
    shift = est - est_pad
    lo, hi = np.clip(np.percentile(ps, [2.5, 97.5]) + shift, 0, 100)
    out.write(f'{name}\t{est:.1f}\t{lo:.1f}\t{hi:.1f}\t{tot}\t{L}\n')
    print(f'{name:<52}{est:>6.1f}  [{lo:>5.1f},{hi:>6.1f}]  {tot:>9} tok')
out.close()
print(f'wrote unit_ci_{tag}.tsv')
