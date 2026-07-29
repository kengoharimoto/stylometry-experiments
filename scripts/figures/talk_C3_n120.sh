#!/bin/bash
# DICSEP 11 talk: C3 (char trigram) figure family on the n=120 corpus.
# Run from the repo root. Results land in results_..._dicsep2026_n120_<ts>/.
set -e
exec Rscript scripts/clusters.R \
    --corpus-dir=corpus/epic_puranas_sandhied \
    --files-from=manifests/dicsep2026_n120.txt \
    --features=c --ngram-size=3 \
    --mfw-min=2000 --mfw-max=5000 --mfw-incr=1000 \
    "$@"
