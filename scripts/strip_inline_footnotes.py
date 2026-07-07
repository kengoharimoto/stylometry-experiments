#!/usr/bin/env python3
"""Strip inline footnote-reference markers from epic_puranas corpus files.

Parenthetical digits like "(1)" are editorial footnote markers, never part of the
IAST text; they appear standalone, glued to a word ("(1)prathamo"), or as part of
a star-passage citation in visnudharma_pu ("002.015,*(1)", "002.*(2)").

Removal order:
  1. "[,.]?*(n)"  -> ''   (star-passage footnotes; only fires where '*(n)' exists,
     so it is a no-op on files without star markers)
  2. "(n)"        -> ''   (plain footnote markers)

Numeric verse-reference tails (e.g. "002.015") are left intact.

Usage: python3 strip_inline_footnotes.py <file> [<file> ...]
Writes each file in place after saving a <file>.orig backup (skipped if one exists).
"""
import re
import shutil
import sys

STAR  = re.compile(r'[,.]?\*\(\d+\)')
PLAIN = re.compile(r'\(\d+\)')


def clean_text(text):
    text = STAR.sub('', text)
    text = PLAIN.sub('', text)
    # tidy any doubled spaces the removals leave behind
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text


def main(paths):
    for p in paths:
        with open(p, encoding='utf-8') as fh:
            src = fh.read()
        before = len(PLAIN.findall(src))
        out = clean_text(src)
        after = len(PLAIN.findall(out))
        bak = p + '.orig'
        try:
            with open(bak, 'x', encoding='utf-8') as fh:
                fh.write(src)
            bak_note = f'backup: {bak}'
        except FileExistsError:
            bak_note = 'backup exists, kept'
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(out)
        print(f'{p}: removed {before - after} markers ({before}->{after})  [{bak_note}]')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: strip_inline_footnotes.py <file> [<file> ...]')
    main(sys.argv[1:])
