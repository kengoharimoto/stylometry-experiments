#!/usr/bin/env python3
"""Cheap diagnostics D2/D3 for the closing-parvans length-artifact brief.

Uses the exact hero pipeline (via figcommon) so numbers are comparable to the
deck. Reports, per lens (W1 words, C3 3-grams) and for Burrows's Delta:
  D2  axis-1 position vs log(token count), all 101 units, correlation
  D3  mean Delta of each unit to the other 100, ranked
      + nearest neighbour of every MBh unit (is 16<->17 mutual?)
"""
import numpy as np
import figcommon as fc

CLOSING = ['mahabharata_15-asramavasikaparvan', 'mahabharata_16-mausalaparvan',
           'mahabharata_17-mahaprasthanikaparvan',
           'mahabharata_18-svargarohanaparvan']


def token_count(name, features):
    corpus = fc.ROOT / ('corpus/epic_puranas_unsandhied' if features == 'w'
                        else 'corpus/epic_puranas_sandhied')
    return len((corpus / f'{name}.txt').read_text(encoding='utf-8').split())


for feats in ('w', 'c'):
    lens = 'W1 words' if feats == 'w' else 'C3 3-grams'
    names, _, X, Z = fc.load_profiles(feats)
    D = fc.distance_matrix(X, Z, 'delta')
    n = len(names)

    # hero orientation gives axis-1; reuse hero_layout only for W1-delta,
    # else align this lens's delta MDS to hero for a comparable axis-1.
    names_ref, Yref, _ = fc.hero_layout()
    order = [names.index(nm) for nm in names_ref]
    Y = fc.cmdscale(D)[order]
    Y, sim = fc.procrustes_align(Y, Yref)
    axis1 = {nm: Y[i, 0] for i, nm in enumerate(names_ref)}

    counts = {nm: token_count(nm, feats) for nm in names}
    logN = np.array([np.log10(counts[nm]) for nm in names_ref])
    a1 = np.array([axis1[nm] for nm in names_ref])
    r = np.corrcoef(logN, a1)[0, 1]

    meanD = {names[i]: D[i].sum() / (n - 1) for i in range(n)}
    rank = sorted(names, key=lambda nm: -meanD[nm])

    print(f'\n===== {lens} · Burrows Delta '
          f'(axis-1 alignment to hero: {sim:.2f}) =====')
    print(f'D2  corr(axis-1, log10 N) = {r:+.2f}   '
          f'(axis-1: negative = "earlier/epic" pole)')
    print('    closing parvans (axis-1, N):')
    for nm in CLOSING:
        print(f'      {nm.split("-")[0]:<16} axis1={axis1[nm]:+.3f}  '
              f'N={counts[nm]:>7}  logN={np.log10(counts[nm]):.2f}')

    print('D3  mean-Delta ranking (most isolated first), top 12:')
    for k, nm in enumerate(rank[:12], 1):
        tag = '  <-- closing parvan' if nm in CLOSING else ''
        print(f'      {k:>2}. {nm.split("-")[0]:<20} '
              f'meanD={meanD[nm]:.3f}  N={counts[nm]}{tag}')
    for nm in CLOSING:
        print(f'      (rank of {nm.split("-")[0]}: '
              f'{rank.index(nm)+1}/{n})')

    print('D3  nearest neighbour of each MBh unit:')
    idx = {nm: i for i, nm in enumerate(names)}
    nn = {}
    for nm in names:
        if not nm.startswith('mahabharata_'):
            continue
        i = idx[nm]
        j = min((k for k in range(n) if k != i), key=lambda k: D[i, k])
        nn[nm] = names[j]
    for nm in sorted(nn):
        mutual = '  [MUTUAL]' if nn.get(nn[nm]) == nm else ''
        print(f'      {nm.split("-")[0]:<18} -> {nn[nm].split("-")[0]}{mutual}')
