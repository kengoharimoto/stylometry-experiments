# 2026-08-30: no-reuse-representative restructure, paratext fix, full pipeline refresh

One session (local Mac, Claude), commits `476ec34` → `5ccbc22`. This
note is the consolidated record; `article/claims_evidence_map.md` is
the citation authority, this note the narrative + operational memo
for future sessions (including waffle).

## 1. The restructure (Kengo's call)

The draft (`article/draft_dh.md`) was rewritten so that the
**no-reuse corpus is THE corpus of the paper**, not the privileged
member of a pair, and so that comparisons against uncorrected builds
(with reuse, with colophons, spaced trigrams) are **diagnoses of
contamination, never robustness tests**. Concretely:

- Reuse-stripping moved into §2.2 as corpus construction (with
  colophon removal and the word-division discipline); the old §3.2
  "reuse independence" robustness paragraph is gone.
- The old §7.2 lens-swap material (R1: no-reuse W1 axis partly a
  length artifact) moved into §3.4 — the chronology is trigram-led
  from the start; W1 corroborates orderings/directions only.
- Old §7 reframed as "What the absorbed text was doing: the
  with-reuse map as diagnostic"; the "precedence" subsection
  dissolved (no competition to adjudicate). Table 1 columns:
  no-reuse | with-reuse | **drag** (= with-reuse − no-reuse;
  positive = absorbed material had dragged the text lateward).
- §8 leads with no-reuse values everywhere.
- **Terminology RULED (reaffirming 2026-08-21): plain
  with-reuse / no-reuse.** The interim "cleaned / transmitted /
  composition" build labels were reverted (`e4b5d4c`). Ordinary
  text-critical uses of transmitted/transmission stay legitimate.

## 2. Old Skandapurāṇa passage (Kengo's corrections)

- The SP is a **validation**, not a departure: its editors
  (Adriaensen, Bakker, Isaacson) place it among the oldest purāṇas,
  **second only to the Vāyupurāṇa in its undivided form** (the
  purāṇa later split into the printed Vāyu and Brahmāṇḍa).
- **Do not write "ur-Vāyu"** — the editors don't use the term.
- **Hazra and the Mārkaṇḍeya comparison dropped**: Hazra did not
  know the old SP as an independent purāṇa, so there never was an
  apparent conflict (a non-issue, not even a soft-point locator).
  Hazra 1940 removed from the references.
- The pāśupata-layer contrast is stated plainly (transmission
  conservatism does not by itself make text measure early); the
  "one transmission, early core measuring early…" slogan is retired.

## 3. Open items closed (Kengo's calls)

- **§2.4 lens disjointness**: both lenses' signal attributed against
  the C3 no-reuse axis (the R1-safe construction);
  `a2_bridge_c3_classes.py --noreuse` →
  `class_signal_shares_noreuse.tsv`. Shares build-stable
  (closed classes 37%/11%, interior ~61%, particles 4% vs 36%).
- **§8 within-host layer comparison**: KEPT, restated explicitly as
  a same-transmission projection on the with-reuse map
  (apparatus-style direction test).
- **§5 trigram glosses verified by source-word attribution** over
  the no-reuse corpus: **mṛt = smṛta-** (NOT amṛta — the citation
  formula, converging with W1's smṛtam/ucyate/proktam), **aye =
  -ayet causative optatives** (pūjayet, kārayet…), rah = brahma-,
  hat = hatvā/hata- (+mahat), han part-dhanus/dhanaṃjaya; ātr and
  kal genuinely mixed, left unglossed.

## 4. Paratext fix (Kengo-approved)

Standalone running-title lines — same paratext class as colophons,
missed by `is_colophon_line()` because they carry no iti/adhyāyaḥ
formula — struck from ALL corpus variants (sandhied, unsandhied,
both no-reuse; nospace rebuilt):

- Garuḍa `śrīgaruḍamahāpurāṇam` × 312 (k1 236 / k2 47 / k3 29)
- Devībhāgavata `śrīmaddevībhāgavatam` × 12
- Agni `śrīrāmāvatāra-varṇanaṃ/-varṇanam/-kathanaṃ` × 6
- **Skipped by Kengo's call**: the 2× cases (śrīmārkaṇḍeyapurāṇam,
  śrīmanmaharṣi… lines).

Filter: `is_colophon_line()` gained an exact-match `_TITLE_LINES`
set (`scripts/process_epic_puranas_unsandhied_local.py`). **No
generic standalone-line rule is safe**: the Agni carries ~130
per-adhyāya topic titles (-kathanaṃ ×39, -vidhiḥ ×18, -vidhānaṃ ×16,
-varṇanaṃ, -vratāni, …) tangled with ~300 GENUINE unspaced verse
pādas, plus 30 bhagavānuvāca speaker lines. → **OPEN: Agni topic
titles need a curated eye-review if pursued** (~2 percentiles of
Agni position at stake).

Measured impact (pre-refresh check): Garuḍa 0/−1.6/0, Devībhāgavata
−0.8, Agni −2.4 percentiles (earlier-ward, as the late-styled title
diction predicted); global ρ 0.9992. No-reuse corpus total now
**3,555,225 words** (−947). Corpora are git-tracked (`dd2c526`) —
waffle gets the fix via `git pull`; pre-fix file versions live in
git history.

## 5. Pipeline refresh (everything regenerated post-fix)

All frames/TSVs/figures now derive from the fixed corpora; the
draft's numbers were updated wholesale (commit `5ccbc22`, 74 files).
Headline state: cross-lens 0.93 (0.928); Fig 2 adopted cell 0.929,
max 0.937 at W1-800 × C3-3000; null battery C3 real 8.6% / exch.
7.1 ± 0.4% / het. 2.5% / drift 40.9% at ρ 0.996; jackknife ≥ 0.991;
B2b loss 0.85–0.87 vs gains 0.61–0.70 (thresholds 1.1–1.3; committed
TSV at 1.3); decomposition interior 0.96 / boundary 0.04–0.08; SP
28 [26, 32]; Kirfel bands 25–33 / 67–94; E1 MBh 13 apparatus
47 [44, 53] vs 30, MBh 18 61 [38, 80] vs 8; **drag table 15
CI-separated rows** (Dharmasaṃhitā now separates cleanly; PPL IIB,
Kūrma 2, Rām 6 fell inside their intervals; Vāyu-upasaṃhāra† and
MBh 13 Anuśāsana entered); stylo cross-validation 1.0000 on the
rebuilt no-reuse nospace corpus.

**Substantive correction found during the refresh — the cliff
claim.** The interim §3.1 statement "W1's high-MFW cliff disappears
without reuse" conflated raw axis-1 with the Procrustes-aligned
plane. Correct statement (now in §3.1/§7.1, guardrailed in the
claims map): at high MFW the drift gradient is **demoted** from W1's
first axis on BOTH builds (raw axis-1 vs adopted ordering: 0.49
no-reuse, 0.14 with-reuse at 5000 MFW); with reuse in, the usurping
first axis anti-correlates with its no-reuse counterpart (−0.87) —
it is made of the shared material; the aligned top-2 plane retains
the ordering on both builds (0.92–0.94). Never write "the cliff
disappears"; always state the raw-vs-aligned convention when
discussing high-MFW W1.

## 6. Operational notes for waffle sessions

- **Scripts now run on both machines**: every generator gained a
  `STYLO_ROOT` env override (defaults to
  `/mnt/kengo/stylometry-experiments`, so waffle needs no env; on
  the Mac export `STYLO_ROOT=~/Desktop/stylometric_works`). Scripts
  patched: unit_bootstrap_cis, movers_table, e1_project,
  axis3_analysis, flattened_pairs, q3_y_covariates, b5_arch,
  b2_null_models, b2b_loss_gain, a1_loadings, a2_decomposition,
  b1_variance, b3_convergent_orderings, a2_bridge_c3_classes,
  fig1_map_pair, fig2_convergence.
- `--noreuse` modes added to a1/a2/b1/b3/bridge (w + --noreuse
  refused per R1 throughout).
- **`movers_table.py c --markdown` now emits Table 1 in the drag
  format directly** (no-reuse | with-reuse | drag, sorted by drag) —
  regenerate, never hand-edit.
- **Traps** (also in the claims map §0): `mfw_sweep_noreuse/
  coords_mfw*.tsv` are SPACED C3 — the no-space no-reuse sweep is
  `c3_nospace_noreuse/`; `b2b_loss_gain_*_noreuse_500.tsv` sit at
  THRESH 1.3 and are silently overwritten by runs at other
  thresholds (restore from git; cite the sweep, not one setting);
  the W1-rates loading table (`loadings_W1rates_vs_C3axis_...`) is
  correlated against the C3 axis — never against the W1-noreuse
  axis.
- **On waffle after `git pull`**: rebuild the untracked nospace
  corpora (`python3 scripts/build_nospace_sandhied_corpus.py` for
  the with-reuse variant, and with `--manifest
  manifests/noreuse2026_n126.txt --source-dir
  corpus/epic_puranas_sandhied_noreuse --out-dir
  corpus/epic_puranas_sandhied_noreuse_nospace`), and delete any
  stale `.cache_freq_*.rds` in the corpus dirs before stylo runs.
- Incidental find, unfixed: the Garuḍa's opening incipit lines
  ("śrī gaṇādhipataye namaḥ", "atha śrīgaruḍamahāpurāṇaṃ
  prārabhyate") remain in the corpus — one-line front matter,
  negligible, noted for completeness.

## 7. Still open (also in claims map §8)

1. Agni per-adhyāya topic titles (curated review; Kengo to decide).
2. E1-full: Belvalkar print apparatus OCR — optional, magnitudes
   only; not needed for the DH submission.
3. Venue (Kengo).
