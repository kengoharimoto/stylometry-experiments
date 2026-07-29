"""
repair_kirfel_diacritics.py

Chandra OCR (chandra-ocr-2) erratically drops IAST underdots when reading
Kirfel's Purāṇapañcalakṣaṇa: ~33% of visargas come out as plain "h"
("prabhuh"), vocalic ṛ as "r" ("asrjat"), etc.  Verified against 600-dpi
renders of the print, which has the dots throughout.  This repairs the two
loss classes that are phonotactically decidable from the text alone:

  h -> ḥ   when a vowel precedes and no letter follows (word-final visarga:
           no Sanskrit word ends in plain -h), or a voiceless k/p/s/ś/ṣ
           follows (duḥkha, niḥsvana, āyuḥpravardhana: the clusters hk, hp,
           hs never occur natively).  Genuine h-clusters (brāhmaṇa, jihvā,
           gṛhṇāti) have h before voiced sounds and are untouched.

  r -> ṛ   when neither neighbour is a vowel (asrjat, smrtah, prthvī,
           word-initial rte/rsi): a syllable needs a vowel, so vowel-less
           r can only be vocalic ṛ.  vartma, rāṣṭra, ācārya all keep r.

n -> ṇ (hiranya) needs the ṇatva rule and is left to the re-OCR / vision
pass; residuals are reported so the remaining damage is measurable.

Lines starting with "#" (segmenter comments, German headings) are passed
through untouched.  Files are rewritten in place; git holds the previous
state.

Usage:
  python3 scripts/repair_kirfel_diacritics.py [--dry-run]
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CORPUS = REPO_ROOT / "corpus" / "epic_puranas"

VOWEL = "aāiīuūeoṛṝḷ"                    # ai/au are covered by a/u
LETTER = "a-zāīūṛṝḷṅñṭḍṇśṣḥṃ'’"

# word-final visarga: vowel + h + no following letter
RE_H_FINAL = re.compile(rf"(?<=[{VOWEL}])h(?![{LETTER}])")
# visarga in compounds: vowel + h + voiceless consonant (hk/hp/hs don't exist)
RE_H_VOICELESS = re.compile(rf"(?<=[{VOWEL}])h(?=[kpsśṣ])")
# vocalic ṛ: r with no vowel on either side (start-of-word counts as no vowel)
RE_R_VOCALIC = re.compile(rf"(?<![{VOWEL}])r(?![{VOWEL}])(?=[{LETTER}])")


def repair_line(line: str) -> str:
    if line.lstrip().startswith("#"):
        return line
    line = RE_H_FINAL.sub("ḥ", line)
    line = RE_H_VOICELESS.sub("ḥ", line)
    line = RE_R_VOCALIC.sub("ṛ", line)
    return line


def residuals(text: str) -> dict:
    """Damage indicators that should be ~0 after repair (h) or are known
    to remain (n->ṇ is not repaired here)."""
    body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
    return {
        "plain-h-final": len(re.findall(rf"[{VOWEL}]h(?![{LETTER}])", body)),
        "hiranya-like": len(re.findall(r"hiranya|brahmān", body)),
    }


SELF_TESTS = [
    # visarga
    ("prabhuh, |", "prabhuḥ, |"),
    ("tayoh śakalayor", "tayoḥ śakalayor"),
    ("nah śrutaṃ", "naḥ śrutaṃ"),
    ("svargyam āyuhpravardhanaṃ |", "svargyam āyuḥpravardhanaṃ |"),
    ("duhkhaṃ", "duḥkhaṃ"),
    # genuine h untouched
    ("brāhmaṇā hi jihvā gṛhṇāti", "brāhmaṇā hi jihvā gṛhṇāti"),
    ("saha tena mahātmanā", "saha tena mahātmanā"),
    # vocalic ṛ
    ("ākāśam asrjat prabhuh", "ākāśam asṛjat prabhuḥ"),
    ("smrtah. || 11 ||", "smṛtaḥ. || 11 ||"),
    ("apsu pāriplavāṃ prthvīṃ", "apsu pāriplavāṃ pṛthvīṃ"),
    ("rte tu devān rsayaś ca", "ṛte tu devān ṛsayaś ca"),  # ṣ-restoration is out of scope
    ("nirrtir", "nirṛtir"),
    # genuine r untouched
    ("vartate rājā mantriṇā, ācāryas tatra rāṣṭre", "vartate rājā mantriṇā, ācāryas tatra rāṣṭre"),
    ("punar eva, pitur vacaḥ", "punar eva, pitur vacaḥ"),
    ("sarva-dharma", "sarva-dharma"),
    # already-correct text is a fixed point
    ("tayoḥ śakalayor madhya ākāśam asṛjat prabhuḥ, |",
     "tayoḥ śakalayor madhya ākāśam asṛjat prabhuḥ, |"),
    # comment lines untouched (German "auch" etc.)
    ("# Abschnitt. Sarga und Pratisarga, auch hier", "# Abschnitt. Sarga und Pratisarga, auch hier"),
]


def run_self_tests() -> None:
    bad = [(i, o, repair_line(i)) for i, o in SELF_TESTS if repair_line(i) != o]
    for i, want, got in bad:
        print(f"SELF-TEST FAIL:\n  in:   {i!r}\n  want: {want!r}\n  got:  {got!r}")
    if bad:
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="Report changes without writing files.")
    args = ap.parse_args()

    run_self_tests()

    for path in sorted(CORPUS.glob("kirfel_*.txt")):
        text = path.read_text(encoding="utf-8")
        before = residuals(text)
        repaired = "\n".join(repair_line(l) for l in text.splitlines())
        if text.endswith("\n"):
            repaired += "\n"
        after = residuals(repaired)
        nchanged = sum(1 for a, b in zip(text.splitlines(), repaired.splitlines())
                       if a != b)
        print(f"{path.name}: {nchanged} lines changed; "
              f"plain-h {before['plain-h-final']} -> {after['plain-h-final']}; "
              f"hiranya-like remaining {after['hiranya-like']}")
        if not args.dry_run:
            path.write_text(repaired, encoding="utf-8")


if __name__ == "__main__":
    main()
