#!/usr/bin/env python3
"""Partition the source-level shared halves by the family classes assigned at
the sandhied level (attribution via clean_line -> cstream, the same mapping
build_noreuse_corpus.py used for its source-level output)."""
import sys
from pathlib import Path

ROOT = Path('/mnt/kengo/stylometry-experiments')
sys.path.insert(0, str(ROOT / 'scripts'))
from build_epic_puranas_sandhied import clean_line                 # noqa: E402
from process_epic_puranas_unsandhied_local import skip_test_for    # noqa: E402

HERE = Path(__file__).parent
SAN = ROOT / 'corpus/complements_sandhied'
SRC = ROOT / 'corpus/complements_src'

KEEP = set("abcdefghijklmnopqrstuvwxyzāīūṛṝḷḹṃḥśṣṇṭḍṅñ'")
def cstream(s):
    return ''.join(c for c in s.lower() if c in KEEP).replace("'", '')

UNITS = [p.name[:-len('_shared.txt')] for p in sorted(SRC.glob('*_shared.txt'))
         if not any(p.name.endswith(f'_shared_{b}.txt') for b in ('ppl', 'vayubd', 'other'))]

print(f'{"unit":<48}{"ppl":>8}{"vayubd":>8}{"other":>8}{"unmapped":>9}  (src words)')
for u in UNITS:
    cls = {}
    for b in ('ppl', 'vayubd', 'other'):
        for l in (SAN / f'{u}_shared_{b}.txt').read_text(encoding='utf-8').splitlines():
            cls[cstream(l)] = b
    skip = skip_test_for(f'{u}.txt')
    out = {b: [] for b in ('ppl', 'vayubd', 'other')}
    unmapped = 0
    for l in (SRC / f'{u}_shared.txt').read_text(encoding='utf-8').splitlines():
        c = clean_line(l, skip)
        b = cls.get(cstream(c)) if c is not None else None
        if b is None:
            unmapped += 1
            continue
        out[b].append(l)
    for b, lines in out.items():
        (SRC / f'{u}_shared_{b}.txt').write_text(
            '\n'.join(lines) + ('\n' if lines else ''), encoding='utf-8')
    w = {b: sum(len(l.split()) for l in ls) for b, ls in out.items()}
    print(f'{u:<48}{w["ppl"]:>8}{w["vayubd"]:>8}{w["other"]:>8}{unmapped:>9}')
