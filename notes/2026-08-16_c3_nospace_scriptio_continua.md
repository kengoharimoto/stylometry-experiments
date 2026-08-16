# C3 without word division: the scriptio-continua check

2026-08-16. Kengo's worry: C3 trigrams include spaces, so many top features
are case-ending-plus-space types — but word division in romanized Sanskrit
is *editorial* (manuscripts are scriptio continua; recitation pauses need
not fall at printed spaces). Does the C3 map depend on it?

## Method

`hero_mds.py --strip-spaces` (new flag): delete ALL whitespace (word spaces
and line breaks) before counting, so trigrams run over the continuous
sandhied stream. Same manifest (`dicsep2026_n127_ppl`), Burrows's Delta,
MFW 250/500/1000/5000, Procrustes-aligned onto the W1-delta hero reference
like every sweep run. No stylo counterpart run exists, so the wordlist
validation is skipped (flagged in the script). Bundle:
`materials/presentation_2026/figures/c3_nospace/` (coords TSVs,
`analyze_nospace.py`, no-space C3-500 map figure).

Feature anatomy: **167 of the standard top-500 trigrams (33%) contain a
space** — 'aṃ ', 'aḥ ', 'ca ', ' pr', 'ḥ s'... — exactly the
ending-plus-boundary types Kengo suspected. 333 of the space-free ones are
shared with the no-space top-500.

## Results

1. **The axis does not depend on word division.** ρ_x(no-space, standard) =
   0.90–0.94 across MFW 250–5000; the left-to-right stratum ordering is
   unchanged; the closing parvans stay at the pole (15: 1→4, 16: 6→5,
   17: 0→0, 18: 6→10). Rām-trails-MBh on C3 survives (medians: MBh 7 vs
   Rām 12, was 7 vs 14).
2. **Removing spaces makes C3 agree with W1 *better*, at every MFW.**
   ρ_x vs the W1 hero: 0.90/0.91/0.91/0.87 (no-space) against
   0.85/0.86/0.85/0.82 (standard). At the sweet spot vs W1-500:
   **0.894 → 0.949**. Mean |C3 − W1| percentile gap per text: 11.4 → 9.7.
   The editorial spaces were adding lens-specific noise, not drift signal.
3. **The movers move *toward* their W1 positions (7 of the 9 largest).**
   Percentiles (std → no-space, W1-500 in brackets):
   - ŚiP Dharmasaṃhitā 95 → 49 [61]; ŚiP Sanatkumāra 99 → 79 [79];
     Padma-a 82 → 53 [40]; old SP adhy. 1–31 53 → 36 [21].
   - Kirfel's *late* Textgruppen move later: Ia 36 → 60 [72],
     III 44 → 73 [69], IIB 64 → 87 [85], IIA 60 → 93 [64, overshoot].
     Standard C3 was *understating* their lateness.
4. **The early PPL block does not move**: Textgruppe I 24 → 27,
   II 28 → 29, ungrouped 22 → 25. PPL priority is untouched — and the
   internal PPL stratigraphy (early block vs Ia/IIA/IIB/III) comes out
   *sharper* without spaces, now matching Kirfel's own grouping on both
   lenses.

## Reading

Word division contributes editorial noise to C3, and stripping it yields a
cleaner lens: closer to W1, sharper internal PPL stratigraphy, all headline
findings intact. The texts that moved most are exactly those whose sources
plausibly carry distinctive spacing conventions (the OCR-derived Kirfel
PPL columns; the Śivadharma/Padma editions) — consistent with the standing
caution that orthographic conventions are editorial, not authorial. This
experiment removes one editorial layer from C3; sandhi itself (also partly
editorial in normalized e-texts) remains, per the axis-anatomy plan's A4
caution.

**Decision for the article (Kengo's call):** adopt no-space C3-500 as the
article's C3 convention, or keep standard C3-500 and cite this as a
robustness check. If adopted, the C3 side of every downstream instrument
needs the no-space variant re-run (Gower projections, line-bootstrap CIs —
the space-padded line counting becomes plain concatenation), and
C3 percentiles quoted in the 2026-08-14 notes for the §3 movers (e.g. old
SP 1–31 at C3 54; the Śivadharma pair's late-pole ranks) are
instrument-specific and would shift.

## Files

- `scripts/presentation/hero_mds.py` — `--strip-spaces` flag (default off;
  deck figures unaffected).
- `materials/presentation_2026/figures/c3_nospace/` —
  `coords_nospace_mfw{250,500,1000,5000}.tsv`, `analyze_nospace.py`,
  `companion_C3_delta_MDS_dicsep2026_n127_ppl_nospace.{png,pdf}`.
