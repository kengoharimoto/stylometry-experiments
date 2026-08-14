# Stratigraphy inside the reused material: shared halves split by counterpart family

2026-08-14. Continuation of `2026-08-14_complement_halves_vayu_bd_visnu.md`.
The shared half of each Vāyu / Brahmāṇḍa / Viṣṇu unit is now partitioned by
*which family* each dropped line matched, giving three layers per unit:

- **ppl** — lines matching a kirfel unit (PPL-parallel; may also match others)
- **vayubd** — lines matching inside the Vāyu/Brahmāṇḍa complex
  (vayupurana, brahmandapurana, vayu_ba families), no kirfel match
- **other** — lines matching only other families

## Method

`complement_halves/attribute_families.py` re-runs the matching of
`build_noreuse_corpus.py` exactly (cstream units, 8-char shingles, df ≤ 400,
≥ 2 shared rare shingles, rapidfuzz ≥ 70, cross-family only), restricted to
the 20 target units, recording matched counterpart families per line.
Validation: **every** complement line re-matched (0 misses in all 20 units) —
the partition is exhaustive. Subset files:
`corpus/complements_sandhied/<unit>_shared_{ppl,vayubd,other}.txt` (+ the
per-line map in `corpus/complements_sandhied/attribution.tsv`), source-level
counterparts partitioned by the same cstream mapping
(`partition_src.py`) and ByT5-unsandhied into `corpus/complements_unsandhied/`.
All subsets projected into the fixed sweet-spot maps (W1-500 / C3-500,
manifest `dicsep2026_n127_ppl`) by the same Gower supplementary projection
(`project_subsets.py`; base map reproduced at r = 1.0000). Results:
`subsets_{W1,C3}_500.tsv`, figure `subset_layers_dotstrip.{png,pdf}`.

The PPL-parallel material concentrates exactly where the pañcalakṣaṇa
predicts: V1 cosmogony (4.0k sandhied words), V6 pṛthu–prajāpati (3.8k),
V8 vaṃśas (10.1k), Bḍ1 (7.0k), Bḍ2 (11.1k), Vi1 (2.6k); thin elsewhere.

## Result

Drift-axis percentiles for the six units with ≥ 1k words in both the ppl and
vayubd layers:

| unit | W1 ppl / vayubd | C3 ppl / vayubd |
|---|---|---|
| V1 frame–cosmogony | 74 / 66 | 96 / 87 |
| V3 kalpas–śiva-lineages | 55 / 63 | 81 / 86 |
| V6 pṛthu–prajāpati | 34 / 57 | 68 / 76 |
| V7 śrāddha-kalpa (ppl 384 w) | 30 / 86 | 53 / 94 |
| V8 vaṃśas | 21 / 36 | 39 / 65 |
| Bḍ1 | 58 / 66 | 86 / 82 |
| Bḍ2 | 23 / 62 | 41 / 79 |

(constituted PPL on the same maps: I 22 / ungrouped 23 / II 37 on W1;
22–28 on C3. Full table incl. thin subsets in the TSVs.)

1. **The PPL layer inside the Vāyu/Brahmāṇḍa is older-styled than the
   Vāyu↔Bḍ common layer** — consistently on both feature systems for the
   genealogical/list cores (V6, V7, V8, Bḍ2; V3 mildly). V8's and Bḍ2's
   PPL-parallel verses land at percentile 21–23 on W1, *inside* the
   constituted-PPL band: the purāṇas' own transmitted copies of PPL material
   are linguistically as old as Kirfel's constitution. The Vāyu↔Bḍ common
   text around them sits 15–40 points later.
2. **Exception: V1 (sṛṣṭi/cosmogony).** Its PPL-parallels are *late*-styled
   (74/96), slightly later than its vayubd layer — the cosmogony parallels
   pattern with the late Textgruppen (IIA/IIB sit at 60–78 on these maps),
   not with PPL I/II. Kirfel's own late strata, seen from the borrower side.
3. **The Viṣṇupurāṇa reverses the pattern** (Vi1: ppl 63 / vayubd 26 on W1;
   Vi3: 67 / 50): its pañcalakṣaṇa-parallel material is *not* early-styled.
   Consistent with the ViP's reputation as a literary reworking — it
   paraphrases the old material into its own (later) idiom, unlike the
   Vāyu/Bḍ which transmit it.
4. Layer ordering within Vāyu/Bḍ, summarized: **ppl < vayubd ≈ residue** —
   an old imported stratum inside a later composition, visible purely from
   counted linguistic habits.

## Consequence for the chronology argument

This is the stratigraphic decomposition the article needs: the drift axis
separates *transmission layers within a single text*. The Vāyu(-prokta) is
not an old purāṇa; it is a late-idiom composition (unique residue and
Vāyu↔Bḍ common text at percentile ~60–90) that embeds a genuinely archaic
genealogical stratum (percentile ~20–40) — and that stratum is the PPL,
whose constituted Textgruppen I/II sit in the same band. The Vāyu's
reputation for antiquity is its cargo, not its voice.

## Caveats / next

- The V8/vaṃśa genre control still applies to the *absolute* earliness of
  the ppl layer (list-genre style), though not to the ppl-vs-vayubd
  *contrast* within the same section, which is genre-matched by construction.
- Bootstrap CIs on projected layer positions (thin layers flagged in the
  figure at < 150 words are not interpretable).
- Attribution classes overlap (a ppl line may also match vayubd
  counterparts); the ppl bucket takes precedence. `attribution.tsv` has the
  full family sets per line for finer splits.
