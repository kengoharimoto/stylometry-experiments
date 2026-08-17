#!/usr/bin/env python3
"""Scan the E-texts library for verbatim overlaps with the Bhagavatapurana.

Method: normalize everything to a bare IAST letter stream (lowercase, all
whitespace/punctuation/digits removed). Index every k-mer (k=21) of the BhP
stream; scan candidate files at stride s=10, so any common substring of
length >= k+s-1 = 30 (~ half-sloka) is guaranteed to contain a sampled
k-mer; extend candidate hits bidirectionally to maximal matches; merge
overlaps. Report matches >= 30 chars with BhP locus, raw context and a
crude named/unnamed flag (bhāgavat- within +-300 raw chars).
"""
import re, sys, unicodedata
from pathlib import Path
from array import array

ROOT = Path('/mnt2/kengo/E-texts')
BHP = ROOT / '1_sanskr/3_purana/unknown_bhagavatapurana_all.txt'
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('bhp_matches.tsv')
K, STRIDE, MINLEN = 21, 10, 30

KEEP = set("abcdefghijklmnopqrstuvwxyzāīūṛṝḷḹṃḥśṣṇṭḍṅñ'")
TRANS = {'’': "'", '‘': "'", 'ṁ': 'ṃ', 'ê': 'e', 'ô': 'o'}

def norm_stream(raw):
    """Return (normalized string, array of raw-offsets per kept char)."""
    out, offs = [], array('l')
    for i, ch in enumerate(raw):
        c = ch.lower()
        c = TRANS.get(c, c)
        if c in KEEP:
            out.append(c)
            offs.append(i)
    return ''.join(out), offs

# ---- build BhP index -------------------------------------------------
tag_re = re.compile(r'^(BhP_[\d.]+/?\d*)\s+(.*)')
bhp_parts, bhp_tags = [], []   # tags: (stream_offset, tag)
pos = 0
for line in BHP.read_text(encoding='utf-8', errors='replace').splitlines():
    m = tag_re.match(line)
    if not m:
        continue
    s, _ = norm_stream(m.group(2))
    if not s:
        continue
    bhp_tags.append((pos, m.group(1)))
    bhp_parts.append(s)
    pos += len(s)
BHP_S = ''.join(bhp_parts)
print(f'BhP stream: {len(BHP_S):,} chars, {len(bhp_tags):,} padas', flush=True)

index = {}
for i in range(len(BHP_S) - K + 1):
    km = BHP_S[i:i+K]
    if km not in index:
        index[km] = i
print(f'index: {len(index):,} k-mers', flush=True)

import bisect
tag_offs = [t[0] for t in bhp_tags]
def locus(p):
    return bhp_tags[max(0, bisect.bisect_right(tag_offs, p) - 1)][1]

# ---- candidate files -------------------------------------------------
SCAN_DIRS = ['1_sanskr', '2_pali', '2_prakrt', '3_nia', '5_var',
             '6_other_languages', '00_inbox', '30_review']
EXCL = re.compile(r'bhagavatapurana|bhagavata_|bhagavatapur|-bhagavatapurana|'
                  r'devibhagavata|_trash', re.I)
files = []
for d in SCAN_DIRS:
    p = ROOT / d
    if p.is_dir():
        files += [f for f in p.rglob('*.txt') if not EXCL.search(str(f))]
files.sort()
print(f'{len(files)} files to scan', flush=True)

NAMED = re.compile(r'bhāgavat|bhagavat', re.I)

def scan_file(path):
    try:
        raw = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return []
    s, offs = norm_stream(raw)
    n = len(s)
    if n < MINLEN:
        return []
    hits = []   # (cand_start, cand_end, bhp_start)
    i = 0
    while i <= n - K:
        j = index.get(s[i:i+K])
        if j is not None:
            # extend
            a, b = i, i + K          # cand [a,b)
            ja, jb = j, j + K        # bhp
            while a > 0 and ja > 0 and s[a-1] == BHP_S[ja-1]:
                a -= 1; ja -= 1
            while b < n and jb < len(BHP_S) and s[b] == BHP_S[jb]:
                b += 1; jb += 1
            if b - a >= MINLEN:
                if hits and a <= hits[-1][1]:
                    if b > hits[-1][1]:
                        pa, pb, pj = hits[-1]
                        if b - a > pb - pa:
                            hits[-1] = (a, b, ja)
                        else:
                            hits[-1] = (pa, b, pj)
                else:
                    hits.append((a, b, ja))
                i = b - K + 1 if b - K + 1 > i else i + STRIDE
                continue
        i += STRIDE
    rows = []
    for a, b, ja in hits:
        ra, rb = offs[a], offs[b-1] + 1
        ctx = raw[max(0, ra-250):min(len(raw), rb+250)]
        named = bool(NAMED.search(ctx))
        snippet = ' '.join(raw[ra:rb].split())
        rows.append((str(path.relative_to(ROOT)), b - a, locus(ja),
                     'named' if named else 'unnamed', snippet[:200],
                     ' '.join(ctx.split())[:400]))
    return rows

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('file\tlen\tbhp_locus\tattrib\tmatch\tcontext\n')
    for nf, path in enumerate(files):
        rows = scan_file(path)
        for r in rows:
            f.write('\t'.join(map(str, r)) + '\n')
        if nf % 500 == 0:
            print(f'{nf}/{len(files)} {path.name} ({sum(1 for _ in open(OUT))-1} rows)', flush=True)
print('done', flush=True)
