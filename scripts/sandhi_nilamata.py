#!/usr/bin/env python3
"""Apply external sandhi to the Nilamatapurana source (one-off fix, 2026-07-09).

The nilamatapurana_au source came with sandhi editorially dissolved: '+' marks
each junction where sandhi applies, '&' marks pada boundaries, and words stand in
pausa form (final s for etymological s/visarga) — i.e. exactly the apply_sandhi.py
convention. Every other text in corpus/epic_puranas is ordinary sandhied surface
text, so the dissolved Nilamata distorted both analysis branches:

  - C3 (sandhied char 3-grams): huge raw-cosine outlier — the dissolution
    reallocates precisely the top-frequency space-adjacent trigrams.
  - W1 (unsandhied): the segmentation model, fed already-dissolved input, passed
    through pausa -s forms it normally emits as -h (tatas/tatah split etc.).
  - BOTH: pausa spelling (m for m-anusvara, s for visarga) removes diacritics, so
    is_skip_line()'s >85%-ASCII English detector silently dropped 795 of 2241
    genuine lines (1446 survived).

Fix: run apply_sandhi over the '+'-marked source and let the standard pipelines
(build_epic_puranas_sandhied.py; unsandhi via process_epic_puranas_unsandhied_local
on the GPU box) regenerate both corpus versions from the result.

The '+'-marked input this was run on is the version of
corpus/epic_puranas/nilamatapurana_au.txt at commit 03a7046 and earlier
(corpus/epic_puranas/nilamatapurana_au.txt.orig is the untouched raw original).

Usage: python3 scripts/sandhi_nilamata.py INPUT OUTPUT
"""
import sys

sys.path.insert(0, '/Users/kengo_1/Documents/E-texts/40_tools/scripts')
from apply_sandhi import apply_sandhi

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding='utf-8') as f:
        lines = f.read().splitlines()
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(apply_sandhi(l) for l in lines) + '\n')
