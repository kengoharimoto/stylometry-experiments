#!/usr/bin/env python3
"""B2 (axis-anatomy plan): null and generative models for the MDS gradient.

Three synthetic corpora with the REAL unit sizes and feature inventory,
features multinomial:
  1 exchangeable  — every unit drawn from one shared rate vector
                    (calibrates "no structure");
  2 heterogeneity — each unit gets its own rates, drawn i.i.d. per feature
                    with the empirically observed between-text variance,
                    but NO covariance structure;
  3 drift process — rates follow per-feature Brownian paths over a shared
                    latent order (cross-sectional variance matched to the
                    empirical one), units sampled along it.
For each: axis-1 variance share, axis-1/axis-2 ratio, and (model 3) how
well MDS axis 1 recovers the latent order. The point: a dominant,
ordering-shaped first axis is the signature of AUTOCORRELATED change —
mere heterogeneity of equal magnitude does not produce it.

Usage: b2_null_models.py w|c [replicates]
"""
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
FEAT = sys.argv[1] if len(sys.argv) > 1 else 'w'
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 10
W1 = FEAT == 'w'
MFW = 500
RNG = np.random.default_rng(20260816)

CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'


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
T = np.array([sum(c.values()) for c in counts])
Xr = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, T)])
N = len(names)

pbar = Xr.mean(0)                    # corpus mean rates of the 500
svar = Xr.std(0)                     # empirical between-text SD per feature
other = max(1e-9, 1.0 - pbar.sum())  # non-top-500 mass


def spectrum(X):
    sd = X.std(0)
    keep = sd > 0
    Z = (X[:, keep] - X[:, keep].mean(0)) / sd[keep]
    D = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)
    J = np.eye(N) - 1 / N
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1]
    pos = w[idx][w[idx] > 0]
    ax1 = V[:, idx[0]] * np.sqrt(w[idx[0]])
    return pos[0] / pos.sum(), pos[0] / pos[1], ax1


def sample_counts(P):
    """multinomial counts for each unit given per-unit rate matrix P."""
    X = np.empty((N, MFW))
    for i in range(N):
        pr = np.append(P[i], other)
        pr = np.clip(pr, 0, None)
        pr = pr / pr.sum()
        draw = RNG.multinomial(T[i], pr)
        X[i] = draw[:MFW] / T[i]
    return X


def run_model(kind):
    shares, ratios, rhos = [], [], []
    for _ in range(REPS):
        if kind == 'exchangeable':
            P = np.tile(pbar, (N, 1))
            t = None
        elif kind == 'heterogeneity':
            P = RNG.normal(pbar, svar, size=(N, MFW))
            t = None
        elif kind == 'drift':
            t = np.sort(RNG.uniform(0, 1, N))
            order = RNG.permutation(N)          # units in random order along t
            dt = np.diff(np.concatenate([[0], t]))
            steps = RNG.normal(0, 1, size=(N, MFW)) * np.sqrt(dt)[:, None]
            B = np.cumsum(steps, axis=0)        # Brownian path per feature
            B = B - B.mean(0)
            bsd = B.std(0)
            bsd[bsd == 0] = 1
            P = np.empty((N, MFW))
            P[order] = pbar + B / bsd * svar    # cross-sectional var matched
            tt = np.empty(N)
            tt[order] = t
            t = tt
        X = sample_counts(P)
        s, r, ax1 = spectrum(X)
        shares.append(s)
        ratios.append(r)
        if t is not None:
            rhos.append(abs(spearmanr(ax1, t).statistic))
    return (np.mean(shares), np.std(shares), np.mean(ratios), np.std(ratios),
            (np.mean(rhos), np.std(rhos)) if rhos else (float('nan'), float('nan')))


tag = 'W1' if W1 else 'C3'
s_real, r_real, _ = spectrum(Xr)
print(f'{tag}-500, {REPS} replicates per model')
print(f'{"model":<16} {"axis-1 share":>14} {"axis1/axis2":>12} {"rho(axis1,t)":>13}')
print(f'{"REAL corpus":<16} {100*s_real:>13.1f}% {r_real:>12.2f} {"—":>13}')
rows = [('real', s_real, 0, r_real, 0, float('nan'), float('nan'))]
for kind in ['exchangeable', 'heterogeneity', 'drift']:
    s, ss, r, rs, (rho, rhos_) = run_model(kind)
    rows.append((kind, s, ss, r, rs, rho, rhos_))
    rtxt = f'{rho:.3f}±{rhos_:.3f}' if not np.isnan(rho) else '—'
    print(f'{kind:<16} {100*s:>10.1f}±{100*ss:.1f}% {r:>9.2f}±{rs:.2f} {rtxt:>13}')

with open(HERE / f'b2_models_{tag}_500.tsv', 'w', encoding='utf-8') as f:
    f.write('model\taxis1_share\taxis1_share_sd\tratio12\tratio12_sd\trho_order\trho_order_sd\n')
    for r_ in rows:
        f.write(r_[0] + '\t' + '\t'.join(f'{v:.4f}' for v in r_[1:]) + '\n')
print(f'wrote b2_models_{tag}_500.tsv')
