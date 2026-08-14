#!/usr/bin/env python3
"""Project the family-attributed subsets of each shared half (ppl / vayubd /
other), plus the unique residue, into the fixed sweet-spot MDS maps.

Same base-map computation and Gower supplementary projection as
project_halves.py. Also projects the constituted PPL units' own positions for
reference (they are base texts; their percentiles are read off the map).

Usage: project_subsets.py w|c
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
MIN_WORDS = 150          # flag thinner subsets; still projected, marked '*'

BASE_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
RESID_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied_noreuse' if W1 else 'corpus/epic_puranas_sandhied_noreuse')
SHARED_CORPUS = ROOT / ('corpus/complements_unsandhied' if W1 else 'corpus/complements_sandhied')
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
REF_COORDS = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                     if W1 else 'materials/presentation_2026/figures/mfw_sweep/coords_mfw500.tsv')

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
    txt = re.sub(r'\s+', ' ', path.read_text(encoding='utf-8').lower()).strip()
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
assert len(names) == len(manifest)

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

def place(cnt):
    tot = sum(cnt.values())
    x = np.array([cnt.get(f, 0) / tot for f in feats])
    z = (x - mu) / sd
    d2 = (np.abs(z[None, :] - Z).mean(1)) ** 2
    b = -0.5 * (d2 - rowm - d2.mean() + grand)
    y = (V[:, idx].T @ b) / np.sqrt(np.maximum(lam, 1e-12))
    return (y - base_mean_unrot) @ rot + R.mean(0)

xs = np.sort(Y[:, 0])
def pctile(x):
    return 100.0 * np.searchsorted(xs, x) / (N - 1)

tag = 'W1' if W1 else 'C3'
KINDS = [('resid', lambda u: RESID_CORPUS / f'{u}.txt'),
         ('ppl', lambda u: SHARED_CORPUS / f'{u}_shared_ppl.txt'),
         ('vayubd', lambda u: SHARED_CORPUS / f'{u}_shared_vayubd.txt'),
         ('other', lambda u: SHARED_CORPUS / f'{u}_shared_other.txt')]

print(f'\n{"unit":<48}{"whole":>7}{"resid":>8}{"ppl":>8}{"vayubd":>8}{"other":>8}'
      f'   (* = <{MIN_WORDS} words, - = empty)')
out = open(HERE / f'subsets_{tag}_500.tsv', 'w', encoding='utf-8')
out.write('unit\tkind\tx\ty\tpct\twords\n')
for n, (x, y) in zip(names, Y):
    out.write(f'{n}\tbase\t{x:.6f}\t{y:.6f}\t{pctile(x):.1f}\t\n')
for u in UNITS:
    cells = [f'{pctile(Y[names.index(u), 0]):>7.0f}']
    for kind, pf in KINDS:
        p = pf(u)
        if not p.exists() or not p.read_text(encoding='utf-8').strip():
            cells.append(f'{"-":>8}')
            continue
        cnt = count_fn(p)
        nw = len(p.read_text(encoding='utf-8').split())
        yx, yy = place(cnt)
        star = '*' if nw < MIN_WORDS else ''
        cells.append(f'{pctile(yx):>7.0f}{star or " "}')
        out.write(f'{u}\t{kind}\t{yx:.6f}\t{yy:.6f}\t{pctile(yx):.1f}\t{nw}\n')
    print(f'{u:<48}' + ''.join(cells))
out.close()

# reference: constituted PPL units on the same map
print('\nconstituted PPL (base-map percentiles):')
for n in names:
    if n.startswith('kirfel'):
        print(f'  {n:<48}{pctile(Y[names.index(n), 0]):>5.0f}')
print(f'\nwrote subsets_{tag}_500.tsv')
