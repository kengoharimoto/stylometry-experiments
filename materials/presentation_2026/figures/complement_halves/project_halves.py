#!/usr/bin/env python3
"""Project shared/residue halves of Vayu, Brahmanda and Visnu units as
supplementary points into the sweet-spot delta MDS map.

Base map: manifest units on the full (reuse-in) corpus, top-N features by
summed raw counts, Burrows's delta, classical MDS — the same computation as
hero_mds.py. The halves are z-scored with the BASE mean/std and placed by
Gower's supplementary-point formula, so they do not disturb the base map.

Usage: project_halves.py w|c
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
W1 = FEAT == 'w'
MFW = 500

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

def word_counts(path):
    return Counter(path.read_text(encoding='utf-8').lower().split())

def trigram_counts(path):
    # article C3 convention (2026-08-16): scriptio continua — all whitespace
    # removed; word division is editorial (see c3_nospace note)
    txt = re.sub(r'\s+', '', path.read_text(encoding='utf-8').lower())
    return Counter(txt[i:i + 3] for i in range(len(txt) - 2))

count_fn = word_counts if W1 else trigram_counts

manifest = {l.strip()[:-4] if l.strip().endswith('.txt') else l.strip()
            for l in MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}
names, counts = [], []
for p in sorted(BASE_CORPUS.glob('*.txt')):
    if p.stem in manifest:
        names.append(p.stem)
        counts.append(count_fn(p))
assert len(names) == len(manifest), sorted(manifest - set(names))

raw = Counter()
for c in counts:
    raw.update(c)
feats = [w for w, _ in raw.most_common(MFW)]
totals = [sum(c.values()) for c in counts]
X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])
mu, sd = X.mean(0), X.std(0)
Z = (X - mu) / sd

N = len(names)
D = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)
J = np.eye(N) - 1 / N
B = -0.5 * J @ (D ** 2) @ J
w, V = np.linalg.eigh(B)
idx = np.argsort(w)[::-1][:2]
lam = w[idx]
Y = V[:, idx] * np.sqrt(np.maximum(lam, 0))

# orient onto the saved sweet-spot layout (rotation/reflection only)
ref = {}
with open(REF_COORDS, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        ref[row['text']] = (float(row['x']), float(row['y']))
R = np.array([ref[n] for n in names])
A, Bm = R - R.mean(0), Y - Y.mean(0)
U_, _, Vt_ = np.linalg.svd(Bm.T @ A)
rot = U_ @ Vt_
Y = Bm @ rot + R.mean(0)
chk = np.corrcoef(Y[:, 0], R[:, 0])[0, 1]
print(f'base map vs saved sweet-spot coords: r_x = {chk:.4f} (want ~1)')

# supplementary projection (Gower): b_i = -0.5 (d_i^2 - rowmean_i(D^2) - mean(d^2) + grandmean(D^2))
D2 = D ** 2
rowm = D2.mean(1)
grand = D2.mean()

base_mean_unrot = (V[:, idx] * np.sqrt(np.maximum(lam, 0))).mean(0)
def place(cnt):
    tot = sum(cnt.values())
    x = np.array([cnt.get(f, 0) / tot for f in feats])
    z = (x - mu) / sd
    d2 = (np.abs(z[None, :] - Z).mean(1)) ** 2
    b = -0.5 * (d2 - rowm - d2.mean() + grand)
    y = (V[:, idx].T @ b) / np.sqrt(np.maximum(lam, 1e-12))
    return (y - base_mean_unrot) @ rot + R.mean(0)

# sanity: projecting a base text must land on its own coords
i0 = names.index(UNITS[0])
err = np.linalg.norm(place(counts[i0]) - Y[i0])
print(f'self-projection error ({UNITS[0]}): {err:.5f}')

xs = np.sort(Y[:, 0])
def pctile(x):
    return 100.0 * np.searchsorted(xs, x) / (N - 1)

rows = []
print(f'\n{"unit":<48}{"whole":>7}{"resid":>7}{"shared":>7}   (percentile of x on base map)')
for u in UNITS:
    whole = pctile(Y[names.index(u), 0]) if u in names else float('nan')
    out = {'unit': u, 'whole': whole}
    for kind, path in [('resid', RESID_CORPUS / f'{u}.txt'),
                       ('shared', SHARED_CORPUS / f'{u}_shared.txt')]:
        cnt = count_fn(path)
        yx, yy = place(cnt)
        out[kind] = pctile(yx)
        out[f'{kind}_xy'] = (yx, yy)
        out[f'{kind}_words'] = sum(cnt.values()) if W1 else len(path.read_text(encoding='utf-8').split())
    rows.append(out)
    print(f'{u:<48}{out["whole"]:>7.0f}{out["resid"]:>7.0f}{out["shared"]:>7.0f}')

tag = 'W1' if W1 else 'C3'
with open(HERE / f'halves_{tag}_500.tsv', 'w', encoding='utf-8') as f:
    f.write('unit\tkind\tx\ty\tpct\twords\n')
    for n, (x, y) in zip(names, Y):
        f.write(f'{n}\tbase\t{x:.6f}\t{y:.6f}\t{pctile(x):.1f}\t\n')
    for o in rows:
        for kind in ['resid', 'shared']:
            x, y = o[f'{kind}_xy']
            f.write(f'{o["unit"]}\t{kind}\t{x:.6f}\t{y:.6f}\t{o[kind]:.1f}\t{o[f"{kind}_words"]}\n')
print(f'\nwrote halves_{tag}_500.tsv')
