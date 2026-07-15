#!/usr/bin/env python3
"""D4 (merge test) and D6 (Rāmāyaṇa control) for the closing-parvans brief."""
import re
from collections import Counter
import numpy as np
import figcommon as fc

CLOSING = ['mahabharata_15-asramavasikaparvan', 'mahabharata_16-mausalaparvan',
           'mahabharata_17-mahaprasthanikaparvan',
           'mahabharata_18-svargarohanaparvan']


def chunk_vector(text, feats, features):
    if features == 'w':
        c = Counter(text.split())
    else:
        t = re.sub(r'\s+', ' ', text).strip()
        c = Counter(t[i:i + 3] for i in range(len(t) - 2))
    tot = sum(c.values())
    return np.array([c.get(w, 0) / tot for w in feats])


def project(text, feats_key):
    corpus = fc.ROOT / ('corpus/epic_puranas_unsandhied' if feats_key == 'w'
                        else 'corpus/epic_puranas_sandhied')
    names, feat_list, X, _ = fc.load_profiles(feats_key)
    names_ref, Yref, _ = fc.hero_layout()
    cv = chunk_vector(text, feat_list, feats_key)
    Xaug = np.vstack([X, cv])
    Zaug = (Xaug - Xaug.mean(0)) / Xaug.std(0)
    Yaug = fc.cmdscale(fc.distance_matrix(Xaug, Zaug, 'delta'))
    idx = {nm: i for i, nm in enumerate(names + ['__c__'])}
    A = Yref - Yref.mean(0)
    anch = Yaug[[idx[nm] for nm in names_ref]]
    mu = anch.mean(0); B = anch - mu
    U, s, Vt = np.linalg.svd(B.T @ A)
    return ((Yaug[idx['__c__']] - mu) @ (U @ Vt))[0]


def cat(stems, feats_key):
    corpus = fc.ROOT / ('corpus/epic_puranas_unsandhied' if feats_key == 'w'
                        else 'corpus/epic_puranas_sandhied')
    return '\n'.join((corpus / f'{s}.txt').read_text(encoding='utf-8')
                     for s in stems)


for feats in ('w', 'c'):
    lens = 'W1' if feats == 'w' else 'C3'
    names, _, X, _ = fc.load_profiles(feats)
    names_ref, Yref, _ = fc.hero_layout()
    Y = fc.cmdscale(fc.distance_matrix(X, (X - X.mean(0)) / X.std(0), 'delta'))
    Y = Y[[names.index(nm) for nm in names_ref]]
    Af = Yref - Yref.mean(0); Bf = Y - Y.mean(0)
    U, s, Vt = np.linalg.svd(Bf.T @ Af)
    Y = Bf @ (U @ Vt)
    a1 = {nm: Y[i, 0] for i, nm in enumerate(names_ref)}

    print(f'\n===== {lens} · Burrows Delta (axis-1: - = epic pole) =====')
    print('D4  merge test (axis-1 of concatenated units):')
    for lab, stems in [('15+16+17+18', CLOSING), ('16+17+18', CLOSING[1:])]:
        print(f'      {lab:<12} -> {project(cat(stems, feats), feats):+.3f}')
    for nm in CLOSING:
        print(f'      (single {nm.split("-")[0]}: {a1[nm]:+.3f})')
    ref = {'MBh 6': 'mahabharata_06-bhismaparvan',
           'MBh 9': 'mahabharata_09-salyaparvan',
           'MBh 11': 'mahabharata_11-striparvan',
           'MBh 14': 'mahabharata_14-asvamedhikaparvan'}
    print('      reference full units: '
          + ', '.join(f'{k} {a1[v]:+.2f}' for k, v in ref.items()))

    print('D6  Rāmāyaṇa control (Bāla/Uttara are late epic but NOT short):')
    corpus = fc.ROOT / ('corpus/epic_puranas_unsandhied' if feats == 'w'
                        else 'corpus/epic_puranas_sandhied')
    for nm in sorted(n for n in names_ref if n.startswith('ramayana_')):
        N = len((corpus / f'{nm}.txt').read_text().split())
        tag = '  <-- late epic, long' if nm.startswith(
            ('ramayana_01', 'ramayana_07')) else ''
        print(f'      {nm.split("-")[0]:<14} axis1={a1[nm]:+.3f}  '
              f'N={N:>6}{tag}')
