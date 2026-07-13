# Stylo tokenization bug: IAST words split at Latin Extended Additional characters

**Date found:** 2026-07-10 (while validating the presentation hero plot)
**Fixed in:** `scripts/clusters.R` (`splitting.rule = "[[:space:]]+"`), first
corrected runs `results_epic_puranas_unsandhied_W1_50-80_20260710_170027/` and
`results_epic_puranas_sandhied_C3_2000-5000_20260710_170252/`.

## The bug

With `corpus.lang = "English.all"` (the default in `clusters.R`), stylo 0.7.5's
tokenizer treats **Latin Extended Additional characters — ṣ ṭ ḍ ṇ ḥ ṃ ṛ ṅ (the
U+1E00 block) — as word separators**, while accepting ASCII, Latin-1 (ñ), and
Latin Extended-A (ā ī ū ś). IAST tokens were silently mutilated:

    guṇa -> gu | a      kṛta -> k | ta      lakṣmī -> lak | mī     tataḥ -> tata

Diagnosis was conclusive: replicating this splitting in Python reproduces
stylo's saved distance table to r = 0.999999 (correct tokenization only reaches
r ≈ 0.94), and stylo's own `wordlist.txt` contained fragments (`k`, `am`, `i`,
`lak`, `gu`, `pu`, `var`) among the "most frequent words".

## Impact on results made before 2026-07-10

Every stylo run in this repo executed on this machine used the mutilated
tokens. In practice:

- **W1 (word unigrams):** the MFW band was a mixture of genuine particles
  (*ca, eva, tu, na, tathā, api, iti* — these contain no U+1E00 characters and
  survived intact) and morphological fragments. Results were meaningful —
  the W1/C3 convergence and the macro-clusters stand — but "50–80 MFW ≈
  particles" in the earlier notes is only partly accurate.
- **C3 (char 3-grams):** worse conceptually. N-grams were built from the split
  tokens, so **visarga, anusvāra, the retroflex series, and ṛ were entirely
  absent from the feature space** — much of the phonotactic/sandhi signal C3
  was supposed to capture was discarded. The corrected C3 run's wordlist
  contains ~6,000 n-gram types with these characters.
- Applies equally to the GI and Delta-NN runs made with the R pipeline here;
  those should be regenerated before being cited.

## The fix

Our corpora are pre-cleaned, space-separated tokens, so the correct rule is
whitespace splitting. `clusters.R` now passes
`splitting.rule = "[[:space:]]+"` to the parsing `stylo()` call and stamps the
frequency-cache tag with `_ws` so caches from the old tokenization are never
reused. Verified: corrected W1 top-80 = real words only; my independent Python
pipeline (whitespace tokens, wordlist ranked by raw summed counts) matches the
corrected stylo distance table to r = 1.0 and the wordlist 80/80.

## Methodological silver lining

The headline findings survived the bug (fragments still carry morphological
signal, and the macro-structure replicated in the corrupted feature spaces
too) — worth remembering as an unintentional robustness check. But all figures
and numbers for the presentation and paper must come from the corrected
(2026-07-10+) runs.
