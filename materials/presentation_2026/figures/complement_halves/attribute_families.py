#!/usr/bin/env python3
"""Attribute each dropped line of the 20 target units to the counterpart
families it matched, using exactly the matching of build_noreuse_corpus.py
(cstream units deduped per text, 8-char shingles, df cap 400, >=2 shared rare
shingles, rapidfuzz ratio >= 70, cross-family only).

Output: for every target unit, a partition of its shared (dropped) lines into
  ppl     -- matched a kirfel unit (PPL-parallel), possibly others too
  vayubd  -- matched inside the Vayu/Brahmanda complex (vayupurana,
             brahmandapurana, vayu_ba families), no kirfel match
  other   -- matched only other families
Writes corpus/complements_sandhied/<unit>_shared_{ppl,vayubd,other}.txt and a
per-line family map (attribution.tsv). Validates that the union of matched
lines equals the complement file.
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

from rapidfuzz import fuzz

ROOT = Path('/mnt/kengo/stylometry-experiments')
CORPUS = ROOT / 'corpus/epic_puranas_sandhied'
COMP = ROOT / 'corpus/complements_sandhied'
HERE = Path(__file__).parent

KEEP = set("abcdefghijklmnopqrstuvwxyzāīūṛṝḷḹṃḥśṣṇṭḍṅñ'")
SHINGLE = 8
DF_CAP = 400
MIN_SHARED = 2
MIN_CHARS = 20
RATIO = 70
CORE_FAMS = {'vayupurana', 'brahmandapurana', 'vayu'}   # vayu = vayu_ba

TARGETS = ([f'vayupurana_{s}_iast' for s in
            ['01_frame-and-cosmogony', '02_pashupata-yoga', '03_kalpas-and-shiva-lineages',
             '04_bhuvana-vinyasa', '05_jyotis-and-purvardha-close',
             '06_prthu-and-prajapati-lineages', '07_shraddha-kalpa',
             '08_manu-candra-vishnu-vamsha', '09_upasamhara', '10_gaya-mahatmya']]
           + ['vayupurana_revakhanda']
           + [f'brahmandapurana_khanda-{k}_u' for k in '123']
           + [f'visnupurana_amsa-{a}_u' for a in '123456'])

def cstream(s):
    return ''.join(c for c in s.lower() if c in KEEP).replace("'", '')

def family(name):
    return name.split('_', 1)[0]

texts, units, unit_text = [], [], []
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
fam = [family(t) for t in texts]
tid_of = {t: i for i, t in enumerate(texts)}
target_tids = {tid_of[t] for t in TARGETS}
print(f'{len(texts)} texts, {len(units)} units', flush=True)

df = Counter()
for cs in units:
    df.update({cs[i:i + SHINGLE] for i in range(len(cs) - SHINGLE + 1)})
keep = {g for g, n in df.items() if n <= DF_CAP}
print(f'{len(df)} shingle types, {len(df) - len(keep)} capped', flush=True)

index = defaultdict(list)
for ui, cs in enumerate(units):
    for g in {cs[i:i + SHINGLE] for i in range(len(cs) - SHINGLE + 1)} & keep:
        index[g].append(ui)

# for target-unit lines only: which counterpart families match?
matched = defaultdict(set)          # (tid, cstream) -> {counterpart family}
checked = 0
tlines = [ui for ui in range(len(units)) if unit_text[ui] in target_tids]
for k, ui in enumerate(tlines):
    cs = units[ui]
    ta = unit_text[ui]
    cand = Counter()
    for g in {cs[i:i + SHINGLE] for i in range(len(cs) - SHINGLE + 1)} & keep:
        for vj in index[g]:
            if vj != ui and fam[unit_text[vj]] != fam[ta]:
                cand[vj] += 1
    for vj, n in cand.items():
        if n < MIN_SHARED:
            continue
        checked += 1
        if fuzz.ratio(cs, units[vj]) >= RATIO:
            matched[(ta, cs)].add(fam[unit_text[vj]])
    if k % 5000 == 0:
        print(f'  {k}/{len(tlines)} target lines, {checked} pairs scored', flush=True)

# partition + validate against the complement files
print(f'\n{"unit":<48}{"ppl":>8}{"vayubd":>8}{"other":>8}{"miss":>6}  (words)')
with open(HERE / 'attribution.tsv', 'w', encoding='utf-8') as af:
    af.write('unit\tclass\tfamilies\tline\n')
    for t in TARGETS:
        tid = tid_of[t]
        comp_lines = (COMP / f'{t}_shared.txt').read_text(encoding='utf-8').splitlines()
        buckets = {'ppl': [], 'vayubd': [], 'other': []}
        miss = 0
        for l in comp_lines:
            fams = matched.get((tid, cstream(l)), set())
            if not fams:
                miss += 1
                continue
            if 'kirfel' in fams:
                b = 'ppl'
            elif fams & CORE_FAMS:
                b = 'vayubd'
            else:
                b = 'other'
            buckets[b].append(l)
            af.write(f'{t}\t{b}\t{",".join(sorted(fams))}\t{l}\n')
        for b, lines in buckets.items():
            (COMP / f'{t}_shared_{b}.txt').write_text(
                '\n'.join(lines) + ('\n' if lines else ''), encoding='utf-8')
        w = {b: sum(len(l.split()) for l in ls) for b, ls in buckets.items()}
        print(f'{t:<48}{w["ppl"]:>8}{w["vayubd"]:>8}{w["other"]:>8}{miss:>6}')
print('\nwrote subsets to', COMP, 'and attribution.tsv')
