# stylometric_works — session orientation

Read this first in every session, on the Mac or on waffle.

## Where the current state lives

- Authoritative operational record: `notes/2026-08-30_cleaned_corpus_restructure_paratext_fix_refresh.md`
  (section 6 = operational notes, incl. the waffle steps; section 7 = still open).
- Claims-to-evidence map for the DH article: `article/claims_evidence_map.md` (section 0 = traps, section 8 = open items).
- Dated session notes in `notes/` are the git-carried memory; newer notes supersede older ones.
- `notes/WAFFLE_TODO_sutasamhita_unsandhi.md` is DONE (commit 745ded4). Do not redo it.

## Two machines

- Mac: `~/Desktop/stylometric_works`; export `STYLO_ROOT=~/Desktop/stylometric_works` before running scripts.
- waffle (Linux GPU box, user `kengo`): clone at `/mnt/kengo/stylometry-experiments`; `STYLO_ROOT` defaults to that path, no env needed.
- Corpus text moves between machines by `git pull`, never rsync.

## On waffle, after every `git pull` that touches `corpus/`

1. Rebuild the untracked nospace corpora:

   ```bash
   python3 scripts/build_nospace_sandhied_corpus.py
   python3 scripts/build_nospace_sandhied_corpus.py \
       --manifest manifests/noreuse2026_n126.txt \
       --source-dir corpus/epic_puranas_sandhied_noreuse \
       --out-dir corpus/epic_puranas_sandhied_noreuse_nospace
   ```

2. Remove stale `.cache_freq_*.rds` / `.cache_*.rds` files in the corpus dirs before any stylo run
   (list them and get explicit confirmation first; see rules below).

## Standing rules

- Never delete files without showing the full list and getting explicit confirmation.
- Use `python3`, never `python`.
- Sandhi in the corpus is editorial, not authorial; do not build interpretation on it.
- `--noreuse` with W1 (`w`) is refused by design (rule R1); do not work around it.
- Regenerate tables with the scripts (e.g. `movers_table.py c --markdown`), never hand-edit them.
