# Corpora

The prepared text corpora the scripts in this repository operate on. The
whole tree is versioned here (since 2026-08-14; the epic_puranas builds were
already tracked before that), except regenerable stylo frequency caches
(`.cache_freq_*.rds`).

Provenance: the texts derive from GRETIL e-texts, critical-edition e-text
lineages, and OCR of printed editions, cleaned and prepared by the scripts in
`scripts/` (see the repo README). Check per-text provenance before re-hosting
any of this material elsewhere.

## Directories

- `epic_puranas/` — raw prepared sources (cleaned line-per-half-śloka IAST);
  `.txt.orig` files are the pre-cleaning states kept for provenance
- `epic_puranas_sandhied/` — sandhied build (C3 analyses);
  `scripts/build_epic_puranas_sandhied.py`
- `epic_puranas_unsandhied/` — ByT5 word-split build (W1 analyses);
  `scripts/process_epic_puranas_unsandhied_local.py` + `unsandhi_local.sh`
- `epic_puranas_noreuse/`, `epic_puranas_sandhied_noreuse/`,
  `epic_puranas_unsandhied_noreuse/` — parallels-removed builds
  (`scripts/build_noreuse_corpus.py`; kirfel family = one-directional reuse
  source)
- `complements_sandhied/`, `complements_src/`, `complements_unsandhied/` —
  the removed ("shared") halves of Vāyu/Brahmāṇḍa/Viṣṇu units as standalone
  files, plus family-attributed subsets (`_shared_{ppl,vayubd,other}`) and
  the per-line attribution map (`complements_sandhied/attribution.tsv`);
  `scripts/build_complement_units.py` and
  `materials/presentation_2026/figures/complement_halves/attribute_families.py`
- `epic_puranas_excluded/` — units excluded from the study corpus
- `epic_puranas_unsandhied_stale_backup/` — pre-reprocess backup of the
  unsandhied build, kept for comparison
- `gi/`, `main/`, `noroots/` — placeholder directories for the earlier
  GI / clustering experiments; prepare those corpora locally (see the repo
  README) — they are not distributed here

Corpus history (marker cleanup, unsandhi reprocess, PPL re-import) is
documented in `notes/`.
