#!/usr/bin/env python3
"""Cross-validate the no-space C3-500 convention against an R stylo run.

The adopted C3 lens (scriptio continua, colophon-free) rests on the Python
pipeline alone; stylo has no strip-spaces mode. scripts/
build_nospace_sandhied_corpus.py writes a pre-stripped corpus, and
scripts/clusters.R run on it (--features=c --ngram-size=3 --mfw-min=500
--mfw-max=500) is an independent code path from raw text to distance matrix.
This script compares the two:

  1. feature list: stylo's top-500 char-3-gram wordlist vs the Python count
     (recomputed here with hero_mds's exact recipe: lowercase, delete all
     whitespace, count trigrams, rank by raw corpus-summed counts);
  2. distance structure: stylo's saved delta distance table vs the Python
     delta matrix (Pearson/Spearman on the upper triangle);
  3. the map: classical MDS of stylo's distances, Procrustes-aligned
     (rotation/reflection only, matching hero_mds) onto the article frame
     figures/c3_nospace/coords_nospace_mfw500.tsv; reports axis ρ.

Exit nonzero if feature overlap < 0.98 (the hero_mds validation threshold)
or axis-1 ρ < 0.99.
"""
import csv
import re
import sys

NOREUSE = '--noreuse' in sys.argv
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr, pearsonr

ROOT = Path(__file__).resolve().parents[2]
if NOREUSE:
    CORPUS = ROOT / 'corpus/epic_puranas_sandhied_noreuse'
    MANIFEST = ROOT / 'manifests/noreuse2026_n126.txt'
    REF = ROOT / 'materials/presentation_2026/figures/mds3d/coords_C3-500ns_noreuse_n126.tsv'
    RUN_GLOB = 'results_epic_puranas_sandhied_noreuse_nospace_C3_*/'
else:
    CORPUS = ROOT / 'corpus/epic_puranas_sandhied'
    MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
    REF = ROOT / 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv'
    RUN_GLOB = 'results_epic_puranas_sandhied_nospace_C3_*/'
MFW = 500

# latest matching stylo run on the pre-stripped corpus
runs = sorted((p for p in ROOT.glob(RUN_GLOB)
               if NOREUSE or 'noreuse' not in p.name),
              key=lambda p: p.name[-15:])
if not runs:
    sys.exit('no results_epic_puranas_sandhied_nospace_C3_* run found — '
             'run scripts/clusters.R on the pre-stripped corpus first')
RUN = runs[-1]
print(f'stylo run: {RUN.name}')

units = {l.strip()[:-4] if l.strip().endswith('.txt') else l.strip()
         for l in MANIFEST.read_text(encoding='utf-8').splitlines()
         if l.strip() and not l.startswith('#')}

# ── 1. feature list ──────────────────────────────────────────────────────────
raw = Counter()
py_counts, names = {}, []
for p in sorted(CORPUS.glob('*.txt')):
    if p.stem not in units:
        continue
    txt = re.sub(r'\s+', '', p.read_text(encoding='utf-8').lower())
    c = Counter(txt[i:i + 3] for i in range(len(txt) - 2))
    names.append(p.stem)
    py_counts[p.stem] = c
    raw.update(c)
py_feats = [w for w, _ in raw.most_common(MFW)]

wl_lines = [l for l in (RUN / 'wordlist.txt').read_text(encoding='utf-8')
            .splitlines() if l and not l.startswith('#')]
stylo_feats = [l[0::2] for l in wl_lines][:MFW]   # chars joined by spaces

overlap = len(set(py_feats) & set(stylo_feats))
print(f'top-{MFW} feature overlap: {overlap}/{MFW}')

# ── 2. distance structure ────────────────────────────────────────────────────
# NB clusters.R overwrites distance_table_<mfw>mfw_0c.txt once per distance
# measure, so the surviving copy is the LAST measure of its loop (minmax), not
# delta. The delta table must be extracted separately, e.g.
#   Rscript -e 'library(stylo); f <- t(as.matrix(read.table(
#     "<run>/frequencies_analyzed_500mfw_0c.txt", header=TRUE, row.names=1,
#     check.names=FALSE))); write.table(as.matrix(dist.delta(f)),
#     "<run>/distance_table_delta_500mfw.txt", quote=TRUE)'
dts = sorted(RUN.glob(f'distance_table_delta_{MFW}mfw*.txt'))
if not dts:
    sys.exit(f'no distance_table_delta_{MFW}mfw* in {RUN.name} — extract it '
             'with stylo::dist.delta (see comment in this script)')
with open(dts[-1], encoding='utf-8') as f:
    rows = list(csv.reader(f, delimiter=' ', skipinitialspace=True))
stylo_names = [n.strip('"') for n in rows[0]]
D_stylo = np.array([[float(v) for v in r[1:]] for r in rows[1:]])
order = [stylo_names.index(n) for n in names]
D_stylo = D_stylo[np.ix_(order, order)]

totals = {n: sum(c.values()) for n, c in py_counts.items()}
X = np.array([[py_counts[n].get(w, 0) / totals[n] for w in py_feats]
              for n in names])
Z = (X - X.mean(0)) / X.std(0)
D_py = np.abs(Z[:, None, :] - Z[None, :, :]).mean(-1)   # Burrows's Delta

iu = np.triu_indices(len(names), 1)
pr = pearsonr(D_py[iu], D_stylo[iu])[0]
sr = spearmanr(D_py[iu], D_stylo[iu])[0]
print(f'distance matrices (upper triangle): pearson {pr:.4f}, '
      f'spearman {sr:.4f}')

# ── 3. the map ───────────────────────────────────────────────────────────────
def cmds(D, k=2):
    n = len(D)
    J = np.eye(n) - 1 / n
    B = -0.5 * J @ (D ** 2) @ J
    w, v = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1][:k]
    return v[:, idx] * np.sqrt(np.maximum(w[idx], 0))

ref = {}
with open(REF, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        ref[row['text']] = (float(row['x']), float(row['y']))
R = np.array([ref[n] for n in names])

Y = cmds(D_stylo)
A, B = Y - Y.mean(0), R - R.mean(0)
U, _, Vt = np.linalg.svd(A.T @ B)          # rotation/reflection only
Y_al = A @ (U @ Vt)

rx = spearmanr(Y_al[:, 0], R[:, 0])[0]
ry = spearmanr(Y_al[:, 1], R[:, 1])[0]
print(f'stylo-MDS vs article frame after Procrustes: '
      f'rho_x {rx:.4f}, rho_y {ry:.4f}')

ok = overlap / MFW >= 0.98 and abs(rx) >= 0.99
print('VALIDATION ' + ('PASSED' if ok else 'FAILED'))
sys.exit(0 if ok else 1)
