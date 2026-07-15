#!/usr/bin/env python3
"""F3: "style as unconscious countable habits" for the chronology presentation.

Left panel: the top-20 most frequent words of the unsandhied corpus (share of
all running words) — the audience sees that the features are humble particles,
not content words. Right panel: for four of these particles, per-text
frequencies in three well-separated strata (epic core, old puranic core,
Bhagavata), showing that the habits differ consistently between strata — the
entire signal the map is built from.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

import figcommon as fc

rng = np.random.default_rng(20260713)

strata, labels_map, _ = fc.load_strata()
names, feats, X, _ = fc.load_profiles('w', 80)

corpus = fc.ROOT / 'corpus/epic_puranas_unsandhied'
raw, tot = Counter(), 0
for p in sorted(corpus.glob('*.txt')):
    c = fc.word_counts(p)
    raw.update(c)
    tot += sum(c.values())
top20 = raw.most_common(20)

EXAMPLES = ['tu', 'eva', 'tathā', 'vai']         # strong stratum contrasts
GROUPS = [1, 3, 7]                               # Mahābhārata, old pur. core, BhP
GROUP_LABEL = {s: labels_map[next(n for n in names if strata[n] == s)]
               for s in GROUPS}

fig = plt.figure(figsize=(13.33, 7.5))
axl = fig.add_axes([0.06, 0.10, 0.40, 0.76])
axr = fig.add_axes([0.56, 0.10, 0.41, 0.76])

# ── Left: top-20 MFW ─────────────────────────────────────────────────────────
words = [w for w, _ in top20][::-1]
share = [100 * n / tot for _, n in top20][::-1]
bars = axl.barh(range(20), share, height=0.62, color='#5b7fa3', zorder=3)
axl.set_yticks(range(20), words, fontsize=11, style='italic')
axl.set_xlabel('share of all running words (%)', fontsize=10)
axl.set_title('the 20 most frequent words of the corpus', fontsize=12, pad=10)
for i, v in enumerate(share):
    axl.text(v + 0.04, i, f'{v:.2f}', va='center', fontsize=8, color='#555555')
axl.set_xlim(0, 4.35)
axl.tick_params(axis='x', labelsize=9)
axl.spines[['top', 'right']].set_visible(False)
axl.set_axisbelow(True)
axl.xaxis.grid(True, color='#e3e3e3', lw=0.7)

# ── Right: the same particles, counted per stratum ───────────────────────────
row_gap = 1.0
for r, w in enumerate(EXAMPLES):
    j = feats.index(w)
    y0 = (len(EXAMPLES) - 1 - r) * row_gap
    for k, s in enumerate(GROUPS):
        sel = [i for i, n in enumerate(names) if strata[n] == s]
        v = X[sel, j] * 1000
        y = y0 + (1 - k) * 0.22 + rng.uniform(-0.045, 0.045, len(sel))
        axr.scatter(v, y, s=34, c=fc.PALETTE[s], alpha=0.85,
                    edgecolors='white', linewidths=0.5, zorder=3)
        med = np.median(v)
        axr.plot([med, med], [y0 + (1 - k) * 0.22 - 0.11, y0 + (1 - k) * 0.22 + 0.11],
                 color=fc.PALETTE[s], lw=2.2, zorder=4)
    axr.text(-2.2, y0 + 0.22, w, ha='right', va='center', fontsize=13,
             style='italic', fontweight='bold')
    if r < len(EXAMPLES) - 1:
        axr.axhline(y0 - row_gap / 2, color='#e3e3e3', lw=0.7)

axr.set_xlim(-0.5, 27)
axr.set_ylim(-0.45, (len(EXAMPLES) - 1) * row_gap + 0.55)
axr.set_yticks([])
axr.set_xlabel('occurrences per 1,000 words (one dot = one text; bar = group median)',
               fontsize=10)
axr.set_title('four of these words, counted text by text', fontsize=12, pad=10)
axr.tick_params(axis='x', labelsize=9)
axr.spines[['top', 'right', 'left']].set_visible(False)
axr.set_axisbelow(True)
axr.xaxis.grid(True, color='#e3e3e3', lw=0.7)

handles = [plt.Line2D([], [], marker='o', linestyle='', markersize=7,
                      markerfacecolor=fc.PALETTE[s], markeredgecolor='white',
                      label=GROUP_LABEL[s]) for s in GROUPS]
axr.legend(handles=handles, loc='lower right', fontsize=10, frameon=False,
           handletextpad=0.2, borderaxespad=0.4)

fig.suptitle('Style as unconscious, countable habits', fontsize=15, y=0.97)

out = fc.FIGDIR / 'mfw_habits'
fig.savefig(f'{out}.png', dpi=200)
fig.savefig(f'{out}.pdf')
print('wrote', out.with_suffix('.png'))
