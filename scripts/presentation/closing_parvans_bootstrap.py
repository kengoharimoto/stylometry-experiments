#!/usr/bin/env python3
"""D1: length bootstrap for the closing-parvans length-artifact brief.

Draw random *contiguous* word windows (1k/2k/5k/10k) from units whose
chronological position is not in doubt (MBh 3, 7, 12, Vāyu, Agni), push each
window through the identical hero pipeline, and read off where it lands on
axis 1 of the opening map. If short windows of the Śāntiparvan drift to the
epic ("earliest") pole, length — not date — is what axis 1 measures at that
pole, and the closing parvans MBh 15–18 carry no chronological signal.

Both lenses (W1 words, C3 3-grams), Burrows's Delta, aligned to the hero.
Output: figures/closing_parvans_length + printed numbers.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import re
import numpy as np

import figcommon as fc

SOURCES = [                       # (file stem, short label) — position secure
    ('mahabharata_03-aranyakaparvan', 'MBh 3'),
    ('mahabharata_07-dronaparvan', 'MBh 7'),
    ('mahabharata_12-santiparvan', 'MBh 12'),
    ('vayupurana', 'Vāyu'),
    ('agnipurana_u', 'Agni'),
]
CLOSING = [('mahabharata_15-asramavasikaparvan', 'MBh 15'),
           ('mahabharata_16-mausalaparvan', 'MBh 16'),
           ('mahabharata_17-mahaprasthanikaparvan', 'MBh 17'),
           ('mahabharata_18-svargarohanaparvan', 'MBh 18')]
SIZES = [1000, 2000, 5000, 10000]
REPS = 40
SEED = 20260715
SRC_COLOR = {'MBh 3': '#1f5fa8', 'MBh 7': '#3b7dd8', 'MBh 12': '#8fbf3f',
             'Vāyu': '#1a7a3a', 'Agni': '#e08a1e'}


def chunk_vector(tokens, feats, features):
    """Relative-frequency vector of a token window on the fixed MFW list."""
    if features == 'w':
        c = Counter(tokens)
    else:
        txt = re.sub(r'\s+', ' ', ' '.join(tokens)).strip()
        c = Counter(txt[i:i + 3] for i in range(len(txt) - 2))
    tot = sum(c.values())
    return np.array([c.get(w, 0) / tot for w in feats])


def align_to_hero(Yaug, names_aug, names_ref, Yref):
    """Procrustes-fit the 101 anchors to hero; apply same map to the chunk."""
    idx = {nm: i for i, nm in enumerate(names_aug)}
    A = Yref - Yref.mean(0)
    anch = Yaug[[idx[nm] for nm in names_ref]]
    mu = anch.mean(0)
    B = anch - mu
    U, s, Vt = np.linalg.svd(B.T @ A)
    R = U @ Vt
    chunk = (Yaug[idx['__chunk__']] - mu) @ R
    return chunk            # (axis1, axis2) of the window on the hero map


results = {}                # (feats, label, size) -> list of axis-1 values
closing_axis1 = {}          # feats -> {label: (axis1, N)}

for feats in ('w', 'c'):
    corpus = fc.ROOT / ('corpus/epic_puranas_unsandhied' if feats == 'w'
                        else 'corpus/epic_puranas_sandhied')
    names, feat_list, X, _ = fc.load_profiles(feats)
    names_ref, Yref, _ = fc.hero_layout()
    rng = np.random.default_rng(SEED)

    # real closing-parvan axis-1 (from the full unit), for reference lines
    Yfull = fc.cmdscale(fc.distance_matrix(X, (X - X.mean(0)) / X.std(0),
                                           'delta'))
    Yfull = Yfull[[names.index(nm) for nm in names_ref]]
    Af = Yref - Yref.mean(0); Bf = Yfull - Yfull.mean(0)
    U, s, Vt = np.linalg.svd(Bf.T @ Af)
    Yfull = Bf @ (U @ Vt)
    a1_ref = {nm: Yfull[i, 0] for i, nm in enumerate(names_ref)}
    closing_axis1[feats] = {
        lab: (a1_ref[nm], len((corpus / f'{nm}.txt').read_text().split()))
        for nm, lab in CLOSING}

    for stem, label in SOURCES:
        toks = (corpus / f'{stem}.txt').read_text(encoding='utf-8').split()
        for size in SIZES:
            if size > len(toks) - 1:
                continue
            vals = []
            for _ in range(REPS):
                start = rng.integers(0, len(toks) - size)
                cv = chunk_vector(toks[start:start + size], feat_list, feats)
                Xaug = np.vstack([X, cv])
                Zaug = (Xaug - Xaug.mean(0)) / Xaug.std(0)
                D = fc.distance_matrix(Xaug, Zaug, 'delta')
                Yaug = fc.cmdscale(D)
                chunk = align_to_hero(Yaug, names + ['__chunk__'],
                                      names_ref, Yref)
                vals.append(chunk[0])
            results[(feats, label, size)] = vals
            print(f'{("W1" if feats=="w" else "C3")}  {label:<7} '
                  f'N={size:>6}  axis1 mean={np.mean(vals):+.3f} '
                  f'sd={np.std(vals):.3f}  '
                  f'[{np.min(vals):+.2f},{np.max(vals):+.2f}]')

# ------------------------------------------------------------------- figure
fig, axes = plt.subplots(1, 2, figsize=(13.33, 7.5))
fig.subplots_adjust(left=0.055, right=0.79, top=0.76, bottom=0.165, wspace=0.14)
xpos = {s: np.log10(s) for s in SIZES}

for ax, feats in zip(axes, ('w', 'c')):
    a1c = closing_axis1[feats]
    # the epic pole: use MBh 7 full-unit axis-1 as the "genuine early" mark
    for lab, (a1, N) in a1c.items():
        ax.scatter([np.log10(N)], [a1], marker='*', s=190,
                   c='#c23b3b', edgecolors='white', linewidths=0.6, zorder=6)
        ax.annotate(f'{lab}', (np.log10(N), a1), fontsize=8, color='#c23b3b',
                    xytext=(4, 4), textcoords='offset points', zorder=6)
    for stem, label in SOURCES:
        xs, means, sds = [], [], []
        for size in SIZES:
            key = (feats, label, size)
            if key not in results:
                continue
            v = results[key]
            x = xpos[size] + (hash(label) % 5 - 2) * 0.012
            ax.scatter([x] * len(v), v, s=9, c=SRC_COLOR[label], alpha=0.35,
                       zorder=3, linewidths=0)
            xs.append(x); means.append(np.mean(v)); sds.append(np.std(v))
        ax.plot(xs, means, '-', color=SRC_COLOR[label], lw=1.6, zorder=4,
                label=label)
        ax.scatter(xs, means, s=26, c=SRC_COLOR[label], edgecolors='white',
                   linewidths=0.6, zorder=5)
    ax.set_xticks([np.log10(s) for s in SIZES])
    ax.set_xticklabels([f'{s//1000}k' for s in SIZES], fontsize=9)
    ax.set_xlabel('contiguous sample size (words)', fontsize=10)
    ax.set_title('W1 · words' if feats == 'w' else 'C3 · character 3-grams',
                 fontsize=12)
    ax.axhline(0, color='#dddddd', lw=0.8, zorder=1)
    for sp in ('top', 'right'):
        ax.spines[sp].set_color('#cccccc')
    ax.grid(axis='y', color='#eeeeee', lw=0.6)

axes[0].set_ylabel('position on axis 1 of the opening map\n'
                   '←  earlier / epic pole        later  →', fontsize=10)

handles, labels_ = axes[0].get_legend_handles_labels()
from matplotlib.lines import Line2D
handles.append(Line2D([], [], marker='*', linestyle='', markersize=11,
                      markerfacecolor='#c23b3b', markeredgecolor='white',
                      label='MBh 15–18 (full unit)'))
fig.legend(handles=handles, loc='center left', bbox_to_anchor=(0.805, 0.5),
           fontsize=9, frameon=False, title='sampled from\n(secure position)',
           title_fontsize=9, labelspacing=0.7)

fig.suptitle('Why do the last Parvans of the Mahābhārata land at the epic '
             'pole? Can the length be the reason?',
             fontsize=15, x=0.055, ha='left', y=0.955)
fig.text(0.055, 0.895,
         'Random contiguous windows of securely-placed texts (MBh 3/7/12, '
         'Vāyu, Agni), each pushed through the identical pipeline and placed\n'
         'on the opening map. Two failure modes converge on the same length: '
         'the 3-gram lens drifts systematically leftward as the window\n'
         'shrinks, while the word lens keeps its mean but scatters so widely '
         'that single short windows reach the epic pole. The closing\n'
         'parvans (red) are single draws that small — MBh 16–18 sit inside '
         'the 1–2k scatter; only MBh 15, four times longer, stands apart.',
         fontsize=9.5, color='#555555', va='top', linespacing=1.5)

matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.it'] = 'SF Pro Display:italic'
fig.text(0.5, 0.025,
         'Yet length is not the whole story: merged into one ~17k-word unit '
         'the closing parvans stay at the pole.\nSo the age of the material '
         'that might have been $\\it{added}$ could be old, after all? '
         'Something to consider…',
         ha='center', va='bottom', fontsize=10, color='#16324f',
         fontweight='bold', linespacing=1.4)

out = fc.FIGDIR / 'closing_parvans_length'
fig.savefig(f'{out}.png', dpi=200)
fig.savefig(f'{out}.pdf')
print('\nwrote', out.with_suffix('.png'))
