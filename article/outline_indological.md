# Outline A — Indological venue

**Candidate venues:** Indo-Iranian Journal (long articles welcome, Brill);
Journal of the American Oriental Society; WZKS; Asiatische Studien.
**Audience assumption:** knows the texts, Kirfel, Hazra, Rocher's
skepticism, the epic-strata debates; does NOT know Delta, MDS, or why 500
features is a defensible knob. **Length budget:** 15,000–20,000 words +
appendices. **Register:** the stylometry is taught patiently; the results
are organized by *text-historical question*, because that is what this
reader came for.

**Working title idea:** "A drift axis for epic and purāṇic Sanskrit:
stylometric evidence for the relative chronology of the pañcalakṣaṇa
corpus, the early purāṇas, and the Mahābhārata's closing books."

---

## 1. The problem (≈1,500 w)
Purāṇic chronology after Kirfel and Hazra; Rocher's counsel of despair;
why relative ordering of *language states* is the tractable question.
What stylometry can and cannot promise (language age ≠ book age, stated
on page one, not in the small print). The three questions the paper
answers (what is counted; why an ordering emerges; what it yields).

## 2. Corpus and method, taught (≈3,000 w)
127 units; the two lenses explained for a philologist: W1 = the habits of
whole words once editorial sandhi is undone; C3 = the texture of the
continuous syllable stream exactly as a manuscript reader meets it
(scriptio continua — word division is editorial, so we strip it). Delta
and MDS in one page each, with the null-model intuition (B2) previewed in
prose. The layer instrument: fixed map + projection + bootstrap CIs.
Hygiene as philology: colophons are paratext and measurably bias the map
(ρ −0.58) — the kind of detail this audience will trust us for.
*Figures: hero map pair; one-page "how to read the map" box.*

## 3. Is the axis real? (≈2,500 w)
Compressed validation stack, each item one paragraph + table row: MFW
sweep, metric sweep, reuse removal, names struck, jackknife, independent
implementation (stylo, exact), convergent orderings (B3), null models (B2)
— here the length-artifact lesson of the exchangeable null is worth its
own paragraph. Length limits: the sub-3k uncertainty region and the
shared-failure-mode confession (1.8). *Figures: convergence heatmap;
robustness summary table; length-control panel.*

## 4. What the axis counts (≈2,000 w)
A1 poles in words a philologist can verify (tam/sa/abravīt/iva vs
ādi/-ika/-yet); A2's answer — pervasive, redundant usage change, no class
necessary, nearly every class sufficient. **The marked/unmarked point**
(Kengo, 2026-08-17): the drifters are ordinary words at shifting rates —
precisely the material a grammar of deviations (Oberlies) is structurally
blind to, and the band conscious archaizing cannot easily target; hence
external validation comes from known relative order and dated anchors
(§3, §7), not from grammar-checking the feature list. *Figures: two-pole
loading table; A2 decomposition tables.*

## 5. The retention clock (≈1,200 w)
B2b for a humanist: glottochronology's retention idea applied to style
frequencies; losses are the clock (ρ 0.939), gains are the community
structure; why this makes "drift axis" more than a metaphor.

## 6. Findings I — the pañcalakṣaṇa corpus and the early purāṇas (≈3,000 w)
6.2 PPL priority; Textgruppen sort to Kirfel's grouping; Vāyu "cargo, not
voice"; V8/Bḍ2 stratigraphy; the V1 counter-case printed honestly; ViP as
reworker. 6.3 PPL → old SP → Mārk sequence with interleaving; the
transmission-conservatism confound bounded. 6.7 the external witness
chain (singular purāṇa, vāyu-prokta continuity, pañcalakṣaṇa definition)
— full treatment, this is the audience for it. *Figures: stratigraphy
dot-strip; forest plot; dated-witnesses table.*

## 7. Findings II — the epics (≈2,500 w)
6.1 closing parvans: the block claim, five objections answered, E1
validation, the Lüders/Jacobi convergence, Brockington compatibility.
6.5 Rāmāyaṇa: the feature-system split; kāṇḍa compression; the attestation
sweep incl. the citation-asymmetry refinement. *Figures: E1 CI table +
dumbbell; kāṇḍa/parvan strip; Rām witness table.*

## 8. Findings III — the Bhāgavata question, posed not answered (≈2,000 w)
Symmetric wording throughout: the register isolation, U-shape,
over-performance, ViP affinity by subtraction, BhP 9's PPL inheritance;
the three-channel pre-1000 quotation negative; Māṭhara as crux; both
readings (early language state faithfully transmitted vs late archaizing
mastery) laid out with what would decide between them. *Figures: U-shape
curve; oldest-witnesses table.*

## 9. The second axis, briefly (≈800 w)
No arch; catalogue ↔ devotion to the extent the lenses agree (ρ ≈ 0.8);
explicitly not a second chronology.

## 10. Conclusions + honest-limits section (≈1,200 w)
What is now established, what is bounded, what is open (BhP; absolute
dates out of scope). Language age ≠ book age reprised.

## Appendices
A: feature lists and per-class tables. B: robustness detail (metric/MFW
full tables). C: the E1 protocol. D: external-witness loci in full.
Data/code availability statement (repo + TSVs).

---

**What this variant cuts:** most of B2's simulation detail (one figure +
appendix); Q3 covariate machinery; the DH-facing methodological novelty
framing (no-space trigrams etc. are *explained* but not *sold*).
**Dependencies:** A5 (worked-example boxes in §6–8); A4 dropped
2026-08-17 (see claims map §4.5) — no longer blocking.
**Risks:** length; a referee hostile to quantification — mitigated by §3's
stack and by every claim carrying a philological handle; a referee
demanding an Oberlies comparison — answered head-on by §4's
marked/unmarked argument; the SP-before-Mārk claim will draw fire — the
CI table and confound-bounding must be airtight.
