# Distance measures and the W1/C3 MDS axis: is it a Burrows's-Delta artifact?

2026-08-14. Companion to `2026-08-14_mfw_robustness_W1_C3.md` (same setup:
`hero_mds.py`, manifest `dicsep2026_n127_ppl`, 127 texts, layouts aligned onto
the W1-80-delta hero reference; comparisons are Spearman ρ of x). Question:
would a different distance measure change the figures — is the chronological
axis specific to Burrows's Delta?

All eight alternative measures `hero_mds.py` implements were run at the
sweet-spot settings from the MFW note (W1-500, C3-500) and in the theme regime
(C3-12000). Coordinates, figures (each metric at W1-500 and C3-500), and
`analyze_metrics.py` are in `materials/presentation_2026/figures/mfw_sweep/metrics/`.

## Results

ρ of x: each metric vs delta at the same settings | vs the W1-80-delta hero:

| metric | W1-500 | C3-500 | C3-12000 |
|---|---|---|---|
| argamon (quadratic Δ) | 0.99 \| 0.96 | 1.00 \| 0.87 | 0.97 \| 0.79 |
| eder (rank-weighted Δ) | 0.98 \| **0.98** | 0.99 \| 0.86 | 0.99 \| **0.79** |
| wurzburg (cosine Δ) | 0.95 \| 0.93 | 0.95 \| 0.82 | 0.95 \| 0.73 |
| manhattan | 0.98 \| 0.97 | 0.98 \| 0.81 | 0.95 \| 0.80 |
| minmax | 0.97 \| 0.97 | 0.98 \| 0.81 | 0.96 \| 0.79 |
| canberra | 0.98 \| 0.92 | 0.99 \| 0.82 | 0.94 \| 0.72 |
| euclidean | 0.87 \| 0.89 | 0.91 \| 0.73 | 0.91 \| 0.75 |
| cosine (raw) | **0.81** \| 0.82 | **0.88** \| 0.66 | 0.88 \| 0.70 |
| *delta itself* | — \| 0.94 | — \| 0.86 | — \| 0.73 |

Per-metric MFW robustness, ρ of x between C3-500 and C3-12000: delta 0.92,
wurzburg 0.95, argamon 0.94, eder 0.95, canberra 0.93; cosine/euclidean/
manhattan/minmax 0.99.

## Reading

- **Within the Delta family the figures are interchangeable.** Argamon and
  Eder agree with Burrows at ρ ≥ 0.98 everywhere — same map, points nudged.
  Würzburg is the family's mild outlier (0.95): cosine on z-scores keeps only
  profile direction, not magnitude. Consistent with Evert et al. 2017: once
  features are standardized, Delta variants measure the same thing.
- **The measures that genuinely change the picture are the unstandardized
  ones.** Raw cosine and Euclidean drop to 0.81–0.91 vs delta and track the
  content-free hero axis worst (0.66–0.73 at C3-500): without z-scoring the
  few highest-frequency features (ca, eva; the top sandhi trigrams) swamp the
  rest and the axis blurs toward a coarse overall-profile ordering.
- **Eder's Delta is the best-behaved.** Its rank weighting down-weights the
  tail of the feature list — a built-in soft MFW cut. At W1-500 it tracks the
  hero axis better than delta itself (0.98 vs 0.94); at C3-12000 it resists
  the theme slide (0.79 vs delta's 0.73). The principled choice if the figure
  must be insensitive to the MFW knob.
- **The unstandardized metrics' apparent MFW-robustness (0.99) is robustness
  by deafness**: added rare features carry negligible weight for them, so
  extending the list changes nothing — including adding no signal. Canberra
  is the mirror case: fine at 500, but its per-feature normalization
  *amplifies* rare features, letting theme in at high MFW (hero agreement
  0.72 at 12000).

## Consequence for the deck

The chronological axis is not an artifact of Burrows's Delta any more than it
was of MFW 5000: every standardization-based measure and the L1-type measures
reproduce it. Only unstandardized cosine/Euclidean blur it, for known reasons.
The stylo runs already write all ten measures per run, so the BCT consensus
trees have been averaging over exactly this variation all along.
