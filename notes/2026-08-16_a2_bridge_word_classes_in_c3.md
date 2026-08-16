# A2 bridge: the word classes behind W1 are NOT what C3 counts

2026-08-16. Kengo's question after the A1 tables: W1 and C3 produce nearly
the same picture (x-agreement 0.95) — is the distribution of the word
classes that drive W1 equally reflected in the character trigrams?

Method (`axis_anatomy/a2_bridge_c3_classes.py`): every corpus token of
every no-space C3 top-500 trigram is attributed to its source word (with
position: initial/final/interior/whole) or, if it spans a word junction,
to the majority-owner word. Source words are classified by the same
rule-based classifier applied to the W1-500 list (particle/indeclinable,
pronoun, narrative verb, prescriptive verb, numeral-and-list, content).
Axis signal = |ρ_x|-weighted share. Classifier is provisional pending the
A2 review; assignments dumped in `w1_class_assignments.tsv`.

## Result: the lenses agree on the map while counting different material

Signal share by class (vs token share in parentheses):

| class | W1 signal (rate share) | C3 signal (token share) |
|---|---|---|
| particle/indeclinable | 10.6% (36.5%) | 4.0% (5.2%) |
| pronoun | 13.2% (17.8%) | 1.9% (2.0%) |
| narrative verb | 4.5% (3.4%) | 1.7% (1.4%) |
| prescriptive verb | 1.6% (0.6%) | 1.0% (0.7%) |
| numeral/list | 8.0% (2.8%) | 3.9% (2.8%) |
| content | 62.0% (38.8%) | **87.6%** (87.9%) |

Closed classes carry 38% of the W1 axis but only 12% of the C3 axis.
Three observations:

1. **C3's drift signal lives inside the open-class lexicon** — but as
   *morphology*, not lexis: its top loadings are inflectional and
   derivational material embedded in content words (-vān from bhagavān/
   sarvān; smṛ- from the smṛtaḥ/smṛtam citation formulas; -ikā/-ika
   derivatives; -yet optatives inside pūjayet/kārayet), plus junction
   phonology. W1, counting whole word forms, cannot see below the word;
   C3 can, and that is where most of its signal sits.
2. **On W1 too, the particles are NOT the axis** — they are 36.5% of the
   top-500 token mass but only 10.6% of the loading mass. Particles are
   ubiquitous *and stable*; what loads is the narrative-dialogic lexicon
   and formulae (pronouns 13%, and the 62% open-class share led by rāja-,
   vīra, speech verbs, jñāna, ādi). This corrects the deck-era shorthand
   "the axis is particle habits." A2 proper ("does the particle class
   alone reproduce the axis?") will quantify how far the shorthand goes.
3. **No positional concentration**: C3 signal tracks token share across
   positions (interior 61/58%, junction 16/17%, final 10/13%, initial
   12/11%) — the axis does not privilege endings or junctions per se.

**Upshot for the article**: the convergence argument gets its strongest
form. The two lenses agree on the ordering (ρ 0.95) while drawing on
largely *disjoint linguistic strata* — W1 on closed-class habits plus
open-class narrative lexis; C3 on sub-lexical morphology and phrase
phonology. This is two nearly-independent witnesses of one drift, not one
signal counted twice.

## Flag: colophon paratext inside the C3 late pole

The source attribution exposes one contaminant the trigram lens carries:
several strong late-pole trigrams feed measurably on **chapter-colophon
formulas** — 'hyā'/'dhy' from ('a)dhyāyaḥ, 'hāp' from mahāpurāṇe, 'ikā'
with śrīkālikāpurāṇe among top sources. Purāṇic chapter colophons
("iti śrī...mahāpurāṇe...adhyāyaḥ") are transmission paratext, not
composition language, and purāṇas have many short chapters while epics
have long ones — a systematic late-pole boost. Bounds: the W1 lens (0.95
agreement) is largely colophon-insensitive on its top loadings, and the
reuse-removal/exclusion robustness already limits how much any single
vocabulary stratum can carry. **Open item: a colophon-stripped corpus
variant** (regex on iti-śrī...adhyāyaḥ-type lines) to measure the
contribution directly — same harness as the no-space check.

## Files

`axis_anatomy/`: a2_bridge_c3_classes.py, class_signal_shares.tsv,
c3_trigram_sources.tsv (per-trigram junction/final/class shares),
w1_class_assignments.tsv (for the A2 review).
