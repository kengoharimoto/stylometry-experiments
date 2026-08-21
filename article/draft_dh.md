# Losses are the clock: recovering relative chronology from stylometric drift in the Sanskrit epics and purāṇas

**Status: DRAFT 2026-08-19 (terminology 2026-08-21: the
"transmitted/composed" pair is dropped for plain "with-reuse/no-reuse"
throughout, Kengo's call) — restructured for the no-reuse precedence
reframe (new §7 "Two chronologies"; §8 validation updated with
no-reuse-chronology values; genre control replaced by the strip-first
defense per claims map §6.4; new §9.2 third dimension; conclusion
updated). Reframe numbers verified against
`figures/noreuse_reframe/unit_ci_*` + `movers_C3.tsv`,
`axis_anatomy/b2_models_*_noreuse_500.tsv`,
`e1_apparatus/e1_apparatus_C3_noreuse_500.tsv`, and
`mds3d/axis3_stats.tsv`. Earlier verification (2026-08-17): §4
null-model shares, §6 retention correlations, §8 E1/stratigraphy values
against the post-colophon-clean TSVs. Citations are author-year
placeholders; bibliography to be assembled and verified.**

**Target:** DSH / Journal of Cultural Analytics (per `outline_dh.md`).

---

## Abstract (draft)

Stylometry's standard successes are attributions: a bounded set of
candidate authors, a disputed text, a verdict. We report a different kind
of result on a harder kind of corpus. The Sanskrit epics and purāṇas —
here 127 textual units totalling 4.5 million words — have no authors to
attribute, grew by accretion over roughly a millennium, share large
amounts of text verbatim, and reach us through editions whose
orthography, word division, and paratexts are editorial, often with minimal philological care. We show that two
feature systems with almost no linguistic material in common — word
frequencies computed on algorithmically de-sandhied text, and character
trigrams computed on the undivided (not even spaces) sandhied stream — independently
recover the same one-dimensional ordering of these texts (Spearman ρ =
0.953), and that this ordering survives removal of shared text, proper
names, and sectarian vocabulary, is invariant across feature-set sizes
and distance measures, and is reproduced exactly by an independent
implementation. Null models show that a dominant, ordering-shaped,
length-independent first axis of the kind we observe is the signature of
autocorrelated change — many small habits shifting together — and not of
mere heterogeneity. A split-half decomposition explains the mechanism:
depletion of an early-characteristic feature inventory alone reproduces
the ordering (ρ = 0.939), while feature gains order the late texts only
loosely. Losses are the clock; gains have no systems. Because these
texts absorb one another on a large scale, we further compute the
chronology twice — with shared text included and with it
stripped: stripping preserves the global ordering
(ρ = 0.98 on trigrams) but moves individual texts in philologically
interpretable ways — the great compilations look later with their
borrowed skin on — and we give the stripped map precedence for dating
composition, with the trigram lens carrying it (on stripped residues,
the word lens develops a length artifact that our own null-model
diagnostic catches). The
instrument validates on layers of independently known relative order and
yields philologically consequential results, including a resolution of
the axis into register and chronology components. We state throughout
what the method measures — the relative age of language states, which is
not the same as the age of books.

---

## 1. Introduction

Computational stylometry earned its credibility on authorship. Given a
disputed document and a closed set of candidates, features as unassuming
as the frequencies of the most common words separate hands with a
reliability that has survived two decades of adversarial testing
[Burrows 2002; Juola 2006; Evert et al. 2017]. Chronology is the rarer
and harder target. Intra-author stylochronometry — ordering one writer's
works along their lifetime — has a literature but also a warning label:
the signal is weak, genre-entangled, and easily overwhelmed by editorial
noise [Stamou 2008]. Ordering an entire *tradition*, where no author is
available to hold style constant, would seem to compound the problem
past usefulness.

This paper argues the opposite, for a specific and well-motivated class
of corpus: large, formulaic, anonymous traditions that accreted over
centuries. Such corpora surrender the authorship signal entirely — and
in exchange, if usage drifts slowly and cumulatively across generations
of composers, they may expose a *diachronic* signal that single-author
corpora are too short-lived to show. The Sanskrit epic–purāṇic corpus is
close to an ideal test case, for reasons both attractive and hostile.
Attractive: it is enormous (our working corpus is 4.5 million words and
is a fraction of the whole), metrically and formulaically constrained
(most of it is śloka verse), and philology has spent a century
establishing islands of *relative* order within it — layers, borrowings,
and datable external witnesses — against which an instrument can be
validated without assuming any absolute date. Hostile: it has no
authors; its texts copy each other on a scale that dwarfs most reuse
problems in the field; and everything a stylometrist would normally
tokenize — word boundaries, sandhi, orthography, even the colophons
interleaved with the text — is in some measure the work of editors and
scribes rather than composers.

Our contributions are methodological first and philological second. We
show: (i) a **two-lens design** in which two feature systems with almost
disjoint linguistic content — word unigrams on neurally de-sandhied
text, and character trigrams on the undivided sandhied stream — act as
independent witnesses of one ordering (§2–3); (ii) a battery of
robustness controls adapted to this corpus's specific pathologies —
verbatim reuse, editorial word division, paratextual contamination,
extreme length imbalance (§2–3); (iii) a **null-model calibration**
establishing what kind of process does and does not produce a dominant,
ordering-shaped first axis in a distance embedding (§4); (iv) a
**retention decomposition** that explains *why* the axis orders the
corpus: the depletion of an early-characteristic feature inventory
carries the chronological signal essentially alone (§6); (v) a
**with-reuse-versus-no-reuse comparison**: rebuilding the corpus with
shared text stripped and reading the differences between the two maps as
findings — which text is dragged where by what it absorbed — rather than
as a robustness footnote (§7); and (vi)
validation against independently known relative order — critical-edition
apparatus known to be later than its constituted text, and source layers
known to be older than their host redactions — on both maps (§8). Along the way the
corpus pays the method back with findings that bear on live questions in
Sanskrit philology; we state them at the resolution the instrument
supports and no further.

Two disclaimers frame everything that follows. First, the method orders
*language states*, not books: a faithfully transmitted old text and an
old text are indistinguishable from inside a corpus, and transmission
can both preserve and level. We return to this limit repeatedly; it is
not a footnote but a property of the measurement — though §7 partially
operationalizes it, separating the age of the language a text *carries*
from the age of the language its compilers *wrote*. Second, the first axis
of an embedding is not intrinsically a timeline. The work of this paper
is precisely to close the gap between "the corpus has a dominant axis"
and "that axis is a chronology" — by construction (§3), by null models
(§4), by mechanism (§6), and by external validation (§8).

## 2. A hostile corpus, and the preprocessing it forces

### 2.1 What a stylometrist needs to know about Sanskrit transmission

Classical Sanskrit text is transmitted as a continuous euphonic stream.
*Sandhi*, the obligatory phonological fusion at word junctions, rewrites
word boundaries: *tataḥ* + *uvāca* surfaces as *tata uvāca*, *ca* + *api*
as *cāpi*. Manuscripts compound the difficulty by writing without word
division (*scriptio continua*); the spaces in a printed edition are the
editor's analysis, not the tradition's testimony, and editorial habits
differ by edition, era, and school. Above the letter, the transmitted
stream is punctuated by *colophons* — chapter-closing formulas naming the
work and section — which are paratext added and normalized by scribes,
not composed text. A stylometric pipeline that tokenizes a printed
edition therefore measures three superimposed authorships at once: the
composer's, the scribal tradition's, and the editor's.

This is not a peculiarity to be normalized away by better cleaning; it
forces a design decision. Any single featurization inherits one
particular mixture of those three hands. Our response is to build two
featurizations that inherit *different* mixtures — and to treat their
agreement, not either one alone, as the measurement.

### 2.2 The two lenses

**W1 (words, de-sandhied).** We resolve sandhi computationally with a
byte-level sequence-to-sequence model (ByT5) fine-tuned for Sanskrit
sandhi resolution, run offline in int8 quantization over the full corpus
[CITE: unsandhi model]. The output is a word-segmented text on which we
count word unigrams and keep the 500 most frequent words (MFW) as
features. We say "most frequent words" and not "function words"
deliberately: in a śloka corpus the top 500 contains, alongside genuine
particles and pronouns, high-frequency content and formulaic vocabulary
(*deva*, *dharma*, *rājan* are all in the top 80), and the analysis in
§5 depends on being honest about that composition.

**C3 (character trigrams, no word division).** From the sandhied text we
strip *all* whitespace — restoring, in effect, scriptio continua — and
count character trigrams over the continuous stream, keeping the top
500. Stripping the spaces is not a convenience but a correction: word
division is editorial, and when we counted trigrams over spaced text,
33% of the top-500 features contained a space character, importing the
editors' segmentation habits directly into the feature space. Removing
them measurably improved agreement with the word lens at every feature-set
size we tested (§3.2), and the texts that moved most were precisely
those from editions with distinctive spacing conventions — movement, in
seven of the nine largest cases, *toward* the position the word lens had
assigned them all along. Encoding granularity below the space level is
not a live issue: re-encoding the IAST digraphs (kh, bh, ai, …) as
single phoneme symbols changes the ordering by ρ ≥ 0.99 and we cite it
only as a preempted objection.

Both lenses feed the same instrument: Burrows's Delta [Burrows 2002] on
the 500 z-scored feature rates, classical multidimensional scaling of
the resulting distance matrix, and Procrustes alignment (rotation and
reflection only) of all configurations onto a fixed reference frame so
that coordinates are comparable across runs. For questions about layers
and subsets of texts we never recompute the map on a mutilated corpus;
we project the subset into the fixed map as supplementary points (Gower
projection) and attach confidence intervals by bootstrap over lines
(B = 500). The corpus comprises 127 units totalling 4,490,750
de-sandhied words (unit sizes 1.0k–462k, median 17.3k; the length floor
this range imposes is treated in §3.4): the books of the two epics
(Mahābhārata parvans, Rāmāyaṇa kāṇḍas) plus selected Critical-Edition
appendix blocks as separate units, whole purāṇas or their major
divisions, a small śāstra/ritual outgroup, and the seven text-group
units of Kirfel's constituted *Purāṇapañcalakṣaṇa* reconstruction
[Kirfel 1927], included as first-class units because §8's validation
turns on them.

### 2.3 Why two lenses constitute two witnesses

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

### 2.4 Three lessons in corpus hygiene, told against ourselves

Three episodes from this project generalize to any stylometric work on
non-Latin-script or editorially mediated corpora, and we report them as
methods results rather than confessions.

**Tokenization silently mutilated by locale assumptions.** R stylo
0.7.5 with `corpus.lang = "English.all"` treats the Latin Extended
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
text (the Nīlamatapurāṇa) arrived from an edition with sandhi
editorially dissolved: ~19% of its word boundaries carried pausa forms
against a corpus norm of ~2.5%. In raw-cosine MDS on character trigrams
it was a spectacular outlier (nearest-neighbour distance 12.8× the
corpus median); under Delta and other z-scoring measures it sat
normally (1.5–1.9×). The divergence is principled — z-scoring subtracts
the shared Zipfian head where orthographic convention lives, raw cosine
does not — and it converts an embarrassment into an instrument:
*disagreement between standardized and unstandardized metrics over a
single text is a preprocessing-inconsistency detector*. (A silent
secondary fault compounded the episode: an >85%-ASCII line filter meant
to drop English contamination was eating a third of the text's genuine
lines. Silent filters deserve per-file survival statistics.)

**Paratext with a directional bias.** Chapter colophons are only 0.9% of
corpus words, but they are not noise: their density varies by genre
(purāṇas have many short chapters) and their formulas are late-styled,
so they bias colophon-heavy texts *lateward*. Across affected units the
correlation between colophon fraction and position shift on removal was
−0.58, with single-unit shifts up to 15 percentiles. We removed
colophons corpus-wide with a validated line filter and re-ran every
instrument; no headline conclusion moved (map correlation before/after:
ρ = 0.998 on W1, 0.991 on C3), several tightened, and the two lenses
agreed better (0.950 → 0.953). The general point: paratext is not
random clutter — it is systematically distributed, and in a diachronic
analysis systematically distributed means directionally biasing.

## 3. The ordering and its robustness

### 3.1 The convergence result

At the adopted settings — 500 MFW for W1, 500 space-free trigrams for
C3 — the first MDS axes of the two lenses agree across the 127 units at
Spearman ρ = **0.953** [FIGURE 1: the two maps side by side; FIGURE 2:
W1×C3 agreement across the joint sweep]. A full grid sweep (W1 from 30
to 5000 MFW; C3 from 250 to 12,000 features) locates the agreement ridge
at moderate feature counts on both sides, peaking at 500×500; the
adopted setting is the peak of measured cross-lens agreement, not a
tuned free parameter.

The sweep's two failure regimes are as informative as its plateau. W1 is
stable from 80 to ~800 MFW (ρ ≥ 0.91 against the plateau ordering) and
then collapses — 0.83 at 1500, 0.39 at 3000, 0.04 at 5000 — as the
feature list leaves the shared vocabulary and fills with text-specific
content words: the axis becomes a topic model and stops ordering.
C3, by contrast, is nearly invariant from 250 to 12,000 features
(ρ ≥ 0.95 between any two settings): sub-lexical features saturate the
shared inventory early, and additional features add resolution, not
topics. The asymmetry matters for practice: with sub-lexical features
the feature-count knob is forgiving; with word features it is the
difference between measuring usage and measuring subject matter.

### 3.2 What the ordering does not depend on

**Distance measure.** Every standardization-based measure we tested
(classic, Argamon's rotated, Eder's, and Würzburg cosine Delta) and the
L1-family measures (Manhattan, Canberra, min-max) reproduce the axis at
ρ = 0.95–1.00 at the adopted settings. Only unstandardized cosine and
Euclidean distance blur it (0.81–0.91), for the textbook reason: without
z-scoring, the Zipfian head dominates and the discriminative mid-ranks
are drowned. Two cautions from the metric sweep deserve wider currency.
First, the apparent robustness of unstandardized metrics to feature-set
size (ρ = 0.99 across settings) is *robustness by deafness* — added
features carry negligible weight, so nothing changes because nothing is
heard. Second, Canberra shows the mirror pathology: its per-feature
normalization amplifies rare features, so it holds at 500 features and
degrades by 12,000 as content leaks in. Within the Delta family,
interchangeability is expected [Evert et al. 2017] and we count it as a
consistency check, not independent confirmation.

**Verbatim reuse.** This corpus shares text on a scale that makes reuse
the first objection to any similarity result: whole genealogical
chapters circulate across purāṇas nearly verbatim. We rebuilt the corpus
with cross-text verbatim reuse removed (shingle matching with fuzzy
extension; both directions; the removal itself validated by
byte-reconstruction) and re-ran the full sweep. The ordering is
unchanged: cross-build agreement is ρ = 0.98–0.99 on C3 (at 500 and
1000 features) and ρ = 0.98 on W1 at 80–200 MFW, easing to 0.91 at
W1-500 — the adopted setting sits at the edge of the reuse-stripped
build's plateau, which narrows for a mechanical reason (removing
parallels shrinks token counts, so the shared word inventory is
exhausted at lower ranks), and on that build the sweep recommends
W1 200–500; the ordering itself is the same across the plateau. The
collapsed high-MFW W1 regime, by contrast, *anti-correlates* across
builds (−0.86 at 5000 MFW) — direct confirmation that beyond the cliff
W1 measures the shared material itself, while below it the axis is
indifferent to whether the shared material is present at all. This
robustness result is deliberately minimal: §7 returns to the stripped
build with the opposite question — not whether the ordering survives
(it does) but what the differences between the two maps *mean*.

**Names and sectarian vocabulary.** Striking all 36 theonyms and
divine-name stems from the W1-500 list (refilling to 500 from the
frequency ranking) leaves the axis at ρ = 0.9976 against baseline;
striking 67 names plus ritual and sectarian lexemes leaves 0.9898, with
a maximum single-text movement of 13 percentiles. The ordering is not a
disguised sectarian sorting.

**Implementation.** The full C3 pipeline — feature list, frequency
table, Delta distance matrix, and map — is reproduced exactly by an
independent implementation (stylo 0.7.5 in R, fed the pre-stripped
corpus): 500/500 identical features, distance-matrix correlation
1.0000, map correlation 1.0000. We mention this not as ceremony but
because §2.4's tokenization episode shows exactly how much an
"independent implementation" can silently fail to be one; the
replication was run with the tokenizer verified.

**Single texts.** Deleting any one of the 127 units (with feature refill
and recomputation) leaves the axis at ρ ≥ 0.98; deleting the two
highest-leverage groups a referee would nominate — the śāstra outgroup
and a late two-text pair that anchors the far end — leaves ρ ≥ 0.99. No
small set of texts carries the axis.

### 3.3 What the ordering is made of

The axis is not a few-feature artifact: only 4 of 500 W1 features and 8
of 500 C3 features correlate with it at |ρ| ≥ 0.7 (median |ρ| = 0.28
and 0.23 respectively).
A class decomposition — computing the axis from each linguistic class
alone, and with each class removed and refilled — shows that *no class
is necessary and nearly every class suffices*: particles alone
reproduce the ordering at 0.89, content words alone at 0.94,
word-interior trigrams alone at 0.97, and every single-class removal
leaves ρ ≥ 0.94. The one genuine exception is boundary phonology:
junction-spanning and word-final trigrams alone fail (ρ = 0.11–0.14) —
sandhi texture, the most edition-sensitive stratum, is precisely where
the ordering is *not*. We defer the full anatomy and its linguistic
reading to §5, but the redundancy result belongs here, among the
robustness facts: an axis that survives the removal of any feature
class it is accused of depending on is not that class's artifact.

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

### 3.4 The honest boundary: unit length

Length is the one failure mode the two lenses *share*, so their
agreement — the paper's central device — offers no protection against
it, and it must be bounded directly. Window-resampling experiments
(contiguous windows of 1k–10k words drawn from long texts) show the two
lenses failing in different but equally disqualifying ways below a few
thousand words: W1 positions keep a stable mean but explode in variance
(single 1k windows of one mid-corpus text span half the axis); C3
positions drift systematically with window size. We therefore treat
every unit below ~3,000 words as an *uncertainty region* — its
individual position is not evidence — and make claims about short texts
only at the level of merged blocks large enough to clear the floor,
with bootstrap confidence intervals. §7's and §8's cases inherit this
discipline; no headline claim in this paper rests on the individual
position of a short unit. The corpus's length imbalance (1k–462k words
per unit) is thus not normalized away but converted into an explicit
resolution limit of the instrument.

## 4. Why a drift axis emerges: null and generative models

Everything in §3 shows that the corpus *has* a dominant, robust first
axis. Nothing in §3 says what kind of process produces one. This section
calibrates that question with three synthetic corpora, each matched to
the real one in unit count, unit sizes, and feature inventory, with
features drawn multinomially (10 replicates each; both lenses, W1
reported here, C3 mirroring throughout).

**Null 1: exchangeable.** All units sample from one shared rate vector —
no heterogeneity at all. Its first MDS axis nonetheless carries 13.1 ±
0.4% of the squared-distance variance, statistically indistinguishable
from the real corpus's 13.4%. The resemblance is a trap, and diagnosing
it is the section's first methodological point: the null's axis is a
**length artifact** (correlation with log unit length: ρ = 0.91 —
smaller samples deviate more in every feature, and Delta geometry
arranges units by sampling noise magnitude). The real axis is
length-independent (ρ = 0.065 against log length). *First-axis variance
share is uninterpretable without a length diagnostic beside it*; we
suggest this pairing as standard practice for any MDS/PCA-based claim
about corpus structure — and §7.2 applies it to catch exactly such an
artifact arising in our own stripped build.

**Null 2: heterogeneity without covariance.** Each unit receives its own
rate vector, drawn i.i.d. around the corpus mean with the empirically
observed per-feature between-text variance — as much per-text
distinctiveness as the real corpus, but uncorrelated across features.
The dominant axis collapses: 3.3 ± 0.1% variance share. Mere
distinctiveness, however strong, does not make a gradient.

**Generative model: drift.** Feature rates evolve as a slow random walk
along a latent order (step variance fitted to the observed between-text
variance), and units sample from their position's rates. Now the first
axis carries 43.4 ± 2.7% and — the decisive property — recovers the
latent generation order at ρ = 0.986 ± 0.006 (C3: 0.997). A dominant,
ordering-shaped, length-independent first axis is the *signature of
autocorrelated change*: many features shifting together along an
underlying progression. The real corpus's 13.4% sits between the
heterogeneity floor and the pure-drift ceiling, which is what a real
tradition should do — its variance budget is shared among drift,
register, genre, and idiosyncrasy; §9 locates the two largest non-drift
components.

**The axis is a property of the distances, not of MDS.** Four methods
with different assumptions — PCA on the z-scored features (no distance
matrix, no double-centering, L2 where Delta is L1), 1-D isomap
(geodesics), spectral seriation (Fiedler vector), and a
Hamiltonian-path/TSP seriation — were run on both lenses. Every global
embedding finds the drift gradient in its top-2 plane (PCA: ρ = 0.997
W1, 0.995 C3 after alignment; isomap 0.92/0.85; Fiedler 0.95/0.82). On
C3 the *raw* first dimensions disagree across methods, and the reason is
itself a result: C3's top two eigenvalues are nearly degenerate (ratio
1.07, vs 1.68 on W1), because the register dimension (§9) is almost as
strong as the drift dimension — so which one surfaces first is
method-dependent while the plane containing both is not. The TSP
seriation fails on both lenses (ρ ≈ 0.24–0.29), and its failure is
independent evidence: path seriation tracks a gradient only when the
data are effectively one-dimensional, so its snake-folding here
confirms a genuine second dimension before §9 measures one. We do not
use t-SNE or UMAP anywhere: they preserve local neighborhoods and
discard exactly the global geometry a gradient reading lives in.

## 5. What the axis counts

The loading tables put linguistic flesh on the statistical skeleton. On
W1, the pole that anchors the early end is the machinery of narrated
dialogue: anaphoric pronoun chains (*tam* ρ = −0.78, *sa* −0.70),
narrative preterites (*abravīt* −0.68, *āsīt* −0.59, *jagāma* −0.63),
speech-sequencing converbs (*śrutvā* −0.65, *uktvā* −0.62), the simile
particle *iva* (−0.62), and the second-person apparatus of face-to-face
address (*tvām*, *tava*, vocative *rājan*). The late pole is the
machinery of exposition: itemizing *-ādi* (+0.79, the strongest single
loading in either lens), *jñāna/jñānam*, *brahma*, sentence-connective
*tad* (+0.60), and — in C3 — the optative endings of prescription
(*-yet* +0.71, *-yāt* +0.66) and the taddhita derivative suffixes of
technical vocabulary (*-ikā/-ika* +0.77/+0.56). Both lenses, read
blind, describe the same drift: from narrated encounter toward
enumerated doctrine. Whether that gradient is *temporal* is not settled
by naming it; that burden falls on §6 and §8.

Three structural facts sharpen the picture. First, the signal is
radically distributed (§3.3): the poles just quoted are the readable tip
of five hundred small correlations, not a shortlist that carries the
axis. Second, the two lenses reach their agreement from different
structural levels of the language — W1 from whole-word habits of every
class, C3 predominantly from word-internal morphology (§2.3) — so the
register reading is corroborated across levels, not repeated. Third, the
class decomposition's one strong negative localizes what the axis is
*not*: boundary phonology alone (junction and word-final trigrams)
retains almost nothing of the ordering (ρ = 0.11–0.14). The stratum
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
A only, we selected features characteristic of the epic pole (81
features with early/late rate ratio ≥ 1.5) and of the late pole (65
features, inverse criterion). On half B only — text the selection never
saw — we scored each unit's **loss component** (depletion of the
early-typical inventory) and **gain component** (acquisition of the
late-typical inventory), and compared each to the drift axis.

The loss component alone reproduces the ordering at ρ = **0.939**. The
gain component reaches 0.720. Adding gains to losses improves the
ordering only marginally (0.951): the clock is carried by what texts
*stop doing*. The asymmetry deepens inside subpopulations, where the
easy epic-versus-late contrast is unavailable: within the late block
alone, losses still order at 0.941 while gains fall to 0.683; within all
non-epic units, 0.891 versus 0.571. And a strict presence/absence
variant — scoring only whether features occur at all, the literal Dollo
reading — collapses to 0.474: the early inventory does not *vanish*
from late texts, it *dwindles*. The defensible form of the hypothesis is
therefore not Dollo's law transplanted, but Swadesh's retention rate
generalized from a cognate list to the frequency spectrum of style:
**losses are the clock; gains are the community structure.** The gains
side is not noise — late texts share their acquisitions, which is
precisely why the gain component tracks affiliation (§9 finds the same
structure from another direction) — but it is the wrong hand for
telling time.

The decomposition replicates on the trigram lens, and on the no-reuse
chronology of §7: loss alone orders at 0.856–0.868 invariantly across
feature-selection thresholds and across both corpus builds, with gains
at 0.60–0.69 — the same asymmetry from independent features, on a map
built from residues (the trigram feature sets are flatter, so the
absolute correlations sit below W1's; the shape is identical).

This decomposition upgrades the paper's claim from correlation to
mechanism. The drift axis works as a chronometer *because* it is, in
effect, a retention measure computed over five hundred features at
once; and it predicts where the method should transfer: any long
tradition whose composition is continuous and whose feature inventory
depletes faster than it recycles — legal formulae, liturgical corpora,
scholastic commentary chains — is a candidate.

## 7. Two chronologies: with the shared text and without

### 7.1 Why one map is not enough

Section 3.2 established that the ordering survives the removal of shared
text; this section argues that the *differences* between the two maps
are themselves the finding. A purāṇa as transmitted is a mixture: the
compilers' own composition plus everything the tradition deposited into
it — inherited cores, migrating māhātmyas, wholesale incorporations of
other works. Its position on the with-reuse map is the center
of mass of that mixture, and every borrowed layer drags the position
toward wherever the *source's* language sits. For the question "what
language does this text carry?" that map is the right instrument. For
the question "when was this text composed?" it is systematically
confounded — these texts kept being upgraded, and a text's borrowed skin
answers for its sources, not for its makers. The reuse-stripped corpus
(shingle-matched fuzzy removal at a threshold calibrated against
known-unrelated control pairs; symmetric drop, except that Kirfel's
constituted *Purāṇapañcalakṣaṇa* is treated as the one known *source*:
its lines are removed from the purāṇas, never from the reconstruction)
approximates each text's own diction, and its map approximates the
chronology of composition. We therefore report both chronologies, and
give the no-reuse one precedence for dating claims.

### 7.2 The lenses swap roles on residues

Before reading the stripped map we re-ran §4's null battery on it, and
the length diagnostic earned its keep. Stripping is savagely uneven —
residues span 648 to 345,000 words — and on samples that small the word
lens's exchangeable null now produces a *stronger* first axis than the
real corpus's own (18.5 ± 0.4% share, ρ = 0.96 against log length,
versus the real axis's 12.8% at ρ = 0.44): on residues, W1's first axis
is partly a length artifact, and we do not cite its per-unit positions.
The trigram lens is immune for a mechanical reason — even a small
residue supplies hundreds of thousands of trigram events, so its
exchangeable null stays weak (6.9% share) and its real axis stays
length-clean (ρ = 0.064). The no-reuse chronology is therefore
**trigram-led**: C3 supplies the numbers, W1 corroborates the ordering
(cross-lens ρ = 0.93 on the stripped build) and the movers' directions.
The with-reuse hero map's division of labor is thereby inverted, which
is itself a portable lesson: whichever lens has the smaller event count
per unit inherits the small-sample regime.

### 7.3 What moves, and what the moves mean

Globally the two chronologies agree — Spearman ρ = 0.982 between the
with-reuse and no-reuse orderings on C3 (0.908 on W1) — so nothing in
§§3–6 is at stake. Locally, sixteen of 126 units move with
non-overlapping bootstrap intervals [TABLE: movers, C3, both positions
with CIs], and the moves sort into three legible classes.

**The great compilations move early.** The largest moves of
well-measured texts run toward the early pole: the Brahmāṇḍapurāṇa from
the 63rd percentile to the 44th, its second khaṇḍa −12, the Śivapurāṇa's
Dharmasaṃhitā −10 (the one named move whose intervals graze rather than
separate, overlapping by 0.4 of a percentile), the Mārkaṇḍeya −6, and —
smaller but CI-clean — the
two giant compilations, Padma (48 → 44) and Bhaviṣya (64 → 61). Read
with §7.1: what these texts absorbed sits, on average, *later* than what
their compilers wrote. The Śivadharma corpus makes the mechanism
concrete: the Śivadharmaśāstra and Śivadharmottara sit at the far late
pole (percentiles 91–95), and the texts that absorbed them wholesale —
the Bhaviṣya incorporates roughly a quarter of each; the Padma, the
Dharmasaṃhitā, and the Revākhaṇḍa large shares — are precisely
early-ward movers: their borrowed skin had been answering for their
position. Symmetrically, a few texts move late (the Vāyu, 71 → 81; its
third section +11; the Śivapurāṇa's Umāsaṃhitā +9): what *they* carried
was older than their own hand.

**The old-core carriers dissolve.** The sections of the Vāyu and the
Viṣṇu aṃśas that carry the shared genealogical inheritance retain almost
nothing under the strip — the Vāyu's manu-vaṃśa section keeps 1,064 of
20,373 words — and drop below the §3.4 length floor: their no-reuse
positions are simply not measurable, and we grey them out rather than
read them. That emptiness is a measurement, not a failure: for these
texts, the transmitted text *is* mostly the shared inheritance, which is
Kirfel's century-old thesis [Kirfel 1927] restated as a retention
statistic.

**Pseudo-neighborhoods fall away.** On the with-reuse map, the
Viṣṇupurāṇa's nearest neighbors are its own copyists — texts that
absorbed it. On the stripped map those neighbors recede, and on its own
diction the Viṣṇu sits as close to the Bhāgavata as to anything else.
The two texts treat the same narrative material with almost no shared
wording (under the symmetric strip, the Viṣṇu's Kṛṣṇa book loses 80% of
its words to parallels elsewhere; the Bhāgavata's, treating the same
story, loses 6%) — two independent tellings, no copying in either
direction, and a stylistic kinship that the with-reuse map had buried
under the Viṣṇu's borrowed skin. We offer this as the reuse-strip
design's characteristic yield: it does not merely defend a result, it
un-hides relationships.

### 7.4 What precedence means, and does not mean

Giving the no-reuse chronology precedence is a statement about *which
question each map answers*, not a demotion of the with-reuse map. Every
claim in §8 is therefore validated on both; where the two disagree about
an individual text, the no-reuse reading dates the compilers and the
with-reuse reading dates the language the tradition chose to keep — and
the gap between them measures how much a text is an anthology. The
first disclaimer of §1 does not dissolve: even a residue is transmitted,
and below-threshold paraphrase of inherited material survives the strip.
The strip narrows the gap between language age and composition age; it
does not close it.

## 8. Validation on known relative order, and what the corpus says back

Absolute dates cannot validate this instrument — the corpus has few to
none. Relative order can, because philology has established some
orderings that are independent of anything our features see.

**Known-later material measures later.** The Critical Editions of the
Mahābhārata mark material excluded from the constituted text — passages
the editors judged, on manuscript-stemmatic grounds, to be later
accretions. We rebuilt, for five books, three objects: the constituted
text, the apparatus material alone, and the augmented (vulgate-like)
text, and projected all of them as supplementary points with bootstrap
confidence intervals. In every case, on both lenses, the apparatus
material styles later than its constituted text, and every augmented
text sits lateward of its constituted counterpart. For the epilogue
books the effect is dramatic — Book 18's apparatus projects at the 65th
percentile [48, 81] of the drift axis against its constituted text's
5th; for the control (Book 13, a book *known* to be didactically
swollen) the apparatus sits at 57 [56, 61] against 36. The validation
carries over to the no-reuse chronology, where it matters most: on the
stripped trigram map Book 13's apparatus projects at 48 [43, 52] against
its constituted text's 31, Book 18's at 61 [39, 82] against 8, and all
five books are directional. (One asymmetry must be stated: the apparatus
files themselves are not stripped — they lie outside the strip's corpus
— so their positions still mix the accretors' composition with whatever
the accretors absorbed; that mixture is exactly what §7 taught us to
read, and the direction test does not depend on resolving it.) The e-text
apparatus we used is a subset of the full print apparatus, so these
separations are lower bounds. What this validates is precise and
limited: the axis correctly orders *layers of known relative date within
one transmission*. It cannot, and does not claim to, distinguish early
composition from faithful early-style transmission.

**Known-earlier material measures earlier.** Kirfel's 1927
reconstruction of the *Purāṇapañcalakṣaṇa* (PPL) — the genealogical
core-corpus his synoptic philology identified as the purāṇas' common
inheritance — enters our corpus both as constituted reconstruction and
as an identifiable layer inside its host purāṇas. Inside the Vāyu and
Brahmāṇḍa purāṇas, the PPL-parallel layer projects consistently earlier
than the same texts' other shared layer (the Vāyu–Brahmāṇḍa common
text): e.g., 28 [25, 31] versus 57 [42, 66], and 31 [29, 36] versus 79
[75, 83], on units where both layers are substantial (CIs by line
bootstrap; both lenses concur). Kirfel's own internal grouping is
likewise recovered: his early Textgruppen project in a tight early band
(percentiles 23–37 across both lenses, with Textgruppe I and the
ungrouped core at 23–29) and his late Textgruppen far later (48–79 on
the word lens, 66–95 on the trigram lens) — a century-old stratigraphy,
built from entirely different evidence, sorted correctly by feature
statistics.

The no-reuse chronology strengthens this validation in a way the
with-reuse map cannot. Because the strip is one-directional for the
PPL — its lines are removed from the purāṇas, never from the
reconstruction — the stripped corpus contains the constituted PPL and
*no near-verbatim copy of it anywhere else*: the reconstruction can no
longer affect its carriers' positions, nor they its. On that map the PPL
keeps its band (Textgruppe I at the 25th percentile [23, 30], the
ungrouped core at 25 [24, 27]) while its chief carrier's residue reads
late (the Vāyu at 81 [78, 85], against 71 with reuse included). The oldest
stratum is early on a map from which its own copies are absent, and the
carriers are late once they stop speaking its words — a separation
between textually disjoint bodies, which is the strongest form the
priority claim can take.

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
instead. First, the strip (§7): the no-reuse map contains no
near-verbatim PPL text outside the reconstruction, so the PPL's early
band and its carriers' late residues are positions of textually disjoint
bodies — the version of the objection with teeth, "the PPL sits at the
center of gravity of its own descendants," is answered by construction.
Second, the early pole is not genealogical: the earliest units on every
build are the epics' battle and dialogue books, thin in vaṃśa material,
while the pure-genealogy reconstruction's carriers read *late* once
their inherited genealogy is stripped — list-register per se does not
read early. Third, the apparatus experiment above is the genre-matched
validation — same books, same idiom, known-later material measuring
later. Fourth, register variation has its own axis, orthogonal to the
chronology (§9): the instrument books register separately rather than
folding it into the clock.

**What the corpus says back.** Findings that clear the validation bar,
stated at the instrument's resolution: (i) The Mahābhārata's four
closing books, merged into one ~17k-word block (individually they sit
below the length floor), project at the extreme early pole on both
lenses — with the apparatus experiment showing the constituted text
itself owns that position. The stylometry is consistent with an
early-fixed narrative kernel that was appended to the epic late *as
books*; it cannot arbitrate between early composition and early-style
transmission, and we say so. The claim carries to the no-reuse
chronology essentially unchanged — the four books share little text with
the rest of the corpus (88–95% of their trigram mass survives the
strip), and their residues stay at the early pole (percentiles 1–8).
(ii) The old Skandapurāṇa — transmitted in
Nepalese manuscripts of the ninth century — projects earlier than the
Mārkaṇḍeyapurāṇa as a whole on both lenses with separated confidence
intervals, against the received relative dating. On the no-reuse
chronology the direction holds but the gap narrows (SP 29 [27, 32],
Mārk 32 [28, 35]): the Mārkaṇḍeya is one of §7's early-ward movers, and
what separates the two texts with reuse included is partly the
Mārkaṇḍeya's absorbed later material — the no-reuse reading brings the
two compilations closer in time than the with-reuse one suggests. At layer
level the two interleave, and the same text's late block (its pāśupata
chapters) projects at the far late pole under identical transmission
(98 [97, 99] even as a stripped residue, though at 2.9k residual words
that value brushes the length floor) — which is
also the strongest available answer to the transmission-conservatism
confound. (iii) The Bhāgavatapurāṇa, whose date is a famous open
question, is the corpus's most isolated register (every one of its
books' nearest neighbours is internal to it), and its position is
strongly scale-dependent across feature-set sizes in a way no other
text shows. Our instrument *poses* the Bhāgavata question sharply —
early language state faithfully carried, or late mastery of the old
register — and does not answer it; we flag it as the natural target for
methods beyond frequency stylometry. §9.2 gives this isolation a
geometric statement, and shows the chronology does not depend on it.

## 9. Beyond the first axis: register, and one text's own dimension

### 9.1 The second dimension is register, not a second chronology

A one-gradient corpus embedded by classical MDS is expected to bend the
gradient into the second axis (the Guttman "horseshoe"), so before
interpreting our second dimension we measured the arch: the quadratic
fit of y on x explains R² = 0.018 (W1) and 0.007 (C3) — there is no
horseshoe to subtract, a point worth registering given how routinely
the arch is either invoked or ignored. The second dimensions of the two
lenses agree at ρ = 0.82, so y is a real, shared property of the texts,
and its covariates name it: at one pole, third-person enumerative
cataloguing (list connectives, numeral vocabulary); at the other,
second-person devotional address (optative share, devotional-vocabulary
density, ρ up to −0.60). Coded covariates explain about half the rank
variance (R² ≈ 0.45–0.55); the residue is register texture our codes
do not capture. Two disciplining facts: sectarian *identity* (Śaiva
versus Vaiṣṇava lexicon polarity) correlates with y at ≈ 0 — y measures
devotional *density*, not which deity receives it; and nearness on y
without nearness on x means register kinship, never date. The second
axis is where the "community structure" of §6's gains lives, and
treating it as a second chronology is the misreading this section
exists to prevent.

### 9.2 The third dimension is one text, and flat maps hide it

Two-dimensional maps stop where the eigenvalues tell them to; ours do
not stop cleanly. The third MDS axis carries almost as much variance as
the second (7.3% versus 8.0% on W1; 6.7% versus 9.5% on C3, with-reuse
build), so we examined it rather than discarding it, aligning the two
lenses' three-dimensional configurations by Procrustes rotation. The
per-axis cross-lens agreements are 0.97 / 0.86 / 0.46 on the
with-reuse build and 0.95 / 0.74 / 0.74 on the no-reuse one: on the
no-reuse build, the third dimension is as much a shared
property of the texts as the second.

And it is, to a first approximation, *one text's own dimension*. The
thirteen Bhāgavata units monopolize one pole: on the no-reuse build
their mean position sits 3.8 (W1) and 4.9 (C3) standard deviations of
the remaining corpus away from it, and axis-3 position correlates with
Bhāgavata membership at r = 0.76/0.84. Remove the Bhāgavata and the
third axis's cross-lens agreement drops (to 0.65 no-reuse, 0.27
with-reuse) while the first axis's is untouched (0.97/0.95). Two
consequences follow. First, §8's "most isolated register" claim gains a
geometric form: the Bhāgavata's idiosyncrasy is not an extreme position
on either shared dimension but a *direction of its own*, recovered
jointly by two feature systems that share almost no linguistic
material. Second — and this is the referee-proofing — the chronology is
orthogonal to the corpus's most idiosyncratic member: classical MDS
banks the Bhāgavata's peculiarity on its own axis, and the ordering is
unchanged by the text's removal. (The length diagnostic again: on the
with-reuse build W1's third axis is length-tinged, ρ = 0.54, so the
clean form of this result rests on C3 and the no-reuse build, where
axis 3 is length-clean at ρ ≤ 0.06.)

The flattening cost of 2-D also deserves one number, because readers
*will* measure distances on the printed maps with their eyes. The
Śivapurāṇa's Sanatkumārasaṃhitā and Viṣṇupurāṇa book 3 — Delta 0.92,
each roughly the fiftieth-nearest neighbor of the other — render 0.043
apart in the with-reuse W1 plane, indistinguishable from genuine
neighbors; the third axis recovers them to 0.190. The rule we draw:
on a crowded 2-D map, only axis-1 position is load-bearing; pairwise
proximity in the middle is not evidence of affinity. We publish
rotatable three-dimensional versions of all four maps as supplementary
material so that no reader is limited to the flattening we chose.

## 10. Conclusion

For authorless, accreting, editorially mediated corpora, we propose a
chronology-capable stylometric recipe with six components: two feature
systems engineered to inherit different mixtures of composer, scribe,
and editor, whose agreement is the measurement (§2); robustness sweeps
that seek out the failure regimes and read them (§3); fixed-map
supplementary projection with bootstrap intervals for every layer and
subset question (§2.2, §8); null-model calibration pairing variance
share with a length diagnostic (§4); a split-half retention
decomposition that tests whether the ordering has the mechanistic
signature of drift (§6); and a with-reuse-versus-no-reuse comparison
that turns the corpus's worst pathology — wholesale text reuse — into
its most informative instrument, dating the compilers separately from
the language they carried (§7). On the Sanskrit epic–purāṇic corpus the
recipe
yields an ordering that two near-disjoint witnesses agree on, that no
tested confound explains, that behaves like autocorrelated loss, and
that correctly orders every independently known relative sequence we
could construct — on both chronologies. Its limits are equally definite:
a ~3,000-word
resolution floor, blindness below the level of merged blocks, and the
standing epistemic gap between language age and book age — a gap the
no-reuse chronology narrows but, since even a residue is transmitted,
never closes. Within those
limits, a millennium of anonymous tradition turns out to keep time — not
in its marked archaisms, which imitators can reach, but in the
unconscious frequency band where five hundred small habits drift, and
mostly fade, together.

---

*[Bibliography to assemble: Burrows 2002; Juola 2006; Stamou 2008;
Evert et al. 2017; Eder (corpus-size and non-English Delta); Swadesh
1955; Nicholls & Gray 2008; Oberlies 2003; Kirfel 1927; plus Sanskrit
NLP citations (ByT5 sandhi model, digital corpora) and the
philological apparatus for §8's cases. All author-year pairs above are
placeholders pending verification.]*
