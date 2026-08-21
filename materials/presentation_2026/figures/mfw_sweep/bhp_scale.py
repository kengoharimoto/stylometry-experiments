#!/usr/bin/env python3
"""BhP scale-dependence across feature-set sizes, both builds (draft §8 iii).

The with-reuse diagnostic (2026-08-14 three-debates note): the BhP's mean
W1 drift percentile is scale-dependent (19 @30 MFW, 52 @80, 50 @500,
26 @5000) while genuinely early texts stay early at every scale. This
script makes that measurement citable and re-runs it on the no-reuse
build, on both lenses, with a length diagnostic per setting: the W1
no-reuse axis is partly a length artifact at 500 MFW (R1), so W1-noreuse
percentiles are read as a cross-scale *pattern* with rho_logT printed
beside each setting, never as citable positions (claims map §0 gate).

Pipeline replicates hero_mds: relative rates, corpus z-score, Burrows's
Delta, classical MDS axis 1; axis oriented per setting against the
article reference coordinates (early pole low).

Outputs: bhp_scale_settings.tsv (one row per build x lens x setting:
group mean percentiles, rho vs reference, rho_logT) and
bhp_scale_ranges.tsv (per text: percentile range across settings —
tests "scale-dependent in a way no other text shows").

Usage: bhp_scale.py [with|noreuse|both]
"""
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent

BUILDS = {
    'with': ('manifests/dicsep2026_n127_ppl.txt',
             'corpus/epic_puranas_unsandhied',
             'corpus/epic_puranas_sandhied'),
    'noreuse': ('manifests/noreuse2026_n126.txt',
                'corpus/epic_puranas_unsandhied_noreuse',
                'corpus/epic_puranas_sandhied_noreuse'),
}
SETTINGS = {'W1': [30, 80, 500, 1500, 5000],
            'C3': [250, 500, 2000, 5000, 12000]}
REF = {('with', 'W1'): 'materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv',
       ('with', 'C3'): 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv',
       ('noreuse', 'W1'): 'materials/presentation_2026/figures/mds3d/coords_W1-500_noreuse_n126.tsv',
       ('noreuse', 'C3'): 'materials/presentation_2026/figures/mds3d/coords_C3-500ns_noreuse_n126.tsv'}

GROUPS = {
    'BhP': lambda n: n.startswith('bhagavatapurana'),
    'MBh': lambda n: n.startswith('mahabharata_') and 'appendix' not in n,
    'Ram': lambda n: n.startswith('ramayana'),
}

which = sys.argv[1] if len(sys.argv) > 1 else 'both'
builds = list(BUILDS) if which == 'both' else [which]


def top2(X):
    Z = (X - X.mean(0)) / np.maximum(X.std(0), 1e-12)
    D = squareform(pdist(Z, 'cityblock') / Z.shape[1])
    n = len(D)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    vals, vecs = np.linalg.eigh(B)
    idx = np.argsort(vals)[::-1][:2]
    return [vecs[:, i] * np.sqrt(max(vals[i], 0.0)) for i in idx]


rows, range_rows = [], []
for build in builds:
    man_p, w_dir, c_dir = BUILDS[build]
    manifest = {l.strip().removesuffix('.txt') for l in
                (ROOT / man_p).read_text(encoding='utf-8').splitlines()
                if l.strip() and not l.startswith('#')}
    for lens in ('W1', 'C3'):
        corpus = ROOT / (w_dir if lens == 'W1' else c_dir)
        names, counts, totals = [], [], []
        for p in sorted(corpus.glob('*.txt')):
            if p.stem not in manifest:
                continue
            if lens == 'W1':
                toks = p.read_text(encoding='utf-8').lower().split()
                c = Counter(toks)
                tot = len(toks)
            else:
                s = re.sub(r'\s+', '', p.read_text(encoding='utf-8').lower())
                c = Counter(s[i:i + 3] for i in range(len(s) - 2))
                tot = max(sum(c.values()), 1)
            names.append(p.stem)
            counts.append(c)
            totals.append(tot)
        raw = Counter()
        for c in counts:
            raw.update(c)
        ranked = [w for w, _ in raw.most_common(max(SETTINGS[lens]))]
        # log unit length in WORDS on both lenses (the R1 diagnostic)
        wdirp = ROOT / w_dir
        logT = np.array([np.log(len((wdirp / f'{n}.txt')
                        .read_text(encoding='utf-8').split()))
                         for n in names])
        ref = {}
        for l in (ROOT / REF[(build, lens)]).read_text(encoding='utf-8').splitlines()[1:]:
            f = l.split('\t')
            ref[f[0]] = float(f[1])
        refx = np.array([ref[n] for n in names])
        masks = {g: np.array([pred(n) for n in names])
                 for g, pred in GROUPS.items()}
        pcts, valid = {}, {}
        for mfw in SETTINGS[lens]:
            feats = ranked[:mfw]
            X = np.array([[c.get(w, 0) / t for w in feats]
                          for c, t in zip(counts, totals)])
            # near-degenerate top eigenvalues (esp. C3) mean the drift
            # axis may surface second; pick the top-2 axis that matches
            # the reference (the plane is stable, its ordering is not)
            cands = top2(X)
            rs = [spearmanr(a, refx).statistic for a in cands]
            k = int(np.argmax([abs(r) for r in rs]))
            ax = cands[k] if rs[k] >= 0 else -cands[k]
            r_ref = abs(rs[k])
            r_len = spearmanr(ax, logT).statistic
            pct = np.argsort(np.argsort(ax)) / (len(names) - 1) * 100
            pcts[mfw] = pct
            valid[mfw] = r_ref >= 0.9
            row = {'build': build, 'lens': lens, 'mfw': mfw, 'axis': k + 1,
                   'rho_ref': r_ref, 'rho_logT': r_len}
            for g, m in masks.items():
                row[f'{g}_mean_pct'] = pct[m].mean()
            rows.append(row)
            print(f'{build:8}{lens} mfw {mfw:>6} (axis {k + 1}): '
                  + '  '.join(f'{g} {pct[m].mean():5.1f}' for g, m in masks.items())
                  + f'   rho_ref {r_ref:.3f}  rho_logT {r_len:+.3f}'
                  + ('' if valid[mfw] else '   [axis no longer the drift axis]'))
        vset = [m for m in SETTINGS[lens] if valid[m]]
        P = np.column_stack([pcts[m] for m in vset])
        rng = P.max(1) - P.min(1)
        for n, r in zip(names, rng):
            range_rows.append({'build': build, 'lens': lens, 'text': n,
                               'pct_range': r})
        order = np.argsort(-rng)
        bhp_rng = rng[masks['BhP']]
        print(f'  cross-scale pct range over VALID settings (rho_ref>=0.9: '
              f'{vset}): BhP mean {bhp_rng.mean():.1f} '
              f'(units {bhp_rng.min():.0f}-{bhp_rng.max():.0f}); '
              f'corpus median {np.median(rng):.1f}; BhP mean is worse than '
              f'{100 * (rng[~masks["BhP"]] < bhp_rng.mean()).mean():.0f}% of other units')
        print('  top-6 ranges: ' + '; '.join(
            f'{names[i]} {rng[i]:.0f}' for i in order[:6]))

with open(HERE / 'bhp_scale_settings.tsv', 'w', encoding='utf-8') as f:
    ks = ['build', 'lens', 'mfw', 'axis', 'BhP_mean_pct', 'MBh_mean_pct',
          'Ram_mean_pct', 'rho_ref', 'rho_logT']
    f.write('\t'.join(ks) + '\n')
    for r in rows:
        f.write('\t'.join(f'{r[k]:.4f}' if isinstance(r[k], float)
                          else str(r[k]) for k in ks) + '\n')
with open(HERE / 'bhp_scale_ranges.tsv', 'w', encoding='utf-8') as f:
    f.write('build\tlens\ttext\tpct_range\n')
    for r in range_rows:
        f.write(f"{r['build']}\t{r['lens']}\t{r['text']}\t{r['pct_range']:.2f}\n")
print('wrote bhp_scale_settings.tsv, bhp_scale_ranges.tsv')
