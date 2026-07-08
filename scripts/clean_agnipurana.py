#!/usr/bin/env python3
"""Clean the GRETIL Agnipurāṇa file for stylometry.

The raw agnipurana_u.txt is the GRETIL edition WITH full critical apparatus and
page furniture, unlike its clean corpus siblings. That non-text material makes it
an extreme stylometric outlier. This pass removes:

  1. Front matter / table of contents (anukramaṇikā) preceding the first verse.
  2. Critical-apparatus footnote lines (manuscript variant readings), which begin
     with a digit, e.g.  "1 dharaṇyā iti kha, cihnitapustakapāṭhaḥ".
  3. GRETIL markup lines beginning with ':' ( :n note blocks, :p page markers,
     :e colophons, :ś chapter headings ) and '%' chapter comments.
  4. Underscore separator rules.
  5. Inline footnote reference numbers glued onto words, e.g.  "śriyaṃ(1)" -> "śriyaṃ".

Everything else -- verse lines (with their /AP_x.y.../ tags, kept to match how the
sibling files keep their own reference tags), speaker attributions (uvāca / ūcuḥ),
and ritual mantra lines -- is preserved. Mantra content is genuine text; only
editorial/structural material and inline footnote markers are stripped here.

NOTE: the /AP_x.y.../ reference tags are NOT dropped by this pass, so they stay in
the cleaned corpus alongside the sibling files' own reference markers. Unlike those
siblings' letterless numeric markers (e.g. "01.01.001/1"), the AP_ tags contain
Latin letters and would leak into the unsandhied output, so they are stripped one
layer downstream, at inference time, by strip_ref_markers() in
process_epic_puranas_unsandhied[_local].py.

Usage: python3 clean_agnipurana.py <infile> <outfile>
"""
import re
import sys

INLINE_FOOTNOTE = re.compile(r'\([0-9]+\)')
AP_TAG = re.compile(r'AP_[0-9]')
# A handful of apparatus notes appear as free-standing lines without a leading
# digit or ':' marker (e.g. "... iti ṅa, cihnitapustakapāṭhaḥ"). They always
# carry textual-criticism vocabulary and never an AP_ tag, so drop untagged
# lines matching this signature.
APPARATUS_SIG = re.compile(r'cih.nitapustak|labdhapustak|mudritapāṭh|pāṭhāntar|mallabdh')


def clean(lines):
    # 1. Drop all front matter before the first verse (first line with an AP_ tag).
    first_verse = next((i for i, ln in enumerate(lines) if AP_TAG.search(ln)), 0)
    body = lines[first_verse:]

    out = []
    for raw in body:
        line = raw.rstrip('\n')
        stripped = line.strip()

        if not stripped:
            out.append('')
            continue
        # 3. GRETIL markup / structural comment lines.
        if stripped[0] in ':%':
            continue
        # 4. Underscore separator rules.
        if set(stripped) <= {'_'}:
            continue
        # 2. Critical-apparatus footnote lines begin with a digit. Verse lines
        #    never do (they end with an AP_ tag), so this is safe here.
        if stripped[0].isdigit():
            continue
        # 2b. Free-standing apparatus notes without a leading digit/marker.
        if not AP_TAG.search(line) and APPARATUS_SIG.search(line):
            continue

        # 5. Strip inline footnote reference numbers, then tidy whitespace.
        line = INLINE_FOOTNOTE.sub('', line)
        line = re.sub(r'[ \t]+', ' ', line).strip()
        out.append(line)

    # Collapse runs of blank lines to a single blank.
    result = []
    for ln in out:
        if ln == '' and (not result or result[-1] == ''):
            continue
        result.append(ln)
    while result and result[0] == '':
        result.pop(0)
    while result and result[-1] == '':
        result.pop()
    return result


def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: clean_agnipurana.py <infile> <outfile>')
    with open(sys.argv[1], encoding='utf-8') as fh:
        lines = fh.readlines()
    cleaned = clean(lines)
    with open(sys.argv[2], 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(cleaned) + '\n')
    print(f'in : {len(lines)} lines')
    print(f'out: {len(cleaned)} lines')


if __name__ == '__main__':
    main()
