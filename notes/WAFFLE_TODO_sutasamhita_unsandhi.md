# Instructions for Claude running on waffle — Sūtasaṃhitā khaṇḍa-4 swap

Written 2026-07-23 on the Mac. Goal: swap the re-extracted Sūtasaṃhitā
khaṇḍa-4 mūla into the corpus as one atomic commit. Only the unsandhi step
*needs* waffle (the ByT5 GPU pipeline); doing the whole swap here keeps the
three corpus dirs consistent in a single commit.

## Background (one paragraph)

`corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4_v2.txt` (committed
8e56f56) is a re-extraction of the mūla from the ĀnSS OCR: 4,958 lines,
98.9% verse recall by number evidence. The current canonical unit
(`..._khanda-4.txt`, no `_v2`) came from a v1 heuristic that silently
dropped ~half the verses — every figure/stylo number based on this unit
undercounts its text. See `scripts/extract_sutasamhita_mula_v2.py`
docstring for the failure modes.

## Steps

All from the repo root of the stylometric_works clone on waffle, after
`git pull` (must include commit 8e56f56 or later).

1. **Swap the raw unit** (keep the canonical name; retire the old text):

   ```bash
   mv corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4.txt \
      corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4.txt.v1_backup
   git mv corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4_v2.txt \
      corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4.txt
   ```

   (`.v1_backup` is untracked; the v1 text stays retrievable from git
   history anyway. Do NOT delete files — repo owner's standing rule.)

2. **Rebuild the sandhied unit** (runs anywhere, no GPU):

   ```bash
   python3 scripts/build_epic_puranas_sandhied.py \
       skandamahapurana_sutasamhita_khanda-4.txt --force
   ```

   (Check the script's actual flag for overwriting; if there is no
   `--force`, remove the existing
   `corpus/epic_puranas_sandhied/skandamahapurana_sutasamhita_khanda-4.txt`
   first — that is a regeneration, not a deletion of unique data.)

3. **Rebuild the unsandhied unit** (the waffle-only step; RTX PRO 6000,
   ByT5-Sanskrit CT2 int8 at `/mnt/code/byt5-analyzer`):

   ```bash
   scripts/unsandhi_local.sh skandamahapurana_sutasamhita_khanda-4.txt --force
   ```

   Same note about `--force` as above (the underlying
   `process_epic_puranas_unsandhied_local.py` skips existing outputs
   without it).

4. **Verify before committing** — all three should now describe the same,
   roughly-doubled text:

   ```bash
   wc -l corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4.txt \
         corpus/epic_puranas_sandhied/skandamahapurana_sutasamhita_khanda-4.txt \
         corpus/epic_puranas_unsandhied/skandamahapurana_sutasamhita_khanda-4.txt
   ```

   Expect ~4.9k raw lines (was ~3.0k). Sanity-check the unsandhied output:
   spot-read 10 lines (words split, no `||`, no digits, IAST only), and
   confirm no mass line-dropping by `is_skip_line()` (the pausa/ASCII trap
   that once truncated the Nīlamata — see
   notes/2026-07-09_nilamata_sandhi_episode.md).

5. **Commit** (raw swap + sandhied + unsandhied together, one commit),
   message along the lines of: "Swap in re-extracted Sūtasaṃhitā khaṇḍa-4
   (98.9% verse recall, was ~50%)". Push.

## What this does NOT include (done later on the Mac)

- Regenerating figures (hero + highlights + companion + robustness + mfw +
  explainer + consensus tree + reuse overlay), stylo W1/C3 reruns, and the
  all-pairs reuse scan (`scripts/presentation/corpus_reuse_scan.py`,
  ~25 min) — the corpus text change invalidates all of these. The Mac
  session knows the drill (same cascade as the 2026-07-23 Matsya fix,
  commits 6557f36 + 04f87f8).
- Word-count changes on slides (corpus total shifts by ~+8k words; the
  "≈ 4.6 million" claim is safe).
- The Sūtasaṃhitā stratum note in chronology_strata.tsv mentions nothing
  text-critical — no edit needed there.

## Context that may save you a wrong turn

- The unit is IAST throughout; the ĀnSS OCR source it came from lives on
  the Mac (`~/Documents/E-texts/00_inbox/New/sutasamhita_khanda4_roman.txt`),
  not in this repo. You never need it for this task.
- Verse-closer markers `|| N ||` are already stripped from the v2 file?
  NO — they are still present (`... || 54 ||` style) plus adhyāya
  colophons. `build_epic_puranas_sandhied.py`'s `strip_ref_markers()` is
  expected to remove the digits; verify on the output. If digits survive
  into the sandhied/unsandhied units, strip `\|\|?\s*\d*\s*\|\|?` and bare
  daṇḍas in the raw file first, mirroring how the other corpus units look
  (no daṇḍas, no verse numbers, colophons kept as plain lines).
