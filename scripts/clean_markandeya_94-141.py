#!/usr/bin/env python3
"""Build corpus/epic_puranas/markandeyapurana_adhyaya-94-141_u.txt from the raw
per-chapter mkp/*.mix.txt files (E-texts/10_sources_raw/sources_puranas/mkp).

Covers B-edition chapters 94-141 (= N 91-134; 141 is the B appendix carrying
N 134.40-42), i.e. everything after the Devīmāhātmya, which the existing
GRETIL-derived markandeyapurana_adhyaya-1-93_u.txt already ends with.

Source format: verse lines prefixed '#' (B edition) and '=' (N edition), with
'+' sandhi-dissolution junctions, '&' pāda separators, '-' compound splits,
'\\speaker' tags and TeX apparatus lines ('\\var', '$\\emend...'). Per the
corpus decision the N line is followed; mark137 (single-edition, unprefixed)
supplies its text as-is; mark117 is an empty placeholder (no such chapter in
the Bib.Ind. edition) and is skipped.

Output: cleaned, still-sandhied verse-per-line text (sandhi restored from the
'+' markers via apply_sandhi), ready for build_epic_puranas_sandhied.py and the
unsandhi pipeline like any other base-corpus file.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, '/Users/kengo_1/Documents/E-texts/40_tools/scripts')
from apply_sandhi import apply_sandhi

SRC = Path('/Users/kengo_1/Documents/E-texts/10_sources_raw/sources_puranas/mkp')
OUT = Path(__file__).resolve().parents[1] / 'corpus/epic_puranas/markandeyapurana_adhyaya-94-141_u.txt'

APPARATUS = re.compile(r'^\s*(\\var|\{\\rm|\$?\\emend|\$?\\conj|\$)')


def clean_line(line: str) -> str:
    line = line.replace('R̥', 'ṛ').replace('r̥', 'ṛ')
    line = re.sub(r'\\pag\{[^}]*\}', '', line)
    line = re.sub(r'\\[a-zA-Z]+', ' ', line)   # tag words: \speaker \col \wit \iti
    line = re.sub(r'[{}"$]', '', line)
    # compound-split hyphens: rejoin (sandhied corpus keeps compounds solid)
    line = re.sub(r'(?<=\S)-(?=\S)', '', line)
    line = re.sub(r'\s+', ' ', line).strip()
    line = apply_sandhi(line).strip()
    # apply_sandhi writes e/o + a- as "o 'a" (avagraha + retained vowel);
    # printed editions elide: "o '". Normalize so C3 trigrams match the
    # edition-derived corpus convention.
    return re.sub(r"'a", "'", line)


def chapter_lines(path: Path) -> list[str]:
    raw = path.read_text(encoding='utf-8').splitlines()
    body = [l for l in raw if l.strip() and not l.startswith('%')]
    eq = [l[1:] for l in body if l.startswith('=')]
    if eq:                      # paired B/N text: follow the N line
        text = eq
    else:                       # single-edition chapter (mark137)
        text = [l for l in body if not l.startswith('#') and not APPARATUS.match(l)]
    out = []
    for l in text:
        if APPARATUS.match(l):
            continue
        c = clean_line(l)
        if sum(ch.isalpha() for ch in c) >= 2:
            out.append(c)
    return out


def main():
    files = sorted(SRC.glob('mark*.mix.txt'))
    files = [f for f in files if (m := re.match(r'mark(\d+)', f.name))
             and 94 <= int(m.group(1)) <= 141 and f.name != 'mark117.mix.txt']
    all_lines = []
    for f in files:
        lines = chapter_lines(f)
        print(f'{f.name}: {len(lines)} lines')
        all_lines.extend(lines)
    OUT.write_text('\n'.join(all_lines) + '\n', encoding='utf-8')
    words = sum(len(l.split()) for l in all_lines)
    print(f'\nwrote {OUT}  ({len(all_lines)} lines, ~{words} words)')


if __name__ == '__main__':
    main()
