"""
process_epic_puranas_unsandhied.py

Batch-processes all .txt files in corpus/epic_puranas/ through the Dharmamitra API
(mode='unsandhied') and writes plain word-only output to corpus/epic_puranas_unsandhied/.

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
INPUT_DIR   = REPO_ROOT / "corpus" / "epic_puranas"
OUTPUT_DIR  = REPO_ROOT / "corpus" / "epic_puranas_unsandhied"

# ── API ───────────────────────────────────────────────────────────────────────
API_URL     = "https://dharmamitra.org/api/tagging/"
API_HEADERS = {
    "Accept": "*/*",
    "Authorization": "Basic b2xkc3R1ZGVudDpiZWhhcHB5",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}
BATCH_SIZE  = 25   # API rejects batches >~30 lines with HTTP 500
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
    # Unrecoverable: raise so the whole file is abandoned (no partial output) and
    # retried on the next run, rather than silently writing incomplete data.
    raise RuntimeError(f"API failed after {RETRY_LIMIT} attempts for a batch of {len(texts)} lines")


def _is_tag(s: str) -> bool:
    """Return True if s looks like a Dharmamitra morphological tag (SNM, Cp, SPr3O…).

    Tags are ASCII and start UPPERCASE. The leading-case (not any-uppercase) test
    avoids misclassifying Harvard-Kyoto Sanskrit words (maGgala=maṅgala, pitR=pitṛ),
    which are ASCII with embedded capitals but start lowercase.
    """
    return bool(s) and s.isascii() and s[:1].isupper()


# Source lines carry editorial furniture that IAST Sanskrit never does, and which
# the model otherwise mangles into junk tokens that survive word extraction.
# strip_ref_markers() removes three families before processing:
#
# 1. Letter-bearing GRETIL reference tags -- an uppercase sigil + "_" + a numeric
#    reference, e.g. agni "/AP_1.001ab/", viṣṇu "// ViP_1,1.0 //", brahmāṇḍa
#    "// BndP_1,1.1 //". The sigil+"_"+digit anchor never occurs in IAST, so it
#    also catches agni's malformed variants (glued "smaretAP_24.045cd/",
#    asterisked "/AP_*1.001ab/", dot-prefixed "/.AP_81.083ab/", diacritic-labelled
#    "/AP_221ā.001ab/"). Contrast the letterless leading markers other corpora
#    carry (bhagavata "01.01.001/1", ramayana "1.001.001a"), which are harmless.
# 2. Any remaining digits -- only ever verse numbers; IAST tokens contain none.
# 3. nīlamatapurāṇa's editorial separators: "+" joins words within a pāda and "&"
#    marks a pāda boundary; both become spaces.
# 4. Lacuna markers -- RUNS of dashes ("-- -- --" / em-dashes) marking lost akṣaras,
#    which the model hallucinates into "ro-0 di-1 …". Only runs of >=2 dashes are
#    stripped; a single intra-word hyphen (compound boundary) is preserved.
_REF_TAG_RE = re.compile(r'[/|।॥.]{0,2}\s*[A-Z][A-Za-z]{0,5}_\*?[0-9][^\s/|।॥]*/?')
_SEP_RE     = re.compile(r'[+&]')
_DIGITS_RE  = re.compile(r'[0-9]+')
_LACUNA_RE  = re.compile(r'[-—–]{2,}')


def strip_ref_markers(line: str) -> str:
    """Strip reference tags, verse numbers, word/pāda separators, and lacuna runs."""
    line = _REF_TAG_RE.sub(' ', line)   # must run first: needs the digit anchor
    line = _SEP_RE.sub(' ', line)
    line = _LACUNA_RE.sub(' ', line)
    line = _DIGITS_RE.sub('', line)
    return line


def has_sanskrit(line: str) -> bool:
    """True if the (already stripped) line still holds real Sanskrit word content."""
    return sum(1 for c in line if c.isalpha()) >= 2


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

    # strip_ref_markers() removes every digit from the input, so any digit in the
    # output is a model hallucination (e.g. "ro-0"/"ad-20" junk emitted on short
    # speaker-attribution lines); drop those tokens as a backstop.
    return [w for w in words if not any(c.isdigit() for c in w)]


def process_file(input_path: Path, output_path: Path) -> None:
    lines = input_path.read_text(encoding="utf-8").splitlines()

    # Strip editorial furniture up front, then drop lines left without Sanskrit
    # content (pure lacuna / verse-number rows), which the model would otherwise
    # hallucinate into junk. The stored text is already stripped.
    to_process = []
    for i, l in enumerate(lines):
        if is_skip_line(l):
            continue
        s = strip_ref_markers(l)
        if has_sanskrit(s):
            to_process.append((i, s))

    if not to_process:
        output_path.write_text("", encoding="utf-8")
        return

    all_words: list[str] = []
    total = len(to_process)
    done  = 0

    for batch_start in range(0, total, BATCH_SIZE):
        batch = to_process[batch_start : batch_start + BATCH_SIZE]
        batch_texts = [l for _, l in batch]   # batch is already stripped

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
