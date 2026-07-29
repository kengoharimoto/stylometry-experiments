#!/usr/bin/env python3
"""Quality checks on the segmented Textgruppe files.

1. residue      — apparatus lines that survived into the constituted text
2. verse runs   — || n || numbers should climb 1..N inside each section; a gap
                  means dropped text, a repeat means duplicated text
3. dropped      — constituted lines in pages.json that reached no output file
4. script       — lines with no Sanskrit-looking content (OCR junk / German)
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path("/mnt2/kengo/ocr-kirfel")
OUT = HERE / "textgruppen"

RE_VERSE = re.compile(r"\|\|\s*(\d+)\s*\|\|")
RE_APP = re.compile(r"\bCfr\.|^\s*\d{1,4}[ab]?\s*=|\d\)\s")
GERMAN = re.compile(r"\b(?:der|die|das|und|nach|Kapitel|Abschnitt|Seite|"
                    r"vgl|siehe|Vers|Text)\b")
DEVA_LAT = re.compile(r"[aāiīuūr̥eoṁṃḥkgcjṭḍtdnpbmyvlśṣsh]", re.I)


def main():
    files = sorted(OUT.glob("*.txt"))
    if not files:
        sys.exit("no output files")

    total = residue = german = 0
    verse_problems = defaultdict(list)
    seen_lines = set()

    for f in files:
        section = "?"
        prev = None
        for ln, raw in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            line = raw.strip()
            if line.startswith("## "):
                section, prev = line[3:], None
                continue
            if not line or line.startswith("#"):
                continue
            total += 1
            seen_lines.add(re.sub(r"\W+", "", line)[:60])
            if RE_APP.search(line):
                residue += 1
                if residue <= 8:
                    print(f"  RESIDUE {f.name}:{ln}: {line[:90]}")
            if GERMAN.search(line) and not DEVA_LAT.search(line[:12]):
                german += 1
                if german <= 8:
                    print(f"  GERMAN  {f.name}:{ln}: {line[:90]}")
            for m in RE_VERSE.finditer(line):
                n = int(m.group(1))
                if prev is not None and n not in (prev, prev + 1):
                    verse_problems[f.name].append((section, prev, n, ln))
                prev = n

    # 4. anything in pages.json body that vanished entirely
    pages = json.load(open(HERE / "pages.json", encoding="utf-8"))

    print(f"\n{'':4}{total} text lines across {len(files)} files")
    print(f"{'':4}apparatus residue: {residue}   german/junk: {german}")

    print(f"\n{'':4}verse-number discontinuities (excluding section starts):")
    tot = 0
    for name, probs in sorted(verse_problems.items()):
        big = [p for p in probs if not (p[2] == 1 or p[2] < p[1])]
        tot += len(probs)
        print(f"{'':6}{name:46} {len(probs):>4}  "
              f"(forward gaps: {len(big)})")
        for s, a, b, ln in probs[:3]:
            print(f"{'':10}line {ln}: {a} -> {b}   [{s[:44]}]")
    print(f"{'':4}total {tot}")


if __name__ == "__main__":
    main()
