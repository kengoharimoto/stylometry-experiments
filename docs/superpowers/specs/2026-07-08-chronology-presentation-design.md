# Design: 30-minute presentation — "Chronological Stratification in the Epics and Purāṇas: Evidence from Stylometric Seriation"

**Date:** 2026-07-08
**Deliverable:** A PowerPoint (`.pptx`) slide deck, ~20 content slides plus backup
slides, delivering on the submitted abstract (`materials/abstract_harimoto.md`).
**Audience:** Scholars of the Sanskrit epics and Purāṇas; mostly unfamiliar with
computational text analysis (a few specialists present).
**Timing assumption:** ~25 min talk + 5 min Q&A.

## Narrative strategy

Approach A ("the axis emerges"), modified per author: **open with the payoff
plot itself** — a fully annotated MDS scatter in which the texts visibly sit in
the familiar relative chronological order — and only then unpack how the plot
was obtained. Methods are kept intuitive (no formulas in the main deck).

## Five-act structure

### Act 1 — The picture (3–4 min, slides 1–4)
1. Title slide (title from the abstract; speaker/venue placeholders).
2. **Hero plot**: custom MDS scatter (wurzburg / Cosine Delta, 2026-07-08 run),
   color-coded by chronological stratum, clean labels on landmark texts
   (MBh parvans, Rām kāṇḍas, Vāyu/Brahmāṇḍa, Viṣṇu/Mārkaṇḍeya,
   Agni/Garuḍa/Nārada, Bhāgavata), horizontal arrow *earlier ⟶ later*.
3. The claim stated plainly: no dates, no chronology, no philological judgment
   entered the computation — only counted linguistic habits — yet the map
   reproduces the accepted relative chronology.
4. The question raised: what was counted, and can the axis be trusted?

### Act 2 — How the plot was made (6–7 min, slides 5–9)
- Corpus: 101 texts/sections (epics by parvan/kāṇḍa; purāṇas whole or by
  khaṇḍa/saṃhitā); brief note on sources and the length-imbalance caveat.
- "Style as unconscious countable habits": actual top MFW from this corpus
  (*ca, tu, hi, eva, tathā…*).
- Two independent lenses: word unigrams on unsandhied (segmented) text vs.
  character 3-grams on raw sandhied text; one line on why these are nearly
  orthogonal measurements.
- Distance table (101×101) → MDS as "flattening a mileage chart into a map"
  (explainer graphic).

### Act 3 — Reading the map (7–8 min, slides 10–14)
Guided tour; each stop a philological sanity check:
- Epic zone: battle books 6–9 tight (7↔8 tightest); MBh 12–13 drift toward
  purāṇa-space; Rām core 2–6 vs. Bāla↔Uttara mutual affinity (NN in both
  feature sets) — higher criticism recovered blind.
- Old purāṇic core: Vāyu↔Brahmāṇḍa at 0.08 ("Kirfel's *Vāyuproktaṃ Purāṇam*
  as a number"); Viṣṇu↔Mārkaṇḍeya; Matsya adhy. 176 parallel material.
- Late sectarian-encyclopedic zone: Agni–Garuḍa–Nārada digests; the
  Śivapurāṇa's saṃhitās refuse to unify (compilation model confirmed).
- The Bhāgavata: all twelve skandhas' nearest neighbours internal; deliberate
  archaizing does not fool the model.

### Act 4 — Why believe the axis? Robustness (5 min, slides 15–17)
- The abstract's core argument: the seriation axis replicates across feature
  sets (W1 vs. C3), preprocessing (sandhied vs. unsandhied), and distance
  metrics. Small-multiples grid of 4–6 MDS plots with identical coloring.
- Convergence argument: any unsandhi-pipeline artifact could affect only W1,
  any orthographic/sandhi artifact only C3 — agreement means the signal is in
  the texts.
- The **second** axis is unstable (genre? region? sect?) — one slide of honest
  agnosticism, as promised in the abstract.

### Act 5 — Caveats and implications (3–4 min, slides 18–20)
- The axis as diachronic linguistic drift — confounded with genre/metre
  (particles as anuṣṭubh fillers) and with borrowing (shared ślokas drive the
  tightest links; Delta cannot distinguish "same school" from "copied the same
  2,000 ślokas").
- Purāṇas have no authors: this is stratum/textual-family detection, not
  authorship attribution.
- Implication: stylometry as an independent, replicable check on relative
  chronology; limits of MDS when axes resist stable labels.
- Closing slide returns to the hero plot.

### Backup slides (for Q&A)
- Delta in more detail (still mostly verbal).
- Full 101-text corpus list with strata.
- Length-imbalance caveat (sub-5k-word fragments, inflated distances).
- W1/C3 disagreement cases as diagnostics — esp. the commentary-contaminated
  BhP 10.29–33 file (word features contaminated, character features robust).
- BCT consensus tree (wurzburg).

## Figures (all built fresh; raw stylo PDFs not used in main deck)

| Fig | Content | Source data |
|---|---|---|
| F1 | Hero MDS plot, annotated, stratum-colored | latest run distance tables / MDS coords |
| F2 | Small-multiples robustness grid (W1 vs C3 × 2–3 metrics) | same |
| F3 | Top-MFW chart/table for "countable habits" | frequency tables / corpus |
| F4 | "Mileage chart → map" MDS explainer | constructed |

Plot style: readable at slide scale (≤ ~30 labelled points; unlabelled points
as colored dots), IAST in labels, consistent stratum palette across all figures.

## Chronology reference (user-confirmed gate)

Before any plotting, draft a stratum assignment for all 101 texts —
provisional scheme: ① epic core, ② late epic strata (MBh 12–13, Rām 1+7),
③ old purāṇic core, ④ middle purāṇic, ⑤ late sectarian/encyclopedic, with the
Bhāgavata specially marked — based on Kirfel/Hazra and the interpretation
notes. **The user corrects/approves this table before figures are built.**

## Early validation gate

The hero plot must actually show the seriation. First step of implementation:
extract MDS coordinates from the 2026-07-08 W1 and C3 runs, check which
metric/configuration displays the chronological axis most cleanly, and show
the user 2–3 candidates before committing to F1.

## Build pipeline

1. Python (matplotlib) scripts under `scripts/presentation/` generate figures
   as PNG/PDF into `materials/presentation_2026/figures/`.
2. Deck built as `.pptx` (via the document-skills:pptx workflow) into
   `materials/presentation_2026/`.
3. Slide text drafted in Markdown first for user review, then rendered.

## Out of scope

- New stylometric runs (uses existing 2026-07-08 results).
- Speaker notes beyond brief per-slide cues.
- Devanagari typography (IAST throughout).
