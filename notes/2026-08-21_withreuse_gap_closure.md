# Closing the two with-reuse-only gaps (draft audit 2026-08-21)

Context: after §9 went no-reuse-led, an audit found exactly two draft
claims resting on with-reuse-only measurements with no no-reuse
counterpart: the §3.2 theonym/sectarian strike test and §8(iii)'s
Bhāgavata scale-dependence clause. Both were run today. The first
replicated and now covers both builds; the second **did not survive
instrument hygiene and is retired**.

## 1. Theonym/ritual strike test — all four variants

Instrument: `mfw_sweep/exclusion_test.py`, extended with `--c3`
(trigram analogue: a trigram is struck if it is a substring of any
listed name/ritual lexeme — deliberately over-broad, so a surviving
axis is the conservative statement) and `--noreuse`. ρ of struck axis
vs baseline (names-only / names+ritual; struck counts of 500 in
parentheses):

| variant | names-only | names+ritual |
|---|---|---|
| W1 with-reuse | 0.9976 (38) | 0.9910 (70) |
| C3 with-reuse | 0.9890 (105) | 0.9796 (160) |
| **C3 no-reuse** | **0.9778 (103)** | **0.9678 (157)** |
| W1 no-reuse (ordering-level only, R1 gate) | 0.9984 (39) | 0.9952 (69) |

Max single-text movement 13 pts (W1 with-reuse); largest no-reuse
movers are sub-3k residues (ViP aṃśa 6, +24) plus BhP units moving
*later* (+18…+20 — striking devotional vocabulary pushes the BhP
late-ward, consistent with §9.1-noreuse's sect covariate). Verdict:
the ordering is not a disguised sectarian sorting on either build.

Numbers provenance: the committed script's W1 with-reuse run gives
38/70 struck and 0.9976/0.9910 — this supersedes the draft's earlier
36/67/0.9898 (an earlier exclusion-list version; commit cfed7cf's
0.998/0.990 matches today's run). Draft §3.2 updated to the
reproducible numbers.

## 2. BhP scale-dependence — retired

Instrument: `mfw_sweep/bhp_scale.py` → `bhp_scale_settings.tsv`,
`bhp_scale_ranges.tsv`. Method: at each MFW setting (W1: 30–5000; C3:
250–12,000), both builds, compute the Delta+MDS **top-2 plane**, take
the axis best matching the article reference frame (the C3 eigenpair
is near-degenerate, so the drift axis may surface second), and mark a
setting valid only if ρ_ref ≥ 0.9; ρ(axis, log words) printed beside
every setting.

The 2026-08-14 three-debates measurement (BhP mean W1 pct 19@30 →
52@80 → 50@500 → 26@5000; "genuinely early texts stay early at every
scale") dissolves:

- **The @30 leg reads no instrument at all**: at 30 MFW neither axis
  of the plane reaches ρ_ref 0.75 on any build. There is no drift axis
  to have a position on.
- **The @5000 leg read a length axis**: W1-with @5000 axis 1 has
  ρ_ref 0.14 and ρ_logT +0.91. The drift axis survives as *axis 2*
  there — and puts the BhP at 56, in line with every other valid
  setting (56.0 @80, 53.4 @500, 47.3 @1500, 55.9 @5000-ax2).
- Within valid settings, the BhP's cross-scale percentile range is
  **ordinary**: W1 with-reuse mean 14.9 vs corpus median 16.7 (larger
  than only 43% of other units); W1 no-reuse 51%; C3 no-reuse 46%.
  The big cross-scale movers are the usual small/PPL units.

Consequences applied: the §8(iii) clause "strongly scale-dependent …
in a way no other text shows" is **deleted from the draft** (the
isolation claim stands, now verified on both builds: every BhP unit's
nearest neighbour is internal on the no-reuse maps too); claims map
§6.6 row struck with a do-not-cite; the three-debates note carries an
addendum. The 2026-08-14 note's own annotation (Kengo) had already
gated the "artifact" inference; today's result removes the measurement
under it.

**One open anomaly, flagged not concluded:** on with-reuse C3 the
BhP's valid-settings range (mean 27.0 vs median 11.1) is larger than
94% of units — possibly a real register-by-feature-stratum
interaction, but it rides on the rotated C3 reference frame (the
article's C3 coords are hero-oriented, |ρ| vs raw axis 1 = 0.86) and
disappears on the no-reuse build. Not draft material; revisit only if
the BhP question gets its own study.

## Standing consequence for practice

The scale-check's method note generalizes: **any per-text claim read
off a sweep must verify per setting that the axis is still the drift
axis** (ρ_ref beside every setting, top-2 plane not raw axis 1, length
diagnostic beside both). §3.1's cliff and §4's degenerate-eigenvalue
observation predicted exactly the two failure modes found here.
