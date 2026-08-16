#!/usr/bin/env python3
"""Build the pre-stripped sandhied corpus for the stylo no-space C3 counterpart.

The article's C3 convention counts character trigrams over the continuous
sandhied stream (scriptio continua): hero_mds.py --strip-spaces lowercases and
deletes ALL whitespace (word spaces and line breaks) before counting. R stylo
has no such mode, so the cross-validation feeds it this corpus instead: each
manifest unit written as a single line with every whitespace character removed.
Under splitting.rule = whitespace each file is then one token, and stylo's
char-3-gram features run over the identical stream (stylo lowercases via
preserve.case = FALSE; case is left untouched here).

Source: corpus/epic_puranas_sandhied (colophon-free since 2026-08-16).
Output: corpus/epic_puranas_sandhied_nospace (manifest units only).

Usage: python3 scripts/build_nospace_sandhied_corpus.py \
           [--manifest manifests/dicsep2026_n127_ppl.txt]
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ap = argparse.ArgumentParser()
ap.add_argument('--manifest', default='manifests/dicsep2026_n127_ppl.txt')
ap.add_argument('--source-dir', default='corpus/epic_puranas_sandhied')
ap.add_argument('--out-dir', default='corpus/epic_puranas_sandhied_nospace')
args = ap.parse_args()

src = ROOT / args.source_dir
out = ROOT / args.out_dir
out.mkdir(exist_ok=True)

units = [l.strip() for l in (ROOT / args.manifest).read_text(encoding='utf-8')
         .splitlines() if l.strip() and not l.startswith('#')]
units = [u if u.endswith('.txt') else u + '.txt' for u in units]

missing = [u for u in units if not (src / u).exists()]
if missing:
    sys.exit(f'manifest units not in {src}: {missing}')

for u in units:
    txt = (src / u).read_text(encoding='utf-8')
    (out / u).write_text(re.sub(r'\s+', '', txt) + '\n', encoding='utf-8')

stale = [p.name for p in out.glob('*.txt') if p.name not in set(units)]
print(f'{len(units)} units written to {out}')
if stale:
    print(f'WARNING: {len(stale)} stale file(s) from a previous build in '
          f'{out} (not in manifest): {stale[:5]}{"..." if len(stale) > 5 else ""}')
