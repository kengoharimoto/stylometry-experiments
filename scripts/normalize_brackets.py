#!/usr/bin/env python3
"""Normalize editorial square-brackets in epic_puranas files.

Bracket contents fall into two classes:
  REMOVE (editorial/apparatus/reference):
    - numbers / star / ref tags: [42], [*42], [Vdha_3,343.1.12]
    - illegible & lacuna markers: [??], [!!!], [...], [lacuna], []
    - English/German notes & cross-refs: [note: ...], [COMM.: ...], [idem ...],
      [Gap in Original], [steht so dort]
  KEEP (unwrap, drop only the brackets):
    - editorially supplied Sanskrit: [mathurā-māhātmyam], [saṃsmarantaḥ]
    - bracketed colophons: [iti nīlamate dhānyapākas+|]

Heuristic: a bracket is editorial if its content has a digit, one of * ! ? °, is
punctuation-only, or contains an English/German apparatus keyword; otherwise it is
supplied Sanskrit and is unwrapped.

Usage: python3 normalize_brackets.py <file> [<file> ...]
Writes each file in place after saving a <file>.orig backup (skipped if one exists).
"""
import re
import sys

KEYWORD = re.compile(r'note|comm|idem|gap|steht|dort|corr|\bed\b|\bread\b|\bcf\b'
                     r'|lacuna|incomplete|original|verse', re.I)
PUNCT_ONLY_C = re.compile(r'[.\s|+/·:-]*$')       # bracket content that is only punctuation


def _bracket(m):
    c = m.group(1)
    if not c.strip():
        return ''
    if re.search(r'\d|[*!?°]', c):
        return ''
    if KEYWORD.search(c):
        return ''
    if PUNCT_ONLY_C.fullmatch(c):
        return ''
    return c                                       # unwrap supplied Sanskrit / colophon


def clean_text(text):
    text = re.sub(r'\[([^\[\]]*)\]', _bracket, text)
    text = text.replace('[', '').replace(']', '')  # orphan brackets
    out = []
    for line in text.split('\n'):
        line = re.sub(r'[ \t]{2,}', ' ', line).rstrip()
        if line.strip() and re.fullmatch(r'[.\s|]*', line):
            continue                               # punctuation-only leftover
        out.append(line)
    res = []
    for l in out:
        if l == '' and (not res or res[-1] == ''):
            continue
        res.append(l)
    return '\n'.join(res)


def main(paths):
    for p in paths:
        src = open(p, encoding='utf-8').read()
        before = src.count('[') + src.count(']')
        out = clean_text(src)
        after = out.count('[') + out.count(']')
        try:
            open(p + '.orig', 'x', encoding='utf-8').write(src)
            note = 'backup saved'
        except FileExistsError:
            note = 'backup exists, kept'
        open(p, 'w', encoding='utf-8').write(out)
        print(f'{p.split("/")[-1]}: brackets {before}->{after}  [{note}]')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: normalize_brackets.py <file> [<file> ...]')
    main(sys.argv[1:])
