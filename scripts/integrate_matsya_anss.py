#!/usr/bin/env python3
"""Integrate the ĀnSS-OCR-supplied Matsyapurāṇa chapters into the corpus.

Merges the Matsyapurāṇa into a single complete file
    matsyapurana_pu.txt   (adhyāyas 1-291)
from three sources:
    chs 1-175           GRETIL (matsyapurana_adhyaya-1-176_pu.txt, whose
                        ch 176 is truncated and therefore dropped)
    chs 177-291         web e-text via matsyapurana_adhyaya-177-291_pu.txt
                        (chs 277 & 284 missing there)
    chs 176, 277, 284   Chandra OCR of ĀnSS 54 (see
                        /mnt2/kengo/ocr-matsya/assemble_chapters.py);
                        expect isolated OCR misreadings there at a rate a
                        couple of orders above the typed text.

Unlike the Bhāgavata's skandha files, the Matsya has no analysis-motivated
subdivision, so it is kept as ONE text unit; the source seams (175/176 and
the three OCR chapters) are documentation-level facts, not file boundaries.
Seam safety for char-3-gram features is verified by
scripts/sanity_check_matsya_seam.py (chance-level source classification
after nasal+ortho+space normalization).

The old split .txt files are removed (the GRETIL .orig backup is kept);
derived corpora must be rebuilt afterwards:
    python3 scripts/build_epic_puranas_sandhied.py matsyapurana_pu.txt --force
    scripts/unsandhi_local.sh matsyapurana_pu.txt --force

Usage: python3 scripts/integrate_matsya_anss.py
"""
import re
from pathlib import Path

CORPUS = Path(__file__).parent.parent / 'corpus' / 'epic_puranas'
# GRETIL source: the pre-integration file if present, else its .orig backup
GRETIL = CORPUS / 'matsyapurana_adhyaya-1-176_pu.txt'
WEB = CORPUS / 'matsyapurana_adhyaya-177-291_pu.txt'
ANSS = Path('/mnt2/kengo/ocr-matsya/chapters_iast.txt')
OUT = CORPUS / 'matsyapurana_pu.txt'
# transitional names from the first (two-file) integration run
OLD_SPLIT = [CORPUS / 'matsyapurana_adhyaya-1-175_pu.txt',
             CORPUS / 'matsyapurana_adhyaya-176-291_pu.txt']


def split_chapters(text):
    return {
        int(m.group(1)): m.group(0).strip()
        for m in re.finditer(
            r'Matsya-Purāṇa (\d+)\n.*?(?=Matsya-Purāṇa \d+\n|\Z)', text, re.S)
    }


def main():
    gret_path = GRETIL if GRETIL.exists() else OLD_SPLIT[0]
    web_path = WEB if WEB.exists() else OLD_SPLIT[1]
    gret = split_chapters(gret_path.read_text(encoding='utf-8'))
    web = split_chapters(web_path.read_text(encoding='utf-8'))
    anss = split_chapters(ANSS.read_text(encoding='utf-8'))
    assert set(anss) >= {176, 277, 284}, sorted(anss)

    merged = {n: gret[n] for n in range(1, 176)}
    merged.update({n: web[n] for n in web if n >= 177})
    for n in (176, 277, 284):
        merged.setdefault(n, anss[n])
    assert sorted(merged) == list(range(1, 292)), sorted(merged)
    OUT.write_text(
        '\n\n\n'.join(merged[n] for n in sorted(merged)) + '\n',
        encoding='utf-8')

    for p in [GRETIL, WEB, *OLD_SPLIT]:
        if p.exists():
            p.unlink()
    print(f'wrote {OUT.name} ({len(merged)} chapters, '
          f'176/277/284 from ĀnSS OCR)')


if __name__ == '__main__':
    main()
