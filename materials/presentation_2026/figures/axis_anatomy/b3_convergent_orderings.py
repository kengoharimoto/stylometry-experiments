#!/usr/bin/env python3
"""B3 (axis-anatomy plan): convergent orderings.

If the gradient is a property of the distance structure rather than of
MDS, then orderings derived under different assumptions must agree:
  - spectral seriation (Fiedler vector of the affinity Laplacian)
  - 1-D isomap (geodesic distances over a k-NN graph, classical MDS)
  - TSP/Hamiltonian-path seriation (nearest-neighbour + 2-opt, best of
    several starts)
  - plain PCA on the z-scored feature matrix (near-equivalent to
    classical MDS on Delta, but with directly readable loadings)
Each is compared (|Spearman|) against the article's sweet-spot MDS axis.
t-SNE/UMAP are deliberately absent: they preserve local neighbourhoods
and discard the global geometry a gradient reading lives in.

Usage: b3_convergent_orderings.py w|c
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.sparse.csgraph import shortest_path
from scipy.stats import spearmanr

import os

ROOT = Path(os.environ.get('STYLO_ROOT', '/mnt/kengo/stylometry-experiments'))
HERE = Path(__file__).parent
NOREUSE = '--noreuse' in sys.argv
argv = [a for a in sys.argv if a != '--noreuse']
FEAT = argv[1] if len(argv) > 1 else 'w'
W1 = FEAT == 'w'
MFW = 500
RNG = np.random.default_rng(20260816)
if W1 and NOREUSE:
    sys.exit('w + --noreuse refused: the no-reuse W1 axis is partly a '
             'length artifact (R1) — run c --noreuse instead')

if NOREUSE:
    CORPUS = ROOT / 'corpus/epic_puranas_sandhied_noreuse'
    MANIFEST = ROOT / 'manifests/noreuse2026_n126.txt'
    COORDS = ROOT / 'materials/presentation_2026/figures/mds3d/coords_C3-500ns_noreuse_n126.tsv'
else:
    CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
    MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
    COORDS = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                     if W1 else 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv')


def counts_of(path):
    if W1:
        return Counter(path.read_text(encoding='utf-8').lower().split())
    t = re.sub(r'\s+', '', path.read_text(encoding='utf-8').lower())
    return Counter(t[i:i + 3] for i in range(len(t) - 2))


manifest = {l.strip().removesuffix('.txt') for l in
            MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}
names, counts = [], []
for p in sorted(CORPUS.glob('*.txt')):
    if p.stem in manifest:
        names.append(p.stem)
        counts.append(counts_of(p))
raw = Counter()
for c in counts:
    raw.update(c)
feats = [w for w, _ in raw.most_common(MFW)]
T = [sum(c.values()) for c in counts]
X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, T)])
Z = (X - X.mean(0)) / X.std(0)
D = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)
N = len(names)

with open(COORDS, encoding='utf-8') as f:
    xref = {r['text']: float(r['x']) for r in csv.DictReader(f, delimiter='\t')}
x = np.array([xref[n] for n in names])

orderings = {}

# 1 spectral seriation: Fiedler vector of the Gaussian-affinity Laplacian
sigma = np.median(D[np.triu_indices(N, 1)])
W = np.exp(-(D ** 2) / (2 * sigma ** 2))
np.fill_diagonal(W, 0)
L = np.diag(W.sum(1)) - W
lw, lv = np.linalg.eigh(L)
orderings['fiedler'] = lv[:, 1]                     # second-smallest eigenvector

# 2 one-dimensional isomap (k-NN geodesics -> classical MDS, 1 dim)
K = 10
G = np.full((N, N), np.inf)
for i in range(N):
    nn = np.argsort(D[i])[1:K + 1]
    G[i, nn] = D[i, nn]
G = np.minimum(G, G.T)
GD = shortest_path(G, method='D', directed=False)
assert np.isfinite(GD).all(), 'kNN graph disconnected — raise K'
J = np.eye(N) - 1 / N
B = -0.5 * J @ (GD ** 2) @ J
bw, bv = np.linalg.eigh(B)
i1 = np.argmax(bw)
orderings['isomap1d'] = bv[:, i1] * np.sqrt(bw[i1])

# 3 TSP path seriation: NN construction from several starts + full 2-opt
def path_len(p):
    return D[p[:-1], p[1:]].sum()


def two_opt(p):
    improved = True
    while improved:
        improved = False
        for i in range(1, N - 1):
            for j in range(i + 1, N):
                a, b = p[i - 1], p[i]
                c, d = p[j], p[(j + 1) % N] if j + 1 < N else None
                if d is None:
                    delta = D[a, p[j]] - D[a, b]
                else:
                    delta = (D[a, c] + D[b, d]) - (D[a, b] + D[c, d])
                if delta < -1e-12:
                    p[i:j + 1] = p[i:j + 1][::-1]
                    improved = True
    return p


best = None
for s in RNG.choice(N, size=6, replace=False):
    p = [int(s)]
    left = set(range(N)) - {int(s)}
    while left:
        nxt = min(left, key=lambda j: D[p[-1], j])
        p.append(nxt)
        left.remove(nxt)
    p = two_opt(np.array(p))
    if best is None or path_len(p) < path_len(best):
        best = p
pos = np.empty(N)
pos[best] = np.arange(N)
orderings['tsp_path'] = pos

# 4 plain PCA on the z-scored features
U, S, Vt = np.linalg.svd(Z - Z.mean(0), full_matrices=False)
orderings['pca1'] = U[:, 0] * S[0]

# 2-D variants for the near-degenerate case (C3's axis1/axis2 ratio is 1.13,
# so which real dimension a method ranks "first" is ambiguous; the fair
# object of comparison is the method's top-2 plane, Procrustes-rotated onto
# the map, then the first aligned coordinate vs x).
with open(COORDS, encoding='utf-8') as f:
    yref = {r['text']: float(r['y']) for r in csv.DictReader(f, delimiter='\t')}
ymap = np.array([yref[n] for n in names])
R2 = np.column_stack([x, ymap])
planes = {
    'pca_2d': (U[:, :2] * S[:2]),
    'isomap_2d': bv[:, np.argsort(bw)[::-1][:2]] * np.sqrt(np.maximum(bw[np.argsort(bw)[::-1][:2]], 0)),
    'fiedler_2d': lv[:, 1:3],
}
aligned = {}
for k, P in planes.items():
    A = R2 - R2.mean(0)
    Bm = P - P.mean(0)
    # scale-free orthogonal Procrustes
    U_, _, Vt_ = np.linalg.svd(Bm.T @ A)
    aligned[k] = (Bm @ (U_ @ Vt_))[:, 0]

tag = ('W1' if W1 else 'C3') + ('_noreuse' if NOREUSE else '')
keys = list(orderings)
print(f'{tag}-500: |rho| of each ordering vs the sweet-spot MDS axis')
rows = []
for k in keys:
    r = abs(spearmanr(orderings[k], x).statistic)
    rows.append((k, r))
    print(f'  {k:<10} {r:.4f}')
print('\naligned top-2 plane, first coordinate vs x:')
for k, v in aligned.items():
    print(f'  {k:<11} {abs(spearmanr(v, x).statistic):.4f}')

print('\npairwise |rho| among the orderings:')
for i, a in enumerate(keys):
    for b in keys[i + 1:]:
        print(f'  {a:<10} x {b:<10} '
              f'{abs(spearmanr(orderings[a], orderings[b]).statistic):.4f}')

with open(HERE / f'b3_orderings_{tag}_500.tsv', 'w', encoding='utf-8') as f:
    f.write('text\tmds_x\t' + '\t'.join(keys) + '\n')
    for i, n in enumerate(names):
        f.write(n + f'\t{x[i]:.6f}\t' +
                '\t'.join(f'{orderings[k][i]:.6f}' for k in keys) + '\n')
print(f'wrote b3_orderings_{tag}_500.tsv')
