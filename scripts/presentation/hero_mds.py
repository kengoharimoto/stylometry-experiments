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
import matplotlib.font_manager as fm
import matplotlib.patheffects as pe
from matplotlib.colors import to_rgb


def use_sf_pro():
    """Render figures in SF Pro Display (Apple system font), matching the deck.

    Full IAST coverage verified; falls back silently if the fonts are absent.
    """
    for f in ('Regular', 'Bold', 'RegularItalic', 'BoldItalic',
              'Semibold', 'Medium', 'Light'):
        p = f'/Library/Fonts/SF-Pro-Display-{f}.otf'
        try:
            fm.fontManager.addfont(p)
        except (FileNotFoundError, OSError):
            pass
    if any('SF Pro Display' in f.name for f in fm.fontManager.ttflist):
        plt.rcParams['font.family'] = 'SF Pro Display'


use_sf_pro()

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
ap.add_argument('--highlight', default=None,
                choices=['epic', 'oldcore', 'oldsp', 'late', 'sip', 'bhp', 'skmp'],
                help='fade all strata except the named zone (Act 3 tour slides)')
ap.add_argument('--dump-coords', metavar='PATH',
                help='write the MDS coordinates as TSV (text, x, y) and exit '
                     'without plotting — for overlay figures that must sit on '
                     'the identical layout')
ap.add_argument('--compare-metrics', action='store_true',
                help='report each metric\'s distance-matrix correlation with '
                     'the W1-delta hero matrix, then exit')
ap.add_argument('--files-from', metavar='MANIFEST',
                help='corpus manifest (one unit basename per line, as in '
                     'manifests/); the manifest name is appended to the output '
                     'filename, so variants never overwrite the deck hero')
args = ap.parse_args()

MANIFEST = None
if args.files_from:
    mpath = Path(args.files_from)
    entries = [l.strip() for l in mpath.read_text(encoding='utf-8').splitlines()]
    MANIFEST = {e[:-4] if e.endswith('.txt') else e
                for e in entries if e and not e.startswith('#')}
    MANIFEST_LABEL = mpath.stem

W1 = args.features == 'w'
MFW = args.mfw or (80 if W1 else 5000)
CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
RESULTS = sorted(ROOT.glob('results_epic_puranas_unsandhied_W1_50-80_*/' if W1 else
                           'results_epic_puranas_sandhied_C3_2000-5000_*/'))[-1]
tag = f"{'W1' if W1 else 'C3'}_{args.metric}"
OUT = FIGDIR / (f'hero_W1_delta_MDS' if (W1 and args.metric == 'delta')
                else f'companion_{tag}_MDS')
if MANIFEST is not None:
    OUT = OUT.with_name(f'{OUT.name}_{MANIFEST_LABEL}')
HIGHLIGHT_STRATA = {'epic': {1, 2}, 'oldcore': {3}, 'oldsp': {4}, 'late': {5},
                    'sip': {6}, 'bhp': {7, 8}, 'skmp': {10}}
hl = HIGHLIGHT_STRATA.get(args.highlight)
if hl:
    OUT = OUT.with_name(f'{OUT.name}_hl-{args.highlight}')
FADE, FADE_TXT = '#d4d4d4', '#b8b8b8'

# ── Stratum table ─────────────────────────────────────────────────────────────
strata, labels_map, notes = {}, {}, {}
with open(STRATA, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        strata[row['text']] = int(row['stratum'])
        labels_map[row['text']] = row['label']
        notes[row['text']] = row.get('note', '') or ''

PALETTE = {                       # 1 MBh · 2 Rām · 3 old core · 4 old SP ·
    1: '#1f5fa8', 2: '#7ba7d4',   # 5 sectarian & encyclopedic · 6 ŚiP · 7 Bhāgavata ·
    3: '#1a7a3a', 4: '#7a4ba8',   # 8 BhP+comm · 9 Śāstra · 10 Skāndamahāpurāṇa
    5: '#e08a1e', 6: '#c23b3b', 7: '#e0bf1e', 8: '#7f7f7f', 9: '#3bbfbf',
    10: '#6b4423',                # deliberately unlike the old-SP purple: the
                                  # shared name is not a shared text
    11: '#d4589e',                # epic Appendix I (rose)
    12: '#0f8bb0',                # Harivaṃśa (azure)
    13: '#87104a',                # Śivadharma (deep maroon)
    14: '#2b2b2b',                # Purāṇapañcalakṣaṇa (charcoal)
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
    if MANIFEST is not None and p.stem not in MANIFEST:
        continue
    names.append(p.stem)
    counts.append(count_fn(p))
if MANIFEST is not None:
    missing = MANIFEST - set(names)
    if missing:
        sys.exit(f'manifest units not in {CORPUS}: {sorted(missing)}')

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
        if MANIFEST is not None and p.stem not in MANIFEST:
            continue
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
    # hero: orient by convention — epics left (horizontal), Bhāgavata low
    # (vertical). Vertical is anchored on the Bhāgavata (stratum 8) rather than
    # the epics so it stays stable regardless of how the epic strata are coded.
    epic = np.array([strata[n] == 1 for n in names])
    bhag = np.array([strata[n] == 7 for n in names])   # Bhāgavata (was 8)
    if Y[epic, 0].mean() > Y[~epic, 0].mean():
        Y[:, 0] = -Y[:, 0]
    if Y[bhag, 1].mean() > 0:
        Y[:, 1] = -Y[:, 1]
else:
    # companions: rotate/reflect onto the hero layout (MDS orientation is
    # arbitrary; Procrustes alignment makes the figures directly comparable)
    ref_names, ref_counts = [], []
    for p in sorted((ROOT / 'corpus/epic_puranas_unsandhied').glob('*.txt')):
        if MANIFEST is not None and p.stem not in MANIFEST:
            continue
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
    bhag = np.array([strata[n] == 7 for n in names])   # Bhāgavata (was 8)
    if Yref[epic, 0].mean() > Yref[~epic, 0].mean():
        Yref[:, 0] = -Yref[:, 0]
    if Yref[bhag, 1].mean() > 0:
        Yref[:, 1] = -Yref[:, 1]
    A = Yref - Yref.mean(0)
    Bm = Y - Y.mean(0)
    U_, _, Vt_ = np.linalg.svd(Bm.T @ A)
    Y = Bm @ (U_ @ Vt_)

if args.dump_coords:
    with open(args.dump_coords, 'w', encoding='utf-8') as f:
        f.write('text\tx\ty\n')
        for n, (x, y) in zip(names, Y):
            f.write(f'{n}\t{x:.6f}\t{y:.6f}\n')
    print('wrote', args.dump_coords)
    sys.exit(0)

# ── Point codes and display names: shared with the other figures ─────────────
from figcommon import CODES, code, display  # noqa: E402

codes = {n: code(n) for n in names}
group_members = {s: sorted([n for n in names if strata[n] == s]) for s in GROUP_ORDER}
for s in GROUP_ORDER:   # codes must be unique within each color group
    cs = [codes[n] for n in group_members[s]]
    assert len(cs) == len(set(cs)), f'duplicate codes in group {s}: {cs}'

tiny = {n for n in names if 'FLAG: tiny' in notes[n] or 'excerpt' in notes[n]}

def darken(hexcol, f=0.55):
    return tuple(c * f for c in to_rgb(hexcol))

# ── Plot ──────────────────────────────────────────────────────────────────────
# Projection layout: the full 111-code key lives on backup slide B2; the slide
# figure spends its whole width on the map, with a compact strata-only legend
# strip along the bottom right (bottom left stays clear for the tour cards).
fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0.005, 0.145, 0.99, 0.755])
xpad = 0.025 * (Y[:, 0].max() - Y[:, 0].min())
ypad = 0.026 * (Y[:, 1].max() - Y[:, 1].min())
ax.set_xlim(Y[:, 0].min() - xpad, Y[:, 0].max() + xpad)
ax.set_ylim(Y[:, 1].min() - ypad, Y[:, 1].max() + ypad)

for s in GROUP_ORDER:
    sel = [i for i, n in enumerate(names) if strata[n] == s]
    if not sel:
        continue
    sizes = [34 if names[i] in tiny else 72 for i in sel]
    faded = hl and s not in hl
    ax.scatter(Y[sel, 0], Y[sel, 1], s=sizes,
               c=FADE if faded else PALETTE[s], alpha=0.9,
               edgecolors='white', linewidths=0.7, zorder=2 if faded else 3)

# Labels: white halo so neighboring dots can't swallow them; each starts just
# above its point, then figcommon.repel_labels nudges collisions apart and
# draws leader lines. Independent of the hl coloring — every highlight variant
# gets the identical label layout.
from figcommon import repel_labels, label_start_positions  # noqa: E402
HALO = [pe.withStroke(linewidth=2.8, foreground='white')]
start = label_start_positions(fig, ax, Y)
texts = []
for i, n in enumerate(names):
    faded = hl and strata[n] not in hl
    texts.append(ax.text(start[i, 0], start[i, 1], codes[n],
                 ha='center', va='center',
                 fontsize=10.5, fontweight='bold',
                 color=FADE_TXT if faded else darken(PALETTE[strata[n]], 0.62),
                 zorder=5 if faded else 6, path_effects=HALO))
repel_labels(fig, ax, texts, Y)

# axis annotation lives BELOW the plot area — no collision with points
fig.text(0.5, 0.126, 'earlier  →  later', ha='center', va='center',
         fontsize=14, color='#555555', style='italic')
ax.annotate('', xy=(0.97, 0.104), xytext=(0.03, 0.104),
            xycoords='figure fraction', textcoords='figure fraction',
            annotation_clip=False,
            arrowprops=dict(arrowstyle='-|>', color='#555555', lw=2.2))

feat_desc = ('80 most frequent words' if W1
             else f'{MFW} most frequent character 3-grams')
corpus_desc = 'unsandhied' if W1 else 'sandhied'
METRIC_NAMES = {'delta': 'Burrows’s Delta', 'wurzburg': 'Cosine Delta',
                'argamon': 'Argamon’s Delta', 'eder': 'Eder’s Delta',
                'cosine': 'cosine distance', 'euclidean': 'Euclidean distance',
                'manhattan': 'Manhattan distance', 'canberra': 'Canberra distance',
                'minmax': 'min-max distance'}
ax.set_title(f'{len(names)} epic and purāṇic texts, arranged only by counted linguistic habits\n'
             f'({METRIC_NAMES[args.metric]} on {feat_desc}, {corpus_desc} text · '
             'multidimensional scaling)', fontsize=15)
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(False)

# ── Strata legend (matplotlib native columns; right of the tour-card zone) ──
from matplotlib.lines import Line2D
leg = [(s, labels_map[group_members[s][0]]) for s in GROUP_ORDER if group_members[s]]
handles = [Line2D([], [], marker='o', linestyle='', markersize=8,
                  markerfacecolor=(FADE if hl and s not in hl else PALETTE[s]),
                  markeredgecolor='white', label=txt) for s, txt in leg]
# 13 groups (deck hero): anchored right of the tour-card zone. A 14th group
# (the PPL variant) would clip at the figure edge, so that case pulls the
# legend left and tightens the columns.
legend = fig.legend(handles=handles, ncol=5, loc='lower center',
                    bbox_to_anchor=(0.60 if len(leg) > 13 else 0.652, -0.014),
                    frameon=False,
                    fontsize=10.8,
                    columnspacing=0.7 if len(leg) > 13 else 0.9,
                    handletextpad=0.2, labelspacing=0.4)
for t, (s, _) in zip(legend.get_texts(), leg):
    faded = hl and s not in hl
    t.set_color(FADE_TXT if faded else darken(PALETTE[s], 0.45))
    t.set_fontweight('bold')

fig.savefig(f'{OUT}.png', dpi=200)
fig.savefig(f'{OUT}.pdf')
print('wrote', OUT.with_suffix('.png'))
