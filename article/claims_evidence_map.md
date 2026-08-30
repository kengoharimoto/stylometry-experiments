# Claims-and-evidence map (venue-neutral)

**Date:** 2026-08-30 (major revision for the cleaned-corpus restructure;
previous state 2026-08-17)
**Purpose:** the single source of truth for drafting. Every article variant
(see `outline_*.md`) draws its claims, numbers, and figures from here, so
the variants cannot drift apart factually.

**Citation rule:** numbers in this map are for architecture and orientation,
transcribed from the notes. Before any number goes into printable prose,
verify it against the source note and, where applicable, the TSV it cites.
Canonical values are **cleaned-build** (reuse-stripped, colophon-free,
no-space C3, manifest `noreuse2026_n126`) — with-reuse values appear
only in the §7-diagnostic role and must be labeled as such; the
provenance gates in §0 list the traps.

---

## 0. Conventions and provenance gates

- **Corpus (the corpus of the article): the cleaned build** — reuse
  stripped (RATIO-70 shingle strip, kirfel one-directional),
  colophon-free, 126 units, manifest `noreuse2026_n126`, 3,556,172
  de-sandhied words, residues 648–344,712 (median 15.1k), 18 units
  below the 3k floor. 126 = the transmitted inventory's 127 minus
  `vayu_ba` (the Vāyu–Brahmāṇḍa common text — shared text by
  construction, zero residue). The transmitted inventory (127 units,
  `dicsep2026_n127_ppl`, colophon-free since 2026-08-16) survives for
  exactly one purpose: the §7 diagnostic comparison.
- Lenses: **W1-500** (unsandhied words, ByT5 int8 pipeline) and **C3-500
  no-space** (char trigrams over the whitespace-stripped sandhied stream,
  `hero_mds.py --strip-spaces`). Burrows's Delta, classical MDS,
  Procrustes-aligned to the hero reference.
- Layer/subset instrument: fixed-map Gower supplementary projection +
  line-bootstrap CIs (B=500, seed 20260814). Never recompute the map on
  gutted corpora for layer questions.
- **RESTRUCTURE 2026-08-30 (Kengo; supersedes the 2026-08-19
  "precedence" framing).** The cleaned build is not the privileged
  member of a pair — it is **the corpus, full stop**. Uncleaned
  variants (with reuse, with colophons, spaced trigrams) are
  mismeasurements, not baselines; comparisons against them are
  **diagnoses of what the contamination was doing, never robustness
  tests**. The with-reuse build appears in the draft exactly once
  (§7, "what the absorbed text was doing"), where the difference
  between the builds is the finding (drag = with-reuse minus cleaned
  position; positive = absorbed material had dragged the text
  lateward). "Precedence" language is gone — there is no competition
  to adjudicate. Draft restructured accordingly (commits 476ec34 →
  1e8a187); stage-2/3 recomputes put cleaned-build values behind
  every representative number.
  **Terminology — RULED 2026-08-30 (Kengo): reverted to plain
  "with-reuse / no-reuse", reaffirming the 2026-08-21 rule** (both
  corpora are transmitted; "composed" overclaims; "transmitted"
  collides with text-critical transmission). The restructured draft's
  interim "cleaned / as transmitted / composition" build-labels were
  removed (commit e4b5d4c): the corpus of the paper is "the no-reuse
  corpus", §7 is "the with-reuse map as diagnostic", Table 1 columns
  are no-reuse | with-reuse | drag. Ordinary text-critical uses of
  transmitted/transmission remain legitimate ("a purāṇa as
  transmitted is a mixture"; "even a residue is transmitted"). This
  map's own entries above use "cleaned build" descriptively in dated
  records — do not import that word into draft prose.
  Notes written before 2026-08-21 keep the old wording as dated
  records. Evidence, movers tables, caveats, and the work queue
  are in `2026-08-19_noreuse_precedence_reframe.md`. **Gates (R1/R2 ran
  2026-08-19, same note):** (a) the cleaned chronology is **C3-led** —
  the no-reuse W1 axis is partly a length artifact (exchangeable null:
  18.5% share, ρ 0.96 vs logT; real ρ 0.44), so W1-noreuse per-unit
  percentiles/shift magnitudes are NOT citable — W1 confirms signs and
  the ordering (ρ 0.93 cross-lens) only; (b) citable cleaned-build
  numbers come from `figures/noreuse_reframe/unit_ci_*` +
  `movers_C3.tsv` (fixed-map Gower + line-bootstrap, B=500),
  `axis_anatomy/b2_models_*_noreuse_500.tsv`, and the **2026-08-30
  stage-3 TSVs**: `c3_nospace_noreuse/` (no-space C3 sweep coords +
  `fig2_grid_noreuse.tsv` + `metrics/`),
  `axis_anatomy/a2_decomposition_noreuse.tsv`,
  `b1_jackknife_C3_noreuse_500.tsv`, `b3_orderings_C3_noreuse_500.tsv`,
  `loadings_C3_noreuse_500.tsv`,
  `loadings_W1rates_vs_C3axis_noreuse_500.tsv` (W1 rates correlated
  against the C3 axis — the R1-safe word-level loading table) — not
  from the earlier exploratory tables in the note; (c) sub-3k residues
  (most Vāyu sections, Viṣṇu aṃśas 1/2/5/6, MBh 17–18; 18 units in
  all) are uncertainty regions in every cleaned-build exhibit, faded
  in Fig 1.
- **Label glossary** (the letter codes come from four dated queues):
  **Q1/Q2/Q3** = the three research questions of
  `2026-08-14_axis_anatomy_plan.md` (what moves a text / why drift shows
  in MDS / what is y). **A1–A5** = Q1 experiments there (A1 loadings, A2
  class decomposition, A3 minimal set [open], A4 documented-diachrony
  link [DROPPED 2026-08-17], A5 per-text anatomy [open]); **A6** is a
  2026-08-19 addition outside Q1: axis-3/BhP statistics (done).
  **B1–B5, B2b** = Q2 experiments there (B1 variance anatomy, B2 null
  models, B2b loss/gain retention clock, B3 convergent orderings, B4
  time-likeness assembly, B5 arch check); **C1** = Q3 arch removal.
  **D1–D6 / E1–E2** = the July closing-parvans length brief
  (`CLOSING_PARVANS_length_artifact_brief.md`); D1/D4 are the length
  diagnostics, and E1 grew into the CE-apparatus validation
  (`2026-08-14_e1_apparatus_experiment.md`). **R1–R4** = the 2026-08-19
  no-reuse reframe queue (all closed; see §0 reframe entry and §8).
- **Traps when quoting notes:**
  - Never quote pre-clean numbers (git ≤ d9532dd; the pre-clean unsandhied
    corpus survives only in commit 0b666a9's safety copy).
  - C3 percentiles in the 2026-08-14 notes are **standard-C3**; the
    conversion table is `2026-08-16_nospace_c3_adoption_rerun.md` — but
    that note's tables are themselves **pre-clean**; final C3 numbers come
    from `2026-08-16_colophon_corpus_cleanup.md` and the post-clean TSVs.
  - B1 jackknife numbers in `2026-08-16_axis_anatomy_a1_b1_b5.md` are
    pre-clean (conclusions insensitive; re-run if a referee needs it).
  - **`mfw_sweep_noreuse/coords_mfw*.tsv` are SPACED C3** (discovered
    2026-08-30: 0.888 vs the no-space article frame) — never audit a
    no-space cleaned-build claim against them; the no-space no-reuse
    sweep is `c3_nospace_noreuse/coords_c3ns_mfw*.tsv`. (The W1 sweep
    coords in `mfw_sweep_noreuse/` are fine, 0.999 vs frame.)
  - `b2b_loss_gain_C3{,_noreuse}_500.tsv` are at THRESH **1.3**
    (loss 0.864 / gain 0.62 on noreuse); re-running the script at
    another threshold silently overwrites them — restore from git if
    that happens, and always cite the threshold sweep (1.1–1.3), not
    one setting.
  - No pre-2026-07-10 R-pipeline number is citable (stylo tokenization bug).
  - July BhP fuzzy-sweep numbers only with the `--normalise-cand-length`
    caveat; the normcut run's original delta numbers (105,795 rows /
    27,433 units / 152 works) are exclusion-bug pool artifacts — use only
    the ADDENDUM values in `2026-08-17_bhp_fuzzy_sweep_normcut.md`
    (7,500 → 7,970 units, 138 new works; BhP 9 × PPL stats unaffected).

---

## 1. The instrument and its validation

**1.1 Two-lens convergence (the design's spine).** Two near-orthogonal
feature systems — whole-word habits on editorially undone sandhi vs
sub-lexical trigrams on the continuous sandhied stream — recover the same
ordering on the cleaned build: **ρ_x = 0.93** (0.9267 all 126 units,
0.9284 above the floor, article-frame `unit_ci_*` positions; the
aligned sweep grid's 500×500 cell reads 0.930). **Trigram-led**: C3
carries per-unit values, W1 corroborates the ordering (R1 gate). The
old 0.953 is the with-reuse value — diagnostic context only, no
longer the headline anywhere. The A2 bridge shows the lenses draw on
largely disjoint material (closed classes = 38% of W1's signal but
12% of C3's; C3 is 61% word-interior morphology) — **shares still
pre-strip; open item §8**.
→ `2026-07-08_W1-unsandhied_vs_C3-sandhied_interpretation.md`,
`2026-08-16_a2_bridge_word_classes_in_c3.md`. Fig: Figure 1 (rebuilt
cleaned 2026-08-30) + Figure 2.

**1.2 MFW robustness — re-derived on the CLEANED build 2026-08-30
(supersedes the 2026-08-21 with-reuse grid; those values survive only
as §7-diagnostic context).** Broad plateau 0.93–0.94 (W1 500–1500 ×
C3 1000–5000); adopted 500×500 = **0.930**; grid max 0.936 at
W1-800×C3-3000 — the adopted cell sits on the plateau within 0.006
of the max, "peak" wording is retired, "plateau" is the claim.
C3-nospace invariant 250–5000 (ρ ≥ 0.93 vs adopted 500; pairwise min
over 250–8000 = 0.879 at 500↔8000), easing 0.88 @8000 / 0.79 @12000.
W1 stabilizes from ~200 MFW (0.98 vs adopted) and — the headline
change — **has NO high-MFW cliff on the cleaned build** (0.92 @5000
vs adopted): the with-reuse cliff (0.51 @3000 / 0.14 @5000) was the
lens measuring the shared material (cross-build anti-correlation
−0.86 @5000), i.e. a reuse phenomenon, now told as diagnosis in
draft §3.1/§7.1. All grid cells Procrustes-aligned to the article
frame before comparison (load-bearing on residues — register nearly
as strong as drift). Sources:
`c3_nospace_noreuse/fig2_grid_noreuse.tsv` + regenerated
`fig2_convergence/` TSVs. **Never audit no-space cleaned claims
against `mfw_sweep/coords_mfw*.tsv` or
`mfw_sweep_noreuse/coords_mfw*.tsv` — both SPACED C3.** Terminology
guardrail: say "most frequent words", not "function words" (top-80
already contains deva, dharma, śiva).
Fig: **Figure 2 REBUILT cleaned 2026-08-30** (`fig2_convergence/`).

**1.3 Metric robustness — re-run on the CLEANED build 2026-08-30.**
Standardized family + L1 measures reproduce the axis at 0.98–1.00
(argamon 0.984, canberra 0.985, eder 0.990, manhattan 0.988, minmax
0.982; Würzburg cosine 0.897 — quote "0.98–1.00, Würzburg 0.90").
Unstandardized cosine/Euclidean **collapse** (0.26 / 0.63), harder
than the with-reuse "blur" (0.81–0.91): on residues of very unequal
size the Zipfian-head domination is total. The old "robustness by
deafness" caution (unstandardized stable at 0.99 across feature
counts) was a with-reuse phenomenon — on residues cosine is not even
self-stable (≈ 0.5 across settings); draft §3.2 states both halves.
Delta-family interchange expected (Evert et al. 2017) — consistency
check, not independent confirmation.
→ `c3_nospace_noreuse/metrics/coords_*.tsv`;
`2026-08-14_distance_metrics_W1_C3.md` (with-reuse history). Fig: 9-row table.

**1.4 The with-reuse comparison — REFRAMED 2026-08-30: diagnostic,
NOT robustness.** "The ordering survives reuse removal" is no longer
a claim the article makes in §3 — reuse removal is corpus
construction (§2.2). The cross-build facts move to draft §7 as
diagnosis: global agreement ρ 0.982 C3 / 0.908 W1 (why the
contaminated discovery pointed true — drags largely cancel at global
scale); high-MFW anti-correlation −0.86 (what the with-reuse cliff
was measuring); 16 CI-separated movers = the drag table.
→ `2026-08-14_mfw_robustness_noreuse.md` (dated record),
`noreuse_reframe/movers_C3.tsv`. Fig: Table 1 (drag table).

**1.5 Names/sectarian vocabulary struck.** Cleaned-build values are
the citable ones (draft §3.2): C3 trigram analogue (strike any
trigram occurring inside a listed lexeme; over-broad by design,
105–160 of 500 struck) **0.9836/0.9798**; W1 0.9984/0.9952 —
ordering-level only (R1 gate). C3 baselines Procrustes-rotated into
the article frame per the 2026-08-21 frame fix (raw C3 axis 1 sits
22–28° off the published drift axis). With-reuse variants (W1
0.9976/0.9910, C3 0.9892/0.9853) are history, not draft material.
BhP moves slightly *later* under the strike on every variant.
→ `mfw_sweep/exclusion_test.py` (`--c3`, `--noreuse`),
`mfw_sweep/exclusion_results_*_noreuse.tsv`;
`2026-08-21_withreuse_gap_closure.md`.

**1.6 Encoding corrections (C3) — framing per the 2026-08-30
restructure: corrections that define the corpus, not survived
perturbations.** Word division is editorial → no-space C3 is the
corpus convention (spaced C3 was mismeasuring: 33% of top-500
features carried a space; movers moved toward their W1 positions
when it was fixed). Digraph romanization measured non-issue
(ρ ≥ 0.99, cite as preempted objection). Colophons were real
directional paratext bias (ρ −0.58 with shift, single units up to 15
pts) → removal is definitional; the only "after" number quoted is
that the lenses agreed better (correction behaving as a correction),
never "no headline moved".
→ `2026-08-16_c3_nospace_scriptio_continua.md`, `_c3_phoneme_digraph_check.md`,
`_c3_colophon_stripped_check.md`, `_colophon_corpus_cleanup.md`.

**1.7 Independent implementation — RE-RUN ON THE CLEANED BUILD
2026-08-30.** No-space C3-500 reproduced exactly by R stylo 0.7.5 on
the whitespace-pre-stripped cleaned corpus
(`corpus/epic_puranas_sandhied_noreuse_nospace`, results dir
20260830_161355; `validate_nospace_stylo.py --noreuse`): features
500/500, Delta matrices ρ 1.0000, map ρ 1.0000 vs the article frame.
The 2026-08-16 with-reuse cross-validation stands as history.
→ `2026-08-16_stylo_nospace_crossvalidation.md` (methods sentence —
update its build description before quoting).

**1.8 Length limits (the honest boundary).** Sub-3k-word units are
uncertainty regions (D1); length is the failure mode both lenses *share*,
so convergence does not defend against it — must be said out loud.
→ `2026-07-15_closing_parvans_length_diagnostics.md`,
`CLOSING_PARVANS_length_artifact_brief.md`. Fig: axis-1 vs sample-size panel.

**1.9 Hygiene worked examples (optional methods color).** Nīlamata sandhi
episode: raw cosine as a preprocessing-inconsistency detector (12.8× NN
outlierness vs 1.5× for wurzburg). Stylo U+1E00 tokenization bug: non-ASCII
splitting silently mutilated IAST; survived-anyway robustness anecdote.
→ `2026-07-09_nilamata_sandhi_episode.md`, `2026-07-10_stylo_tokenization_bug.md`.

---

## 2. Q2(a): why a drift axis emerges (mechanics)

**2.1 B1 variance anatomy — CLEANED values 2026-08-30.** C3 spectrum
8.7 / 7.2 / 5.7 / 4.9% (axes 1–4), ratio12 **1.21** (W1: 12.8%,
ratio12 1.31); jackknife over all 126 deletions ρ ≥ **0.991**
(median 0.999, axis-1 share stable 8.4–8.9%); leverage suspects
(śāstra outgroup, Śivadharma pair) cleared at ≥ 0.993 singly or
together. Sources: `axis_anatomy/b1_jackknife_C3_noreuse_500.tsv`,
`b2_models_C3_noreuse_500.tsv`. The with-reuse spectrum (13.4%/1.68
W1, 10.2%/1.07 C3, `b2_models_{W1,C3}_500.tsv`) is diagnostic
context only. Note the near-degeneracy story SOFTENS on the cleaned
build (1.21 vs 1.07) — see 2.3 for what that does to the
multi-method reading.
→ `2026-08-16_axis_anatomy_a1_b1_b5.md` (pre-clean history).

**2.2 B2 null models (the methodological centerpiece) — CLEANED
values (run 2026-08-19, promoted to headline 2026-08-30).** C3: real
axis-1 share **8.7%**, length-clean (ρ 0.064 vs logT); exchangeable
null 6.9 ± 0.2% — close to real, and the length diagnostic is what
exposes it (the null's axis is sampling-noise geometry);
heterogeneity without covariance 2.5 ± 0.1%; Brownian drift 40.9 ±
1.5%, recovering the latent order at ρ 0.996 ± 0.002 (W1 0.974),
length-clean. W1 residues: exchangeable null 18.5% at ρ 0.96 vs logT
BEATS the real W1 axis (12.8% at 0.44) — the R1 catch, told in draft
§3.4 as the diagnostic catching our own lens. Share alone can
mislead; always report the length diagnostic beside it.
→ `axis_anatomy/b2_models_{W1,C3}_noreuse_500.tsv`;
`2026-08-16_b2_models_loss_gain.md` (with-reuse history: 13.1%
null / 13.4% real / 3.3% / 43.4%, ρ 0.986). Fig: null-model table
with length-diagnostic column.

**2.3 B3 convergent orderings — RE-RUN CLEANED 2026-08-30; the
reading CHANGES.** On the carrying lens: PCA recovers the gradient
in its aligned top-2 plane at **0.984** (raw pca1 0.834); isomap
0.77; **Fiedler FAILS (0.12 aligned / 0.21 raw) — it did not fail
with-reuse (0.82)** — and TSP fails as before (0.21). New wording
(draft §4): methods that retain a plane recover the gradient;
methods that force one dimension (path or single spectral
coordinate) cannot choose between two near-equal directions and
fold — their failure is evidence FOR the second dimension, not
against the first. Do not quote the with-reuse
"PCA/isomap/Fiedler all find it" sentence. t-SNE/UMAP exclusion
unchanged.
→ `axis_anatomy/b3_orderings_C3_noreuse_500.tsv`;
`2026-08-16_b3_convergent_orderings.md` (with-reuse history).

---

## 3. Q1: what the axis counts

**3.1 A1 loadings — CLEANED tables 2026-08-30.** Distributed: 5/500
C3 features at |ρ| ≥ 0.7 (41 at ≥ 0.5), median |ρ| 0.205; W1-rates
table 3/500 at ≥ 0.7, median 0.249. Word-level poles (W1 rates vs
the **C3** axis — the R1-safe construction; never correlate W1 rates
against the W1-noreuse axis): early = adya −0.75, rāja/rājan
−0.74/−0.70, tvām −0.70, vīra −0.70, tam −0.67, iva −0.66, raṇe
−0.65, tava −0.64, ratha(m) −0.62, dhanuḥ −0.60; late = ādi +0.64,
brahma +0.63, jñāna(m) +0.54/+0.49, kramāt +0.53, namaḥ +0.53,
**smṛtam +0.53 / ucyate +0.50 / proktam +0.47 (citation formulas —
new, the transmitted corpus had blurred them)**, bhavet +0.48, eka
+0.48. C3 poles: rāj/āja −0.81/−0.75, hat/han −0.70/−0.51, -āmi
−0.62 early; mṛt +0.71, -ikā +0.70, ahm (brahm) +0.68, ādi +0.62
late — **glosses pending Kengo's vetting (mṛt = amṛta vs mṛtyu; aye;
ātr)**. Whether the register gradient is temporal is Q2's question,
not A1's claim.
→ `axis_anatomy/loadings_C3_noreuse_500.tsv`,
`loadings_W1rates_vs_C3axis_noreuse_500.tsv`;
`2026-08-16_axis_anatomy_a1_b1_b5.md` (with-reuse history: tam −0.78
etc. — do not quote against the draft). Fig: two-pole loading table.

**3.2 A2 class decomposition (Q1's answer) — CLEANED (C3-only, R1)
2026-08-30.** No class necessary, broad classes sufficient:
word-interior trigrams alone **0.961**, content-source trigrams
alone 0.909, word-initial alone 0.858; every single-class removal
≥ 0.840 (most ≥ 0.89). The one real exception: junction/word-final
trigrams alone fail (**0.089 / 0.029**) — boundary phonology, the
edition-sensitive stratum, is where the ordering is not. The W1
class rows (particles alone 0.889, content 0.941, etc.) are
with-reuse-only — R1 bars a W1-noreuse decomposition; the draft's
§3.3 is C3-phrased. Perturbation check (max Δρ 0.031) is the
with-reuse W1 run; draft cites it as classifier-robustness at one
remove. → `axis_anatomy/a2_decomposition_noreuse.tsv`;
`2026-08-16_a2_class_decomposition.md`,
`_a2_bridge_word_classes_in_c3.md` (with-reuse). Fig: decomposition
table (Q1 centerpiece).

**3.3 A3 minimal sufficient set — RUN 2026-08-29 (for the Indological
companion; the DH draft does not cite it).** Verdict: **the axis
resists compression** — greedy selection (half-split guarded) never
reaches holdout ρ 0.95 on W1; holdout peaks at k = 7 (0.9165 held-out,
0.9513 full-corpus: ādi, adya, rājānam, sma, jñānam, mama, dattvā) and
overfits beyond. Corroborates A1/A2 redundancy from a third direction.
C3 compresses to 3 trigrams (rāj, tāṃ, ātr; holdout 0.9585) — but a
trigram is a feature *family*, quote only with that caveat.
→ `axis_anatomy/a3_minimal_set.py`, `a3_minimal_set_{W1,C3}.tsv`,
`2026-08-29_a3_a5_minimal_set_text_anatomy.md`.

**3.4 A5 per-text anatomy — RUN 2026-08-29 (for the Indological
companion; the DH draft does not cite it).** contribution = z × loading
per feature per featured text (PPL I/ungrouped, old SP, ŚDh, ŚDhU,
merged MBh 15–18, merged BhP-12); the weighted z-sum proxies the axis
at ρ 0.9953 (W1) / 0.9956 (C3). Headlines: old SP early = narrative
anaphora/simile machinery; closing block = court + frame-dialogue
vocabulary; ŚDh late = sectarian-ritual stratum (but survives the 1.5
strike — names what carries, not what it reduces to); BhP early-ward
pull is part presence of dialogue vocabulary, part *absence* of late
prescriptive machinery (symmetric wording gate applies).
→ `axis_anatomy/a5_text_anatomy.py`, `a5_text_anatomy_{W1,C3}.tsv`,
same note.

---

## 4. Q2(b): why the axis is time-like

**4.1 B2b retention clock (Kengo's hypothesis, confirmed in frequency
form) — CLEANED headline 2026-08-30.** Split-half design on the
carrying lens: loss alone **0.856–0.868** invariant across
thresholds 1.1–1.3; gains 0.62–0.69; combined 0.82–0.90 (at the
loosest threshold combined < loss — gains can subtract); within the
late block alone loss 0.77–0.86 vs gain 0.52–0.72; within non-epic
0.73–0.75 vs 0.39–0.51; strict presence/absence ≈ 0.40 (0.36–0.42) —
dwindles, not vanishes. Threshold 1.5 is degenerate on C3 (late set
= 1 trigram) — always cite the sweep, not one setting. Committed TSV
at THRESH 1.3 (loss 0.864 / gain 0.62):
`b2b_loss_gain_C3_noreuse_500.tsv`. W1+noreuse refused by the script
(R1 gate); the with-reuse W1 headline (loss 0.939 from 81 features,
gains 0.720, presence 0.474, late block 0.941) is history — the
draft's §6 carries no with-reuse values. Slogan unchanged: "losses
are the clock; gains are the community structure." Frame via
Swadesh-style retention on frequencies, stochastic Dollo (Nicholls &
Gray 2008) as the character-loss relative; do not overclaim the
strict Dollo form. → `2026-08-16_b2_models_loss_gain.md` (design +
with-reuse history), threshold-sweep printouts 2026-08-30 (session
log; values in draft §6).

**4.2 E1: known-order layers (validation as a layer-dating
instrument) — CLEANED values lead (2026-08-30 flip).** CE-excluded
apparatus is uniformly later-styled than its constituted text, every
augmented unit moves lateward, all five books directional. **Primary
citations = cleaned trigram map
(`e1_apparatus/e1_apparatus_C3_noreuse_500.tsv` + constituted
comparators from `unit_ci_C3_noreuse.tsv`): MBh 13 control apparatus
48 [43, 52] vs constituted 31; MBh 18 apparatus 61 [39, 82] vs 8.**
The with-reuse W1 values (MBh 18: 65.1 [47.6, 81.0] vs 4.8; MBh 13:
57.1 [56.3, 61.1] vs 35.7, `e1_apparatus_W1_500.tsv`) are at most a
corroborating clause. Stated asymmetry: the apparatus files
themselves are NOT stripped (outside the strip's corpus) — their
positions mix accretors' composition with what the accretors
absorbed; the direction test doesn't depend on resolving it. Lower
bounds (e-text subset, not Belvalkar's full print apparatus). E1
cannot arbitrate "early composition" vs "looks early".
→ `2026-08-14_e1_apparatus_experiment.md` (+ no-space conversions in
the rerun note; its 62/55/33 values are pre-clean). Fig: 5-row CI
table; dumbbell plot.

**4.3 Internal stratigraphy of known relative order.** PPL stratum inside
Vāyu/Bḍ earlier than the Vāyu↔Bḍ common text (post-clean C3: V8 28 vs 57;
Bḍ2 31 vs 79; CI-separated); SP's pāśupata block late (99) inside an
early text; Kirfel's late Textgruppen sort to his own grouping.
→ `2026-08-14_shared_layers_by_family.md`, `2026-08-16` rerun/cleanup notes.

**4.4 Alternatives survived.** Length (D1/D4), genre (bounded, §6.6),
filler density (refuted: corr 0.27, lowest-density texts at the *late*
pole), names/sectarian vocabulary (struck at ρ 0.99), reuse (removed),
MFW and metric sweeps. → assembled per B4.

**4.5 A4 external diachrony — DROPPED (2026-08-17, Kengo's call).**
Kengo's review of the candidate table found the design category-mismatched:
Oberlies/Meenakshi document *marked deviations and functions* from the
classical standard, not the frequencies of unmarked vocabulary — and the
axis is made entirely of the latter. Any "expected direction" column would
be our own inference dressed as external documentation (soft circularity);
the one literature-licensed subset (obsolete forms must decline) is
sparse, scribally leveled, and un-diagnostic on failure. The external
burden of Q2(b) rests on 4.2/4.3 (known relative order — stronger than any
grammar comparison) and 4.6 (dated anchors). **Promoted to a methods
point instead:** the axis lives in the unmarked frequency band that
grammars of deviation are structurally blind to — which is also the band
conscious imitation cannot easily target; state this where Q1 is
summarized, and use it to answer the "did you check Oberlies?" referee
head-on. Fallback if a referee insists: the bounded obsolete-form
depletion check, with its transmission-leveling caveat stated.

**4.6 Anchors with external dates.** Old SP's 9th-c. Nepalese transmission;
Śivadharma's external dating; epics' relative-antiquity consensus. BhP is
**never** in this list. Honest limit stated every time: the axis orders
*language states*; language age ≠ book age (transmission can preserve or
level; the SP transmission-conservatism confound bounds but does not
explain — its own pāśupata block styles late under identical transmission).

---

## 5. Q3: the second axis

**5.1 No arch.** y ~ quadratic(x): R² = 0.018 (W1) / 0.007 (C3)
with-reuse; **no-reuse: C3 0.006, W1 0.174** (the R1 length artifact,
not a horseshoe — quote it as such). The Guttman-horseshoe reading is
dead on arrival; must be measured before interpreting y, and was.
→ `2026-08-16_axis_anatomy_a1_b1_b5.md`; no-reuse values printed by
`q3_y_covariates.py --noreuse` (2026-08-21).

**5.2 Named, with its confidence stated.** Cross-lens ρ_y **0.82** raw
(post-clean). Axis 2 = third-person enumerative cataloguing ↔
second-person devotional address. Strongest covariate: devotional-vocab
*density* (C3 −0.60); sect polarity ~0 vs y (it loads on x instead);
combined covariates explain about half the rank variance (R² 0.45–0.55).
C4 within-family checks concur (ŚiP saṃhitās −0.62; optative share tops
MBh/Rām). Write-up rule: name it "to the extent the lenses agree";
**never a second chronology** — y-nearness without x-nearness is register
kinship, not date. → `2026-08-16_q3_y_axis_covariates.md`. Fig: covariate ×
lens table with "vs x" contrast column.
**No-reuse replication (2026-08-21,
`axis_anatomy/q3_y_covariates_noreuse.tsv`, draft §9.1 numbers):**
naming carries over (sect density −0.52, optative −0.59 on C3, robust
to sub-3k drop; combined trigram R² 0.58) with four differences to
state honestly: ρ_y 0.69 (vs 0.82); y inherits a length covariate on
residues (≈ −0.4, W1 −0.59 — quote C3); sect polarity −0.33 on
residues (≈0 only on full texts); and **the BhP no longer anchors the
in-plane pole** (within 0.25 SD, sign lens-dependent — its identity
moved to axis 3, tie to §5.3/§9.2). The old "BhP anchors the
devotional pole" wording is with-reuse-only — do not use it for the
no-reuse build.

**5.3 The third axis (draft §9.2) — no-reuse-only reading (Kengo,
2026-08-21).** All §9.2 statistics come from the no-reuse build:
variance shares 5.6/9.7% (W1 ax3/ax2) and 5.7/7.2% (C3), cross-lens
per-axis 0.95/0.74/0.74, BhP offset +3.8/+4.9 SD, point-biserial
0.76/0.84, BhP-excluded ax3 0.65 / ax1 0.95, length ρ ≤ 0.06 — source
`figures/mds3d/axis3_stats.tsv` (A6). The ONE permitted with-reuse
number is the foil 0.46 (ax3 cross-lens before the strip) — precedence
evidence, keep it. Flattening exhibit = **Bh2~Vi3 on C3 no-reuse**
(Delta 1.183, ranks 78/99, 2-D 0.042, 3-D 0.64; residues 3.9k/4.8k) +
non-BhP ŚDh~V10 (Delta 1.346, ranks 105/83, 2-D 0.038); census 86
pairs C3-no / 79 W1-no, ~1/3 BhP — source
`figures/mds3d/flattened_pairs.tsv` (filter `sub3k`=0 before citing a
pair). The old Sn–Vi3 exhibit was with-reuse-W1 and does NOT replicate
on no-reuse maps — do not reintroduce it in the draft (it survives in
`notes/2026-08-21_3d_projection.md` as the origin story). Wording:
BhP symmetric, never archaizer/anchor.

---

## 6. Text-historical findings (the payoffs)

**6.1 Closing parvans.** The merged block (15–18, ~17k words) sits at the
extreme epic pole; not length (D4), not genre, not filler; E1 shows the
constituted text owns the position. Block-level claims ONLY (sub-3k units
are uncertainty regions). Wording: "heavily edited before the archetype
behind the Critical Edition was fixed"; consistent with an early-fixed
narrative kernel appended late as books (Lüders/Jacobi), compatible with
Brockington's late-epilogue verdict about their status as *books*.
→ `2026-08-14_closing_parvans_claim_and_objections.md`, `2026-07-15` diagnostics.

**6.2 PPL priority (stage 1 of the theory).** PPL Textgruppe I + ungrouped
hold linguistic priority; late Textgruppen sort to Kirfel's own
grouping. **Citable band values (2026-08-30) = the CLEANED trigram
map, `unit_ci_C3_noreuse.tsv`: early I 24.8 [23.2, 29.6] / ungrouped
24.8 [23.6, 27.2] / II 32.0 [27.2, 38.4] (draft: "25–32"); late Ia
64.0 [50.7, 73.6] / III 73.6 [63.6, 83.2] / IIB 88.0 [83.2, 90.4] /
IIA 93.6 [89.6, 96.8] (draft: "64–94"). The with-reuse post-clean
bands (early 23–37, late 48–79 W1 / 66–95 C3) are superseded for the
draft.** The Vāyu is a late-idiom composition embedding a
genuinely archaic genealogical stratum — "its reputation for antiquity is
its cargo, not its voice." Counter-cases to print: V1 cosmogony reversal
(real, C3-suggestive); ViP paraphrase reversal (W1-led) — the ViP reworks
rather than transmits. → `2026-08-14_shared_layers_by_family.md`,
`_complement_halves_vayu_bd_visnu.md`, post-clean values in cleanup note.
Fig: dot-strip stratigraphy figure; PPL-vs-vayubd CI table.

**6.3 Sequence: PPL → old SP → Mārk — REFRAMED as VALIDATION (Kengo,
2026-08-30).** The old SP is placed by its editors (Adriaensen,
Bakker, Isaacson) among the oldest purāṇas, **after only the
ur-Vāyu** — so the instrument's placement is *agreement with the
philology that had the text*, not a departure. Hazra's received
dating is no counter-witness: **he did not know the SP as an
independent purāṇa** — his chronology was built without the text.
Draft §8 carries this as a bold-led validation item ("an
independently established early purāṇa measures early"), moved out
of "what the corpus says back". Cleaned values: SP 29 [27, 32]
earlier than Mārk 32 [28, 35]; the with-reuse gap was wider partly
because of the Mārk's +6 drag (absorbed later material) — §7
cross-reference. Layer level: sequence interleaves (Mārk 94–141
at/below the PPL band; SP pāśupata block 98 [97, 99] as a stripped
residue, 2.9k words — brushes the floor, flag it). The ur-Vāyu
parenthetical in the draft (the editors' one earlier text = the kind
of dissolved core the strip greys out; the Vāyu residue answers for
compilers, not the ur-text) is Claude's inference — **Kengo to
confirm it matches the editors' position**. Transmission-conservatism
confound flagged and bounded by the pāśupata contrast.
→ `2026-08-14_sp_mark_ppl_sequence.md` (pre-reframe record; its
"contra the received relative dating" framing is superseded),
Adriaensen et al. 1998. Fig: forest plot of PPL/SP/Mārk layers.

**6.4 Genre control (vaṃśa) — DROPPED as circular (2026-08-19, Kengo's
call), replaced by the strip-first defense.** The vaṃśa marker split
never measured register in this corpus: per Kirfel, the genealogical
genre IS the shared ancient inheritance, so the gen-half Δ conflates
"list-register reads early" with "these lines are genuinely old borrowed
text" — inseparable even on the residue build (sub-threshold paraphrase
survives the strip; Vāyu-08's residue keeps 178 vaṃśa words). A
dharma-pulls-late variant is circular the same way (the movers table
shows borrowed mass drags toward its *sources'* position — an age effect
wearing genre clothes, both directions). Do not run or resurrect
content-split genre controls; the 2026-08-14 and 2026-08-19 TSVs
(`genre_control/genre_control_*_500.tsv`) are retained as documentation.

**The genealogy-therefore-early objection is answered instead by:**
1. **The strip itself (primary; both directions).** The one-directional
   strip (kirfel = source) removes every near-verbatim PPL line from the
   containers while the PPL keeps everything. Container side: the
   carriers no longer contain the PPL, so **the PPL cannot affect its
   containers' positions** — their late residues (Vāyu 80.8 C3-noreuse)
   are the compilers' own voice, not cargo. PPL side: the PPL keeps its
   band (I 24.8 [23.2, 29.6], ungrouped 24.8 [23.6, 27.2]) against a
   corpus none of whose texts carry its copies — no center-of-gravity
   echo. The stratigraphic separation is therefore between textually
   disjoint bodies; what remains is style. (Qualifier: "no PPL text"
   means above the ratio-70 match threshold; sub-threshold paraphrase
   can survive — which is why the content-split control stayed circular
   while this construction-level argument does not depend on it.)
2. **The early pole is not genealogical.** The earliest units on every
   build are epic battle/dialogue parvans and Rām kāṇḍas, thin on vaṃśa
   material. List-register per se does not read early.
3. **E1** — same genre both sides, known-later measures later (§4.2;
   noreuse values in the reframe note).
4. **Axis-2 orthogonality** — register variation has its own dimension
   (§5; arch check R² ≤ 0.02).
→ `2026-08-19_noreuse_precedence_reframe.md` §R3 + this decision.

**6.5 Rāmāyaṇa.** Feature-system split: C3-only trail vs MBh (medians 7 vs
12 post-nospace); W1 as archaic as MBh. Kāṇḍas internally compressed, no
Bāla/Uttara lateness signature — evidence of near-contemporary composition
of the kāṇḍa texts (D6 "late control" withdrawn). External sweep: earliest
attestation ~1st–2nd c. (Aśvaghoṣa), dense by the 7th; but proof-text
quotation asymmetric vs MBh (nibandha ratio ≈ 1:7–1:10) — a genre/register
fact, not a date fact. → `2026-08-14_three_debates...md`,
`2026-08-17_ramayana_first_references_sweep.md`. Fig: kāṇḍa/parvan strip; witness table.

**6.6 Bhāgavata (the open question, symmetric wording ONLY).**
Corpus-internal: sui-generis register (all skandhas' NNs internal —
verified on both builds 2026-08-21);
~~scale-dependent U-shape (mean W1 pct 19@30 → ~50@80–500 → 26@5000)~~
**RETIRED 2026-08-21, do not cite:** the U-shape's outer legs read
non-drift axes (at 30 MFW no setting yields the drift axis, ρ_ref ≤
0.70; the @5000 axis-1 is a length axis, ρ_logT +0.91 — the drift axis
survives as axis 2 there and puts BhP at 56). Within valid settings the
BhP's cross-scale movement is ordinary on W1 and on the no-reuse build
(`mfw_sweep/bhp_scale_settings.tsv`, `bhp_scale_ranges.tsv`; one open
anomaly on with-reuse C3 flagged in the note, not draft material);
over-performance on epic-discriminative words (39% vs late block 5%);
noreuse reveals ViP-register affinity by *subtraction* (BhP retention
89–99%); BhP 9 verbatim-inherits the PPL vaṃśa stock (35 hemistichs ≥
0.85) — the sharing exists exactly where the genre is. External: three
channels (exact shingles, fuzzy, semantic) agree — **no BhP-distinctive
quote in any securely datable author before ~1000**; Māṭhara is the sole,
dating-circular possible exception (cite as crux, not anchor); Utpala's
Spandapradīpikā must be cited from the literature (not in library).
Guardrails: never "archaizer" as premise; never an anchor; the disowned
"artifact" verdict and the wrong "ViP dependency" argument must not
appear. The article *poses* the BhP question with both readings open.
→ `2026-07-30_visnu-bhagavata_noreuse_observation.md`, `2026-08-17_bhp_*` (3 notes),
`2026-08-14_three_debates...md`. Fig: U-shape curve; retention table;
oldest-witnesses table.

**6.7 Purāṇa-genre philology.** Dated non-purāṇic witnesses use "purāṇa"
in the singular in lore-enumerations for centuries (Patañjali, Arthaśāstra,
Amarakośa) while ritual lists go plural early (Manu 3.232); pañcalakṣaṇa
definition bridges them; vāyu-prokta attribution continuous MBh 3 →
Vācaspati ~950. The one purāṇa named across a millennium is the corpus
whose oldest stratum the axis isolates. → `2026-08-14_purana_witnesses_library_sweep.md`,
`_three_debates` §3. Fig: dated-witnesses table.

---

## 7. Standing guardrails (collected wording rules)

1. BhP: symmetric wording; never an anchor; never "archaizer" as premise.
2. Closing parvans: block-level only; language age ≠ book age.
3. Sub-3k units: uncertainty regions, no individual ranks.
4. "Most frequent words", not "function words".
5. Sandhi/orthography/word-division: editorial, not authorial — any C3
   finding that could be edition-driven is flagged, not interpreted.
6. PPL: a corpus reconstruction, not a transmitted title; "earliest layer"
   claims stay layer-specific (V1 cosmogony is the printed counter-case).
7. y is never a second chronology.
8. Genre: no content-split genre control is cited (dropped as circular,
   §6.4) — the genealogy objection is answered strip-first (PPL early on
   a PPL-free corpus), then epic-narrative early pole, E1, axis-2
   orthogonality.
9. Mārk 1–80 is the *latest* Mārk layer (the misattributed early claim is
   corrected in `sp_mark` — do not resurrect it).
10. Report axis-1 share only together with the length diagnostic.
11. **Departures from received chronology = problem-locators (Kengo,
    2026-08-29).** Validation means independently *known* relative
    order — the instrument passes every such case; never hedge that
    with "generally". Where the ordering contradicts *received
    opinion* (BhP placement, MBh/Rām precedence), frame the
    contradiction as landing where scholars had already recorded
    reservations — the method locates where the received chronology
    is soft. Never frame such departures as validation failures.
    Kept general in the DH draft; the Indological companion names the
    reservations. (SP-before-Mārk left this list 2026-08-30 — it is
    now a validation item, §6.3: the editors who knew the text concur;
    Hazra's chronology was built without it.)
12. **Abstract generality (Kengo, 2026-08-29):** "chronology on a
    corpus" stays general — śāstric experiments suggest the method
    may transfer to philosophical texts; don't narrow it to
    "authorless".
13. **With-reuse values are diagnostic, never robustness
    (2026-08-30).** No with-reuse number appears as a representative
    result anywhere; where one appears (draft §7, or a with-reuse
    foil like the axis-3 0.46), it is labeled as a measurement of
    what the contamination was doing. "The ordering survives X" is
    banned phrasing for reuse/colophons/spacing — the cleansing
    defines the corpus; the comparison diagnoses the contamination.
14. **Cleaned-build C3 is the carrying lens everywhere.** Per-unit
    claims cite C3 percentiles from `unit_ci_C3_noreuse.tsv`; W1
    corroborates orderings and directions only (R1); W1 feature
    rates may be correlated against the C3 axis (the §5
    construction) but never against the W1-noreuse axis.
15. **Terminology — settled (Kengo, 2026-08-30): plain
    with-reuse/no-reuse for build labels**; "cleaned", "transmitted
    map", "composition" never name a build in draft prose (see §0).

---

## 8. Open dependencies before final prose

| Item | What | Who | Blocking what |
|---|---|---|---|
| ~~A4~~ | DROPPED 2026-08-17 — see §4.5; nothing blocks on it now | — | — |
| ~~R1~~ | DONE 2026-08-19 — verdict: no-reuse chronology is C3-led, W1-noreuse partly length artifact (see §0 gate) | — | — |
| ~~R2~~ | DONE 2026-08-19 — `noreuse_reframe/movers_C3.tsv` is the citable consequences table (16 CI-separated moves) | — | — |
| ~~R3~~ | DONE 2026-08-19. PPL bands + E1 carry over; genre control then DROPPED as circular (Kengo) — §6.4 now carries the strip-first replacement defense | — | — |
| ~~R4~~ | RESOLVED 2026-08-19 (Kengo): borrowed mass drags toward the sources' position; Śivadharma-incorporators late-ward | — | — |
| ~~A6~~ | DONE 2026-08-19: `figures/mds3d/axis3_stats.tsv` (axis3_analysis.py) — citable axis-3/BhP numbers | — | — |
| ~~A5~~ | DONE 2026-08-29 — `a5_text_anatomy_{W1,C3}.tsv`, feeds the Indological companion's worked-example boxes (§3.4) | — | — |
| ~~A3~~ | DONE 2026-08-29 — axis resists compression; 7-feature honest exhibit if wanted (§3.3) | — | — |
| E1-full | Belvalkar print apparatus (OCR) | optional | strengthens 4.2 magnitudes |
| ~~B1 re-run~~ | DONE 2026-08-30 on the cleaned build (`b1_jackknife_C3_noreuse_500.tsv`, min 0.991) | — | — |
| Terminology | rule on cleaned/transmitted vs with-reuse/no-reuse (§0, guardrail 15) | Kengo | draft wording pass |
| A2-bridge | which axis for W1 signal shares under R1, then `a2_bridge_c3_classes.py --noreuse` | Kengo (design), then cheap run | §2.4 draft slot (1.1 shares) |
| §8 layers | within-host layer projection: restate as same-transmission or drop for the disjoint form | Kengo | §8 draft slot |
| §5 glosses | vet trigram glosses (mṛt, aye, ātr, …) | Kengo | §5 wording |
| ur-Vāyu note | confirm the draft's ur-Vāyu parenthetical matches Adriaensen et al.'s position | Kengo | §6.3 / draft §8 |
| Venue | pick from outline variants | Kengo | everything downstream |

## 9. Figure/table shortlist (cross-variant core)

1. **Hero map pair — REBUILT ON THE CLEANED BUILD 2026-08-30**
   (`figures/fig1_map_pair/fig1_map_pair.{py,pdf,png}`; C3 panel (a)
   first — trigram-led; coords from `mds3d/*_noreuse_n126.tsv`;
   sub-floor residues faded per §3.4 discipline; greedy label
   placement, final label polish at proofs). — all variants
2. W1×C3 convergence heatmap — REBUILT cleaned 2026-08-30, plateau
   wording (1.1–1.2). — all
3. A2 decomposition tables (Q1 centerpiece). — all
4. B2 null-model table with length-diagnostic column. — DH/wide lead fig
5. B2b loss/gain table ("retention clock"). — wide's headline, DH core
6. Layer stratigraphy dot-strip with bootstrap whiskers (6.2). — Indological lead
7. PPL/SP/Mārk forest plot (6.3). — Indological
8. E1 CI table + dumbbell (4.2). — all
9. Genre-control CI table with Δ (6.4). — Indological/DH
10. Q3 covariate table (5.2). — DH; compressed elsewhere
11. External-witness tables: purāṇa usage; Rām attestation; BhP oldest
    quotes (6.5–6.7). — Indological; SI elsewhere
12. Closing-parvans length-control panel (1.8). — all (the honesty figure)
13. **§7.2 drag table — COLUMNS INVERTED 2026-08-30** (Table 1: 16
    CI-separated + grazing Dh; now composition (cleaned) |
    as transmitted | drag, drag = with-reuse − cleaned, positive =
    absorbed material dragged lateward; sorted by drag descending;
    V8/Vi5 †-flagged sub-3k). The draft's table was hand-inverted
    from the 2026-08-21 output — **`movers_table.py` still emits the
    old column order; teach it the new format before the next
    regeneration, then regenerate, never hand-edit.**
14. One-line chronology strip with CI whiskers, both C3 builds
    (`figures/one_line/one_line_C3.pdf`; true axis-1 coordinates from
    the coords TSVs, R2 CIs mapped rank→coordinate). Candidate
    alternative/supplement to fig 1; shows the epic shelf, crowded
    middle, sparse late tail at true distances. — DH/wide
