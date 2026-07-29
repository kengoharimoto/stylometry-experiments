#!/bin/bash
# DICSEP 11 talk: W1 (word unigram) figure family on the n=120 corpus.
# Run from the repo root. Results land in results_..._dicsep2026_n120_<ts>/.
set -e
exec Rscript scripts/clusters.R \
    --corpus-dir=corpus/epic_puranas_unsandhied \
    --files-from=manifests/dicsep2026_n120.txt \
    --features=w --ngram-size=1 \
    --mfw-min=50 --mfw-max=80 --mfw-incr=10 \
    "$@"
