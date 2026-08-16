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

## Bootstrap CIs (added the same day)

`complement_halves/bootstrap_cis.py`: line bootstrap, B = 500, seed fixed.
Each layer's lines are resampled with replacement, reprofiled, and reprojected
into the fixed map; 95% CI = 2.5/97.5 quantiles of the drift percentile.
W1 subsets are single-line ByT5 output, so lines there are 16-word
pseudo-verses. For C3, per-line trigram counting cannot see line-junction
trigrams, so lines are counted space-padded and the replicate distribution is
pivot-shifted onto the exact whole-text estimate (which matches the map dots).
Results in `bootstrap_{W1,C3}_500.tsv`; whiskers now drawn in the dot-strip
figure (thin layers < 150 words get no whisker).

CI-backed verdicts on the headline contrasts (ppl vs vayubd, est [95% CI]):

| unit | W1 | C3 | separated? |
|---|---|---|---|
| V8 vaṃśas | 21 [21,22] vs 36 [30,46] | 39 [33,42] vs 65 [60,77] | **yes, both** |
| Bḍ2 | 23 [21,27] vs 62 [59,66] | 41 [40,47] vs 79 [76,82] | **yes, both** |
| V7 śrāddha-kalpa | 30 [26,42] vs 86 [81,87] | 53 [29,80] vs 94 [93,95] | **yes, both** |
| V6 pṛthu–prajāpati | 34 [29,42] vs 57 [49,62] | 68 [58,76] vs 76 [71,81] | W1 yes, C3 overlaps |
| V1 cosmogony (reversed) | 74 [63,83] vs 66 [58,79] | 96 [94,98] vs 87 [79,89] | C3 yes, W1 overlaps |
| Vi1 (reversed) | 63 [55,77] vs 26 [21,47] | 78 [71,86] vs 50 [21,77] | W1 yes, C3 overlaps |

Constituted PPL, the heterogeneity claim: I 23 [21,26], II 38 [33,44],
ungrouped 24 [21,27] vs IIA 78 [63,86], IIB 70 [63,81], III 77 [61,86] on W1
(C3: 24/28/23 vs 60/64/45) — the early block and the late block are cleanly
non-overlapping on both feature systems.

So with error bars: the core stratigraphy (PPL layer earlier than the Vāyu↔Bḍ
common layer in V7/V8/Bḍ2, direction consistent in V6) is solid; the V1
late-cosmogony reversal is significant on C3 only and should be stated as
suggestive; the ViP paraphrase reversal rests on W1.

## Caveats / next

- The V8/vaṃśa genre control still applies to the *absolute* earliness of
  the ppl layer (list-genre style), though not to the ppl-vs-vayubd
  *contrast* within the same section, which is genre-matched by construction.
- Attribution classes overlap (a ppl line may also match vayubd
  counterparts); the ppl bucket takes precedence. `attribution.tsv` has the
  full family sets per line for finer splits.

---

**2026-08-16 instrument update:** the article adopted the no-space
(scriptio-continua) C3 convention and this instrument's C3 side was
re-run against the no-space base map. C3 percentiles quoted above are
the standard-C3 values; see `2026-08-16_nospace_c3_adoption_rerun.md`
for the conversion of the headline rows (conclusions hold; layer
separations sharpen; the C3 genre-floor margin narrows). W1 numbers
are unchanged.
