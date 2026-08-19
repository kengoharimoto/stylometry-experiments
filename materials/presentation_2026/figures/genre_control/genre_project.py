#!/usr/bin/env python3
"""Vamsa genre control: project each panel text's genealogy-like half (gen)
and remainder (rest) into the fixed sweet-spot map; line-bootstrap CIs.

Delta = pct(gen) - pct(rest) estimates the genre pull for that text. Same
projection/bootstrap machinery as complement_halves/bootstrap_cis.py.

Usage: genre_project.py w|c [B] [--noreuse]

--noreuse (2026-08-19, reframe R3): project the reuse-stripped genre halves
(build_genre_split.py --noreuse) into the fixed no-reuse map (manifest
noreuse2026_n126, orientation mds3d/coords_C3-500ns_noreuse_n126.tsv).
Both the map and both halves are then residue. C3 only — see R1.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
NOREUSE = '--noreuse' in sys.argv
argv = [a for a in sys.argv if a != '--noreuse']
FEAT = argv[1] if len(argv) > 1 else 'c'
B = int(argv[2]) if len(argv) > 2 else 200
W1 = FEAT == 'w'
MFW = 500
RNG = np.random.default_rng(20260814)

if NOREUSE and W1:
    sys.exit('--noreuse is C3-only: the no-reuse W1 axis is partly a length '
             'artifact (see R1 in notes/2026-08-19_noreuse_precedence_reframe.md)')

if NOREUSE:
    BASE_CORPUS = ROOT / 'corpus/epic_puranas_sandhied_noreuse'
    GEN_CORPUS = ROOT / 'corpus/genre_control_sandhied_noreuse'
    MANIFEST = ROOT / 'manifests/noreuse2026_n126.txt'
    REF_COORDS = ROOT / 'materials/presentation_2026/figures/mds3d/coords_C3-500ns_noreuse_n126.tsv'
else:
    BASE_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
    GEN_CORPUS = ROOT / ('corpus/genre_control_unsandhied' if W1 else 'corpus/genre_control_sandhied')
    MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
    REF_COORDS = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                         if W1 else 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv')

PANEL = ['mahabharata_01-adiparvan', 'harivamsa', 'matsyapurana_pu',
         'markandeyapurana', 'brahmapurana_pu', 'agnipurana_u',
         'bhavisyapurana', 'garudapurana_khanda-1_u',
         'bhagavatapurana_skandha-09_u', 'kurmapurana_khanda-1_u',
         'padmapurana_a',
         'vayupurana_08_manu-candra-vishnu-vamsha_iast',
         'vayupurana_06_prthu-and-prajapati-lineages_iast']

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

tag = ('W1' if W1 else 'C3') + ('_noreuse' if NOREUSE else '')
out = open(HERE / f'genre_control_{tag}_500.tsv', 'w', encoding='utf-8')
out.write('unit\tkind\test\tlo\thi\ttokens\n')
print(f'{"unit":<48}{"whole":>6}{"gen":>18}{"rest":>18}{"delta":>7}')
for u in PANEL:
    whole = pctile(Y[names.index(u), 0]) if u in names else float('nan')
    res = {}
    for kind in ('gen', 'rest'):
        r = boot(GEN_CORPUS / f'{u}_{kind}.txt')
        if r:
            res[kind] = r
            out.write(f'{u}\t{kind}\t{r[0]:.1f}\t{r[1]:.1f}\t{r[2]:.1f}\t{r[3]}\n')
    if len(res) == 2:
        g, r_ = res['gen'], res['rest']
        print(f'{u:<48}{whole:>6.0f}'
              f'{g[0]:>7.0f} [{g[1]:>3.0f},{g[2]:>4.0f}]'
              f'{r_[0]:>7.0f} [{r_[1]:>3.0f},{r_[2]:>4.0f}]'
              f'{g[0]-r_[0]:>+7.0f}')
out.close()
print(f'\nwrote genre_control_{tag}_500.tsv  (B={B})')
