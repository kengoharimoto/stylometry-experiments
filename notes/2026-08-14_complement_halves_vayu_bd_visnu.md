# Shared vs unique halves of Vāyu / Brahmāṇḍa / Viṣṇu on the drift axis

2026-08-14. Follow-up to `2026-08-14_mfw_robustness_noreuse.md` and the
question whether the Vāyu(-prokta) purāṇa is genuinely old or merely
*contains* old, much-reused material (the PPL). The noreuse build keeps each
unit's unique residue; this experiment reconstructs the removed material as
standalone "shared" units and places **both halves of each unit** on the
canonical drift map.

## Build

`scripts/build_complement_units.py`: for 20 units (Vāyu sections 1–10 +
Revākhaṇḍa, Brahmāṇḍa khaṇḍas 1–3, Viṣṇu aṃśas 1–6), the shared half =
lines of the sandhied original whose cstream is absent from the sandhied
noreuse file — byte-exact reconstruction of what `build_noreuse_corpus.py`
dropped (verified: kept + shared = original for every unit). Source-level
counterparts recovered by subsequence walk, then unsandhied with the local
ByT5 pipeline (`EPIC_INPUT_DIR=corpus/complements_src ... unsandhi_local.sh`)
into `corpus/complements_unsandhied/`. Note "shared" = matched against *any*
other family (for Vāyu that is mostly the Vāyu↔Brahmāṇḍa common text, PPL
parallels included), not PPL-parallels only.

## Placement: supplementary projection into the fixed map

`materials/presentation_2026/figures/complement_halves/project_halves.py`:
base map = the sweet-spot map (Burrows's Delta, MFW 500, manifest
`dicsep2026_n127_ppl`, W1 unsandhied / C3 sandhied), reproduced exactly
(r = 1.0000 vs the saved sweep coordinates). Each half is profiled on the
base features, z-scored with the **base** mean/std, and projected by Gower's
supplementary-point formula — the base map is untouched, and the projection
is invariant to a uniform inflation of squared distances, which is exactly
the artifact small samples produce under Delta. Self-projection of a base
text reproduces its coordinates to numerical zero.

## Result: the halves nearly coincide on the drift axis

Percentile of x on the 127-text base map (whole / residue / shared):

| unit | W1-500 | C3-500 |
|---|---|---|
| V1 frame-cosmogony | 79 / 82 / 78 | 94 / 87 / 96 |
| V2 pāśupata-yoga | 93 / 87 / 95 | 97 / 94 / 99 |
| V3 kalpas-śiva-lineages | 52 / 48 / 52 | 67 / 62 / 68 |
| V4 bhuvana-vinyāsa | 71 / 63 / 79 | 81 / 79 / 83 |
| V5 jyotis | 71 / 63 / 72 | 87 / 79 / 89 |
| V6 pṛthu-prajāpati | 47 / 42 / 47 | 70 / 65 / 71 |
| V7 śrāddha-kalpa | 82 / 81 / 82 | 90 / 82 / 91 |
| V8 manu-candra-viṣṇu-vaṃśa | 24 / 28 / 24 | 45 / 38 / 47 |
| V9 upasaṃhāra | 79 / 72 / 76 | 93 / 71 / 96 |
| V10 gayā-māhātmya | 83 / 79 / 86 | 76 / 73 / 80 |
| V Revākhaṇḍa | 63 / 61 / 67 | 66 / 60 / 73 |
| Bḍ1 | 65 / 63 / 63 | 85 / 91 / 83 |
| Bḍ2 | 35 / 30 / 36 | 56 / 53 / 59 |
| Bḍ3 | 63 / 62 / 76 | 84 / 82 / 94 |
| Vi1–Vi6 (range) | whole 27–85, halves within ±17 | whole 33–79, halves within ±14 |

Figure: `complement_halves_MDS.{png,pdf}` in the same directory — the
resid↔shared segments are short and mostly *vertical*; the drift axis barely
distinguishes the halves.

## Reading

1. **Each unit's shared and unique material speak with nearly the same
   voice on the drift axis.** Differences are 0–9 percentiles for most units
   (max 17), with the shared half trending slightly *later*, not earlier —
   most consistently on C3. There is no old-shared-core-plus-late-additions
   split *within* these units.
2. **This corrects the reading of the noreuse-map shifts** in
   `2026-08-14_mfw_robustness_noreuse.md`: the dramatic residue movements
   there (V8 jumping 24→75 on W1) do not survive the fixed-space instrument.
   Those were effects of recomputing features and z-stats on a corpus of
   gutted units, not properties of the texts. For layer questions, use
   fixed-space projection; use recomputed maps only for whole-corpus
   robustness checks on adequately sized units.
3. **The Vāyu-as-oldest question**: the answer sharpens. The Vāyu is late-ish
   on the drift axis *in both of its layers* — its unique verses and its
   shared verses alike sit at the 47–97th percentile for every section except
   the vaṃśa block (V8: 24–28 W1, both halves), with V6/V3 middling. Its
   apparent antiquity cannot be rescued by blaming late unique additions;
   only the genealogical core patterns early, and that in both halves.
   Meanwhile the constituted PPL Textgruppen I/II sit at percentile 22–43.
   Caveat for V8: vaṃśa lists are a particle-poor genre — some of its early
   placement may be register, not date; the genre control remains to be run.
4. Bḍ2 remains the earliest-styled Brahmāṇḍa khaṇḍa in both halves; the
   Viṣṇu aṃśas are heterogeneous (Vi5 early, Vi3 late) with halves agreeing.

## Next

- Split each shared half by counterpart family (PPL-parallel vs Vāyu↔Bḍ vs
  other) — the PPL question proper needs the PPL-parallel subset isolated.
- Bootstrap CIs (feature + verse resampling) on projected positions,
  especially for the thin residues (V5 residue: 460 sandhied words).
- Genre control for list/vaṃśa material.
