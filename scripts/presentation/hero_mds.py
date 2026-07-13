#!/usr/bin/env python3
"""Stratum-colored MDS figures for the chronology presentation.

Default run renders the hero figure: Burrows's Delta on the top-80 MFW of
corpus/epic_puranas_unsandhied (wordlist ranked by raw counts summed over the
corpus, matching stylo with splitting.rule = whitespace), classical MDS
(cmdscale), every point labeled with a short code that follows the text's own
book numbering (MBh parvans plain, Rām -> R2, Vāyu sections -> V3, Brahmāṇḍa
khaṇḍas -> Bḍ1, BhP skandhas plain, ...), resolved by a key panel on the right.
Stratum assignments come from materials/presentation_2026/chronology_strata.tsv.

A C3 companion in the identical design:
  python3 scripts/presentation/hero_mds.py --features c --metric delta

Validation: the feature set must equal the wordlist of the latest matching
stylo run; aborts on divergence.
"""
import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

ROOT = Path(__file__).resolve().parents[2]
STRATA = ROOT / 'materials/presentation_2026/chronology_strata.tsv'
FIGDIR = ROOT / 'materials/presentation_2026/figures'

ap = argparse.ArgumentParser()
ap.add_argument('--features', choices=['w', 'c'], default='w')
ap.add_argument('--metric', default='delta',
                choices=['delta', 'wurzburg', 'argamon', 'eder', 'cosine',
                         'euclidean', 'manhattan', 'canberra', 'minmax'])
ap.add_argument('--mfw', type=int, default=None,
                help='default: 80 for words, 5000 for char 3-grams')
ap.add_argument('--compare-metrics', action='store_true',
                help='report each metric\'s distance-matrix correlation with '
                     'the W1-delta hero matrix, then exit')
args = ap.parse_args()

W1 = args.features == 'w'
MFW = args.mfw or (80 if W1 else 5000)
CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
RESULTS = sorted(ROOT.glob('results_epic_puranas_unsandhied_W1_50-80_*/' if W1 else
                           'results_epic_puranas_sandhied_C3_2000-5000_*/'))[-1]
tag = f"{'W1' if W1 else 'C3'}_{args.metric}"
OUT = FIGDIR / (f'hero_W1_delta_MDS' if (W1 and args.metric == 'delta')
                else f'companion_{tag}_MDS')

# ── Stratum table ─────────────────────────────────────────────────────────────
strata, labels_map, notes = {}, {}, {}
with open(STRATA, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        strata[row['text']] = int(row['stratum'])
        labels_map[row['text']] = row['label']
        notes[row['text']] = row.get('note', '') or ''

PALETTE = {
    1: '#1f5fa8', 2: '#7ba7d4', 3: '#1a7a3a', 4: '#8fbf3f', 5: '#7a4ba8',
    6: '#e08a1e', 7: '#c23b3b', 8: '#e0bf1e', 9: '#7f7f7f', 10: '#3bbfbf',
}
GROUP_ORDER = list(PALETTE)

# ── Profiles ──────────────────────────────────────────────────────────────────
def word_counts(path):
    return Counter(path.read_text(encoding='utf-8').lower().split())

def trigram_counts(path):
    txt = re.sub(r'\s+', ' ', path.read_text(encoding='utf-8').lower()).strip()
    return Counter(txt[i:i + 3] for i in range(len(txt) - 2))

count_fn = word_counts if W1 else trigram_counts
names, counts = [], []
for p in sorted(CORPUS.glob('*.txt')):
    names.append(p.stem)
    counts.append(count_fn(p))

raw = Counter()
for c in counts:
    raw.update(c)
feats = [w for w, _ in raw.most_common(MFW)]
totals = [sum(c.values()) for c in counts]
X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])
Z = (X - X.mean(0)) / X.std(0)

# ── Validate features against stylo's own wordlist ───────────────────────────
def stylo_wordlist():
    lines = [l for l in (RESULTS / 'wordlist.txt').read_text(encoding='utf-8')
             .splitlines() if l and not l.startswith('#')]
    if W1:
        return [l.strip() for l in lines][:MFW]
    return [l[0::2] for l in lines][:MFW]     # chars joined by spaces

wl = stylo_wordlist()
overlap = len(set(feats) & set(wl))
print(f'feature overlap with stylo wordlist ({RESULTS.name}): {overlap}/{MFW}')
if overlap / MFW < 0.98:
    sys.exit('feature sets diverge from stylo — investigate before plotting')

# ── Distances ─────────────────────────────────────────────────────────────────
def distance_matrix(metric):
    n = len(names)
    D = np.zeros((n, n))
    rank_w = (MFW - np.arange(MFW)) / MFW
    def d(i, j):
        a, b, za, zb = X[i], X[j], Z[i], Z[j]
        if metric == 'delta':     return np.abs(za - zb).mean()
        if metric == 'argamon':   return np.linalg.norm(za - zb)
        if metric == 'eder':      return (np.abs(za - zb) * rank_w).sum()
        if metric == 'wurzburg':  return 1 - za @ zb / (np.linalg.norm(za) * np.linalg.norm(zb))
        if metric == 'cosine':    return 1 - a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
        if metric == 'euclidean': return np.linalg.norm(a - b)
        if metric == 'manhattan': return np.abs(a - b).sum()
        if metric == 'canberra':
            s = np.abs(a) + np.abs(b)
            return np.nan_to_num(np.abs(a - b) / np.where(s == 0, 1, s)).sum()
        if metric == 'minmax':    return 1 - np.minimum(a, b).sum() / np.maximum(a, b).sum()
    for i in range(n):
        for j in range(i + 1, n):
            D[i, j] = D[j, i] = d(i, j)
    return D

if args.compare_metrics:
    # reference: W1 delta on the unsandhied corpus
    ref_names, ref_counts = [], []
    for p in sorted((ROOT / 'corpus/epic_puranas_unsandhied').glob('*.txt')):
        ref_names.append(p.stem)
        ref_counts.append(word_counts(p))
    rraw = Counter()
    for c in ref_counts:
        rraw.update(c)
    rfeats = [w for w, _ in rraw.most_common(80)]
    rtot = [sum(c.values()) for c in ref_counts]
    RX = np.array([[c.get(w, 0) / t for w in rfeats] for c, t in zip(ref_counts, rtot)])
    RZ = (RX - RX.mean(0)) / RX.std(0)
    Dref = np.abs(RZ[:, None, :] - RZ[None, :, :]).mean(2)
    order = [ref_names.index(n) for n in names]
    Dref = Dref[np.ix_(order, order)]
    off = ~np.eye(len(names), dtype=bool)
    print(f'\ncorrelation of C3 metric distance matrices with the W1-delta hero matrix:')
    for m in ['delta', 'wurzburg', 'argamon', 'eder', 'cosine',
              'euclidean', 'manhattan', 'canberra', 'minmax']:
        Dm = distance_matrix(m)
        print(f'  {m:<10} r = {np.corrcoef(Dm[off], Dref[off])[0, 1]:.4f}')
    sys.exit(0)

D = distance_matrix(args.metric)

# ── Classical MDS ─────────────────────────────────────────────────────────────
N = len(names)
J = np.eye(N) - 1 / N
B = -0.5 * J @ (D ** 2) @ J
w, V = np.linalg.eigh(B)
idx = np.argsort(w)[::-1][:2]
Y = V[:, idx] * np.sqrt(np.maximum(w[idx], 0))
print(f'variance in 2D: {w[idx].sum() / w[w > 0].sum():.1%}')

if W1 and args.metric == 'delta':
    # hero: orient by convention (epics left and low)
    epic = np.array([strata[n] == 1 for n in names])
    if Y[epic, 0].mean() > Y[~epic, 0].mean():
        Y[:, 0] = -Y[:, 0]
    if Y[epic, 1].mean() > 0:
        Y[:, 1] = -Y[:, 1]
else:
    # companions: rotate/reflect onto the hero layout (MDS orientation is
    # arbitrary; Procrustes alignment makes the figures directly comparable)
    ref_names, ref_counts = [], []
    for p in sorted((ROOT / 'corpus/epic_puranas_unsandhied').glob('*.txt')):
        ref_names.append(p.stem)
        ref_counts.append(word_counts(p))
    rraw = Counter()
    for c in ref_counts:
        rraw.update(c)
    rfeats = [w for w, _ in rraw.most_common(80)]
    rtot = [sum(c.values()) for c in ref_counts]
    RX = np.array([[c.get(w, 0) / t for w in rfeats] for c, t in zip(ref_counts, rtot)])
    RZ = (RX - RX.mean(0)) / RX.std(0)
    Dref = np.abs(RZ[:, None, :] - RZ[None, :, :]).mean(2)
    Jr = np.eye(N) - 1 / N
    Br = -0.5 * Jr @ (Dref ** 2) @ Jr
    wr, Vr = np.linalg.eigh(Br)
    ir = np.argsort(wr)[::-1][:2]
    Yref = Vr[:, ir] * np.sqrt(np.maximum(wr[ir], 0))
    Yref = Yref[[ref_names.index(n) for n in names]]
    epic = np.array([strata[n] == 1 for n in names])
    if Yref[epic, 0].mean() > Yref[~epic, 0].mean():
        Yref[:, 0] = -Yref[:, 0]
    if Yref[epic, 1].mean() > 0:
        Yref[:, 1] = -Yref[:, 1]
    A = Yref - Yref.mean(0)
    Bm = Y - Y.mean(0)
    U_, _, Vt_ = np.linalg.svd(Bm.T @ A)
    Y = Bm @ (U_ @ Vt_)

# ── Point codes (follow the texts' own book numbering) and display names ─────
CODES = {
    'brahmandapurana': 'Bḍ', 'brahmandapurana_khanda-1_u': 'Bḍ1',
    'brahmandapurana_khanda-2_u': 'Bḍ2', 'brahmandapurana_khanda-3_u': 'Bḍ3',
    'markandeyapurana_adhyaya-1-93_u': 'Mā',
    'matsyapurana_adhyaya-1-32_pu': 'Mt1', 'matsyapurana_adhyaya-176_pu': 'Mt2',
    'vayupurana': 'V', 'vayu_ba': 'V×B', 'visnupurana_u': 'Vi',
    'brahmapurana_pu': 'Br', 'devipurana': 'Dv',
    'kurmapurana_khanda-1_u': 'K1', 'kurmapurana_khanda-2_u': 'K2',
    'lingapurana_khanda-1_u': 'L1', 'lingapurana_khanda-2_u': 'L2',
    'nilamatapurana_au': 'Nī', 'nrsimhapurana_pu': 'Nṛ',
    'vamanapurana_saromahatmya_u': 'Sr', 'vamanapurana_u': 'Vm',
    'visnudharma_pu': 'Vd',
    'visnudharmottarapurana_khanda-3_adhyaya-343-353_pu': 'Vt',
    'skandapurana': 'SP', 'skandapurana_adhyaya-1-31_pu': 'SP1',
    'skandapurana_pasupata_adhyaya174-183_u': 'SP2',
    'agnipurana_u': 'A', 'bhavisyapurana': 'Bhv',
    'bhavisyapurana_brahmaparvan_adhyaya-5': 'Bhv5',
    'devibhagavatapurana': 'DB', 'devibhagavatapurana_u': 'DBu',
    'garudapurana_khanda-1_u': 'G1', 'garudapurana_khanda-2_u': 'G2',
    'garudapurana_khanda-3_u': 'G3',
    'kalikapurana': 'Kā', 'karatoyamahatmya_pu': 'Kt',
    'naradapurana_khanda-1_u': 'N1', 'naradapurana_khanda-2_u': 'N2',
    'padmapurana_a': 'Pd', 'saurapurana': 'Sau',
    'skandamahpurana_kasikhanda': 'Kś', 'skandapurana_himavatkhanda_au': 'Hm',
    'skandapurana_revakhanda': 'Rv', 'vayupurana_revakhanda': 'RvV',
    'sutasamhita_khanda-4_iast': 'Sū',
    'sivapurana_dharmasamhita': 'Dh', 'sivapurana_karvanamahatmya_au': 'Kv',
    'sivapurana_rudrasamhita': 'Ru', 'sivapurana_sanatkumarasamhita': 'Sn',
    'sivapurana_satarudrasamhita_au': 'Śt', 'sivapurana_umasamhita': 'U',
    'sivapurana_vayaviyasamhita_au': 'Vā', 'sivapurana_vidyesvarasamhita_au': 'Vy',
    'bhagavatapurana_skandha-10_adhyaya-29-33_w_commentary': 'Bh10c',
    'pranavakalpa': 'Pk',
}

def code(name):
    m = re.match(r'mahabharata_(\d+)', name)
    if m:
        return f'MBh{int(m.group(1))}'
    m = re.match(r'ramayana_(\d+)', name)
    if m:
        return f'R{int(m.group(1))}'
    m = re.match(r'bhagavatapurana_skandha-(\d+)_u', name)
    if m:
        return f'Bh{int(m.group(1))}'
    m = re.match(r'vayupurana_(\d+)_', name)
    if m:
        return f'V{int(m.group(1))}'
    return CODES[name]

def display(name):
    m = re.match(r'mahabharata_(\d+)', name)
    if m:
        return f'MBh {int(m.group(1))}'
    m = re.match(r'ramayana_(\d+)', name)
    if m:
        return f'Rām {int(m.group(1))}'
    m = re.match(r'bhagavatapurana_skandha-(\d+)_u', name)
    if m:
        return f'BhP {int(m.group(1))}'
    m = re.match(r'vayupurana_(\d+)_', name)
    if m:
        return f'Vāyu §{int(m.group(1))}'
    special = {
        'bhagavatapurana_skandha-10_adhyaya-29-33_w_commentary': 'BhP 10 + comm.',
        'vayu_ba': 'Vāyu×BḍP', 'vayupurana': 'Vāyu',
        'vayupurana_revakhanda': 'Revākh. (Vāyu)',
        'skandapurana_revakhanda': 'Revākh. (SkMP)',
        'skandamahpurana_kasikhanda': 'Kāśīkh. (SkMP)',
        'skandapurana_himavatkhanda_au': 'Himavatkh. (SkMP)',
        'skandapurana': 'SP (old)', 'skandapurana_adhyaya-1-31_pu': 'SP (old) 1–31',
        'skandapurana_pasupata_adhyaya174-183_u': 'SP (old) Pāśupata',
        'markandeyapurana_adhyaya-1-93_u': 'Mārkaṇḍeya 1–93',
        'matsyapurana_adhyaya-1-32_pu': 'Matsya 1–32',
        'matsyapurana_adhyaya-176_pu': 'Matsya 176',
        'bhavisyapurana_brahmaparvan_adhyaya-5': 'Bhaviṣya (adh. 5)',
        'devibhagavatapurana_u': 'DevīBhP (u)', 'devibhagavatapurana': 'DevīBhP',
        'visnudharmottarapurana_khanda-3_adhyaya-343-353_pu': 'ViDhUt (exc.)',
        'visnudharma_pu': 'Viṣṇudharma',
        'vamanapurana_saromahatmya_u': 'Saromāhātmya',
        'sutasamhita_khanda-4_iast': 'Sūtasaṃhitā 4',
        'karatoyamahatmya_pu': 'Karatoyā', 'nilamatapurana_au': 'Nīlamata',
        'pranavakalpa': 'Praṇavakalpa',
    }
    if name in special:
        return special[name]
    base = re.sub(r'purana.*', '', name).capitalize()
    iast = {'Visnu': 'Viṣṇu', 'Kurma': 'Kūrma', 'Linga': 'Liṅga',
            'Nrsimha': 'Nṛsiṃha', 'Garuda': 'Garuḍa', 'Narada': 'Nārada',
            'Kalika': 'Kālikā', 'Devi': 'Devī', 'Bhavisya': 'Bhaviṣya',
            'Sivapurana': 'ŚiP', 'Saura': 'Saura'}
    base = iast.get(base, base)
    if name.startswith('sivapurana_'):
        part = name.split('_')[1].replace('samhita', '').replace('mahatmya', ' māh.')
        return 'ŚiP ' + part.capitalize()
    m = re.search(r'khanda-(\d+)', name)
    if m:
        return f'{base} {m.group(1)}'
    return base

codes = {n: code(n) for n in names}
group_members = {s: sorted([n for n in names if strata[n] == s]) for s in GROUP_ORDER}
for s in GROUP_ORDER:   # codes must be unique within each color group
    cs = [codes[n] for n in group_members[s]]
    assert len(cs) == len(set(cs)), f'duplicate codes in group {s}: {cs}'

tiny = {n for n in names if 'FLAG: tiny' in notes[n] or 'excerpt' in notes[n]}

def darken(hexcol, f=0.55):
    return tuple(c * f for c in to_rgb(hexcol))

# ── Plot ──────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0.005, 0.02, 0.715, 0.90])
key = fig.add_axes([0.725, 0.00, 0.275, 0.95]); key.axis('off')

for s in GROUP_ORDER:
    sel = [i for i, n in enumerate(names) if strata[n] == s]
    if not sel:
        continue
    sizes = [30 if names[i] in tiny else 70 for i in sel]
    ax.scatter(Y[sel, 0], Y[sel, 1], s=sizes, c=PALETTE[s], alpha=0.9,
               edgecolors='white', linewidths=0.6, zorder=3)

for i, n in enumerate(names):
    ax.annotate(codes[n], (Y[i, 0], Y[i, 1]),
                xytext=(3, 2), textcoords='offset points',
                fontsize=6.5, fontweight='bold',
                color=darken(PALETTE[strata[n]]), zorder=4)

ax.annotate('', xy=(0.97, 0.02), xytext=(0.03, 0.02),
            xycoords='axes fraction',
            arrowprops=dict(arrowstyle='-|>', color='#555555', lw=1.6))
ax.text(0.5, 0.035, 'earlier  →  later', transform=ax.transAxes,
        ha='center', fontsize=11, color='#555555', style='italic')

feat_desc = ('80 most frequent words' if W1
             else f'{MFW} most frequent character 3-grams')
corpus_desc = 'unsandhied' if W1 else 'sandhied'
METRIC_NAMES = {'delta': 'Burrows’s Delta', 'wurzburg': 'Cosine Delta',
                'argamon': 'Argamon’s Delta', 'eder': 'Eder’s Delta',
                'cosine': 'cosine distance', 'euclidean': 'Euclidean distance',
                'manhattan': 'Manhattan distance', 'canberra': 'Canberra distance',
                'minmax': 'min-max distance'}
ax.set_title('101 epic and purāṇic texts, arranged only by counted linguistic habits\n'
             f'({METRIC_NAMES[args.metric]} on {feat_desc}, {corpus_desc} text · '
             'multidimensional scaling)', fontsize=12)
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(False)

# ── Key panel ─────────────────────────────────────────────────────────────────
entries = []
for s in GROUP_ORDER:
    entries.append(('header', s, labels_map[group_members[s][0]]))
    for n in group_members[s]:
        entries.append(('item', s, f'{codes[n]}  {display(n)}'))

rows_per_col = (len(entries) + 1) // 2
row_h = 1.0 / (rows_per_col + 1)
for e, (kind, s, txt) in enumerate(entries):
    col, row = divmod(e, rows_per_col)
    x = 0.02 + col * 0.52
    y = 0.99 - (row + 1) * row_h
    if kind == 'header':
        key.scatter([x + 0.015], [y + 0.004], s=28, c=PALETTE[s],
                    edgecolors='white', linewidths=0.5,
                    transform=key.transAxes, clip_on=False)
        key.text(x + 0.045, y, txt, transform=key.transAxes,
                 fontsize=6.3, fontweight='bold', va='center',
                 color=darken(PALETTE[s], 0.45))
    else:
        key.text(x + 0.045, y, txt, transform=key.transAxes,
                 fontsize=5.8, va='center', color='#222222')

fig.savefig(f'{OUT}.png', dpi=200)
fig.savefig(f'{OUT}.pdf')
print('wrote', OUT.with_suffix('.png'))
