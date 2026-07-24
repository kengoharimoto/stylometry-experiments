#!/usr/bin/env python3
"""Extract the large Appendix-I passages of the Harivaṃśa (Vaidya CE) from the
GRETIL appendix file into standalone corpus units.

Source: E-texts/1_sanskr/2_epic/mbh/ext/unknown_harivamsa_appendix_padapatha.txt

Units (mainline appendix text only, its own **-sub-insertions dropped):
  App.I 29-29F + 30   Kṛṣṇa's Mathurā carita additions
  App.I 31            Vaiṣṇava cosmological block (kimarthaṃ bhagavān viṣṇuḥ...)
  App.I 41            Padmanābha sleeping on the ocean
  App.I 42 + 42A-B    prādurbhāva/avatāra block (vulgate Bhaviṣyaparvan core)

File conventions (differ from the main HV file — see clean_harivamsa_ce.py):
  - mainline lines end in a "/ HV_App.I,<sec>.<line> /"-style reference
    (delimiters /, //, |, ||, or @ around the ref); <sec> may have a letter
    suffix (6A, 29F ...).  Even pādas of long metres are indented with THREE
    non-breaking spaces but are mainline text -> kept.
  - **-passages (sub-insertions, refs contain "**") and lines indented with
    five or more NBSPs -> dropped.
  - [h: ... :h] headers, [k: ... :k] apparatus, blanks -> dropped.
  - {interlocutor} lines carry no reference; attached to the passage of the
    NEXT reference line -> kept unwrapped.
Within kept text: "(sic)", "(?)"/"(??)" doubt marks (also inside a word:
"taptaṃ (pyed??)"), "..." lacuna dots and stray "*" are removed.

For each unit writes corpus/epic_puranas/<outname>.txt.orig (raw selected
lines) and <outname>.txt (cleaned).

Usage: python3 extract_harivamsa_appendix.py [<source-file>]
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DIR = REPO / 'corpus' / 'epic_puranas'
DEFAULT_SRC = ('/Users/kengo_1/Documents/E-texts/1_sanskr/2_epic/mbh/ext/'
               'unknown_harivamsa_appendix_padapatha.txt')

UNITS = [
    (re.compile(r'^(29[A-F]?|30)$'), 'harivamsa_appendix-29-30_mathura'),
    (re.compile(r'^31$'),            'harivamsa_appendix-31'),
    (re.compile(r'^41$'),            'harivamsa_appendix-41'),
    (re.compile(r'^42[AB]?$'),       'harivamsa_appendix-42_pradurbhava'),
]

NBSP = '\xa0'
REF = re.compile(r'[/|@]+\s*HV_App\.I,(\d+[A-Z]*)\.\d+\s*[/|@]+\s*$')
DOUBT = re.compile(r'\(\s*[^)]*[?!]+\s*\)|\(sic\)')  # (?) (??) (pyed??) (!) (sic)

SOURCE_FIXES = [                 # typos in the GRETIL source, verified in context
    ('ahaṃkāra7s ca', 'ahaṃkāraś ca'),   # App.I 29
    ('k,rtavarmā', 'kṛtavarmā'),         # App.I 29
]


def clean_text(txt):
    txt = DOUBT.sub('', txt)
    for old, new in SOURCE_FIXES:
        txt = txt.replace(old, new)
    txt = txt.replace('+ +', '')         # compound split across pādas -> join
    txt = re.sub(r'\+\s+', '', txt)      # "tattvārtha+ vicāra..." -> join
    txt = txt.replace('+', '')
    txt = re.sub(r'\.\.+|-{2,}', ' ', txt)   # lacuna dot/dash runs
    txt = re.sub(r'-+(\s|$)', r'\1', txt)    # glide notation "guṇavaty- api"
    txt = txt.replace('*', ' ').replace('(', ' ').replace(')', ' ')
    txt = txt.replace('/', ' ').replace('|', ' ').replace('@', ' ')
    txt = txt.replace(',', ' ')
    return re.sub(r'\s{2,}', ' ', txt).strip()


def main(src):
    lines = open(src, encoding='utf-8').read().split('\n')
    start = next(i for i, l in enumerate(lines)
                 if re.search(r'HV_App\.I,1\.1', l))
    raw = {name: [] for _, name in UNITS}
    out = {name: [] for _, name in UNITS}
    pending = []                        # {interlocutor} lines awaiting a ref
    for l in lines[start:]:
        s = l.rstrip()
        if (not s.strip() or '**' in s or s.startswith(NBSP * 5)
                or s.lstrip(NBSP).startswith(('[h:', '[k:'))
                or '[k:' in s or s == '[Colophon]'):
            continue
        body = s.lstrip(NBSP).strip()
        if body.startswith('{') and body.endswith('}'):
            pending.append(body[1:-1].strip())
            continue
        m = REF.search(body)
        if not m:
            continue                    # no reference -> not mainline text
        sec = m.group(1)
        for rx, name in UNITS:
            if rx.match(sec):
                for sp in pending:
                    raw[name].append('{' + sp + '}')
                    out[name].append(sp)
                raw[name].append(s)
                t = clean_text(REF.sub('', body))
                if t:
                    out[name].append(t)
                break
        pending = []
    for _, name in UNITS:
        (DIR / f'{name}.txt.orig').write_text(
            '\n'.join(raw[name]) + '\n', encoding='utf-8')
        (DIR / f'{name}.txt').write_text(
            '\n'.join(out[name]) + '\n', encoding='utf-8')
        print(f'{name}: {len(out[name])} lines')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC)
