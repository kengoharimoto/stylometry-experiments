# MFW robustness of the W1 and C3 delta MDS axes; W1×C3 convergence

2026-08-14. Question: is the C3 companion's horizontal axis (read as linguistic
drift, "earlier → later") an artifact of the 5000-MFW setting — i.e. is theme
leaking in — and where is the sweet spot for both feature systems? Follow-up:
do W1 and C3 converge on the same axis at some MFW?

## Method

`scripts/presentation/hero_mds.py --mfw N` sweeps, Burrows's Delta, MDS,
manifest `dicsep2026_n127_ppl` (127 texts), on the corpora the deck uses:
W1 on `corpus/epic_puranas_unsandhied`, C3 on `corpus/epic_puranas_sandhied`.

- C3 sweep: MFW 250, 500, 1000, 2000, 3000, 5000 (deck default), 8000, 12000.
- W1 sweep: MFW 30, 50, 80 (deck default), 120, 200, 300, 500, 800, 1500,
  3000, 5000.

All C3 layouts are Procrustes-rotated by the script onto the W1 hero reference;
W1 layouts share the fixed sign convention (epics left, Bhāgavata down), so
dim-1 (x) is directly comparable across runs. Every run passed the wordlist
validation against the 2026-08-13 stylo runs (both wordlists hold ~20k
features). Comparisons are Spearman ρ of x across the 127 texts.

Everything (per-MFW figures PNG+PDF, contact sheets, coordinate TSVs, analysis
scripts) is in `materials/presentation_2026/figures/mfw_sweep/`; rerun the
tables with `analyze_c3.py` / `analyze_w1.py` there.

## C3: the horizontal axis is robust; theme is a slow slide upward

| MFW | ρ_x vs 5000 | ρ_x vs W1-80 hero | ρ_y vs 5000 |
|---|---|---|---|
| 250 | 0.95 | **0.85** | 0.40 |
| 500 | 0.98 | **0.86** | 0.50 |
| 1000 | 0.99 | 0.85 | 0.48 |
| 2000 | 0.99 | 0.83 | 0.58 |
| 3000 | 1.00 | 0.83 | 0.88 |
| 5000 | — | 0.82 | — |
| 8000 | 0.98 | 0.77 | 0.95 |
| 12000 | 0.96 | 0.73 | 0.88 |

- x is essentially invariant from 250 to 12000 MFW (all ρ ≥ 0.95, adjacent
  steps ≥ 0.98): the chronological reading does not hinge on 5000.
- Agreement with the content-free W1-80 axis peaks at 250–1000 and declines
  monotonically past 5000 — theme leaks in gradually at high MFW. High MFW
  also compresses genuine spread (śāstra stratum mean x 0.63 @250 → 0.16
  @12000; epics −0.48 → −0.18) and 2-D variance (23.7% → 17.4%).
- The MFW-sensitive dimension is y, not x (ρ_y vs 5000 only 0.40–0.58 below
  3000): dim 2 absorbs the thematic/lexical content.
- Movers with rising MFW: Bhāgavata skandhas drift left toward the epics
  (archaizing lexicon rewarded — skandha 5 rank 73 → 41 from 250 to 5000);
  Gayā-māhātmya and Garuḍa khaṇḍas 2–3 drift right ~30 ranks.

## W1: plateau 80–800, cliff above ~1500

| MFW | ρ_x vs 80 | best ρ_x vs C3 (at C3 MFW) |
|---|---|---|
| 30 | 0.74 | 0.67 (500) |
| 50 | 0.81 | 0.70 (500) |
| 80 | — | 0.86 (500) |
| 120 | 0.99 | 0.87 (500) |
| 200 | 0.99 | 0.87 (500) |
| 300 | 0.96 | 0.88 (500) |
| **500** | 0.94 | **0.89 (500)** |
| 800 | 0.91 | 0.89 (500) |
| 1500 | 0.83 | 0.89 (5000) |
| 3000 | 0.39 | 0.76 (12000) |
| 5000 | 0.04 | 0.50 (12000) |

- Below 80 is too thin and archaism-vulnerable: at MFW 30–50 the Bhāgavata
  strata sit far left among the epics (mean x −0.33 / −0.19 @30) — with only
  the top particles as evidence, an archaic particle repertoire (imitated or
  inherited — open question) is indistinguishable from epic usage —
  and the śāstra/Śivadharma outgroups have not yet separated. Words ranked
  ~50–80 carry real signal (the 50→80 step, ρ 0.81, is the one discontinuity
  in the low range).
- 80–800 is a plateau: adjacent steps ≥ 0.98, everything agrees with the
  MFW-80 hero at ρ ≥ 0.91. The deck's 80 sits just inside its lower edge.
- Above ~1500 the axis collapses outright: ρ vs 80 is 0.39 @3000 and 0.04
  @5000 (the map has no gradient — MBh scattered mid-field). C3 degrades
  gracefully because trigrams keep averaging over morphology; W1 has a cliff
  because past the function-word inventory every added word is a content word.

## Convergence: W1-500 × C3-500, ρ = 0.894

The full 11×8 cross-matrix (see `analyze_w1.py` output) has a ridge along
W1 500–1500 × C3 500–5000 (ρ ≈ 0.87–0.89) peaking at 500×500, falling away in
every direction. The current deck pairing (W1-80 × C3-5000) agrees at 0.816.
Corner check: W1-5000 correlates better with C3-12000 (0.50) than with C3-250
(0.20) — at extreme MFW the two systems re-converge weakly on the shared
*theme* signal; the mid-range ridge is the linguistic one.

## Recommendation

W1 at 200–500 and C3 at 500–1000: inside both stability plateaus, maximal
cross-method agreement (~0.89), furthest from the theme regime at both ends.
Single-number choice: 500 and 500. The deck's current 80/5000 is defensible
(x is stable there), but 500/500 makes the "two independent feature systems,
one chronology" claim measurably stronger.

## Addendum 2026-08-14: name/ritual exclusion test; "function words" framing

Kengo's challenge: the W1-500 list is framed as function words, but what is
actually in it? Inspection: the grammatical layer dominates only ranks ~1–50;
the top 80 already contain śiva (77), bhagavān (78), deva (45), dharma (58),
rājan (74); ranks 481–500 are almost entirely content words (indraḥ, svarga,
bhīṣmaḥ, viprāḥ, jajñe, īśvara, śrāddham...). Consequences: (a) say "most
frequent words (MFW)", not "function words", and describe the function-word
share as falling with rank; (b) the phrase "the content-free W1-80 axis"
above overstates — W1-80 is content-light, not content-free.

Sensitivity test (`figures/mfw_sweep/exclusion_test.py`; baseline reproduces
the saved mfw500 sweep coords at rho 1.0000). Strike from the ranked list and
refill to 500:

- **names/theonyms only** (36 of the top 500): axis-1 Spearman rho vs
  baseline **0.9976**; max mover 8 pts (BhP skandha 2, later).
- **names + ritual/sectarian lexemes** (67 of the top 500, incl. dharma-,
  brahma-forms, yajña, tīrtha, pūjā, vratam, śrāddham, svarga, veda, om,
  demon-class nouns, jajñe): axis-1 rho **0.9898**; max mover 13 pts
  (ViP aṃśa 2, later); Śaiva units drift ~10–12 pts earlier.

The BhP skandha mean moves 50.9 → 52.6 → 54.8 (slightly *later*): its
mid-map position is not manufactured by name/theonym frequencies. For the
article: the W1-500 axis is not carried by proper names or sectarian
vocabulary — strike all of them and the axis reproduces at rho ≈ 0.99.

## Repo change

`scripts/presentation/hero_mds.py:354` hardcoded "80 most frequent words" in
the W1 figure subtitle regardless of `--mfw` (the C3 branch already
interpolated the number). Fixed; the default hero title is unchanged.
