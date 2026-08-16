#!/usr/bin/env python3
"""Does the two-letter romanization of single phonemes affect the C3 map?

IAST writes the ten aspirates (kh gh ch jh ṭh ḍh th dh ph bh) and the
diphthongs ai/au with two letters, so a character 3-gram spans 1.5-3
phonemes depending on content. hero_mds.py --phonemes maps each digraph to
a single SLP1-style symbol before counting (on top of --strip-spaces), so
a 3-gram spans exactly three phonemes. Coordinates are Procrustes-aligned
onto the same W1-delta reference as every other run.
"""
import csv
import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).parent
NS = HERE.parent / 'c3_nospace'
SW = HERE.parent / 'mfw_sweep'
ROOT = Path('/mnt/kengo/stylometry-experiments')
MFWS = [250, 500, 1000]


def load(p):
    with open(p, encoding='utf-8') as f:
        return {r['text']: (float(r['x']), float(r['y']))
                for r in csv.DictReader(f, delimiter='\t')}


w1500 = load(SW / 'coords_W1_mfw500.tsv')
names = sorted(w1500)


def col(d, i):
    return np.array([d[t][i] for t in names])


w5x = col(w1500, 0)
print('MFW   rho_x(phon,nospace)  rho_x(phon,W1-500)  rho_x(nospace,W1-500)')
for m in MFWS:
    ph = load(HERE / f'coords_phon_mfw{m}.tsv')
    ns = load(NS / f'coords_nospace_mfw{m}.tsv')
    a = spearmanr(col(ph, 0), col(ns, 0)).statistic
    b = spearmanr(col(ph, 0), w5x).statistic
    c = spearmanr(col(ns, 0), w5x).statistic
    print(f'{m:<5} {a:>18.4f} {b:>19.4f} {c:>21.4f}')

ph = load(HERE / 'coords_phon_mfw500.tsv')
ns = load(NS / 'coords_nospace_mfw500.tsv')
px, nx = col(ph, 0), col(ns, 0)


def pct(v, i):
    return round(100 * (v < v[i]).sum() / (len(v) - 1))


gap_ns = np.mean([abs(pct(nx, i) - pct(w5x, i)) for i in range(len(names))])
gap_ph = np.mean([abs(pct(px, i) - pct(w5x, i)) for i in range(len(names))])
print(f'\nmean |C3 - W1-500| pct gap: nospace {gap_ns:.1f} -> phoneme {gap_ph:.1f}')

rp = np.argsort(np.argsort(px))
rn = np.argsort(np.argsort(nx))
dr = rp - rn
print('\nbiggest x-rank movers, nospace -> phoneme (MFW 500):')
for i in np.argsort(-np.abs(dr))[:8]:
    print(f'  {names[i]:<46} pct {pct(nx, i)} -> {pct(px, i)}  (W1 {pct(w5x, i)})')

# how digraph-entangled is the adopted (no-space) top-500?
CORP = ROOT / 'corpus/epic_puranas_sandhied'
MAN = {l.strip().removesuffix('.txt') for l in
       (ROOT / 'manifests/dicsep2026_n127_ppl.txt').read_text().splitlines()
       if l.strip() and not l.startswith('#')}
raw = Counter()
for p in sorted(CORP.glob('*.txt')):
    if p.stem in MAN:
        t = re.sub(r'\s+', '', p.read_text(encoding='utf-8').lower())
        raw.update(t[i:i + 3] for i in range(len(t) - 2))
top = [g for g, _ in raw.most_common(500)]
digs = ['kh', 'gh', 'ch', 'jh', 'ṭh', 'ḍh', 'th', 'dh', 'ph', 'bh', 'ai', 'au']
n_full = sum(1 for g in top if any(d in g for d in digs))
print(f'\nno-space top-500: {n_full} contain a full digraph phoneme')
