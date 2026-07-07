#!/usr/bin/env python3
"""Reduce Pune Critical Edition Mahābhārata (GRETIL) files to constituted text.

Every line has the form  "<line-id>\\t<text>".  The line-id encodes the passage:
  - constituted text : "NN,NNN.NNN" + pāda letter (lower a-h for verse, upper A-H
    for prose), e.g. "01,002.123a", "01,001.001A"
  - star passage     : contains '*', e.g. "01,002.126d*0128_01(127ab)"  (interpolation)
  - appendix passage : contains '@', e.g. "09,056.003d@003_0009"        (appendix)

For a stylometric sample of the constituted epic we keep only constituted-text
lines, drop the '*' / '@' insertion passages, and strip the line-id prefix so the
output is plain verse/prose text consistent with the other corpus files.

Within a kept text field we also strip editorial brackets: the Śāntiparvan name-
litany numbers "[1] [2] ..." and emendation brackets like "[hṛ]", plus any leaked
apparatus code and stray parenthetical footnote markers.

Usage: python3 clean_mahabharata_ce.py <file> [<file> ...]
Writes each file in place after saving a <file>.orig backup (skipped if one exists).
"""
import re
import sys

ENUM_BR   = re.compile(r'\[[\d_]+\]')            # [1], [6_116] litany/footnote numbers -> drop
LEAK_APPAR = re.compile(r'^[a-z]?[@*]\d')        # leaked interpolation code in text field
PARN_FN   = re.compile(r'\(\d+\)')               # stray (n) footnote markers


def clean(lines):
    out = []
    for raw in lines:
        line = raw.rstrip('\n')
        if '\t' not in line:
            continue                              # id-only line (empty appendix marker etc.)
        idp, txt = line.split('\t', 1)
        if '*' in idp or '@' in idp:
            continue                              # star / appendix insertion -> drop
        if LEAK_APPAR.match(txt.lstrip()):
            continue                              # interpolation code leaked into text -> drop
        txt = ENUM_BR.sub('', txt)               # drop "[1]" enumeration numbers
        txt = txt.replace('[', '').replace(']', '')  # keep supplied text "[hṛ]" -> "hṛ"
        txt = PARN_FN.sub('', txt)
        txt = re.sub(r'[ \t]{2,}', ' ', txt).strip()
        if txt:
            out.append(txt)
    return out


def main(paths):
    for p in paths:
        with open(p, encoding='utf-8') as fh:
            src = fh.readlines()
        cleaned = clean(src)
        bak = p + '.orig'
        try:
            with open(bak, 'x', encoding='utf-8') as fh:
                fh.writelines(src)
            note = f'backup: {bak}'
        except FileExistsError:
            note = 'backup exists, kept'
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(cleaned) + '\n')
        print(f'{p.split("/")[-1]}: {len(src)} -> {len(cleaned)} lines  [{note}]')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: clean_mahabharata_ce.py <file> [<file> ...]')
    main(sys.argv[1:])
