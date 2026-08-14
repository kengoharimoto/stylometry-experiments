#!/usr/bin/env python3
"""Vamsa genre control: project each panel text's genealogy-like half (gen)
and remainder (rest) into the fixed sweet-spot map; line-bootstrap CIs.

Delta = pct(gen) - pct(rest) estimates the genre pull for that text. Same
projection/bootstrap machinery as complement_halves/bootstrap_cis.py.

Usage: genre_project.py w|c [B]
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
FEAT = sys.argv[1] if len(sys.argv) > 1 else 'c'
B = int(sys.argv[2]) if len(sys.argv) > 2 else 200
W1 = FEAT == 'w'
MFW = 500
RNG = np.random.default_rng(20260814)

BASE_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
GEN_CORPUS = ROOT / ('corpus/e1_apparatus_unsandhied' if W1 else 'corpus/e1_apparatus_sandhied')
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
REF_COORDS = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                     if W1 else 'materials/presentation_2026/figures/mfw_sweep/coords_mfw500.tsv')

PANEL = ['mahabharata_15-asramavasikaparvan', 'mahabharata_16-mausalaparvan',
         'mahabharata_17-mahaprasthanikaparvan',
         'mahabharata_18-svargarohanaparvan', 'mahabharata_13-anusasanaparvan']

def word_counts_text(txt):
    return Counter(txt.lower().split())

def trigram_counts_text(txt):
    txt = re.sub(r'\s+', ' ', txt.lower()).strip()
    return Counter(txt[i:i + 3] for i in range(len(txt) - 2))

count_text = word_counts_text if W1 else trigram_counts_text

manifest = {l.strip()[:-4] if l.strip().endswith('.txt') else l.strip()
            for l in MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}
names, counts = [], []
for p in sorted(BASE_CORPUS.glob('*.txt')):
    if p.stem in manifest:
        names.append(p.stem)
        counts.append(count_text(p.read_text(encoding='utf-8')))
assert len(names) == len(manifest)

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
with open(REF_COORDS, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        ref[row['text']] = (float(row['x']), float(row['y']))
R = np.array([ref[n] for n in names])
A, Bm = R - R.mean(0), Y0 - Y0.mean(0)
U_, _, Vt_ = np.linalg.svd(Bm.T @ A)
rot = U_ @ Vt_
Y = Bm @ rot + R.mean(0)
print(f'base map vs saved sweet-spot coords: r_x = {np.corrcoef(Y[:,0], R[:,0])[0,1]:.4f}')

D2 = D ** 2
rowm = D2.mean(1)
grand = D2.mean()
base_mean_unrot = Y0.mean(0)
xs = np.sort(Y[:, 0])
Vk = V[:, idx]
sqrt_lam = np.sqrt(np.maximum(lam, 1e-12))

def place_x(fv, tot):
    z = (fv / tot - mu) / sd
    d2 = (np.abs(z[None, :] - Z).mean(1)) ** 2
    b = -0.5 * (d2 - rowm - d2.mean() + grand)
    y = ((Vk.T @ b) / sqrt_lam - base_mean_unrot) @ rot + R.mean(0)
    return y[0]

def pctile(x):
    return min(100.0, 100.0 * np.searchsorted(xs, x) / (N - 1))

def line_matrix(lines):
    F = np.zeros((len(lines), MFW))
    T = np.zeros(len(lines))
    for i, l in enumerate(lines):
        c = count_text(l if W1 else f' {l} ')
        T[i] = sum(c.values())
        for k, v in c.items():
            j = fidx.get(k)
            if j is not None:
                F[i, j] = v
    return F, T

def boot(path):
    lines = [l for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]
    if len(lines) == 1 and W1:
        toks = lines[0].split()
        lines = [' '.join(toks[i:i + 16]) for i in range(0, len(toks), 16)]
    F, T = line_matrix(lines)
    keep = T > 0
    F, T = F[keep], T[keep]
    L = len(T)
    if L < 2 or T.sum() < 50:
        return None
    cfull = count_text(path.read_text(encoding='utf-8'))
    fv = np.zeros(MFW)
    for k, v in cfull.items():
        j = fidx.get(k)
        if j is not None:
            fv[j] = v
    est = pctile(place_x(fv, sum(cfull.values())))
    est_pad = pctile(place_x(F.sum(0), T.sum()))
    ps = np.empty(B)
    for b in range(B):
        ii = RNG.integers(0, L, L)
        ps[b] = pctile(place_x(F[ii].sum(0), T[ii].sum()))
    shift = est - est_pad
    lo, hi = np.clip(np.percentile(ps, [2.5, 97.5]) + shift, 0, 100)
    return est, lo, hi, int(T.sum())

tag = 'W1' if W1 else 'C3'
out = open(HERE / f'e1_apparatus_{tag}_500.tsv', 'w', encoding='utf-8')
out.write('unit\tkind\test\tlo\thi\ttokens\n')
print(f'{"unit":<40}{"const":>6}{"apparatus":>18}{"augmented":>18}{"aug-const":>10}')
for u in PANEL:
    whole = pctile(Y[names.index(u), 0]) if u in names else float('nan')
    res = {}
    short = u.split('-')[0]
    for kind in ('augmented', 'apparatus'):
        r = boot(GEN_CORPUS / f'{short}_{kind}.txt')
        if r:
            res[kind] = r
            out.write(f'{u}\t{kind}\t{r[0]:.1f}\t{r[1]:.1f}\t{r[2]:.1f}\t{r[3]}\n')
    if len(res) == 2:
        g, r_ = res['apparatus'], res['augmented']
        print(f'{u:<40}{whole:>6.0f}'
              f'{g[0]:>7.0f} [{g[1]:>3.0f},{g[2]:>4.0f}]'
              f'{r_[0]:>7.0f} [{r_[1]:>3.0f},{r_[2]:>4.0f}]'
              f'{r_[0]-whole:>+10.0f}')
out.close()
print(f'\nwrote e1_apparatus_{tag}_500.tsv  (B={B})')
