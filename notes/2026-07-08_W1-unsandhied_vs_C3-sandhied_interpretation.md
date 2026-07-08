# Interpretation notes: W1 unsandhied vs. C3 sandhied (epic_puranas corpus)

**Date:** 2026-07-08
**Analyses compared:**

| Run | Corpus | Features | MFW/MFC range | Result directory |
|---|---|---|---|---|
| W1 | `corpus/epic_puranas_unsandhied` (101 texts) | word unigrams | 50–80 by 10, culling 0% | `results_epic_puranas_unsandhied_W1_50-80_20260708_151314/` |
| C3 | `corpus/epic_puranas_sandhied` (101 texts, same set) | character 3-grams | 2000–5000 by 1000, culling 0% | `results_epic_puranas_sandhied_C3_2000-5000_20260708_152435/` |

Both run through `scripts/clusters.R` (stylo 0.7.5), 10 distance measures × CA/BCT/MDS + PCV.
Observations below are based on the wurzburg (Cosine Delta) BCT plots and on
nearest-neighbor (NN) extraction from the distance tables (W1 @ 80 MFW,
`distance_table_80mfw_0c.txt`; C3 @ 5000 MFC, `distance_table_5000mfw_0c.txt`).

---

## 1. Headline: the two feature sets largely agree

The most important methodological finding. The feature sets are nearly orthogonal
in what they measure — unsandhied word unigrams capture function-word/particle
usage after the unsandhi segmentation pipeline; sandhied character 3-grams capture
morphology, phonotactics, and sandhi habits on raw text with *no* segmentation.
Yet the macro-clusters replicate in both:

- **MBh parvans** cohere, with identical internal structure: battle books 6–9
  form a sub-block (7↔8 tightest: 0.112 W1 / 0.133 C3), 12↔13 pair off,
  1–3–14 group together.
- **Rāmāyaṇa kāṇḍas** cohere, and in *both* analyses Bālakāṇḍa's NN is
  Uttarakāṇḍa (0.197 / 0.240).
- **Bhāgavata skandhas** form a tight, isolated block in both.
- **Vāyu ↔ Brahmāṇḍa** almost fused (0.085 / 0.080 — the smallest distances in
  either table).
- Replicating pairs/trios: **Agni–Garuḍa(kh.1)–Nārada(kh.1)**; **Kūrma 1↔2**;
  **Liṅga 1↔2**; **ŚiP Dharma↔Sanatkumāra**; **ŚiP Vāyavīya↔Vidyeśvara**.

Any artifact of the unsandhi pipeline could only affect W1; any
orthographic/sandhi artifact only C3. Convergence therefore means the signal is
in the texts, not in the preprocessing.

## 2. Agreement with known philology (sanity checks pass)

- **Bāla ↔ Uttara** (Rām 1 NN = Rām 7 in both): matches the consensus that
  books 1 and 7 are later additions to the core Rām 2–6. Arguably the prettiest
  single result in the data.
- **Vāyu ↔ Brahmāṇḍa** at 0.08: Kirfel's common-ancestor thesis (the
  *Vāyuproktaṃ Purāṇam*) as a number. The thematic Vāyu sections 01–09 all point
  back into the Vāyu/Brahmāṇḍa block; Vāyu 08 (Manu-Candra-Viṣṇu-vaṃśa) → Brahmāṇḍa
  kh. 2, exactly where the texts run parallel. *Caveat:* at this distance much of
  the similarity is literally shared verses (textual identity, not merely
  stylistic kinship). Also: if `vayu_ba` and `vayupurana` are two editions of the
  same text, one pseudo-replicates the other and should be dropped.
- **The two Revākhaṇḍas find each other** (0.182 / 0.208): the double
  transmission under Skanda's and Vāyu's names, recovered blind by both feature
  sets.
- **Brahmapurāṇa ↔ MBh 13 Anuśāsana** (NN in C3, 0.191; second in W1, 0.161):
  the Brahmapurāṇa's heavy borrowing from the epic, and the epic-purāṇic didactic
  register of MBh 12–13. Relatedly, MBh 12–13 lean toward purāṇa-space rather
  than the battle books — consistent with Śānti/Anuśāsana as late didactic strata
  contemporaneous with early purāṇic composition.
- **Matsya adhy. 176 ↔ Brahmāṇḍa** in both: pañcalakṣaṇa-parallel material
  (Kirfel's Matsya–Vāyu–Brahmāṇḍa group).
- **Viṣṇu ↔ Mārkaṇḍeya** mutual NNs in C3 (0.207): both usually placed in the
  older core stratum of the genre.
- **Śivapurāṇa is not a stylistic unit.** Its saṃhitās scatter as a compilation
  model predicts: Umāsaṃhitā sits with Brahmāṇḍa/Vāyu (it demonstrably shares
  material with that corpus); Rudrasaṃhitā pairs with Devībhāgavata;
  Dharma↔Sanatkumāra and Vāyavīya↔Vidyeśvara form their own pairs. Stylometry
  independently refuses to reunify the ŚiP — a real observation about its
  redactional heterogeneity.
- **The Bhāgavata stands alone.** All twelve skandhas' NNs are internal to the
  BhP in both analyses; nothing else in the 101-text corpus comes near. Its
  deliberately archaizing, Vedicizing style is *sui generis* — consistent with
  the single-author/single-milieu hypothesis, and the internal cohesion (even
  prose-heavy skandha 5 stays inside) supports compositional unity over
  accretion. The model is not fooled by the archaizing imitation of the old core.

## 3. W1 / C3 disagreements — diagnostic, not noise

- **`bhagavatapurana_skandha-10_adhyaya-29-33_w_commentary`**: W1 sends it to
  Kāśīkhaṇḍa (0.318!); C3 correctly reattaches it to BhP skandha 10 (0.332).
  The commentary prose dominates the word-unigram profile (śāstric particles,
  *iti*, *evam*, etc.) while the mūla's phonic texture survives in character
  3-grams. Lesson: commentary contamination distorts word-level features far more
  than character-level ones. → this file should be excluded or cleaned.
- **`devibhagavatapurana_u` vs `devibhagavatapurana`**: C3 pairs them (0.327);
  W1 sends `_u` to Saura/Kālikā first. If `_u` is partial or differently
  processed, the unsandhi step may be shifting its word profile.
- **Ayodhyākāṇḍa (`_a`)**: NN is MBh Āraṇyakaparvan in both runs, not another
  Rām kāṇḍa. Could be genuine (epic register of the core Rām), but both
  `ramayana_02_a` and `ramayana_03_a` carry an `_a` suffix — if they come from a
  different edition/source, source-specific orthography may be leaking in.
  → worth checking provenance.

## 4. Validity caveats

1. **50–80 MFW in śloka texts ≈ particles and metrical fillers** (*ca, tu, hi,
   eva, caiva, tathā, atha…*). Exactly the function words Delta theory wants,
   but in anuṣṭubh they double as metre-fillers — part of what clusters is
   metrical habit and genre register, not authorship. The epic-vs-purāṇa
   separation is partly a genre effect.
2. **Purāṇas have no authors.** These are multi-layer compilations; stylometry
   recovers at best the redactional register of the final transmitted text. The
   method is being used for textual-family detection, not authorship attribution
   — legitimate, but interpretation must shift accordingly.
3. **Borrowing ≠ stylistic kinship.** The tightest links (Vāyu–Brahmāṇḍa,
   Revākhaṇḍas, Brahmapurāṇa–MBh 13) are substantially driven by shared verses.
   Delta cannot distinguish "same school" from "copied the same 2,000 ślokas."
4. **Severe length imbalance** — 122-line fragments against 40,000-line texts.
   Everything under a few thousand words (Bhaviṣya Brahmaparvan adhy. 5,
   Karatoyāmāhātmya, Nīlamata, MBh Mausala/Mahāprasthānika/Svargārohaṇa,
   SP Pāśupata excerpt, Praṇavakalpa) has inflated NN distances (0.3–0.5) and
   drifts toward the center of the BCT star. The unresolved central burst in the
   radial plots is this: only tight clusters survive 0.5 consensus; the rest is
   honest agnosticism, not evidence of isolation.
5. **Mixed sources** (`_iast`, `_pu`, `_au`, `_u` suffixes) can inject
   orthographic signal, especially into C3. The W1/C3 convergence is the best
   defense and mostly holds — but the `_a` Rāmāyaṇa files and the commentary
   file show where it leaks.

## 5. Summary picture

The corpus resolves into:

1. an **epic zone** with internal chronology visible (battle-books core vs.
   didactic MBh 12–13 vs. frame books; Rām core 2–6 vs. late 1+7);
2. an **old purāṇic core** — Vāyu/Brahmāṇḍa/Matsya-parallels/Viṣṇu/Mārkaṇḍeya —
   held together partly by genuine shared ancestry of the pañcalakṣaṇa type;
3. a **later sectarian-encyclopedic zone** (Agni–Garuḍa–Nārada digests;
   Bhaviṣya–Devībhāgavata; the scattered Śivapurāṇa saṃhitās);
4. the **Bhāgavata as deliberate outsider** — stylometric evidence for its late,
   unitary, literary character.

Broad agreement with 20th-c. philology (Kirfel, Hazra, epic higher criticism),
obtained from two independent feature sets — one of which never saw a word
boundary — validates that Delta-family methods transfer to Sanskrit. The caveats
concern *interpreting* clusters (borrowing, genre, metre, length), not whether
they are real.

## 6. Next steps

- Drop the sub-5k-word fragments and the duplicate Vāyu (`vayu_ba` or
  `vayupurana`), clean/exclude the commentary-contaminated BhP 10.29–33 file,
  and re-run.
- Run a culled analysis (e.g. culling ≥ 50%) to suppress the borrowed-passage
  effect and isolate register from parallels.
- Check provenance of the `_a` Rāmāyaṇa files (02, 03).
