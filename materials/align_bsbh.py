#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import math
from difflib import SequenceMatcher
from collections import defaultdict

WORD_RE = re.compile(r"[a-zāīūṛṝḷḹṅñṭḍṇśṣḥṃ’']+", re.IGNORECASE)

def normalize(s: str) -> str:
    s = s.lower()
    s = s.replace("‘", "'").replace("’", "'")
    words = WORD_RE.findall(s)
    return " ".join(words)

def words(s: str):
    return normalize(s).split()

def build_shingle_index(uns_lines, k=5, step=1):
    """
    Build an index from k-word shingles to candidate line positions.
    We index over the *entire* unsandhied token stream, but keep back-maps to line numbers.
    """
    # Flatten tokens with line backpointers
    token_stream = []
    token_to_line = []
    for i, line in enumerate(uns_lines):
        ws = words(line)
        for w in ws:
            token_stream.append(w)
            token_to_line.append(i)

    idx = defaultdict(list)
    for t in range(0, len(token_stream) - k + 1, step):
        sh = " ".join(token_stream[t:t+k])
        idx[sh].append(t)

    return idx, token_stream, token_to_line

def segment_text(seg_text: str):
    # Split on 2+ spaces OR newlines; drop empties
    raw = re.split(r"(?:\s{2,}|\n+)", seg_text.strip())
    segs = [normalize(x) for x in raw]
    return [s for s in segs if s]

def pick_candidate_token_positions(seg_norm: str, idx, k=5, max_shingles=30):
    ws = seg_norm.split()
    if len(ws) < k:
        return []

    # Take shingles spread across the segment
    if len(ws) - k + 1 <= max_shingles:
        shingle_positions = list(range(0, len(ws) - k + 1))
    else:
        # sample evenly
        shingle_positions = [int(round(i)) for i in
                            [j * (len(ws) - k) / (max_shingles - 1) for j in range(max_shingles)]]
        shingle_positions = sorted(set(shingle_positions))

    candidates = []
    for pos in shingle_positions:
        sh = " ".join(ws[pos:pos+k])
        candidates.extend(idx.get(sh, []))

    return candidates

def similarity(a: str, b: str) -> float:
    # SequenceMatcher is character-based; good enough on normalized word strings.
    return SequenceMatcher(None, a, b).ratio()

def tokens_to_line_range(token_to_line, start_token, end_token):
    # end_token is exclusive
    start_line = token_to_line[start_token]
    end_line = token_to_line[end_token - 1]
    return start_line, end_line

def slice_uns_window_by_token(token_stream, start_token, end_token):
    return " ".join(token_stream[start_token:end_token])

def main():
    if len(sys.argv) != 3:
        print("Usage: align_bsbh.py <unsandhied.txt> <segmented_complete.txt>", file=sys.stderr)
        sys.exit(2)

    uns_path, seg_path = sys.argv[1], sys.argv[2]

    with open(uns_path, "r", encoding="utf-8") as f:
        uns_lines = [line.rstrip("\n") for line in f if line.strip()]

    with open(seg_path, "r", encoding="utf-8") as f:
        seg_text = f.read()

    segs = segment_text(seg_text)

    print(f"Unsandhied: {len(uns_lines)} non-empty lines")
    print(f"Segmented:  {len(segs)} segments (split on 2+ spaces/newlines)")

    # Build index on unsandhied
    K = 5
    idx, token_stream, token_to_line = build_shingle_index(uns_lines, k=K, step=1)
    print(f"Unsandhied token stream: {len(token_stream)} tokens")
    print(f"Shingle index size: {len(idx)} unique {K}-word shingles")

    # Alignment parameters
    # We align segments to an unsandhied *token window* of roughly similar size.
    # Allow some slack (window_scale).
    window_scale = 1.35
    # Candidate search: try candidates, but keep only a manageable number
    max_candidates = 400
    # Monotonic alignment: we never go backwards in token_stream
    cursor_token = 0

    align_rows = []
    matched_token_ranges = []

    for sid, seg in enumerate(segs):
        seg_ws = seg.split()
        if not seg_ws:
            continue

        # Candidate positions via shingles
        cands = pick_candidate_token_positions(seg, idx, k=K, max_shingles=30)
        # Keep only candidates >= cursor_token (monotonic)
        cands = [c for c in cands if c >= cursor_token]
        if not cands:
            # No candidates: skip but record as unmatched
            align_rows.append((sid, -1, -1, -1, -1, 0.0))
            continue

        # Score candidates by building a plausible window around each candidate.
        # We treat candidate token position as an approximate start.
        seg_len = len(seg_ws)
        win_len = max(30, int(math.ceil(seg_len * window_scale)))

        # Deduplicate candidates (keep earliest occurrences)
        cands = sorted(set(cands))[:max_candidates]

        best = (0.0, None, None)  # (score, start_token, end_token)
        for c in cands:
            st = c
            en = min(len(token_stream), st + win_len)
            if en <= st + 5:
                continue
            cand_txt = slice_uns_window_by_token(token_stream, st, en)
            sc = similarity(seg, cand_txt)
            if sc > best[0]:
                best = (sc, st, en)

        score, st, en = best
        if st is None:
            align_rows.append((sid, -1, -1, -1, -1, 0.0))
            continue

        # Convert token range → line range
        line_start, line_end = tokens_to_line_range(token_to_line, st, en)
        align_rows.append((sid, st, en, line_start, line_end, score))
        matched_token_ranges.append((st, en, sid, score))

        # Advance cursor: move forward a bit past st (not to en, to tolerate varying window sizes)
        cursor_token = max(cursor_token, st + max(10, int(seg_len * 0.6)))

    # Write alignment TSV
    with open("alignment.tsv", "w", encoding="utf-8") as out:
        out.write("segment_id\tstart_token\tend_token\tstart_line\tend_line\tscore\n")
        for row in align_rows:
            out.write("\t".join(map(str, row)) + "\n")

    # Derive and write gaps: sort matched ranges by start_token, then look for big uncovered spans
    matched_token_ranges.sort()
    gaps = []
    prev_end = 0
    for (st, en, sid, sc) in matched_token_ranges:
        if st > prev_end:
            gaps.append((prev_end, st))
        prev_end = max(prev_end, en)
    if prev_end < len(token_stream):
        gaps.append((prev_end, len(token_stream)))

    # Filter to "significant" gaps (adjust threshold if needed)
    # Here: gaps spanning at least 2,000 tokens
    significant = [(a, b) for (a, b) in gaps if (b - a) >= 2000]

    def anchor_for_tokens(a, b, n=25):
        left = " ".join(token_stream[a:a+n])
        right = " ".join(token_stream[max(a, b-n):b])
        return left, right

    with open("gaps.txt", "w", encoding="utf-8") as out:
        out.write(f"Found {len(significant)} significant gaps (>=2000 tokens).\n\n")
        for gi, (a, b) in enumerate(significant, 1):
            ls, le = tokens_to_line_range(token_to_line, a, b)
            left, right = anchor_for_tokens(a, b)
            out.write(f"GAP {gi}: tokens {a}..{b}  (len={b-a})  ~ lines {ls}..{le}\n")
            out.write(f"  LEFT-ANCHOR : {left}\n")
            out.write(f"  RIGHT-ANCHOR: {right}\n\n")

    print("Wrote: alignment.tsv (segment → unsandhied line range + score)")
    print("Wrote: gaps.txt (large missing spans in segmented vs unsandhied)")

if __name__ == "__main__":
    main()