#!/usr/bin/env python3
"""Hero MDS plot for the chronology presentation.

Recomputes Burrows's Delta (mean |dz| over the top-80 MFW; wordlist ranked by
raw counts summed over the corpus, matching stylo) on
corpus/epic_puranas_unsandhied, runs classical MDS (cmdscale), and renders the
stratum-colored scatter used as the opening slide: every point carries a serial
number within its group, resolved by the key panel on the right. Stratum
assignments come from materials/presentation_2026/chronology_strata.tsv.

Validation: the 80-word feature set must equal the wordlist of the latest
stylo W1 run (which uses splitting.rule = whitespace); aborts on divergence.

Usage: python3 scripts/presentation/hero_mds.py
Writes materials/presentation_2026/figures/hero_W1_delta_MDS.{png,pdf}
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / 'corpus/epic_puranas_unsandhied'
STRATA = ROOT / 'materials/presentation_2026/chronology_strata.tsv'
RESULTS = sorted(ROOT.glob('results_epic_puranas_unsandhied_W1_50-80_*/'))[-1]
OUT = ROOT / 'materials/presentation_2026/figures/hero_W1_delta_MDS'
MFW = 80

# ── Stratum table ─────────────────────────────────────────────────────────────
strata, labels_map, notes = {}, {}, {}
with open(STRATA, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        strata[row['text']] = int(row['stratum'])
        labels_map[row['text']] = row['label']
        notes[row['text']] = row.get('note', '') or ''

PALETTE = {
    1: '#1f5fa8',   # epic core          — deep blue
    2: '#7ba7d4',   # late epic          — light blue
    3: '#1a7a3a',   # old puranic core   — green
    4: '#8fbf3f',   # middle puranic     — yellow-green
    5: '#7a4ba8',   # old Skandapurana   — purple
    6: '#e08a1e',   # late sectarian     — orange
    7: '#c23b3b',   # Sivapurana         — red
    8: '#e0bf1e',   # Bhagavata          — gold
    9: '#7f7f7f',   # BhP w/ commentary  — grey
    10: '#3bbfbf',  # Sastra             — teal
}
GROUP_ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# ── Delta distances ───────────────────────────────────────────────────────────
names, counts = [], []
for p in sorted(CORPUS.glob('*.txt')):
    words = p.read_text(encoding='utf-8').lower().split()
    names.append(p.stem)
    counts.append(Counter(words))

# stylo ranks the wordlist by raw counts summed over the whole corpus
raw = Counter()
for c in counts:
    raw.update(c)
feats = [w for w, _ in raw.most_common(MFW)]
totals = [sum(c.values()) for c in counts]
X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])
Z = (X - X.mean(0)) / X.std(0)
D = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)

# ── Validate features against stylo's own wordlist (latest W1 run) ───────────
stylo_wl = [w.strip() for w in (RESULTS / 'wordlist.txt').read_text().splitlines()
            if w.strip() and not w.startswith('#')][:MFW]
overlap = len(set(feats) & set(stylo_wl))
print(f'MFW overlap with stylo wordlist ({RESULTS.name}): {overlap}/{MFW}')
if overlap < MFW:
    sys.exit('feature sets diverge from stylo — investigate before plotting')

# ── Classical MDS ─────────────────────────────────────────────────────────────
N = len(names)
J = np.eye(N) - 1 / N
B = -0.5 * J @ (D ** 2) @ J
w, V = np.linalg.eigh(B)
idx = np.argsort(w)[::-1][:2]
Y = V[:, idx] * np.sqrt(np.maximum(w[idx], 0))
print(f'variance in 2D: {w[idx].sum() / w[w > 0].sum():.1%}')

# Orient: epic core on the left (earlier -> later reads left to right)
epic = np.array([strata[n] == 1 for n in names])
if Y[epic, 0].mean() > Y[~epic, 0].mean():
    Y[:, 0] = -Y[:, 0]
if Y[epic, 1].mean() > 0:          # keep epics low-left for stability across runs
    Y[:, 1] = -Y[:, 1]

# ── Display names ─────────────────────────────────────────────────────────────
def display(name: str) -> str:
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
        'vayu_ba': 'Vāyu×BḍP',
        'vayupurana': 'Vāyu',
        'vayupurana_revakhanda': 'Revākh. (Vāyu)',
        'skandapurana_revakhanda': 'Revākh. (SkMP)',
        'skandamahpurana_kasikhanda': 'Kāśīkh. (SkMP)',
        'skandapurana_himavatkhanda_au': 'Himavatkh. (SkMP)',
        'skandapurana': 'SP (old)',
        'skandapurana_adhyaya-1-31_pu': 'SP (old) 1–31',
        'skandapurana_pasupata_adhyaya174-183_u': 'SP (old) Pāśupata',
        'markandeyapurana_adhyaya-1-93_u': 'Mārkaṇḍeya 1–93',
        'matsyapurana_adhyaya-1-32_pu': 'Matsya 1–32',
        'matsyapurana_adhyaya-176_pu': 'Matsya 176',
        'bhavisyapurana_brahmaparvan_adhyaya-5': 'Bhaviṣya (adh. 5)',
        'devibhagavatapurana_u': 'DevīBhP (u)',
        'devibhagavatapurana': 'DevīBhP',
        'visnudharmottarapurana_khanda-3_adhyaya-343-353_pu': 'ViDhUt (exc.)',
        'visnudharma_pu': 'Viṣṇudharma',
        'vamanapurana_saromahatmya_u': 'Saromāhātmya',
        'sutasamhita_khanda-4_iast': 'Sūtasaṃhitā 4',
        'karatoyamahatmya_pu': 'Karatoyā',
        'nilamatapurana_au': 'Nīlamata',
        'pranavakalpa': 'Praṇavakalpa',
    }
    if name in special:
        return special[name]
    base = re.sub(r'purana.*', '', name)
    base = base.capitalize()
    iast = {'Visnu': 'Viṣṇu', 'Kurma': 'Kūrma', 'Linga': 'Liṅga', 'Nrsimha': 'Nṛsiṃha',
            'Garuda': 'Garuḍa', 'Narada': 'Nārada', 'Kalika': 'Kālikā', 'Devi': 'Devī',
            'Bhavisya': 'Bhaviṣya', 'Sivapurana': 'ŚiP', 'Saura': 'Saura'}
    base = iast.get(base, base)
    if name.startswith('sivapurana_'):
        part = name.split('_')[1].replace('samhita', '').replace('mahatmya', ' māh.')
        return 'ŚiP ' + part.capitalize()
    m = re.search(r'khanda-(\d+)', name)
    if m:
        return f'{base} {m.group(1)}'
    return base

tiny = {n for n in names if 'FLAG: tiny' in notes[n] or 'excerpt' in notes[n]}

# ── Serial numbers within each group ─────────────────────────────────────────
from matplotlib.colors import to_rgb

def darken(hexcol, f=0.55):
    return tuple(c * f for c in to_rgb(hexcol))

group_members = {s: sorted([n for n in names if strata[n] == s]) for s in GROUP_ORDER}
serial = {}
for s in GROUP_ORDER:
    for k, n in enumerate(group_members[s], 1):
        serial[n] = k

# ── Plot ──────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(13.33, 7.5))   # 16:9 slide
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
    ax.annotate(str(serial[n]), (Y[i, 0], Y[i, 1]),
                xytext=(3, 2), textcoords='offset points',
                fontsize=6.5, fontweight='bold',
                color=darken(PALETTE[strata[n]]), zorder=4)

ax.annotate('', xy=(0.97, 0.02), xytext=(0.03, 0.02),
            xycoords='axes fraction',
            arrowprops=dict(arrowstyle='-|>', color='#555555', lw=1.6))
ax.text(0.5, 0.035, 'earlier  →  later', transform=ax.transAxes,
        ha='center', fontsize=11, color='#555555', style='italic')

ax.set_title('101 epic and purāṇic texts, arranged only by counted linguistic habits\n'
             '(Burrows’s Delta on 80 most frequent words · multidimensional scaling)',
             fontsize=12)
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(False)

# ── Key panel: two columns listing every numbered text ───────────────────────
entries = []   # (kind, group, text)
for s in GROUP_ORDER:
    entries.append(('header', s, labels_map[group_members[s][0]]))
    for n in group_members[s]:
        entries.append(('item', s, f'{serial[n]}  {display(n)}'))

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
