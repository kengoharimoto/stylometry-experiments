# Plan: three explanatory questions for the article

**Date:** 2026-08-14 (evening)
**For:** future sessions in this repo, with Kengo
**Status:** plan only; nothing below has been run.

The article currently *validates* the drift axis (MFW sweep, metric sweep,
reuse removal, layer stratigraphy, genre control, exclusion test) but does
not yet *explain* it. Three questions to examine and, hopefully, answer:

- **Q1.** What exactly moves a text left or right?
- **Q2.** Why does chronology — or rather linguistic drift — appear in the
  MDS at all?
- **Q3.** What exactly is in the y-axis?

Shared infrastructure, already built and to be reused rather than
reinvented: the fixed sweet-spot maps and Gower supplementary projection
(`complement_halves/project_halves.py`), line-bootstrap CIs
(`bootstrap_cis.py`), the exclusion-and-refill harness
(`mfw_sweep/exclusion_test.py`), and the sweep coordinate TSVs. All new
work at W1-500 / C3-500, manifest `dicsep2026_n127_ppl`, unless noted.

---

## Q1 — What moves a text left or right?

The axis is a weighted disagreement in habits; the question is *which*
habits, and whether they form a linguistically coherent set.

**A1. Loading table (cheap, do first).** For each of the 500 features,
correlate its z-scored rate with axis-1 position across the 127 units
(Spearman, both lenses). Deliverable: the full ranked loading table
(TSV) and a top-50 table for the article. This turns "an average of
disagreements" into a named list.

**A2. Class decomposition (the core experiment).** Hand-classify the
W1-500 list into linguistic classes — (i) particles/indeclinables,
(ii) pronouns/pro-forms, (iii) finite verb forms and auxiliaries,
(iv) converbs/infinitives, (v) case-form vocabulary of narration
(uvāca, abravīt, dṛṣṭvā...), (vi) content lexemes. (The
`sanskrit_indeclinables` list in materials/feature_sets/ is a starting
point for (i).) For C3-500, classify trigrams mechanically: word-final
sequences (inflectional endings), word-initial, cross-junction, interior.
Then run the axis (a) on each class alone and (b) with each class removed,
refilled — the `exclusion_test.py` harness generalizes directly. Deliverable:
a ρ-vs-baseline matrix answering *which class suffices* and *which class is
necessary*. If particles alone reproduce the axis at ρ ≥ 0.95, the axis is a
particle-habit gradient and the article can say so; if no single class
suffices, the axis is distributed usage change — also a finding.

**A3. Minimal sufficient set.** Greedy forward selection: how few features
reproduce the axis at ρ ≥ 0.95? If the answer is ~20, print them in the
article — the reader can check them against their own philological
intuitions. (Guard against overfitting: select on a random half of the
units, evaluate ρ on the other half.)

**A4. Link the top drifters to known diachrony.** Take the top ~30 loading
features and check each against documented diachronic tendencies of epic vs
classical vs late usage (Oberlies' epic-Sanskrit grammar, Meenakshi's epic
syntax; e.g. narrative sma/ha/vai receding, tu/eva/tathā pāda-filler
economy, converb preferences, the spread of relative-correlative frames).
Deliverable: a table "feature — direction on the axis — independently
documented drift". Every row where the two agree is external, non-circular
evidence for Q2's answer; rows that disagree are honest anomalies to print.
For C3: long-compound junction density as a proxy for the known growth of
compound length; final-anusvāra/visarga treatment as edition-dependent
(flag, don't interpret — sandhi conventions are editorial, not authorial).

**A5. Per-text anatomy of extremes.** For a handful of texts whose position
the article discusses (closing-parvans block, PPL I, old SP, BhP, Śivadharma
pair), decompose their axis-1 displacement into per-feature contributions
(the Delta summands projected on the axis). Deliverable: "why *this* text
sits *there*", stated in words a philologist can verify by reading a page.

---

## Q2 — Why does linguistic drift appear in the MDS?

Two sub-questions, kept apart: (a) why does *a dominant gradient* emerge as
axis 1, mathematically; (b) why is that gradient *time-like*, historically.

**B1. Variance anatomy (cheap).** Eigenvalue spectrum of the classical MDS
for both lenses: how much of the squared-distance variance axis 1 carries,
the gap to axis 2, and the stability of axis 1 under unit deletion
(jackknife over the 127 units: drop one, realign, ρ). Establishes that
axis 1 is not an artifact of a few leverage points (the Śivadharma pair and
the śāstra outgroup are the suspects to check).

**B2. Null and generative models (the argument's spine).** Three synthetic
corpora, same n and unit sizes, features multinomial:
  1. **Exchangeable null**: all units drawn from one shared rate vector →
     MDS should show no dominant axis (eigenvalue spectrum flat-ish). This
     calibrates what "no structure" looks like.
  2. **Random heterogeneity**: each unit gets its own rates, drawn i.i.d.
     around the corpus mean with the empirically observed per-feature
     between-text variance, but with *no covariance structure* → axis 1
     exists but explains little, and no ordering is recoverable.
  3. **Drift process**: rates evolve as a slow random walk along a latent
     order (fitted to the observed per-feature variance), units sampled
     along it → MDS axis 1 recovers the generation order (measure ρ).
  The point for the article: a dominant, ordering-shaped first axis is the
  *signature of autocorrelated change* — many small habits shifting
  together — and is not produced by mere heterogeneity. That is what
  "linguistic drift appears in the MDS" means mechanically.

**B2b. The loss/gain decomposition (Kengo's hypothesis).** Hypothesis
(2026-08-14): drift appears because a language starts with a set of
features which randomly *disappear* over time while new features randomly
*emerge*; since a disappeared feature is unlikely to re-emerge (the Dollo
asymmetry), chronology is effectively the fraction of original features
lost, and emergences can be ignored for dating. Nearest named relatives:
**Dollo's law** / the **stochastic Dollo** birth-death model of language
phylogenetics (Nicholls & Gray), and **glottochronology** (Swadesh:
date = retention rate of an original inventory) — our version applies the
idea to style features rather than cognates.

Test: define the "original feature set" empirically (features
characteristic of the epic pole / oldest stratum, selected on a split half
to avoid circularity), then decompose each text's axis-1 displacement into
a **loss component** (depletion of original features) and a **gain
component** (acquisition of late-pole features). Predictions if the
hypothesis holds: (i) the loss component alone reproduces the ordering
(ρ ≥ ~0.9); (ii) the gain component orders the late texts only loosely.
Known complications to report either way: our features are frequencies,
not presence/absence, and some move *up* early (tu/eva/tathā/vai peak in
the old purāṇic core, not the epics) — the pure-loss model needs the
weaker, defensible form "**losses are the clock; gains are the community
structure**"; and the late pole's coherence (sectarian digests resembling
one another) already shows emergences are shared innovations, not
per-text randomness. If (i) holds, Q2(b) gets a genuinely explanatory
answer: the drift axis works because it is, in effect, a retention
measure. Article citation trail: Swadesh; Dollo characters; Nicholls &
Gray 2008; Gray & Atkinson-style applications.

**B3. Convergent orderings.** Compare MDS axis 1 with orderings that make
different assumptions: spectral seriation of the Delta matrix (Fiedler
vector), 1-D isomap, and a TSP/Hamiltonian-path seriation. If all produce
the same order (ρ ≥ 0.95), the gradient is a property of the distance
structure, not of MDS. (This also preempts a methods referee.)

**B4. The time-likeness argument (assembly, not new computation).** Why
believe the gradient is *temporal* rather than some other one-dimensional
habit contrast? Assemble the existing evidence in one place, ordered by
strength: (i) layers of known relative order are correctly ordered — every
CE-excluded accretion later than its host (E1), PPL stratum inside Vāyu/Bḍ
with the constituted PPL, SP's pāśupata block late inside an early text;
(ii) the axis survives every non-temporal explanation actually tested
(length D1/D4, genre pull bounded, filler density refuted, names/sectarian
vocabulary struck at ρ 0.99, reuse removal, MFW and metric sweeps);
(iii) A4's external agreement with independently documented diachrony
(once run — this is the piece that closes the circle non-circularly);
(iv) anchor texts with external date evidence (old SP's early Nepalese
transmission; Śivadharma's external dating; the epics' relative-antiquity
consensus) sit where the temporal reading predicts. State the honest limit:
the axis orders *language states*, and language age ≠ book age
(transmission can preserve or level) — the closing-parvans wording already
has this right. Keep the BhP out of the anchor list: its date is a question
the axis poses, not an anchor.

**B5. The arch check (bridges to Q3).** Classical MDS on a corpus with one
strong gradient is known to bend the gradient into axis 2 (the
Guttman/horseshoe effect; cf. correspondence-analysis seriation practice).
Fit y ~ quadratic(x) across the 127 units, both lenses. The R² of that fit
is the fraction of the y-axis that is *the x-axis folded over* — it must be
measured before interpreting y at all.

---

## Q3 — What exactly is in the y-axis?

Treat y as a residual object: first remove what is mechanically explained,
then see what human-meaningful structure survives.

**C1. Arch removal.** From B5: detrended y (residual of the quadratic fit)
is the candidate "real" second dimension. All subsequent steps run on both
raw y and detrended y.

**C2. Cross-lens agreement (the decisive filter).** The two lenses agree on
x at ρ ≈ 0.89. Compute ρ(y_W1, y_C3) — aligned by Procrustes as usual — for
raw and detrended y. Three regimes: agree strongly → y is a real property
of the texts, worth naming; agree weakly → y is partly lens-specific;
agree not at all → each lens's y is its own noise/artifact dimension and
the article should say y carries no shared signal beyond the arch.
(The MFW sweep already hints C3's y is the theme-absorbing, MFW-sensitive
dimension — ρ_y vs 5000 as low as 0.40 below 3000 MFW.)

**C3. Loadings and covariates for y.** Same loading table as A1 but for
axis 2. Then correlate y with codeable covariates, in order of prior
plausibility:
  - **sectarian/thematic register**: strata coding (Śaiva vs Vaiṣṇava vs
    goddess material), rate of theonym-family vocabulary (the exclusion
    lists from `exclusion_test.py` give this for free);
  - **the Bhāgavata direction**: the deck's vertical convention is
    anchored on BhP-low — what covaries with BhP-ward y? (its known
    peculiar register; state without a date directional);
  - **discourse form**: direct-speech density (uvāca/āha frequency),
    vocative density, imperative/optative share — narrative-dialogic vs
    prescriptive-expository;
  - **meter mix** where feasible: anuṣṭubh vs triṣṭubh share (the long
    epic upajāti passages are register islands);
  - **unit length and edition family**: the boring confounds, checked
    last but reported (C3-y especially: sandhi/orthography conventions
    are editorial and may stratify by source edition — treat any such
    signal as edition noise, not authorial style).
  Deliverable: an R²/ρ table "what y correlates with", both lenses.

**C4. Within-family y.** For families with many units (MBh parvans, Rām
kāṇḍas, ŚiP saṃhitās, BhP skandhas), examine y spread with x roughly held:
if y separates saṃhitās by sect/topic inside one transmission, the register
reading is confirmed at fine grain.

**C5. Write-up rule.** Whatever survives C1–C4 gets *named* in the article
("axis 2 is, to the extent the lenses agree, X — plus a known MDS arch and
lens-specific residue"); what does not survive gets *bounded* ("no shared
interpretable content beyond..."). Either outcome is publishable; the
failure mode to avoid is narrating raw y-positions as if they were a second
chronology. They never were: nearness on y without nearness on x means
register kinship, not date.

---

## Order of work and dependencies

1. **A1 + B1 + B5** — one session, all cheap, no new corpora; A1's table
   feeds A2/A4/A5, B5 gates all of Q3.
2. **A2 + A3** — the classification is the only hand-work (Kengo reviews
   the class assignments before anything is computed from them).
3. **C1–C3** — after B5; C2 is the decision point for how much Q3 space
   the article gets.
4. **B2 + B2b + B3** — self-contained methods work; can run any time; B2 is
   the article's methodological centerpiece for Q2(a), B2b for Q2(b) (its
   epic-pole feature set should be defined after A1's loadings exist).
   B3 gains a plain PCA on the z-scored features as a fourth convergent
   ordering — near-equivalent to classical MDS but with directly readable
   loadings; and the methods section states in one sentence why t-SNE/UMAP
   are *not* used (they preserve local neighborhoods and discard the global
   geometry a gradient reading lives in).
5. **A4 + B4** — reading-and-assembly work (grammars, secondary
   literature), best done against A1's finished table; closes Q2(b).
6. **A5 + C4** — polish passes once the above have stabilized.

Rough estimate: items 1–4 are each a focused session with existing
infrastructure; item 5 is Kengo-led with a session assembling tables.

## Article mapping

- Q1 → the "what is being counted, really" section (A2's class answer +
  A3's minimal set + A5's worked examples).
- Q2(a) → methods/robustness section (B1–B3: a gradient axis is the
  signature of correlated drift, and it is not MDS-specific).
- Q2(b) → the argument section (B4's assembled stack, with A4 as the
  non-circular external link).
- Q3 → a short honest section: arch + what the lenses share + what they
  don't; kills the "second chronology" misreading pre-emptively.

## Standing cautions (carried over)

- BhP: never an anchor, never "archaizer" as premise; symmetric wording.
- Closing parvans: block-level claims only; language age ≠ book age.
- Sandhi/orthography: editorial, not authorial — any C3 finding that could
  be edition-driven gets flagged, not interpreted.
- PPL: a corpus reconstruction, not a transmitted title; "earliest layer"
  claims stay layer-specific (the V1 cosmogony counter-case is real).
