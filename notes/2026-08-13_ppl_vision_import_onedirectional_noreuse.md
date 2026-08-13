# PPL vision-adjudicated import; one-directional no-reuse experiment

2026-08-13. Follow-up to the 2026-07-29 quarantine (c087e9a) and the completed
Chandra×Surya vision-adjudication pass in /mnt2/kengo/ocr-kirfel (commits
bba466e, 35021c1: 2,531/2,648 verdicts, 1,756 overrides).

## Quarantine lifted

The seven `kirfel_ppl_*_col1` units were re-imported from
`/mnt2/kengo/ocr-kirfel/textgruppen/`, then re-passed through
`repair_kirfel_diacritics.py` (514 residual word-final plain-h; hiraṇya-type
n-residuals down to 7 corpus-wide) and `join_kirfel_padas.py` (13,826 → 9,966
half-śloka lines). Retroflex shares, the quarantine's failure criterion, now sit
inside the reference band:

| unit | ṇ-share | ṣ-share | ś-share | words |
|---|---|---|---|---|
| Textgruppe I | 19.5% | 19.8% | 24.0% | 25,633 |
| Ia | 20.5% | 19.1% | 26.3% | 6,517 |
| II | 20.4% | 19.2% | 25.7% | 8,806 |
| IIA | 22.1% | 18.8% | 19.3% | 5,360 |
| IIB | 19.6% | 19.2% | 19.5% | 15,482 |
| III | 22.6% | 19.1% | 24.7% | 3,142 |
| ungrouped | 21.7% | 19.3% | 21.8% | 14,204 |
| *Harivaṃśa (ref)* | *22.5%* | *22.0%* | *24.2%* | |
| *Brahmāṇḍa (ref)* | *17.6%* | *20.1%* | *24.9%* | |
| *Matsya (ref)* | *23.0%* | *20.7%* | *24.8%* | |

(Metric: ṇ/(n+ṇ−ṅ−ñ), ṣ/(s+ṣ+ś), ś/(s+ṣ+ś), lowercased, comment lines
excluded. The old build's ṇ-share ran 16.2% on Textgruppe I under this metric.)
Residual caution: ṣ-share runs ~1 point under the reference floor, worst in the
cosmogony groups (IIA/IIB), which also have depressed ś — smaller but real
residual damage; it no longer dominates C3's top trigrams.

OCR-robustness check: nearest-neighbor structure of the with-reuse C3 and W1
n=127 maps is unchanged between the quarantined build and the vision build —
the July placements were never OCR artifacts at the neighbor level.

## One-directional no-reuse design

Question: where does the PPL sit if, per Kirfel, the purāṇas incorporated the
PPL? Then "purāṇas minus cross-family parallels" = "purāṇas without the PPL",
and the constituted PPL itself should stay intact. `build_noreuse_corpus.py`
now treats the kirfel family as the reuse SOURCE (`SOURCE_FAM`): kirfel lines
participate in matching but are never dropped; a confirmed kirfel↔purāṇa match
drops only the purāṇa line. This also strips narrow-witness PPL material that
purāṇa-vs-purāṇa matching cannot see (e.g. Textgruppe III's Matsya-only
creation block). All seven PPL units retain 100.0%; the purāṇa side prunes as
in July (Vāyu 18.8%, Matsya 38.9%, Brahmāṇḍa 41.3%, vayu_ba 2 words).

## Findings (runs of 2026-08-13, manifest noreuse2026_n126, ratio 70)

**C3 sandhied no-reuse** (5000 MFW distance table): every PPL unit's nearest
non-PPL neighbor is a Mahābhārata parvan, thematically matched — genealogy
groups (I, II, ungrouped) → Ādiparvan; cosmogony groups (IIA, IIB) →
Śāntiparvan; Ia, III → Anuśāsanaparvan. Vāyu falls to rank 43 from PPL-I,
Brahmāṇḍa to rank 50; Harivaṃśa alone stays close (rank 6), consistent with
its khila status. With reuse present the same units' nearest neighbors are
their own witnesses (Harivaṃśa, Vāyu-01, Viṣṇu-1). Reading: strip the shared
text and the purāṇas' own residues do not carry PPL-like surface style; the
pañcalakṣaṇa core's phonic/orthographic texture is epic-register.

**W1 unsandhied no-reuse** (80 MFW): the function-word profile disagrees —
nearest non-PPL neighbors stay purāṇic: IIA → Matsya, IIB/ungrouped → Vāyu-03,
III → Vāyu, Ia → Vāyu-06 (0.289, still ranks above five of the six other PPL
units), I → Skanda, II → Harivaṃśa-appendix-Mathurā. So: epic-like sound
texture, Vāyu-Brahmāṇḍa-like grammatical usage. Same C3/W1 split as the
2026-07-08 interpretation note. Caveat: the heavily pruned Vāyu sections are
small (Vāyu-06 970 words, Vāyu-03 2,355), so W1 distances there are noisy.

## Where everything lives (for studying the results)

Results dirs, all timestamped 2026-08-13, each with distance tables per MFW
band plus the full 31-variant figure family (5 distance measures × MDS/CA/BCT,
consensus trees, PCA):

- with-reuse C3: `results_epic_puranas_sandhied_C3_2000-5000_dicsep2026_n127_ppl_20260813_144752`
- with-reuse W1: `results_epic_puranas_unsandhied_W1_50-80_dicsep2026_n127_ppl_20260813_144758`
- no-reuse C3:  `results_epic_puranas_sandhied_noreuse_C3_2000-5000_noreuse2026_n126_20260813_144911`
- no-reuse W1:  `results_epic_puranas_unsandhied_noreuse_W1_50-80_noreuse2026_n126_20260813_145611`

Figures (`materials/presentation_2026/figures/`): the with-reuse hero
`hero_W1_delta_MDS_dicsep2026_n127_ppl` was regenerated in place;
`hero_W1_delta_MDS_noreuse2026_n126` and `companion_C3_delta_MDS_noreuse2026_n126`
are the one-directional pair (PPL plotted as Pl1/Pl1a/Pl2/Pl2A/Pl2B/Pl3/PlU,
stratum 14). The July `_noreuse2026_n119` pair (symmetric drop, PPL excluded)
remains untouched and is what the deck's B8a/B8b slides still embed.

The per-unit retention table for the one-directional build is in the b1e2b51
commit message; regenerate anytime with `python3 scripts/build_noreuse_corpus.py`
(stdout).

## What to scrutinize before this goes into the deck

The crux is the C3/W1 disagreement about the PPL (epic-like sound texture vs
Vāyu-Bḍ-like function words). Checks that would firm it up or kill it:

1. Does the C3 "MBh parvans nearest" pattern hold across the other distance
   measures (canberra/cosine/argamon/minmax EDGES files), or is it
   delta-specific?
2. Does it hold across the MFW bands (2000/3000/4000 vs 5000)?
3. Sample-size control: the pruned Vāyu sections are 460–3k words; PPL units
   are 2.3k–19k. W1 at 80 MFW is length-sensitive — the Ia→Vāyu-06 proximity
   (0.289) rests on 970 surviving words.
4. Genre confound: what survives pruning in the purāṇas is their non-shared
   (often discursive/māhātmya) material, while the PPL is wall-to-wall
   pañcalakṣaṇa narrative. Some of the "epic-ward" C3 movement may be the
   purāṇa residues moving away, not the PPL moving toward the epic — the
   with-reuse vs no-reuse coordinate comparison (Procrustes-aligned hero maps)
   can separate the two.
