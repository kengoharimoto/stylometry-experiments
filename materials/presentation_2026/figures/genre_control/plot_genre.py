#!/usr/bin/env python3
"""Vamsa genre control figure: per panel text, the genealogy-like half (gen)
vs the remainder (rest) on the drift axis, with 95% line-bootstrap CIs.
PPL-witness texts (whose genealogy sections transmit pancalaksana material)
are marked; the constituted PPL I/II band is shaded."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).parent

LABEL = {'mahabharata_01-adiparvan': 'MBh 1 Ādi',
         'harivamsa': 'Harivaṃśa †',
         'matsyapurana_pu': 'Matsya †',
         'markandeyapurana': 'Mārkaṇḍeya',
         'brahmapurana_pu': 'Brahma †',
         'agnipurana_u': 'Agni',
         'bhavisyapurana': 'Bhaviṣya',
         'garudapurana_khanda-1_u': 'Garuḍa 1',
         'bhagavatapurana_skandha-09_u': 'BhP 9',
         'kurmapurana_khanda-1_u': 'Kūrma 1',
         'padmapurana_a': 'Padma A',
         'vayupurana_08_manu-candra-vishnu-vamsha_iast': 'V8 vaṃśas †',
         'vayupurana_06_prthu-and-prajapati-lineages_iast': 'V6 pṛthu–praj. †'}
ORDER = list(LABEL)
GEN_COL, REST_COL = '#1a7a3a', '#7f7f7f'
BAND = {'W1': (22, 38), 'C3': (22, 28)}   # constituted PPL I/II/ungrouped

def load(tag):
    d = {}
    with open(HERE / f'genre_control_{tag}_500.tsv', encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            d[(r['unit'], r['kind'])] = (float(r['est']), float(r['lo']), float(r['hi']))
    return d

fig, axes = plt.subplots(1, 2, figsize=(13.33, 6.6), sharey=True)
ys = range(len(ORDER) - 1, -1, -1)
for ax, tag, sub in [(axes[0], 'W1', '500 most frequent words'),
                     (axes[1], 'C3', '500 most frequent character 3-grams')]:
    d = load(tag)
    b0, b1 = BAND[tag]
    ax.axvspan(b0, b1, color='#1f5fa8', alpha=0.10, zorder=0)
    ax.text((b0 + b1) / 2, len(ORDER) / 2 - 0.5, 'constituted PPL I / II',
            ha='center', va='center', rotation=90, fontsize=10,
            color='#1f5fa8', alpha=0.75, style='italic', zorder=1)
    for y, u in zip(ys, ORDER):
        ax.axhline(y, color='#eeeeee', lw=0.8, zorder=0)
        if (u, 'gen') not in d or (u, 'rest') not in d:
            continue
        ge, gl, gh = d[(u, 'gen')]
        re_, rl, rh = d[(u, 'rest')]
        ax.plot([ge, re_], [y, y], color='#cccccc', lw=1.0, zorder=2)
        for est, lo, hi, col, yy in [(re_, rl, rh, REST_COL, y + 0.10),
                                     (ge, gl, gh, GEN_COL, y - 0.10)]:
            ax.plot([lo, hi], [yy, yy], color=col, lw=1.6, alpha=0.5,
                    solid_capstyle='butt', zorder=2)
            ax.scatter(est, yy, s=64, color=col, edgecolors='white',
                       linewidths=0.9, zorder=3)
    ax.set_title(f"{tag} — Burrows's Delta, {sub}", fontsize=12.5)
    ax.set_xlim(0, 100)
    ax.set_xlabel('drift-axis percentile   (earlier → later)', fontsize=11)
    for sp in ax.spines.values():
        sp.set_visible(False)
axes[0].set_yticks(list(ys))
axes[0].set_yticklabels([LABEL[u] for u in ORDER], fontsize=10.5)
axes[1].tick_params(axis='y', length=0)

handles = [Line2D([], [], marker='o', linestyle='', markersize=9,
                  markerfacecolor=GEN_COL, markeredgecolor='white',
                  label='genealogy-like verses'),
           Line2D([], [], marker='o', linestyle='', markersize=9,
                  markerfacecolor=REST_COL, markeredgecolor='white',
                  label='rest of the same text')]
fig.legend(handles=handles, ncol=2, loc='lower center', frameon=False, fontsize=11)
fig.suptitle('Vaṃśa genre control: genealogy-like verses vs the rest, within one text\n'
             '† = PPL witness (its genealogy text transmits pañcalakṣaṇa material)',
             fontsize=13.5)
fig.tight_layout(rect=[0, 0.06, 1, 0.90])
for ext in ('png', 'pdf'):
    fig.savefig(HERE / f'genre_control_dotplot.{ext}', dpi=200)
print('wrote', HERE / 'genre_control_dotplot.png')
