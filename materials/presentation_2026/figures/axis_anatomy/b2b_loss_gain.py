#!/usr/bin/env python3
"""B2b (axis-anatomy plan): Kengo's loss/gain (Dollo-style) decomposition.

Hypothesis: drift = random disappearance of original features (which do
not re-emerge) + random emergence of new ones; chronology is effectively
the fraction of the original inventory lost, and emergences can be
ignored for dating ("losses are the clock; gains are the community
structure"). Named relatives: Dollo's law / stochastic Dollo (Nicholls &
Gray 2008), Swadesh's glottochronology — applied to style features.

Design (split-half, non-circular): each unit's token stream is split into
alternating 16-token blocks (half A / half B). The ORIGINAL feature set is
defined on half A only, as features overrepresented in the epic strata
(externally given: strata 1–2), and the LATE set as features
overrepresented in the late sectarian block (stratum 5). Scores are then
computed on half B only:
  retention_i = rate mass on the original set  (loss = its depletion)
  gain_i      = rate mass on the late set
Predictions: (i) loss alone reproduces the axis (rho >= ~0.9);
(ii) gain orders the late texts only loosely.

Usage: b2b_loss_gain.py [w|c] [--noreuse]

2026-08-19 (reframe): 'c' runs the identical design on no-space C3 —
the stream is whitespace-stripped and split into alternating 128-char
blocks (~16 words), trigrams counted within blocks; --noreuse runs on
the stripped corpus/manifest against the composed-chronology coords.
w + --noreuse is refused (R1: the no-reuse W1 axis is partly a length
artifact; see notes/2026-08-19_noreuse_precedence_reframe.md).
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
MFW = 500
NOREUSE = '--noreuse' in sys.argv
argv = [a for a in sys.argv if a != '--noreuse']
FEAT = argv[1] if len(argv) > 1 else 'w'
# rate-ratio threshold for the early/late sets: 1.5 (the W1 default) is
# degenerate on C3 — trigram rate ratios are much flatter than word rate
# ratios (at 1.5 the late set is a single trigram) — so C3 runs must
# report a sweep, not one tuned value
THRESH = float(argv[2]) if len(argv) > 2 else 1.5
W1 = FEAT == 'w'
if W1 and NOREUSE:
    sys.exit('w + --noreuse refused: the no-reuse W1 axis is partly a '
             'length artifact (R1) — run c --noreuse instead')
if W1:
    CORPUS = ROOT / 'corpus/epic_puranas_unsandhied'
    MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
    COORDS = ROOT / 'materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
elif not NOREUSE:
    CORPUS = ROOT / 'corpus/epic_puranas_sandhied'
    MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
    COORDS = ROOT / 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv'
else:
    CORPUS = ROOT / 'corpus/epic_puranas_sandhied_noreuse'
    MANIFEST = ROOT / 'manifests/noreuse2026_n126.txt'
    COORDS = ROOT / 'materials/presentation_2026/figures/mds3d/coords_C3-500ns_noreuse_n126.tsv'
STRATA = ROOT / 'materials/presentation_2026/chronology_strata.tsv'
TAG = ('W1' if W1 else 'C3') + ('_noreuse' if NOREUSE else '') + '_500'

manifest = {l.strip().removesuffix('.txt') for l in
            MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}
strata = {}
with open(STRATA, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        strata[row['text']] = int(row['stratum'])
coords = {}
with open(COORDS, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        coords[row['text']] = float(row['x'])

names, cA, cB = [], [], []
for p in sorted(CORPUS.glob('*.txt')):
    if p.stem not in manifest:
        continue
    a, b = Counter(), Counter()
    if W1:
        toks = p.read_text(encoding='utf-8').lower().split()
        blocks = [toks[i:i + 16] for i in range(0, len(toks), 16)]
        for k, blk in enumerate(blocks):
            (a if k % 2 == 0 else b).update(blk)
    else:
        # article C3 convention: scriptio continua; alternating 128-char
        # blocks (~16 words); trigrams counted within blocks (junction
        # trigrams across block cuts are dropped, same on both halves)
        s = re.sub(r'\s+', '', p.read_text(encoding='utf-8').lower())
        for k in range(0, len(s), 128):
            blk = s[k:k + 128]
            tgt = a if (k // 128) % 2 == 0 else b
            tgt.update(blk[i:i + 3] for i in range(len(blk) - 2))
    names.append(p.stem)
    cA.append(a)
    cB.append(b)

raw = Counter()
for c in cA:
    raw.update(c)
feats = [w for w, _ in raw.most_common(MFW)]     # top-500 defined on half A
TA = np.array([sum(c.values()) for c in cA])
TB = np.array([sum(c.values()) for c in cB])
XA = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(cA, TA)])
XB = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(cB, TB)])

epic = np.array([strata[n] in (1, 2) for n in names])
late = np.array([strata[n] == 5 for n in names])
x = np.array([coords[n] for n in names])

mean_all = XA.mean(0)
idx_orig = np.where((XA[epic].mean(0) / np.maximum(mean_all, 1e-12)) >= THRESH)[0]
idx_late = np.where((XA[late].mean(0) / np.maximum(mean_all, 1e-12)) >= THRESH)[0]
overlap = set(idx_orig) & set(idx_late)
idx_orig = np.array(sorted(set(idx_orig) - overlap))
idx_late = np.array(sorted(set(idx_late) - overlap))
print(f'original set (epic-typical, half A, ratio>={THRESH}): {len(idx_orig)} features')
print(f'late set (late-block-typical): {len(idx_late)} features; overlap dropped: {len(overlap)}')
print('original sample:', ' '.join(feats[j] for j in idx_orig[:15]))
print('late sample:    ', ' '.join(feats[j] for j in idx_late[:15]))

retention = XB[:, idx_orig].sum(1)     # half-B rate mass on original set
gain = XB[:, idx_late].sum(1)
loss_order = -retention                # depleted = later

r_loss = spearmanr(loss_order, x).statistic
r_gain = spearmanr(gain, x).statistic
r_comb = spearmanr(gain - retention, x).statistic
print(f'\nrho(axis, loss alone)  = {r_loss:.4f}')
print(f'rho(axis, gain alone)  = {r_gain:.4f}')
print(f'rho(axis, gain - retention) = {r_comb:.4f}')

# prediction (ii): within-group resolution
for label, mask in [('non-late (strata != 5)', ~late), ('late block only', late),
                    ('non-epic (strata not 1-2)', ~epic)]:
    rl = spearmanr(loss_order[mask], x[mask]).statistic
    rg = spearmanr(gain[mask], x[mask]).statistic
    print(f'  within {label:<26} loss {rl:>7.3f}   gain {rg:>7.3f}   (n={mask.sum()})')

# presence/absence complication: do original features disappear or dwindle?
pres_A = (XA[:, idx_orig] > 0)
pres_B = (XB[:, idx_orig] > 0)
frac_present = pres_B.mean(1)
r_pres = spearmanr(-frac_present, x).statistic
print(f'\npresence/absence variant (fraction of original set attested in half B):')
print(f'  rho(axis, presence-loss) = {r_pres:.4f}')

with open(HERE / f'b2b_loss_gain_{TAG}.tsv', 'w', encoding='utf-8') as f:
    f.write('text\tstratum\tx\tretention\tgain\tfrac_orig_present\n')
    for i, n in enumerate(names):
        f.write(f'{n}\t{strata[n]}\t{x[i]:.6f}\t{retention[i]:.6f}\t'
                f'{gain[i]:.6f}\t{frac_present[i]:.4f}\n')
print(f'wrote b2b_loss_gain_{TAG}.tsv')
