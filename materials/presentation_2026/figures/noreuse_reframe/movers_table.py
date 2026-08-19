#!/usr/bin/env python3
"""Join the per-unit CI tables into the movers table of the reframe note:
with-reuse vs no-reuse axis-1 percentile per unit, CI-grade, per lens.

A move counts as CI-separated when the two intervals do not overlap.
Sub-3k residues (W1 words in the noreuse corpus) are flagged.

Usage: movers_table.py w|c
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, '/mnt/kengo/stylometry-experiments/scripts/presentation')
import figcommon  # noqa: E402

HERE = Path(__file__).parent
ROOT = Path('/mnt/kengo/stylometry-experiments')
FEAT = sys.argv[1] if len(sys.argv) > 1 else 'w'
tag = 'W1' if FEAT == 'w' else 'C3'


def load(build):
    with open(HERE / f'unit_ci_{tag}_{build}.tsv', encoding='utf-8') as f:
        return {r['unit']: (float(r['est']), float(r['lo']), float(r['hi']))
                for r in csv.DictReader(f, delimiter='\t')}


A, B = load('withreuse'), load('noreuse')
res_dir = ROOT / 'corpus/epic_puranas_unsandhied_noreuse'
rows = []
for u in sorted(set(A) & set(B)):
    ea, la, ha = A[u]
    eb, lb, hb = B[u]
    resw = len((res_dir / f'{u}.txt').read_text(encoding='utf-8').split())
    sep = hb < la or ha < lb
    rows.append((u, figcommon.code(u), ea, la, ha, eb, lb, hb,
                 eb - ea, resw, sep))

rows.sort(key=lambda r: r[8])
out = HERE / f'movers_{tag}.tsv'
with open(out, 'w', encoding='utf-8') as f:
    f.write('unit\tcode\twith_est\twith_lo\twith_hi\tnoreuse_est\t'
            'noreuse_lo\tnoreuse_hi\tshift\tresidue_words\tci_separated\n')
    for r in rows:
        f.write('\t'.join(str(x) for x in r) + '\n')

print(f'{tag}: {len(rows)} units; CI-separated moves: '
      f'{sum(1 for r in rows if r[10])}')
print(f'{"code":<6}{"with":>16}{"noreuse":>18}{"shift":>7}{"resid":>9}  sep')
for r in rows:
    if r[10] or abs(r[8]) >= 10:
        flag = '*' if r[9] < 3000 else ' '
        print(f'{r[1]:<6}{r[2]:>5.1f} [{r[3]:>4.1f},{r[4]:>5.1f}]'
              f'{r[5]:>6.1f} [{r[6]:>4.1f},{r[7]:>5.1f}]{r[8]:>+7.1f}'
              f'{r[9]:>9}{flag}  {"Y" if r[10] else ""}')
print(f'wrote {out.name}   (* = sub-3k residue)')
