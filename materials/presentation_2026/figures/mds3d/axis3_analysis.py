#!/usr/bin/env python3
"""A6 (reframe queue): instrument-grade statistics for the third MDS axis.

Inputs: the four article-standard distance tables, produced by
  python3 scripts/presentation/hero_mds.py --mfw 500
      --files-from manifests/dicsep2026_n127_ppl.txt --dump-dist <W1 with>
  python3 scripts/presentation/hero_mds.py --mfw 500
      --corpus-dir corpus/epic_puranas_unsandhied_noreuse
      --files-from manifests/noreuse2026_n126.txt --dump-dist <W1 no>
  (C3: add --features c --strip-spaces; sandhied corpora accordingly.)

For each build (with-reuse n127, no-reuse n126) this computes, from the
3-axis classical MDS of each lens and a joint 3-D Procrustes alignment of
C3 onto W1:
  - variance shares of axes 1-3 per lens;
  - cross-lens Spearman rho per aligned axis;
  - the Bhagavata statistics: point-biserial r(axis3, BhP membership),
    BhP mean axis-3 offset in SD of the rest, per lens;
  - axis-1 and axis-3 cross-lens rho with the 13 BhP units excluded
    (re-aligned on the remainder);
  - rho(axis3, log unit words) per lens (length diagnostic, cf. B2);
  - the flattening exhibit: Sn-Vi3 (sivapurana_sanatkumarasamhita vs
    visnupurana_amsa-3_u) 2-D distance, 3-D distance, and full Delta,
    per lens.

Writes axis3_stats.tsv next to this script.

Usage: axis3_analysis.py W1_WITH C3_WITH W1_NO C3_NO
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
BHP_PREFIX = 'bhagavatapurana'
PAIR = ('sivapurana_sanatkumarasamhita', 'visnupurana_amsa-3_u')


def read_dist(p):
    with open(p) as f:
        names = [h.strip('"') for h in f.readline().split()]
        D = np.array([[float(x) for x in l.split()[1:]] for l in f])
    return names, D


def mds3(D):
    n = len(D)
    J = np.eye(n) - 1 / n
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    i = np.argsort(w)[::-1]
    w, V = w[i], V[:, i]
    shares = w[:3] / w[w > 0].sum()
    return V[:, :3] * np.sqrt(np.maximum(w[:3], 0)), shares


def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def procrustes(A, B):
    """Rotate B (n,3) onto A (n,3); returns aligned B."""
    A0, B0 = A - A.mean(0), B - B.mean(0)
    U, _, Vt = np.linalg.svd(B0.T @ A0)
    return B0 @ (U @ Vt), A0


def analyze(label, w1_path, c3_path, corpus_dir):
    nw, Dw = read_dist(w1_path)
    nc, Dc = read_dist(c3_path)
    Xw, sh_w = mds3(Dw)
    Xc0, sh_c = mds3(Dc)
    Xc = Xc0[[nc.index(n) for n in nw]]
    Bal, A = procrustes(Xw, Xc)
    bhp = np.array([n.startswith(BHP_PREFIX) for n in nw])
    logT = np.array([np.log(len((ROOT / corpus_dir / f'{n}.txt')
                                .read_text(encoding='utf-8').split()))
                     for n in nw])
    rows = {}
    rows['share_ax1_W1'], rows['share_ax2_W1'], rows['share_ax3_W1'] = sh_w
    rows['share_ax1_C3'], rows['share_ax2_C3'], rows['share_ax3_C3'] = sh_c
    for ax in range(3):
        rows[f'crosslens_ax{ax+1}'] = spearman(A[:, ax], Bal[:, ax])
    for lens, X3 in (('W1', A), ('C3', Bal)):
        r = float(np.corrcoef(X3[:, 2], bhp.astype(float))[0, 1])
        z = (X3[bhp, 2].mean() - X3[~bhp, 2].mean()) / X3[~bhp, 2].std()
        rows[f'bhp_pointbiserial_{lens}'] = abs(r)
        rows[f'bhp_offset_sd_{lens}'] = abs(float(z))
        rows[f'logT_ax3_{lens}'] = abs(spearman(X3[:, 2], logT))
    m = ~bhp
    Bm, Am = procrustes(Xw[m], Xc[m])
    rows['crosslens_ax1_noBhP'] = spearman(Am[:, 0], Bm[:, 0])
    rows['crosslens_ax3_noBhP'] = spearman(Am[:, 2], Bm[:, 2])
    i, j = nw.index(PAIR[0]), nw.index(PAIR[1])
    for lens, X3, D in (('W1', Xw, Dw), ('C3', Xc, Dc)):
        rows[f'pair_2d_{lens}'] = float(np.linalg.norm(X3[i, :2] - X3[j, :2]))
        rows[f'pair_3d_{lens}'] = float(np.linalg.norm(X3[i] - X3[j]))
    rows['pair_delta_W1'] = float(Dw[i, j])
    ic, jc = nc.index(PAIR[0]), nc.index(PAIR[1])
    rows['pair_delta_C3'] = float(Dc[ic, jc])
    return rows


if len(sys.argv) != 5:
    sys.exit(__doc__)
builds = [('with-reuse_n127', sys.argv[1], sys.argv[2],
           'corpus/epic_puranas_unsandhied'),
          ('no-reuse_n126', sys.argv[3], sys.argv[4],
           'corpus/epic_puranas_unsandhied_noreuse')]
results = {label: analyze(label, w, c, cd) for label, w, c, cd in builds}

keys = list(next(iter(results.values())))
with open(HERE / 'axis3_stats.tsv', 'w', encoding='utf-8') as f:
    f.write('stat\t' + '\t'.join(results) + '\n')
    for k in keys:
        f.write(k + '\t' + '\t'.join(f'{results[b][k]:.4f}' for b in results) + '\n')
print(f'{"stat":<26}' + ''.join(f'{b:>18}' for b in results))
for k in keys:
    print(f'{k:<26}' + ''.join(f'{results[b][k]:>18.3f}' for b in results))
print('wrote axis3_stats.tsv')
