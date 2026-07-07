"""
process_gi_unsandhied.py

Batch-processes all .txt files in corpus/gi/ through the Dharmamitra API
(mode='unsandhied') and writes plain word-only output to corpus/gi_unsandhied/.

Output: one file per input, containing only the unsandhied word tokens
        separated by spaces — no punctuation, no structure, no metadata.

Resumable: already-completed output files are skipped.
"""

import json
import re
import sys
import time
import os
from pathlib import Path

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
REPO_ROOT   = SCRIPT_DIR.parent
INPUT_DIR   = REPO_ROOT / "corpus" / "gi"
OUTPUT_DIR  = REPO_ROOT / "corpus" / "gi_unsandhied"

# ── API ───────────────────────────────────────────────────────────────────────
API_URL     = "https://dharmamitra.org/api/tagging/"
API_HEADERS = {
    "Accept": "*/*",
    "Authorization": "Basic b2xkc3R1ZGVudDpiZWhhcHB5",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}
BATCH_SIZE  = 50
RETRY_LIMIT = 5
RETRY_DELAY = 10   # seconds between retries

# ── Helpers ───────────────────────────────────────────────────────────────────

# IAST diacritic characters
_DIACRITICS = frozenset('āīūṛṝḷṃḥṅñṇṭḍśṣĀĪŪṚṜḶṂḤṄÑṆṬḌŚṢ')

_NON_SANSK_RE = re.compile(
    r'^\\[A-Za-z]'            # GRETIL editorial tags like \Eb, \Ef
    r'|^[=_\-]{3,}'           # separator lines (===, ___, ---)
    r'|^https?://'            # URLs
    r'|^http://'
)

def is_skip_line(line: str) -> bool:
    """Return True for lines that should not be sent to the API."""
    s = line.strip()
    if not s:
        return True
    if _NON_SANSK_RE.search(s):
        return True
    # Single-character lines: isolated diacritics from GRETIL encoding tables
    non_space = s.replace(' ', '')
    if len(non_space) <= 1:
        return True
    # Lines composed mainly of ASCII letters (English prose, headers)
    ascii_letters = sum(1 for c in s if c.isascii() and c.isalpha())
    total_letters = sum(1 for c in s if c.isalpha())
    if total_letters > 0 and ascii_letters / total_letters > 0.85:
        return True
    # Lines with no diacritics AND fewer than 4 words (short Latin-only labels
    # from encoding tables like "long a", "vocalic r", "retroflex t")
    has_diacritic = any(c in _DIACRITICS for c in s)
    if not has_diacritic and len(s.split()) < 4:
        return True
    return False


def call_api(texts: list[str]) -> list[str]:
    """Call Dharmamitra tagging API; return list of '_'-separated word strings."""
    payload = {
        "texts": texts,
        "mode": "unsandhied",
        "input_encoding": "iast",
        "human_readable_tags": True,
    }
    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            resp = requests.post(
                API_URL, headers=API_HEADERS, json=payload, timeout=120
            )
            resp.raise_for_status()
            return resp.json()["results"]
        except Exception as exc:
            print(
                f"    [warn] API error attempt {attempt}/{RETRY_LIMIT}: {exc}",
                file=sys.stderr,
            )
            if attempt < RETRY_LIMIT:
                time.sleep(RETRY_DELAY)
    # On total failure, return empty strings so this file can still be written
    return [""] * len(texts)


def _is_tag(s: str) -> bool:
    """Return True if s looks like a Dharmamitra morphological tag (SNM, Cp, SPr3O…)."""
    return bool(s) and s.isascii() and any(c.isupper() for c in s)


def extract_words(api_result: str) -> list[str]:
    """
    Parse Dharmamitra API unsandhied output into clean Sanskrit word tokens.

    The API separates word groups with SPACES.  Within each group underscores
    connect the parts:
      - Triple (recognised word):  sandhied_unsandhied_TAG  e.g. abdāt_abda_SBM
      - Pair (no morphology tag):  sandhied_unsandhied_     e.g. ūrdhvam_ūrdhvam_
      - Flat (unrecognised span):  word1_word2_word3_…       e.g. yat_vyāvṛttam_manaḥ_…

    We take the UNSANDHIED (second) part from triples/pairs, and all parts from
    flat lists, discarding the sandhied originals and all morphological tags.
    """
    words = []
    for group in api_result.split(" "):
        group = group.strip()
        if not group or group in {"/", "|", "||", "।", "॥"}:
            continue

        parts = [p for p in group.split("_") if p.strip()]
        if not parts:
            continue

        last = parts[-1]

        if _is_tag(last) and len(parts) >= 2:
            # Triple: sandhied_unsandhied_TAG — take unsandhied (index 1)
            unsandhied = parts[1]
            if unsandhied and not _is_tag(unsandhied) and any(c.isalpha() for c in unsandhied):
                words.append(unsandhied)

        elif len(parts) == 2:
            # Pair without tag: sandhied_unsandhied — take unsandhied (index 1)
            unsandhied = parts[1]
            if unsandhied and not _is_tag(unsandhied) and any(c.isalpha() for c in unsandhied):
                words.append(unsandhied)

        elif len(parts) == 1:
            # Single token
            word = parts[0]
            if not _is_tag(word) and any(c.isalpha() for c in word):
                words.append(word)

        else:
            # Flat list (more than 2 parts, no trailing tag) — keep all valid parts
            for part in parts:
                if not part or part in {"/", "|", "||", "।", "॥"}:
                    continue
                if _is_tag(part):
                    continue
                if not any(c.isalpha() for c in part):
                    continue
                words.append(part)

    return words


def process_file(input_path: Path, output_path: Path) -> None:
    lines = input_path.read_text(encoding="utf-8").splitlines()

    # Collect indices of lines that need API processing
    to_process = [(i, l) for i, l in enumerate(lines) if not is_skip_line(l)]

    if not to_process:
        output_path.write_text("", encoding="utf-8")
        return

    all_words: list[str] = []
    total = len(to_process)
    done  = 0

    for batch_start in range(0, total, BATCH_SIZE):
        batch = to_process[batch_start : batch_start + BATCH_SIZE]
        batch_texts = [l for _, l in batch]

        results = call_api(batch_texts)

        for result in results:
            all_words.extend(extract_words(result))

        done += len(batch)
        pct   = 100 * done / total
        print(f"    {done}/{total} lines  ({pct:.0f}%)", end="\r", flush=True)

    print()  # newline after progress

    output_path.write_text(" ".join(all_words) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    input_files = sorted(INPUT_DIR.glob("*.txt"))
    total_files = len(input_files)
    print(f"Input directory : {INPUT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Files to process: {total_files}")
    print()

    for file_idx, input_path in enumerate(input_files, 1):
        output_path = OUTPUT_DIR / input_path.name

        if output_path.exists():
            print(f"[{file_idx:3}/{total_files}] SKIP  {input_path.name}")
            continue

        print(f"[{file_idx:3}/{total_files}] {input_path.name}")
        try:
            process_file(input_path, output_path)
        except Exception as exc:
            print(f"  [ERROR] {exc}", file=sys.stderr)
            # Leave no partial output so the file will be retried next run
            if output_path.exists():
                output_path.unlink()
            continue

    print("\nDone.")


if __name__ == "__main__":
    main()
