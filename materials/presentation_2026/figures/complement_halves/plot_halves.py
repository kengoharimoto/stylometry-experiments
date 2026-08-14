#!/usr/bin/env python3
"""Two-panel figure: shared vs residue halves of Vayu/Brahmanda/Visnu units
projected into the fixed sweet-spot delta MDS maps (W1-500, C3-500).

Deck visual language: gray base map, family hues from the deck palette,
open marker = unique residue, filled marker = shared (removed) half,
segment connects the two halves of one unit."""
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).parent

FAM = {'vayupurana': ('Vāyu', '#1a7a3a'),
       'brahmandapurana': ('Brahmāṇḍa', '#7a4ba8'),
       'visnupurana': ('Viṣṇu', '#e08a1e')}
CODE = {'vayupurana_01_frame-and-cosmogony_iast': 'V1',
        'vayupurana_02_pashupata-yoga_iast': 'V2',
        'vayupurana_03_kalpas-and-shiva-lineages_iast': 'V3',
        'vayupurana_04_bhuvana-vinyasa_iast': 'V4',
        'vayupurana_05_jyotis-and-purvardha-close_iast': 'V5',
        'vayupurana_06_prthu-and-prajapati-lineages_iast': 'V6',
        'vayupurana_07_shraddha-kalpa_iast': 'V7',
        'vayupurana_08_manu-candra-vishnu-vamsha_iast': 'V8',
        'vayupurana_09_upasamhara_iast': 'V9',
        'vayupurana_10_gaya-mahatmya_iast': 'V10',
        'vayupurana_revakhanda': 'VR',
        'brahmandapurana_khanda-1_u': 'Bḍ1',
        'brahmandapurana_khanda-2_u': 'Bḍ2',
        'brahmandapurana_khanda-3_u': 'Bḍ3',
        'visnupurana_amsa-1_u': 'Vi1', 'visnupurana_amsa-2_u': 'Vi2',
        'visnupurana_amsa-3_u': 'Vi3', 'visnupurana_amsa-4_u': 'Vi4',
        'visnupurana_amsa-5_u': 'Vi5', 'visnupurana_amsa-6_u': 'Vi6'}

def load(tag):
    base, halves = [], {}
    with open(HERE / f'halves_{tag}_500.tsv', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            if row['kind'] == 'base':
                base.append((float(row['x']), float(row['y'])))
            else:
                halves.setdefault(row['unit'], {})[row['kind']] = (
                    float(row['x']), float(row['y']))
    return np.array(base), halves

fig, axes = plt.subplots(2, 1, figsize=(13.33, 15))
for ax, (tag, sub) in zip(axes, [
        ('W1', "Burrows's Delta, 500 most frequent words (unsandhied)"),
        ('C3', "Burrows's Delta, 500 most frequent character 3-grams (sandhied)")]):
    base, halves = load(tag)
    ax.scatter(base[:, 0], base[:, 1], s=42, c='#d4d4d4',
               edgecolors='white', linewidths=0.6, zorder=1)
    for u, kinds in halves.items():
        fam = u.split('_', 1)[0]
        name, col = FAM[fam]
        (rx, ry), (sx, sy) = kinds['resid'], kinds['shared']
        ax.plot([rx, sx], [ry, sy], color=col, lw=1.1, alpha=0.65, zorder=2)
        ax.scatter([rx], [ry], s=86, facecolors='white', edgecolors=col,
                   linewidths=1.8, zorder=3)
        ax.scatter([sx], [sy], s=86, facecolors=col, edgecolors='white',
                   linewidths=1.2, zorder=3)
        mx, my = (rx + sx) / 2, (ry + sy) / 2
        ax.annotate(CODE[u], (mx, my), fontsize=10.5, fontweight='bold',
                    color=tuple(c * 0.55 for c in matplotlib.colors.to_rgb(col)),
                    xytext=(0, 7), textcoords='offset points', ha='center')
    ax.set_title(f'{sub}\nfilled = shared (removed) half · open = unique residue',
                 fontsize=13)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.annotate('', xy=(0.98, -0.015), xytext=(0.02, -0.015),
                xycoords='axes fraction',
                arrowprops=dict(arrowstyle='-|>', color='#777777', lw=1.4))
    ax.text(0.5, -0.045, 'earlier  →  later', transform=ax.transAxes,
            ha='center', fontsize=12, style='italic', color='#555555')

from matplotlib.lines import Line2D
handles = [Line2D([], [], marker='o', linestyle='', markersize=9,
                  markerfacecolor=col, markeredgecolor='white', label=name)
           for name, col in FAM.values()]
handles += [Line2D([], [], marker='o', linestyle='', markersize=9,
                   markerfacecolor=c, markeredgecolor='#666666', label=l)
            for c, l in [('#666666', 'shared (removed) half'),
                         ('white', 'unique residue')]]
fig.legend(handles=handles, ncol=5, loc='lower center', frameon=False,
           fontsize=11.5, bbox_to_anchor=(0.5, 0.005))
fig.suptitle('Shared vs unique halves of Vāyu / Brahmāṇḍa / Viṣṇu units,\n'
             'projected into the fixed 127-text drift map (gray)', fontsize=15, y=0.985)
fig.tight_layout(rect=[0, 0.03, 1, 0.96])
for ext in ['png', 'pdf']:
    fig.savefig(HERE / f'complement_halves_MDS.{ext}', dpi=200)
print('wrote', HERE / 'complement_halves_MDS.png')
