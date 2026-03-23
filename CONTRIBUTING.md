# Contributing

## Scope

This repository is intended to remain a lightweight, reproducible analysis repo.

Please avoid adding:

- corpus files
- generated results
- editor or machine-local files
- large archives or exploratory exports

## Workflow

1. Keep analysis scripts runnable from the repository root with relative paths.
2. Put older or one-off helpers in `scripts/legacy/` rather than mixing them with the main entry points.
3. Keep `corpus/` empty in Git; use only the placeholder directories already provided.
4. Prefer updating documentation when changing script assumptions, dependencies, or expected directory layout.

## Dependencies

- Use base R plus clearly declared packages where possible.
- If a new package is required, update `scripts/install_packages.R` and `README.md`.

## Outputs

- Write generated outputs to ignored directories such as `results/`.
- Do not commit regenerated PDFs, CSVs, logs, or notebook-oriented exports unless they are explicitly curated for release.
