# STATUS 2026-08-16 — where we are, resume here

> **SUPERSEDED IN PART 2026-08-19 — read
> `2026-08-19_noreuse_precedence_reframe.md` FIRST.** Kengo's reframe:
> the article gives precedence to the **no-reuse** maps as the chronology
> of original compositions (with-reuse = tradition as transmitted); the
> no-reuse chronology is **C3-led** (W1-noreuse partly length artifact —
> magnitudes not citable); citable numbers from
> `figures/noreuse_reframe/` (movers_C3.tsv, unit_ci_*). E1 and PPL
> bands carry over to the composition chronology. **The vaṃśa genre
> control is DROPPED as circular** (the genre bullet at the bottom of
> this file is obsolete) — the genealogy objection is answered
> strip-first; see claims map §6.4. Axis 3 ≈ the Bhāgavata dimension
> (3-D viewers in `figures/mds3d/`). Drafting state:
> `article/claims_evidence_map.md` (single source of truth, §0 gates),
> `article/draft_dh.md` (complete DH draft, Kengo's editing pass in
> flight; reframe surgery pending).

For the next session. The deliverable is the **article** on stylometric
analyses producing chronological ordering of Sanskrit epic/purāṇic texts.
The DICSEP deck is frozen — never touch it. The working plan is
`2026-08-14_axis_anatomy_plan.md` (Q1/Q2/Q3); the article's claims and
objection-answers are in the 2026-08-14 notes.

## Current conventions (everything below runs on these)

- Burrows's Delta, manifest `dicsep2026_n127_ppl` (127 units).
- **W1-500**: unsandhied words, ref frame
  `figures/mfw_sweep/coords_W1_mfw500.tsv`.
- **C3-500 no-space** (scriptio continua — ALL whitespace stripped before
  trigram counting; `hero_mds.py --strip-spaces`), ref frame
  `figures/c3_nospace/coords_nospace_mfw500.tsv`.
- **Corpus is colophon-free since 2026-08-16** (`is_colophon_line()` in
  the shared source filter; base + derived corpora regenerated, ByT5
  re-run). Never quote pre-clean numbers (git ≤ d9532dd).
- W1×C3 sweet-spot convergence: **0.953**.
- No-space C3 is stylo-cross-validated EXACTLY (500/500 features, delta
  Pearson/Spearman 1.0000, map ρ 1.0000) — see
  `2026-08-16_stylo_nospace_crossvalidation.md`; the "Python pipeline
  alone" caveat is closed.
- Layer/subset questions: fixed-map Gower projection + line-bootstrap CIs
  (B=500, seed 20260814); never recompute the map on gutted corpora.

## What happened 2026-08-16 (this session, 12 notes)

1. **C3 encoding series** (Kengo's methodological instincts, all three
   confirmed productive):
   - Word division is editorial → no-space C3 adopted; convergence
     0.894→0.949 (`c3_nospace` note + adoption/rerun note).
   - Aspirate digraphs: measured non-issue, ρ 0.99 (`c3_phoneme` note);
     kept as robustness citation.
   - Colophons: real directional paratext bias (ρ −0.58 with shift) →
     **full corpus cleanup**, all instruments re-run both lenses; every
     headline result held or tightened (`colophon_corpus_cleanup` note).
2. **Axis-anatomy plan, computational items ALL DONE** (post-clean):
   - A1 loadings: axis distributed (4–8/500 features ≥|0.7|); early =
     narrative-dialogic machinery, late = śāstric-doxographic (ādi +0.81).
   - A2 bridge + decomposition: lenses agree on the map (0.95) from
     ~disjoint material (W1 closed-class+lexis vs C3 word-internal
     morphology); **no class necessary, nearly every class suffices**
     (particles alone 0.89, content alone 0.94, interior trigrams 0.97;
     junction/final alone fail 0.11–0.14). Hand review of classes
     mooted (perturbation max Δρ 0.031); Kengo reviews only the
     printed article table.
   - B1: axis-1 share 13.4%/10.6%, jackknife ≥0.983, leverage groups
     cleared.
   - B2: heterogeneity-without-covariance gives 3.3% axis; drift process
     gives 43% + order recovered at 0.99; exchangeable null = length
     artifact (real axis vs log-length: 0.065).
   - **B2b (Kengo's Dollo/glottochronology hypothesis): CONFIRMED in
     frequency form** — depletion of 81 epic-typical features (split-half
     selected) alone reproduces the axis at **ρ 0.939** (0.94 even
     within the late block); gains loose (0.72); strict presence/absence
     only 0.47 → the clock is *frequency retention*. "Losses are the
     clock; gains are the community structure."
   - B3: gradient present in every global method's top-2 plane (PCA
     0.995+ both lenses); C3 raw first-axis flips = near-degenerate
     spectrum (a corpus property); TSP snake-fold failure independently
     proves the real second dimension.
   - B5 + Q3: **no Guttman arch** (R² ≤ 0.02); cross-lens ρ_y 0.82;
     **axis 2 named: enumerative catalogue ↔ devotional address** —
     strongest covariate is devotional-vocab *density* (C3 −0.60), sect
     polarity ~0; combined rank-R² 0.45–0.55; C4 within-family checks
     concur. BhP anchors the devotional pole (register fact, no date
     claim — standing guardrail).

## Open items (in rough priority for the article)

1. **Article plan/outline** — NOT YET WRITTEN. Map the ~25 notes
   (2026-08-14 evidence chain + 2026-08-16 anatomy) onto a section
   structure; pick venue (decides length + how much stylometry pedagogy).
2. **A4 (Kengo-led)**: top ~30 drifters vs documented diachrony
   (Oberlies epic grammar, Meenakshi epic syntax); table
   "feature — axis direction — independently documented drift". The
   non-circular external link that closes Q2(b). Session assembles, Kengo
   reads.
3. **A5**: per-text anatomy of the extremes (closing-parvans block,
   PPL I, old SP, BhP, Śivadharma pair) — per-feature Delta contributions
   in words a philologist can verify. Best after the prose knows which
   texts it features.
4. Full-strength E1 (Belvalkar print apparatus, needs OCR) and per-parvan
   didactic-overlay proxy — old strengthening items, optional.
5. Housekeeping: `corpus/epic_puranas_unsandhied_precolophon_bak/` is
   in fact TRACKED (committed in 0b666a9) and is the only exact record of
   the pre-clean unsandhied corpus (the ≤ d9532dd tracked copies are stale
   — all 74 differ). Keep it in git; the working-tree copy may be git-rm'd
   without loss. B1 jackknife numbers in the anatomy note are pre-clean
   (conclusions insensitive).

## Key claims inventory (all CI-backed, post-clean, both lenses)

- Closing parvans: merged block at epic pole; E1 validates axis on
  known-order layers; formulation + objections in
  `2026-08-14_closing_parvans_claim_and_objections.md`.
- PPL priority: early block 24–32 both lenses; late Textgruppen sort to
  Kirfel's own grouping; PPL stratum inside Vāyu/Bḍ earlier than
  Vāyu↔Bḍ common text (V8 28 vs 57; Bḍ2 31 vs 79).
- Sequence: PPL I/ungrouped → old SP (26/29) before Mārk whole (35/38),
  CI-separated; Mārk 94–141 at/below the PPL band (25/25);
  purāṇa-reference philology in `three_debates` + `purana_witnesses`
  notes.
- BhP: scale-dependence U-shape + over-performance; symmetric wording
  ONLY (never "archaizer" as premise); never an anchor. NEW 2026-08-18:
  inbound channel — the BhP quotes/presupposes the Brahmasūtra (1.1.1
  verbatim unit; frame 1.5.4; corpus-unique parābhidhyāna in skandhas
  3+5; samanvaya cluster; 12.13 colophon); converges with the outbound
  pre-1000 silence on the same window; a milieu argument, still not an
  absolute anchor — see `2026-08-18_bhp_brahmasutra_dependence.md`.
- Rām: trails MBh on C3 only (medians 7 vs 12); W1 no.
- Genre: ~~vaṃśa pull bounded; W1 floor argument decisive; C3 floor
  narrowed post-nospace — lean on W1 + the genre-immune layer argument.~~
  **OBSOLETE 2026-08-19: genre control dropped as circular (Kirfel:
  vaṃśa genre IS the shared inheritance). Strip-first defense instead —
  see the banner above and claims map §6.4.**
