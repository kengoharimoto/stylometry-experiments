#!/usr/bin/env python3
"""Interactive 3-D MDS viewer: one self-contained HTML per distance table.

The 2-D hero maps compress the crowded middle; pairs like Sn/Vi3 that are
Delta 0.45 apart (rank ~50 in each other's neighbour lists) land on top of
each other. A third MDS axis (6.3% share on the no-reuse W1 table, vs
14.0/12.4 for axes 1-2) recovers much of that separation, and a rotatable
view keeps it legible: the "Front" button is exactly the published 2-D
plane, and dragging shows what the flattening hid.

Writes materials/presentation_2026/figures/mds3d/<name>.html — vanilla
canvas JS, no dependencies, works offline in any browser.

Usage:
  python3 scripts/presentation/mds3d_viewer.py DIST_TABLE OUT_NAME \
      [--title T] [--subtitle S] [--ref COORDS_TSV] \
      [--highlight TEXTNAME ...] [--note TEXT]

DIST_TABLE is a stylo distance table (quoted names header + rows).
--ref: published 2-D coords TSV (text/x/y); the Front plane is
Procrustes-rotated in-plane onto it (2026-08-21 fix — sign flips alone
left the C3 Front planes 22-28 deg off the article frame; z is
untouched). Without it, axis 1 is oriented MBh-left and axis 2 is left
as computed. --highlight (repeatable) rings
those units; if exactly two are given, a dashed tether with a live
distance readout connects them.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figcommon  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / 'materials/presentation_2026/figures/mds3d'
STRATA = ROOT / 'materials/presentation_2026/chronology_strata.tsv'

GROUPS_LEGEND = [
    ('#1f5fa8', 'Mahābhārata'), ('#7ba7d4', 'Rāmāyaṇa'),
    ('#1a7a3a', 'old purāṇic core'), ('#7a4ba8', 'old Skandapurāṇa'),
    ('#e08a1e', 'sectarian & encyclopedic'), ('#c23b3b', 'Śivapurāṇa'),
    ('#e0bf1e', 'Bhāgavata'), ('#7f7f7f', 'BhP + commentary'),
    ('#3bbfbf', 'śāstra'), ('#6b4423', 'Skāndamahāpurāṇa'),
    ('#d4589e', 'epic Appendix I'), ('#0f8bb0', 'Harivaṃśa'),
    ('#87104a', 'Śivadharma'), ('#2b2b2b', 'Purāṇapañcalakṣaṇa'),
]
HL_COLORS = ['#b8860b', '#c2185b', '#00695c', '#4527a0']


def read_dist(path):
    with open(path) as f:
        names = [h.strip('"') for h in f.readline().split()]
        D = np.array([[float(x) for x in line.split()[1:]] for line in f])
    return names, D


def mds3(D):
    n = len(D)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1]
    w, V = w[idx], V[:, idx]
    shares = w[:6] / w[w > 0].sum()
    return V[:, :3] * np.sqrt(w[:3]), shares


def orient(X, names, ref_path):
    if ref_path:
        # full in-plane 2-D Procrustes onto the published coords, not
        # just sign flips: on C3 the raw eigen axes sit 22-28 deg from
        # the article frame (near-degenerate top eigenpair), so sign
        # flipping alone left the Front plane tilted (fixed 2026-08-21;
        # z is untouched — an in-plane rotation)
        ref = {r['text']: (float(r['x']), float(r['y']))
               for r in csv.DictReader(open(ref_path), delimiter='\t')}
        shared = [i for i, n in enumerate(names) if n in ref]
        R = np.array([ref[names[i]] for i in shared])
        P = X[shared][:, :2]
        Rm, Pm = R.mean(0), P.mean(0)
        U, _, Vt = np.linalg.svd((P - Pm).T @ (R - Rm))
        rot = U @ Vt
        X[:, :2] = (X[:, :2] - Pm) @ rot + Rm
        r = np.corrcoef(X[shared, 0], R[:, 0])[0, 1]
        print(f'orient: Front plane Procrustes-aligned to {ref_path} '
              f'(axis-1 corr after rotation: {r:.4f})')
    else:
        mbh = [i for i, n in enumerate(names)
               if n.startswith('mahabharata_') and 'appendix' not in n]
        if mbh and X[mbh, 0].mean() > 0:
            X[:, 0] *= -1
    return X


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dist_table')
    ap.add_argument('out_name')
    ap.add_argument('--title', default='3-D MDS')
    ap.add_argument('--subtitle', default='')
    ap.add_argument('--ref')
    ap.add_argument('--highlight', action='append', default=[])
    ap.add_argument('--note', default='')
    a = ap.parse_args()

    names, D = read_dist(a.dist_table)
    X, shares = mds3(D)
    X = orient(X, names, a.ref)
    strata = {r['text']: int(r['stratum'])
              for r in csv.DictReader(open(STRATA), delimiter='\t')}
    pts = [{'name': n, 'code': figcommon.code(n),
            'color': figcommon.PALETTE.get(strata.get(n, 0), '#999999'),
            'x': round(float(X[i, 0]), 4), 'y': round(float(X[i, 1]), 4),
            'z': round(float(X[i, 2]), 4)} for i, n in enumerate(names)]
    hl = {n: HL_COLORS[i % len(HL_COLORS)] for i, n in enumerate(a.highlight)}
    for n in hl:
        if n not in names:
            sys.exit(f'--highlight {n}: not in distance table')
    tether = a.highlight[:2] if len(a.highlight) == 2 else []
    if tether:
        i, j = names.index(tether[0]), names.index(tether[1])
        d3 = float(np.linalg.norm(X[i] - X[j]))
        d2 = float(np.linalg.norm(X[i, :2] - X[j, :2]))
        delta = float(D[i, j])
        tether_info = (f'{figcommon.code(tether[0])}–{figcommon.code(tether[1])}: '
                       f'3-D distance {d3:.3f} (2-D plane alone: {d2:.3f}; '
                       f'full Delta: {delta:.3f})')
    else:
        tether_info = ''
    subtitle = a.subtitle or (
        f'Axis shares: {shares[0]:.1%} · {shares[1]:.1%} · {shares[2]:.1%}. '
        'Drag to rotate; the Front button is the published 2-D plane.')

    tpl = (Path(__file__).parent / 'mds3d_template.html').read_text()
    html = (tpl.replace('__DATA__', json.dumps(pts, ensure_ascii=False))
               .replace('__TITLE__', a.title)
               .replace('__SUBTITLE__', subtitle)
               .replace('__HL__', json.dumps(hl, ensure_ascii=False))
               .replace('__TETHER__', json.dumps(tether))
               .replace('__TETHERINFO__', tether_info)
               .replace('__NOTE__', a.note)
               .replace('__LEGEND__', json.dumps(GROUPS_LEGEND)))
    OUTDIR.mkdir(exist_ok=True)
    out = OUTDIR / f'{a.out_name}.html'
    out.write_text(html)
    print(f'{out}  ({len(names)} units; shares '
          f'{" ".join(f"{s:.3f}" for s in shares)})')


if __name__ == '__main__':
    main()
