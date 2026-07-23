#!/usr/bin/env python3
"""Text-reuse network overlaid on the hero stylometric map.

Points and layout are exactly the hero figure's (figcommon.hero_layout()); on
top, an edge joins text pairs whose shared-text scan (corpus_reuse_scan.py →
materials/presentation_2026/reuse_pairs.tsv) found line-level containment at
or above a threshold: the share of the smaller text's half-śloka lines with a
rapidfuzz-confirmed match in the other.

The corpus deliberately carries some texts both whole and in parts (Vāyu and
its ten sections, Brahmāṇḍa and its khaṇḍas, old SP and two excerpts, ...), so
those units are collapsed into families first: intra-family pairs are
definitional containment, not borrowing, and are skipped; each family pair
keeps only its strongest member edge. vayu_ba (the V×B comparison unit) is
derived from two other units and never drawn.

Edges are a neutral ink so the stratum palette keeps carrying identity; width
and darkness scale with containment. The right panel ranks the links.

  python3 scripts/presentation/reuse_overlay.py [--min-containment 0.05]
"""
import argparse
import csv
import re

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

from figcommon import (FIGDIR, ROOT, PALETTE, GROUP_ORDER, code, display,
                       hero_layout, load_strata)

ap = argparse.ArgumentParser()
ap.add_argument('--min-containment', type=float, default=0.05,
                help='draw an edge at or above this line-containment share')
args = ap.parse_args()

PAIRS = ROOT / 'materials/presentation_2026/reuse_pairs.tsv'
OUT = FIGDIR / 'reuse_overlay_MDS'


def family(n):
    """Collapse whole/part/excerpt units of one work into one family."""
    if n == 'vayu_ba' or re.match(r'vayupurana(_\d+_|$)', n):
        return 'vayu'                       # Vāyu whole + ten sections + V×B
    for fam in ('brahmandapurana', 'skandapurana', 'matsyapurana',
                'devibhagavatapurana', 'bhagavatapurana_skandha-10',
                'garudapurana', 'kurmapurana', 'lingapurana', 'naradapurana'):
        if n == fam or n.startswith(fam + '_') or n.startswith(fam):
            if n.startswith(fam):
                return fam
    return n


strata, labels_map, notes = load_strata()
names, Y, _ = hero_layout()
pos = {n: Y[i] for i, n in enumerate(names)}
codes = {n: code(n) for n in names}

best = {}                                   # (fam_a, fam_b) -> strongest edge
with open(PAIRS, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        a, b = row['a'], row['b']
        if 'vayu_ba' in (a, b) or a not in pos or b not in pos:
            continue
        fa, fb = family(a), family(b)
        if fa == fb:                        # whole vs its own part: definitional
            continue
        ua, ub = int(row['units_a']), int(row['units_b'])
        na, nb = int(row['matched_a']), int(row['matched_b'])
        c = (na if ua <= ub else nb) / min(ua, ub)
        k = tuple(sorted((fa, fb)))
        if c >= args.min_containment and c > best.get(k, (None, None, 0))[2]:
            best[k] = (a, b, c)

edges = sorted(best.values(), key=lambda e: -e[2])
print(f'{len(edges)} links at containment ≥ {args.min_containment:.0%}')
for a, b, c in edges:
    print(f'  {display(a):28} ↔ {display(b):28} {c:6.1%}')

tiny = {n for n in names if 'FLAG: tiny' in notes[n] or 'excerpt' in notes[n]}


def darken(hexcol, f=0.55):
    return tuple(c * f for c in to_rgb(hexcol))


fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0.005, 0.02, 0.715, 0.90])
key = fig.add_axes([0.725, 0.00, 0.275, 0.95]); key.axis('off')

# ── Reuse edges (under the points) ───────────────────────────────────────────
EDGE_INK = '#3a3a3a'
for a, b, c in edges:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.plot([x1, x2], [y1, y2], '-', color=EDGE_INK,
            lw=0.7 + 5.0 * np.sqrt(c), alpha=0.22 + 0.6 * np.sqrt(c),
            solid_capstyle='round', zorder=1)

# ── Points and codes, exactly as the hero ────────────────────────────────────
linked = {t for a, b, _ in edges for t in (a, b)}
for s in GROUP_ORDER:
    sel = [i for i, n in enumerate(names) if strata[n] == s]
    if sel:
        ax.scatter(Y[sel, 0], Y[sel, 1],
                   s=[30 if names[i] in tiny else 70 for i in sel],
                   c=PALETTE[s], alpha=0.9, edgecolors='white',
                   linewidths=0.6, zorder=3)
for i, n in enumerate(names):
    ax.annotate(codes[n], (Y[i, 0], Y[i, 1]),
                xytext=(3, 2), textcoords='offset points',
                fontsize=6.5, fontweight='bold',
                color=darken(PALETTE[strata[n]]),
                alpha=1.0 if n in linked else 0.5, zorder=4)

ax.set_title('Shared text overlaid on the stylometric map\n'
             '(line width = share of the smaller text’s half-śloka lines '
             'recurring in the other; same map as the hero figure)',
             fontsize=12)
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(False)

# ── Key panel: ranked links ──────────────────────────────────────────────────
key.text(0.02, 0.985, f'shared-text links (≥ {args.min_containment:.0%} of '
                      'the smaller text)',
         transform=key.transAxes, fontsize=7.5, fontweight='bold', va='top')
row_h = min(0.030, 0.90 / max(len(edges), 1))
for e, (a, b, c) in enumerate(edges):
    y = 0.945 - e * row_h
    key.plot([0.02, 0.075], [y + 0.004, y + 0.004], '-', color=EDGE_INK,
             lw=0.7 + 5.0 * np.sqrt(c), alpha=0.22 + 0.6 * np.sqrt(c),
             solid_capstyle='round', transform=key.transAxes, clip_on=False)
    key.text(0.10, y, f'{c:4.0%}', transform=key.transAxes,
             fontsize=6.4, va='center', fontweight='bold', color='#222222')
    key.text(0.20, y, f'{display(a)}  ↔  {display(b)}',
             transform=key.transAxes, fontsize=6.4, va='center',
             color='#222222')
key.text(0.02, 0.004,
         'rapidfuzz ratio ≥ 80 on akṣara streams, half-śloka lines,\n'
         'char-8-gram prefilter, stock formulae excluded;\n'
         'whole/part units of one work collapsed (strongest edge kept)',
         transform=key.transAxes, fontsize=6.0, va='bottom', color='#777777')

fig.savefig(f'{OUT}.png', dpi=200)
fig.savefig(f'{OUT}.pdf')
print('wrote', OUT.with_suffix('.png'))
