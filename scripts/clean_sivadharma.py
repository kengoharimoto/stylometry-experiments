#!/usr/bin/env python3
"""Clean the Śivadharmaśāstra and Śivadharmottara e-texts into corpus units.

Sources (E-texts/1_sanskr/4_rellit/saiva/sivadharma/):
  unknown_sivadharmasastra.txt   Acharya (IFP): Naraharinath ed. + T32 collation
  unknown_sivadharmottara.txt    Acharya / Operato / Goodall, T75 + Bodl. collation
Each raw source is saved as corpus/epic_puranas/<out>.txt.orig.

Both files interleave apparatus with the mainline text:
  - "%%" comments and "%" apparatus lines            -> drop
  - variant lines containing "\\" sigla (\\T32, \\T75, \\Bodl., \\ed, \\conj,
    \\Colo) — whether or not they end in a daṇḍa     -> drop
  - variant/note lines with "/ Bodl." "/ T75" sigla  -> drop
  - English editorial lines (any ASCII capital)      -> drop
  - "p.N" page markers, "……" dot-run rows            -> drop
  - "===>" editorial tails inside a text line        -> cut the tail
Kept mainline text: verse lines ending "|" / "|| n.n ||" (ŚDhU ch.10 uses a
bare trailing number instead), speaker lines, Sanskrit chapter incipits and
colophons.  Daṇḍas, verse numbers and stray punctuation are stripped; in the
ŚDhŚ an intra-word "." encodes an elided initial a- (prathamo.adhyāyaḥ) and
is replaced by an avagraha ("prathamo 'dhyāyaḥ").

Usage: python3 clean_sivadharma.py     (paths fixed; writes corpus files)
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DIR = REPO / 'corpus' / 'epic_puranas'
SRC = Path('/Users/kengo_1/Documents/E-texts/1_sanskr/4_rellit/saiva/sivadharma')

UNITS = [
    ('unknown_sivadharmasastra.txt', 'sivadharmasastra'),
    ('unknown_sivadharmottara.txt',  'sivadharmottara'),
]

SIGLA_SLASH = re.compile(r'/\s*(Bodl|T\d|ed\b|conj)')
VERSE_NUM = re.compile(r'\|\|?\s*[\d.]+\s*(\|\|?|$)')   # || 1.2 || , also mid-line
TRAIL_NUM = re.compile(r'(\s+\d+[a-d]?)+\s*$')          # "… tarkaḥ 3" / "… 8 82"
ATTACHED_PAREN = re.compile(r'\(\s*[^)]*\)(?=\w)|(?<=\w)\([^)]*\)')  # variant
BR_JUNK = re.compile(r'\[[^\]]*[A-Za-z0-9?][^\]]*\]')   # [bodl fol51r] [..?]
BR_MULTI = re.compile(r'(?<=\w)\[[^\]]*\s[^\]]*\]')     # word[multi word var.]

SOURCE_FIXES = [('li"gaṃ', 'liṅgaṃ')]   # ŚDhŚ mis-encoded ṅ


def clean_line(s):
    s = s.strip()
    first = next((c for c in s if c.isalpha()), '')
    if (not s or s.startswith('%') or '\\' in s
            or SIGLA_SLASH.search(s)
            or re.search(r'[A-Z]', s) or (first and first.isupper())
            or re.match(r'^p\.?\s*\d+$', s)
            or re.match(r'^[….]+$', s)):
        return None
    s = s.split('===>')[0]
    for old, new in SOURCE_FIXES:
        s = s.replace(old, new)
    s = s.replace('’', "'")
    s = VERSE_NUM.sub('', s)
    s = TRAIL_NUM.sub('', s)
    s = re.sub(r'\(\s*\?+\s*\)|!', '', s)     # (?) doubt marks, exclamations
    s = BR_JUNK.sub('', s)                    # bracketed folio refs / queries
    s = BR_MULTI.sub('', s)                   # attached multi-word variants
    s = s.replace('[', '').replace(']', '')   # supplied letters: deva[s]
    s = ATTACHED_PAREN.sub('', s)             # attached (variant) readings
    s = s.replace('(', ' ').replace(')', ' ') # standalone parens: keep text
    s = s.replace('|', ' ')
    s = re.sub(r'…+|\.\.+', ' ', s)
    s = re.sub(r"([oe])\.(?=\w)", r"\1 '", s) # elided a-: prathamo.adhyāyaḥ
    s = re.sub(r'[-–]+(\s|$)', r'\1', s)      # editorial compound hyphens
    s = re.sub(r'(?<=\w)[-–](?=\w)', '', s)   # mid-word split: kula-rūpa
    s = re.sub(r'[.,:;_?]', ' ', s)
    s = re.sub(r'\s+\d+(\s|$)', r'\1', s)     # stray bare digits
    s = re.sub(r'\s{2,}', ' ', s).strip()
    return s or None


def main():
    for src, out in UNITS:
        raw = (SRC / src).read_text(encoding='utf-8')
        (DIR / f'{out}.txt.orig').write_text(raw, encoding='utf-8')
        cleaned = [c for c in (clean_line(l) for l in raw.split('\n')) if c]
        (DIR / f'{out}.txt').write_text('\n'.join(cleaned) + '\n', encoding='utf-8')
        print(f'{out}: {len(cleaned)} lines, {sum(len(c.split()) for c in cleaned)} words')


if __name__ == '__main__':
    main()
