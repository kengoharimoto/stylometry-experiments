#!/usr/bin/env python3
"""Dot-strip: drift-axis percentile of each unit's unique residue and its
shared material split by counterpart family (PPL-parallel, Vayu-Bd common,
other), W1-500 and C3-500 panels. Shaded band = constituted PPL Textgruppen
I/II/ungrouped on the same map."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).parent

CODE = {'vayupurana_01_frame-and-cosmogony_iast': 'V1 frame–cosmogony',
        'vayupurana_02_pashupata-yoga_iast': 'V2 pāśupata-yoga',
        'vayupurana_03_kalpas-and-shiva-lineages_iast': 'V3 kalpas–śiva-lineages',
        'vayupurana_04_bhuvana-vinyasa_iast': 'V4 bhuvana-vinyāsa',
        'vayupurana_05_jyotis-and-purvardha-close_iast': 'V5 jyotis',
        'vayupurana_06_prthu-and-prajapati-lineages_iast': 'V6 pṛthu–prajāpati',
        'vayupurana_07_shraddha-kalpa_iast': 'V7 śrāddha-kalpa',
        'vayupurana_08_manu-candra-vishnu-vamsha_iast': 'V8 vaṃśas',
        'vayupurana_09_upasamhara_iast': 'V9 upasaṃhāra',
        'vayupurana_10_gaya-mahatmya_iast': 'V10 gayā-māhātmya',
        'vayupurana_revakhanda': 'V Revākhaṇḍa',
        'brahmandapurana_khanda-1_u': 'Bḍ1',
        'brahmandapurana_khanda-2_u': 'Bḍ2',
        'brahmandapurana_khanda-3_u': 'Bḍ3',
        'visnupurana_amsa-1_u': 'Vi1', 'visnupurana_amsa-2_u': 'Vi2',
        'visnupurana_amsa-3_u': 'Vi3', 'visnupurana_amsa-4_u': 'Vi4',
        'visnupurana_amsa-5_u': 'Vi5', 'visnupurana_amsa-6_u': 'Vi6'}
UNITS = list(CODE)

KIND_COL = {'ppl': '#1f5fa8', 'vayubd': '#1a7a3a', 'other': '#e08a1e'}
KIND_LBL = {'ppl': 'PPL-parallel', 'vayubd': 'Vāyu↔Bḍ common', 'other': 'other families'}
MIN_WORDS = 150

def load(tag):
    rows, band = {}, []
    with open(HERE / f'subsets_{tag}_500.tsv', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            p = min(float(row['pct']), 100.0)
            if row['kind'] == 'base':
                if row['unit'] in ('kirfel_ppl_textgruppe_I_col1',
                                   'kirfel_ppl_textgruppe_II_col1',
                                   'kirfel_ppl_ungrouped_col1'):
                    band.append(p)
            else:
                w = int(row['words']) if row['words'] else 0
                rows.setdefault(row['unit'], {})[row['kind']] = (p, w)
    ci = {}
    bpath = HERE / f'bootstrap_{tag}_500.tsv'
    if bpath.exists():
        with open(bpath, encoding='utf-8') as f:
            for row in csv.DictReader(f, delimiter='\t'):
                ci[(row['unit'], row['kind'])] = (float(row['lo']), float(row['hi']))
    return rows, (min(band), max(band)), ci

fig, axes = plt.subplots(1, 2, figsize=(13.33, 8.4), sharey=True)
ys = range(len(UNITS) - 1, -1, -1)
for ax, tag, sub in [(axes[0], 'W1', '500 most frequent words'),
                     (axes[1], 'C3', '500 most frequent character 3-grams')]:
    rows, band, ci = load(tag)
    ax.axvspan(band[0], band[1], color='#1f5fa8', alpha=0.10, zorder=0)
    ax.text((band[0] + band[1]) / 2, len(UNITS) / 2 - 0.5, 'constituted PPL I / II',
            ha='center', va='center', rotation=90, fontsize=10,
            color='#1f5fa8', alpha=0.75, style='italic', zorder=1)
    for y, u in zip(ys, UNITS):
        ax.axhline(y, color='#eeeeee', lw=0.8, zorder=0)
        r = rows.get(u, {})
        # slight per-kind vertical offsets so whiskers do not overprint
        offs = {'resid': 0.22, 'ppl': 0.07, 'vayubd': -0.07, 'other': -0.22}
        if 'resid' in r:
            yy = y + offs['resid']
            if (u, 'resid') in ci:
                lo, hi = ci[(u, 'resid')]
                ax.plot([lo, hi], [yy, yy], color='#888888', lw=1.6,
                        alpha=0.55, solid_capstyle='butt', zorder=2)
            ax.scatter(r['resid'][0], yy, s=64, facecolors='white',
                       edgecolors='#555555', linewidths=1.6, zorder=3)
        for kind in ('ppl', 'vayubd', 'other'):
            if kind not in r:
                continue
            p, w = r[kind]
            thin = w < MIN_WORDS
            yy = y + offs[kind]
            if (u, kind) in ci and not thin:
                lo, hi = ci[(u, kind)]
                ax.plot([lo, hi], [yy, yy], color=KIND_COL[kind], lw=1.6,
                        alpha=0.5, solid_capstyle='butt', zorder=2)
            ax.scatter(p, yy, s=26 if thin else 70, color=KIND_COL[kind],
                       alpha=0.45 if thin else 1.0, edgecolors='white',
                       linewidths=0.8, zorder=4)
    ax.set_title(f"{tag} — Burrows's Delta, {sub}", fontsize=12.5)
    ax.set_xlim(0, 100)
    ax.set_xlabel('drift-axis percentile   (earlier → later)', fontsize=11)
    ax.tick_params(axis='x', labelsize=10)
    for sp in ax.spines.values():
        sp.set_visible(False)
axes[0].set_yticks(list(ys))
axes[0].set_yticklabels([CODE[u] for u in UNITS], fontsize=10.5)
axes[1].tick_params(axis='y', length=0)

handles = [Line2D([], [], marker='o', linestyle='', markersize=9,
                  markerfacecolor='white', markeredgecolor='#555555',
                  label='unique residue')]
handles += [Line2D([], [], marker='o', linestyle='', markersize=9,
                   markerfacecolor=KIND_COL[k], markeredgecolor='white',
                   label=KIND_LBL[k]) for k in ('ppl', 'vayubd', 'other')]
handles += [Line2D([], [], marker='o', linestyle='', markersize=5,
                   markerfacecolor='#999999', alpha=0.45,
                   markeredgecolor='white', label=f'< {MIN_WORDS} words (unreliable)')]
fig.legend(handles=handles, ncol=5, loc='lower center', frameon=False, fontsize=10.5)
fig.suptitle('Shared material split by counterpart family: drift-axis position per layer\n'
             '(supplementary projection into the fixed 127-text sweet-spot maps)',
             fontsize=14)
fig.tight_layout(rect=[0, 0.05, 1, 0.92])
for ext in ('png', 'pdf'):
    fig.savefig(HERE / f'subset_layers_dotstrip.{ext}', dpi=200)
print('wrote', HERE / 'subset_layers_dotstrip.png')
