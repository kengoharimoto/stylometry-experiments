#!/usr/bin/env python3
"""E1 apparatus experiment: build augmented units (constituted text + the
CE-excluded star passages and Appendix I material present in the GRETIL
e-text) and apparatus-only units, for MBh 15-18 and the MBh 13 control.

Sources: corpus/epic_puranas/mahabharata_XX.txt        (constituted, cleaned)
         corpus/epic_puranas/mahabharata_XX.txt.orig   ("id<TAB>text" raw;
         lines whose id contains '*' or '@' are the apparatus)
Apparatus lines are cleaned with extract_mbh_appendix.clean_text.

Outputs (source level, for the ByT5 pass, and sandhied level via
build_epic_puranas_sandhied.clean_line):
  corpus/e1_apparatus_src/mahabharata_XX_{augmented,apparatus}.txt
  corpus/e1_apparatus_sandhied/...
"""
import sys
from pathlib import Path

ROOT = Path('/mnt/kengo/stylometry-experiments')
sys.path.insert(0, str(ROOT / 'scripts'))
from extract_mbh_appendix import clean_text                        # noqa: E402
from build_epic_puranas_sandhied import clean_line                 # noqa: E402
from process_epic_puranas_unsandhied_local import skip_test_for    # noqa: E402

DIR = ROOT / 'corpus/epic_puranas'
OUT_SRC = ROOT / 'corpus/e1_apparatus_src'
OUT_SAN = ROOT / 'corpus/e1_apparatus_sandhied'
OUT_SRC.mkdir(exist_ok=True)
OUT_SAN.mkdir(exist_ok=True)

PARVANS = ['15-asramavasikaparvan', '16-mausalaparvan',
           '17-mahaprasthanikaparvan', '18-svargarohanaparvan',
           '13-anusasanaparvan']

print(f'{"parvan":<28}{"const words":>12}{"appar words":>12}{"growth":>8}')
for p in PARVANS:
    const = [l for l in (DIR / f'mahabharata_{p}.txt')
             .read_text(encoding='utf-8').splitlines() if l.strip()]
    appar = []
    for line in (DIR / f'mahabharata_{p}.txt.orig').open(encoding='utf-8'):
        line = line.rstrip('\n')
        if '\t' not in line:
            continue
        idp, txt = line.split('\t', 1)
        if '*' in idp or '@' in idp:
            t = clean_text(txt)
            if t:
                appar.append(t)
    name = f'mahabharata_{p.split("-")[0]}'
    units = {f'{name}_augmented': const + appar, f'{name}_apparatus': appar}
    skip = skip_test_for(f'mahabharata_{p}.txt')
    for uname, lines in units.items():
        (OUT_SRC / f'{uname}.txt').write_text('\n'.join(lines) + '\n',
                                              encoding='utf-8')
        san = [c for c in (clean_line(l, skip) for l in lines) if c]
        (OUT_SAN / f'{uname}.txt').write_text('\n'.join(san) + '\n',
                                              encoding='utf-8')
    wc_ = sum(len(l.split()) for l in const)
    wa = sum(len(l.split()) for l in appar)
    print(f'{p:<28}{wc_:>12}{wa:>12}{wa/wc_:>8.0%}')
