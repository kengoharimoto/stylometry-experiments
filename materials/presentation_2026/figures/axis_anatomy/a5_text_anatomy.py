#!/usr/bin/env python3
"""A5 (axis-anatomy plan): per-text anatomy of the article's featured texts.

For each featured text, decompose its pull along the drift axis into
per-feature contributions: contribution_f = z_f * rho_f, where z_f is
the text's corpus z-score on feature f and rho_f the feature's axis
loading (A1's Spearman rho vs the committed article-frame axis-1
coordinates). The loading-weighted z-score sum is a transparent linear
proxy for axis position (its rank agreement with the real axis is
printed as a sanity line); the top contributions say in checkable words
why *this* text sits *there*.

Featured texts (per the plan note): the merged MBh 15-18 closing block,
PPL Textgruppe I and the ungrouped core, the old Skandapurana, the
Bhagavata (the 12 skandha units merged; the skandha-10 with-commentary
unit is excluded as contaminated by commentary), and the Sivadharma
pair. Corpus-unit texts use their manifest counts; the two merged
blocks are count sums z-scored against the same corpus statistics.

Usage: a5_text_anatomy.py w|c   ->  a5_text_anatomy_{W1,C3}.tsv

2026-08-29, run for the Indological companion (Kengo's call): the DH
draft does not cite this. With-reuse build: the anatomy describes the
language a text *carries* (its transmitted mixture), which is the right
object for worked examples a reader checks against the printed page.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
FEAT = sys.argv[1] if len(sys.argv) > 1 else 'w'
W1 = FEAT == 'w'
MFW = 500
TOPN = 20

BASE_CORPUS = ROOT / ('corpus/epic_puranas_unsandhied' if W1 else 'corpus/epic_puranas_sandhied')
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
COORDS = ROOT / ('materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
                 if W1 else 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv')

FEATURED_UNITS = ['kirfel_ppl_textgruppe_I_col1', 'kirfel_ppl_ungrouped_col1',
                  'skandapurana', 'sivadharmasastra', 'sivadharmottara']
MERGED = {
    'mbh_15-18_block': ['mahabharata_15-asramavasikaparvan',
                        'mahabharata_16-mausalaparvan',
                        'mahabharata_17-mahaprasthanikaparvan',
                        'mahabharata_18-svargarohanaparvan'],
    'bhagavata_merged_12sk': [f'bhagavatapurana_skandha-{i:02d}_u'
                              for i in range(1, 13)],
}


def word_counts(path):
    return Counter(path.read_text(encoding='utf-8').lower().split())


def trigram_counts(path):
    txt = re.sub(r'\s+', '', path.read_text(encoding='utf-8').lower())
    return Counter(txt[i:i + 3] for i in range(len(txt) - 2))


count_fn = word_counts if W1 else trigram_counts

manifest = {l.strip().removesuffix('.txt') for l in
            MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}
names, counts = [], []
for p in sorted(BASE_CORPUS.glob('*.txt')):
    if p.stem in manifest:
        names.append(p.stem)
        counts.append(count_fn(p))
assert len(names) == len(manifest)

raw = Counter()
for c in counts:
    raw.update(c)
feats = [w for w, _ in raw.most_common(MFW)]
totals = [sum(c.values()) for c in counts]
X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])
mu, sd = X.mean(0), X.std(0)

coords = {}
with open(COORDS, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        coords[row['text']] = float(row['x'])
x = np.array([coords[n] for n in names])
pct = {n: p for n, p in
       zip(names, np.argsort(np.argsort(x)) / (len(names) - 1) * 100)}

rho = np.array([spearmanr(X[:, j], x).statistic for j in range(MFW)])

# sanity: the loading-weighted z-score sum vs the real axis
Z = (X - mu) / sd
proxy = (Z * rho).mean(1)
print(f'[{ "W1" if W1 else "C3" }] sanity: rho(loading-weighted z sum, axis 1) '
      f'= {spearmanr(proxy, x).statistic:.4f} over {len(names)} units')

targets = {}
for n in FEATURED_UNITS:
    targets[n] = X[names.index(n)]
for label, members in MERGED.items():
    agg = Counter()
    for m in members:
        agg.update(counts[names.index(m)])
    tot = sum(agg.values())
    targets[label] = np.array([agg.get(w, 0) / tot for w in feats])

out = HERE / f'a5_text_anatomy_{"W1" if W1 else "C3"}.tsv'
with open(out, 'w', encoding='utf-8') as fh:
    fh.write('text\tfeature\tz\trho_x\tcontribution\trate_permille\tcorpus_permille\n')
    for label, rates in targets.items():
        z = (rates - mu) / sd
        contrib = z * rho
        where = (f'map pct {pct[label]:.0f}' if label in pct else
                 'merged block (supplementary)')
        print(f'\n=== {label} ({where}) ===')
        order = np.argsort(contrib)
        print(f'strongest EARLY-ward contributions (feature: z, rho, text vs corpus per-mille):')
        for j in order[:TOPN]:
            print(f'  {feats[j]!r:<14} z {z[j]:+6.2f}  rho {rho[j]:+.2f}  '
                  f'{1000 * rates[j]:8.2f} vs {1000 * mu[j]:6.2f}')
        print(f'strongest LATE-ward contributions:')
        for j in order[-TOPN:][::-1]:
            print(f'  {feats[j]!r:<14} z {z[j]:+6.2f}  rho {rho[j]:+.2f}  '
                  f'{1000 * rates[j]:8.2f} vs {1000 * mu[j]:6.2f}')
        for j in np.argsort(-np.abs(contrib)):
            fh.write(f'{label}\t{feats[j]}\t{z[j]:.3f}\t{rho[j]:.3f}\t'
                     f'{contrib[j]:.3f}\t{1000 * rates[j]:.3f}\t'
                     f'{1000 * mu[j]:.3f}\n')
print(f'\nwrote {out.name} ({len(targets)} texts x {MFW} features)')
