"""
Extract verses-only from skandamahapurana_sutasamhita_khanda-4.txt, dropping the
Mādhavācārya commentary, OCR artifacts, page numbers, and running
headers/footers.

Heuristic: a line ending `|| N ||` is treated as a verse-closer iff it
AND its immediately-preceding non-blank line both look like verse pādas
(short, free of commentary signals). Otherwise the `|| N ||` is the end
of a commentary block and is skipped.

Output: corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4_verses.txt
"""

import re
from pathlib import Path

SRC = Path("corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4.txt")
DST = Path("corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4_verses.txt")

VERSE_CLOSE = re.compile(r"\|\|\s*\d+\s*\|\|\s*$")

# Words/markers that strongly indicate prose commentary
PROSE_MARKERS = re.compile(
    r"(vyākhyā|nigadvyā|ityāha|saṃbandhaḥ|tātparyam|"
    r"ārabhamāṇo|abhipretam|ucyate\b|kathyate|tātparyadīpikā|"
    r"ityarthaḥ|tyarthaḥ\s*\|\||śrīsūtasaṃhitā|"
    r"'?dhyāyaḥ\s*\||iti\s*\|\|)"
)

# Lines that are clearly noise — skipped when walking backward
DIACRITICS = frozenset("āīūṛṝḷṃḥṅñṇṭḍśṣĀĪŪṚṜḶṂḤṄÑṆṬḌŚṢ")

def is_junk_line(line: str) -> bool:
    """Headers, page numbers, OCR garbage — invisible to verse-walk."""
    s = line.strip()
    if not s:
        return True
    # Bare page number
    if s.isdigit():
        return True
    # Single-character lines
    if len(s.replace(" ", "")) <= 1:
        return True
    # Known running headers
    if s in {"sūtasaṃhitā |", "sūtasaṃhitā", '"', '",', "Fr"}:
        return True
    if s.startswith("[ 4 yajñavaibhava") or s.startswith("tātparyadīpikā"):
        return True
    # Mostly ASCII letters (English / OCR garbage)
    letters = [c for c in s if c.isalpha()]
    if letters:
        ascii_ratio = sum(1 for c in letters if c.isascii()) / len(letters)
        if ascii_ratio > 0.8:
            return True
    # Footnote markers like "1 ga. pūveṃ |", "2 adhyāyaḥ ]"
    if re.match(r"^\d+\s+[a-zA-Zḥṛ]{1,4}\.\s", s):
        return True
    # Page-edge labels like "5 adhyāyaḥ ]", "22 adhyāyaḥ ]"
    if re.match(r"^\d+\s+\S+\s*\]\s*$", s):
        return True
    # Chapter colophon fragments
    if "khaṇḍe" in s and "nāma" in s and not s.endswith(("|", "||")):
        return True
    # Bracket-only or punctuation-heavy short lines
    if len(s) < 6 and not any(c in DIACRITICS or c.isalpha() for c in s):
        return True
    return False

def looks_like_pada(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    # Strip trailing verse-number marker for length analysis
    body = VERSE_CLOSE.sub("", s).strip().rstrip("|").strip()
    if len(body) < 8 or len(body) > 75:
        return False
    if '"' in s or '“' in s or '”' in s:
        return False
    if " - " in s or "--" in s:
        return False
    if s.endswith("-"):  # hyphenated continuation = prose wrap
        return False
    if PROSE_MARKERS.search(s):
        return False
    if re.search(r"\biti\s*\|?\s*$", s):
        return False
    if "|| iti ||" in s or "iti ||" in s:
        return False
    # Mid-line single danda is a strong commentary signal
    # (verse pādas place danda only at the end)
    body_no_close = VERSE_CLOSE.sub("", s).rstrip().rstrip("|").rstrip()
    if "|" in body_no_close:
        return False
    return True


def main() -> None:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    n = len(lines)
    out: list[str] = []
    used = [False] * n
    verses_found = 0

    for i, ln in enumerate(lines):
        if not VERSE_CLOSE.search(ln):
            continue
        if not looks_like_pada(ln):
            continue
        # Look at the previous non-junk line — it should also be a pāda
        j = i - 1
        while j >= 0 and is_junk_line(lines[j]):
            j -= 1
        if j < 0 or not looks_like_pada(lines[j]):
            continue
        # Walk back collecting pāda lines until we hit prose or another
        # already-claimed verse closer. Junk lines (headers, page numbers)
        # are transparently skipped.
        block = [i]
        k = j
        while k >= 0:
            if is_junk_line(lines[k]):
                k -= 1
                continue
            if used[k]:
                break
            s = lines[k].strip()
            if VERSE_CLOSE.search(s):
                break
            if not looks_like_pada(s):
                break
            block.append(k)
            k -= 1
        block.reverse()
        for idx in block:
            used[idx] = True
            out.append(lines[idx].rstrip())
        verses_found += 1

    DST.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Source lines : {n}")
    print(f"Verses found : {verses_found}")
    print(f"Output lines : {len(out)}")
    print(f"Wrote        : {DST}")


if __name__ == "__main__":
    main()
