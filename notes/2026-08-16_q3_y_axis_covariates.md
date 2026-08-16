# Q3: the y-axis has a name — enumerative catalogue vs devotional address

2026-08-16. The axis-anatomy plan's C-series covariate step, on the
colophon-free corpus. Prerequisites already in hand: no arch (B5, R² ≤
0.02), cross-lens y agreement 0.82 raw / 0.79 detrended, and B3's
independent confirmation that y is a real organized dimension (TSP
snake-fold; C3 methods ranking it first). Script
`axis_anatomy/q3_y_covariates.py`; tables `q3_y_covariates.tsv`
(covariate × lens ρ), `q3_unit_covariates.tsv` (per-unit values).

## What y correlates with (Spearman; y oriented BhP-low)

| covariate | W1 y (det) | C3 y (det) | vs x, for contrast |
|---|---|---|---|
| sectarian+ritual vocab density | −0.44 (−0.43) | **−0.60 (−0.60)** | +0.44 / +0.37 |
| optative share | −0.36 (−0.33) | −0.54 (−0.52) | +0.63 / +0.56 |
| vaiṣṇava lexicon | −0.34 (−0.36) | −0.34 (−0.35) | +0.11 / 0.00 |
| speech-frame density | −0.36 (−0.42) | −0.13 | −0.46 / −0.51 |
| śaiva lexicon | −0.18 | −0.44 | +0.62 / +0.64 |
| goddess lexicon | −0.17 | −0.29 | +0.31 / +0.33 |
| śaiva-vs-vaiṣṇava polarity | +0.04 | −0.17 | +0.39 / +0.48 |
| log length | −0.24 | −0.18 | −0.07 |
| quotative iti | +0.05 | +0.05 | +0.11 / +0.20 |

Combined (rank-OLS on sect_total + optative + speech + vaiṣṇava +
log_len): R² = 0.45 (W1), 0.55 (C3).

## Reading

**The low-y (Bhāgavata-ward) pole is the devotional-address register.**
Its strongest correlate is sectarian-devotional vocabulary *density* —
not which sect (the śaiva-vs-vaiṣṇava polarity is ~0 against y; both
sects' theonym rates load on x, the drift axis, more than on y). The
feature loadings say it directly: the most BhP-ward W1 features are
bhaktyā, hareḥ, śrī, para-, and the 1st/2nd-person machinery (aham, tvad,
kim, sva-) — prayer and address. On C3, low-y is anusvāra-junction
morphology (aṃs, yaṃ, ṃvi, naṃ — accusative/1-2p verbal strings).

**The high-y pole is the enumerative catalogue register.** Top features:
ca (+0.72), eva, tu, vai, teṣām, ete, sahasrāṇi, trayaḥ, sarvaśas —
coordination, deixis, and number words; on C3, visarga-sandhi junctions
(śca, āḥp, ḥsa, aśc — nominative chains under ca-coordination). This is
the vaṃśa/cosmology list style.

**So axis 2 ≈ third-person enumerative cataloguing ↔ second-person
devotional address**, with the two lenses agreeing morphosyntactically
(nominative-chain junctions vs accusative/address junctions) — a genuine
register dimension, orthogonal to drift by construction and now
orthogonal to it in *content* (its strongest covariates are the ones
whose x-correlations run the other way or vanish).

**Bounds (C5's write-up rule applied):** the covariates explain about
half the rank variance (R² 0.45–0.55); the rest is register texture our
simple codes don't capture. Name y as "the catalogue↔devotion register
axis (to the extent the lenses agree, ρ ≈ 0.8)"; never as a second
chronology — y-nearness without x-nearness is register kinship, not
date. Length is a minor y covariate (−0.2) and worth one caveat line.

**C4 (within families, x roughly held):** the corpus-wide pattern
recurs: within the ŚiP saṃhitās y tracks sectarian-vocab density
(ρ −0.62); within MBh parvans and Rām kāṇḍas the optative share is the
top within-family y correlate (−0.67, −0.82). BhP skandhas: small-n,
mixed. The register reading survives at fine grain.

**BhP corollary (neutral wording):** the Bhāgavata anchors the
devotional pole because its register is saturated bhakti-address — a
*register* fact, stated without any date directional.

## Remaining Q3/plan items

- A5 per-text anatomies (worked examples for the article's extremes).
- A4 Kengo-led external-diachrony reading against Oberlies/Meenakshi.
- Optional: edition-family coding as a y covariate (deferred — needs
  per-text provenance hand-coding).
