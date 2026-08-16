# Axis anatomy, session 1: A1 loadings, B1 variance, B5 arch check

2026-08-16. First bundle of the axis-anatomy plan
(`2026-08-14_axis_anatomy_plan.md`): the cheap, no-new-corpora items.
Everything at the article conventions — W1-500 (unsandhied) and no-space
C3-500 (scriptio continua), Burrows's Delta, manifest `dicsep2026_n127_ppl`,
axis positions from the saved sweet-spot coordinate frames. Bundle:
`materials/presentation_2026/figures/axis_anatomy/` (three scripts, loading
TSVs, jackknife TSVs, arch residuals).

## A1 — What loads on the drift axis

Full ranked tables: `loadings_{W1,C3}_500.tsv` (feature, ρ_x, ρ_y, mean
rate, early-quartile and late-quartile per-mille rates).

**The axis is distributed, not a few-feature artifact**: |ρ_x| ≥ 0.7 for
only 4 (W1) / 8 (C3) of 500 features; ≥ 0.5 for 99 / 58; median |ρ_x|
0.28 / 0.23. No feature class can be struck to kill it (consistent with
the name/ritual exclusion test's ρ 0.998).

**W1 top loadings read as a two-register contrast.** Early pole (rate
falls with x): the epic narrative-dialogic machinery — anaphoric pronouns
(tam −0.78, sa −0.70, enam, tān, tvām), speech-frame verbs (abravīt −0.67,
uktvā, vacaḥ, āsīt, jagāma), narrative converbs (dṛṣṭvā, śrutvā), iva
(−0.64), vocative rājan, and epic content vocabulary (vīra, raṇe, rāja-,
mahā-, putram, balam). Late pole (rate rises with x): the śāstric-
doxographic apparatus — ādi "-etc." (+0.81, the strongest single loading),
jñāna/jñānam, brahma, list numerals (tri, aṣṭa, ṣaṣ, eka, dvi via C3),
prescriptive optatives (bhavet, kuryāt, pūjayet, jāyate), citation
participles (smṛtam, proktam), kramāt, and theonyms (śiva, viṣṇu, rudra —
already shown non-load-bearing by the exclusion test).

**C3 says the same thing morphologically**: early = narrative inflection
and vocabulary fragments (rāj/āja −0.81/−0.80, tāṃ, hat(a)-, -vān, bal-);
late = *derivational and prescriptive morphology* — -ika/-ikā suffixes
(+0.78), optative endings -yet/-yāt (+0.70/+0.64), abstract/technical
clusters (dhy, khy, sth), numeral morphology (ñca = pañca, dvi), ādi,
smṛ-. The two lenses independently converge on: **the drift axis is a
narrative-dialogic → prescriptive-doxographic register gradient in the
unconscious feature band**. Whether that gradient is *temporal* is Q2's
question (B4's assembled stack + A4's external diachrony check); A1's
contribution is that the feature anatomy is linguistically coherent and
classifiable — ready for A2's class decomposition.

## B1 — Variance anatomy: the axis is nobody's artifact

Eigenvalue spectrum (positive part):

| | axis 1 | axis 2 | ratio | axes 3–5 |
|---|---|---|---|---|
| W1-500 | 13.5% | 8.0% | 1.69 | 7.2 / 5.7 / 4.3% |
| C3-500 | 10.6% | 9.4% | 1.13 | 6.6 / 5.2 / 4.7% |

Jackknife (drop one unit, refill features, recompute, align):
axis-1 ρ ≥ **0.997** (W1) / ≥ **0.983** (C3) across all 127 deletions,
median 0.9996 / 0.9991; axis-1 variance share moves only within
13.2–13.7% / 10.3–10.8%. The least stable single drops are tiny or
peripheral units (MBh 17; ŚiP Vidyeśvara on C3). Grouped deletions of the
leverage suspects — the śāstra outgroup, the Śivadharma pair, both — leave
the axis at ρ ≥ 0.988 on both lenses. **No unit or suspect group carries
the axis.**

Reading the shares: 13.5% (W1) of squared-distance variance in one axis of
a 127-text corpus spanning ~1500 years is a dominant gradient (the next
axis drops to 8.0%), but the spectrum is fat-tailed — most Delta variance
is idiosyncratic text-pair structure, which is why the *map* needs the
convergence argument and not just the picture. C3's near-parity ratio
(1.13) says its second dimension is almost as organized as its first —
consistent with B5's finding that y is real, and with the deck's old
observation that C3-y absorbs theme.

## B5 — There is no arch; y is real and shared

Quadratic fit y ~ x²: **R² = 0.018 (W1), 0.007 (C3)** — the Guttman/
horseshoe fold is absent; the y-axis is not the x-axis bent over. (Linear
R² ~ 0.000 both — x and y are uncorrelated, as MDS guarantees.) With the
gradient carrying only ~11–14% of variance, there is simply not enough
one-dimensional dominance to fold.

Cross-lens y agreement (the plan's C2 decisive filter, answered early):
**ρ(y_W1, y_C3) = 0.844 raw, 0.824 after arch-detrending.** This is the
"agree strongly" regime: axis 2 is a real, shared property of the texts —
not lens noise, not arch — and deserves a name. Caveat to carry: both
coordinate frames were Procrustes-rotated onto the same hero reference
(rotation/reflection only), which is what makes their axes comparable;
the agreement is a property of the aligned configurations.
`b5_arch_residuals.tsv` holds detrended y for the C3-covariate step.

## Consequences for the plan

- **Q3 is unlocked and promoted**: with no arch and ρ_y 0.84, the C3 step
  (covariates: sectarian register, discourse form, meter mix, direct-speech
  density) is now the highest-value next item — y will support a real
  finding, not a bounding exercise. Run on raw y (arch negligible), report
  detrended alongside.
- **A2 next for Q1**: the class decomposition needs Kengo's review of the
  hand-classification of the W1-500 list before anything is computed
  (per the plan). A1's table is the input; the classes suggested by the
  loadings are (i) pronouns/pro-forms, (ii) speech-frame verbs and
  narrative converbs, (iii) particles, (iv) optatives/prescriptives,
  (v) numerals and ādi-type list machinery, (vi) content lexemes.
- **B4 gains a sentence**: the axis survives deletion of any unit and of
  the outgroup blocks; robustness now includes leverage.
