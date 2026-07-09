# The Nīlamata episode: an orthographic-convention outlier and what it teaches

**Date:** 2026-07-09
**Runs affected:** all epic_puranas runs through 2026-07-08; fixed in
`results_epic_puranas_unsandhied_W1_50-80_20260709_133712/` and
`results_epic_puranas_sandhied_C3_2000-5000_20260709_133938/` (commits
`eebd55b`, `e6dc12a`, and this one).

## Symptom

While selecting MDS candidates for the presentation, `nilamatapurana_au`
appeared as a massive outlier — but **only in the C3 cosine MDS**. No other
metric's plot, and nothing in W1, flagged it.

## Cause

Unlike every other text in `corpus/epic_puranas`, the Nīlamata source came with
sandhi editorially dissolved: `+` at each sandhi junction, `&` at pāda
boundaries, words in pausa form (final `s` for etymological s/visarga, `m` for
would-be anusvāra). The cleaning pipeline stripped `+`/`&` to spaces, leaving
dissolved text in the *sandhied* corpus. Three distinct corruptions followed:

1. **C3**: ~19% of word boundaries carried pausa `-s` (corpus norm ~2.5%),
   radically reallocating the top-frequency space-adjacent trigrams.
2. **W1**: the segmentation model, fed already-dissolved input, passed through
   pausa forms it normally normalizes (`tatas`/`tataḥ` splits in the MFW band).
3. **Both, silently**: pausa spelling strips diacritics (`ṃ`→`m`, `ḥ`→`s`), so
   `is_skip_line()`'s >85%-ASCII English detector dropped **795 of 2241
   genuine lines** — a third of the text — before either pipeline saw them.

## Why only *cosine*, and only in C3 — measured, not guessed

Outlierness of the dissolved Nīlamata by metric (NN distance ÷ corpus median
NN; and distance from centroid in the 2D MDS relative to the 95th percentile):

| metric | NN ratio | MDS outlierness |
|---|---|---|
| cosine (raw freqs) | **12.8×** | **4.5** |
| euclidean (raw) | 3.9× | 1.5 |
| manhattan / canberra / minmax (raw) | 1.6–2.3× | < 0.5 |
| delta / argamon / eder (z-scored) | 1.7–1.9× | < 0.7 |
| wurzburg (cosine on z) | 1.5× | 0.04 |

Trigram frequencies are Zipfian, so raw cosine is governed by the top few
hundred trigrams — exactly the space-adjacent patterns the dissolution
reallocates. Properly sandhied texts share that distributional head almost
exactly, so their mutual cosine distances are tiny; a text with a different
head sticks out at an enormous angle. Z-scoring (the Delta family) subtracts
the shared head and equalizes feature variance, diluting damage concentrated
in a few hundred features across all 5000; Würzburg additionally
length-normalizes the z-vectors, discarding the deviation's magnitude — which
is why Cosine Delta was nearly blind to it (mean-distance ratio 1.01). W1
never showed it because the unsandhied corpus is uniformly dissolved.

## Fix

The `+`-marked source is natively in the `apply_sandhi.py` convention, so
`scripts/sandhi_nilamata.py` runs `apply_sandhi` over it (respecting the
edition's own junction markup, e.g. the kept hiatus in `devī umā`); the
standard builders then regenerated both corpus versions. The sandhied source
also restores the diacritics, so line survival rose 1446 → 2241 and the
unsandhied version grew 8.5k → 14.2k words (re-run on the GPU box).

## Result

Nīlamata rejoins the corpus unremarkably in both branches (NN ratio 1.38× in
each), and W1/C3 now agree on its neighborhood: Matsya-parallel material in
both (adhy. 176 / 1–32), with Kālikā and Bhaviṣya adjacent in C3 and
Skanda-Revākhaṇḍa nearby — a late, Kashmirian, māhātmya-flavored placement
that makes philological sense.

## Lessons (presentation backup slide material)

- **Raw cosine is a preprocessing-inconsistency detector.** It is the one
  metric hypersensitive to top-of-distribution orthographic convention, which
  makes it poor for attribution but excellent as a corpus-hygiene diagnostic —
  the complement of the BhP 10.29–33 commentary case (which W1 caught and C3
  survived).
- **Metric disagreement is diagnostic, not noise** (reinforces §3 of the
  2026-07-08 interpretation notes): when one configuration isolates a text
  that the others place normally, suspect the pipeline before the text.
- **Silent filters bite hardest.** The ASCII-ratio heuristic quietly cost a
  third of a text; convention-dependent preprocessing should be validated
  per-file (the pausa-`s` rate scan now serves as that check).
