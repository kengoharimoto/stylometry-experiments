#!/usr/bin/env python3
"""Clean bhavisyapurana.txt for stylometry.

Base IAST verse text is sound. Artifacts removed:
  - anukramaṇikā / index lines: begin with TWO numbers (footnote-no + chapter-no)
    and list chapter topics, ending "ślo. N", e.g. "7 16 vivāhavidhivarṇanam ślo. 68"
  - publisher / reprint bibliographic lines at the top, e.g. "(khemarāja ..., mumbaī)"
  - pure-numeric chapter markers ("1.1") and bare "N ||" count lines
  - 'Â' / 'â' mojibake characters
  - inline footnote-reference digits embedded in verse text, either at pāda start
    ("4 bhūpatiḥ ...", "1 vada ...") or glued to a word ("3sthūlāgrā", "ka5rkaṭākṣāḥ")

Verse/chapter numbers delimited by '|' (e.g. "| | 34", "||49||", "|| 4.175.60 |")
are genuine structure and preserved.

Usage: python3 clean_bhavisyapurana.py <infile> <outfile>
"""
import re
import sys

L = 'a-zāīūṛṝḷḹṃḥṅñṇśṣṭḍ'
DROP = [
    re.compile(r'^\s*\d+\s+\d+[.\s]'),       # two-number index line ("30 4. ...", "19 29 ...")
    re.compile(r'ślo\s*[.,\-]?\s*\d'),       # any anukramaṇikā entry ("ślo. 90", "ślo, 9", "ślo 38")
    re.compile(r'^\s*\('),                   # (publisher, city)
    re.compile(r'prakāśaka'),                # reprint/publisher line
    re.compile(r'^\s*[0-9.]+\s*$'),          # pure-numeric chapter marker "1.1", "5"
    re.compile(r'^\s*\d+\s*\|\|?\s*$'),      # bare "892 ||" count line
]
MOJIBAKE  = re.compile(r'[Ââ]')
INLINE_FN = re.compile(r'\s*\(\d+\)')                   # (1) footnote reference marker
LEAD_NUM  = re.compile(rf'^\s*\d+\s+(?=[{L}])')          # pāda-initial footnote digit
GLUED_NUM = re.compile(rf'(?<=[{L}])\d+|\d+(?=[{L}])')   # footnote digit glued to a word


def clean(lines):
    out = []
    for raw in lines:
        line = raw.rstrip('\n')
        if any(p.search(line) for p in DROP):
            continue
        if not line.strip():
            out.append('')
            continue
        line = MOJIBAKE.sub(' ', line)
        line = INLINE_FN.sub('', line)
        line = LEAD_NUM.sub('', line)
        line = GLUED_NUM.sub('', line)
        line = re.sub(r'[ \t]+', ' ', line).strip()
        out.append(line)
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
        sys.exit('Usage: clean_bhavisyapurana.py <infile> <outfile>')
    lines = open(sys.argv[1], encoding='utf-8').readlines()
    cleaned = clean(lines)
    open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(cleaned) + '\n')
    print(f'in : {len(lines)} lines')
    print(f'out: {len(cleaned)} lines')


if __name__ == '__main__':
    main()
