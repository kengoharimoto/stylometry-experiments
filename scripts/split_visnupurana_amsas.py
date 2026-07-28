#!/usr/bin/env python3
"""Split corpus/epic_puranas/visnupurana_u.txt into its six aṃśas.

The base file marks each verse with a trailing "// ViP_a,c.v //" ref, usually
on the second line of a two-line verse; speaker lines and blanks carry no ref.
Each line is therefore assigned to the aṃśa of the NEXT ref at or after it
(trailing lines after the last ref stay with aṃśa 6), so verse halves, speaker
tags and colophon lines travel with their verse. The whole-text unit stays in
the corpus (Vāyu/Mārkaṇḍeya precedent); outputs are visnupurana_amsa-N_u.txt.
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / 'corpus/epic_puranas'
lines = (BASE / 'visnupurana_u.txt').read_text(encoding='utf-8').splitlines()

REF = re.compile(r'ViP_(\d),')
nxt = [None] * len(lines)
cur = None
for i in range(len(lines) - 1, -1, -1):
    m = REF.search(lines[i])
    if m:
        cur = int(m.group(1))
    nxt[i] = cur
for i in range(len(lines)):        # trailing lines after the last ref
    if nxt[i] is None:
        nxt[i] = 6 if i > 0 else 1

for a in range(1, 7):
    out = BASE / f'visnupurana_amsa-{a}_u.txt'
    chunk = [l for l, x in zip(lines, nxt) if x == a]
    out.write_text('\n'.join(chunk) + '\n', encoding='utf-8')
    words = sum(len(l.split()) for l in chunk)
    print(f'{out.name}: {len(chunk)} lines, ~{words} words')
