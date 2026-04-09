# Scripts Overview

This directory contains the main maintained analysis scripts for the repository.

## Main Scripts

- `install_packages.R`: installs the required R packages used by the maintained workflows.
- `clusters.R`: baseline clustering workflow for the main corpus. Accepts command-line flags for corpus path, feature type, MFW range, culling, consensus strength, plot dimensions, and per-group highlight colors.
- `clusters_command_builder.html`: static browser-based command builder for `clusters.R`.
- `clusters_tf_idf.R`: clustering workflow with additional TF-IDF / rare-word analysis.
- `cluster_w_indeclinables.R`: clustering workflow using a curated set of Sanskrit indeclinables as features.
- `indeclinables_mfw_variations.R`: repeats the indeclinables-based analysis across multiple MFW windows.
- `test_all_disputed.R`: runs General Imposters tests for all disputed texts in `corpus/main`.
- `test_all_disputed_w3g.R`: broader disputed-text GI suite across multiple n-gram and distance configurations.
- `comprehensive_gi_test.R`: configurable General Imposters runner with command-line options for target, candidates, feature counts, exclusions, and diagnostics.
- `comprehensive_gi_command_builder_app.R`: Shiny app that helps compose commands for `comprehensive_gi_test.R`.
- `comprehensive_gi_command_builder.html`: static browser-based command builder for the same workflow.

## Other Maintained Scripts

- `test_all_combinations.R`: exploratory GI test suite covering many combinations of n-gram types and distance metrics.

## Legacy Scripts

Older, one-off, or superseded helpers are kept in `legacy/`. See `legacy/README.md` for details.
