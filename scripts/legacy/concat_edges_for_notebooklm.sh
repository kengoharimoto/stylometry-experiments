#!/usr/bin/env bash
set -euo pipefail

# Concatenate EDGES CSV files into bundles for NotebookLM upload.
# Adds a "File" column with the source filename so configurations are traceable.
# Large bundles are split into parts to stay under NotebookLM's ~500K field limit.

RESULTS_DIR="results"
OUT_DIR="notebooklm_edges"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

# Concatenate EDGES files from one or more directories into a single CSV.
concat_bundle() {
  local bundle_name="$1"
  shift
  local search_dirs=("$@")

  local outfile="$OUT_DIR/${bundle_name}.csv"
  local count=0

  echo "File,Source,Target,Weight,Type" > "$outfile"

  for dir in "${search_dirs[@]}"; do
    if [[ ! -d "$RESULTS_DIR/$dir" ]]; then
      echo "  SKIP (not found): $RESULTS_DIR/$dir"
      continue
    fi
    while IFS= read -r -d '' f; do
      local relpath="${f#$RESULTS_DIR/}"
      tail -n +2 "$f" | while IFS= read -r line; do
        echo "$relpath,$line"
      done >> "$outfile"
      count=$((count + 1))
    done < <(find "$RESULTS_DIR/$dir" -name '*EDGES*' -type f -print0 | sort -z)
  done

  local size rows fields
  size=$(wc -c < "$outfile" | tr -d ' ')
  rows=$(tail -n +2 "$outfile" | wc -l | tr -d ' ')
  fields=$(awk -F',' '{t+=NF}END{print t}' "$outfile")
  printf "  %-40s %4d files  %7d rows  %8d fields  %s\n" \
    "$bundle_name.csv" "$count" "$rows" "$fields" \
    "$(numfmt --to=iec "$size" 2>/dev/null || echo "${size}B")"
}

report_file() {
  local label="$1" outfile="$2" count="$3"
  local size rows fields
  size=$(wc -c < "$outfile" | tr -d ' ')
  rows=$(tail -n +2 "$outfile" | wc -l | tr -d ' ')
  fields=$(awk -F',' '{t+=NF}END{print t}' "$outfile")
  printf "  %-40s %4d files  %7d rows  %8d fields  %s\n" \
    "$label" "$count" "$rows" "$fields" \
    "$(numfmt --to=iec "$size" 2>/dev/null || echo "${size}B")"
}

echo "Concatenating EDGES files into $OUT_DIR/"
echo "============================================"

# --- W1_50-100: split 3 parts (~260-360K fields each) ---
concat_bundle "W1_50-100_part1" \
  "W1_50-100/20260207_192248" \
  "W1_50-100/20260208_160625" \
  "W1_50-100/20260209_120031" \
  "W1_50-100/20260209_131543"

concat_bundle "W1_50-100_part2" \
  "W1_50-100/20260209_134446" \
  "W1_50-100/20260209_141036" \
  "W1_50-100/20260209_143757" \
  "W1_50-100/20260209_150942"

concat_bundle "W1_50-100_part3" \
  "W1_50-100/20260209_155606" \
  "W1_50-100/20260212_145548" \
  "W1_50-100/20260212_154625"

# --- W1_50-80: split 2 parts (~232K + ~197K fields) ---
concat_bundle "W1_50-80_part1" \
  "W1_50-80/20260211_170540" \
  "W1_50-80/20260211_173920" \
  "W1_50-80/20260211_175329" \
  "W1_50-80/20260211_175826"

concat_bundle "W1_50-80_part2" \
  "results_W1_50-80_20260213_173042" \
  "results_W1_50-80_20260214_185336" \
  "results_W1_50-80_20260214_185950"

concat_bundle "W1_100"         "W1_100"

# --- W1_100-500: split 2 parts (~150K + ~157K fields) ---
concat_bundle "W1_100-500_part1" \
  "W1_100-500/base" \
  "W1_100-500/final"

concat_bundle "W1_100-500_part2" \
  "W1_100-500/with_borrowers" \
  "W1_100-500/with_commentaries"

concat_bundle "W1_600-1000"    "W1_600-1000"
concat_bundle "W1_10000-15000" "W1_10000-15000"

# --- C3_2000-5000: split 2 parts ---
concat_bundle "C3_2000-5000_part1" \
  "C3_2000-5000/20260209_161855" \
  "C3_2000-5000/20260209_191552" \
  "C3_2000-5000/20260210_130948" \
  "C3_2000-5000/20260210_154647" \
  "C3_2000-5000/20260211_160216"

concat_bundle "C3_2000-5000_part2" \
  "C3_2000-5000/20260211_161132" \
  "C3_2000-5000/20260211_161506" \
  "C3_2000-5000/20260211_162913" \
  "C3_2000-5000/20260211_165022"

concat_bundle "C3_other" \
  "C3_1000-3000" "C3_early" "C3_nospace"

# --- Indeclinables main (OK as-is) ---
concat_bundle "indeclinables_main" \
  "indeclinables/20260212_164753" \
  "indeclinables/20260212_165243" \
  "indeclinables/old"

# --- Indeclinables MFW variations: split 2 parts by file order ---
INDECL_DIR="$RESULTS_DIR/indeclinables/mfw_variations_20260212_170400"

# Build file list portably (handles spaces in filenames)
INDECL_TOTAL=0
while IFS= read -r -d '' f; do
  eval "INDECL_FILE_${INDECL_TOTAL}=\"\$f\""
  INDECL_TOTAL=$((INDECL_TOTAL + 1))
done < <(find "$INDECL_DIR" -name '*EDGES*' -type f -print0 | sort -z)
INDECL_HALF=$(( INDECL_TOTAL / 2 ))

for part in 1 2; do
  outfile="$OUT_DIR/indeclinables_mfw_part${part}.csv"
  echo "File,Source,Target,Weight,Type" > "$outfile"
  count=0

  if [[ $part -eq 1 ]]; then
    start=0; end=$INDECL_HALF
  else
    start=$INDECL_HALF; end=$INDECL_TOTAL
  fi

  for (( i=start; i<end; i++ )); do
    eval "f=\"\$INDECL_FILE_${i}\""
    relpath="${f#$RESULTS_DIR/}"
    tail -n +2 "$f" | while IFS= read -r line; do
      echo "$relpath,$line"
    done >> "$outfile"
    count=$((count + 1))
  done

  report_file "indeclinables_mfw_part${part}.csv" "$outfile" "$count"
done

# --- Early: split 2 parts (~183K + ~180K fields) ---
concat_bundle "early_part1" \
  "early/BCT_100-500_MFW" \
  "early/BCT_100-500_MFW_2grams" \
  "early/BCT_100-500_MFW_2grams_old" \
  "early/BCT_100-500_c3" \
  "early/CA_500_MFW" \
  "early/CA_500_MFW_2grams"

concat_bundle "early_part2" \
  "early/CA_500_c3" \
  "early/MDS_500_MFW" \
  "early/MDS_500_MFW_2grams" \
  "early/MDS_500_c3" \
  "early/preparatory"

echo ""
echo "Done. Output in $OUT_DIR/"
echo ""
ls -lh "$OUT_DIR/"
echo ""
echo "Total bundle files: $(ls "$OUT_DIR/"*.csv | wc -l | tr -d ' ')"
