"""
process_epic_puranas_unsandhied_local.py

Local, offline replacement for process_epic_puranas_unsandhied.py.

Instead of calling the remote Dharmamitra tagging API, this loads the
int8-quantised CTranslate2 build of the ByT5-Sanskrit model
(/mnt/code/byt5-analyzer/ctranslate/ct2-byt5sanskrit-int8) and runs
segmentation (= unsandhi) inference on the GPU in-process.

The task is selected by prefixing each input line with "S " (segmentation),
exactly as byt5-analyzer/run_endpoint.py does. Output is the unsandhied
word-forms joined by "_"; we keep only the alphabetic word tokens and write
them space-separated to corpus/epic_puranas_unsandhied/, one file per input.

Line filtering (which lines get sent to the model) reuses is_skip_line() from
the API script so the remaining files are processed identically to the ones
already done.

Resumable: already-completed output files are skipped.

Run via scripts/unsandhi_local.sh, which sets the CUDA cuBLAS LD_PRELOAD and
points at the byt5-analyzer venv. int8 GEMM on Blackwell (sm_120) requires the
CUDA 12.9 cuBLAS to be preloaded; the wrapper handles that.
"""

import os
import re
import sys
import time
from pathlib import Path

# ── Line filtering ────────────────────────────────────────────────────────────
# Kept byte-for-byte identical to process_epic_puranas_unsandhied.is_skip_line so
# the remaining files are filtered exactly like the ones already processed via the
# API. (Inlined rather than imported to avoid that module's `requests` dependency,
# which this offline script does not need.)

_DIACRITICS = frozenset('āīūṛṝḷṃḥṅñṇṭḍśṣĀĪŪṚṜḶṂḤṄÑṆṬḌŚṢ')

_NON_SANSK_RE = re.compile(
    r'^\\[A-Za-z]'            # GRETIL editorial tags like \Eb, \Ef
    r'|^[=_\-]{3,}'           # separator lines (===, ___, ---)
    r'|^https?://'            # URLs
    r'|^http://'
)


def is_skip_line(line: str) -> bool:
    """Return True for lines that should not be sent to the model."""
    s = line.strip()
    if not s:
        return True
    if _NON_SANSK_RE.search(s):
        return True
    non_space = s.replace(' ', '')
    if len(non_space) <= 1:
        return True
    ascii_letters = sum(1 for c in s if c.isascii() and c.isalpha())
    total_letters = sum(1 for c in s if c.isalpha())
    if total_letters > 0 and ascii_letters / total_letters > 0.85:
        return True
    has_diacritic = any(c in _DIACRITICS for c in s)
    if not has_diacritic and len(s.split()) < 4:
        return True
    return False

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT  = SCRIPT_DIR.parent
INPUT_DIR  = REPO_ROOT / "corpus" / "epic_puranas"
OUTPUT_DIR = REPO_ROOT / "corpus" / "epic_puranas_unsandhied"

# ── Model ─────────────────────────────────────────────────────────────────────
MODEL_PATH   = os.getenv(
    "CT2_MODEL_PATH", "/mnt/code/byt5-analyzer/ctranslate/ct2-byt5sanskrit-int8"
)
TOKENIZER    = os.getenv("CT2_TOKENIZER", "chronbmm/sanskrit5-multitask")
DEVICE       = os.getenv("CTRANSLATE_DEVICE", "cuda")
DEVICE_INDEX = int(os.getenv("CTRANSLATE_DEVICE_INDEX", "0"))
COMPUTE_TYPE = os.getenv("CTRANSLATE_COMPUTE_TYPE", "int8")  # honour the int8 build
PREFIX       = "S "   # segmentation task = unsandhi
MAX_LENGTH   = 512    # ByT5 is byte-level; the served model uses 512
BATCH_SIZE   = int(os.getenv("CT2_BATCH_SIZE", "256"))

_PUNCT = {"/", "|", "//", "||", "।", "॥"}

# Source lines carry editorial furniture that IAST Sanskrit never does, and which
# the byte-level model otherwise mangles into junk tokens that survive word
# extraction. strip_ref_markers() removes four families before inference:
#
# 1. Letter-bearing GRETIL reference tags -- an uppercase sigil + "_" + a
#    numeric reference, e.g. agni "/AP_1.001ab/", viṣṇu "// ViP_1,1.0 //",
#    brahmāṇḍa "// BndP_1,1.1 //". The sigil+"_"+digit anchor never occurs in
#    IAST, so it also catches agni's malformed variants: glued to the previous
#    word ("smaretAP_24.045cd/"), asterisked ("/AP_*1.001ab/"), and dot-prefixed
#    ("/.AP_81.083ab/"). Contrast the letterless leading markers other corpora
#    carry (bhagavata "01.01.001/1", ramayana "1.001.001a"), which are harmless.
# 2. Any remaining digits -- these are only ever verse numbers, never part of an
#    IAST word token, so stripping every digit run is safe.
# 3. nīlamatapurāṇa's editorial separators: "+" joins words within a pāda
#    ("devam+harim") and "&" marks a pāda boundary ("&varadam"); both become spaces.
# 4. Lacuna markers -- RUNS of dashes ("-- -- --" in the skandapurāṇa critical
#    edition, em-dashes elsewhere) marking lost/illegible akṣaras. Fed to the model
#    they hallucinate into "ro-0 di-1 di-1 …". Only runs of >=2 dashes are stripped;
#    a SINGLE intra-word hyphen is a compound boundary (bhagavata "ī-ś", padma) and
#    is preserved. Content-free lines (pure lacuna / verse-number rows) are dropped
#    upstream in process_file once stripping leaves them without Sanskrit letters.
# Anchor: optional daṇḍa/slash, an ASCII uppercase sigil, "_", optional "*", a
# digit; then consume the reference tail up to the next delimiter (space, slash or
# daṇḍa) so diacritic-bearing labels like agni's "/AP_221ā.001ab/" are caught whole.
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


def _is_ascii_noise(part: str) -> bool:
    """
    True for uppercase-initial pure-ASCII tokens, which are never lowercase-IAST
    Sanskrit content. Covers three junk classes:
      - the multitask model's grammatical-tag hallucinations (SNM, SLNe, PNM, PGM,
        DuLM …) emitted attached to words on colophon lines ("…_adhyāyaḥ_SNM");
      - leaked running-header / title fragments (Matsya from "Matsya-Purāṇa N", Mang);
      - stray capitals (R, I, Cp).
    Harvard-Kyoto-encoded Sanskrit words (maGgala=maṅgala, aGga, pitR=pitṛ) are also
    ASCII with embedded capitals but start LOWERCASE, so the leading-case test keeps
    them; diacritic-bearing IAST words are non-ASCII and never match.
    """
    return part.isascii() and part[:1].isupper()


def extract_words(result: str) -> list[str]:
    """
    Parse the model's segmentation output into clean word tokens.

    Segmentation output joins the unsandhied word-forms of a line with "_"
    (with a trailing "_"), and daṇḍas survive as separate whitespace tokens,
    e.g.  "naram_ca_eva_narottamam_ /".  We split on whitespace and "_", strip
    daṇḍa/slash punctuation the model occasionally glues onto a word ("//utpanna"
    -> "utpanna"), keep tokens containing a letter, and drop punctuation.

    Two model-hallucination classes are dropped:
      - Digit-bearing tokens: strip_ref_markers() removes every digit from the
        input, so any digit in the output is junk -- e.g. "ro-0 fl-2 di-1 ad-20"
        the model emits on short speaker-attribution lines like "vāyuruvāca||".
      - Uppercase-initial ASCII noise: model tags, header fragments (see
        _is_ascii_noise).
    """
    words: list[str] = []
    for group in result.split():
        if group in _PUNCT:
            continue
        parts = [p.strip("/|।॥. \t") for p in group.split("_")]
        for part in parts:
            if not any(c.isalpha() for c in part):
                continue
            if any(c.isdigit() for c in part):
                continue
            if _is_ascii_noise(part):
                continue
            words.append(part)
    return words


def process_file(translator, tokenizer, input_path: Path, output_path: Path) -> None:
    lines = input_path.read_text(encoding="utf-8").splitlines()
    # Strip editorial furniture up front, then drop lines left without Sanskrit
    # content (pure lacuna / verse-number rows), which the model would otherwise
    # hallucinate into junk. Downstream batches receive the already-stripped text.
    to_process = []
    for l in lines:
        if is_skip_line(l):
            continue
        s = strip_ref_markers(l)
        if has_sanskrit(s):
            to_process.append(s)

    if not to_process:
        output_path.write_text("", encoding="utf-8")
        return

    all_words: list[str] = []
    total = len(to_process)
    done  = 0

    for start in range(0, total, BATCH_SIZE):
        batch = to_process[start : start + BATCH_SIZE]
        texts = [PREFIX + l for l in batch]   # batch is already stripped
        enc = tokenizer(texts, truncation=True, max_length=MAX_LENGTH)
        tokens = [tokenizer.convert_ids_to_tokens(ids) for ids in enc["input_ids"]]
        results = translator.translate_batch(
            tokens,
            max_decoding_length=MAX_LENGTH,
            beam_size=1,
            max_batch_size=BATCH_SIZE,
        )
        for r in results:
            decoded = tokenizer.decode(
                tokenizer.convert_tokens_to_ids(r.hypotheses[0])
            )
            all_words.extend(extract_words(decoded))

        done += len(batch)
        pct = 100 * done / total
        print(f"    {done}/{total} lines  ({pct:.0f}%)", end="\r", flush=True)

    print()
    output_path.write_text(" ".join(all_words) + "\n", encoding="utf-8")


def select_shard(files: list[Path], shard: int, num_shards: int) -> list[Path]:
    """
    Deterministically assign files to `num_shards` shards, balanced by file size
    (longest-processing-time greedy), and return only this shard's files.

    Every process runs the identical assignment over the identical file list, so
    the shards are disjoint and cover everything with no coordination needed.
    """
    if num_shards <= 1:
        return files
    sized = sorted(files, key=lambda p: p.stat().st_size, reverse=True)
    loads = [0] * num_shards
    mine: list[Path] = []
    for p in sized:
        j = loads.index(min(loads))
        loads[j] += p.stat().st_size
        if j == shard:
            mine.append(p)
    # Preserve alphabetical order within the shard for readable logs.
    return sorted(mine)


def main() -> None:
    import argparse
    import ctranslate2
    import transformers

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", help="Restrict to these basenames (default: all).")
    ap.add_argument("--force", action="store_true",
                    help="Reprocess even if an output file already exists.")
    ap.add_argument("--shard", type=int, default=0, help="This shard's index (0-based).")
    ap.add_argument("--num-shards", type=int, default=1,
                    help="Total number of shards (e.g. one per GPU).")
    args = ap.parse_args()

    tag = f"[shard {args.shard}/{args.num_shards}] " if args.num_shards > 1 else ""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"{tag}Model           : {MODEL_PATH}")
    print(f"{tag}Device          : {DEVICE}:{DEVICE_INDEX}  compute_type={COMPUTE_TYPE}"
          f"  (CUDA_VISIBLE_DEVICES={os.getenv('CUDA_VISIBLE_DEVICES', 'unset')})")
    tokenizer  = transformers.AutoTokenizer.from_pretrained(TOKENIZER)
    translator = ctranslate2.Translator(
        MODEL_PATH,
        device=DEVICE,
        device_index=DEVICE_INDEX,
        compute_type=COMPUTE_TYPE,
    )
    print(f"{tag}Resolved compute: {translator.compute_type}")

    input_files = sorted(
        p for p in INPUT_DIR.glob("*.txt") if not p.name.endswith(".orig")
    )
    if args.files:
        wanted = set(args.files)
        input_files = [p for p in input_files if p.name in wanted]
    input_files = select_shard(input_files, args.shard, args.num_shards)

    total_files = len(input_files)
    print(f"{tag}Input directory : {INPUT_DIR}")
    print(f"{tag}Output directory: {OUTPUT_DIR}")
    print(f"{tag}Files to process: {total_files}  (force={args.force})")
    print()

    for file_idx, input_path in enumerate(input_files, 1):
        output_path = OUTPUT_DIR / input_path.name
        if output_path.exists() and not args.force:
            print(f"{tag}[{file_idx:3}/{total_files}] SKIP  {input_path.name}")
            continue

        print(f"{tag}[{file_idx:3}/{total_files}] {input_path.name}")
        t0 = time.time()
        try:
            process_file(translator, tokenizer, input_path, output_path)
        except Exception as exc:
            print(f"{tag}  [ERROR] {exc}", file=sys.stderr)
            if output_path.exists():
                output_path.unlink()   # no partial output; retried next run
            continue
        print(f"{tag}    done in {time.time() - t0:.1f}s")

    print(f"\n{tag}Done.")


if __name__ == "__main__":
    main()
