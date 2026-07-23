#!/usr/bin/env python3
"""All-pairs shared-text scan over corpus/epic_puranas_sandhied.

Word-based overlap undercounts (fused/inconsistent word boundaries destroy
word n-grams — see E-texts/40_tools/scripts/rf_fullscan.py, which found ~400
shared half-ślokas where word-bigrams found 12), so this follows that script's
architecture: compare raw akṣara streams (spaces/punctuation stripped) with
rapidfuzz, prefiltered by shared character shingles.

Units are the sandhied corpus's half-śloka lines (cstream length ≥ 20). A pair
of units from different texts is a candidate when it shares ≥ 2 exact 8-char
shingles (shingles occurring in > 400 units are dropped as stock formulae /
speaker tags), and counts as shared when rapidfuzz ratio ≥ 80 on the streams.

Per text pair the headline number is line containment: the fraction of the
smaller text's units with a confirmed match in the other. Control-level noise
(unrelated texts) sits well under 1%; genuine borrowing runs 5–100%.

Writes materials/presentation_2026/reuse_pairs.tsv, sorted by containment.
"""
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from rapidfuzz import fuzz

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / 'corpus/epic_puranas_sandhied'
OUT = ROOT / 'materials/presentation_2026/reuse_pairs.tsv'

KEEP = set("abcdefghijklmnopqrstuvwxyzāīūṛṝḷḹṃḥśṣṇṭḍṅñ'")
SHINGLE = 8
DF_CAP = 400          # shingles in more units than this = formulaic, not borrowed
MIN_SHARED = 2        # candidate pairs must share this many rare shingles
MIN_CHARS = 20        # skip speaker tags, refs, header junk
RATIO = 80


def cstream(s):
    return ''.join(c for c in s.lower() if c in KEEP).replace("'", '')


# ── Load units ────────────────────────────────────────────────────────────────
texts, units, unit_text = [], [], []      # unit_text[i] = text id of unit i
for p in sorted(CORPUS.glob('*.txt')):
    tid = len(texts)
    texts.append(p.stem)
    seen = set()
    for line in p.read_text(encoding='utf-8').splitlines():
        cs = cstream(line)
        if len(cs) >= MIN_CHARS and cs not in seen:
            seen.add(cs)
            units.append(cs)
            unit_text.append(tid)
n_units_per = Counter(unit_text)
print(f'{len(texts)} texts, {len(units)} units')

# ── Shingle index with df cap ─────────────────────────────────────────────────
df = Counter()
for cs in units:
    df.update({cs[i:i + SHINGLE] for i in range(len(cs) - SHINGLE + 1)})
keep = {g for g, n in df.items() if n <= DF_CAP}
print(f'{len(df)} shingle types, {len(df) - len(keep)} capped as formulaic')

index = defaultdict(list)
for ui, cs in enumerate(units):
    for g in {cs[i:i + SHINGLE] for i in range(len(cs) - SHINGLE + 1)} & keep:
        index[g].append(ui)

# ── Candidates → rapidfuzz confirmation ──────────────────────────────────────
matched = defaultdict(set)                # (tid_a, tid_b) -> unit ids of a matched in b
checked = 0
for ui, cs in enumerate(units):
    ta = unit_text[ui]
    cand = Counter()
    for g in {cs[i:i + SHINGLE] for i in range(len(cs) - SHINGLE + 1)} & keep:
        for vj in index[g]:
            if unit_text[vj] != ta and vj > ui:
                cand[vj] += 1
    for vj, n in cand.items():
        if n < MIN_SHARED:
            continue
        checked += 1
        if fuzz.ratio(cs, units[vj]) >= RATIO:
            tb = unit_text[vj]
            matched[(ta, tb)].add(ui)
            matched[(tb, ta)].add(vj)
    if ui % 20000 == 0:
        print(f'  {ui}/{len(units)} units scanned, {checked} pairs scored')

# ── Per-pair containment ──────────────────────────────────────────────────────
rows = []
for a, b in combinations(range(len(texts)), 2):
    na, nb = len(matched.get((a, b), ())), len(matched.get((b, a), ()))
    if not na and not nb:
        continue
    ua, ub = n_units_per[a], n_units_per[b]
    # containment = the smaller text's own matched share (max() would overshoot
    # past 100% when the larger text matches one unit many times)
    rows.append((texts[a], texts[b], (na if ua <= ub else nb) / min(ua, ub),
                 na, nb, ua, ub))
rows.sort(key=lambda r: -r[2])

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('a\tb\tcontainment\tmatched_a\tmatched_b\tunits_a\tunits_b\n')
    for r in rows:
        f.write(f'{r[0]}\t{r[1]}\t{r[2]:.5f}\t{r[3]}\t{r[4]}\t{r[5]}\t{r[6]}\n')
print(f'wrote {OUT} ({len(rows)} nonzero pairs)')

print(f"\n{'pair':72} containment  matched lines")
for a, b, c, na, nb, ua, ub in rows[:45]:
    print(f'{a} ↔ {b:38}  {c:6.1%}   {max(na, nb)}')
