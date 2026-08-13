#!/usr/bin/env python3
"""Build corpus/epic_puranas_sandhied_noreuse/: the sandhied corpus with
cross-text reused lines removed.

Matching is identical to corpus_reuse_scan.py (this is that scan re-emitting
per-line verdicts instead of pair aggregates): units are half-śloka lines as
akṣara streams, candidate pairs share >= 2 rare 8-char shingles (shingles in
> 400 units are formulaic and exempt -- stock phrasing is style, not
borrowing), confirmed at rapidfuzz ratio >= 80.

A confirmed cross-family match drops the line from BOTH texts (the experiment
asks what remains when shared text is gone, so neither copy survives).
EXCEPTION: the kirfel family (Purāṇapañcalakṣaṇa) is treated as the reuse
SOURCE under Kirfel's hypothesis that the purāṇas incorporated the PPL --
a kirfel<->purāṇa match drops only the purāṇa line, so the constituted PPL
survives intact while the purāṇas are rendered "without the PPL". Texts
of the same work family (shared filename prefix before the first "_") are
exempt: the corpus holds containers next to their own subdivisions
(markandeyapurana + its three parts, visnupurana + six aṃśas, ...), and that
overlap is unit structure, not reuse. Note vayu_ba is its own family and is
by construction shared Vāyu/Bḍ text -- expect it to shrink to almost nothing.

Writes the retention table to stdout; lines whose stream is < 20 chars (refs,
tags) are kept as-is (the scanner never saw them).

Usage: python3 scripts/build_noreuse_corpus.py
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

from rapidfuzz import fuzz

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'corpus/epic_puranas_sandhied'
OUT = ROOT / 'corpus/epic_puranas_sandhied_noreuse'
# Source-level counterpart: the same drop decisions applied to the raw
# corpus/epic_puranas lines (matched via the sandhied cleaning), so the byt5
# unsandhi pass can regenerate a word-split corpus for W1 runs.
SRC = ROOT / 'corpus/epic_puranas'
SRC_OUT = ROOT / 'corpus/epic_puranas_noreuse'

sys.path.insert(0, str(ROOT / 'scripts'))
from build_epic_puranas_sandhied import clean_line          # noqa: E402
from process_epic_puranas_unsandhied_local import skip_test_for  # noqa: E402

KEEP = set("abcdefghijklmnopqrstuvwxyzāīūṛṝḷḹṃḥśṣṇṭḍṅñ'")
SHINGLE = 8
DF_CAP = 400
MIN_SHARED = 2
MIN_CHARS = 20
# Calibrated 2026-07-29: control pairs with no genuine reuse (Rām5/BhP11,
# MBh8/Liṅga2, DevīBhP/Rām2) max out at 63-67, so 70 removes recension-variant
# parallels (śvetapiṅgalam/kṛṣṇalohitam-type) with zero measured false
# positives. The scan's original 80 was calibrated for conservative pair
# counting, not exhaustive removal, and left such variants in place.
RATIO = 70
# One-directional family: matches trigger removal from the counterpart text,
# but this family's own lines are never dropped (see docstring).
SOURCE_FAM = 'kirfel'


def cstream(s):
    return ''.join(c for c in s.lower() if c in KEEP).replace("'", '')


def family(name):
    return name.split('_', 1)[0]


# ── Load units (deduped per text, as in the scan) ────────────────────────────
texts, units, unit_text = [], [], []
stream_of = []                    # per text: {cstream} of its scanned units
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
    stream_of.append(seen)
fam = [family(t) for t in texts]
print(f'{len(texts)} texts, {len(units)} units')

# ── Shingle index with df cap ────────────────────────────────────────────────
df = Counter()
for cs in units:
    df.update({cs[i:i + SHINGLE] for i in range(len(cs) - SHINGLE + 1)})
keep = {g for g, n in df.items() if n <= DF_CAP}
print(f'{len(df)} shingle types, {len(df) - len(keep)} capped as formulaic')

index = defaultdict(list)
for ui, cs in enumerate(units):
    for g in {cs[i:i + SHINGLE] for i in range(len(cs) - SHINGLE + 1)} & keep:
        index[g].append(ui)

# ── Cross-family matches -> dropped streams per text ─────────────────────────
drop = defaultdict(set)           # tid -> {cstream to drop}
checked = 0
for ui, cs in enumerate(units):
    ta = unit_text[ui]
    cand = Counter()
    for g in {cs[i:i + SHINGLE] for i in range(len(cs) - SHINGLE + 1)} & keep:
        for vj in index[g]:
            if vj > ui and fam[unit_text[vj]] != fam[ta]:
                cand[vj] += 1
    for vj, n in cand.items():
        if n < MIN_SHARED:
            continue
        checked += 1
        if fuzz.ratio(cs, units[vj]) >= RATIO:
            if fam[ta] != SOURCE_FAM:
                drop[ta].add(cs)
            if fam[unit_text[vj]] != SOURCE_FAM:
                drop[unit_text[vj]].add(units[vj])
    if ui % 20000 == 0:
        print(f'  {ui}/{len(units)} units scanned, {checked} pairs scored', flush=True)

# ── Write the noreuse corpus ─────────────────────────────────────────────────
OUT.mkdir(exist_ok=True)
print(f"\n{'text':55} {'lines':>7} {'dropped':>8} {'kept words':>10} {'retention':>9}")
for tid, name in enumerate(texts):
    src = (CORPUS / f'{name}.txt').read_text(encoding='utf-8').splitlines()
    dropped = drop.get(tid, set())
    kept = [l for l in src if cstream(l) not in dropped]
    (OUT / f'{name}.txt').write_text('\n'.join(kept) + ('\n' if kept else ''),
                                     encoding='utf-8')
    w_src = sum(len(l.split()) for l in src)
    w_kept = sum(len(l.split()) for l in kept)
    print(f'{name:55} {len(src):>7} {len(src) - len(kept):>8} {w_kept:>10} '
          f'{w_kept / w_src if w_src else 0:>9.1%}')

# ── Source-level noreuse (input for the byt5 unsandhi pass) ──────────────────
SRC_OUT.mkdir(exist_ok=True)
for tid, name in enumerate(texts):
    src_path = SRC / f'{name}.txt'
    if not src_path.exists():
        print(f'  (no source file for {name}, skipped)')
        continue
    dropped = drop.get(tid, set())
    skip = skip_test_for(src_path.name)
    kept = []
    for l in src_path.read_text(encoding='utf-8').splitlines():
        c = clean_line(l, skip)
        if c is not None and cstream(c) in dropped:
            continue                      # the reused line, at source level
        kept.append(l)
    (SRC_OUT / f'{name}.txt').write_text('\n'.join(kept) + ('\n' if kept else ''),
                                         encoding='utf-8')
print(f'source-level noreuse written to {SRC_OUT}')
