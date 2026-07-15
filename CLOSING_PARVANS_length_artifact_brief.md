# Brief: why MBh 15–18 land at the "early" pole — and how to find out

**For:** a future Claude Code session working in `/Users/kengo_1/Desktop/stylometric_works`
**With:** Kengo Harimoto
**Status:** hypothesis + test plan. Nothing here has been run yet.

---

## 1. The observation

In the stylometric seriation of the 101-unit epic/purāṇa corpus (see
`materials/presentation_2026/`, deck `chronology_stratification.pptx`), the first MDS
axis reproduces the received relative chronology: epic core left, old purāṇic core
(Vāyu/Brahmāṇḍa/Viṣṇu/Mārkaṇḍeya) upper middle, digest purāṇas (Agni/Garuḍa/Nārada)
right, Bhāgavata displaced downward.

**The anomaly:** the closing parvans — MBh 15 (Āśramavāsika), 16 (Mausala),
17 (Mahāprasthānika), 18 (Svargārohaṇa) — sit at the *extreme left*, i.e. at the
"earliest" end, in practically every configuration. Often further left than MBh 6–9,
sometimes at the extreme of the whole corpus. They are coded **late epic** in the
received-chronology coloring, so this is a flat contradiction of the color scheme the
map is supposed to recover.

**Why this matters:** taken at face value the result says MBh 17 is stylistically
earlier than the Rāmāyaṇa core and earlier than the battle books. Nobody believes that,
Kengo included. The finding proves too much, which is the classic signature of an
artifact. But it may not be *purely* artifact, and the residual is philologically
interesting (§5).

---

## 2. Primary hypothesis: text length

MBh 16–18 are among the shortest units in the corpus by a wide margin.

| Unit | approx. size (CE) |
|---|---|
| MBh 17 (Mahāprasthānika) | 3 adhyāyas, ~100 ślokas → order of **1,000 running words** |
| MBh 18 (Svargārohaṇa) | 5 adhyāyas, ~200 ślokas |
| MBh 16 (Mausala) | 9 adhyāyas, ~270 ślokas |
| MBh 15 (Āśramavāsika) | ~1,060 ślokas — bigger, but still small for this corpus |
| **corpus mean unit** | 4.6M words / 101 units ≈ **45,000 words** |

Get the exact token counts from the pipeline; the point is the order of magnitude.
MBh 17 is roughly **2% of the mean unit size**.

### Mechanism (a): z-scores go to noise

For a function word with true rate *p* in a text of *N* tokens, sd(*f*) ≈ √(*p*/*N*).
For *ca* (*p* ≈ 0.02) at *N* = 2,000, the sampling sd is ~16% of the mean — plausibly
the same order as the *between-text* sd across the 101 units. So for MBh 16–18 the
per-feature z-scores that feed Burrows's Delta are roughly half sampling noise.

### Mechanism (b): noise → periphery, and the periphery is on the left

Noise inflates a unit's Delta to *everything*. In classical MDS on a corpus where
~75 of 101 units are purāṇic, the centroid sits deep in purāṇa-space and axis 1 is
substantially a *distance-from-the-bulk* axis. "Far from everything" therefore renders
as "far left" = "maximally epic" = "earliest." The displacement is directional even
though the noise is not.

### Mechanism (c): the features are expository filler, so genre loads onto axis 1

Slide 6 of the deck: the old purāṇic core uses *tu / eva / tathā / vai* 2–4× as often as
the epic core. These are the pāda-fillers of enumerative, doctrinal, list-making śloka —
which is why MBh 12–13 drift right. Books 16–17 are the most concentrated pure narrative
in the whole MBh: no frame-dialogue padding, no genealogy, no doctrine. On a
"density of expository filler" axis they belong at the far end **by genre, regardless of
date**. The deck already concedes this in the caveats slide (18); the closing parvans are
where the concession bites hardest.

### The robustness argument does not cover this

Deck slide 16 argues: a segmentation flaw could only distort the word lens; a sandhi
convention only the 3-gram lens; a quirk of one metric fails to explain the other five.
True — but **short length is a failure mode the two lenses share**. Worse, the 3-gram
lens is *more* fragile at short *N*, not less: 5,000 features over ~1,000 words leaves
most 3-grams with counts of 0–2. Agreement between the lenses on MBh 16–18 is therefore
not corroboration; it is two instruments failing the same way.

**This needs to be said out loud in the talk, or a hostile questioner will say it.**

---

## 3. Diagnostics, in order of decisiveness

### D1 — Length bootstrap (the decisive one)

Draw random *contiguous* samples of 1,000 / 2,000 / 5,000 / 10,000 words from units whose
true position is not in doubt — MBh 3, MBh 7, MBh 12, Vāyu, Agni — and push each sample
through the **identical** pipeline (both lenses, all metrics). Project the samples into the
existing MDS configuration, or refit and compare.

- **If 2,000-word chunks of the Śāntiparvan also drift left** → length explains it, full
  stop, and the closing parvans carry no chronological information at all.
- Use contiguous chunks, not random bags of words: contiguity preserves local register and
  is the honest analogue of a short parvan.
- ≥30 replicates per size per source text so the scatter is characterizable.

**Deliverable:** a panel showing axis-1 position vs. sample size, with the MBh 15–18
positions overplotted. This belongs in the robustness grid.

### D2 — Axis-1 position vs. log(N), all 101 units

Cheap. If there is a systematic relation at the short end, the axis is length-contaminated
and the deck must say so.

### D3 — Mean Delta to all others

Rank all 101 units by mean Delta to the rest. If MBh 16–18 are at the top (far from
*everything*, including each other), their MDS position is peripheral artifact, not
stratum.

**Sharpest single check:** *are MBh 16 and 17 each other's nearest neighbours?* They are
adjacent in transmission and narratively continuous. If they are not, their positions are
noise-driven and that is close to dispositive on its own.

### D4 — Merge test

Concatenate 15+16+17+18 (~1,600 ślokas) into one unit and rerun. Also try 16+17+18 alone
(the closing triad). If the merged unit lands near MBh 11/14 instead of beyond MBh 6–9,
length was doing the work.

### D5 — Feature-level attribution

For MBh 16 and 17, list the top-10 features by contribution to their displacement along
axis 1. Expect *tu / eva / vai / tathā* near zero. Then ask the honest question: are they
near zero because of *style*, or because at *N* ≈ 1,500 you would expect a handful of
tokens and got two?

### D6 — Rāmāyaṇa control

Do **Rām 1 (Bāla)** and **Rām 7 (Uttara)** also drift left? They are coded late epic and
they are *not* short. If the leftward drift is confined to the four short MBh units and
does not touch Bāla/Uttara, that is close to a clean demonstration that the cause is
length rather than the "late epic" coloring being wrong.

---

## 4. Interpretation table

| Outcome of D1/D3/D4 | Reading |
|---|---|
| Short chunks of MBh 12 / Vāyu also go left; MBh 16–18 have max mean-Delta; 16 and 17 not mutual NN; merged unit relocates | Pure length artifact. Exclude units below a size floor, or report them with an explicit uncertainty region. Say so in the talk. |
| Some drift remains after length is controlled; merged unit still sits left of MBh 6–9; 15 less displaced than 16–17 | **Residual signal — see §5.** |

---

## 5. If a residual survives: the interesting reading

Do **not** conclude "these books are early." Conclude:

> **Books 16–18 are late as *books* but redactionally thin as *text*.**

They are short precisely because nobody expanded them. The Brahmanical didactic overlay
that swelled MBh 12–14 and reshaped their particle habits never landed on the Mausala or
the Mahāprasthānika. On this reading, what axis 1 measures at the epic pole is not
antiquity but **absence of redactional overlay** — and low expository-particle density is
exactly what an unexpanded text looks like.

This *reconciles* the stylometry with the received "late epilogue" verdict (Brockington,
*The Sanskrit Epics* 1998, 153–54) rather than contradicting it. And it makes an
old-kernel argument respectable without claiming the parvans are early — which is exactly
the argument the comparative evidence supports:

- Lüders, "Die Jātakas und die Epik. I. Die Kṛṣṇa-Sage," *ZDMG* 58 (1904): 687–714
  (Ghata-Jātaka 454: an independent Yādava destruction cycle)
- Jacobi, "Die Jaina Legende von dem Untergange Dvāravatī's...," *ZDMG* 42 (1888): 493–529
- Tieken, "The Mahābhārata after the Great Battle," *WZKS* 48 (2004): 5–46
- Austin, "The Sārasvata Yātsattra in Mahābhārata 17 and 18," *IJHS* 12.3 (2008): 283–308
- Bronkhorst, "Archetypes and Bottlenecks," *Studia Orientalia* 110 (2011): 39–54 — note:
  **no Śāradā mss exist for MBh 13, 16, 17, 18**, so the constituted text of the closing
  parvans rests on a narrower and different manuscript base than the rest.

### Two experiments that would test the "redactional thinness" reading

**E1 — The apparatus experiment (potentially the novel result).**
Take the asterisked passages and appendix material that the Critical Edition *excludes*
from 15–18 (Belvalkar's volume) and add it back. If the books swing **rightward**, the
epic-pole position is a property of the *constituted* text — i.e. of redactional thinness
— and Belvalkar's apparatus has been turned into a measuring instrument. This is a real
paper. It also generalizes: the same test on MBh 13 (massively expanded, per Bronkhorst /
Reich) predicts the opposite gradient.

**E2 — MBh 15 vs 16–17 gradient.**
The Āśramavāsika has genuine didactic content (the āśrama frame, Vyāsa's discourse). If it
is *less* displaced than 16–17, the gradient tracks expository density, not date — which
supports §5 and rules out naïve archaism.

---

## 6. Practical notes for the session

- Reuse the existing pipeline end-to-end for D1; a bespoke re-implementation will not be
  comparable. Find the script that produced `figures/hero_W1_delta_MDS.png` and the
  robustness grid and drive the bootstrap through it.
- Both lenses, all six metric configurations, for every diagnostic — the whole point is
  that length is the one thing they *don't* disagree about.
- Keep the two parallel corpora (sandhied / unsandhied) straight; token counts differ
  between them, so the size floor must be computed per corpus.
- Ask Kengo for the exact per-unit token counts before assuming any of the śloka figures
  above.
- Target artefact: a **length-control panel** for the robustness grid, plus one sentence
  for the caveats slide. That is what he actually needs before the talk.

---

## 7. One-line summary

The closing parvans are not early; they are *short* and *unexpanded*, and the axis cannot
currently tell those two things apart from being old. Prove that with D1, then decide
whether E1 turns the weakness into the paper.
