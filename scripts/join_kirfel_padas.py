#!/usr/bin/env python3
"""Normalize the Kirfel PPL corpus files to one half-śloka per line.

The segmenter honored Kirfel's print line breaks, which drop to one pāda per
line in the parallel-column stretches and for longer meters. The rest of the
corpus is one half-śloka per line, and line-granularity mismatches distort
line-level tooling (the reuse scanner's fuzz.ratio is symmetric, so a pāda
inside a half-śloka scores ~65 and escapes the match).

Joining rule, from Kirfel's own punctuation: a line is terminal when it ends
with the half-verse daṇḍa "|" or a verse number "|| n ||" (trailing ".", ","
or "]" allowed); anything else is a continuation and joins the next line.
"#" comment lines and blanks flush the buffer and pass through untouched.
A buffer never grows past 6 source lines (defensive flush for stretches
where OCR lost the daṇḍa).

Rewrites corpus/epic_puranas/kirfel_*.txt in place; git holds the previous
state. Rebuild the derived corpora afterwards.

Usage: python3 scripts/join_kirfel_padas.py [--dry-run]
"""
import argparse
import re
import statistics
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[1] / 'corpus/epic_puranas'

RE_TERMINAL = re.compile(r'(\|\|\s*\d*\s*\|\||\|)[\s.,;\])]*$')
MAX_BUFFER = 6


def join_lines(lines):
    out, buf = [], []
    def flush():
        if buf:
            out.append(' '.join(buf))
            buf.clear()
    for raw in lines:
        s = raw.strip()
        if not s or s.startswith('#'):
            flush()
            out.append(raw)
            continue
        buf.append(s)
        if RE_TERMINAL.search(s) or len(buf) >= MAX_BUFFER:
            flush()
    flush()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    for p in sorted(CORPUS.glob('kirfel_*.txt')):
        lines = p.read_text(encoding='utf-8').splitlines()
        joined = join_lines(lines)
        def body_lens(ls):
            return [len(l) for l in ls if l.strip() and not l.lstrip().startswith('#')]
        print(f'{p.name}: {len(lines)} -> {len(joined)} lines; '
              f'median body len {statistics.median(body_lens(lines)):.0f} -> '
              f'{statistics.median(body_lens(joined)):.0f} chars')
        if not args.dry_run:
            p.write_text('\n'.join(joined) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
