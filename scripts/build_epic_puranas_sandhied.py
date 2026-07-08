"""
build_epic_puranas_sandhied.py

Produce CLEAN, still-SANDHIED versions of the epic_puranas texts for character
n-gram analysis, in a separate directory. This does NOT run the unsandhi model and
does NOT split words -- sandhi is preserved exactly as in the source. It only
removes the editorial furniture that pollutes the text, reusing the same, already
validated cleaning primitives as the unsandhied pipeline so both corpora select the
same lines:

  - is_skip_line()      -- drop front matter, tables, English, separator rows
  - strip_ref_markers() -- remove letter-sigil reference tags (/AP_.../, //ViP_.../),
                           verse-number digits, nilamata "+"/"&" separators, and
                           lacuna dash-runs ("-- --")
  - has_sanskrit()      -- keep only lines that still hold real Sanskrit content

On top of that, a per-token whitelist keeps only letters and the avagraha ("'"/"’"),
which:
  - strips daṇḍas ("/ | । ॥") and any residual punctuation,
  - joins compound-boundary hyphens ("vakṣaḥ-kṣetra" -> "vakṣaḥkṣetra"),
  - drops leading verse-reference residue ("1.001.001a" -> "a" -> dropped),
  - drops uppercase-initial tokens -- running-header/title fragments
    ("Matsya-Purāṇa") and stray model/tag caps -- while KEEPING Harvard-Kyoto
    Sanskrit words, which start lowercase ("maGgala"=maṅgala, "pitR"=pitṛ).

Output: corpus/epic_puranas_sandhied/<name>.txt, one cleaned line per surviving
source line (verse structure preserved). Source corpus/epic_puranas/ and
corpus/epic_puranas_unsandhied/ are never touched.

Fast (no GPU, no model). Resumable: existing output files are skipped unless --force.

Usage:
  python3 scripts/build_epic_puranas_sandhied.py [basenames…] [--force]
"""

import argparse
import sys
from pathlib import Path

# Reuse the vetted cleaning primitives from the unsandhied pipeline. That module's
# heavy deps (ctranslate2/transformers) are imported lazily inside its main(), so a
# top-level import here stays light.
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from process_epic_puranas_unsandhied_local import (  # noqa: E402
    is_skip_line,
    strip_ref_markers,
    has_sanskrit,
)

REPO_ROOT  = SCRIPT_DIR.parent
INPUT_DIR  = REPO_ROOT / "corpus" / "epic_puranas"
OUTPUT_DIR = REPO_ROOT / "corpus" / "epic_puranas_sandhied"

# Characters kept inside a token: any Unicode letter (preserves all IAST diacritics
# and Harvard-Kyoto capitals) plus the avagraha (sandhi-elision mark).
_AVAGRAHA = "'’"


def clean_token(tok: str) -> str | None:
    """Whitelist a token to letters + avagraha; return None if it should be dropped."""
    w = "".join(c for c in tok if c.isalpha() or c in _AVAGRAHA)
    first_alpha = next((c for c in w if c.isalpha()), "")
    if not first_alpha:
        return None                     # punctuation-only (daṇḍa, stray marks)
    if first_alpha.isupper():
        return None                     # header/title fragment or model/tag caps
    if len(w) == 1 and w.isascii():
        return None                     # leading verse-ref residue ("a", "o", …)
    return w


def clean_line(line: str) -> str | None:
    """Return the cleaned sandhied line, or None if nothing usable remains."""
    if is_skip_line(line):
        return None
    s = strip_ref_markers(line)
    out = []
    for tok in s.split():
        w = clean_token(tok)
        if w:
            out.append(w)
    if not out:
        return None
    joined = " ".join(out)
    return joined if has_sanskrit(joined) else None


def process_file(input_path: Path, output_path: Path) -> tuple[int, int]:
    lines = input_path.read_text(encoding="utf-8").splitlines()
    kept = [c for c in (clean_line(l) for l in lines) if c is not None]
    output_path.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    return len(lines), len(kept)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", help="Restrict to these basenames (default: all).")
    ap.add_argument("--force", action="store_true",
                    help="Rebuild even if an output file already exists.")
    args = ap.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    input_files = sorted(
        p for p in INPUT_DIR.glob("*.txt") if not p.name.endswith(".orig")
    )
    if args.files:
        wanted = set(args.files)
        input_files = [p for p in input_files if p.name in wanted]

    total = len(input_files)
    print(f"Input : {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Files : {total}  (force={args.force})\n")

    for idx, input_path in enumerate(input_files, 1):
        output_path = OUTPUT_DIR / input_path.name
        if output_path.exists() and not args.force:
            print(f"[{idx:3}/{total}] SKIP  {input_path.name}")
            continue
        n_in, n_out = process_file(input_path, output_path)
        print(f"[{idx:3}/{total}] {input_path.name}  ({n_in} → {n_out} lines)")

    print("\nDone.")


if __name__ == "__main__":
    main()
