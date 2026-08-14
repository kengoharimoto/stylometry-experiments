#!/usr/bin/env python3
"""Vamsa genre control: split each panel text's lines into genealogy-like
(gen) vs the rest, at the sandhied and source levels.

A line is genealogy-like if it or an adjacent line matches the marker stems
(putr, vams, jajn, ajayat, janaya, dayada, apatya, anvavaya, duhit,
manvantara, ...). The +-1 smoothing captures the contiguous list blocks that
carry no marker on every line. Source-level lines are mapped through
clean_line -> cstream as in the complements pipeline.
"""
import re
import sys
from pathlib import Path

ROOT = Path('/mnt/kengo/stylometry-experiments')
sys.path.insert(0, str(ROOT / 'scripts'))
from build_epic_puranas_sandhied import clean_line                 # noqa: E402
from process_epic_puranas_unsandhied_local import skip_test_for    # noqa: E402

PAT = re.compile(r'putr|sūnu|jajñ|ajāyat|janayā|ajanay|vaṃś|dāyād|apaty'
                 r'|anvavāy|duhit|prajajñ|jāyata|janiṣy|manvantar', re.I)
PANEL = ['mahabharata_01-adiparvan', 'harivamsa', 'matsyapurana_pu',
         'markandeyapurana', 'brahmapurana_pu', 'agnipurana_u',
         'bhavisyapurana', 'garudapurana_khanda-1_u',
         'bhagavatapurana_skandha-09_u', 'kurmapurana_khanda-1_u',
         'padmapurana_a',
         'vayupurana_08_manu-candra-vishnu-vamsha_iast',
         'vayupurana_06_prthu-and-prajapati-lineages_iast']

KEEP = set("abcdefghijklmnopqrstuvwxyzāīūṛṝḷḹṃḥśṣṇṭḍṅñ'")
def cstream(s):
    return ''.join(c for c in s.lower() if c in KEEP).replace("'", '')

SAN = ROOT / 'corpus/epic_puranas_sandhied'
SRC = ROOT / 'corpus/epic_puranas'
OUT_SAN = ROOT / 'corpus/genre_control_sandhied'
OUT_SRC = ROOT / 'corpus/genre_control_src'
OUT_SAN.mkdir(exist_ok=True)
OUT_SRC.mkdir(exist_ok=True)

print(f'{"unit":<48}{"gen words":>10}{"rest words":>11}')
for u in PANEL:
    lines = (SAN / f'{u}.txt').read_text(encoding='utf-8').splitlines()
    hit = [bool(PAT.search(l)) for l in lines]
    sm = [hit[i] or (i > 0 and hit[i - 1]) or (i + 1 < len(hit) and hit[i + 1])
          for i in range(len(lines))]
    cls = {}          # cstream -> True(gen)/False(rest); gen wins on conflict
    for l, s in zip(lines, sm):
        cs = cstream(l)
        cls[cs] = cls.get(cs, False) or s
    parts = {'gen': [l for l, s in zip(lines, sm) if s],
             'rest': [l for l, s in zip(lines, sm) if not s]}
    for k, ls in parts.items():
        (OUT_SAN / f'{u}_{k}.txt').write_text('\n'.join(ls) + '\n', encoding='utf-8')

    skip = skip_test_for(f'{u}.txt')
    sparts = {'gen': [], 'rest': []}
    unmapped = 0
    for l in (SRC / f'{u}.txt').read_text(encoding='utf-8').splitlines():
        c = clean_line(l, skip)
        if c is None:
            unmapped += 1
            continue
        b = cls.get(cstream(c))
        if b is None:
            unmapped += 1
            continue
        sparts['gen' if b else 'rest'].append(l)
    for k, ls in sparts.items():
        (OUT_SRC / f'{u}_{k}.txt').write_text('\n'.join(ls) + '\n', encoding='utf-8')
    print(f'{u:<48}'
          f'{sum(len(l.split()) for l in parts["gen"]):>10}'
          f'{sum(len(l.split()) for l in parts["rest"]):>11}'
          + (f'   ({unmapped} src lines unmapped)' if unmapped > 20 else ''))
