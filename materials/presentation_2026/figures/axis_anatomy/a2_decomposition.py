#!/usr/bin/env python3
"""A2 (axis-anatomy plan): class decomposition of the drift axis.

Which feature class SUFFICES to reproduce the axis (class-alone), and which
is NECESSARY (class-removed, refilled to 500 from the frequency ranking)?
W1 classes come from the rule-based classifier (same as the A2 bridge);
C3 trigrams are classified mechanically by majority position
(interior/final/initial/junction) and by majority source-word class, from
a fresh scan of the cleaned corpus.

Review-replacement: a perturbation run flips every ambiguous W1 assignment
(pronoun/content <-> particle boundary cases) and reports how much any
class-level rho moves. Small deltas = hand review cannot change the
conclusions.
"""
import csv
import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
MFW = 500
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'

# ── classifier (same rules as a2_bridge_c3_classes.py) ───────────────────────
INDECL = {l.strip() for l in
          (ROOT / 'materials/feature_sets/sanskrit_indeclinables_clean.txt')
          .read_text(encoding='utf-8').splitlines() if l.strip()}
INDECL |= {'caiva', 'cāpi', 'vāpi', 'naiva', 'tathaiva', 'yathaiva', 'hyeva',
           'tveva', 'caivam', 'no', 'cid', 'cit', 'svid'}
PRON = set('''sa saḥ tam taṃ tat tad te tau tān tena tasya tasmai tasmāt
tasmin tayā tayoḥ tābhiḥ tāsām teṣām teṣu taiḥ tā tāḥ tām tāṃ tasyāḥ tasyām
eṣa eṣaḥ etat etad etam ete etān etena etasya eṣā etām enam enaṃ enām enat
ayam iyam idam imam imāṃ imām ime imān anena asya asmai asmāt asmin anayā
ebhiḥ eṣām eṣu asau amum yaḥ yat yad yam yaṃ ye yau yān yena yasya yasmai
yasmāt yasmin yayā yeṣām yeṣu yaiḥ yā yāḥ yām yāṃ yasyāḥ kaḥ kim kam kaṃ ke
kena kasya kasmai kasmāt kasmin kaiḥ kā kāṃ aham mām māṃ mayā mama mahyam
mayi vayam naḥ asmān asmābhiḥ asmākam tvam tvām tvayā tava tubhyam tvayi
yūyam vaḥ yuṣmān bhavān bhavantam bhavatā svam svayam'''.split())
VERB_NARR = set('''uvāca ūcuḥ āha āhuḥ abravīt abruvan avadat provāca
prāha āsīt āsan abhavat abhavan babhūva babhūvuḥ jagāma jagmuḥ āgamat
āyayau yayau prayayau āsa cakāra cakruḥ dadau dadhau jajñe'''.split())
NUM_STEMS = ('eka', 'dvi', 'dvā', 'tri', 'catur', 'catvār', 'pañca', 'ṣaṣ',
             'ṣaḍ', 'sapta', 'aṣṭa', 'nava', 'daśa', 'śata', 'sahasra',
             'ayuta', 'koṭi')
ADI_FORMS = ('ādi', 'ādiḥ', 'ādim', 'ādau', 'ādyāḥ', 'ādyāś', 'ādayaḥ',
             'ādīni', 'ādibhiḥ', 'ādyaiḥ', 'ādikam', 'ādye')
KRAMA = {'kramāt', 'krameṇa', 'kramaśaḥ', 'kramam'}


def classify(w):
    if w in INDECL:
        return 'particle'
    if w in PRON:
        return 'pronoun'
    if w in VERB_NARR or w.endswith('tvā') or w.endswith('vīt'):
        return 'verb_narrative'
    if ((w.endswith('et') and len(w) >= 4 and w not in ('cet', 'ced'))
            or w.endswith('yāt') or w.endswith('eyuḥ') or w == 'syāt'):
        return 'verb_prescriptive'
    if (w.startswith(NUM_STEMS) or w in KRAMA or w in ADI_FORMS
            or w.endswith(ADI_FORMS[:1] + ADI_FORMS[4:])):
        return 'numeral_list'
    return 'content'


CLASSES = ['particle', 'pronoun', 'verb_narrative', 'verb_prescriptive',
           'numeral_list', 'content']
CLOSED = CLASSES[:5]

# boundary-case flips for the perturbation run (worst-case hand-review moves)
AMBIG = {'tad': 'particle', 'tat': 'particle', 'yat': 'particle',
         'yad': 'particle', 'kim': 'particle', 'te': 'particle',
         'ye': 'particle', 'svayam': 'particle', 'nāma': 'particle',
         'param': 'particle', 'punar': 'particle', 'sma': 'particle'}

manifest = {l.strip().removesuffix('.txt') for l in
            MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}


def load_x(path):
    with open(path, encoding='utf-8') as f:
        return {r['text']: float(r['x']) for r in csv.DictReader(f, delimiter='\t')}


def axis_rho(counts, feats, x_ref):
    """Delta -> classical MDS axis 1 on the given feature set; |rho| vs ref."""
    totals = [sum(c.values()) for c in counts]
    X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])
    sd = X.std(0)
    keep = sd > 0
    Z = (X[:, keep] - X[:, keep].mean(0)) / sd[keep]
    D = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)
    n = len(D)
    J = np.eye(n) - 1 / n
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    i = np.argmax(w)
    ax = V[:, i] * np.sqrt(max(w[i], 0))
    return abs(spearmanr(ax, x_ref).statistic)


def decompose(lens, counts, names, ranked, feat_class, x_ref, label):
    """class-alone and class-removed(refilled) rho table for one lens."""
    rows = []
    present = [c for c in dict.fromkeys(feat_class.values())]
    top = ranked[:MFW]
    for cl in present + ['closed_union']:
        members = ([f for f in top if feat_class[f] == cl] if cl != 'closed_union'
                   else [f for f in top if feat_class[f] in
                         ('particle', 'pronoun', 'verb_narrative',
                          'verb_prescriptive', 'numeral_list',
                          'junction', 'final', 'initial')
                         and feat_class[f] != 'content'])
        if cl == 'closed_union' and lens == 'C3':
            continue
        if not members:
            continue
        alone = axis_rho(counts, members, x_ref)
        removed_feats = [f for f in ranked if f not in set(members)][:MFW]
        removed = axis_rho(counts, removed_feats, x_ref)
        rows.append((lens, label, cl, len(members), alone, removed))
    return rows


results = []

# ── W1 ───────────────────────────────────────────────────────────────────────
W1_CORPUS = ROOT / 'corpus/epic_puranas_unsandhied'
w1_counts, w1_names = [], []
for p in sorted(W1_CORPUS.glob('*.txt')):
    if p.stem in manifest:
        w1_names.append(p.stem)
        w1_counts.append(Counter(p.read_text(encoding='utf-8').lower().split()))
raw = Counter()
for c in w1_counts:
    raw.update(c)
w1_ranked = [w for w, _ in raw.most_common(20000)]
w1_x = load_x(ROOT / 'materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv')
x_ref = np.array([w1_x[n] for n in w1_names])

base_cls = {f: classify(f) for f in w1_ranked}
results += decompose('W1', w1_counts, w1_names, w1_ranked, base_cls, x_ref, 'base')

pert_cls = dict(base_cls)
for w, cl in AMBIG.items():
    pert_cls[w] = cl
results += decompose('W1', w1_counts, w1_names, w1_ranked, pert_cls, x_ref, 'perturbed')

# ── C3 (no-space): mechanical position classes + source-word classes ─────────
C3_CORPUS = ROOT / 'corpus/epic_puranas_sandhied'
c3_counts, c3_names = [], []
for p in sorted(C3_CORPUS.glob('*.txt')):
    if p.stem in manifest:
        c3_names.append(p.stem)
        t = re.sub(r'\s+', '', p.read_text(encoding='utf-8').lower())
        c3_counts.append(Counter(t[i:i + 3] for i in range(len(t) - 2)))
rawc = Counter()
for c in c3_counts:
    rawc.update(c)
c3_ranked = [g for g, _ in rawc.most_common(20000)]
c3_x = load_x(ROOT / 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv')
xc_ref = np.array([c3_x[n] for n in c3_names])

# fresh source scan on the cleaned corpus, over the top-2000 trigrams so
# refilled sets are classified too
TOPSCAN = set(c3_ranked[:2000])
pos_counts = {g: Counter() for g in TOPSCAN}
cls_counts = {g: Counter() for g in TOPSCAN}
wc_cache = {}
for p in sorted(C3_CORPUS.glob('*.txt')):
    if p.stem not in manifest:
        continue
    for line in p.read_text(encoding='utf-8').lower().splitlines():
        toks = line.split()
        if not toks:
            continue
        stream = ''.join(toks)
        ids = []
        for wi, t in enumerate(toks):
            ids.extend([wi] * len(t))
        n = len(stream)
        for i in range(n - 2):
            g = stream[i:i + 3]
            if g not in TOPSCAN:
                continue
            a, b, c_ = ids[i], ids[i + 1], ids[i + 2]
            if a == c_:
                start = i == 0 or ids[i - 1] != a
                end = i + 3 == n or ids[i + 3] != a
                pos = ('whole' if start and end else 'initial' if start
                       else 'final' if end else 'interior')
                src = toks[a]
            else:
                pos = 'junction'
                src = toks[b]
            cl = wc_cache.get(src)
            if cl is None:
                cl = classify(src)
                wc_cache[src] = cl
            pos_counts[g][pos] += 1
            cls_counts[g][cl] += 1

pos_class = {g: (pos_counts[g].most_common(1)[0][0] if pos_counts[g] else 'interior')
             for g in TOPSCAN}
src_class = {g: (cls_counts[g].most_common(1)[0][0] if cls_counts[g] else 'content')
             for g in TOPSCAN}
c3_ranked2k = [g for g in c3_ranked if g in TOPSCAN]
results += decompose('C3', c3_counts, c3_names, c3_ranked2k, pos_class, xc_ref, 'position')
results += decompose('C3', c3_counts, c3_names, c3_ranked2k, src_class, xc_ref, 'source-class')

with open(HERE / 'a2_decomposition.tsv', 'w', encoding='utf-8') as f:
    f.write('lens\trun\tclass\tn_features\trho_alone\trho_removed\n')
    for r in results:
        f.write('\t'.join(str(v) if not isinstance(v, float) else f'{v:.4f}'
                          for v in r) + '\n')

print(f'{"lens":<4} {"run":<12} {"class":<18} {"n":>4} {"alone":>7} {"removed":>8}')
for lens, run, cl, n, a, r in results:
    print(f'{lens:<4} {run:<12} {cl:<18} {n:>4} {a:>7.3f} {r:>8.3f}')

# perturbation deltas
base = {(r[0], r[2]): (r[4], r[5]) for r in results if r[1] == 'base'}
pert = {(r[0], r[2]): (r[4], r[5]) for r in results if r[1] == 'perturbed'}
if pert:
    dmax = max(max(abs(pert[k][0] - base[k][0]), abs(pert[k][1] - base[k][1]))
               for k in pert if k in base)
    print(f'\nperturbation (12 boundary words flipped): max |delta rho| = {dmax:.4f}')
print('wrote a2_decomposition.tsv')
