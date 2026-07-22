# Slide text draft — Chronological Stratification in the Epics and Purāṇas: Evidence from Stylometric Seriation

Draft for review before .pptx assembly. Conventions:

- **On slide** = text that appears on the slide (kept lean; the voice carries the rest).
- **Cue** = one-line speaker note, not slide text.
- Figures refer to `materials/presentation_2026/figures/`.
- All numbers from the 2026-07-10 runs (post-tokenization-fix), recomputed 2026-07-13:
  W1 = Burrows's Delta on top-80 words, unsandhied; C3 = Manhattan on top-5000
  character 3-grams, sandhied. Corpus median pair distance: 1.04 (W1), 0.49 (C3).

---

## Act 1 — The picture (slides 1–4, ~3–4 min)

### Slide 1 · Title

**On slide:**

> **Chronological Stratification in the Epics and Purāṇas**
> Evidence from Stylometric Seriation
>
> Kengo Harimoto
> *(DICSEP 11 · 4 August 2026)*

**Cue:** thirty seconds; straight into the picture.

### Slide 2 · The map

**Figure:** `hero_W1_delta_MDS` (full slide).

**On slide:** nothing beyond the figure and its built-in key.

**Cue:** let the audience find their texts. Point out: epics left, old purāṇic
core upper middle, sectarian digests right, Bhāgavata below. One color = one
stratum *of the received scholarly chronology*, not of the computation.

### Slide 3 · The claim

**On slide:**

> This map was drawn by **counting linguistic habits** — nothing else.
>
> - no dates
> - no chronology
> - no philological judgment
>
> entered the computation. The colors were painted on **afterwards**.
>
> Yet the familiar relative chronology reads left to right.

**Cue:** the coloring is the only place where received scholarship touches the
plot; the geometry is blind.

### Slide 4 · The question

**On slide:**

> Two questions worth thirty minutes:
>
> 1. **What** exactly was counted?
> 2. Can the left–right axis be **trusted** — or is it an artifact of one
>    method?

**Cue:** roadmap sentence: first how the map is made, then a guided tour, then
the robustness case, then honest caveats.

---

## Act 2 — How the map was made (slides 5–9, ~6–7 min)

### Slide 5 · The corpus

**On slide:**

> **100 texts and sections · ≈ 4.6 million words**
>
> - Mahābhārata by parvan (18) · Rāmāyaṇa by kāṇḍa (7)
> - purāṇas whole, or by khaṇḍa / saṃhitā where transmission demands it
> - machine-readable editions, cleaned; two parallel versions of every text —
>   with and without sandhi dissolved
>
> *Caveat kept in view: sections differ enormously in length; short fragments
> are marked with smaller dots on every map.*

**Cue:** one line on sources (e-text provenance); don't linger.

**Backup (if asked how the multi-part texts were divided):** four principles,
not one. (a) transmitted structural units — MBh parvans, Rām kāṇḍas, Bhāgavata
skandhas, khaṇḍas of Brahmāṇḍa/Garuḍa/Kūrma/Liṅga/Nārada, Śivapurāṇa saṃhitās;
(b) adhyāya ranges cut for this study (Matsya 1–32, Mārkaṇḍeya 1–93, SP
174–183, ViDhU 3.343–353); (c) thematic blocks of the Vāyupurāṇa, table below;
(d) whole texts. Note also that several works appear both whole *and* in parts
as separate points (Vāyu, Brahmāṇḍa, Bhāgavata, Devībhāgavata) — the parts are
plotted alongside the wholes, so e.g. Vāyu has eleven dots on the map. In the
Devībhāgavata's case the part is the **Devīgītā** (DBhP 7.31–40, plotted as
**DG**), which is also present inside the parent file from a second e-text; the
two transcriptions of the passage differ only in word division and agree to a
3-gram cosine distance of 0.014, so the duplication is textually harmless. See
B3 for why DG's apparent displacement from its host is nonetheless not
reportable.

**Backup — the ten Vāyupurāṇa sections.** Chapter numbering restarts at the
pūrvārdha/uttarārdha break, which is exactly the 05/06 file boundary. The cuts
all fall on transmitted adhyāya boundaries; only the *grouping* into ten blocks
is editorial. Parts sum to exactly the 73,540 words of the whole file, and the
colophon count matches (107 = 107), so the partition loses nothing.

| file | section | adhyāyas | words |
|---|---|---|---|
| V1 | frame and cosmogony | pūrv. 1–10 | 6,348 |
| V2 | **yoga / ascetic praxis** (see below) | pūrv. 11–20 | 2,262 |
| V3 | kalpas and Śiva lineages | pūrv. 21–33 | 8,956 |
| V4 | bhuvana-vinyāsa | pūrv. 34–49 | 6,784 |
| V5 | jyotiṣ and pūrvārdha close | pūrv. 50–61 | 9,041 |
| V6 | Pṛthu and Prajāpati lineages | utt. 1–9 | 9,104 |
| V7 | śrāddha-kalpa | utt. 10–22 | 6,757 |
| V8 | Manu, Candra, Viṣṇu vaṃśa | utt. 23–37 | 14,278 |
| V9 | upasaṃhāra | utt. 38–42 | 5,681 |
| V10 | Gayāmāhātmya | utt. 43–50 | 4,329 |

Caveat if pressed: the e-text carries 107 colophons where 111 chapters are
expected, and pūrv. 34 has none, so that one boundary is inferred from the
neighbouring files rather than read off directly. (Colophon spelling varies —
`vāyuprokte`, `vāyu prokte`, `vāyuprākte` — so searches must allow for it.)

**Backup — what is actually in V2.** The file name "pāśupata-yoga" is our
grouping label, not a heading of the text. The ten chapters colophon as:

| ch. | colophon title | words |
|---|---|---|
| 11 | **pāśupatayoga** | 428 |
| 12 | yogopasarga-nirūpaṇa | 260 |
| 13 | yogaiśvaryāṇi | 84 |
| 14 | **pāśupatayoga** | 259 |
| 15 | **pāśupatayoga** | 137 |
| 16 | śaucācāra-lakṣaṇa | 153 |
| 17 | paramāśrama-prāpti-kathana | 54 |
| 18 | yati-prāyaścitta-vidhi | 187 |
| 19 | ariṣṭāni | 322 |
| 20 | oṅkāra-prāpti-lakṣaṇa | 320 |

So the Pāśupata heading *is* in the text, on three chapters — 11, 14 and 15.
Rocher names 15, which is one of them. But those three are only **824 words,
37% of the unit**; the remaining 63% is general yoga, ascetic discipline,
penance, omens and oṃkāra. V2 is a yoga/ascetic-praxis block that contains
Pāśupata chapters, not a Pāśupata section.

*Record of a dropped claim (2026-07-22).* An earlier draft of Slide 12 paired
V2 with the Skandapurāṇa's Pāśupata chapters as two convergent jumps to the far
right. That is withdrawn, for two independent reasons. **Content:** V2 is 63%
non-Pāśupata (table above), so it is not comparable in kind to SP2, which is
Pāśupata doctrine throughout; and the three Pāśupata chapters cannot be
isolated and measured, since 824 words is far below the size at which a
position can be read. **Measurement:** under the same length control that SP2
passes, V2's position is marginal in the word lens (+0.723 against a null of
+0.256 ± 0.302 from the other nine Vāyu sections — 8% of windows reach it) and
*absent* in the 3-gram lens (+0.134 against a null of +0.109 ± 0.081 — the null
median, 50% of windows reach it). V2 is also the shortest Vāyu section and has
the 4th-highest mean Delta in the corpus, the
peripheral-artifact signature of D3. Mechanism is variance, not bias: same-size
control windows from Agni and MBh 12 drift only +0.08 and +0.05, so shortness
does not push a text rightward; it gives a 3,280-word unit a ±0.26 spread on an
axis the corpus spans in 1.53. Keep this in case the pairing is proposed again.

### Slide 6 · Style as unconscious, countable habits

**Figure:** `mfw_habits` (full slide).

**On slide:** figure only.

**Cue:** left: the features are *ca, tu, eva, na, sa, tathā…* — grammatical
glue, not content. Nobody composes with their rate of *tu* in mind. Right: the
old purāṇic core uses *tu, eva, tathā, vai* about 1.5–3× as often as the
Mahābhārata; the Bhāgavata suppresses all four. These boring words carry the
signal. Possibly the quality of the composers? Those words are very often supplied as fillers. The fewer uses might indicate the author not needing fillers. In that sense, the Bhāgavata's suppression of those words might suggest literary quality.

### Slide 7 · From counts to distances

**On slide:**

> For each pair of texts: **how differently do they use their most common
> words?**
>
> - similar habits → small number
> - different habits → large number
>
> Result: a **100 × 100 table of stylistic distances**
> (Burrows's Delta — the standard workhorse of stylometry, in use since 2002)
>
> | pair | distance |
> |---|---|
> | MBh 7 (Droṇa) ↔ MBh 8 (Karṇa) | 0.29 |
> | Vāyu ↔ Brahmāṇḍa | 0.29 |
> | *typical pair in this corpus* | *1.04* |
> | Rām 2 (Ayodhyā) ↔ Agni | 1.37 |

**Cue:** no formulas; "an average of disagreements in word habits, in units of
what is normal for this corpus." The table rows preview later stops on the tour.

### Slide 8 · Two independent lenses

**On slide:**

> The same corpus, measured twice:
>
> | | **Lens 1 — words** | **Lens 2 — letter groups** |
> |---|---|---|
> | counts | the 80 most frequent **words** | the 5,000 most frequent **3-letter sequences** |
> | input | sandhi **dissolved** (segmented) | raw **sandhied** text |
> | sees | particles, pronouns, vocabulary habits | morphology, phonology |
>
> **Independent failure modes**: nothing that could fool one lens can fool the other.

**Cue:** flag now, cash in at Act 4: any segmentation-pipeline artifact could
only touch Lens 1; any orthographic/sandhi artifact only Lens 2.

**Backup (if asked "what are the top 3-grams?"):** ␣ = space; trigrams run
across word boundaries. Shares are of all 30.5 M trigram tokens in the
sandhied corpus.

| | | | | |
|---|---|---|---|---|
| 1. `aṃ␣` 1.35% | 6. `āṃ␣` 0.46% | 11. `ya␣` 0.35% | 16. `tat` 0.32% | 21. `␣vi` 0.29% |
| 2. `aḥ␣` 0.89% | 7. `␣ca` 0.42% | 12. `␣pr` 0.35% | 17. `ata` 0.31% | 22. `ath` 0.28% |
| 3. `␣sa` 0.68% | 8. `am␣` 0.41% | 13. `āḥ␣` 0.34% | 18. `ama` 0.30% | 23. `bha` 0.28% |
| 4. `␣ta` 0.50% | 9. `ara` 0.38% | 14. `␣ma` 0.34% | 19. `␣bh` 0.30% | 24. `ava` 0.27% |
| 5. `ca␣` 0.50% | 10. `ḥ␣s` 0.36% | 15. `pra` 0.32% | 20. `ḥ␣p` 0.29% | 25. `yat` 0.26% |

The answer that matters: these are **not words**. The top of the list is
inflectional endings (`aṃ␣ aḥ␣ āṃ␣ am␣ āḥ␣` — accusative and nominative
terminations) and sandhi junctions (`ḥ␣s ḥ␣p` — visarga before a following
sibilant or stop). That is Lens 2 doing exactly what the slide claims:
morphology and phonology, not vocabulary. Only a handful of the top 25
(`␣ca ca␣ tat yat`) overlap with Lens 1's particles.

Depth of the feature set, if pressed: 19,320 distinct trigrams occur; the 5,000
we keep cover 98.4% of all tokens. Rank 100 is `dev` (0.148%), rank 1,000
`ñān` (0.024%), rank 5,000 `mīm` (0.001%, 322 occurrences) — so the tail is
genuinely rare material, and the cut is not arbitrary-looking.

### Slide 9 · From a distance table to a map

**Figure:** `mds_explainer` (full slide).

**On slide:** figure only.

**Cue:** the mileage-chart analogy — given only road distances between cities
you can redraw the map of India. MDS does exactly that with stylistic
distances. The opening map is this, with the full 100 × 100 table. The axes
mean nothing by themselves; only *nearness* does.　You can rotate the map as much as you like.

---

## Act 3 — Reading the map (slides 10–15, ~8–9 min)

*(Slides 10–15 reuse the hero figure with the relevant zone highlighted /
zoomed; highlight variants to be generated at assembly time.)*

### Slide 10 · The epic zone

**On slide:**

> - battle books **MBh 6–9** cluster tightly — Droṇa ↔ Karṇa the tightest
>   pair (0.29 ≈ ¼ of a typical distance)
> - **MBh 12–13** (Śānti, Anuśāsana): mutual nearest neighbours — and drifted
>   toward purāṇa-space...
> - **Rām 2–6** hold together; **Bāla(R1)'s nearest neighbour is the Uttara(R7)...** —
>   in both lenses
>
> *The stratification of higher criticism, recovered blind.*

**Cue:** the machine has read no Hopkins and no Brockington, yet finds the
didactic parvans late and the frame kāṇḍas apart from the core. (Precision for
Q&A: Bāla↔Uttara is mutual in the word lens; in the 3-gram lens Bāla's NN is
Uttara, Uttara's is MBh 3.)

### Slide 11 · The old purāṇic core?

**On slide:**

> - **Vāyu ↔ Brahmāṇḍa: 0.29** — a quarter of a typical distance.
>   Kirfel's single *Vāyuproktaṃ Purāṇam*, as a number.
> - **Viṣṇu ↔ Mārkaṇḍeya**: mutual nearest neighbours, in both lenses
> - Matsya's cosmogonic chapters sit with them

**Cue:** the philology (Kirfel 1927) predicted this cluster a century ago; the
counting confirms it without being told. The Vāyu∩Brahmāṇḍa common-material
extract (V×B on the map) sits closest of all to both. V2, chapters on yoga, is in far right. As tempting as it is to suspect something may be behind, it turns out that it is there because it is short. A test (examining whether as short texts as V2 from the rest of the Vāyu can be as in far right as V2) confirmed that.

### Slide 12 · The old Skandapurāṇa: mostly old but Pāśupata yoga added later

**On slide:** figure `hero_W1_delta_MDS_hl-oldsp` (old SP highlighted).

> - the **old Skandapurāṇa** (Nepal/Bengal recension, oldest MS 811 CE) sits
>   **between the epics and the old purāṇic core** (axis-1 ≈ −0.3)
> - word lens: its nearest neighbours are **MBh 1, MBh 10 and Rām 6** — it keeps
>   epic diction
> - but its **Pāśupata section (SP2) jumps far right** (axis-1 ≈ +0.48), out
>   among the sectarian digests

**Cue:** a single work, stratified in front of the audience. The narrative body
is a genuine bridge between epic and purāṇa (in the 3-gram lens it shifts toward
Matsya/Brahma, the old core); the Pāśupata doctrinal chapters land at the far
right with the Śivapurāṇa (Umā, Sanatkumāra) as their word-lens neighbours — a
sectarian register inside an early text.

Caveat for Q&A: SP2 is a short excerpt, so its exact position is soft, but the
direction of the jump is unmistakable — and it survives a length control.

**Length control, run 2026-07-22 (`scripts/presentation/pasupata_length_control.py`).**
Method = D1 of the closing-parvans brief: contiguous windows of SP2's exact size
drawn from the *rest* of the Skandapurāṇa, pushed through the identical pipeline
and projected onto the hero map — a null for "where does a random short stretch
of this text land?"

| | observed axis-1 | null (same N, rest of SkP) | verdict |
|---|---|---|---|
| **SP2**, W1 | +0.481 | −0.313 ± 0.263 | +3.0 sd, 2% of windows reach it |
| **SP2**, C3 | +0.126 | −0.071 ± 0.069 | +2.9 sd, 2% of windows reach it |

Both lenses agree, at ~3 sd each, so the jump is not a shortness artifact. Say
this in one sentence if the length objection comes from the floor; the numbers
are here if pressed.

**Live cue:** mention the forthcoming edition of the Pāśupata-yoga chapters —
the lenses flag exactly what its editors suspected.

### Slide 13 · The sectarian & encyclopedic mass

**On slide:**

> - one broad, continuous stratum — **no clean line** between "middle" and "late"
> - **Agni · Garuḍa · Nārada**: the encyclopedic digests, crowded on the far right
> - internally **blurry** — exactly what compilation literature should look like

**Cue:** folded into one group on purpose. On the map the old boundary between
"middle purāṇic" and "late sectarian/encyclopedic" does not survive — the two
overlap heavily on axis 1 (medians +0.05 vs +0.21, ranges swamping the gap) and
the split rested on external dating and genre, not on the counts. The stratum
shades from texts still close to the old core (Kūrma, Liṅga, Viṣṇudharmottara)
out to the self-quoting digests at the right, where the style is simply the
style of the digest.

### Slide 14 · A purāṇa that refuses to unify

**On slide:**

> The **Śivapurāṇa**, plotted saṃhitā by saṃhitā:
>
> - its seven saṃhitās **scatter across the late zone**
> - only 3 of 8 sections (word lens; 4 of 8 in the 3-gram lens) have their
>   nearest neighbour inside the Śivapurāṇa
>
> *Compare the Bhāgavata on the next slide — cohesion is measurable.*

**Cue:** the compilation model of the ŚiP, confirmed from word counts alone;
contrast set up deliberately.

### Slide 15 · The Bhāgavata

**On slide:**

> The **Bhāgavatapurāṇa**, plotted skandha by skandha:
>
> - **all twelve skandhas' nearest neighbours are internal** — in both lenses
> - a single stylistic island, despite its deliberately archaizing,
>   Vedicizing Sanskrit
>
> *Archaism is a costume; habit is a fingerprint.*

**Cue:** the BhP tries to sound ancient — and fools no counter of particles.
Its position (below, not left) shows the second axis at work: it is *unlike*
everything, not *early*.

---

## Act 4 — Why believe the axis? (slides 16–18, ~5 min)

### Slide 16 · The same map from six different measurements

**Figure:** `robustness_grid` (full slide).

**On slide:** figure only.

**Cue:** walk the grid: top row words/unsandhied, bottom row 3-grams/sandhied,
three distance metrics each — six independent analysis pipelines, one geometry.
Layout agreement with the opening map: 0.95–0.96 (words), 0.82–0.89 (3-grams).
The epic→purāṇic axis survives every change of lens.

### Slide 17 · The convergence argument

**On slide:**

> Suppose the axis were an **artifact**:
>
> - a flaw in sandhi **segmentation** → could distort the **word** lens only
> - an **orthographic / sandhi** convention → could distort the **3-gram**
>   lens only
> - a quirk of one **distance formula** → fails to explain the other five
>
> The lenses share almost no assumptions — yet draw the same axis.
>
> **The signal is in the texts.**

**Cue:** this is the abstract's core argument; deliver slowly.

### Slide 18 · What the second axis is *not*

**On slide:**

> The vertical axis is **unstable** across configurations.
>
> Depending on features and metric it separates by something like **genre**,
> **region**, or **sectarian register** — no labeling survives all six panels.
>
> Honest conclusion: **one axis is chronology-like and robust; the second
> resists a stable name.**

**Cue:** promised in the abstract; agnosticism as a feature, not a weakness.
The Bhāgavata's vertical displacement is the clearest case.

---

## Act 5 — Caveats and implications (slides 19–21, ~3–4 min)

### Slide 19 · What the axis is made of

**On slide:**

> "Diachronic linguistic drift" — but **confounded**:
>
> - **metre**: the favourite particles are anuṣṭubh fillers; particle habits
>   are partly versification habits
> - **borrowing**: the tightest links ride on shared ślokas — Delta cannot
>   tell "same school" from "copied the same 2,000 verses"
> - **genre**: narrative vs. didactic vs. digest

**Cue:** drift, metre, borrowing and genre are entangled *in the texts
themselves*; the axis is real but not purely temporal.

### Slide 20 · What this is — and is not

**On slide:**

> - Purāṇas have **no authors** → this is **stratum and textual-family
>   detection**, not authorship attribution
> - Stylometry offers an **independent, replicable check** on relative
>   chronology — a third witness beside content criteria and testimonia
> - It will not date your text; it will tell you **whose company it keeps**

**Cue:** position the method modestly; invite collaboration on specific
text-historical problems.

### Slide 21 · Closing

**Figure:** `hero_W1_delta_MDS` again (full slide).

**On slide (one line over the figure):**

> *Counted habits, familiar history.*

**Cue:** end where we began — now everyone can read the map. Thanks; over to
questions.

---

## Backup slides (Q&A)

### B1 · Burrows's Delta, one level deeper

**On slide:**

> - for each of the top-80 words: how far is each text from the **corpus
>   average** rate, in standard deviations (a *z*-score)?
> - Delta(A, B) = the **average disagreement** of A and B across those words
> - variants used in the grid: Cosine Delta (angle instead of average),
>   min-max and Manhattan (raw-frequency geometry)

### B2 · The full corpus with strata

**On slide:** the 100-text table from `chronology_strata.tsv`, 9 strata,
two columns. *(Rendered at assembly time; likely two slides.)*

### B3 · The length caveat

**On slide:**

> - sections range from a few thousand to hundreds of thousands of words
> - short sections have noisy profiles → inflated distances, positions
>   unreliable
> - marked as **small dots** on every map; none of the argument rests on them

**Cue — the floor, with a number.** Draw random contiguous windows of a given
size from a text whose position is secure, run them through the identical
pipeline, and see how far they scatter on axis 1 (D1 of the closing-parvans
brief; `scripts/presentation/pasupata_length_control.py`). The corpus spans 1.53
on that axis. A 5,238-word window of the **Devībhāgavata** lands anywhere from
−0.80 to +0.78 (sd 0.40) — *half the map*. A 3,280-word window of the Vāyu
scatters ±0.30. So the honest floor is higher than the "5k" rule of thumb: for a
stylistically heterogeneous host, even a 5k section carries an uncertainty of
roughly a fifth of the axis.

Crucially the mechanism is **variance, not bias** — same-size control windows
from Agni and MBh 12 drift only +0.08 and +0.05, so shortness does not push a
text in any particular direction. It just widens the error bar. This is why a
short section landing somewhere surprising is not evidence, and why SP2 (Slide
12), which clears its null by ~3 sd in *both* lenses, is.

**Record of two ideas tested and dropped (2026-07-22).** Both were short
sections that looked displaced from their host and turned out not to be.
**Vāyu V2** — see the note under Slide 5. **Devīgītā** (DBhP 7.31–40, plotted as
DG): sits at axis-1 +0.271 against its parent's −0.113, which looks like a
doctrinal insert detaching from its narrative host — exactly the Slide 12
phenomenon. But against a null of windows drawn from the rest of the DBhP it is
only +0.75 sd out in the word lens (27% of windows reach it) and +1.22 sd in the
3-gram lens (13%). The Devībhāgavata is simply too heterogeneous internally for
a 5k section to be locatable. Worth knowing that the Devīgītā *is* a clean,
self-contained unit textually — it just cannot be shown to be stylistically
distinct at this length. (Minor: in the word-lens run the donor pool was the
full parent, since the excision anchors matched only the sandhied file; the
Devīgītā is 2.3% of the parent, so the effect is negligible.)

### B4 · When the lenses disagree — a diagnostic, not a failure

**On slide:**

> **BhP 10.29–33 transmitted with commentary** (Bh10c on the maps):
>
> - **word lens**: nearest neighbour = Kāśīkhaṇḍa — expelled from the
>   Bhāgavata cluster (commentary vocabulary contaminates word counts)
> - **3-gram lens**: nearest neighbour = BhP 10 — back inside the family
>
> Disagreement between lenses **flags preprocessing problems** — it does not
> hide them.

**Cue:** if asked about pipeline trust: same story with the Nīlamata, where a
raw-cosine outlier exposed an editorially dissolved source text (2026-07-09).

### B5 · Consensus tree

**On slide:** figure `consensus_tree` — bootstrap consensus tree, Cosine Delta
on the same 80 words, 500 replicates (words resampled with replacement),
neighbour-joining per replicate, majority-rule consensus; rooted on MBh 6,
leaves colored by stratum. 27 branches survive the ≥ 50% cut, mean support
0.76.

**Cue:** for anyone who wants a stemma-shaped answer. The tree recovers the
same groups as the map — the epics, Vāyu–Brahmāṇḍa with the old purāṇic
core, the Bhāgavata, the Śivapurāṇa — so the grouping is not an artefact of
the MDS projection. But a tree asserts descent and nesting, and these texts
drift into one another rather than branching cleanly; the gradual transitions
that carry the chronological argument are exactly what a tree has to hide.
That is why the talk is built on the map. *(Built by
`scripts/presentation/consensus_tree.py`; stylo's own BCT is unusable — the
50–80 MFW range leaves the 0.5-consensus a near-total polytomy.)*

---

## Timing budget

| Act | slides | minutes |
|---|---|---|
| 1 The picture | 1–4 | 3–4 |
| 2 How it was made | 5–9 | 6–7 |
| 3 Reading the map | 10–15 | 8–9 |
| 4 Robustness | 16–18 | 5 |
| 5 Caveats & close | 19–21 | 3–4 |
| **total** | **21** | **~26 + 5 Q&A** |
