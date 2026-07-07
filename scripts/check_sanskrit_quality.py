"""
check_sanskrit_quality.py

Checks corpus/gi_unsandhied/ files against the Monier-Williams dictionary
to surface tokens that are likely OCR errors, stray non-Sanskrit content,
or unusually rare/unrecognised forms.

APPROACH
--------
The gi_unsandhied/ files contain tokens already decomposed by the
Dharmamitra morphological API (sandhi dissolved, compounds split).
Those tokens are inflected forms, so a direct dictionary lookup misses
~45 % of valid Sanskrit.  We apply a suffix-stripping normaliser that
generates plausible stem candidates and checks each against the set of
MW IAST headwords (key_utf8 field).  This raises the match rate to ~85 %
for well-formed Sanskrit text.

Tokens that still cannot be matched after normalisation are reported in
two groups:
  - ARTIFACT  non-IAST characters / digits / punctuation residue
  - UNKNOWN   plausible IAST string but unmatched in MW after normalisation

OUTPUT
------
  corpus/gi_quality/<filename>.tsv   per-file report
  corpus/gi_quality/_summary.tsv     corpus-wide summary, ranked by count

TSV columns: token | count | category (ARTIFACT / UNKNOWN)

Resumable: output files that already exist are skipped.
"""

import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT  = SCRIPT_DIR.parent
INPUT_DIR  = REPO_ROOT / "corpus" / "gi_unsandhied"
OUTPUT_DIR = REPO_ROOT / "corpus" / "gi_quality"
MW_DB      = Path.home() / "Library/Dictionaries/Monier Williams/mw2.db"


_ARTIFACT_RE = re.compile(
    r"\d"                       # digit anywhere in the token
    r"|[^aāiīuūṛṝḷeoṃḥṅñṇṭḍśṣkgcjṭḍtdpbhśṣsnmlrvy'"
    r"AĀIĪUŪṚṜḶEOṂḤṄÑṆṬḌŚṢKGCJṬḌTDPBHŚṢSNMLRVY-]"
)

# Punctuation characters that may prefix a Sanskrit word in quoted/marked text.
# Tokens whose only non-IAST characters are one or more of these at the start
# are reclassified as PREFIXED_UNKNOWN; the stripped core is stored separately.
_QUOTE_DASH_PREFIX_RE = re.compile(r'^["“‘—–]+')

# ── MW headword set ────────────────────────────────────────────────────────────

def load_mw_headwords() -> frozenset[str]:
    db  = sqlite3.connect(MW_DB)
    cur = db.cursor()
    cur.execute("SELECT DISTINCT key_utf8 FROM mw_dict WHERE key_utf8 != ''")
    hw = frozenset(r[0] for r in cur.fetchall())
    db.close()
    return hw


# ── Normalisation / stem-candidate generator ──────────────────────────────────

def candidate_stems(token: str, depth: int = 0) -> list[str]:
    """
    Generate plausible MW headword candidates from an inflected IAST token.
    Returns a deduplicated list, shortest candidates first.
    """
    if depth > 1:
        return [token]

    t = token
    seen: dict[str, None] = {t: None}

    def add(s: str) -> None:
        if s and len(s) >= 2:
            seen[s] = None

    # ── visarga → s, then optionally strip trailing s ──────────────────────
    if t.endswith("ḥ"):
        base = t[:-1]
        add(base + "s")
        # a/ā/i/u-stem nom sg: arthaḥ → artha, siddhiḥ → siddhi
        for v in "aāiu":
            if base.endswith(v):
                add(base)

    # ── direct nom-sg stripping ────────────────────────────────────────────
    if t.endswith("aḥ"):  add(t[:-2])           # a-stem masc/neut nom sg
    if t.endswith("āḥ"):  add(t[:-2])           # ā-stem fem nom sg / a-stem pl
    if t.endswith("iḥ"):  add(t[:-2])           # i-stem nom sg
    if t.endswith("uḥ"):  add(t[:-2])           # u-stem nom sg
    if t.endswith("eḥ"):  add(t[:-2] + "i")     # i-stem gen sg (rāter→rāti)

    # ── anusvāra ───────────────────────────────────────────────────────────
    if t.endswith("ṃ"):
        add(t[:-1] + "m")
        add(t[:-1] + "n")

    # ── nominal ending table ───────────────────────────────────────────────
    _ENDINGS = [
        # a-stems
        ("asya", "a"), ("āya", "a"), ("āt", "a"), ("ena", "a"),
        ("eṣu", "a"), ("aiḥ", "a"), ("ānām", "a"), ("ān", "a"),
        ("āni", "a"), ("ebhyaḥ", "a"), ("asmin", "a"), ("e", "a"),
        ("am", "a"),
        # ā-stems (fem)
        ("āyāḥ", "ā"), ("āyām", "ā"), ("āyai", "ā"), ("āyāt", "ā"),
        # i-stems
        ("ayaḥ", "i"), ("ibhiḥ", "i"), ("iṣu", "i"), ("inā", "i"),
        ("aye", "i"), ("im", "i"), ("ī", "i"),
        ("au", "i"),          # loc sg: śrutau→śruti, ādau→ādi
        # u-stems
        ("oḥ", "u"), ("avaḥ", "u"), ("ubhiḥ", "u"), ("uṣu", "u"),
        ("unā", "u"), ("ave", "u"), ("um", "u"),
        # an/man-stems (with retroflex sandhi)
        ("maṇaḥ", "man"), ("maṇe", "man"), ("maṇi", "man"),
        ("maṇam", "man"), ("mabhiḥ", "man"), ("masu", "man"),
        ("manā", "man"), ("mane", "man"), ("manaḥ", "man"),
        ("manam", "man"), ("mānam", "man"), ("mānaḥ", "man"),
        ("mani", "man"),     # non-retroflex loc sg: ātmani
        # -tva abstract nouns
        ("tvāt", "tva"), ("tvam", "tva"), ("tvaṃ", "tva"), ("tvena", "tva"),
        ("tve", "tva"), ("tvasya", "tva"), ("tvāya", "tva"), ("tvāni", "tva"),
        # -tā abstract nouns
        ("tayā", "tā"), ("tāyāḥ", "tā"), ("tām", "tā"),
        # verb present active / middle
        ("ati", ""), ("anti", ""), ("ate", ""), ("ante", ""),
        ("āmi", ""), ("āvaḥ", ""), ("āmaḥ", ""),
        ("asi", ""), ("athaḥ", ""), ("atha", ""),
        ("ti", ""), ("te", ""), ("yate", ""), ("yati", ""),
        ("ayati", ""), ("ayate", ""),
        # causative marker
        ("ayati", ""), ("ayate", ""),
        # gerund / infinitive
        ("tvā", ""), ("ya", ""), ("tum", ""),
        # gen pl
        ("ānām", "a"), ("īnām", "i"), ("ūnām", "u"),
    ]

    for suf, repl in _ENDINGS:
        if t.endswith(suf) and len(t) - len(suf) >= 2:
            stem = (t[:-len(suf)] + repl) if repl else t[:-len(suf)]
            add(stem)

    # ── n-stem nom sg: ātmā → ātman ───────────────────────────────────────
    if t.endswith("ā") and len(t) >= 3:
        add(t[:-1] + "an")
        add(t[:-1] + "n")

    # ── aṇ-inflection pattern: brahmaṇaḥ → brahman ───────────────────────
    m = re.match(r"^(.+?)aṇ(aḥ|am|e|i|ā|āt|asya|āya|ānām)$", t)
    if m:
        add(m.group(1) + "an")

    # ── negation prefix a- : recurse on base ──────────────────────────────
    if t.startswith("a") and len(t) > 4 and depth == 0:
        for c in candidate_stems(t[1:], depth + 1):
            add("a" + c)

    return list(seen)   # insertion-ordered (dict preserves order in Py 3.7+)


def lookup(token: str, mw: frozenset[str]) -> bool:
    return any(s in mw for s in candidate_stems(token))


# ── Token classification ───────────────────────────────────────────────────────

def classify(token: str, mw: frozenset[str]) -> tuple[str, str] | tuple[None, None]:
    """
    Return (category, core) where category is 'ARTIFACT', 'UNKNOWN',
    'PREFIXED_UNKNOWN', or None (= matched, not reported).
    core is the stripped token for PREFIXED_UNKNOWN, empty string otherwise.
    """
    if len(token) <= 1:
        return None, None
    if token in mw:
        return None, None
    # Check for quote/em-dash prefix before general artifact check
    m = _QUOTE_DASH_PREFIX_RE.match(token)
    if m:
        core = token[m.end():]
        if len(core) >= 2 and not _ARTIFACT_RE.search(core):
            return "PREFIXED_UNKNOWN", core
    if _ARTIFACT_RE.search(token):
        return "ARTIFACT", ""
    if lookup(token, mw):
        return None, None
    return "UNKNOWN", ""


# ── Per-file processing ────────────────────────────────────────────────────────

def process_file(input_path: Path, output_path: Path,
                 mw: frozenset[str]) -> Counter:
    tokens = input_path.read_text(encoding="utf-8").split()
    counts: Counter = Counter()

    for tok in tokens:
        cat, core = classify(tok, mw)
        if cat:
            counts[(tok, cat, core)] += 1

    total = len(tokens)
    n_flagged = sum(counts.values())
    rate = 100 * n_flagged / total if total else 0.0

    with output_path.open("w", encoding="utf-8") as f:
        f.write(f"# total_tokens={total}  flagged={n_flagged}  rate={rate:.1f}%\n")
        f.write("token\tcount\tcategory\tcore\n")
        for (tok, cat, core), cnt in sorted(counts.items(),
                                            key=lambda x: -x[1]):
            f.write(f"{tok}\t{cnt}\t{cat}\t{core}\n")

    return counts


def load_existing(output_path: Path) -> tuple[Counter, int, int]:
    counts: Counter = Counter()
    total = flagged = 0
    with output_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("# "):
                m = re.search(r"total_tokens=(\d+).*flagged=(\d+)", line)
                if m:
                    total, flagged = int(m.group(1)), int(m.group(2))
                continue
            if line.startswith("token\t"):
                continue
            parts = line.split("\t")
            if len(parts) >= 3:
                core = parts[3] if len(parts) == 4 else ""
                counts[(parts[0], parts[2], core)] += int(parts[1])
    return counts, total, flagged


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not MW_DB.exists():
        print(f"[ERROR] MW database not found: {MW_DB}", file=sys.stderr)
        sys.exit(1)

    print("Loading Monier-Williams headwords…", end=" ", flush=True)
    mw = load_mw_headwords()
    print(f"{len(mw):,} headwords loaded.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    input_files = sorted(INPUT_DIR.glob("*.txt"))
    total_files = len(input_files)
    print(f"Input : {INPUT_DIR}  ({total_files} files)")
    print(f"Output: {OUTPUT_DIR}\n")

    all_counts: Counter = Counter()
    corpus_total = corpus_flagged = 0

    for idx, input_path in enumerate(input_files, 1):
        output_path = OUTPUT_DIR / input_path.name

        if output_path.exists():
            counts, tot, flagged = load_existing(output_path)
            rate = 100 * flagged / tot if tot else 0.0
            print(f"[{idx:3}/{total_files}] SKIP  {input_path.name}"
                  f"  ({flagged}/{tot} flagged, {rate:.1f}%)")
        else:
            print(f"[{idx:3}/{total_files}] {input_path.name}", flush=True)
            try:
                counts = process_file(input_path, output_path, mw)
                tot     = len(input_path.read_text(encoding="utf-8").split())
                flagged = sum(counts.values())
            except Exception as exc:
                print(f"  [ERROR] {exc}", file=sys.stderr)
                if output_path.exists():
                    output_path.unlink()
                continue
            rate = 100 * flagged / tot if tot else 0.0
            print(f"          → {flagged}/{tot} tokens flagged ({rate:.1f}%)")

        all_counts.update(counts)
        corpus_total   += tot
        corpus_flagged += flagged

    # ── Corpus summary ────────────────────────────────────────────────────
    summary_path = OUTPUT_DIR / "_summary.tsv"
    corpus_rate  = 100 * corpus_flagged / corpus_total if corpus_total else 0.0

    with summary_path.open("w", encoding="utf-8") as f:
        f.write(f"# corpus total_tokens={corpus_total}  "
                f"flagged={corpus_flagged}  rate={corpus_rate:.1f}%\n")
        f.write("token\ttotal_count\tcategory\tcore\n")
        for (tok, cat, core), cnt in sorted(all_counts.items(), key=lambda x: -x[1]):
            f.write(f"{tok}\t{cnt}\t{cat}\t{core}\n")

    print(f"\nDone.")
    print(f"Flagged: {corpus_flagged:,}/{corpus_total:,} tokens "
          f"({corpus_rate:.1f}%)")
    print(f"Unique flagged types: {len(all_counts):,}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
