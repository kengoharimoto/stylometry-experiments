# Claims-and-evidence map (venue-neutral)

**Date:** 2026-08-17
**Purpose:** the single source of truth for drafting. Every article variant
(see `outline_*.md`) draws its claims, numbers, and figures from here, so
the variants cannot drift apart factually.

**Citation rule:** numbers in this map are for architecture and orientation,
transcribed from the notes. Before any number goes into printable prose,
verify it against the source note and, where applicable, the TSV it cites.
Canonical values are **post-colophon-clean** (corpus state ≥ 2026-08-16)
and **no-space C3**; the provenance gates in §0 list the traps.

---

## 0. Conventions and provenance gates

- Corpus: 127 units, manifest `dicsep2026_n127_ppl`, colophon-free since
  2026-08-16 (`is_colophon_line()` in the shared source filter).
- Lenses: **W1-500** (unsandhied words, ByT5 int8 pipeline) and **C3-500
  no-space** (char trigrams over the whitespace-stripped sandhied stream,
  `hero_mds.py --strip-spaces`). Burrows's Delta, classical MDS,
  Procrustes-aligned to the hero reference.
- Layer/subset instrument: fixed-map Gower supplementary projection +
  line-bootstrap CIs (B=500, seed 20260814). Never recompute the map on
  gutted corpora for layer questions.
- **Traps when quoting notes:**
  - Never quote pre-clean numbers (git ≤ d9532dd; the pre-clean unsandhied
    corpus survives only in commit 0b666a9's safety copy).
  - C3 percentiles in the 2026-08-14 notes are **standard-C3**; the
    conversion table is `2026-08-16_nospace_c3_adoption_rerun.md` — but
    that note's tables are themselves **pre-clean**; final C3 numbers come
    from `2026-08-16_colophon_corpus_cleanup.md` and the post-clean TSVs.
  - B1 jackknife numbers in `2026-08-16_axis_anatomy_a1_b1_b5.md` are
    pre-clean (conclusions insensitive; re-run if a referee needs it).
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
ordering: ρ_x = **0.953** at the 500×500 sweet spot. The A2 bridge shows
they do it from largely disjoint material (closed classes = 38% of W1's
signal but 12% of C3's; C3 is 61% word-interior morphology).
→ `2026-07-08_W1-unsandhied_vs_C3-sandhied_interpretation.md`,
`2026-08-16_a2_bridge_word_classes_in_c3.md`. Fig: convergence table;
class signal-share table.

**1.2 MFW robustness.** C3 x invariant 250–12000 (ρ ≥ 0.95 vs 5000);
W1 plateau 80–800, cliff above ~1500 (content takeover); convergence ridge
peaks at 500×500 (0.894 standard-C3 → 0.949 no-space). Terminology
guardrail: say "most frequent words", not "function words" (top-80 already
contains deva, dharma, śiva). → `2026-08-14_mfw_robustness_W1_C3.md`.
Fig: W1×C3 cross-correlation heatmap; plateau/cliff tables.

**1.3 Metric robustness.** All standardization-based measures and L1-type
measures reproduce the axis (ρ 0.95–1.00); only unstandardized
cosine/Euclidean blur it, for stated reasons; Delta-family interchange is
expected (Evert et al. 2017) — a consistency check, not independent
confirmation. → `2026-08-14_distance_metrics_W1_C3.md`. Fig: 8×3 table.

**1.4 Reuse independence.** Noreuse build reproduces the ordering:
cross-build ρ_x 0.98–0.99 at recommended settings; the collapsed high-MFW
W1 regime anti-correlates (−0.86 at 5000), confirming what the cliff
measures. → `2026-08-14_mfw_robustness_noreuse.md`. Fig: cross-build table.

**1.5 Names/sectarian vocabulary struck.** Strike 36 theonyms → ρ 0.9976;
strike 67 names + ritual lexemes → ρ 0.9898; BhP moves slightly *later*.
→ `2026-08-14_mfw_robustness_W1_C3.md` addendum.

**1.6 Encoding controls (C3).** Word division is editorial → no-space C3
adopted; agreement with W1 improves at every MFW; movers move toward their
W1 positions. Digraph romanization measured non-issue (ρ ≥ 0.99).
Colophons were real directional paratext bias (ρ −0.58 with shift) →
corpus cleaned; headline results held or tightened.
→ `2026-08-16_c3_nospace_scriptio_continua.md`, `_c3_phoneme_digraph_check.md`,
`_c3_colophon_stripped_check.md`, `_colophon_corpus_cleanup.md`.

**1.7 Independent implementation.** No-space C3-500 reproduced exactly by
R stylo 0.7.5 on a pre-stripped corpus: features 500/500, Delta matrices
ρ 1.0000, map ρ 1.0000. Prescribed methods sentence in
`2026-08-16_stylo_nospace_crossvalidation.md`.

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

**2.1 B1 variance anatomy.** Axis-1 share 13.4% (W1) / 10.6% (C3), spectrum
fat-tailed; jackknife over all 127 deletions ρ ≥ 0.983; leverage suspects
(śāstra outgroup, Śivadharma pair) cleared. C3's 1:2 ratio is 1.13 —
near-degenerate, which licenses B3's top-2-plane comparisons.
→ `2026-08-16_axis_anatomy_a1_b1_b5.md` (jackknife pre-clean).

**2.2 B2 null models (the methodological centerpiece).** Exchangeable null:
axis-1 share 13.1% but it is a *length artifact* (ρ 0.91 vs log length;
real axis: 0.065) — share alone can mislead, always report the length
diagnostic beside it. Heterogeneity without covariance: 3.3%. Brownian
drift process: 43.4% and recovers the latent order at ρ 0.986. A dominant,
ordering-shaped, length-independent first axis is the signature of
**autocorrelated change**. → `2026-08-16_b2_models_loss_gain.md`. Fig: null-model
table with length-diagnostic column.

**2.3 B3 convergent orderings.** PCA/isomap/Fiedler all find the gradient
in their top-2 plane (PCA 0.997/0.995 aligned); C3's raw first-axis flips
are a corpus property (near-degenerate spectrum); TSP snake-fold failure
independently proves a real second dimension. One-sentence exclusion of
t-SNE/UMAP (local neighborhoods, no global geometry).
→ `2026-08-16_b3_convergent_orderings.md`. Fig: raw-vs-aligned two-panel table.

---

## 3. Q1: what the axis counts

**3.1 A1 loadings.** Distributed: only 4/500 (W1), 8/500 (C3) features with
|ρ| ≥ 0.7; median |ρ| ~0.25. Poles read as narrative-dialogic (tam, sa,
abravīt, iva) → prescriptive-doxographic (ādi +0.81; -ika/-ikā, -yet/-yāt
optatives). Whether the register gradient is temporal is Q2's question, not
A1's claim. → `2026-08-16_axis_anatomy_a1_b1_b5.md`. Fig: two-pole loading table.

**3.2 A2 class decomposition (Q1's answer).** No class necessary, nearly
every class sufficient: particles alone 0.889, content alone 0.941,
closed-class union 0.947, word-interior trigrams 0.972; every removal ≥
0.94 (W1). The one real exception: junction/word-final trigrams alone fail
(0.11–0.14) — "no slice destroys the ordering, short of restricting to
boundary phonology." The axis is pervasive, redundant usage change; W1 and
C3 converge across *structural levels*, not just word classes.
Classification hand-review mooted by perturbation check (max Δρ 0.031);
Kengo reviews the printed table only. → `2026-08-16_a2_class_decomposition.md`,
`_a2_bridge_word_classes_in_c3.md`. Fig: the two decomposition tables (Q1 centerpiece).

**3.3 A3 minimal sufficient set — NOT RUN.** Plan item (greedy forward
selection, split-half guarded). Largely superseded by A2's redundancy
result; decide: run cheaply for a "here are 20 features you can check by
eye" exhibit, or drop. → decision open.

**3.4 A5 per-text anatomy — NOT RUN.** Per-feature Delta contributions for
the texts the prose features (closing-parvans block, PPL I, old SP, BhP,
Śivadharma pair). Run after outlines fix which texts get worked examples.

---

## 4. Q2(b): why the axis is time-like

**4.1 B2b retention clock (Kengo's hypothesis, confirmed in frequency
form).** Split-half design: depletion of 81 epic-typical features alone
reproduces the ordering at **ρ 0.939** (0.941 within the late block);
gains loose (0.720); strict presence/absence only 0.474. Slogan: "losses
are the clock; gains are the community structure." Frame via Swadesh-style
retention-rate glottochronology on style-feature *frequencies*, with
stochastic Dollo (Nicholls & Gray 2008) as the character-loss relative;
do not overclaim the strict Dollo form. → `2026-08-16_b2_models_loss_gain.md`.

**4.2 E1: known-order layers (validation as a layer-dating instrument).**
CE-excluded apparatus is uniformly later-styled than its constituted text,
both lenses, every augmented unit moves lateward (MBh 18 apparatus
62 [46,76] W1; MBh 13 control 55 [53,59]). Lower bounds (e-text subset,
not Belvalkar's full print apparatus). E1 cannot arbitrate "early
composition" vs "looks early". → `2026-08-14_e1_apparatus_experiment.md`
(+ no-space conversions in the rerun note). Fig: 5-row CI table; dumbbell plot.

**4.3 Internal stratigraphy of known relative order.** PPL stratum inside
Vāyu/Bḍ earlier than the Vāyu↔Bḍ common text (post-clean C3: V8 28 vs 57;
Bḍ2 31 vs 79; CI-separated); SP's pāśupata block late (99) inside an
early text; Kirfel's late Textgruppen sort to his own grouping.
→ `2026-08-14_shared_layers_by_family.md`, `2026-08-16` rerun/cleanup notes.

**4.4 Alternatives survived.** Length (D1/D4), genre (bounded, §6.6),
filler density (refuted: corr 0.27, lowest-density texts at the *late*
pole), names/sectarian vocabulary (struck at ρ 0.99), reuse (removed),
MFW and metric sweeps. → assembled per B4.

**4.5 A4 external diachrony — NOT RUN (Kengo-led).** Top ~30 drifters vs
documented diachronic tendencies (Oberlies' epic grammar, Meenakshi's epic
syntax). The non-circular external link that closes Q2(b). Session
assembles the candidate table; Kengo reads. Agreements are evidence;
disagreements are honest anomalies to print.

**4.6 Anchors with external dates.** Old SP's 9th-c. Nepalese transmission;
Śivadharma's external dating; epics' relative-antiquity consensus. BhP is
**never** in this list. Honest limit stated every time: the axis orders
*language states*; language age ≠ book age (transmission can preserve or
level; the SP transmission-conservatism confound bounds but does not
explain — its own pāśupata block styles late under identical transmission).

---

## 5. Q3: the second axis

**5.1 No arch.** y ~ quadratic(x): R² = 0.018 (W1) / 0.007 (C3) — the
Guttman-horseshoe reading is dead on arrival; must be measured before
interpreting y, and was. → `2026-08-16_axis_anatomy_a1_b1_b5.md`.

**5.2 Named, with its confidence stated.** Cross-lens ρ_y **0.82** raw
(post-clean). Axis 2 = third-person enumerative cataloguing ↔
second-person devotional address. Strongest covariate: devotional-vocab
*density* (C3 −0.60); sect polarity ~0 vs y (it loads on x instead);
combined covariates explain about half the rank variance (R² 0.45–0.55).
C4 within-family checks concur (ŚiP saṃhitās −0.62; optative share tops
MBh/Rām). Write-up rule: name it "to the extent the lenses agree (ρ ≈ 0.8)";
**never a second chronology** — y-nearness without x-nearness is register
kinship, not date. BhP anchors the devotional pole as a *register* fact,
no date directional. → `2026-08-16_q3_y_axis_covariates.md`. Fig: covariate ×
lens table with "vs x" contrast column.

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
hold linguistic priority: pct 22–28 both lenses, CI-backed; late
Textgruppen sort to Kirfel's own grouping (Ia 61, III 73, IIB 87, IIA 93
on no-space C3). The Vāyu is a late-idiom composition embedding a
genuinely archaic genealogical stratum — "its reputation for antiquity is
its cargo, not its voice." Counter-cases to print: V1 cosmogony reversal
(real, C3-suggestive); ViP paraphrase reversal (W1-led) — the ViP reworks
rather than transmits. → `2026-08-14_shared_layers_by_family.md`,
`_complement_halves_vayu_bd_visnu.md`, post-clean values in cleanup note.
Fig: dot-strip stratigraphy figure; PPL-vs-vayubd CI table.

**6.3 Sequence: PPL → old SP → Mārk.** Old SP whole (26 W1 / 31 C3
post-clean) before Mārk whole (35/43), CI-separated both lenses — contra
the received relative dating; at layer level the sequence interleaves
(Mārk 94–141 at/below the PPL band: 25/25 post-clean; SP 174–183 pāśupata
late). Transmission-conservatism confound flagged and bounded.
→ `2026-08-14_sp_mark_ppl_sequence.md` + post-clean conversions. Fig: forest
plot of PPL/SP/Mārk layers.

**6.4 Genre control (vaṃśa).** Real but bounded: pull ≈ 15–25 points for
mid/late texts, ~0 at the epic end; marker-split Δ is an upper bound.
Post-nospace the C3 floor argument is **no longer CI-clean** — lean on W1
(floor ~46 vs PPL 21–24) and on the genre-immune layer argument (V8's PPL
layer earlier than V8's own vaṃśa common layer, same genre both sides).
→ `2026-08-14_vamsa_genre_control.md` + rerun note flag.

**6.5 Rāmāyaṇa.** Feature-system split: C3-only trail vs MBh (medians 7 vs
12 post-nospace); W1 as archaic as MBh. Kāṇḍas internally compressed, no
Bāla/Uttara lateness signature — evidence of near-contemporary composition
of the kāṇḍa texts (D6 "late control" withdrawn). External sweep: earliest
attestation ~1st–2nd c. (Aśvaghoṣa), dense by the 7th; but proof-text
quotation asymmetric vs MBh (nibandha ratio ≈ 1:7–1:10) — a genre/register
fact, not a date fact. → `2026-08-14_three_debates...md`,
`2026-08-17_ramayana_first_references_sweep.md`. Fig: kāṇḍa/parvan strip; witness table.

**6.6 Bhāgavata (the open question, symmetric wording ONLY).**
Corpus-internal: sui-generis register (all skandhas' NNs internal);
scale-dependent U-shape (mean W1 pct 19@30 → ~50@80–500 → 26@5000);
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
8. Genre discount is applied, not just mentioned; C3 genre floor no longer
   CI-clean — use W1 + layer argument.
9. Mārk 1–80 is the *latest* Mārk layer (the misattributed early claim is
   corrected in `sp_mark` — do not resurrect it).
10. Report axis-1 share only together with the length diagnostic.

---

## 8. Open dependencies before final prose

| Item | What | Who | Blocking what |
|---|---|---|---|
| A4 | top-30 drifters vs Oberlies/Meenakshi table | session assembles, Kengo reads | Q2(b) section's external link |
| A5 | per-feature anatomy of featured texts | session | worked-example boxes |
| A3 | minimal sufficient set | decision: run cheap or drop | optional Q1 exhibit |
| E1-full | Belvalkar print apparatus (OCR) | optional | strengthens 4.2 magnitudes |
| B1 re-run | jackknife on post-clean corpus | optional, cheap | footnote hygiene |
| Venue | pick from outline variants | Kengo | everything downstream |

## 9. Figure/table shortlist (cross-variant core)

1. Hero map pair (W1 + no-space C3), post-clean. — all variants
2. W1×C3 convergence heatmap + sweet-spot table (1.1–1.2). — all
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
