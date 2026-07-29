#!/bin/bash
# DICSEP 11 talk: C3 (char trigram) figure family on the n=127 corpus (talk 120 + Kirfel PPL).
# Run from the repo root. Results land in results_..._dicsep2026_n127_ppl_<ts>/.
set -e
exec Rscript scripts/clusters.R \
    --corpus-dir=corpus/epic_puranas_sandhied \
    --files-from=manifests/dicsep2026_n127_ppl.txt \
    --features=c --ngram-size=3 \
    --mfw-min=2000 --mfw-max=5000 --mfw-incr=1000 \
    "$@"
