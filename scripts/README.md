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
- `delta_nn_test.R`: Delta nearest-neighbor attribution. For a given target text, ranks every other text in the corpus by stylistic distance across all available distance measures and two feature types (character trigrams and word unigrams). Reports each candidate's rank and distance per configuration, with an aggregated summary (mean rank, median rank, % in top-1/3/5/10) across all configurations. Deterministic — no imposter pool or random sampling, so results are reproducible and scale cleanly to large corpora. Saves a per-config CSV and a top-N CSV to `results/`. See the flag reference below.
- `delta_nn_command_builder.html`: static browser-based command builder for `delta_nn_test.R`.

### `clusters.R` flag reference

| Flag | Default | Description |
|---|---|---|
| `--corpus-dir=PATH` | `corpus/main` | Corpus directory |
| `--features=w\|c` | `w` | Feature type: `w` = words, `c` = characters |
| `--ngram-size=N` | `1` | N-gram size (1 = unigrams, 3 = trigrams, etc.) |
| `--mfw-min=N` | `50` | Minimum MFW value in the sweep |
| `--mfw-max=N` | `80` | Maximum MFW value in the sweep |
| `--mfw-incr=N` | `10` | MFW step size |
| `--culling-min=N` | `0` | Minimum culling percentage |
| `--culling-max=N` | `0` | Maximum culling percentage |
| `--culling-incr=N` | `0` | Culling step size |
| `--consensus-strength=N` | `0.5` | Consensus tree strength threshold (0–1) |
| `--preserve-case` | | Keep original case (default: lowercase) |
| `--plot-height=N` | `60` | PDF plot height in inches |
| `--plot-width=N` | `50` | PDF plot width in inches |
| `--plot-font-size=N` | `7` | Plot label font size |
| `--exclude=PATTERN` | | Regex applied to filenames to exclude texts |
| `--highlight=G:COLOR,...` | | Comma-separated `group_prefix:color` pairs for per-group label colors, e.g. `sankara:#d62728,ramanuja:#1f77b4` |

Scripts without CLI flags (`clusters_tf_idf.R`, `cluster_w_indeclinables.R`, `indeclinables_mfw_variations.R`, `test_all_disputed.R`, `test_all_disputed_w3g.R`, `test_all_combinations.R`) are configured by editing the variables at the top of the script.

### `comprehensive_gi_test.R` flag reference

| Flag | Default | Description |
|---|---|---|
| `--target=NAME` | *(required)* | Filename stem of the target text |
| `--candidate=NAME` | | A candidate text; may be repeated |
| `--candidates=A,B,C` | | Comma-separated candidate list |
| `--candidate-regex=PATTERN` | | Select candidates by regex |
| `--exclude-imposters=A,B,C` | | Comma-separated imposter exclusion list |
| `--exclude-imposter=NAME` | | Exclude a single imposter; may be repeated |
| `--exclude-imposters-regex=PATTERN` | | Exclude imposters matching a regex |
| `--feature-count=N` | | Sets both trigram and unigram MFW to N |
| `--feature-count-trigrams=N` | `2000` | Character trigram MFW |
| `--feature-count-unigrams=N` | `2000` | Word unigram MFW |
| `--feature-set=PATH` | | Fixed word list to use as features; disables trigram tests |
| `--feature-sample-rate=N` | `0.5` | Fraction of features sampled per iteration |
| `--imposter-sample-rate=N` | `0.5` | Fraction of imposter pool sampled per iteration |
| `--max-imposters=N` | unlimited | Cap the imposter pool to N randomly-drawn texts. Recommended: 30–50 for large corpora |
| `--min-imposter-feature-multiplier=N` | `1.0` | Exclude imposters whose vocabulary is smaller than N × MFW. Set to `2.0` for a conservative threshold; `0` to disable |
| `--iterations=N` | `100` | Number of GI iterations |
| `--diagnostic-mode` | | Use full feature and imposter sets; print closest-text distances |
| `--diagnostic-top-n=N` | `10` | Number of closest texts shown in diagnostic mode |
| `--use-builtin` | | Use stylo's built-in `imposters()` function instead of the custom loop |
| `--corpus-dir=PATH` | `corpus/gi` | Corpus directory |
| `--note=TEXT` | | Short note written at the top of the log |

**Outputs** (written to `results/`):

- `gi_results_TIMESTAMP.txt` — full run log.
- `gi_results_TIMESTAMP.csv` — one row per configuration: setup name, GI score, successful and skipped iterations.
- `gi_iterations_TIMESTAMP.csv` — one row per iteration × configuration: winner, candidate distance, imposter distance, closest candidate, closest imposter.

### `delta_nn_test.R` flag reference

| Flag | Default | Description |
|---|---|---|
| `--target=NAME` | *(required)* | Filename stem of the target text |
| `--candidate=NAME` | | A known-author text to track; may be repeated |
| `--candidates=A,B,C` | | Comma-separated candidate list |
| `--candidate-regex=PATTERN` | | Select candidates by regex |
| `--exclude=A,B,C` | | Texts to omit from the ranking (comma-separated) |
| `--exclude-regex=PATTERN` | | Omit texts matching a regex |
| `--feature-count=N` | `2000` / `200` | Sets both trigram and unigram MFW to N |
| `--feature-count-trigrams=N` | `2000` | Character trigram MFW |
| `--feature-count-unigrams=N` | `200` | Word unigram MFW |
| `--feature-set=PATH` | | Fixed word list to use as features; disables trigram tests |
| `--top-n=N` | `10` | Number of closest texts printed per configuration |
| `--corpus-dir=PATH` | `corpus/gi` | Corpus directory |
| `--note=TEXT` | | Short note written at the top of the log |

**Outputs** (written to `results/`):

- `delta_nn_TIMESTAMP.csv` — one row per configuration × candidate: config name, candidate name, rank, total texts ranked, distance.
- `delta_nn_topn_TIMESTAMP.csv` — one row per configuration × rank position (up to `--top-n`): config, rank, text name, distance, whether the text is a candidate.
- `delta_nn_TIMESTAMP.txt` — full run log mirroring stdout.

**Relationship to GI:** nearest-neighbor attribution asks *who in the corpus is closest to the target* rather than *is the target by candidate A or not*. It does not require an imposter pool and is not affected by pool size. It is however sensitive to topic confounds (e.g. two commentaries on the same base text will share vocabulary regardless of authorship); use `--exclude-regex` or `--exclude` to remove known same-genre texts when this is a concern.

## Other Maintained Scripts

- `test_all_combinations.R`: exploratory GI test suite covering many combinations of n-gram types and distance metrics.

## Legacy Scripts

Older, one-off, or superseded helpers are kept in `legacy/`. See `legacy/README.md` for details.
