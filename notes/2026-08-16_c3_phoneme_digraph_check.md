# C3 digraph-phoneme check: aspirates as two letters do not move the map

2026-08-16. Kengo's second encoding worry: IAST writes the ten aspirates
(kh gh ch jh ṭh ḍh th dh ph bh) — and the diphthongs ai/au — with two roman
letters, though each is one phoneme. A character 3-gram therefore spans
1.5–3 phonemes depending on content; do the analyses depend on that?

## A-priori difference from the space problem

Word division (the previous check) is *editorial* and varies by edition —
a per-text contaminant. The digraph romanization is *uniform* across the
whole corpus: every text pays the same encoding tax, so it cannot bias one
text against another directly; it can only blur resolution (windows
covering fewer phonemes) or entangle features (a trigram ending in a stop
letter may cut an aspirate in half). Expected effect: small.

## Method

`hero_mds.py --phonemes` (new flag, composed with `--strip-spaces`): map
each digraph to a single SLP1-style symbol (kh→K ... bh→B, ai→E, au→O,
longest-match first) before counting, so a 3-gram spans exactly three
phonemes. MFW 250/500/1000, delta, manifest `dicsep2026_n127_ppl`,
Procrustes onto the W1 reference. Bundle:
`materials/presentation_2026/figures/c3_phoneme/` (coords TSVs,
`analyze_phoneme.py`).

## Result: a measured non-issue

- ρ_x(phoneme, no-space) = **0.988 / 0.993 / 0.998** at MFW 250/500/1000 —
  the maps are near-identical. (For scale: 42 of the no-space top-500
  trigrams contain a full digraph.)
- The phoneme encoding *slightly improves* W1 convergence: ρ vs W1-500
  0.9495 → 0.9604 at the sweet spot; mean |C3−W1| percentile gap 6.9 → 6.4.
  The few movers (≤ 20 ranks) mostly shift toward their W1 positions
  (MBh-14 App. Vaiṣṇavadharma 63→79 [W1 86], VDhP-3 excerpt 57→45 [38],
  Śivadharmottara 87→94 [97]).
- No headline unit moves materially; strata ordering unchanged.

## Decision

Keep the adopted **no-space C3** as the article convention; cite this as a
robustness check ("encoding granularity does not matter: ρ ≥ 0.99, and the
phoneme-exact variant agrees with the word lens marginally better").
Switching conventions again would buy ~0.01 of convergence at the cost of
re-running every instrument and explaining a less familiar encoding; the
check is worth more as a preempted objection than as a new convention.
(If a referee insists on phoneme-exact features, the flag exists and the
result is already known.)
