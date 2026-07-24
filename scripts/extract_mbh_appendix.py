#!/usr/bin/env python3
"""Extract large coherent Appendix-I passages from the Pune CE Mahābhārata
GRETIL files (the corpus mahabharata_*.txt.orig backups, "line-id<TAB>text")
into standalone corpus units.

clean_mahabharata_ce.py dropped every '@' appendix line from the parvan files;
here we recover the big coherent appendix texts as their own units — they are
the philologically documented "late integration" stratum:

  MBh  2 App.21     Śiśupāla episode expansion (after 2.35)
  MBh  7 App.8      Vyāsa consoles Yudhiṣṭhira / Ṣoḍaśarājika context (7.49)
  MBh 12 App.29A-E  Sāṃkhya-mokṣa supplements, all inserted at 12.308.191
                    (taken together as one unit)
  MBh 13 App.15     Umā-Maheśvara-saṃvāda (after 13.134)
  MBh 14 App.4      Vaiṣṇavadharma (after 14.96)

For each unit we write:
  corpus/epic_puranas/<outname>.txt.orig  raw selected "id<TAB>text" lines
  corpus/epic_puranas/<outname>.txt       cleaned text, one pāda-line per line

Text cleaning follows clean_mahabharata_ce.py, extended for marks that occur
in appendix passages: "(sic)", "[*]", editor's doubt "[?...]", variant
readings attached to a word "dharmaṃ[rmaḥ]" (dropped), supplied standalone
words "[prārthitaṃ]" (unwrapped), and prose daṇḍas "|".

Usage: python3 extract_mbh_appendix.py        (from anywhere; paths are fixed)
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DIR = REPO / 'corpus' / 'epic_puranas'

# (orig file, appendix-id regex applied to the line-id, output basename)
UNITS = [
    ('mahabharata_02-sabhaparvan.txt.orig',        r'@021_',
     'mahabharata_02-appendix-21_sisupala'),
    ('mahabharata_07-dronaparvan.txt.orig',        r'@008_',
     'mahabharata_07-appendix-08_sodasarajika'),
    ('mahabharata_12-santiparvan.txt.orig',        r'@029[A-E]_',
     'mahabharata_12-appendix-29_moksadharma'),
    ('mahabharata_13-anusasanaparvan.txt.orig',    r'@015_',
     'mahabharata_13-appendix-15_umamahesvara'),
    ('mahabharata_14-asvamedhikaparvan.txt.orig',  r'@004_',
     'mahabharata_14-appendix-04_vaisnavadharma'),
]

ENUM_BR   = re.compile(r'\[[\d_]+\]')      # [1], [6_116] enumeration numbers
QUERY_BR  = re.compile(r'\[\?[^\]]*\]')    # editor's doubt  cū[?dū]raṃ
VAR_BR    = re.compile(r'(?<=\S)\[[^\]]*\]')  # attached variant  dharmaṃ[rmaḥ]
SUPPLIED  = re.compile(r'\[([^\]]*)\]')    # standalone supplied word -> unwrap
PARN_FN   = re.compile(r'\((?:\d+|sic|\?+)\)')  # (n) / (sic) / (?) markers


def clean_text(txt):
    if not any(c.isalpha() for c in txt):
        return ''                        # "++++" / "*****" lacuna rows
    txt = ENUM_BR.sub('', txt)
    txt = txt.replace('[*]', '')
    txt = QUERY_BR.sub('', txt)
    txt = VAR_BR.sub('', txt)
    txt = SUPPLIED.sub(r'\1', txt)
    txt = PARN_FN.sub('', txt)
    txt = txt.replace('|', ' ').replace('/', ' ').replace(',', ' ')
    txt = txt.replace('*', ' ').replace('+', ' ')
    txt = re.sub(r'-+(\s|$)', r'\1', txt)   # trailing compound-break hyphens
    return re.sub(r'\s{2,}', ' ', txt).strip()


def main():
    for orig, pat, outname in UNITS:
        rx = re.compile(pat)
        raw, cleaned = [], []
        for line in (DIR / orig).open(encoding='utf-8'):
            line = line.rstrip('\n')
            if '\t' not in line:
                continue
            idp, txt = line.split('\t', 1)
            if not rx.search(idp):
                continue
            raw.append(line)
            t = clean_text(txt)
            if t:
                cleaned.append(t)
        (DIR / f'{outname}.txt.orig').write_text('\n'.join(raw) + '\n', encoding='utf-8')
        (DIR / f'{outname}.txt').write_text('\n'.join(cleaned) + '\n', encoding='utf-8')
        print(f'{outname}: {len(raw)} raw -> {len(cleaned)} cleaned lines')


if __name__ == '__main__':
    main()
