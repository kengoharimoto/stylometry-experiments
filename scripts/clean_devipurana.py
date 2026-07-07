#!/usr/bin/env python3
"""Clean devipurana.txt for stylometry.

Base IAST verse text is sound. Artifacts removed:
  - front matter before the "TEXT BEGINS HERE" banner: a duplicated chapter-4
    opening plus an English "Suggestions:" editorial discussion.
  - '%' comment/placeholder lines (%%%%%TEXT BEGINS HERE%%%%, %% Chapter-002 ...).
  - bracketed manuscript apparatus, both whole-line ("[na kramā0 ka; ...]") and
    multi-line ("[eteṣāṃ yo dhanaṃ icchet ka |" ... "eteṣāṃ yo vadhamicchet-ga]").
  - inline reference tags: "[004:015]", "||005:011ef||", and "[1]" footnote refs.
  - English editor/translator comments embedded mid-text (e.g. "Note: ... font 8pt.",
    "in pdf page 34", "what to do with this line ?"). These are detected by the
    presence of IAST-illegal Latin letters w/x/z/q/f AFTER refs and mojibake are
    removed, so genuine Sanskrit lines (which never use those letters) are kept.
  - 'â' mojibake is stripped in place (it occurs inside genuine verses), not dropped.

Verse-number lines like "|1||" (no colon) are genuine structure and preserved.

Usage: python3 clean_devipurana.py <infile> <outfile>
"""
import re
import sys

# Reference tags come in several forms: [004:015], [004:039 (unterminated),
# ||005:011ef||, ||055:005:P2||, ||014:007a-d||, ||010:008 p1||, and [1] footnotes.
REF = re.compile(r'\[\s*\d+:\d+[^\]]*\]?|\|\|\s*\d+:\d+[^|]*(?:\|\|)?|\[\d+\]')
# Manuscript-variant apparatus that opens with '||' + text instead of '[' , e.g.
# "||somaṃ rājaṃ ... ka ga]".  Genuine verse text never starts with '||'.
APPAR_PIPE = re.compile(r'^\s*\|\|\s*[^\d|\s]')
# Numbered manuscript-variant footnotes: "1. ka ga pustake ... nāsti |", and a
# stray lone '*'.
APPAR_NOTE = re.compile(r'pustake?.*(nāsti|na vidyate)|ślokārtha')
INLINE_FN  = re.compile(r'\s*\(\d+\)')
LATIN = re.compile(r'[wxzqfWXZQF]')          # IAST-illegal -> English/editorial line
MULTILINE_CAP = 12                            # max lines an unclosed '[' may span


def clean(lines):
    # Drop everything up to and including the "TEXT BEGINS HERE" banner.
    start = 0
    for i, l in enumerate(lines):
        if 'TEXT BEGINS HERE' in l:
            start = i + 1
            break
    body = [l.rstrip('\n') for l in lines[start:]]

    out = []
    i, n = 0, len(body)
    while i < n:
        line = body[i]
        s = line.strip()
        if not s:
            out.append('')
            i += 1
            continue
        if s[0] == '%' or s == '*':
            i += 1
            continue
        if APPAR_NOTE.search(line):           # numbered manuscript-variant footnote
            i += 1
            continue
        if APPAR_PIPE.match(line):            # "||somaṃ ... ka ga]" variant apparatus
            i += 1
            continue
        if s[0] == '[':
            if ']' in line:                   # whole-line apparatus
                i += 1
                continue
            # multi-line apparatus: drop until a line closes with ']'
            j = i + 1
            while j < n and j - i <= MULTILINE_CAP and ']' not in body[j]:
                j += 1
            if j < n and j - i <= MULTILINE_CAP and ']' in body[j]:
                i = j + 1                      # drop the whole span
            else:
                i += 1                         # unterminated: drop only the opener
            continue
        # kept line: strip refs and mojibake, then test for English
        line = REF.sub('', line)
        line = INLINE_FN.sub('', line)
        line = line.replace('â', ' ')
        if LATIN.search(line):
            i += 1
            continue
        line = line.replace('[', '').replace(']', '')   # scrub orphan brackets
        line = re.sub(r'\s*\|\|\s*$', '', line)          # drop dangling trailing "||"
        line = re.sub(r'[ \t]+', ' ', line).strip()
        out.append(line)
        i += 1

    res = []
    for ln in out:
        if ln == '' and (not res or res[-1] == ''):
            continue
        res.append(ln)
    while res and res[0] == '':
        res.pop(0)
    while res and res[-1] == '':
        res.pop()
    return res


def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: clean_devipurana.py <infile> <outfile>')
    lines = open(sys.argv[1], encoding='utf-8').readlines()
    cleaned = clean(lines)
    open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(cleaned) + '\n')
    print(f'in : {len(lines)} lines')
    print(f'out: {len(cleaned)} lines')


if __name__ == '__main__':
    main()
