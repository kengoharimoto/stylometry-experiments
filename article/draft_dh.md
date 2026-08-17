# Losses are the clock: recovering relative chronology from stylometric drift in the Sanskrit epics and purāṇas

**Status: DRAFT 2026-08-17 — §1–3 of 9. Drafted from
`claims_evidence_map.md`; every number cross-checked against the map, but
a final verification pass against the source notes/TSVs is required
before submission. Citations are author-year placeholders; bibliography
to be assembled and verified.**

**Target:** DSH / Journal of Cultural Analytics (per `outline_dh.md`).

---

## Abstract (draft)

Stylometry's standard successes are attributions: a bounded set of
candidate authors, a disputed text, a verdict. We report a different kind
of result on a harder kind of corpus. The Sanskrit epics and purāṇas —
here 127 textual units totalling 4.5 million words — have no authors to
attribute, grew by accretion over roughly a millennium, share large
amounts of text verbatim, and reach us through editions whose
orthography, word division, and paratexts are editorial. We show that two
feature systems with almost no linguistic material in common — word
frequencies computed on algorithmically de-sandhied text, and character
trigrams computed on the undivided sandhied stream — independently
recover the same one-dimensional ordering of these texts (Spearman ρ =
0.95), and that this ordering survives removal of shared text, proper
names, and sectarian vocabulary, is invariant across feature-set sizes
and distance measures, and is reproduced exactly by an independent
implementation. Null models show that a dominant, ordering-shaped,
length-independent first axis of the kind we observe is the signature of
autocorrelated change — many small habits shifting together — and not of
mere heterogeneity. A split-half decomposition explains the mechanism:
depletion of an early-characteristic feature inventory alone reproduces
the ordering (ρ = 0.94), while feature gains order the late texts only
loosely. Losses are the clock; gains are the community structure. The
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
carries the chronological signal essentially alone (§6); and (v)
validation against independently known relative order — critical-edition
apparatus known to be later than its constituted text, and source layers
known to be older than their host redactions (§7). Along the way the
corpus pays the method back with findings that bear on live questions in
Sanskrit philology; we state them at the resolution the instrument
supports and no further.

Two disclaimers frame everything that follows. First, the method orders
*language states*, not books: a faithfully transmitted old text and an
old text are indistinguishable from inside a corpus, and transmission
can both preserve and level. We return to this limit repeatedly; it is
not a footnote but a property of the measurement. Second, the first axis
of an embedding is not intrinsically a timeline. The work of this paper
is precisely to close the gap between "the corpus has a dominant axis"
and "that axis is a chronology" — by construction (§3), by null models
(§4), by mechanism (§6), and by external validation (§7).

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
(B = 500). The corpus comprises 127 units — epic books (parvans,
kāṇḍas), whole purāṇas or their major divisions, and a small śāstra
outgroup — totalling 4,490,750 de-sandhied words (unit sizes 1.0k–462k,
median 17.3k; the length floor this range imposes is treated in §3.4).

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
byte-reconstruction) and re-ran the full sweep. At the recommended
settings the ordering is unchanged: cross-build agreement ρ = 0.98–0.99
(C3-500/1000), 0.98 (W1-80/200). The collapsed high-MFW W1 regime, by
contrast, *anti-correlates* across builds (−0.86 at 5000 MFW) — direct
confirmation that beyond the cliff W1 measures the shared material
itself, while below it the axis is indifferent to whether the shared
material is present at all.

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
of 500 C3 features correlate with it at |ρ| ≥ 0.7 (median |ρ| ≈ 0.25).
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
(§7).

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
with bootstrap confidence intervals. §7's validation cases inherit this
discipline; no headline claim in this paper rests on the individual
position of a short unit. The corpus's length imbalance (1k–462k words
per unit) is thus not normalized away but converted into an explicit
resolution limit of the instrument.

---

*[End of drafted portion. §4 Null models · §5 Anatomy · §6 Retention
clock · §7 Validation & case results · §8 Second dimension ·
§9 Conclusion — to follow.]*
