#!/usr/bin/env python3
"""B5: bootstrap consensus tree (Cosine Delta, W1) for the backup slides.

stylo's own BCT is unusable on a slide (radial plot, overlapping raw
filenames, and — because a 50–80 MFW range yields only a handful of steps —
a 0.5-consensus that collapses most of the tree into one giant polytomy).
So the tree is recomputed here from the same profiles the other figures use:

  bootstrap: resample the 80 MFW columns with replacement (B replicates)
  per replicate: Cosine Delta distances → neighbour-joining tree → splits
  consensus: greedy majority-rule (splits ≥ 50%, added in support order,
             each accepted only if compatible with those already accepted)

The result is drawn as a circular cladogram rooted on the epic core, with
leaves colored by chronological stratum (the palette of the opening map),
so the tree and the map can be read against each other.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

import figcommon as fc

B = 500                     # bootstrap replicates
SEED = 20260714
ROOT_TAXON = 'mahabharata_06-bhismaparvan'   # tree is rooted on this leaf
LABEL_SUPPORT = 6           # print support % for clusters of at least this size


def cosine_delta(Z):
    Zn = Z / np.linalg.norm(Z, axis=1, keepdims=True)
    return 1 - Zn @ Zn.T


def nj_clusters(D):
    """Neighbour-joining; return the leaf-sets of every internal node."""
    Dm = D.astype(float).copy()
    members = [{i} for i in range(len(D))]
    out = []
    while len(members) > 3:
        m = len(members)
        S = Dm.sum(1)
        Q = (m - 2) * Dm - S[:, None] - S[None, :]
        np.fill_diagonal(Q, np.inf)
        i, j = np.unravel_index(np.argmin(Q), Q.shape)
        new = members[i] | members[j]
        out.append(new)
        dnew = 0.5 * (Dm[i] + Dm[j] - Dm[i, j])
        keep = [k for k in range(m) if k not in (i, j)]
        Dn = np.zeros((len(keep) + 1, len(keep) + 1))
        Dn[:-1, :-1] = Dm[np.ix_(keep, keep)]
        Dn[-1, :-1] = Dn[:-1, -1] = dnew[keep]
        Dm = Dn
        members = [members[k] for k in keep] + [new]
    return out


def splits(D, ref, n):
    """Canonical bipartitions of the NJ tree: the side not containing `ref`."""
    allset = set(range(n))
    got = set()
    for c in nj_clusters(D):
        s = allset - c if ref in c else c
        if 2 <= len(s) <= n - 2:
            got.add(frozenset(s))
    return got


def compatible(a, b):
    return a <= b or b <= a or not (a & b)


# ---------------------------------------------------------------- consensus
names, feats, X, Z = fc.load_profiles('w', 80)
strata, labels_map, _ = fc.load_strata()
n = len(names)
ref = names.index(ROOT_TAXON)
rng = np.random.default_rng(SEED)

support = {}
for _ in range(B):
    cols = rng.integers(0, Z.shape[1], Z.shape[1])
    for s in splits(cosine_delta(Z[:, cols]), ref, n):
        support[s] = support.get(s, 0) + 1
support = {s: c / B for s, c in support.items()}

accepted = []
for s in sorted(support, key=lambda s: (-support[s], -len(s))):
    if support[s] <= 0.5:
        break
    if all(compatible(s, a) for a in accepted):
        accepted.append(s)
print(f'{len(accepted)} clusters in the majority-rule consensus '
      f'({B} replicates); mean support '
      f'{np.mean([support[s] for s in accepted]):.2f}')

# ------------------------------------------------------------------- tree
# Every accepted cluster excludes the root taxon, so they nest: the tree
# rooted on that leaf is just their inclusion hierarchy.
root = frozenset(range(n))
nodes = {root: []}                       # cluster -> children (clusters/leaves)
for c in accepted:
    nodes[c] = []


def parent_of(item, own=None):
    """Smallest accepted cluster properly containing `item`."""
    cands = [c for c in accepted if item <= c and c != own]
    return min(cands, key=len) if cands else root


for c in accepted:
    nodes[parent_of(c, own=c)].append(c)
for i in range(n):
    nodes[parent_of(frozenset({i}))].append(i)

leafset = lambda x: frozenset({x}) if isinstance(x, int) else x
mean_stratum = lambda x: np.mean([strata[names[i]] for i in leafset(x)])
for c in nodes:
    nodes[c].sort(key=lambda x: (mean_stratum(x), -len(leafset(x))))

order, depth = [], {}


def walk(node, d):
    depth[node] = d
    if isinstance(node, int):
        order.append(node)
        return
    for ch in nodes[node]:
        walk(ch, d + 1)


walk(root, 0)
maxdepth = max(depth[c] for c in nodes)

# --------------------------------------------------------------- geometry
R = 1.0
GAP = 12.0                                # degrees of blank arc at the root cut
theta = {leaf: np.deg2rad(GAP / 2 + (360 - GAP) * k / (len(order) - 1 + 1e-9))
         for k, leaf in enumerate(order)}
for c in sorted(nodes, key=len):
    if c is not root:
        theta[c] = np.mean([theta[ch] for ch in nodes[c]])
theta[root] = np.mean([theta[ch] for ch in nodes[root]])
rad = {node: R * depth[node] / maxdepth for node in depth}
for leaf in order:
    rad[leaf] = R                         # leaves aligned on the outer circle

pol = lambda r, t: (r * np.cos(t), r * np.sin(t))

# square panel on the right; the left third of the slide carries the text
fig = plt.figure(figsize=(13.33, 7.5))
H = 0.98
ax = fig.add_axes([0.345, 0.01, H * 7.5 / 13.33, H])
ax.set_aspect('equal'); ax.axis('off')
LIM = 1.58                     # room outside the leaf circle for the labels
ax.set_xlim(-LIM, LIM); ax.set_ylim(-LIM, LIM)

for c in nodes:                           # arcs + radial branches
    ts = [theta[ch] for ch in nodes[c]]
    a = np.linspace(min(ts), max(ts), 120)
    ax.plot(*pol(rad[c], a), color='#666666', lw=0.7, zorder=2)
    for ch in nodes[c]:
        r0, r1 = rad[c], rad[ch]
        if isinstance(ch, int):           # dotted leader out to the circle
            inner = R * depth[ch] / maxdepth
            ax.plot(*pol(np.array([r0, inner]), theta[ch]),
                    color='#666666', lw=0.7, zorder=2)
            ax.plot(*pol(np.array([inner, R]), theta[ch]),
                    color='#cccccc', lw=0.5, ls=(0, (1, 2)), zorder=1)
        else:
            ax.plot(*pol(np.array([r0, r1]), theta[ch]),
                    color='#666666', lw=0.7, zorder=2)

for c in accepted:                        # support: dot size, and % if large
    x, y = pol(rad[c], theta[c])
    ax.scatter([x], [y], s=6 + 26 * (support[c] - 0.5) / 0.5, c='#16324f',
               zorder=4, linewidths=0)
    if len(c) >= LABEL_SUPPORT:
        off = 1.0 if np.cos(theta[c]) >= 0 else -1.0
        ax.text(x + 0.022 * off, y + 0.018, f'{support[c] * 100:.0f}',
                fontsize=6, color='#16324f',
                ha='left' if off > 0 else 'right', va='bottom', zorder=5)

import json
disp = {d['text']: d['display'] for d in json.loads(
    (fc.ROOT / 'materials/presentation_2026/corpus_labels.json')
    .read_text(encoding='utf-8'))}
for leaf in order:
    t = theta[leaf]
    deg = np.rad2deg(t) % 360
    flip = 90 < deg < 270
    x, y = pol(R + 0.012, t)
    ax.text(x, y, disp[names[leaf]], fontsize=6.4,
            color=fc.PALETTE[strata[names[leaf]]],
            rotation=deg + 180 if flip else deg, rotation_mode='anchor',
            ha='right' if flip else 'left', va='center', zorder=5)

fig.text(0.04, 0.955, 'A tree instead of a map', fontsize=17,
         fontweight='bold', va='top')
fig.text(0.04, 0.90,
         'Bootstrap consensus tree · Cosine Delta on the same 80 words.\n'
         f'{B} replicates (words resampled with replacement); every branch\n'
         'shown is supported by more than half of them. Rooted on MBh 6.\n'
         'Dots scale with bootstrap support; numbers are percentages.',
         fontsize=9.5, color='#555555', va='top', linespacing=1.6)
fig.text(0.04, 0.20,
         'The tree recovers the groups the map shows — the epics, the old\n'
         'purāṇic core, the Bhāgavata, the Śivapurāṇa — but it has to force\n'
         'them into nested boxes, so the gradual drift between them is\n'
         'exactly what it hides.',
         fontsize=9.5, color='#333333', va='top', linespacing=1.6)

group_label = {s: labels_map[next(nm for nm in names if strata[nm] == s)]
               for s in fc.GROUP_ORDER}
handles = [Line2D([], [], marker='o', linestyle='', markersize=5,
                  markerfacecolor=fc.PALETTE[s], markeredgecolor='white',
                  label=group_label[s]) for s in fc.GROUP_ORDER]
fig.legend(handles=handles, loc='upper left', ncol=1, fontsize=8,
           frameon=False, bbox_to_anchor=(0.04, 0.71),
           handletextpad=0.3, labelspacing=0.55)

out = fc.FIGDIR / 'consensus_tree'
fig.savefig(f'{out}.png', dpi=200)
fig.savefig(f'{out}.pdf')
print('wrote', out.with_suffix('.png'))
