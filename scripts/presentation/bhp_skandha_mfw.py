#!/usr/bin/env python3
"""Backup exhibit: top-10 MFW of every Bhāgavata skandha, one panel each.

Defends the F3/slide claim that the Bhāgavata suppresses tu/eva/tathā/vai:
if the suppression were an artifact of a few books, some skandha would still
use them at purāṇic rates. Each panel footer gives the four rates per 1,000
words; the reference panel carries the old purāṇic core's medians. The
defensible uniform statement (verified 2026-07-23): all 48 cells (12 books ×
4 particles) fall below the old purāṇic core's median rate. NOT defensible:
suppression vs the whole corpus for vai (BhP ≈ MBh ≈ corpus median; only the
old core is vai-heavy) and, for Bh 5/12, eva (8.3/7.3 ≈ low-normal).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter

import figcommon as fc

PARTICLES = ['tu', 'eva', 'tathā', 'vai']        # as in mfw_chart.py
ACCENT = '#c0392b'                               # the four particles
NEUTRAL = '#a8b8c8'                              # everything else
TOPN = 10

corpus = fc.ROOT / 'corpus/epic_puranas_unsandhied'
skandhas = sorted(corpus.glob('bhagavatapurana_skandha-??_u.txt'))
assert len(skandhas) == 12, [p.name for p in skandhas]

strata, _, _ = fc.load_strata()
rest = Counter()
oldcore_rates = []
for p in sorted(corpus.glob('*.txt')):
    if p.name.startswith('bhagavatapurana_'):
        continue
    c = fc.word_counts(p)
    rest.update(c)
    if strata.get(p.stem) == 3:
        t = sum(c.values())
        oldcore_rates.append([1000 * c.get(w, 0) / t for w in PARTICLES])
import numpy as np
OC_MED = np.median(np.array(oldcore_rates), axis=0)

panels = [('rest of the corpus\n(Bhāgavata removed)', rest)]
for p in skandhas:
    n = int(p.stem.split('-')[1].split('_')[0])
    panels.append((f'Bhāgavata {n}', fc.word_counts(p)))

fig, axes = plt.subplots(3, 5, figsize=(13.33, 7.5))
fig.subplots_adjust(left=0.045, right=0.985, top=0.865, bottom=0.06,
                    wspace=0.72, hspace=0.62)
axes = axes.ravel()

for ax, (title, counts) in zip(axes, panels):
    tot = sum(counts.values())
    top = counts.most_common(TOPN)
    words = [w for w, _ in top][::-1]
    share = [100 * c / tot for _, c in top][::-1]
    colors = [ACCENT if w in PARTICLES else NEUTRAL for w in words]
    ax.barh(range(TOPN), share, height=0.66, color=colors, zorder=3)
    ax.set_yticks(range(TOPN), words, fontsize=7.5, style='italic')
    for lbl, w in zip(ax.get_yticklabels(), words):
        if w in PARTICLES:
            lbl.set_color(ACCENT)
            lbl.set_fontweight('bold')
    ax.set_xlim(0, 4.6)
    ax.set_title(title, fontsize=9.5,
                 pad=4 if '\n' in title else 10)
    ax.tick_params(axis='x', labelsize=6.5)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color='#e3e3e3', lw=0.6)
    foot = ' · '.join(f'{w} {1000 * counts.get(w, 0) / tot:.1f}'
                      for w in PARTICLES)
    ax.text(0.5, -0.30, foot, transform=ax.transAxes, ha='center',
            fontsize=6.6, color='#555555')

for ax in axes[len(panels):]:
    ax.axis('off')
note = axes[-1]
note.text(0.02, 0.97,
          'bars: share of the book\'s running\n'
          'words (%), ten most frequent words\n\n'
          'red: tu · eva · tathā · vai\n\n'
          'panel footer: occurrences of the\n'
          'four words per 1,000 words\n\n'
          'old purāṇic core medians:\n'
          + ' · '.join(f'{w} {m:.1f}' for w, m in zip(PARTICLES, OC_MED))
          + '\nevery cell of every book is lower',
          transform=note.transAxes, ha='left', va='top',
          fontsize=8.5, color='#333333', linespacing=1.45)

fig.suptitle('All twelve books of the Bhāgavata run tu, eva, tathā, vai '
             'below the old purāṇic core\'s rates',
             fontsize=14.5, y=0.965)

out = fc.FIGDIR / 'bhp_skandha_mfw'
fig.savefig(f'{out}.png', dpi=200)
fig.savefig(f'{out}.pdf')
print('wrote', out.with_suffix('.png'))
