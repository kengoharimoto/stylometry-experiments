"""
suggest_authorship.py

Aggregates stylo EDGES.csv co-clustering weights across distance measures
and analysis types to suggest which corpus texts may share an author.

For each pair of texts the script computes:
  - raw_score   : sum of edge weights across all EDGES files
  - files_seen  : number of EDGES files where this pair appeared at all
  - max_weight  : highest single-file weight observed for this pair
  - norm_score  : raw_score / (n_files * max_possible_weight)
                  where max_possible_weight = 100 for BCT, 1 for CA/MDS

Pairs are ranked by norm_score.  By default only BCT files are used
(most meaningful for authorship), but --all-types includes CA and MDS.

USAGE
-----
  python3 scripts/suggest_authorship.py  RESULTS_DIR  [RESULTS_DIR ...]
      [--bct-only]          use only BCT edges (default)
      [--all-types]         include CA and MDS edges
      [--min-score FLOAT]   minimum norm_score to report (default 0.3)
      [--unknown-only]      only report pairs where at least one text is unknown
      [--top N]             report only the top N pairs (default: all)
      [--out FILE]          write CSV output to FILE

OUTPUT
------
  Ranked TSV/CSV with columns:
    text_a | text_b | raw_score | files_seen | max_weight | norm_score
"""

import argparse
import csv
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


def edge_type(filename: str) -> str:
    """Return 'BCT', 'CA', 'MDS', or 'OTHER'."""
    name = Path(filename).name
    if "_BCT_" in name:
        return "BCT"
    if "_CA_" in name:
        return "CA"
    if "_MDS_" in name:
        return "MDS"
    return "OTHER"


def collect_edges(results_dirs: list[Path], use_types: set[str]) -> tuple:
    """
    Returns (pairs, n_files) where pairs maps (text_a, text_b) -> {
        'raw': int, 'files': int, 'max_w': int
    }
    Pair keys are always sorted so (a,b) == (b,a).
    norm_score is computed afterwards as raw / max_raw across all pairs.
    """
    pairs: dict = defaultdict(lambda: {"raw": 0, "files": 0, "max_w": 0})

    n_files = 0
    for rdir in results_dirs:
        edge_files = sorted(rdir.glob("*EDGES.csv"))
        for ef in edge_files:
            etype = edge_type(ef.name)
            if etype not in use_types:
                continue
            n_files += 1
            with ef.open(encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    src = row.get("Source", "").strip()
                    tgt = row.get("Target", "").strip()
                    w   = int(row.get("Weight", 1))
                    if not src or not tgt or src == tgt:
                        continue
                    key = tuple(sorted([src, tgt]))
                    pairs[key]["raw"]   += w
                    pairs[key]["files"] += 1
                    pairs[key]["max_w"]  = max(pairs[key]["max_w"], w)

    return pairs, n_files


def norm_score(p: dict, max_raw: int) -> float:
    """Score relative to the most consistently co-clustered pair in the dataset."""
    if max_raw == 0:
        return 0.0
    return p["raw"] / max_raw


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results_dirs", nargs="+", metavar="RESULTS_DIR",
                    help="One or more stylo results directories containing EDGES.csv files")
    ap.add_argument("--bct-only", action="store_true", default=True,
                    help="Use only BCT edges (default)")
    ap.add_argument("--all-types", action="store_true",
                    help="Include CA and MDS edges in addition to BCT")
    ap.add_argument("--min-score", type=float, default=0.3,
                    help="Minimum norm_score to report (default 0.3)")
    ap.add_argument("--unknown-only", action="store_true",
                    help="Only report pairs where at least one text filename starts with 'unknown'")
    ap.add_argument("--top", type=int, default=None, metavar="N",
                    help="Report only the top N pairs")
    ap.add_argument("--out", metavar="FILE",
                    help="Write CSV to FILE instead of stdout")
    args = ap.parse_args()

    use_types = {"BCT"}
    if args.all_types:
        use_types = {"BCT", "CA", "MDS"}

    results_dirs = [Path(d) for d in args.results_dirs]
    for d in results_dirs:
        if not d.is_dir():
            print(f"[ERROR] Not a directory: {d}", file=sys.stderr)
            sys.exit(1)

    print(f"Scanning {len(results_dirs)} results director{'y' if len(results_dirs)==1 else 'ies'}…",
          file=sys.stderr)
    pairs, n_files = collect_edges(results_dirs, use_types)
    print(f"EDGES files read: {n_files}   Unique pairs found: {len(pairs):,}", file=sys.stderr)

    max_raw = max((p["raw"] for p in pairs.values()), default=1)

    # Rank
    ranked = sorted(pairs.items(), key=lambda x: norm_score(x[1], max_raw), reverse=True)

    # Filter
    filtered = []
    for (a, b), p in ranked:
        ns = norm_score(p, max_raw)
        if ns < args.min_score:
            break   # sorted, so no point continuing
        if args.unknown_only:
            if not (a.startswith("unknown") or b.startswith("unknown")):
                continue
        filtered.append((a, b, p, ns))

    if args.top:
        filtered = filtered[:args.top]

    # Output
    fieldnames = ["text_a", "text_b", "raw_score", "files_seen", "max_weight", "norm_score"]
    rows = [
        {
            "text_a": a,
            "text_b": b,
            "raw_score": p["raw"],
            "files_seen": p["files"],
            "max_weight": p["max_w"],
            "norm_score": f"{ns:.3f}",
        }
        for a, b, p, ns in filtered
    ]

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Written {len(rows)} pairs to {args.out}", file=sys.stderr)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
