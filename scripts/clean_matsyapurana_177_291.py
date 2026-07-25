#!/usr/bin/env python3
"""Extract and clean Matsyapurāṇa adhyāyas 177-291 for stylometry.

The corpus file matsyapurana_adhyaya-1-176_pu.txt is the GRETIL e-text (input
by Oliver Hellwig), which simply stops at adhyāya 176 (itself truncated). This
script extracts the remaining chapters from the complete 291-adhyāya IAST
e-text at /mnt2/kengo/E-texts/00_inbox/New/matsya.txt (unknown web provenance,
markdown-per-chapter format, Devanagari daṇḍa punctuation) and converts them to
the layout of the GRETIL corpus file. Verified against the GRETIL overlap
(chapters 1-175): the two e-texts share a common ancestor, ~93-99.9% identical
per chapter at character level after orthographic harmonization.

Artifacts handled:
  - markdown frontmatter ("title: NNN" / "---" fences) -> "Matsya-Purāṇa N"
    chapter heading, matching the GRETIL file.
  - per-chapter summary-title first line ("...varṇanam।", "...māhātmyam") is
    dropped (every chapter except 280 has one; anything that looks like a verse
    or speaker line is kept and warned about instead).
  - speaker lines "matsya uvāca।" -> "matsya uvāca" preceded by a blank line
    (GRETIL layout).
  - verse markers "।। 200.1 ।।", "।। 177.1<eol>", "।। 251..2 ।।" -> "// 200.1 //";
    unnumbered "।।" -> "//"; half-verse daṇḍa "।" -> " /".
  - vocative exclamation marks ("sūta!", "nārada!") are removed; ॐ -> oṃ.
  - trailing double-space soft breaks and blank lines inside verses removed.
  - any character outside IAST + basic punctuation surviving cleanup is
    reported with context on stderr for hand review.
  - verse numbers are checked against the chapter number; mismatches warned.

Known limitations of the source e-text:
  - adhyāya 277 is EMPTY and the block titled 284 is a byte-identical duplicate
    of 283, i.e. the real chapters 277 and 284 are absent. Both are skipped
    here (with warnings) rather than emitted; they must be supplied from a
    scan of the printed edition (e.g. via the Chandra OCR pipeline).
  - occasional dropped half-verses (seen in the GRETIL overlap, e.g. adhyāya
    100); omissions in 177-291 can only be caught against a scan.
  - scattered corrupt verse NUMBERS (e.g. most of 181 numbered 180.x, 284-copy
    numbered 283.x); harmless downstream, where numbers are stripped.

Usage: python3 clean_matsyapurana_177_291.py [<infile> <outfile>]
"""
import re
import sys

INFILE = '/mnt2/kengo/E-texts/00_inbox/New/matsya.txt'
OUTFILE = '/mnt/kengo/stylometry-experiments/corpus/epic_puranas/matsyapurana_adhyaya-177-291_pu.txt'
FIRST, LAST = 177, 291
MISSING = {277, 284}  # empty / duplicate-of-283 in the source e-text

SPEAKER = re.compile(r'^[a-zA-Zāīūṛṝḷṃḥñṅṇṭḍśṣ\s!]*(uvāca|ūcuḥ|uvācuḥ)\s*[।!]*\s*$')
# chars legal in the cleaned output
LEGAL = re.compile(r"[^a-zāīūṛṝḷṃḥñṅṇṭḍśṣ0-9\s/.'’-]")


def clean_chapter(num, text, warn):
    lines = [l.rstrip() for l in text.split('\n')]
    lines = [l for l in lines if l.strip() and l.strip() != '---']

    # drop the summary-title first line unless it looks like verse/speaker text
    first = lines[0].strip()
    if '।।' in first or SPEAKER.match(first):
        warn(f'ch {num}: first line kept (no summary title?): {first[:60]!r}')
    else:
        lines = lines[1:]

    out = []
    for line in lines:
        s = line.strip()
        if SPEAKER.match(s):
            s = re.sub(r'\s*[।!]+\s*$', '', s)
            if out:
                out.append('')
            out.append(s)
            continue
        s = s.replace('!', '')
        s = s.replace('ॐ', 'oṃ')
        # residue seen in 177-291: stray Devanagari virāma ("nair्ṛtī"),
        # zero-width non-joiner, lacuna/uncertainty marks, underscore, and
        # parenthetical variant readings ("gu(mu)ruṃḍā" -> "guruṃḍā").
        s = s.replace('्', '').replace('‌', '').replace('‍', '')
        s = s.replace('॥', '।।')  # true double-danda char -> ।। before marker regexes
        s = re.sub(r'\([^)]*\)', '', s)
        s = re.sub(r'[?*_]', '', s)
        # verse markers: ।। N.M ।। / ।। N.M<eol> / ।। N..M ।। / ।।। variants
        def vnum(m):
            ch, v = m.group(1), m.group(2)
            if int(ch) != num:
                warn(f'ch {num}: verse number {ch}.{v}')
            return f' // {ch}.{v} //'
        s = re.sub(r'\s*।{2,3}\s*(\d+)\.+(\d+)\s*।{0,3}\s*$', vnum, s)
        s = re.sub(r'\s*।{2,3}\s*$', ' //', s)   # unnumbered verse end
        s = re.sub(r'\s*।\s*', ' / ', s)          # half-verse danda
        s = re.sub(r'\s+', ' ', s).strip()
        s = re.sub(r'\s+/$', ' /', s)
        if s:
            out.append(s)

    for line in out:
        for m in LEGAL.finditer(line):
            warn(f'ch {num}: stray char {m.group(0)!r} in: {line[:60]!r}')
    return out


def main():
    infile = sys.argv[1] if len(sys.argv) > 2 else INFILE
    outfile = sys.argv[2] if len(sys.argv) > 2 else OUTFILE
    raw = open(infile, encoding='utf-8').read()
    chapters = re.findall(r'title: (\d+)\s*\n\s*---\n(.*?)(?=\ntitle: \d+|\Z)',
                          raw, re.S)
    chapters = [(int(n), t) for n, t in chapters if FIRST <= int(n) <= LAST]
    assert [n for n, _ in chapters] == list(range(FIRST, LAST + 1)), \
        'chapter range not contiguous'

    warnings = []
    blocks = []
    for num, text in chapters:
        if num in MISSING:
            warnings.append(f'ch {num}: SKIPPED (missing/duplicate in source '
                            f'e-text, supply from a scan)')
            continue
        body = clean_chapter(num, text, warnings.append)
        blocks.append(f'Matsya-Purāṇa {num}\n\n' + '\n'.join(body))

    with open(outfile, 'w', encoding='utf-8') as f:
        f.write('\n\n\n'.join(blocks) + '\n')

    print(f'wrote {outfile}: chapters {FIRST}-{LAST}')
    print(f'{len(warnings)} warnings')
    for w in warnings:
        print('  WARN', w, file=sys.stderr)


if __name__ == '__main__':
    main()
