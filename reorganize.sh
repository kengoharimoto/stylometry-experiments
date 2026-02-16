#!/bin/bash
#
# Reorganize 2024-otao project directory
#
# This script moves files into a coherent structure. Nothing is deleted.
# Review the output, then run with: bash reorganize.sh
#
# To undo: the script prints every move. You can reverse them manually
# or restore from a backup (recommended: copy the dir before running).
#

set -euo pipefail

BASE="/Users/kengo_1/Desktop/stylometry-main/papers/2024-otao"
cd "$BASE"

echo "=== Reorganizing $BASE ==="
echo ""

# ─────────────────────────────────────────────
# 1. SCRIPTS — promote to top level
# ─────────────────────────────────────────────
echo "--- 1. Scripts ---"

mkdir -p scripts/scratch

# Production scripts
for f in \
    clusters.R \
    cluster_w_indeclinables.R \
    clusters_tf_idf.R \
    clusters_by_gemini.R \
    indeclinables_mfw_variations.R \
    test_all_disputed.R \
    test_all_disputed_w3g.R \
    test_all_combinations.R \
    top100.R
do
    [ -f "materials/R scripts/$f" ] && mv -v "materials/R scripts/$f" "scripts/$f"
done

# Scratch/debug scripts
for f in \
    debug.r \
    anotherdebug.r \
    debug_imposters.r \
    r_csv.r \
    r_instructions.r \
    test_with_imposters_function.r \
    test_all_combinations_v1.r \
    thepapertest.r
do
    [ -f "materials/R scripts/$f" ] && mv -v "materials/R scripts/$f" "scripts/scratch/$f"
done

# Shell script
[ -f "materials/organize_clusters.sh" ] && mv -v "materials/organize_clusters.sh" "scripts/organize_clusters.sh"

# Remove empty R scripts dir if empty
rmdir "materials/R scripts" 2>/dev/null || true

echo ""

# ─────────────────────────────────────────────
# 2. CORPUS — group under corpus/
# ─────────────────────────────────────────────
echo "--- 2. Corpus directories ---"

# Rename current corpus/ to a temp name, then nest it
mv -v "corpus" "corpus_main_tmp"
mkdir -p corpus
mv -v "corpus_main_tmp" "corpus/main"

[ -d "corpus_nospace" ]       && mv -v "corpus_nospace"       "corpus/nospace"
[ -d "corpus_orig" ]          && mv -v "corpus_orig"          "corpus/orig"
[ -d "corpus_test" ]          && mv -v "corpus_test"          "corpus/test"
[ -d "corpus_with_noroots" ]  && mv -v "corpus_with_noroots"  "corpus/with_noroots"
[ -d "corpus_noroots" ]       && mv -v "corpus_noroots"       "corpus/noroots"

echo ""

# ─────────────────────────────────────────────
# 3. RESULTS — group under results/
# ─────────────────────────────────────────────
echo "--- 3. Results directories ---"

mkdir -p results

# --- W1 50-100 (14 runs) ---
mkdir -p results/W1_50-100
for d in results_W1_50-100_*/; do
    ts="${d#results_W1_50-100_}"   # extract timestamp
    ts="${ts%/}"
    mv -v "$d" "results/W1_50-100/$ts"
done

# --- W1 50-80 (4 runs) ---
mkdir -p results/W1_50-80
for d in results_W1_50-80_*/; do
    ts="${d#results_W1_50-80_}"
    ts="${ts%/}"
    mv -v "$d" "results/W1_50-80/$ts"
done

# --- W1 600-1000 ---
for d in results_W1_600-1000_*/; do
    ts="${d#results_W1_600-1000_}"
    ts="${ts%/}"
    mkdir -p results/W1_600-1000
    mv -v "$d" "results/W1_600-1000/$ts"
done

# --- W1 10000-15000 ---
for d in results_W1_10000-15000_*/; do
    ts="${d#results_W1_10000-15000_}"
    ts="${ts%/}"
    mkdir -p results/W1_10000-15000
    mv -v "$d" "results/W1_10000-15000/$ts"
done

# --- C3 2000-5000 (9 runs) ---
mkdir -p results/C3_2000-5000
for d in results_C3_2000-5000_*/; do
    ts="${d#results_C3_2000-5000_}"
    ts="${ts%/}"
    mv -v "$d" "results/C3_2000-5000/$ts"
done

# --- C3 1000-3000 ---
for d in results_C3_1000-3000_*/; do
    ts="${d#results_C3_1000-3000_}"
    ts="${ts%/}"
    mkdir -p results/C3_1000-3000
    mv -v "$d" "results/C3_1000-3000/$ts"
done

# --- Indeclinables ---
mkdir -p results/indeclinables
[ -d "clusters_indeclinables_20260212_165243" ] && \
    mv -v "clusters_indeclinables_20260212_165243" "results/indeclinables/20260212_165243"
[ -d "clusters_indeclinables_20260212_164753" ] && \
    mv -v "clusters_indeclinables_20260212_164753" "results/indeclinables/20260212_164753"
[ -d "clusters_indeclinables" ] && \
    mv -v "clusters_indeclinables" "results/indeclinables/old"

# --- Indeclinables MFW variations ---
[ -d "results_indeclinables_mfw_variations_20260212_170400" ] && \
    mv -v "results_indeclinables_mfw_variations_20260212_170400" "results/indeclinables/mfw_variations_20260212_170400"

# --- W1 100-500 corpus variants ---
mkdir -p results/W1_100-500
[ -d "clusters_W1_100-500" ] && \
    mv -v "clusters_W1_100-500" "results/W1_100-500/base"
[ -d "clusters_W1_100-500 with commentaries" ] && \
    mv -v "clusters_W1_100-500 with commentaries" "results/W1_100-500/with_commentaries"
[ -d "clusters_W1_100-500 with Borrowers" ] && \
    mv -v "clusters_W1_100-500 with Borrowers" "results/W1_100-500/with_borrowers"
[ -d "clusters_W1_100-500 after file name changes" ] && \
    mv -v "clusters_W1_100-500 after file name changes" "results/W1_100-500/final"

# --- C3 from corpus_nospace ---
mkdir -p results/C3_nospace
[ -d "clusters c3 1000–5000" ] && \
    mv -v "clusters c3 1000–5000" "results/C3_nospace/1000-5000"
[ -d "clusters c3 500" ] && \
    mv -v "clusters c3 500" "results/C3_nospace/500"

# --- Standalone W1 100 runs ---
mkdir -p results/W1_100
[ -d "clusters_W1_100" ] && \
    mv -v "clusters_W1_100" "results/W1_100/scripted"
[ -d "clusters w1 100" ] && \
    mv -v "clusters w1 100" "results/W1_100/manual"
[ -d "clusters_C3" ] && \
    mv -v "clusters_C3" "results/C3_early"

# --- GI (General Imposters) results ---
mkdir -p results/GI
[ -d "gi results" ] && \
    mv -v "gi results" "results/GI/20260202"
[ -d "gi results 20260201" ] && \
    mv -v "gi results 20260201" "results/GI/20260201"

# --- Early experiments with space-named dirs ---
mkdir -p results/early

[ -d "clusters BCT 100-500 c3" ] && \
    mv -v "clusters BCT 100-500 c3" "results/early/BCT_100-500_c3"

# Note: this dir name has a Unicode minus sign (−), not a regular hyphen
[ -d "clusters BCT 100−500 MFW" ] && \
    mv -v "clusters BCT 100−500 MFW" "results/early/BCT_100-500_MFW"

# Note: this dir name has an en-dash (–)
[ -d "clusters BCT 100–500 MFW 2-grams" ] && \
    mv -v "clusters BCT 100–500 MFW 2-grams" "results/early/BCT_100-500_MFW_2grams"
[ -d "clusters BCT 100–500 MFW 2-grams old" ] && \
    mv -v "clusters BCT 100–500 MFW 2-grams old" "results/early/BCT_100-500_MFW_2grams_old"

[ -d "clusters CA 500 c3" ] && \
    mv -v "clusters CA 500 c3" "results/early/CA_500_c3"
[ -d "clusters CA 500 MFW" ] && \
    mv -v "clusters CA 500 MFW" "results/early/CA_500_MFW"
[ -d "clusters CA 500 MFW 2-grams" ] && \
    mv -v "clusters CA 500 MFW 2-grams" "results/early/CA_500_MFW_2grams"

[ -d "clusters MDS 500 MFW" ] && \
    mv -v "clusters MDS 500 MFW" "results/early/MDS_500_MFW"
[ -d "clusters MDS 500 MFW 2-grams" ] && \
    mv -v "clusters MDS 500 MFW 2-grams" "results/early/MDS_500_MFW_2grams"
[ -d "clusters MDS c3 500" ] && \
    mv -v "clusters MDS c3 500" "results/early/MDS_500_c3"

[ -d "clusters PCR 500 c3" ] && \
    mv -v "clusters PCR 500 c3" "results/early/PCR_500_c3"
[ -d "clusters PCR 500 MFW" ] && \
    mv -v "clusters PCR 500 MFW" "results/early/PCR_500_MFW"
[ -d "clusters PCR 500 MFW 2-grams" ] && \
    mv -v "clusters PCR 500 MFW 2-grams" "results/early/PCR_500_MFW_2grams"

[ -d "clusters PCV 500 c3" ] && \
    mv -v "clusters PCV 500 c3" "results/early/PCV_500_c3"
[ -d "clusters PCV 500 MFW" ] && \
    mv -v "clusters PCV 500 MFW" "results/early/PCV_500_MFW"
[ -d "clusters PCV 500 MFW 2-grams" ] && \
    mv -v "clusters PCV 500 MFW 2-grams" "results/early/PCV_500_MFW_2grams"

[ -d "preparatory experiments" ] && \
    mv -v "preparatory experiments" "results/early/preparatory"

echo ""

# ─────────────────────────────────────────────
# 4. MATERIALS — organize loose files
# ─────────────────────────────────────────────
echo "--- 4. Materials ---"

# Vivarana files
mkdir -p materials/vivarana
for f in vivarana_part_unsandhied.txt vivarana_unsandhied.txt; do
    [ -f "$f" ] && mv -v "$f" "materials/vivarana/$f"
done
for f in materials/vivarana_*.txt; do
    [ -f "$f" ] && mv -v "$f" "materials/vivarana/"
done
[ -f "materials/vivarana_segmented_compelete.json" ] && \
    mv -v "materials/vivarana_segmented_compelete.json" "materials/vivarana/"
[ -f "materials/vivarana_segmented.text" ] && \
    mv -v "materials/vivarana_segmented.text" "materials/vivarana/"
[ -f "materials/vivarana_sentence_segments.txt" ] && \
    mv -v "materials/vivarana_sentence_segments.txt" "materials/vivarana/"
[ -f "materials/vivarana_alpha_only.txt" ] && \
    mv -v "materials/vivarana_alpha_only.txt" "materials/vivarana/"

# Disputed source texts — gather scattered copies
mkdir -p materials/disputed_source
[ -d "disputed" ] && mv -v "disputed" "materials/disputed_source/nospace_corpus"
for f in Disputed_019_YSBhV_segmented_excerpt.txt \
         Disputed0_017_YSBhV_unsegmented_excerpt.txt \
         Disputed0_YSBhV_excerpt_segmented.txt; do
    [ -f "$f" ] && mv -v "$f" "materials/disputed_source/$f"
done
# Also gather the ones inside materials/
for f in materials/Disputed_017_YSBhV_*.txt materials/017_YSBhV_*.txt; do
    [ -f "$f" ] && mv -v "$f" "materials/disputed_source/"
done

# BSBh
[ -f "TheSankara_BSBh_segmented_complete.txt" ] && \
    mv -v "TheSankara_BSBh_segmented_complete.txt" "materials/bsbh/"
[ -f "materials/Sankara_BSBh_rev_whole.txt" ] && \
    mv -v "materials/Sankara_BSBh_rev_whole.txt" "materials/bsbh/"
[ -f "materials/mahabhasya.txt" ] && \
    mv -v "materials/mahabhasya.txt" "materials/"
[ -f "materials/Disputed_020_Patanjali_mahabhasya.txt" ] && \
    mv -v "materials/Disputed_020_Patanjali_mahabhasya.txt" "materials/"

echo ""

# ─────────────────────────────────────────────
# 5. ARCHIVE — collect junk/old/non-essential
# ─────────────────────────────────────────────
echo "--- 5. Archive ---"

mkdir -p archive/zips archive/numbers archive/misc archive/plots

# Zip files
for f in *.zip; do
    [ -f "$f" ] && mv -v "$f" "archive/zips/$f"
done

# .numbers files (Apple-specific)
for f in *.numbers; do
    [ -f "$f" ] && mv -v "$f" "archive/numbers/$f"
done
[ -f "materials/distance_matrix_300MFW.numbers" ] && \
    mv -v "materials/distance_matrix_300MFW.numbers" "archive/numbers/"
[ -f "materials/correspondances in the bsbh files.numbers" ] && \
    mv -v "materials/correspondances in the bsbh files.numbers" "archive/numbers/"

# Old plots
[ -d "Plots 20260202" ] && mv -v "Plots 20260202" "archive/plots/20260202"
[ -d "too old" ]         && mv -v "too old" "archive/plots/too_old"

# Distance matrices (.numbers)
[ -d "distant metrixes" ] && mv -v "distant metrixes" "archive/numbers/distance_matrices"

# Misc loose files
for f in Rplot.pdf stylo_config.txt table_with_frequencies.txt wordlist.txt \
         .Rhistory analyze_disputed.py; do
    [ -f "$f" ] && mv -v "$f" "archive/misc/$f"
done

# Root-level EDGES CSVs (copies exist in csvs/)
for f in 2024-otao_CA_*_EDGES.csv; do
    [ -f "$f" ] && mv -v "$f" "csvs/$f"
done

# Empty data dir
[ -d "data" ] && rmdir "data" 2>/dev/null && echo "Removed empty data/" || true

# Refuge (extra text files not in corpus)
[ -d "refuge" ] && mv -v "refuge" "materials/refuge"

# BSBh dir from root level
[ -d "bsbh" ] && mv -v "bsbh" "materials/bsbh_root"

echo ""

# ─────────────────────────────────────────────
# 6. UPDATE R SCRIPTS — fix corpus paths
# ─────────────────────────────────────────────
echo "--- 6. Updating R script corpus paths ---"

# Most scripts: "corpus" → "corpus/main"
for f in scripts/cluster_w_indeclinables.R \
         scripts/clusters_tf_idf.R \
         scripts/clusters_by_gemini.R \
         scripts/indeclinables_mfw_variations.R \
         scripts/test_all_disputed.R \
         scripts/test_all_disputed_w3g.R \
         scripts/test_all_combinations.R; do
    if [ -f "$f" ]; then
        if grep -q 'CORPUS_DIR <- "corpus"' "$f"; then
            sed -i '' 's|CORPUS_DIR <- "corpus"|CORPUS_DIR <- "corpus/main"|' "$f"
            echo "Updated $f: corpus → corpus/main"
        fi
    fi
done

# clusters.R uses corpus_noroots
if [ -f "scripts/clusters.R" ]; then
    if grep -q 'CORPUS_DIR <- "corpus_noroots"' "scripts/clusters.R"; then
        sed -i '' 's|CORPUS_DIR <- "corpus_noroots"|CORPUS_DIR <- "corpus/noroots"|' "scripts/clusters.R"
        echo "Updated scripts/clusters.R: corpus_noroots → corpus/noroots"
    fi
fi

echo ""

# ─────────────────────────────────────────────
# 7. CLEAN UP — remove .DS_Store files
# ─────────────────────────────────────────────
echo "--- 7. Cleanup ---"
find . -name ".DS_Store" -delete -print 2>/dev/null || true

echo ""
echo "=== Done ==="
echo ""
echo "New structure:"
echo "  corpus/          - all corpus variants (main, nospace, orig, etc.)"
echo "  scripts/         - R scripts (production + scratch/)"
echo "  materials/       - source texts, alignment tools, reference data"
echo "  results/         - all experiment results grouped by feature type"
echo "  csvs/            - standalone EDGES CSVs"
echo "  archive/         - zips, .numbers, old plots, misc working files"
echo ""
echo "To run an R script:  Rscript scripts/clusters.R"
echo "(Scripts use corpus/main or corpus/noroots — edit CORPUS_DIR as needed)"
