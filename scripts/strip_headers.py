#!/usr/bin/env python3
"""Strip non-Sanskrit headers (and footers where present) from corpus files.

Handles two main patterns:
  - GRETIL: boilerplate "THIS ... REFERENCE PURPOSES ONLY" + encoding note +
    "description:/multibyte sequence:" transliteration table. Header ends at
    the blank gap after the table.
  - Muktabodha: ########### banner + metadata block + closing ########### banner.
    Also strips matching footer banner at end of file.

Files matching SARIT or TEI/XML structure are skipped (listed separately);
they need per-text handling.

Usage:
    python3 strip_headers.py --dry-run [paths...]
    python3 strip_headers.py --apply [paths...]
    python3 strip_headers.py --sample N --dry-run     # preview N diverse files
"""
import argparse, os, re, sys, random
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent / "corpus"

# --- detectors -------------------------------------------------------------

GRETIL_MARK   = re.compile(r"FOR REFERENCE PURPOSES ONLY", re.I)
MUKTA_MARK    = re.compile(r"Muktabodha", re.I)
SARIT_MARK    = re.compile(r"\bSARIT\b")
TEI_MARK      = re.compile(r"<\?xml|<TEI", re.I)
BANNER_HASH   = re.compile(r"^[#=]{10,}\s*$")

# Transliteration-table line: a short descriptor like "long a", "visarga",
# "retroflex t", "anusvara", or a single IAST letter on its own.
TRANSLIT_DESCRIPTOR = re.compile(
    r"^\s*(long|short|vocalic|velar|palatal|retroflex|dental|labial|"
    r"anusvara|anusvāra|visarga|avagraha|candrabindu|jihvāmūlīya|upadhmānīya|"
    r"description|multibyte|jihvamuliya|upadhmaniya|anunasika|anunāsika)\b",
    re.I,
)
# Any line that mentions "underbar" is a table entry (e.g. "l underbar  ḻ").
TABLE_UNDERBAR = re.compile(r"\bunderbar\b", re.I)
# Generic table row: short line, ASCII + at most a couple IAST chars at end.
TABLE_GENERIC = re.compile(
    r"^\s*[A-Za-z][A-Za-z _]{0,30}"
    r"\s*[āĀīĪūŪṛṚṝṜḷḶḹḸṅṄñÑṭṬḍḌṇṆśŚṣṢṃṂḥḤēōḻṟṉḵṯ]?\s*$"
)
SINGLE_IAST = re.compile(r"^\s*\S{1,3}\s*$")  # any 1-3 non-space chars on a line

# A line of ASCII-only English prose (no Sanskrit diacritics at all).
IAST_CHARS = "āĀīĪūŪṛṚṝṜḷḶḹḸṅṄñÑṭṬḍḌṇṆśŚṣṢṃṂḥḤēōḻṟṉḵṯ"
HAS_IAST = re.compile(f"[{IAST_CHARS}]")
ASCII_ENGLISH_WORD = re.compile(r"[A-Za-z]{4,}")


def classify(path: Path) -> str:
    """Return 'gretil', 'muktabodha', 'sarit', 'tei', 'editor_only', or 'none'."""
    # Skip unsandhied corpora — user handles those separately.
    if "_unsandhied" in path.as_posix():
        return "none"
    try:
        with path.open(encoding="utf-8", errors="replace") as f:
            head = "".join(next(f, "") for _ in range(80))
    except Exception:
        return "none"
    if TEI_MARK.search(head):
        return "tei"
    if SARIT_MARK.search(head):
        return "sarit"
    if MUKTA_MARK.search(head):
        return "muktabodha"
    if GRETIL_MARK.search(head):
        return "gretil"
    # Muktabodha-style banner block (========) used by some non-Muktabodha files
    first_nonblank = next((ln for ln in head.splitlines() if ln.strip()), "")
    if BANNER_HASH.match(first_nonblank):
        return "muktabodha"
    # Editor-credit-only: "Input by"/"Data-entered"/"entered by"/"% database"
    if re.search(r"Input by|entered by|Data-entered|database copyright|"
                 r"Electronic text|Based on the edition|Typed by|"
                 r"Typed from the edition|etext input|digitized by|"
                 r"digitalised by|Compilation, data entry|"
                 r"transliteration emulates", head, re.I):
        return "editor_only"
    return "none"


# --- strippers -------------------------------------------------------------

def strip_gretil(lines):
    """Cut everything up to and including the transliteration table.

    Strategy: scan forward past the GRETIL marker; then walk through the
    description/multibyte table (short descriptor lines and solo IAST-letter
    lines separated by blanks); stop when we hit a non-table, non-blank line.
    That line is where the Sanskrit begins. Also trim leading/trailing blanks.
    """
    n = len(lines)
    i = 0
    # find the REFERENCE PURPOSES marker
    ref_idx = -1
    for j, ln in enumerate(lines[:200]):
        if GRETIL_MARK.search(ln):
            ref_idx = j
            break
    if ref_idx < 0:
        return lines, None  # shouldn't happen
    # after the marker, skip until we start seeing table-descriptor lines
    i = ref_idx + 1
    # scan for either a description:/multibyte: header or first descriptor line
    saw_table = False
    while i < n and i < ref_idx + 300:
        ln = lines[i].strip()
        if not ln:
            i += 1; continue
        if (TRANSLIT_DESCRIPTOR.match(ln) or SINGLE_IAST.match(ln)
                or TABLE_UNDERBAR.search(ln)
                or (saw_table and TABLE_GENERIC.match(ln) and len(ln) < 60)):
            saw_table = True
            i += 1; continue
        # A line that isn't blank, isn't a descriptor, isn't a single IAST
        # letter → end of table (or there was never a table).
        if saw_table:
            break
        # still in pre-table prose (encoding note, "UTF-8", etc.): skip short
        # English/ASCII-heavy lines.
        if re.search(r"[A-Za-z]", ln) and not re.search(r"[āīūṛṝḷḹṅñṭḍṇśṣṃḥēō]", ln):
            i += 1; continue
        # hit something Sanskrit-looking before any table → stop here
        break
    # trim leading blanks in the remainder
    while i < n and not lines[i].strip():
        i += 1
    # after the table, GRETIL files often have English prose notes, URLs,
    # and short filler lines ("and", "http://..."). We're still inside the
    # header zone, so skip any line without Sanskrit diacritics. Stop on the
    # first line containing IAST chars. Safety cap: 150 lines.
    start_post = i
    while i < n and i - start_post < 150:
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if HAS_IAST.search(ln):
            break
        i += 1
    body = lines[i:]
    # Trim trailing blanks / trailing "EOF" tokens commonly left by GRETIL
    while body and (not body[-1].strip() or body[-1].strip() in {"EOF", "eof"}):
        body.pop()
    return body, i


def strip_muktabodha(lines):
    """Remove banner+metadata at top and matching footer at bottom."""
    n = len(lines)
    # find every banner line in top 150 lines and start content after the LAST
    # one — files with multiple header sections (bibliographic + "main text"
    # banner) benefit from this.
    banners = [j for j, ln in enumerate(lines[:150]) if BANNER_HASH.match(ln)]
    start = banners[-1] + 1 if banners else 0
    # also strip the "Muktabodha E-text in UTF-8" line if it precedes the banner
    # (already captured by start). Trim leading blanks.
    while start < n and not lines[start].strip():
        start += 1

    # footer: scan last 40 lines for Muktabodha footer start
    end = n
    tail_search = lines[max(0, n - 40):]
    for k, ln in enumerate(tail_search):
        if re.search(r"MUKTABODHA INDOLOGICAL RESEARCH INSTITUTE", ln, re.I) \
           or BANNER_HASH.match(ln):
            end = max(0, n - 40) + k
            break
    body = lines[start:end]
    while body and not body[-1].strip():
        body.pop()
    return body, (start, end)


def strip_editor_only(lines):
    """For files with only a small editor-credit header (no GRETIL boilerplate).

    Conservative: remove leading lines that look like metadata (English words
    lacking IAST diacritics, lines starting with '%', or obvious header items)
    until we hit a Sanskrit-looking line.
    """
    n = len(lines)
    # Skip files with only one giant line (hand-crafted unsandhied dumps etc.)
    if n <= 1:
        return lines, 0
    META = re.compile(
        r"^\s*(%|\\section|\\label|\\[a-zA-Z]+\{|"
        r"Input by|Data[- ]entered|entered by|Electronic text|etext input|"
        r"Based on the edition|based on the edition|"
        r"database copyright|Copyright|\(C\)|©|"
        r"Text converted|THIS .*FILE|COPYRIGHT|https?://|www\.|"
        r"Edition|Published|Publisher|Publication|encoding|Encoding|"
        r"Author|Editor|Title|Catalog number|Uniform title|Secondary title|"
        r"Alternate name|Commentator|Notes|Source|Revision|ed\.|publ\.|"
        r"digital[iī]sed by|digitized by|typed by|transliteration emulates|"
        r"word boundaries|padas in text|\[of|/[A-Z])",
        re.I,
    )
    META_SUBSTR = re.compile(
        r"\b(edition|eds?:|etext input|input by|ed\.|publ\.|"
        r"Kaivalyadhama|Steam Press|Bombay|Calcutta|Mithila Institute|"
        r"Śrīveṅkateśvara|Khemarāj|Asiatic Society|Bhandarkar|"
        r"Harrassowitz|Oriental Research|Darbhanga|"
        r"GRETIL|DCS|SARIT|Muktabodha)\b",
        re.I,
    )
    # Find the index of the LAST metadata-like line in the top 60 lines.
    last_meta = -1
    for i in range(min(60, n)):
        ln = lines[i].rstrip()
        if not ln:
            continue
        is_meta = (META.match(ln) or META_SUBSTR.search(ln) or
                   # short English-only line (no diacritics) near top
                   (i < 15 and len(ln) < 80 and re.search(r"[A-Za-z]", ln)
                    and not re.search(r"[āīūṛṝḷḹṅñṭḍṇśṣṃḥēō]", ln)))
        if is_meta:
            last_meta = i
    start = last_meta + 1 if last_meta >= 0 else 0
    while start < n and not lines[start].strip():
        start += 1
    return lines[start:], start


# --- driver ----------------------------------------------------------------

def collect_targets(paths):
    files = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files.extend(sorted(p.rglob("*.txt")))
        elif p.is_file():
            files.append(p)
    return files


def process_file(path: Path, apply: bool):
    with path.open(encoding="utf-8", errors="replace") as f:
        orig = f.read().splitlines(keepends=True)
    kind = classify(path)
    if kind in ("none",):
        return kind, 0, 0, None
    if kind in ("sarit", "tei"):
        return kind, 0, 0, None  # skip

    if kind == "gretil":
        new, cut = strip_gretil(orig)
    elif kind == "muktabodha":
        new, cut = strip_muktabodha(orig)
    elif kind == "editor_only":
        new, cut = strip_editor_only(orig)
    else:
        return kind, 0, 0, None

    removed_top = cut if isinstance(cut, int) else (cut[0] if cut else 0)
    preview = "".join(orig[:removed_top]) if removed_top else ""

    if apply and new != orig:
        path.write_text("".join(new), encoding="utf-8")
    return kind, len(orig), len(new), preview


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--sample", type=int, default=0,
                    help="Preview only N random files")
    ap.add_argument("paths", nargs="*", default=[str(CORPUS)])
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        args.dry_run = True

    files = collect_targets(args.paths)
    results = []
    for fp in files:
        kind = classify(fp)
        if kind == "none":
            continue
        results.append((fp, kind))

    if args.sample:
        # pick one from each category, then fill to N randomly
        by_kind = {}
        for fp, k in results:
            by_kind.setdefault(k, []).append(fp)
        random.seed(1)
        picked = []
        for k, lst in by_kind.items():
            picked.append((lst[0], k))
        remaining = [r for r in results if r not in picked]
        random.shuffle(remaining)
        picked.extend(remaining[: max(0, args.sample - len(picked))])
        results = picked

    counts = {}
    for fp, kind in results:
        k, old, new, preview = process_file(fp, apply=args.apply)
        counts[k] = counts.get(k, 0) + 1
        if args.dry_run:
            print(f"\n===== {fp.relative_to(CORPUS.parent)} [{k}] "
                  f"{old} -> {new} lines =====")
            if preview:
                snippet = preview if len(preview) < 1200 else preview[:1200] + "…"
                print("--- WOULD REMOVE (top) ---")
                print(snippet)
    print("\n=== Summary ===")
    for k, v in sorted(counts.items()):
        print(f"  {k:14s}: {v}")
    print(f"  total processed: {sum(counts.values())}")


if __name__ == "__main__":
    main()
