#!/usr/bin/env python3
"""Reduce the GRETIL Harivaṃśa (Vaidya CE, constituted text with star passages)
to constituted text only, matching the policy of clean_mahabharata_ce.py.

Source: E-texts/1_sanskr/2_epic/mbh/ext/unknown_harivamsa_padapatha.txt
(kept as corpus/epic_puranas/harivamsa.txt.orig; re-run the cleaner from that).

Format differs from the Pune-CE parvan files (which were "line-id<TAB>text"):
  - constituted verse : unindented, "... /" (uneven pāda) or "... // HV_n.n //"
    (one ref is malformed as "HV_70,18" — comma accepted)
  - star passages     : lines indented with U+00A0 non-breaking spaces,
    tagged "| *HV_ref |"                                         -> drop
  - apparatus         : "[k: ... :k]" (nbsp-indented too), plus two stray
    unindented "ḥK,Ñ2.3,... ins. after 36ḥ" lines                -> drop
  - chapter headers   : "[h: ... :h]", "[Colophon]" placeholders -> drop
  - scribal prose     : "||* śrīr astu *||" benedictions          -> drop
  - interlocutor      : "{śaunaka uvāca}"  -> keep, braces stripped
Within kept text: "+ +" compound-split markers are rejoined, "(sic)" and
stray "*" hiatus markers removed, and a handful of source typos fixed
(ASCII-dot diacritics "d."/"h." for ḍ/ḥ, "_" for space in periphrastic
perfects, a stray line-initial ".", a stray "Ṭ" before rājā at HV 9.47,
and "śūrasenā?" for śūrasenāñ at HV 96.52).

Usage: python3 clean_harivamsa_ce.py <src> <dst>
"""
import re
import sys

NBSP = '\xa0'
VERSE_REF = re.compile(r'\s*//\s*HV_[\d.,]+\s*//\s*$')

SOURCE_FIXES = [          # typos in the GRETIL source, verified against context
    ('m_āsa', 'm āsa'),   # nivedayām_āsa, visarjayām_āsa
    ('bhāṇd.aṃ', 'bhāṇḍaṃ'),
    ('vīrah.', 'vīraḥ'),
    ('dhvajāh.', 'dhvajāḥ'),
    ('śūrasenā?', 'śūrasenāñ'),  # -ān + śaśāsa
    ('Ṭrājā', 'rājā'),
]


def clean(lines):
    out, other = [], []
    started = False
    for raw in lines:
        line = raw.rstrip('\n').rstrip()
        if not started:                      # skip GRETIL file header
            started = line.startswith('[h:')
            continue
        if (not line or line.startswith(NBSP) or line.startswith('[h:')
                or '[k:' in line or line == '[Colophon]' or '||*' in line
                or (line.startswith('ḥ') and line.endswith('ḥ'))):
            continue
        if line.startswith('{') and line.endswith('}'):
            out.append(line[1:-1].strip())   # interlocutor
            continue
        if VERSE_REF.search(line) or line.endswith('/'):
            txt = VERSE_REF.sub('', line).rstrip().rstrip('/').rstrip()
            txt = txt.replace('+ +', '').replace('+', '')
            txt = txt.replace('(sic)', '').replace('*', ' ')
            for old, new in SOURCE_FIXES:
                txt = txt.replace(old, new)
            txt = re.sub(r'\s{2,}', ' ', txt).strip().lstrip('. ')
            if txt:
                out.append(txt)
            continue
        other.append(line)
    return out, other


def main(src, dst):
    with open(src, encoding='utf-8') as fh:
        lines = fh.readlines()
    cleaned, other = clean(lines)
    if other:
        print(f'WARNING: {len(other)} unclassified lines dropped:', file=sys.stderr)
        for l in other[:20]:
            print(f'  {l!r}', file=sys.stderr)
    with open(dst, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(cleaned) + '\n')
    print(f'{src.split("/")[-1]}: {len(lines)} -> {len(cleaned)} lines -> {dst}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: clean_harivamsa_ce.py <src> <dst>')
    main(sys.argv[1], sys.argv[2])
