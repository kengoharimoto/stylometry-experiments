# B2 + B2b: the gradient is the signature of autocorrelated change, and losses are the clock

2026-08-16. The axis-anatomy plan's methodological spine (B2) and Kengo's
Dollo-style hypothesis (B2b), run on the colophon-free corpus at article
conventions. Scripts and TSVs in `axis_anatomy/`
(`b2_null_models.py`, `b2b_loss_gain.py`).

## B2 — three synthetic corpora vs the real one

Real unit sizes, real feature inventory, multinomial sampling; 10
replicates per model; seed 20260816.

| model | axis-1 share (W1) | ratio 1/2 | ρ(axis1, latent order) |
|---|---|---|---|
| REAL corpus | 13.4% | 1.68 | — |
| 1 exchangeable (one shared rate vector) | 13.1 ± 0.4% | 2.40 | — |
| 2 heterogeneity (real per-feature variance, NO covariance) | 3.3 ± 0.1% | 1.46 | — |
| 3 drift (Brownian rates along a latent order, variance matched) | 43.4 ± 2.7% | 2.92 | **0.986 ± 0.006** |

C3 mirrors it (real 10.2%; exchangeable 8.4%; heterogeneity 2.3%; drift
44.2% with ρ 0.997).

**Reading — three lessons, one subtle:**

1. **Independent heterogeneity cannot produce the observed axis.** With
   the empirically observed per-feature between-text variance but no
   covariance, axis 1 carries 3.3% (W1) — the real corpus concentrates
   4× more variance in its first axis. A dominant first axis requires
   features to *move together*.
2. **A drift process both produces a dominant axis and makes it the
   order.** Brownian rate evolution along a latent order yields a 43%
   first axis from which MDS recovers the generation order at ρ 0.99.
   The real 13.4% sits between the nulls and the pure-drift corpus, as
   expected: real texts carry drift *plus* register/genre/idiosyncratic
   variance that pure drift lacks.
3. **The exchangeable null's 13.1% is a diagnosed artifact, not
   structure**: its axis 1 correlates with log unit length at ρ 0.91
   (pure sampling noise scales as 1/T — the axis separates small texts
   from large). The real axis 1 correlates with log length at **0.065**.
   So the null calibrates exactly the D1 length caveat, and the real
   axis is demonstrably not that axis. (For the article: report
   axis-1 share *together with* the length-correlation diagnostic;
   share alone can mislead.)

## B2b — the loss/gain decomposition (Kengo's hypothesis)

Split-half, non-circular: original ("epic-typical") and late feature sets
selected on half A only (alternating 16-token blocks; epic = strata 1–2,
late = stratum 5; ratio ≥ 1.5; 81 and 65 features, 1 overlap dropped);
scores computed on half B only. Original sample: mahā iva dṛṣṭvā me idam
śrutvā rājā... Late sample: namaḥ ādi bhavet pāpa syāt muni viṣṇuḥ kuryāt...

| predictor (half B) | ρ vs drift axis |
|---|---|
| **loss alone** (depletion of original-set rate mass) | **0.939** |
| gain alone (late-set rate mass) | 0.720 |
| gain − retention combined | 0.951 |
| within late block only: loss / gain | 0.941 / 0.683 |
| within non-epic units: loss / gain | 0.891 / 0.571 |
| strict presence/absence variant | 0.474 |

**Prediction (i) confirmed**: depletion of the original inventory alone
reproduces the ordering at 0.94 — and keeps ordering *within* the late
block (0.94), where gains stay loose (0.68). **Prediction (ii)
confirmed**: gains add almost nothing to losses (0.951 vs 0.939).
"Losses are the clock; gains are the community structure" stands, with
one sharpening: the clock runs on **frequency retention**, not literal
attestation — the strict Dollo (presence/absence) variant reaches only
0.47 because original features dwindle rather than vanish. The right
citation frame is therefore Swadesh-style retention-rate glottochronology
applied to style-feature *frequencies*, with stochastic-Dollo
(Nicholls & Gray 2008) as the character-loss relative.

## Article mapping

- Q2(a) methods section: the B2 table + the length diagnostic — "a
  dominant, ordering-shaped, length-independent first axis is the
  signature of autocorrelated change; heterogeneity of equal magnitude
  produces no such axis."
- Q2(b) argument section: B2b gives the explanatory mechanism — the axis
  works because it is, in effect, a retention measure; the ordering can
  be recomputed from nothing but the depletion of 81 epic-typical
  features chosen on held-out data.
- Still open in the B-series: B3 convergent orderings (Fiedler/isomap/
  TSP/PCA) — the remaining methods-referee preempt.
