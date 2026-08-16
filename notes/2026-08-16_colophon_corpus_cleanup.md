# Corpus cleanup: colophons removed corpus-wide; all instruments re-run

2026-08-16. Kengo's decision after the colophon-stripped check: clean the
corpus itself. Chapter colophons are transmission paratext, not
composition language, on either lens — and the W1-500 band carried them
too (adhyāyaḥ ρ_x +0.46 at 0.94‰, śrī +0.45, mahāpurāṇe +0.39).

## What was done

1. **`is_colophon_line()` added to the shared source filter**
   (`process_epic_puranas_unsandhied_local.py`, composed into
   `skip_test_for`), so the sandhied and unsandhied pipelines exclude
   colophons identically. Patterns: iti-initial lines with genre markers;
   fused itiśrī...; bare chapter-number lines ending (')dhyāyaḥ;
   paṭala/samāpta/prakaraṇa enders; mid-line "it[iy] śrī...purāṇ[ae]"
   (ref-tag-glued and verse-sharing colophons). Detection on a normalized
   copy (lowercased, digits/daṇḍas/punctuation stripped, curly avagraha
   handled). **Audit finding: bare "sargaḥ$" is NOT safe** — it killed
   genuine verse lines (BhP 3/7/9/10 visargaḥ, LiP/NaP/Vāyu ādisargaḥ);
   Rām-style sarga colophons are iti-initial and caught by the strict
   pattern. Verse-restoration verified after the fix.
2. **Base corpora regenerated**: sandhied rebuilt from source
   (−7,461 lines / 74 units; kirfel constituted files exempt and
   colophon-free); unsandhied re-inferred by ByT5 int8 on GPU 1
   (74 files; e.g. Mārk: adhyāyaḥ tokens 201→1, śrī 142→10). The
   unsandhied corpus turned out never to have been git-tracked — it now
   is.
3. **Derived corpora**: line-structured variants stripped in place
   (equivalent to rebuild; matching is line-local): noreuse source
   −5,028 / sandhied −4,290 (≈3,200 colophons had previously been
   removed as cross-family "reuse"!), complements −556 (colophons had
   been matched into the shared layers), genre −2,947, E1 −0 (the CE
   carries no colophons). Single-line ByT5 variants (unsandhied noreuse /
   complements / genre) regenerated through the now-filtering pipeline
   (`scripts/regen_derived_unsandhied.sh`).
4. **Reference frames regenerated** on the cleaned corpus:
   `mfw_sweep/coords_W1_mfw500.tsv`, `c3_nospace/coords_nospace_mfw500.tsv`
   (in place; pre-clean versions in git history). W1 stylo wordlist
   validation still passes (493/500 overlap with the pre-clean run).
5. **All instruments re-run, both lenses** (halves, subsets, bootstrap
   B=500, sp_mark B=500, genre, E1) + figures + A1/B5 refresh.

## Effect on the maps

- W1 essentially unmoved: ρ_x(old, new) = 0.998.
- C3 ρ_x(old, new) = 0.991; colophon-heavy units land where the
  stripped-map experiment predicted (VDhP-3 excerpt 57→41, ŚiP
  Rudrasaṃhitā 59→48, Devībhāgavata 54→46).
- W1×C3 convergence: 0.9495 → **0.9526**.
- W1-500 no longer contains adhyāyaḥ/mahāpurāṇe; śrī remains at reduced
  rate (1.30‰, loading 0.33) — genuine in-text honorific usage.

## Effect on headline results (all hold; several tighten)

- **SP before Mārk** (C3): 29 [29,31] vs 38 [37,41] — still CI-separated
  (W1: 26 vs 35, unchanged). Mārk 94–141 at 25 [24,30] C3 / 25 [21,28]
  W1 — at or below the PPL early band (25–32) on both lenses.
- **Layer stratigraphy**: V8 ppl 28 [25,31] vs vayubd 57 [42,66];
  Bḍ2 ppl 31 [29,36] vs vayubd 79 [75,83] — separations intact.
- **E1**: every apparatus stratum later than its constituted text; MBh 13
  apparatus strengthens to 61 [57,63] C3; closing parvans stay at the
  pole.
- A1/B5 anatomy: loading distributions and the no-arch result unchanged
  (ρ_y raw 0.82).

## Bookkeeping

- Pre-clean safety copy of the replaced unsandhied base files:
  `corpus/epic_puranas_unsandhied_precolophon_bak/` (untracked; delete
  when comfortable — git history has everything anyway).
- Pre-clean instrument numbers: git history (≤ commit d9532dd); the
  2026-08-16 adoption note's tables are pre-clean values.
- B1 jackknife numbers in the axis-anatomy note are pre-clean; the corpus
  changed by 0.9% of tokens, conclusions insensitive (re-run on request).
- The mfw_sweep/metric/noreuse sweep TSVs and figures document the
  pre-clean corpus; their robustness conclusions (ρ across settings) are
  not corpus-state-sensitive and were not re-run.
- The `c3_nocolophon/` experimental bundle is now historical (its stripped
  variant IS the corpus).
