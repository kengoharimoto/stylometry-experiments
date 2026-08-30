# Losses are the clock: recovering relative chronology from stylometric drift in the Sanskrit epics and purāṇas

**Status: DRAFT 2026-08-30 — restructured so that the cleaned corpus
(reuse stripped, colophons removed, trigrams on the space-free
sandhied stream, words on de-sandhied text) is the representative
result throughout, per Kengo's call: comparisons against uncleaned
builds are diagnoses of contamination, never robustness tests. Main
moves: reuse-stripping is now corpus construction (§2.2), not a §3
control; the old §7.2 lens-swap material moved into §3.4 (the cleaned
chronology is trigram-led from the start); old §7 is reframed as a
diagnostic section ("what the absorbed text was doing") and the
"precedence" subsection is dissolved; §8 leads with cleaned-build
values. Numbers that still need computing on the cleaned build are
marked `[NR-RECOMPUTE: …]` in place, each slot recording the
superseded with-reuse value; see the manifest below. Earlier
verification history: reframe numbers verified 2026-08-21 against
`figures/noreuse_reframe/unit_ci_*` + `movers_C3.tsv`,
`axis_anatomy/b2_models_*_noreuse_500.tsv`,
`e1_apparatus/e1_apparatus_C3_noreuse_500.tsv`, and
`mds3d/axis3_stats.tsv` + `mds3d/flattened_pairs.tsv`; 2026-08-17: §4
null-model shares, §6 retention correlations, §8 E1/stratigraphy
values against the post-colophon-clean TSVs. Bibliography assembled
and verified 2026-08-29; venue reference style to be applied at
submission.**

**RECOMPUTE MANIFEST — stage 2 inventory done 2026-08-30. FILLED
from existing TSVs (values now in the text): §2.2 corpus stats (126
units = 127 minus vayu_ba, which is shared text by construction;
3,556,172 words; residues 648–344,712, median 15.1k; 18 units below
the 3k floor — from `noreuse_reframe/unit_ci_W1_noreuse.tsv`); §3.1
cross-lens ρ = 0.93 confirmed (0.9267 all 126 units, 0.9284 above
floor, article-frame `unit_ci_*` positions); §4 full null battery
both lenses (`axis_anatomy/b2_models_*_noreuse_500.tsv`: C3 real
8.7% length-clean 0.064, exchangeable 6.9 ± 0.2%, heterogeneity 2.5
± 0.1%, drift 40.9 ± 1.5% at ρ = 0.996; W1 real 12.8%/0.44,
exchangeable 18.5%/0.96; eigen ratio12 C3 1.21, W1 1.31); §6 C3
headline loss 0.864 / gain 0.62
(`b2b_loss_gain_C3_noreuse_500.tsv`); §8 Kirfel bands on cleaned C3
(early 25–32, late 64–94, per-TG values from `unit_ci_C3_noreuse`).

**STILL TO RUN (stage 3), all on the cleaned build:**

1. Fig 1 map pair — plotting only: adapt `fig1_map_pair.py` to
   `mds3d/coords_C3-500ns_noreuse_n126.tsv` +
   `coords_W1-500_noreuse_n126.tsv`.
2. Fig 2 sweep grid — REAL COMPUTE: `mfw_sweep_noreuse/coords_mfw*`
   turn out to be the SPACED C3 variant (0.888 vs the no-space
   article frame; W1 coords match at 0.999). Need a no-space C3
   sweep (250–12,000) on the no-reuse corpus, then the aligned
   cross-lens grid; confirm 500 × 500 as adopted setting and the
   regime boundaries quoted in §3.1.
3. §2.4 lens-disjointness attribution (38%/12%, 61%, 4%) verified on
   the cleaned build.
4. §3.2 distance-measure sweep; single-text / group deletion
   (`b1_jackknife` has no noreuse version); implementation
   replication (verify which build stylo was fed).
5. §3.3 loading census + class decomposition (`a2_decomposition`,
   `loadings_*` have no noreuse versions).
6. §4 multi-method battery (PCA, isomap, Fiedler, TSP); recheck the
   method-dependence claim given the softer eigen-degeneracy.
7. §5 loading tables (C3, and W1 above floor).
8. §6 combined loss+gain value; subpopulation and presence/absence
   variants; W1-above-floor corroboration (`b2b_loss_gain.py` on
   noreuse inputs).
9. §8 layer-projection framing — Kengo's call (see slot in §8).

**Target:** DSH / Journal of Cultural Analytics (per `outline_dh.md`).

---

## Abstract (draft)

Stylometry is most commonly applied to author attribution. We report
an accidental discovery that stylometry can reveal chronology on a
corpus, and the verification it demanded. The Sanskrit epics and
purāṇas — here 126 textual units, 4.5 million words as transmitted
and 3.6 million once the text they share is stripped — grew by
accretion over roughly a millennium, share large amounts of text
verbatim, and reach us through editions whose orthography, word
division, and paratexts are editorial. Many of them are available in
editions prepared with minimal philological care. An exploratory
distance map of this corpus, built with no chronological question in
view, nevertheless produced a dominant first axis that arranged the
texts in an order philologists would recognize. This paper
establishes that the axis is what it appears to be, and why. Taking
the observation seriously demanded, first, a corpus fit to measure:
every pathology of the transmission — verbatim reuse between texts,
editorial word division, scribal paratext, editorial sandhi
practice — is corrected in the construction of the corpus itself,
because a measurement taken through any of them answers for scribes,
editors, or sources rather than composers. On the corpus so cleaned,
two feature systems with almost no linguistic material in common —
word frequencies computed on algorithmically de-sandhied text, and
character trigrams computed on the undivided (not even spaces)
sandhied stream — recover the same one-dimensional ordering of these
texts (Spearman ρ = 0.93, with the trigram lens carrying the
per-unit measurement: on stripped residues our own null-model
diagnostic catches a length artifact in the word lens, and we
report accordingly). The ordering survives removal of proper names
and sectarian vocabulary, is invariant across feature-set sizes and
distance measures, and is reproduced by an independent
implementation. Null models show that a dominant, ordering-shaped,
length-independent first axis of the kind we observe is the signature
of autocorrelated change — many small habits shifting together — and
not of mere heterogeneity. A split-half decomposition explains the
mechanism: depletion of an early-characteristic feature inventory
alone reproduces the ordering (ρ ≈ 0.86 on the carrying lens), while
feature gains order the late texts only loosely. Losses are the
clock; gains have no systems. The corpus as transmitted — with its
absorbed text left in — is retained for one purpose only: comparing
each unit's position on the two builds measures what its borrowed
material had been doing to it, and the drags are philologically
legible — the great compilations had been reading later than their
compilers wrote because of what they absorbed. The instrument
validates on layers of independently known relative order and yields
philologically consequential results, including a resolution of the
axis into register and chronology components. Where its ordering
departs from received chronological opinion, the departures fall at
points where scholars had already recorded reservations — so the
method also serves as an instrument for locating where the problems
of the received chronology lie. We state throughout what the method
measures: the relative age of composition, which is not the same as
the adoptation of the text into books.

---

## 1. Introduction

Computational stylometry earned its credibility on authorship. Given a
disputed document and a closed set of candidates, features as unassuming
as the frequencies of the most common words separate hands with a
reliability that has survived two decades of adversarial testing
[Burrows 2002; Juola 2006; Rybicki & Eder 2011; Evert et al. 2017]. Chronology is the rarer
and harder target. Intra-author stylochronometry — ordering one writer's
works along their lifetime — has a literature but also a warning label:
the signal is weak, genre-entangled, and easily overwhelmed by editorial
noise [Stamou 2008]. Ordering an entire *tradition*, where no author is
available to hold style constant, would seem to compound the problem
past usefulness.

What this paper reports is a discovery, not a thesis. The chronological
axis at its centre was met by accident: an exploratory
multidimensional-scaling map of the Sanskrit epic–purāṇic corpus, built
from most-common-word distances with no chronological hypothesis in
view, produced a dominant first axis that, on inspection, arranged the
units in an order philology would recognize. Nothing in the design asked
for time. The article is what taking that observation seriously
demanded — and the first demand was a corpus fit to measure. The map
on which the accident happened was contaminated in every way this
corpus can contaminate a measurement: its texts carry each other's
words wholesale, its word divisions and sandhi are editorial, its
chapter breaks are punctuated by scribal formulas. Each of those
contaminations is directional, not noise, and each had therefore to be
removed from the corpus before any position on the map could be read
as evidence about composition. The second demand was to establish that
the axis of the cleaned corpus is not an artifact of what remains, and
to find the mechanism that produces it. A rationale is available only
in retrospect — in a tradition that accreted over centuries, if usage
drifts slowly across generations of composers, a *diachronic* signal
may emerge — but we found the axis first and the explanation after.
The corpus that yielded the accident is also a good place to
interrogate it, for reasons both attractive and hostile. Attractive:
it is enormous (our working corpus is 4.5 million words and is a
fraction of the whole), metrically and formulaically constrained (most
of it is śloka verse), and philology has spent a century establishing
islands of *relative* order within it — layers, borrowings, and
datable external witnesses — against which an instrument can be
validated without assuming any absolute date. Hostile: it has no
authors; its texts copy each other on a scale that dwarfs most reuse
problems in the field; and everything a stylometrist would normally
tokenize — word boundaries, sandhi, orthography, and the colophons
interleaved with the text — is in significant measure the work of
editors and scribes rather than composers.

Our contributions are methodological first and philological second. We
show: (i) a **two-lens design** in which two feature systems with almost
unrelated linguistic content—word unigrams on neurally de-sandhied
text, and character trigrams on the undivided sandhied stream—act as
independent witnesses of one ordering (§2–3); (ii) a **cleaning
discipline** adapted to this corpus's specific pathologies — verbatim
reuse, editorial word division, paratextual contamination, editorial
sandhi — in which each contamination is diagnosed, shown to be
directional, and corrected in corpus construction rather than tested
after the fact (§2); (iii) a **null-model calibration** establishing
what kind of process does and does not produce a dominant,
ordering-shaped first axis in a distance embedding — a calibration
that also catches one of our own lenses failing on the cleaned corpus
(§3.4, §4); (iv) a **retention decomposition** that explains *why* the
axis orders the corpus: the depletion of an early-characteristic
feature inventory carries the chronological signal essentially alone
(§6); (v) a **diagnostic use of the contaminated map**: comparing each
unit's position on the cleaned corpus against its position with the
absorbed text left in reads off what that material had been doing to
the measurement — which text was dragged where by what it absorbed —
findings in their own right, not robustness checks (§7); and (vi)
validation against independently known relative order — critical-edition
apparatus known to be later than its constituted text, and source layers
known to be older than their host redactions (§8). Along the way the
corpus pays the method back with findings that bear on live questions in
Sanskrit philology; we state them at the resolution the instrument
supports and no further.

Two disclaimers frame everything that follows. First, the method
orders *language states*, not books. All it can see is the language a
text presents, and that language may be old for two reasons the
corpus cannot tell apart: the text was composed early, or it was
compiled later and faithfully preserved early language. This is a limitatioin in our  measurement, and we will point out how it could affect how we see the chronology in the corpus. Stripping absorbed
text (§2.2) reduces one large form of it — a text no longer answers
for the language of the works it swallowed — but the residue is
transmitted, and paraphrase too loose for the strip to catch
survives; the limit may shrink, but it does not vanish. Second, the first
axis of an embedding is not, a priori, a timeline. The work of
this paper is precisely to earn the step from "the corpus has a
dominant axis" to "that axis is a chronology" — by construction (§3),
by null models (§4), by mechanism (§6), and by external validation
(§8).

## 2. The corpus and the preprocessing it forces

### 2.1 What a stylometrist needs to know about Sanskrit transmission

Classical Sanskrit text is transmitted as a continuous euphonic stream.
*Sandhi*, the obligatory phonological fusion at word junctions, rewrites
word boundaries: *tataḥ* + *uvāca* surfaces as *tata uvāca*, *ca* + *api*
as *cāpi*. Manuscripts compound the difficulty by writing without word
division (*scriptio continua*); the spaces in a printed edition are the
editor's analysis, not the tradition's testimony, and editorial habits
differ by edition, era, and region. Above the letter, the transmitted
stream is punctuated by *colophons* — chapter-closing formulas naming the
work and section — which are paratext added and normalized by scribes,
not composed text. A stylometric pipeline that tokenizes a printed
edition therefore measures three superimposed authorships at once: the
composer's, the scribal tradition's, and the editor's.

The fourth thing the corpus does to a stylometrist operates above the
level of the letter: the texts absorb one another. Whole genealogical
chapters circulate across purāṇas nearly verbatim, and entire works
were swallowed by growing compilations. For a chronological
measurement this reuse is not noise but a directional confound, and it
pulls both ways: early material incorporated into a late compilation
drags the compilation's measured language earlier, while late layers
deposited into an early core drag the core later. A position measured
on the intact transmitted text is therefore the center of mass of a
mixture whose components can lie centuries apart — it answers for a
text's sources as much as for its makers.

None of this is a peculiarity to be normalized away by better
cleaning of the usual kind; it dictates the design. Two responses
structure the paper. First, because any single featurization inherits
one particular mixture of the three hands at the level of the letter,
we build two featurizations that inherit *different* mixtures — and
treat their agreement, not either one alone, as the measurement
(§2.3–2.4). Second, because each contamination is directional, each
is corrected in the construction of the corpus itself: colophons are
removed, word division is discarded where it is editorial, and — the
consequential one — cross-text verbatim reuse is stripped. The corpus
of this paper is the cleaned corpus. A measurement taken with the
absorbed text left in is not a baseline and not a robustness
condition; it is a mismeasurement of composition, and it appears in
this paper exactly once, in §7, where the mismeasurement itself is
the object of study.

### 2.2 Building the corpus

The unit inventory comprises the books of the two epics (Mahābhārata
parvans, Rāmāyaṇa kāṇḍas) plus selected Critical-Edition appendix
blocks as separate units, whole purāṇas or their major divisions, a
small śāstra/ritual outgroup, and the seven text-group units of
Kirfel's constituted *Purāṇapañcalakṣaṇa* reconstruction [Kirfel
1927], included as first-class units because §8's validation turns on
them. The source e-texts derive from the GRETIL archive [GRETIL],
from critical-edition e-text lineages, and from OCR of printed
editions. As transmitted, the inventory holds 127 units totalling
4,490,750 de-sandhied words (unit sizes 1.0k–462k, median 17.3k).

Three corrections turn the inventory into the corpus.

**Colophon removal.** Chapter colophons are scribal paratext with a
directional bias (§2.5 reports the diagnosis: their density varies by
genre and their formulas are late-styled, so they bias colophon-heavy
texts lateward). They are removed corpus-wide with a validated line
filter.

**Reuse stripping.** Cross-text verbatim reuse is removed by shingle
matching with fuzzy extension, in both directions, at a threshold
calibrated against known-unrelated control pairs; the removal itself
is validated by byte-reconstruction. The drop is symmetric — a
parallel is removed from both of its carriers — with one deliberate
exception: Kirfel's constituted *Purāṇapañcalakṣaṇa* is treated as
the one known *source*, its lines removed from the purāṇas but never
from the reconstruction (§8 turns this one-directionality into a
validation design). What survives the strip approximates each text's
own diction: the language its compilers wrote rather than the
language they carried. The cleaned corpus holds 126 units — one unit
of the transmitted inventory, the Vāyu–Brahmāṇḍa common text, *is*
shared text by construction and retains no residue — totalling
3,556,172 de-sandhied words. Stripping is savagely uneven — residues
span 648 to 345,000 words (median 15.1k) — and §3.4 converts that
unevenness into an explicit statement of which lens can carry
per-unit measurements and which units fall below the instrument's
floor.

**Word-division discipline.** For the word lens, sandhi is resolved
algorithmically (below), replacing editorial segmentation with a
uniform one; for the trigram lens, *all* whitespace is stripped,
restoring in effect scriptio continua, so that editorial segmentation
does not enter the feature space at all.

Every representative number and figure in this paper is computed on
the corpus so constructed. Where a with-reuse value is cited (§7), it
is cited as a diagnosis of what the absorbed text was doing, and is
labelled as such.

### 2.3 The two lenses

**W1 (words, de-sandhied).** We resolve sandhi computationally with a
byte-level sequence-to-sequence model (ByT5 [Xue et al. 2022])
fine-tuned for Sanskrit sandhi resolution [Nehrdich et al. 2024], run
offline in int8 quantization over the full corpus. The output is a word-segmented text on which we
count word unigrams and keep the 500 most frequent words (MFW) as
features. We say "most frequent words" and not "function words"
deliberately: in a śloka corpus the top 500 contains, alongside genuine
particles and pronouns, high-frequency content and formulaic vocabulary
(*deva*, *dharma*, *rājan* are all in the top 80), and the analysis in
§5 depends on being honest about that composition.

**C3 (character trigrams, no word division).** From the sandhied text we
strip *all* whitespace and count character trigrams over the
continuous stream, keeping the top 500. Stripping the spaces is a
correction, not a convenience: word division is editorial, and when
we counted trigrams over spaced text, 33% of the top-500 features
contained a space character, importing the editors' segmentation
habits directly into the feature space. Removing them measurably
improved agreement with the word lens at every feature-set size we
tested, and the texts that moved most were precisely those from
editions with distinctive spacing conventions — movement, in seven of
the nine largest cases, *toward* the position the word lens had
assigned them all along: the spaced variant had been mismeasuring
them by their editors' habits. Encoding granularity below the space
level is not a live issue: re-encoding the IAST digraphs (kh, bh,
ai, …) as single phoneme symbols changes the ordering by ρ ≥ 0.99 and
we cite it only as a preempted objection.

Both lenses feed the same instrument: Burrows's Delta [Burrows 2002] on
the 500 z-scored feature rates, classical multidimensional scaling of
the resulting distance matrix, and Procrustes alignment (rotation and
reflection only) of all configurations onto a fixed reference frame so
that coordinates are comparable across runs. For questions about layers
and subsets of texts we never recompute the map on a mutilated corpus;
we project the subset into the fixed map as supplementary points (Gower
projection) and attach confidence intervals by bootstrap over lines
(B = 500).

### 2.4 Why two lenses constitute two witnesses

Agreement between two featurizations of the same text is worthless if
they are two names for the same counts. The value of the W1×C3 design
rests on their near-disjointness, which we verified by attributing every
corpus token of every C3 feature to its source word and classifying both
feature sets with the same rule-based classifier. The two lenses draw
their discriminative signal from different strata of the language:
closed-class vocabulary (particles, pronouns) carries 38% of W1's
axis-correlated signal but only 12% of C3's; 61% of C3's signal lives in
word-*internal* trigrams — inflectional and derivational morphology
inside content words — which W1, by construction, aggregates away. The
particle share of C3's signal (4%) is a ninth of the particle share of
the running text (36.5% of tokens), so C3 is not covertly re-counting
the little words that dominate W1's top ranks. When these two systems
agree on an ordering, they agree from different linguistic evidence; we
use that property as the paper's basic epistemic device.
[NR-RECOMPUTE: attribution shares verified on the cleaned build;
cited values computed pre-strip.]

### 2.5 Three lessons in corpus hygiene, told against ourselves

Three episodes from this project generalize to any stylometric work on
non-Latin-script or editorially mediated corpora, and we report them as
methods results rather than confessions. Each ends the same way: the
uncorrected variant was not a defensible baseline that happened to
need improvement — it was mismeasuring, directionally, and the
correction defines the corpus.

**Tokenization silently mutilated by locale assumptions.** R stylo
0.7.5 [Eder, Rybicki & Kestemont 2016] with `corpus.lang =
"English.all"` treats the Latin Extended
Additional block (U+1E00–U+1EFF: ṣ, ṭ, ḍ, ṇ, ḥ, ṃ, ṛ) as word
separators while passing Latin Extended-A (ā, ī, ś) — so every IAST
token containing a retroflex or visarga was split into fragments
(*guṇa* → *gu|a*, *lakṣmī* → *lak|mī*), and the emitted "most frequent
words" included bare fragments. We caught it by re-implementing the
suspected splitting rule and correlating the resulting distance table
against stylo's (r = 0.999999 against the buggy rule; r ≈ 0.94 against
correct tokenization — the discrepancy *is* the diagnosis). The fix is
one line (`splitting.rule = "[[:space:]]+"`); the lesson is not. Verify
the tokenizer's actual behavior on your script's full codepoint range,
and treat "the headline survived the bug" — ours did — as luck, not
vindication.

**A preprocessing inconsistency detected by metric disagreement.** One
text (the Nīlamatapurāṇa) arrived with sandhi editorially dissolved:
~19% of its word boundaries carried pausa forms against a corpus norm
of ~2.5%. In raw-cosine MDS on character trigrams it was a spectacular
outlier (nearest-neighbour distance 12.8× the corpus median); under
Delta it sat normally (1.5–1.9×), because z-scoring subtracts the
shared Zipfian head where orthographic convention lives. The divergence
converts an embarrassment into an instrument: *disagreement between
standardized and unstandardized metrics over a single text is a
preprocessing-inconsistency detector*.

**Paratext with a directional bias.** Chapter colophons are only 0.9% of
corpus words, but they are not noise: their density varies by genre
(purāṇas have many short chapters) and their formulas are late-styled,
so they bias colophon-heavy texts *lateward*. Across affected units the
correlation between colophon fraction and position shift on removal was
−0.58, with single-unit shifts up to 15 percentiles. That is not a
perturbation to be survived; it is a systematic error in a diachronic
measurement, and the corpus is defined with it removed (§2.2). The
correction also behaved as a correction should: after removal the two
lenses agreed better than before it. The general point: paratext is
not random clutter — it is systematically distributed, and in a
diachronic analysis systematically distributed means directionally
biasing.

## 3. The ordering and its robustness

### 3.1 The convergence result

At the adopted settings — 500 MFW for W1, 500 space-free trigrams for
C3 — the first MDS axes of the two lenses agree across the cleaned
corpus at Spearman ρ = **0.93** (Figures 1 and 2). The trigram lens
carries the per-unit measurement and the word lens corroborates the
ordering; §3.4 derives that division of labor from the instrument's
own diagnostics rather than asserting it.

**Figure 1.** The two maps, side by side (cleaned build; classical
MDS of Burrows's Delta; equal aspect): (a) C3-500, character trigrams
on the undivided sandhied stream; (b) W1-500, word unigrams on
algorithmically de-sandhied text. The horizontal axis is the drift
axis (axis-1 agreement ρ = 0.93); colors are text groups, codes in
the supplementary key. *[NR-RECOMPUTE: rebuild
`figures/fig1_map_pair/` on the cleaned build via `fig1_map_pair.py`
from no-reuse article-frame coords; current file is the with-reuse
pair.]*

A full grid sweep locates the agreement ridge at moderate feature
counts on both sides. [NR-RECOMPUTE: sweep grid on the cleaned build
(with-reuse grid ran W1 30–5000 MFW × C3 250–12,000 and peaked at
500 × 500, ρ = 0.953); confirm the ridge location and the adopted
setting. Known already from cross-build spot checks: the cleaned
build's W1 plateau narrows mechanically — stripping shrinks token
counts, exhausting the shared word inventory at lower ranks.] The
adopted setting is the peak of measured cross-lens agreement, not a
tuned free parameter.

The sweep's two failure regimes are as informative as its plateau. W1
holds through the low hundreds of MFW and then collapses as the
feature list leaves the shared vocabulary and fills with
text-specific content words: the axis becomes a topic model and stops
ordering. C3, by contrast, is nearly invariant across an
order-of-magnitude range of feature counts: sub-lexical features
saturate the shared inventory early, and added features long add
resolution, not topics — even C3's eventual degradation is a gentle
slope where W1's is a cliff. [NR-RECOMPUTE: regime boundaries on the
cleaned build; with-reuse values were W1 stable 80–1500 (ρ ≥ 0.93),
0.51 at 3000, 0.14 at 5000; C3 ρ ≥ 0.95 from 250 to 8,000, easing to
0.83 at 12,000.] The asymmetry matters for practice: with sub-lexical
features the feature-count knob is forgiving; with word features it
is the difference between measuring usage and measuring subject
matter.

**Figure 2.** Cross-lens agreement across the joint sweep: Spearman ρ
between the W1 axis at each feature count (rows) and the no-space C3
axis at each (columns), cleaned build. *[NR-RECOMPUTE: regenerate
`figures/fig2_convergence/` on the cleaned build; current grid is
with-reuse.]*

### 3.2 What the ordering does not depend on

**Distance measure.** Every standardization-based measure we tested
(classic, Argamon's rotated, Eder's, and Würzburg cosine Delta) and the
L1-family measures (Manhattan, Canberra, min-max) reproduce the axis
at the adopted settings; only unstandardized cosine and Euclidean
distance blur it, for the textbook reason: without z-scoring, the
Zipfian head dominates and the discriminative mid-ranks are drowned.
[NR-RECOMPUTE: metric sweep on the cleaned build; with-reuse values
were ρ = 0.95–1.00 within the standardized family, 0.81–0.91 for
unstandardized.] One caution from the metric sweep deserves wider
currency: the apparent robustness of unstandardized metrics to
feature-set size (ρ = 0.99 across settings) is *robustness by
deafness* — added features carry negligible weight, so nothing
changes because nothing is heard. Within the Delta family,
interchangeability is expected [Evert et al. 2017] and we count it as a
consistency check, not independent confirmation.

**Names and sectarian vocabulary.** Striking all 38 theonyms and
divine-name stems that reach the W1-500 list (refilling to 500 from
the frequency ranking) leaves the ordering at ρ = 0.9984 against
baseline; striking 70 names plus ritual and sectarian lexemes leaves
0.9952. A trigram-level analogue strikes every trigram that occurs
inside any listed lexeme — deliberately over-broad, removing 105–160
of C3's 500 features including generic strings that merely occur
inside a name — and leaves 0.9836 and 0.9798. The ordering is not a
disguised sectarian sorting.

**Implementation.** The full C3 pipeline — feature list, frequency
table, Delta distance matrix, and map — is reproduced exactly by an
independent implementation (stylo 0.7.5 in R): 500/500 identical
features, distance-matrix correlation 1.0000, map correlation 1.0000.
We mention this not as ceremony but because §2.5's tokenization
episode shows exactly how much an "independent implementation" can
silently fail to be one; the replication was run with the tokenizer
verified. [NR-RECOMPUTE: verify which build the replication was fed;
re-run on the cleaned build if needed.]

**Single texts.** Deleting any one unit (with feature refill and
recomputation) leaves the axis essentially unchanged, as does
deleting the two highest-leverage groups a referee would nominate —
the śāstra outgroup and a late two-text pair that anchors the far
end. No small set of texts carries the axis. [NR-RECOMPUTE:
leave-one-out and group-deletion on the cleaned build; with-reuse
values were ρ ≥ 0.98 and ρ ≥ 0.99.]

### 3.3 What the ordering is made of

The axis is not a few-feature artifact: only a handful of the 500
features on either lens correlate with it strongly, and the median
per-feature correlation is modest. [NR-RECOMPUTE: loading census on
the cleaned build; with-reuse values were 4/500 (W1) and 8/500 (C3)
at |ρ| ≥ 0.7, medians 0.28 and 0.23.]
A class decomposition — computing the axis from each linguistic class
alone, and with each class removed and refilled — shows that *no class
is necessary and nearly every class suffices*: particles alone
reproduce the ordering, content words alone reproduce it,
word-interior trigrams alone reproduce it best of all, and every
single-class removal leaves the axis essentially intact. The one
genuine exception is boundary phonology: junction-spanning and
word-final trigrams alone fail — sandhi texture, the most
edition-sensitive stratum, is precisely where the ordering is *not*.
[NR-RECOMPUTE: class decomposition on the cleaned build; with-reuse
values were particles 0.89, content words 0.94, word-interior
trigrams 0.97, removals ρ ≥ 0.94, boundary trigrams 0.11–0.14.] We
defer the full anatomy and its linguistic reading to §5, but the
redundancy result belongs here, among the robustness facts: an axis
that survives the removal of any feature class it is accused of
depending on is not that class's artifact.

One negative deserves emphasis because it reframes an expectation a
Sanskritist reader may bring. The features that grammars of epic
Sanskrit document — the marked deviations from the classical standard —
are almost entirely absent from the top of the loading table. This is
structural, not accidental: the drifters are ordinary words at shifting
rates, and a grammar of deviations is blind to rates of unmarked
vocabulary by construction [Oberlies 2003]. The axis lives in the
unconscious frequency band — which is also the band a conscious
archaizer cannot easily target. External validation of the axis's
temporal reading therefore cannot come from grammar-checking the
feature list; it comes from known relative order and dated anchors
(§8).

### 3.4 The honest boundary: unit length, and which lens carries the map

Length is the one failure mode the two lenses *share*, so their
agreement — the paper's central device — offers no protection against
it, and it must be bounded directly. Window-resampling experiments
(contiguous windows of 1k–10k words drawn from long texts) show the two
lenses failing in different but equally disqualifying ways below a few
thousand words — a floor consistent with what attribution studies
report for small samples [Eder 2015]: W1 positions keep a stable mean
but explode in variance
(single 1k windows of one mid-corpus text span half the axis); C3
positions drift systematically with window size. We therefore treat
every unit below ~3,000 words as an *uncertainty region* — its
individual position is not evidence — and make claims about short texts
only at the level of merged blocks large enough to clear the floor,
with bootstrap confidence intervals. §7's and §8's cases inherit this
discipline; no headline claim in this paper rests on the individual
position of a short unit.

On the cleaned corpus the floor does real work, because reuse
stripping is savagely uneven: residues span 648 to 345,000 words.
Before reading the maps we ran §4's null battery on the cleaned
build, and the length diagnostic earned its keep against our own
instrument. On samples this small the word lens's exchangeable null
produces a *stronger* first axis than the real corpus's own (18.5 ±
0.4% variance share at ρ = 0.96 against log length, versus the real
W1 axis's 12.8% at ρ = 0.44): on residues, W1's first axis is partly
a length artifact, and we do not cite its per-unit positions. The
trigram lens is immune for a mechanical reason — even a small residue
supplies hundreds of thousands of trigram events, so its exchangeable
null stays weak (6.9% share) and its real axis stays length-clean
(ρ = 0.064). The representative chronology of this paper is therefore
**trigram-led**: C3 supplies the per-unit numbers; W1 corroborates
the ordering (ρ = 0.93, §3.1) and, above the floor, the directions of
individual contrasts. The lesson is portable: whichever lens has the
smaller event count per unit inherits the small-sample regime, and a
length diagnostic must sit beside every variance-share claim (§4).

Eighteen of the 126 residues fall below the floor — the extreme case
is treated in §7: for some old-core carriers almost nothing survives
the strip. They are greyed out on the maps and read as
direction-only, or not at all. The corpus's length imbalance is thus not normalized away but
converted into an explicit resolution limit of the instrument.

## 4. Why a drift axis emerges: null and generative models

Everything in §3 shows that the cleaned corpus *has* a dominant,
robust first axis. Nothing in §3 says what kind of process produces
one. This section calibrates that question with three synthetic
corpora, each matched to the real one in unit count, unit sizes, and
feature inventory, with features drawn multinomially (10 replicates
each; both lenses, C3 — the carrying lens — reported here, W1
mirroring above the length floor).

**Null 1: exchangeable.** All units sample from one shared rate vector —
no heterogeneity at all. Its first MDS axis nonetheless carries 6.9 ±
0.2% of the squared-distance variance, not far below the real C3
axis's 8.7%. The resemblance is a trap, and diagnosing it is the
section's first methodological point: the null's axis is a **length
artifact** (smaller samples deviate more in every feature, and Delta
geometry arranges units by sampling noise magnitude — on the word
lens's far smaller per-unit event counts the same null's share
reaches 18.5 ± 0.4% at ρ = 0.96 against log length). The real C3
axis is length-independent (ρ = 0.064 against log length); the
null's is not. *First-axis variance share is uninterpretable without
a length diagnostic beside it*; we suggest this pairing as standard
practice for any MDS/PCA-based claim about corpus structure — §3.4
is what it caught in our own instrument.

**Null 2: heterogeneity without covariance.** Each unit receives its own
rate vector, drawn i.i.d. around the corpus mean with the empirically
observed per-feature between-text variance — as much per-text
distinctiveness as the real corpus, but uncorrelated across features.
The dominant axis collapses: 2.5 ± 0.1% variance share. Mere
distinctiveness, however strong, does not make a gradient.

**Generative model: drift.** Feature rates evolve as a slow random walk
along a latent order (step variance fitted to the observed between-text
variance), and units sample from their position's rates. Now the first
axis carries 40.9 ± 1.5% and — the decisive property — recovers the
latent generation order at ρ = 0.996 ± 0.002 (W1: 0.974 ± 0.010),
length-clean. A dominant, ordering-shaped, length-independent first
axis is the *signature of autocorrelated change*: many features
shifting together along an underlying progression. The real corpus's
8.7% sits between the heterogeneity floor and the pure-drift
ceiling, which is what a real tradition should do — its variance
budget is shared among drift, register, genre, and idiosyncrasy; §9
locates the two largest non-drift components.

**The axis is a property of the distances, not of MDS.** Four methods
with different assumptions — PCA on the z-scored features (no distance
matrix, no double-centering, L2 where Delta is L1), 1-D isomap
(geodesics), spectral seriation (Fiedler vector), and a
Hamiltonian-path/TSP seriation — were run on both lenses. Every global
embedding finds the drift gradient in its top-2 plane. On C3 the
*raw* first dimensions disagree across methods, and the reason is
itself a result: C3's top two eigenvalues are close (ratio 1.21, vs
1.31 on W1), because the register dimension (§9) is strong relative
to the drift dimension — so which one surfaces first can be
method-dependent while the plane containing both is not. The TSP
seriation fails on both lenses, and its failure is independent
evidence: path seriation tracks a gradient only when the data are
effectively one-dimensional, so its snake-folding here confirms a
genuine second dimension before §9 measures one. We do not use t-SNE
or UMAP anywhere: they preserve local neighborhoods and discard
exactly the global geometry a gradient reading lives in.
[NR-RECOMPUTE: multi-method battery (PCA/isomap/Fiedler/TSP) on the
cleaned build; with-reuse values were PCA 0.997/0.995, isomap
0.92/0.85, Fiedler 0.95/0.82, TSP 0.24–0.29. Eigenvalue ratios above
are cleaned-build values from `b2_models_*_noreuse_500.tsv`; note the
near-degeneracy story is softer than with-reuse (1.07 vs 1.68) —
recheck the method-dependence claim when the battery runs.]

## 5. What the axis counts

The loading tables put linguistic flesh on the statistical skeleton.
On W1, the pole that anchors the early end is the machinery of
narrated dialogue: anaphoric pronoun chains (*tam*, *sa*), narrative
preterites (*abravīt*, *āsīt*, *jagāma*), speech-sequencing converbs
(*śrutvā*, *uktvā*), the simile particle *iva*, and the second-person
apparatus of face-to-face address (*tvām*, *tava*, vocative *rājan*).
The late pole is the machinery of exposition: itemizing *-ādi* (the
strongest single loading in either lens), *jñāna/jñānam*, *brahma*,
sentence-connective *tad*, and — in C3 — the optative endings of
prescription (*-yet*, *-yāt*) and the taddhita derivative suffixes of
technical vocabulary (*-ikā/-ika*). Both lenses, read blind, describe
the same drift: from narrated encounter toward enumerated doctrine.
Whether that gradient is *temporal* is not settled by naming it; that
burden falls on §6 and §8. [NR-RECOMPUTE: loading tables on the
cleaned build (C3, and W1 above the length floor); the per-feature
correlations quoted in earlier drafts (*tam* −0.78, *sa* −0.70,
*abravīt* −0.68, *āsīt* −0.59, *jagāma* −0.63, *śrutvā* −0.65,
*uktvā* −0.62, *iva* −0.62, *-ādi* +0.79, *tad* +0.60, *-yet* +0.71,
*-yāt* +0.66, *-ikā/-ika* +0.77/+0.56) are with-reuse values;
restore exact figures from the cleaned-build tables and confirm the
pole memberships.]

Three structural facts sharpen the picture. First, the signal is
radically distributed (§3.3): the poles just quoted are the readable tip
of five hundred small correlations, not a shortlist that carries the
axis. Second, the two lenses reach their agreement from different
structural levels of the language — W1 from whole-word habits of every
class, C3 predominantly from word-internal morphology (§2.4) — so the
register reading is corroborated across levels, not repeated. Third, the
class decomposition's one strong negative localizes what the axis is
*not*: boundary phonology alone (junction and word-final trigrams)
retains almost nothing of the ordering. The stratum
most exposed to scribal and editorial sandhi practice is the stratum
the chronology is not written in — a fortunate asymmetry, since it is
also the stratum we can least trust our editions to transmit.

A note on classifier dependence: the class decomposition requires
assigning 500 words to classes, and some assignments are arguable
(*tad*, *punar*, *svayam*, …). Flipping all twelve borderline
assignments at once changes no decomposition correlation by more than
0.031; the conclusions are insensitive to the hand that classified.

## 6. Losses are the clock

The null models say the axis behaves like autocorrelated change; this
section asks what kind. The hypothesis — motivated by glottochronology's
retention logic [Swadesh 1955] and by the asymmetry of loss in Dollo
characters [Nicholls & Gray 2008] — is that a tradition's usage
inventory depletes quasi-irreversibly: habits fall out of use and do not
return, while new habits arrive in community-specific bursts. If so, the
fraction of an *early-characteristic* inventory a text retains should be
a clock, and its acquisitions should tell us about affiliation more than
age.

The test must not let the axis pick its own evidence. We split every
unit into alternating 16-token blocks, forming two half-corpora. On half
A only, we selected features characteristic of the epic pole and of
the late pole (rate-ratio criterion, threshold ≥ 1.5 and its
inverse). On half B only — text the selection never saw — we scored
each unit's **loss component** (depletion of the early-typical
inventory) and **gain component** (acquisition of the late-typical
inventory), and compared each to the drift axis.

On the carrying lens of the cleaned build, the loss component alone
reproduces the ordering at ρ = **0.864** at the adopted threshold
(0.856–0.868 invariantly across feature-selection thresholds), while
the gain component reaches only 0.62 (0.60–0.69); adding gains to
losses improves the ordering marginally at best. The clock is
carried by what texts *stop doing*. [NR-RECOMPUTE: combined
loss+gain value at the adopted threshold; corroborate on W1 above
the length floor (the earlier with-reuse W1 headline was loss 0.939,
gains 0.720, combined 0.951, from 81 early and 65 late features).] The asymmetry deepens inside
subpopulations, where the easy epic-versus-late contrast is
unavailable: within the late block alone, and within all non-epic
units, losses continue to order while gains fall away.
[NR-RECOMPUTE: subpopulation values on the cleaned build; with-reuse
W1 values were 0.941 vs 0.683 (late block) and 0.891 vs 0.571
(non-epic).] And a strict presence/absence variant — scoring only
whether features occur at all, the literal Dollo reading —
collapses: the early inventory does not *vanish* from late texts, it
*dwindles*. [NR-RECOMPUTE: presence/absence variant on the cleaned
build; with-reuse value was 0.474.] The defensible form of the
hypothesis is therefore not Dollo's law transplanted, but Swadesh's
retention rate generalized from a cognate list to the frequency
spectrum of style: **losses are the clock; gains are the community
structure.** The gains side is not noise — late texts share their
acquisitions, which is precisely why the gain component tracks
affiliation (§9 finds the same structure from another direction) —
but it is the wrong hand for telling time.

This decomposition upgrades the paper's claim from correlation to
mechanism. The drift axis works as a chronometer *because* it is, in
effect, a retention measure computed over five hundred features at
once; and it predicts where the method should transfer: any long
tradition whose composition is continuous and whose feature inventory
depletes faster than it recycles — legal formulae, liturgical corpora,
scholastic commentary chains — is a candidate.

## 7. What the absorbed text was doing: the transmitted map as diagnostic

### 7.1 The one measurement the transmitted corpus supports

Everything so far was computed on the cleaned corpus, because a
position measured with the absorbed text left in mismeasures
composition (§2.1): a purāṇa as transmitted is a mixture — the
compilers' own composition plus everything the tradition deposited
into it, inherited cores, migrating māhātmyas, wholesale
incorporations of other works — and its measured position is the
center of mass of that mixture, dragged toward wherever each
*source's* language sits. This section is the one place the
transmitted build appears, and it appears as a diagnostic object, not
as a chronology: comparing each unit's position across the two builds
measures what its absorbed material had been doing to it, and the
drags are findings about the texts.

The comparison also closes the loop on the paper's origin. Globally
the two builds order the corpus almost identically — Spearman
ρ = 0.982 on the trigram lens (0.908 on the word lens, which §3.4's
artifact degrades) — which is why the accidental discovery, made on
the contaminated corpus, pointed true: contamination that drags
different texts in different directions largely cancels at the global
scale even as it falsifies individual positions. The same comparison,
pushed past W1's feature cliff, shows what the cliff regime was
measuring all along: at 5000 MFW the orderings of the two builds
*anti-correlate* (−0.86) — beyond the cliff, the word lens measures
the shared material itself, so removing that material inverts it.
Global agreement is not the point of the comparison, and we do not
offer it as reassurance; the point is the sixteen units it conceals.

### 7.2 What the drags mean

Sixteen units differ between the builds with non-overlapping
bootstrap intervals (Table 1). We tabulate each unit's composition
position (cleaned build), the position the transmitted text had been
producing, and the **drag** — transmitted minus composition, so that
a positive drag means the absorbed material had been pulling the
text's apparent position lateward. The moves sort into three legible
classes.

**Table 1.** Every CI-separated drag, plus the one grazing case,
sorted by drag. Percentile positions on the C3-500 maps with 95%
line-bootstrap confidence intervals (B = 500). \* intervals graze
rather than separate (overlap 0.4 of a percentile); † sub-3k-word
residue — direction only, the composition position is below the
length floor (§3.4).

| text | composition (cleaned) | as transmitted | drag |
|---|---|---|---|
| Brahmāṇḍapurāṇa | 44 [40, 47] | 63 [60, 64] | +19 |
| Brahmāṇḍa, khaṇḍa 2 | 28 [26, 34] | 40 [36, 40] | +12 |
| Śivapurāṇa, Dharmasaṃhitā\* | 43 [40, 49] | 53 [48, 59] | +10 |
| MBh 13, App. 15 (Umāmaheśvara) | 72 [69, 74] | 80 [78, 82] | +8 |
| Mārkaṇḍeya, adhy. 1–80 | 36 [34, 37] | 43 [40, 48] | +7 |
| Mārkaṇḍeyapurāṇa | 32 [28, 35] | 38 [36, 40] | +6 |
| PPL, Textgruppe IIB | 88 [83, 90] | 94 [90, 96] | +6 |
| Padmapurāṇa | 44 [40, 46] | 48 [47, 48] | +4 |
| Bhaviṣyapurāṇa | 61 [58, 63] | 64 [64, 67] | +4 |
| Kūrma, khaṇḍa 2 | 87 [82, 90] | 90 [90, 93] | +3 |
| MBh 12, Śāntiparvan | 36 [34, 37] | 38 [37, 40] | +2 |
| Rām 6, Yuddhakāṇḍa | 10 [10, 11] | 8 [7, 10] | −2 |
| Śivapurāṇa, Umāsaṃhitā | 72 [68, 76] | 63 [58, 65] | −9 |
| Vāyupurāṇa | 81 [78, 85] | 71 [68, 76] | −9 |
| Vāyu, kalpas & Śiva lineages | 82 [78, 92] | 71 [62, 75] | −11 |
| Vāyu, manu-vaṃśa section† | 46 [33, 72] | 30 [27, 32] | −16 |
| Viṣṇupurāṇa, aṃśa 5† | 39 [34, 61] | 21 [18, 23] | −19 |

**The great compilations had been reading late.** The largest drags of
well-measured texts are positive: the Brahmāṇḍapurāṇa's transmitted
text had been reading at the 63rd percentile against a composition
position of 44, its second khaṇḍa +12, the Śivapurāṇa's Dharmasaṃhitā
+10 (the grazing case of Table 1), the Mārkaṇḍeya +6, and — smaller
but CI-clean — the two giant compilations, Padma (+4) and Bhaviṣya
(+4). What these texts absorbed sits, on average, *later* than what
their compilers wrote, and it had been answering for them. The
Śivadharma corpus makes the mechanism concrete: the Śivadharmaśāstra
and Śivadharmottara sit at the far late pole (percentiles 91–95), and
the texts that absorbed them wholesale — the Bhaviṣya incorporates
roughly a quarter of each; the Padma, the Dharmasaṃhitā, and the
Revākhaṇḍa large shares — all carried positive drags (the first three
CI-clean or grazing in Table 1; the Revākhaṇḍa's +3 stays within its
intervals): their borrowed skin had been reading in their place.
Symmetrically, a few drags are negative (the Vāyu −9; its third
section −11; the Śivapurāṇa's Umāsaṃhitā −9): what *they* carried was
older than their own hand, and had been making them look earlier
than their compilers wrote.

**The old-core carriers dissolve.** The sections of the Vāyu and the
Viṣṇu aṃśas that carry the shared genealogical inheritance retain almost
nothing under the strip — the Vāyu's manu-vaṃśa section keeps 1,064 of
20,373 words — and drop below the §3.4 length floor: their composition
positions are simply not measurable, and we grey them out rather than
read them. That emptiness is a measurement, not a failure: for these
texts, the transmitted text *is* mostly the shared inheritance, which is
Kirfel's century-old thesis [Kirfel 1927] restated as a retention
statistic.

**Pseudo-neighborhoods fall away.** On the transmitted build, the
Viṣṇupurāṇa's nearest neighbors are its own copyists — texts that
absorbed it. On the cleaned build those neighbors recede, and on its
own diction the Viṣṇu sits as close to the Bhāgavata as to anything
else. The two texts treat the same narrative material with almost no
shared wording (under the symmetric strip, the Viṣṇu's Kṛṣṇa book
loses 80% of its words to parallels elsewhere; the Bhāgavata's,
treating the same story, loses 6%) — two independent tellings, no
copying in either direction, and a stylistic kinship that the
absorbed text had buried. We offer this as the diagnostic
comparison's characteristic yield: beyond quantifying the
contamination it removed, it un-hides relationships.

The drag itself has a reading: it measures how much a text is an
anthology — how far the language a text carries diverges in age from
the language its compilers wrote. Where the drag is near zero, text
and compiler speak from the same moment; where it is large, the
transmitted book is a container for other times. That is the
transmitted map's one legitimate use, and it is a use *of the
difference*, never of the transmitted positions alone.

## 8. Validation on known relative order, and what the corpus says back

Absolute dates cannot validate this instrument — the corpus has few to
none. Relative order can, because philology has established some
orderings that are independent of anything our features see. All
validations below are read on the cleaned build's trigram-led maps;
where a projection necessarily involves shared material, we say so.

**Known-later material measures later.** The Critical Edition of the
Mahābhārata [Sukthankar et al. 1933–1966] marks material excluded from
the constituted text — passages
the editors judged, on manuscript-stemmatic grounds, to be later
accretions. We rebuilt, for five books, three objects: the constituted
text, the apparatus material alone, and the augmented (vulgate-like)
text, and projected all of them as supplementary points with bootstrap
confidence intervals. In every case the apparatus material styles
later than its constituted text, and every augmented text sits
lateward of its constituted counterpart. On the cleaned trigram map,
Book 13's apparatus — the control, a book *known* to be didactically
swollen — projects at the 48th percentile [43, 52] against its
constituted text's 31st; for the epilogue Book 18 the effect is
dramatic, 61 [39, 82] against 8; and all five books are directional.
(One asymmetry must be stated: the apparatus files themselves are not
stripped — they lie outside the strip's corpus — so their positions
still mix the accretors' composition with whatever the accretors
absorbed; that mixture is exactly what §7 taught us to read, and the
direction test does not depend on resolving it.) The e-text apparatus
we used is a subset of the full print apparatus, so these separations
are lower bounds. What this validates is precise and limited: the
axis correctly orders *layers of known relative date within one
transmission*. It cannot, and does not claim to, distinguish early
composition from faithful early-style transmission.

**Known-earlier material measures earlier.** Kirfel's 1927
reconstruction of the *Purāṇapañcalakṣaṇa* (PPL) — the genealogical
core-corpus his synoptic philology identified as the purāṇas' common
inheritance — enters our corpus both as constituted reconstruction
and as an identifiable layer inside its host purāṇas. The cleaned
corpus supports the strongest form of the test, by construction:
because the strip is one-directional for the PPL — its lines removed
from the purāṇas, never from the reconstruction (§2.2) — the cleaned
corpus contains the constituted PPL and *no near-verbatim copy of it
anywhere else*. The reconstruction cannot affect its carriers'
positions, nor they its; whatever positions they take are positions
of textually disjoint bodies. On that map the oldest stratum is
early — Kirfel's Textgruppe I projects at the 25th percentile
[23, 30], the ungrouped core at 25 [24, 27] — while its chief
carrier's residue reads late (the Vāyu at 81 [78, 85]): the carriers
are late once they stop speaking the inheritance's words, which is
the separation a priority claim needs. Kirfel's own internal grouping
is likewise recovered: his early Textgruppen project in a tight early
band (25–32 on the trigram lens: Textgruppe I at 25 [23, 30], the
ungrouped core at 25 [24, 27], Textgruppe II at 32 [27, 38]) and his
late Textgruppen far later (64–94, from Textgruppe Ia at 64 up to IIA
at 94) — a century-old stratigraphy, built from entirely different
evidence, sorted correctly by feature statistics. [NR-RECOMPUTE /
Kengo's call: the within-host layer comparison (PPL-parallel layer vs
Vāyu–Brahmāṇḍa common text: 28 [25, 31] vs 57 [42, 66], and
31 [29, 36] vs 79 [75, 83]) projects shared layers and therefore ran
on the transmitted build — restate it explicitly as a
same-transmission projection, or drop it in favor of the disjoint
form above.]

The obvious objection is genre: genealogical list-verse might simply
*style* early, wherever and whenever it was composed. We answer it
structurally, because in this corpus a content-based genre control is
unconstructible in principle — Kirfel's own result is that the
genealogical genre largely *is* the shared ancient inheritance, so
splitting texts into genealogy-like and remaining halves conflates
register with the age of borrowed text, on every build. (We ran such
splits; their pulls are real, one-directional, and uninterpretable for
exactly this reason — and the strip makes the entanglement vivid: after
shared text is removed, the Vāyu's manu-vaṃśa section contains 178 words
of genealogy of its own.) Four structural facts answer the objection
instead. First, by construction: the cleaned corpus contains no
near-verbatim PPL text outside the reconstruction, so the PPL's early
band and its carriers' late residues are positions of textually
disjoint bodies — the version of the objection with teeth, "the PPL
sits at the center of gravity of its own descendants," cannot arise.
Second, the early pole is not genealogical: the earliest units are
the epics' battle and dialogue books, thin in vaṃśa material, while
the pure-genealogy reconstruction's carriers read *late* once their
inherited genealogy is stripped — list-register per se does not read
early. Third, the apparatus experiment above is the genre-matched
validation — same books, same idiom, known-later material measuring
later. Fourth, register variation has its own axis, orthogonal to the
chronology (§9): the instrument books register separately rather than
folding it into the clock.

**What the corpus says back.** Findings that clear the validation bar,
stated at the instrument's resolution. Each runs against a received
view, and each lands where philology has already recorded hesitation —
a pattern that gives the instrument a second use: not overturning
chronologies by feature count, but locating where the received
chronology's soft points lie. (i) The Mahābhārata's four
closing books, merged into one ~17k-word block (individually they sit
below the length floor), project at the extreme early pole — their
residues at percentiles 1–8 — with the apparatus experiment showing
the constituted text itself owns that position. The finding is
nearly independent of the strip: the four books share little text
with the rest of the corpus (88–95% of their trigram mass survives
it). The stylometry is consistent with an early-fixed narrative
kernel that was appended to the epic late *as books*; it cannot
arbitrate between early composition and early-style transmission,
and we say so. (ii) The old Skandapurāṇa — transmitted in Nepalese
manuscripts of the ninth century [Adriaensen et al. 1998] — projects
earlier than the Mārkaṇḍeyapurāṇa (SP 29 [27, 32], Mārk 32 [28, 35]),
against the received relative dating [Hazra 1940]. The gap is
narrower than the transmitted texts suggest, and §7 says why: the
Mārkaṇḍeya carried a +6 drag — much of what seemed to separate the
two compilations was the Mārkaṇḍeya's absorbed later material, and
on their own diction the two sit close in time, with the direction
holding. At layer level the two interleave, and the same text's late
block (its pāśupata chapters) projects at the far late pole under
identical transmission (98 [97, 99] even as a stripped residue,
though at 2.9k residual words that value brushes the length floor) —
which is also the strongest available answer to the
transmission-conservatism confound. (iii) The Bhāgavatapurāṇa, whose
date is a famous open question, is the corpus's most isolated
register (every one of its books' nearest neighbours is internal to
it — a fact of the cleaned build that the absorbed text of the
transmitted build did not create and does not explain). Our
instrument *poses* the Bhāgavata question sharply — early language
state faithfully carried, or late mastery of the old register — and
does not answer it; we flag it as the natural target for methods
beyond frequency stylometry. §9.2 gives this isolation a geometric
statement, and shows the chronology does not depend on it.

## 9. Beyond the first axis: register, and one text's own dimension

### 9.1 The second dimension is register, not a second chronology

A one-gradient corpus embedded by classical MDS is expected to bend the
gradient into the second axis (the Guttman "horseshoe"), so before
interpreting our second dimension we measured the arch: the quadratic
fit of y on x explains R² = 0.006 on the trigram map (the word lens's
0.174 is §3.4's length artifact resurfacing, not a horseshoe — one
more reason the word lens's per-unit geometry is not read). There is
no arch to subtract, a point worth registering given how routinely it
is either invoked or ignored. The second dimensions of the two lenses
agree at ρ = 0.69, so y is a real, shared property of the texts, and
its covariates name it: at one pole, third-person enumerative
cataloguing (list connectives, numeral vocabulary); at the other,
second-person devotional address (devotional-vocabulary density
−0.52, optative share −0.59 on the trigram map, both robust to
dropping sub-3k residues). Coded covariates explain about half the
trigram rank variance (R² ≈ 0.55–0.58); the rest is register texture
our codes do not capture. Three disciplining facts. On residues, y
inherits a length covariate (ρ ≈ −0.4, against ≈ −0.2 on full
texts), so fine y-contrasts between very unequal residues are not
read. Sectarian *identity* (Śaiva-versus-Vaiṣṇava lexicon polarity)
correlates with y at ≈ 0 on the full texts, with a mild polarity
(−0.33) appearing on residues: y measures devotional *density* first,
which deity receives it a distant second. And nearness on y without
nearness on x means register kinship, never date. One diagnostic
comparison against the transmitted build is itself a finding: with
its absorbed text in, the Bhāgavata had been the devotional pole's
most famous occupant; on its own diction it sits mid-plane on y
(within a quarter standard deviation of the corpus, the sign
disagreeing between lenses) — its devotional idiosyncrasy was partly
its absorbed material's, and what is genuinely its own has moved
wholesale to the third axis (§9.2). The second axis is where the
"community structure" of §6's gains lives, and treating it as a
second chronology is the misreading this section exists to prevent.

### 9.2 The third dimension is one text, and flat maps hide it

Two-dimensional maps stop where the eigenvalues tell them to; ours do
not stop cleanly. The third MDS axis still carries 5.7% of the
variance against the second axis's 7.2% on the trigram lens (5.6%
against 9.7% on W1), so we examined it rather than discarding it,
aligning the two lenses' three-dimensional configurations by
Procrustes rotation. The per-axis cross-lens agreements are
0.95 / 0.74 / 0.74 — and the third figure is itself a diagnostic
argument for the strip: with the absorbed text left in, the two
lenses agree about axis 3 at only 0.46. Only with shared text removed
does the third dimension become as much a shared property of the
texts as the second — one more measurement the transmitted build was
corrupting.

And it is, to a first approximation, *one text's own dimension*. The
thirteen Bhāgavata units monopolize one pole: their mean position
sits 3.8 (W1) and 4.9 (C3) standard deviations of the remaining
corpus away from it, and axis-3 position correlates with Bhāgavata
membership at r = 0.76/0.84. Remove the Bhāgavata and the third
axis's cross-lens agreement drops to 0.65 while the first axis's is
untouched (0.95). Two consequences follow. First, §8's "most isolated
register" claim gains a geometric form: the Bhāgavata's idiosyncrasy
is not an extreme position on either shared dimension but a
*direction of its own*, recovered jointly by two feature systems that
share almost no linguistic material. Second — and this is the
referee-proofing — the chronology is orthogonal to the corpus's most
idiosyncratic member: classical MDS banks the Bhāgavata's peculiarity
on its own axis, and the ordering is unchanged by the text's removal.
(The length diagnostic again: axis 3 is length-clean on both lenses,
ρ ≤ 0.06.)

The flattening cost of 2-D also deserves numbers, because readers
*will* measure distances on the printed maps with their eyes. On the
trigram map, the Bhāgavata's second book and the Viṣṇupurāṇa's third
aṃśa — Delta 1.18, the 78th- and 99th-nearest neighbors of one
another — render 0.042 apart in the plane, inside the closest two
percent of all pairwise renderings; the third axis, which is to say
the Bhāgavata dimension, recovers them to 0.64. Nor is the effect the
Bhāgavata's alone: the Śivadharmaśāstra and the Vāyu's Gayāmāhātmya
(Delta 1.35, mutual neighbor ranks 105 and 83) render 0.038 apart. A
census makes it systematic: 86 pairs on the trigram map (79 on the
word map) sit in the closest two percent of in-plane distances while
their three-dimensional separation is at least three times larger —
and roughly a third of them involve a Bhāgavata unit, the skew axis 3
predicts. The rule we draw: on a crowded 2-D map, only axis-1
position is load-bearing; pairwise proximity in the middle is not
evidence of affinity. We publish rotatable three-dimensional versions
of the maps as supplementary material so that no reader is limited to
the flattening we chose.

## 10. Conclusion

What we met as an accident we leave as a method. For authorless,
accreting, editorially mediated corpora, the verification our
discovered axis demanded distills into a chronology-capable
stylometric recipe with six components: a cleaning discipline that
treats the corpus's pathologies — wholesale reuse, editorial word
division, scribal paratext — as directional contaminations to be
diagnosed and removed in corpus construction, not survived in
robustness tests (§2); two feature systems engineered to inherit
different mixtures of composer, scribe, and editor, whose agreement
is the measurement (§2–3); fixed-map supplementary projection with
bootstrap intervals for every layer and subset question (§2.3, §8);
null-model calibration pairing variance share with a length
diagnostic — a diagnostic sharp enough to catch one of our own lenses
failing on the cleaned corpus (§3.4, §4); a split-half retention
decomposition that tests whether the ordering has the mechanistic
signature of drift (§6); and a diagnostic comparison against the
uncleaned build that turns the corpus's worst pathology — wholesale
text reuse — into an instrument of its own, measuring what each
text's absorbed material had been doing to it and how much each book
is an anthology (§7). On the Sanskrit epic–purāṇic corpus the recipe
yields an ordering that two near-disjoint witnesses agree on, that no
tested confound explains, that behaves like autocorrelated loss, and
that correctly orders every independently known relative sequence we
could construct. Where it contradicts received opinion, it does so at
points that were contested already — the ordering doubles as a map of
where the received chronology is soft. Its limits are equally
definite: a ~3,000-word resolution floor, blindness below the level
of merged blocks, and the standing epistemic gap between language age
and book age — a gap the strip narrows but, since even a residue is
transmitted, never closes. Within those limits, a millennium of
anonymous tradition turns out to keep time — not in its marked
archaisms, which imitators can reach, but in the unconscious
frequency band where five hundred small habits drift, and mostly
fade, together.

---

## References

Adriaensen, R., Bakker, H. T. and Isaacson, H. (1998). *The
Skandapurāṇa, Volume I: Adhyāyas 1–25. Critically Edited with
Prolegomena and English Synopsis*. Groningen: Egbert Forsten.

Burrows, J. (2002). 'Delta': a measure of stylistic difference and a
guide to likely authorship. *Literary and Linguistic Computing*,
17(3): 267–287.

Eder, M. (2015). Does size matter? Authorship attribution, small
samples, big problem. *Digital Scholarship in the Humanities*, 30(2):
167–182.

Eder, M., Rybicki, J. and Kestemont, M. (2016). Stylometry with R: a
package for computational text analysis. *The R Journal*, 8(1):
107–121.

Evert, S., Proisl, T., Jannidis, F., Reger, I., Pielström, S., Schöch,
C. and Vitt, T. (2017). Understanding and explaining Delta measures
for authorship attribution. *Digital Scholarship in the Humanities*,
32(suppl. 2): ii4–ii16.

GRETIL. *Göttingen Register of Electronic Texts in Indian Languages*.
Niedersächsische Staats- und Universitätsbibliothek Göttingen.
https://gretil.sub.uni-goettingen.de/ (accessed August 2026).

Hazra, R. C. (1940). *Studies in the Purāṇic Records on Hindu Rites
and Customs*. Dacca: University of Dacca.

Juola, P. (2006). Authorship attribution. *Foundations and Trends in
Information Retrieval*, 1(3): 233–334.

Kirfel, W. (1927). *Das Purāṇa Pañcalakṣaṇa: Versuch einer
Textgeschichte*. Bonn: Kurt Schroeder.

Nehrdich, S., Hellwig, O. and Keutzer, K. (2024). One model is all you
need: ByT5-Sanskrit, a unified model for Sanskrit NLP tasks. In
Al-Onaizan, Y., Bansal, M. and Chen, Y.-N. (eds), *Findings of the
Association for Computational Linguistics: EMNLP 2024*. Miami:
Association for Computational Linguistics, pp. 13742–13751.

Nicholls, G. K. and Gray, R. D. (2008). Dated ancestral trees from
binary trait data and their application to the diversification of
languages. *Journal of the Royal Statistical Society: Series B*,
70(3): 545–566.

Oberlies, T. (2003). *A Grammar of Epic Sanskrit* (Indian Philology
and South Asian Studies 5). Berlin: Walter de Gruyter.

Rybicki, J. and Eder, M. (2011). Deeper Delta across genres and
languages: do we really need the most frequent words? *Literary and
Linguistic Computing*, 26(3): 315–321.

Stamou, C. (2008). Stylochronometry: stylistic development, sequence
of composition, and relative dating. *Literary and Linguistic
Computing*, 23(2): 181–199.

Sukthankar, V. S., Belvalkar, S. K., Vaidya, P. L. et al. (eds)
(1933–1966). *The Mahābhārata, for the First Time Critically Edited*.
19 vols. Poona: Bhandarkar Oriental Research Institute.

Swadesh, M. (1955). Towards greater accuracy in lexicostatistic
dating. *International Journal of American Linguistics*, 21(2):
121–137.

Xue, L., Barua, A., Constant, N., Al-Rfou, R., Narang, S., Kale, M.,
Roberts, A. and Raffel, C. (2022). ByT5: towards a token-free future
with pre-trained byte-to-byte models. *Transactions of the
Association for Computational Linguistics*, 10: 291–306.
