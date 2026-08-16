#!/usr/bin/env python3
"""Line-bootstrap CIs for the SP/Markandeya/PPL sequence units (the
2026-08-14_sp_mark_ppl_sequence note). Whole units and layer subsets are
placed as supplementary points into the fixed sweet-spot map and
bootstrapped over their own lines ('self' kind).

Originally run from a session scratchpad; recreated as a repo script on
2026-08-16 with the no-space C3 convention.

Usage: sp_mark_cis.py w|c [B]
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
B = int(sys.argv[2]) if len(sys.argv) > 2 else 500
W1 = FEAT == 'w'
MFW = 500
RNG = np.random.default_rng(20260814)

BASE_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
REF_COORDS = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                     if W1 else 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv')

UNITS = ['skandapurana', 'skandapurana_adhyaya-1-31_pu',
         'skandapurana_pasupata_adhyaya174-183_u',
         'markandeyapurana', 'markandeyapurana_adhyaya-1-80_u',
         'markandeyapurana_adhyaya-81-93_devimahatmya_u',
         'markandeyapurana_adhyaya-94-141_u',
         'kirfel_ppl_textgruppe_I_col1', 'kirfel_ppl_ungrouped_col1',
         'kirfel_ppl_textgruppe_II_col1']

def word_counts_text(txt):
    return Counter(txt.lower().split())

def trigram_counts_text(txt):
    # article C3 convention (2026-08-16): scriptio continua — all whitespace
    # removed; word division is editorial (see c3_nospace note)
    txt = re.sub(r'\s+', '', txt.lower())
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
        c = count_text(l)
        T[i] = sum(c.values())
        for k, v in c.items():
            j = fidx.get(k)
            if j is not None:
                F[i, j] = v
    return F, T

def boot(lines, full_text):
    lines = [l for l in lines if l.strip()]
    F, T = line_matrix(lines)
    keep = T > 0
    F, T = F[keep], T[keep]
    L = len(T)
    if L < 2 or T.sum() < 50:
        return None
    cfull = count_text(full_text)
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

def get_lines(path):
    lines = [l for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]
    if len(lines) == 1 and W1:
        toks = lines[0].split()
        lines = [' '.join(toks[i:i + 16]) for i in range(0, len(toks), 16)]
    return lines

tag = 'W1' if W1 else 'C3'
out = open(HERE / f'sp_mark_{tag}_500.tsv', 'w', encoding='utf-8')
out.write('unit\tkind\test\tlo\thi\ttokens\n')
print(f'{"unit":<48}{"est":>6}{"95% CI":>16}{"tokens":>9}')
for u in UNITS:
    path = BASE_CORPUS / f'{u}.txt'
    if not path.exists():
        print(f'{u:<48}  MISSING')
        continue
    r = boot(get_lines(path), path.read_text(encoding='utf-8'))
    if r is None:
        continue
    est, lo, hi, tok = r
    out.write(f'{u}\tself\t{est:.1f}\t{lo:.1f}\t{hi:.1f}\t{tok}\n')
    print(f'{u:<48}{est:>6.0f}   [{lo:>5.0f},{hi:>6.0f}]{tok:>9}')
out.close()
print(f'\nwrote sp_mark_{tag}_500.tsv  (B={B})')
