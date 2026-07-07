#!/usr/bin/env python3
"""Clean saurapurana.txt for stylometry.

The base IAST verse text is sound; the file carries edition furniture:
  - [p. N] page markers (one per line)
  - [SSF: editorial note markers and stray ':' lines
  - pure-numeric running-count lines, e.g. "309 ||"  or  "41 || 589 ||"
  - leading cumulative-count / footnote digits, e.g. "151 || iti ..."  or  "11 dvijaḥ ..."
  - embedded footnote digits glued to a word, e.g. "6ṅacaṅasajñi"
  - 'x' illegible-reading markers: as whole lines, at pāda start, or mid-verse
  - three 'x ... pustake ... nāsti / na vidyate' apparatus lines

Verse numbers delimited by '|' (e.g. "|| 14 ||") and chapter numbers in colophons
are genuine structure and preserved.

Usage: python3 clean_saurapurana.py <infile> <outfile>
"""
import re
import sys

L = 'a-zāīūṛṝḷḹṃḥṅñṇśṣṭḍ'                       # IAST letters
DROP = [
    re.compile(r'^\s*\[p\.'),                  # [p. 12]
    re.compile(r'^\s*\[SSF'),                  # editorial note
    re.compile(r'^\s*:\s*$'),                  # stray colon
    re.compile(r'^\s*\d+\s*\|\|?\s*(\d+\s*\|\|?\s*)?$'),  # "309 ||" / "41 || 589 ||"
    re.compile(r'^\s*[xX*]\s*$'),              # lone illegible / apparatus marker
    re.compile(r'ślokārtha|pustak.*(na vidyate|nāsti|vartate)'),  # apparatus notes
]
LEAD_COLON = re.compile(r'^\s*:\s*')                   # stray leading colon
LEAD_NUM   = re.compile(r'^\s*\d+\s*')                 # leading count/footnote digit (incl. "1724||")
LEAD_X     = re.compile(r'^[xX*]\s*')                  # leading illegible / apparatus marker
GLUED_NUM  = re.compile(rf'(?<=[{L}])\d+|\d+(?=[{L}])') # digit glued to a letter
MID_X      = re.compile(rf'(?<=\s)[xX](?=\s)')         # mid-verse illegible marker
INLINE_FN  = re.compile(r'\s*\(\d+\)')                 # (1) (2) footnote reference markers


def clean(lines):
    out = []
    for raw in lines:
        line = raw.rstrip('\n')
        s = line.strip()
        if not s:
            out.append('')
            continue
        if any(p.search(line) for p in DROP):
            continue
        # Strip leading junk repeatedly: removing a leading count can expose a
        # ':' or '*' marker underneath (e.g. "892 : tasmāt" -> ": tasmāt" -> "tasmāt").
        prev = None
        while prev != line:
            prev = line
            line = LEAD_COLON.sub('', line)
            line = LEAD_X.sub('', line)
            line = LEAD_NUM.sub('', line)
        line = INLINE_FN.sub('', line)
        line = GLUED_NUM.sub('', line)
        line = MID_X.sub('', line)
        line = re.sub(r'[ \t]+', ' ', line).strip()
        if line:
            out.append(line)
    # collapse blank runs
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
        sys.exit('Usage: clean_saurapurana.py <infile> <outfile>')
    lines = open(sys.argv[1], encoding='utf-8').readlines()
    cleaned = clean(lines)
    open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(cleaned) + '\n')
    print(f'in : {len(lines)} lines')
    print(f'out: {len(cleaned)} lines')


if __name__ == '__main__':
    main()
