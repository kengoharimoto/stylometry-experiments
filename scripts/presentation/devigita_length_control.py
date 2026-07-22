"""Length control for the Devigita (DBhP 7.31-40), same D1 method as SP2.

Null: contiguous windows of the Devigita's exact size drawn from the rest of
the Devibhagavatapurana -- with the Devigita's own span (the duplicated
passage) excised from the donor pool, so the null is genuinely 'ordinary DBhP'.
"""
import sys, re
from collections import Counter
import numpy as np
import figcommon as fc

REPS = 200
TARGET = 'devibhagavatapurana_devigita_adhyaya-31-40'
PARENT = 'devibhagavatapurana'
# Devigita span inside the parent, located by anchor lines (1-indexed, sandhied)
ANCHOR_START = "atha ekatriṃśo'dhyāyaḥ"
ANCHOR_END   = "samāpto'yaṃ saptamaḥ skandhaḥ"

names_ref, Yref, _ = fc.hero_layout()
A = Yref - Yref.mean(0)

for feats in ('w', 'c'):
    lens = 'W1 words' if feats == 'w' else 'C3 3-grams'
    corpus = fc.ROOT / ('corpus/epic_puranas_unsandhied' if feats == 'w'
                        else 'corpus/epic_puranas_sandhied')
    names, feat_list, X, Z = fc.load_profiles(feats)
    D = fc.distance_matrix(X, Z, 'delta')
    Y = fc.cmdscale(D)
    Yq = Y[[names.index(n) for n in names_ref]]
    B = Yq - Yq.mean(0)
    U, s, Vt = np.linalg.svd(B.T @ A)
    Yq = B @ (U @ Vt)
    a1 = {n: Yq[i, 0] for i, n in enumerate(names_ref)}

    tgt = (corpus / f'{TARGET}.txt').read_text(encoding='utf-8').split()
    size = len(tgt)
    obs = a1[TARGET]

    # donor pool: parent minus the Devigita span
    plines = (corpus / f'{PARENT}.txt').read_text(encoding='utf-8').split('\n')
    si = next((k for k, l in enumerate(plines) if ANCHOR_START in l), None)
    ei = next((k for k, l in enumerate(plines) if ANCHOR_END in l), None)
    if si is None or ei is None:
        pool = ' '.join(plines).split()
        note = 'span not located; full parent used'
    else:
        pool = (' '.join(plines[:si]) + ' ' + ' '.join(plines[ei+1:])).split()
        note = f'excised parent lines {si+1}-{ei+1} ({ei-si+1} lines)'

    rng = np.random.default_rng(20260722)
    vals = []
    for _ in range(REPS):
        st = rng.integers(0, len(pool) - size)
        win = pool[st:st + size]
        if feats == 'w':
            c = Counter(win)
        else:
            txt = re.sub(r'\s+', ' ', ' '.join(win)).strip()
            c = Counter(txt[i:i+3] for i in range(len(txt)-2))
        tot = sum(c.values())
        cv = np.array([c.get(w, 0)/tot for w in feat_list])
        Xa = np.vstack([X, cv]); Za = (Xa - Xa.mean(0))/Xa.std(0)
        Ya = fc.cmdscale(fc.distance_matrix(Xa, Za, 'delta'))
        idx = {nm: i for i, nm in enumerate(names + ['__chunk__'])}
        anch = Ya[[idx[nm] for nm in names_ref]]; mu = anch.mean(0)
        U2, s2, Vt2 = np.linalg.svd((anch - mu).T @ A)
        vals.append(((Ya[idx['__chunk__']] - mu) @ (U2 @ Vt2))[0])
    vals = np.array(vals)
    print(f'\n{lens}  ({note})')
    print(f'  Devigita: N={size}, axis1={obs:+.3f} | parent axis1={a1[PARENT]:+.3f}')
    print(f'  null n={REPS}: mean={vals.mean():+.3f} sd={vals.std():.3f} '
          f'range [{vals.min():+.3f}, {vals.max():+.3f}]')
    z = (obs - vals.mean())/vals.std()
    print(f'  observed {z:+.2f} sd above null mean; '
          f'{(vals >= obs).mean()*100:.1f}% of windows reach it')
