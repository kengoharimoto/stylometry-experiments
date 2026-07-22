#!/usr/bin/env python3
"""Length control for the Pāśupata sections V2 and SP2.

Slide 11 leans on Vāyu's pāśupata-yoga section (V2, pūrv. 11-20) jumping to the
far right of axis 1, and on the Skandapurāṇa's Pāśupata chapters (SP2) making
the same jump. V2 is the shortest of the ten Vāyu sections by a wide margin
(3,280 words unsandhied), so the D1 test of the closing-parvans brief applies
here too: does a random contiguous stretch of *ordinary* Vāyu, cut to the same
length, land just as far right?

Null distribution: contiguous windows of V2's exact size drawn from the other
nine Vāyu sections (never from V2 itself), pushed through the identical hero
pipeline and Procrustes-projected onto the hero map. Same for SP2 against the
rest of the Skandapurāṇa. Reference nulls from Agni and MBh 12 fix the drift
direction at that length for texts sitting elsewhere on the axis.

Both lenses, Burrows's Delta. Prints numbers; writes no figure.
"""
from collections import Counter
import re
import numpy as np

import figcommon as fc

REPS = 40
SEED = 20260722

# (target stem, label, [donor stems for the null], donor label)
CASES = [
    ('vayupurana_02_pashupata-yoga_iast', 'V2 (Vāyu pāśupata)',
     ['vayupurana_01_frame-and-cosmogony_iast',
      'vayupurana_03_kalpas-and-shiva-lineages_iast',
      'vayupurana_04_bhuvana-vinyasa_iast',
      'vayupurana_05_jyotis-and-purvardha-close_iast',
      'vayupurana_06_prthu-and-prajapati-lineages_iast',
      'vayupurana_07_shraddha-kalpa_iast',
      'vayupurana_08_manu-candra-vishnu-vamsha_iast',
      'vayupurana_09_upasamhara_iast',
      'vayupurana_10_gaya-mahatmya_iast'], 'rest of Vāyu'),
    ('skandapurana_pasupata_adhyaya174-183_u', 'SP2 (SkP pāśupata)',
     ['skandapurana'], 'rest of SkP'),
]
CONTROLS = [('agnipurana_u', 'Agni'), ('mahabharata_12-santiparvan', 'MBh 12')]


def chunk_vector(tokens, feats, features):
    if features == 'w':
        c = Counter(tokens)
    else:
        txt = re.sub(r'\s+', ' ', ' '.join(tokens)).strip()
        c = Counter(txt[i:i + 3] for i in range(len(txt) - 2))
    tot = sum(c.values())
    return np.array([c.get(w, 0) / tot for w in feats])


def align_to_hero(Yaug, names_aug, names_ref, Yref):
    idx = {nm: i for i, nm in enumerate(names_aug)}
    A = Yref - Yref.mean(0)
    anch = Yaug[[idx[nm] for nm in names_ref]]
    mu = anch.mean(0)
    U, s, Vt = np.linalg.svd((anch - mu).T @ A)
    return (Yaug[idx['__chunk__']] - mu) @ (U @ Vt)


names_ref, Yref, _ = fc.hero_layout()

for feats in ('w', 'c'):
    lens = 'W1 words' if feats == 'w' else 'C3 3-grams'
    corpus = fc.ROOT / ('corpus/epic_puranas_unsandhied' if feats == 'w'
                        else 'corpus/epic_puranas_sandhied')
    names, feat_list, X, Z = fc.load_profiles(feats)
    D = fc.distance_matrix(X, Z, 'delta')
    Y = fc.cmdscale(D)
    Yq = Y[[names.index(nm) for nm in names_ref]]
    A = Yref - Yref.mean(0); B = Yq - Yq.mean(0)
    U, s, Vt = np.linalg.svd(B.T @ A)
    Yq = B @ (U @ Vt)
    a1 = {nm: Yq[i, 0] for i, nm in enumerate(names_ref)}
    meanD = {nm: D[names.index(nm)].sum() / (len(names) - 1) for nm in names}
    med = np.median([meanD[nm] for nm in names])

    print(f'\n{"="*74}\n{lens} — Burrows\'s Delta, projected on the hero map')
    print(f'{"="*74}')
    print(f'corpus axis-1 spans {Yq[:,0].min():+.3f} .. {Yq[:,0].max():+.3f}; '
          f'median mean-Delta {med:.3f}')
    rng = np.random.default_rng(SEED)

    for stem, label, donors, donor_label in CASES:
        toks_t = (corpus / f'{stem}.txt').read_text(encoding='utf-8').split()
        size = len(toks_t)
        obs = a1[stem]
        rank = sorted(names, key=lambda n: -meanD[n]).index(stem) + 1
        print(f'\n{label}: N={size}, axis1={obs:+.3f}, '
              f'mean-Delta={meanD[stem]:.3f} (rank {rank}/{len(names)})')

        pools = []
        for d in donors:
            t = (corpus / f'{d}.txt').read_text(encoding='utf-8').split()
            if len(t) > size + 1:
                pools.append(t)
        vals = []
        for _ in range(REPS):
            pool = pools[rng.integers(0, len(pools))]
            st = rng.integers(0, len(pool) - size)
            cv = chunk_vector(pool[st:st + size], feat_list, feats)
            Xa = np.vstack([X, cv])
            Za = (Xa - Xa.mean(0)) / Xa.std(0)
            Ya = fc.cmdscale(fc.distance_matrix(Xa, Za, 'delta'))
            vals.append(align_to_hero(Ya, names + ['__chunk__'],
                                      names_ref, Yref)[0])
        vals = np.array(vals)
        p = (vals >= obs).mean()
        print(f'  null from {donor_label} at N={size}: '
              f'mean={vals.mean():+.3f} sd={vals.std():.3f} '
              f'range [{vals.min():+.3f}, {vals.max():+.3f}]')
        print(f'  observed sits {(obs - vals.mean()) / vals.std():+.2f} sd '
              f'above the null mean; {p*100:.0f}% of windows reach it')

    for stem, label in CONTROLS:
        toks = (corpus / f'{stem}.txt').read_text(encoding='utf-8').split()
        size = len((corpus / f'{CASES[0][0]}.txt')
                   .read_text(encoding='utf-8').split())
        vals = []
        for _ in range(REPS):
            st = rng.integers(0, len(toks) - size)
            cv = chunk_vector(toks[st:st + size], feat_list, feats)
            Xa = np.vstack([X, cv])
            Za = (Xa - Xa.mean(0)) / Xa.std(0)
            Ya = fc.cmdscale(fc.distance_matrix(Xa, Za, 'delta'))
            vals.append(align_to_hero(Ya, names + ['__chunk__'],
                                      names_ref, Yref)[0])
        vals = np.array(vals)
        print(f'\ncontrol {label}: full-unit axis1={a1[stem]:+.3f}; '
              f'windows of N={size} → mean={vals.mean():+.3f} '
              f'sd={vals.std():.3f} (drift {vals.mean()-a1[stem]:+.3f})')
