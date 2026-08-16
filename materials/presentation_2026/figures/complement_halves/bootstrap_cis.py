#!/usr/bin/env python3
"""Line-bootstrap CIs for the projected drift-axis positions of the layer
subsets (residue / ppl / vayubd / other) and the constituted PPL units.

For each subset: B resamples of its lines with replacement -> profile ->
z-score with base stats -> Gower projection into the fixed sweet-spot map ->
drift-axis percentile. Reports the point estimate and the 2.5/97.5 quantiles.

Usage: bootstrap_cis.py w|c [B]
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
RESID_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied_noreuse' if W1 else 'corpus/epic_puranas_sandhied_noreuse')
SHARED_CORPUS = ROOT / ('corpus/complements_unsandhied' if W1 else 'corpus/complements_sandhied')
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
REF_COORDS = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                     if W1 else 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv')

UNITS = ([f'vayupurana_{s}_iast' for s in
          ['01_frame-and-cosmogony', '02_pashupata-yoga', '03_kalpas-and-shiva-lineages',
           '04_bhuvana-vinyasa', '05_jyotis-and-purvardha-close',
           '06_prthu-and-prajapati-lineages', '07_shraddha-kalpa',
           '08_manu-candra-vishnu-vamsha', '09_upasamhara', '10_gaya-mahatmya']]
         + ['vayupurana_revakhanda']
         + [f'brahmandapurana_khanda-{k}_u' for k in '123']
         + [f'visnupurana_amsa-{a}_u' for a in '123456'])
PPL_UNITS = ['kirfel_ppl_textgruppe_I_col1', 'kirfel_ppl_textgruppe_Ia_col1',
             'kirfel_ppl_textgruppe_II_col1', 'kirfel_ppl_textgruppe_IIA_col1',
             'kirfel_ppl_textgruppe_IIB_col1', 'kirfel_ppl_textgruppe_III_col1',
             'kirfel_ppl_ungrouped_col1']

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
    """Per-line feature-count matrix and per-line total token counts.

    Under the no-space C3 convention lines are counted as bare character
    streams (no padding — there are no space trigrams). The exact whole-text
    estimate is computed separately; the replicate distribution is
    pivot-shifted onto it (junction trigrams across line boundaries are
    neighbor-dependent and cannot be attributed to single lines)."""
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
    est = pctile(place_x(fv, sum(cfull.values())))          # exact, matches the map
    est_pad = pctile(place_x(F.sum(0), T.sum()))
    ps = np.empty(B)
    for b in range(B):
        ii = RNG.integers(0, L, L)
        ps[b] = pctile(place_x(F[ii].sum(0), T[ii].sum()))
    shift = est - est_pad
    lo, hi = np.clip(np.percentile(ps, [2.5, 97.5]) + shift, 0, 100)
    return est, lo, hi, int(T.sum())

tag = 'W1' if W1 else 'C3'
out = open(HERE / f'bootstrap_{tag}_500.tsv', 'w', encoding='utf-8')
out.write('unit\tkind\test\tlo\thi\ttokens\n')
print(f'{"unit":<48}{"kind":<8}{"est":>6}{"95% CI":>16}{"tokens":>9}')

# NB: line structure for W1 subsets exists (one line per source line after
# ByT5); residues in the unsandhied noreuse corpus are single-line files, so
# W1 residue lines come from resampling the sandhied residue is not possible —
# instead split the single line into pseudo-verses of ~16 words.
def get_lines(path):
    lines = [l for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]
    if len(lines) == 1 and W1:
        toks = lines[0].split()
        lines = [' '.join(toks[i:i + 16]) for i in range(0, len(toks), 16)]
    return lines

jobs = []
for u in UNITS:
    jobs.append((u, 'resid', RESID_CORPUS / f'{u}.txt'))
    for k in ('ppl', 'vayubd', 'other'):
        jobs.append((u, k, SHARED_CORPUS / f'{u}_shared_{k}.txt'))
for u in PPL_UNITS:
    jobs.append((u, 'constituted', BASE_CORPUS / f'{u}.txt'))

for u, kind, path in jobs:
    if not path.exists() or not path.read_text(encoding='utf-8').strip():
        continue
    r = boot(get_lines(path), path.read_text(encoding='utf-8'))
    if r is None:
        continue
    est, lo, hi, tok = r
    out.write(f'{u}\t{kind}\t{est:.1f}\t{lo:.1f}\t{hi:.1f}\t{tok}\n')
    print(f'{u:<48}{kind:<8}{est:>6.0f}   [{lo:>5.0f},{hi:>6.0f}]{tok:>9}')
out.close()
print(f'\nwrote bootstrap_{tag}_500.tsv  (B={B})')
