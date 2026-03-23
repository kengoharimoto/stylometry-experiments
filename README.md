# Stylometric Experiments on Texts Attributed to Sankara

This repository contains the analysis scripts and minimal supporting files used for stylometric experiments related to prose writings attributed to Sankara.

The corpus itself is not distributed in this repository. The texts used for the underlying study came from:

https://github.com/JacekBakowski/stylometry/tree/main

This repo is intentionally kept lightweight so others can reproduce the experiments with their own prepared local corpus files.

## License

This repository is distributed under the CC BY 4.0 license. See `LICENSE`.

## What Is Included

- `scripts/`: R scripts for clustering and General Imposters experiments
- `scripts/legacy/`: older or one-off helper scripts retained for reference
- `materials/feature_sets/`: curated feature lists used by some GI runs
- `corpus/`: empty placeholder directories expected by the scripts
- `Makefile`: convenience commands for the main supported workflows

## What Is Not Included

- the study corpus
- generated results, PDFs, CSV exports, and notebook-oriented edge files
- ad hoc working files, scratch scripts, logs, and local editor metadata

## Expected Corpus Layout

Several scripts assume one of the following local directories exists:

- `corpus/main`
- `corpus/gi`
- `corpus/noroots`

The repository keeps these directories empty. Populate them locally with the text files you want to analyze.

## Dependencies

The scripts are written in R and currently rely on:

- `stylo`
- `shiny`

Install them with:

```r
install.packages(c("stylo", "shiny"))
```

Or run:

```bash
make install
```

## Reproducing Runs

1. Obtain or prepare the corpus files locally from the source corpus repository above.
2. Place the prepared texts into `corpus/main`, `corpus/gi`, or `corpus/noroots`, depending on the script you want to run.
3. Install the required R packages.
4. Run the scripts from the repository root.

Examples:

```bash
make help
make install
make gi-disputed
make gi-custom
Rscript scripts/test_all_disputed.R
Rscript scripts/test_all_disputed_w3g.R
Rscript scripts/comprehensive_gi_test.R --target=SomeTarget --candidates=CandidateA,CandidateB
Rscript scripts/clusters.R
```

## Notes

- Most scripts use relative paths and are meant to be run from the repository root.
- Output directories such as `results/` are generated locally and are ignored by Git.
- Corpus preparation and text normalization decisions materially affect the results. This repository does not attempt to recreate the full upstream corpus-preparation workflow.
- The main maintained entry points are exposed through `Makefile`. The underlying scripts are `scripts/clusters.R`, `scripts/clusters_tf_idf.R`, `scripts/cluster_w_indeclinables.R`, `scripts/indeclinables_mfw_variations.R`, `scripts/test_all_disputed.R`, `scripts/test_all_disputed_w3g.R`, and `scripts/comprehensive_gi_test.R`.
- The interactive command builder is `scripts/comprehensive_gi_command_builder_app.R`.
- Contribution guidance is in `CONTRIBUTING.md`.
