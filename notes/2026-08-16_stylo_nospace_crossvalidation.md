# Stylo cross-validation of the no-space C3-500: exact agreement

2026-08-16. The adopted no-space C3 convention rested on the Python pipeline
alone (the hero_mds wordlist validation is skipped under `--strip-spaces`;
flagged in the adoption note). Closed today: R stylo run on a pre-stripped
corpus, an independent code path from raw text to distance matrix.

## Method

- `scripts/build_nospace_sandhied_corpus.py` writes
  `corpus/epic_puranas_sandhied_nospace/`: each of the 127 manifest units
  from the colophon-free sandhied corpus as a single line with every
  whitespace character deleted. Under stylo's whitespace splitting rule each
  file is one token, so stylo's char-3-grams run over the identical
  continuous stream as `hero_mds.py --strip-spaces` (lowercasing via
  `preserve.case = FALSE`).
- `scripts/clusters.R --corpus-dir=corpus/epic_puranas_sandhied_nospace
  --features=c --ngram-size=3 --mfw-min=500 --mfw-max=500
  --files-from=manifests/dicsep2026_n127_ppl.txt` →
  `results_epic_puranas_sandhied_nospace_C3_500-500_dicsep2026_n127_ppl_20260816_200522/`.
- `scripts/presentation/validate_nospace_stylo.py` compares (1) stylo's
  top-500 trigram wordlist vs the Python ranking, (2) stylo's delta matrix
  vs the Python Delta matrix, (3) classical MDS of stylo's distances,
  Procrustes-rotated onto the article frame
  (`c3_nospace/coords_nospace_mfw500.tsv`).

## Result

- Feature list: **500/500** identical.
- Per-unit relative frequencies: bit-identical (spot-checked to 6 decimals).
- Delta matrices: **Pearson/Spearman 1.0000** on the upper triangle.
- Map: **ρ_x = ρ_y = 1.0000** against the article frame after Procrustes.

For the methods section: "the no-space C3 feature list, frequency table, and
Delta distance matrix are reproduced exactly by an independent implementation
(stylo 0.7.5 in R) fed the pre-stripped corpus."

## Gotcha recorded

`clusters.R` overwrites `distance_table_<mfw>mfw_0c.txt` once per distance
measure in its loop, so the file that survives a run belongs to the LAST
measure (minmax), not delta. A first comparison against it gave a spurious
0.99-not-1.0; the delta table must be extracted with `stylo::dist.delta`
from `frequencies_analyzed_*.txt` (recipe in the validator's comments —
`distance_table_delta_500mfw.txt` in the results dir). Any future
"stylo disagrees at 0.99" on a clusters.R table: check which measure the
table is before investigating anything else.

## Files

- `scripts/build_nospace_sandhied_corpus.py` (corpus builder)
- `scripts/presentation/validate_nospace_stylo.py` (the comparison; exits
  nonzero below the hero_mds thresholds)
- `corpus/epic_puranas_sandhied_nospace/` (derived, rebuildable)
- results dir as above (wordlist, freq table, delta table)
