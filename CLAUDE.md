# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Stylometric analysis of Sanskrit philosophical texts to investigate the authenticity of prose writings attributed to Śaṅkara (8th c. CE). Uses the R `stylo` package to perform computational text analysis on a corpus of ~78 unsandhied Sanskrit texts spanning multiple philosophical traditions.

The core research question involves relationships between three key texts:
- **Patanjali_PYS** — Yoga Sutras (2nd c. BCE)
- **Disputed0_yvi** — Yoga Vivarana (disputed commentary, attributed to Śaṅkara)
- **TheSankara_BSBh_rev_whole** — Brahma Sutra Bhashya (authenticated Śaṅkara work)

## Running R Scripts

All R scripts are in `materials/R scripts/`. Run from the project root:

```bash
cd /Users/kengo_1/Desktop/stylometry-main/papers/2024-otao
Rscript "materials/R scripts/clusters.R"
Rscript "materials/R scripts/cluster_w_indeclinables.R"
Rscript "materials/R scripts/indeclinables_mfw_variations.R"
```

Scripts require: R with `stylo` package (v0.7.5+). Install with `install.packages("stylo")`.

**Key performance pattern**: Load the corpus once with an initial `stylo()` call using `corpus.dir`, extract `freq_table <- initial_results$table.with.all.freqs`, then pass `frequencies = freq_table` to all subsequent `stylo()` calls. This avoids re-reading/re-tokenizing 78 text files on every iteration.

## Corpus Directories

- **`corpus/`** — Main corpus (78 texts, full versions including root texts)
- **`corpus_noroots/`** — Commentaries with root text passages removed (13 texts: Sankara bhashyas + Borrowers)
- **`corpus_with_noroots/`** — Full corpus + noroot variants combined
- **`corpus_nospace/`** — Numbered/segmented versions for different experiments

Text filename convention: `Category_Author_Work.txt` where Category is one of:
`Bauddha`, `Borrowers`, `Disputed`, `Disputed0`, `Doubtful`, `Mimamsa`, `Nyaya`, `Others`, `Patanjali`, `Samkhya`, `Sankara`, `TheSankara`, `Upanisad`, `Vedantin`

## Results Directory Structure

Results are in timestamped directories named by configuration:
- `results_W1_50-100_YYYYMMDD_HHMMSS/` — Word unigrams, MFW range 50-100
- `results_C3_2000-5000_YYYYMMDD_HHMMSS/` — Character trigrams, MFC range 2000-5000
- `clusters_indeclinables_YYYYMMDD_HHMMSS/` — Indeclinables-only analysis
- `results_indeclinables_mfw_variations_YYYYMMDD_HHMMSS/` — 10 MFW variation tests

Each results directory contains:
- **`*EDGES.csv`** — Primary data files. Format: `Source,Target,Weight,Type`. Weight = number of times two texts cluster together across iterations (higher = more similar). These are the main files used for cross-test analysis.
- **`*.pdf`** — Visual plots (CA dendrograms, BCT consensus trees, MDS scatter plots, PCV biplots)
- **`*DISTANCES.csv`** — Distance matrices between texts

## Analysis Types and Parameters

**Analysis methods** (set via `analysis.type` in stylo):
- `BCT` — Bootstrap Consensus Tree: iterates over MFW range, most robust for separation analysis
- `CA` — Correspondence Analysis: single-point dendrogram
- `MDS` — Multidimensional Scaling: 2D scatter plot
- `PCV` — Principal Components: biplot (no distance measure needed)

**Distance metrics** (set via `distance.measure`):
`delta`, `argamon`, `eder`, `simple`, `canberra`, `manhattan`, `euclidean`, `cosine`, `wurzburg`, `minmax`

**Feature types**:
- W1 (word unigrams): `analyzed.features="w"`, `ngram.size=1`
- C3 (character trigrams): `analyzed.features="c"`, `ngram.size=3`
- Indeclinables: pass a curated list of 59 Sanskrit grammatical particles via `features` parameter, then use `frequencies = freq_table` with the filtered table

## Key Script Architecture

**`clusters.R`** — Main analysis script. Loads corpus once, runs PCV, then loops over 10 distance metrics × 3 methods (CA, BCT, MDS) = 31 total analyses. Uses `corpus_noroots`.

**`cluster_w_indeclinables.R`** — Same architecture but filters frequency table to 55 Sanskrit indeclinables (avyaya). Uses `corpus` directory. The indeclinables list includes particles like `ca`, `tu`, `hi`, `eva`, `api`, `na`, `iti`, etc.

**`indeclinables_mfw_variations.R`** — Runs 10 MFW range variations × 10 metrics × 3 methods = 300 tests to assess robustness.

**`clusters_tf_idf.R`** — TF-IDF weighted variant (generally flattens differences compared to regular clustering).

## Analyzing EDGES Files Programmatically

To compare text relationships across tests, normalize EDGES weights:
```python
ratio = weight / max_weight_in_file  # 0.0 to 1.0
```
This allows comparison across files with different iteration counts. A ratio < 0.25 = weak connection, 0.25-0.50 = moderate, ≥ 0.50 = strong. If two texts share no edge in a file, they never clustered together in that test.

There are ~1,600+ EDGES files across all results directories. Use `glob` patterns like `results_*/*EDGES*` and `clusters_indeclinables_*/*EDGES*` to find them.
