# Closing parvans (MBh 15–18) at the epic pole: diagnostics run

**Date:** 2026-07-15
**Brief:** `CLOSING_PARVANS_length_artifact_brief.md` (test plan, hypotheses D1–D6, E1–E2)
**Scripts:** `scripts/presentation/closing_parvans_diag.py` (D2/D3),
`closing_parvans_bootstrap.py` (D1 + figure), `closing_parvans_d4d6.py` (D4/D6)
**Figure:** `materials/presentation_2026/figures/closing_parvans_length.png`
**Pipeline:** identical to the hero map (figcommon), Burrows's Delta, both lenses
(W1 top-80 words unsandhied / C3 top-5000 char-3-grams sandhied), aligned to hero.
Axis-1 sign: **negative = epic ("earliest") pole.**

## Exact sizes (unsandhied words)
MBh 17 = 1,050 · MBh 18 = 1,947 · MBh 16 = 2,962 · MBh 15 = 11,363.
Corpus mean unit ≈ 45k. So 16–18 are 2–7 % of a mean unit; 15 is mid-small.

## Result in one line
The extreme *individual* positions of MBh 16/17/18 are **not trustworthy** (they are
too short to resolve), **but the epic-pole placement itself is not a length artifact** —
it is a real register/redactional signal. Do **not** say the closing parvans are early;
say they are late-but-redactionally-thin (§5 of the brief). This is the interpretation-
table's *second* row, not the first.

## D1 — length bootstrap (decisive; the figure)
40 random contiguous windows × {1k,2k,5k,10k} words from securely-placed texts
(MBh 3/7/12, Vāyu, Agni), each projected onto the hero map. **Two failure modes
converge at short N:**
- **C3 lens: systematic leftward mean-drift.** Every source moves toward the epic
  pole as the window shrinks. Vāyu: +0.19 (10k) → +0.05 (1k); Agni: +0.30 → +0.10;
  MBh 12: −0.24 → −0.37. Monotone.
- **W1 lens: variance explosion, stable mean.** e.g. Agni mean stays ≈ +0.58 but
  sd 0.09 (10k) → 0.23 (1k) with individual 1k windows reaching −0.26; MBh 12 range
  at 1k = [−0.63, +0.49]. Short windows scatter across the whole axis.
Either way, at 1–2k words a securely-late text **cannot be distinguished from the epic
pole**. This is the failure mode the two lenses *share* (deck slide 16's robustness
argument does not cover it). MBh 16–18 (red stars) sit inside the 1–2k scatter; MBh 15
(4× longer) stands apart.

## D2 — axis-1 vs log(N), all 101 units
corr = −0.10 (W1), +0.21 (C3). Weak/inconsistent **globally** — as expected: length
bites only in the short tail, not linearly across the corpus. Not evidence either way
on its own; D1 is the right tool.

## D3 — isolation (mean Delta to the other 100) + nearest-neighbour test
- **Isolation tracks size.** MBh 17 is the single most isolated unit in the corpus
  (rank 1/101 W1, 3/101 C3); MBh 18 rank 4/4; MBh 16 rank 10/8; MBh 15 only 16/33.
  The top of the isolation list is dominated by tiny units (Bhaviṣya adh.5 N=820,
  Karatoyā N=1008, ŚiP Kārvaṇa N=2738, Vāyu Pāśupata N=3280) — the "short → far from
  everything → periphery" signature.
- **Mutual-NN (sharpest single check): MBh 16 and 17 are NOT mutual NN** despite being
  narratively continuous. W1: 16→Rām 6, 17→MBh 15, 18→MBh 2. C3: 16→MBh 1, 17→MBh 15,
  18→MBh 3. Their specific placements are noise-driven. (17→15 is the one stable edge.)

## D4 — merge test (**refutes pure length artifact**)
Concatenate the closing parvans and re-project:
| merged | W1 axis-1 | C3 axis-1 |
|---|---|---|
| 15+16+17+18 (~17k words) | −0.709 | −0.413 |
| 16+17+18 (~6k words) | −0.647 | −0.465 |
Reference full units (W1): MBh 6 −0.36, MBh 9 −0.48, MBh 11 −0.47, MBh 14 −0.55.
The merged block is no longer short, yet it **stays at the extreme epic pole** rather
than relocating to MBh 11/14. Length is not doing the work; a real residual survives.

## D6 — Rāmāyaṇa "control": WITHDRAWN as framed (see Kengo's correction below)
Numbers (W1): all seven Rām books cluster tightly at the epic pole, −0.49…−0.67
(Rām 1 −0.571 N=18,565; Rām 7 −0.673 N=26,063; Rām 6 −0.485 the least extreme).
The brief framed this as "long late-epic texts sit at the pole → not length." **Kengo
rejected the premise (2026-07-15):** the tight clustering of *all seven* khaṇḍas — 1
and 7 indistinguishable from the core 2–6 — is itself evidence that the khaṇḍa **texts
were composed at about the same time**, even though Books 1 & 7 were structurally *added
to Vālmīki's core* later. "Late addition to the core" (a redactional fact) ≠ "late
composition" (a stylistic fact); the stylometry sees only the latter and finds no gap.
So the Rāmāyaṇa books are **not** a "late" control, and calling them late is exactly the
received-chronology import a validation talk should avoid. D6 is dropped from the
argument. (Its one non-circular residue — that a genuinely *long* narrative text can
occupy the extreme pole — is already delivered by D1's mechanism and is not needed.)
Also note the size regime: the Rām khaṇḍas are all ≥15k words; the closing parvans are
1–3k, an order of magnitude smaller — so Rām's positional stability says nothing about
the sub-5k regime. That regime is exactly what D1 probes, which is why D1 is not
redundant with "just look at the Rāmāyaṇa."

## Synthesis (the reading to take to the talk)
The load-bearing evidence is **D1 + D4**, not D6:
- D1 → the *individual* positions of the sub-3k units MBh 16/17/18 are unresolvable
  (an uncertainty region, not a point).
- D4 → but the *merged* ~17k-word block stays at the pole, so the group's placement is
  a real signal, not length or noise.
Axis 1 at the epic pole measures **absence of expository overlay** (low `tu/eva/tathā/
vai` density — deck slide 6), which *correlates with* but is *not* early date. The MBh
closing parvans are narrative-pure end-matter that nobody padded with the Brahmanical
didactic layer that swelled MBh 12–14 — **late as books, redactionally thin as text.**
This **reconciles** the stylometry with the received "late epilogue" verdict
(Brockington 1998, 153–54) instead of contradicting it. (The Rāmāyaṇa is no longer part
of this argument — see D6.)

## Epic coloring change — DECIDED & IMPLEMENTED 2026-07-15
Kengo's call: **drop the chronological sub-coding of the epics entirely.** There is no
more "epic core" / "late epic" split. The epics are now coloured **by text**:
- stratum 1 = **Mahābhārata** (all 18 parvans; dark blue #1f5fa8)
- stratum 2 = **Rāmāyaṇa** (all 7 khaṇḍas; light blue #7ba7d4)
Rationale: MBh 15–18's extreme position is one of the most interesting findings, so the
map must not pre-encode a "late" verdict on any epic book — the position is a *finding*,
not an input. Purāṇa strata (3–10) are unchanged. `chronology_strata.tsv` updated;
`FLAG: tiny` notes on MBh 16/17/18 preserved (they still render as small dots).
Cascade done: corpus_labels.json + all figures regenerated + deck rebuilt.
Vertical map orientation was re-anchored on **Bhāgavata-low** (stratum 8) instead of
"epics-low", so redefining the epic strata no longer flips the map and the slides'
"Bhāgavata below" narration stays valid (hero_mds.py + figcommon.py).
Particle-habit slide (F3) multiplier recomputed for MBh-as-a-whole: old purāṇic core
uses tu/eva/tathā/vai ≈ 1.5–3× the Mahābhārata (was "2–4×" vs the narrower "epic core").

### Nuance to keep in mind (not acted on)
The all-in-one-region reading is a coarse-grain truth. At fine grain the *word* lens
makes **Bāla ↔ Uttara mutual nearest neighbours** (a distinct framing pair, not melted
into Rām 2–6), and the *3-gram* lens sends both Bāla and Uttara to **MBh 3**. So Rām 1/7
do resemble each other (and MBh) more than the core khaṇḍas — consistent with a
contemporaneous framing layer, but not proof the whole Rāmāyaṇa is one composition. The
coloring is deliberately agnostic about this; the tour-slide note states the NN facts
without a date claim.

Caveat that still must be stated in the talk: the *precise* extreme ranks of the four
short units are unreliable (D1/D3). Report them with an uncertainty region; do not
build any chronological claim on MBh 16/17/18 individually.

Mixed sub-result on E2 (MBh 15 vs 16–17 gradient): holds in C3 (15 least displaced of
the four: −0.41 vs 17's −0.56) but not W1 (15 most displaced, −0.72). Not headline-safe.

## Follow-ups not yet run (from the brief §5)
- **E1 apparatus experiment** (potential paper): add the CE-excluded asterisked/appendix
  material back into 15–18; if they swing rightward, the epic-pole position is a property
  of the *constituted* (thin) text and Belvalkar's apparatus becomes a measuring
  instrument. Predict the opposite gradient for the heavily-expanded MBh 13.
- Note (Bronkhorst 2011): no Śāradā mss for MBh 13, 16, 17, 18 — narrower ms base for
  the constituted closing parvans.

## Deliverable status
Figure `closing_parvans_length.png` is ready as a length-control panel / backup slide.
The caveats-slide sentence and whether to (a) exclude short units, (b) show an
uncertainty region, or (c) foreground the §5 reading is **Kengo's interpretive call** —
not yet wired into the deck.
