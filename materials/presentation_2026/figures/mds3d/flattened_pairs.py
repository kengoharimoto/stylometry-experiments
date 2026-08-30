#!/usr/bin/env python3
"""Flattened pairs: 2-D-close but 3-D/Delta-distinct (Sn-Vi3 analogues).

Systematic version of the Sn-Vi3 flattening exhibit
(notes/2026-08-21_3d_projection.md): on each of the four article maps,
find every pair whose in-plane (published 2-D) distance is in the
closest 2% of all pairwise in-plane distances AND whose 3-D distance is
at least 3x the in-plane distance. For each candidate, attach the full
Delta, the mutual neighbour ranks (rank of b among a's Delta
neighbours and vice versa; 1 = nearest), and unit word counts from the
build's unsandhied corpus (for the sub-3k flag).

3-axis coordinates are read from the committed viewer HTMLs. Frame
history (2026-08-21): the C3 viewers' in-plane frame was originally
rotated ~22-28 deg from the article frame of the coords_*.tsv
(near-degenerate top eigenpair); everything THIS script outputs is
rotation-invariant (pairwise 2-D/3-D distances, Delta, ranks), so the
committed census predates the fix and stands unchanged. The viewers
have since been regenerated with full in-plane Procrustes and now
match the coords TSVs (the frame of record for axis-1 positions).
Distance tables are the same four inputs as axis3_analysis.py,
regenerable via:
  python3 scripts/presentation/hero_mds.py --mfw 500
      --files-from manifests/dicsep2026_n127_ppl.txt --dump-dist <W1 with>
  python3 scripts/presentation/hero_mds.py --mfw 500
      --corpus-dir corpus/epic_puranas_unsandhied_noreuse
      --files-from manifests/noreuse2026_n126.txt --dump-dist <W1 no>
  (C3: add --features c --strip-spaces; sandhied corpora accordingly.)

Writes flattened_pairs.tsv next to this script.

Usage: flattened_pairs.py W1_WITH C3_WITH W1_NO C3_NO
"""
import itertools
import json
import math
import re
import shlex
import sys
from pathlib import Path

import os
ROOT = Path(os.environ.get('STYLO_ROOT', '/mnt/kengo/stylometry-experiments'))
HERE = Path(__file__).parent
CLOSE_PCT = 0.02          # in-plane closeness: 2nd percentile of all pairs
RATIO = 3.0               # 3-D distance must exceed RATIO x in-plane
BHP_PREFIX = 'bhagavatapurana'

MAPS = [
    ('W1_with', 'article_W1-500_n127.html', 'epic_puranas_unsandhied'),
    ('C3_with', 'article_C3-500ns_n127.html', 'epic_puranas_unsandhied'),
    ('W1_no', 'article_W1-500_noreuse_n126.html',
     'epic_puranas_unsandhied_noreuse'),
    ('C3_no', 'article_C3-500ns_noreuse_n126.html',
     'epic_puranas_unsandhied_noreuse'),
]

if len(sys.argv) != 5:
    sys.exit(__doc__)
dist_files = dict(zip([m[0] for m in MAPS], sys.argv[1:5]))


def load_dist(fn):
    lines = Path(fn).read_text(encoding='utf-8').splitlines()
    hdr = shlex.split(lines[0])
    D = {}
    for ln in lines[1:]:
        parts = shlex.split(ln)
        D[parts[0]] = dict(zip(hdr, map(float, parts[1:])))
    return D


out = []
for tag, viewer, corpus in MAPS:
    pts = json.loads(re.search(r'const PTS = (\[.*?\]);',
                               (HERE / viewer).read_text(encoding='utf-8'),
                               re.S).group(1))
    D = load_dist(dist_files[tag])
    names = [p['name'] for p in pts]
    words = {n: len((ROOT / 'corpus' / corpus / f'{n}.txt')
                    .read_text(encoding='utf-8').split()) for n in names}

    def rank(a, b):
        return 1 + sum(1 for n in names if n not in (a, b) and D[a][n] < D[a][b])

    d2s, rows = [], []
    for a, b in itertools.combinations(pts, 2):
        d2 = math.hypot(a['x'] - b['x'], a['y'] - b['y'])
        dz = abs(a['z'] - b['z'])
        d2s.append(d2)
        rows.append((a, b, d2, math.hypot(d2, dz), dz))
    d2s.sort()
    thresh = d2s[int(CLOSE_PCT * len(d2s))]
    med = sorted(D[a][b] for a, b in itertools.combinations(names, 2))
    med = med[len(med) // 2]
    print(f'{tag}: 2-D threshold {thresh:.4f} (2nd pct), median Delta {med:.3f}')

    for a, b, d2, d3, dz in rows:
        if d2 > thresh or d3 < RATIO * max(d2, 1e-9):
            continue
        na, nb = a['name'], b['name']
        out.append({
            'map': tag, 'code_a': a['code'], 'code_b': b['code'],
            'name_a': na, 'name_b': nb,
            'd2': d2, 'd3': d3, 'dz': dz, 'delta': D[na][nb],
            'delta_vs_median': D[na][nb] / med,
            'rank_ab': rank(na, nb), 'rank_ba': rank(nb, na),
            'bhp_pair': int(na.startswith(BHP_PREFIX)
                            or nb.startswith(BHP_PREFIX)),
            'words_a': words[na], 'words_b': words[nb],
            'sub3k': int(min(words[na], words[nb]) < 3000),
        })

out.sort(key=lambda r: (r['map'], -r['dz']))
cols = ['map', 'code_a', 'code_b', 'name_a', 'name_b', 'd2', 'd3', 'dz',
        'delta', 'delta_vs_median', 'rank_ab', 'rank_ba', 'bhp_pair',
        'words_a', 'words_b', 'sub3k']
with open(HERE / 'flattened_pairs.tsv', 'w', encoding='utf-8') as f:
    f.write('\t'.join(cols) + '\n')
    for r in out:
        f.write('\t'.join(f'{r[c]:.4f}' if isinstance(r[c], float)
                          else str(r[c]) for c in cols) + '\n')
n_bhp = sum(r['bhp_pair'] for r in out)
print(f'wrote flattened_pairs.tsv: {len(out)} pairs '
      f'({n_bhp} BhP, {len(out) - n_bhp} non-BhP)')
