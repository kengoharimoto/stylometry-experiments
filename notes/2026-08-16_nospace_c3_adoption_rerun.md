# No-space C3 adopted; downstream C3 instruments re-run

2026-08-16. Following `2026-08-16_c3_nospace_scriptio_continua.md`, Kengo
adopted the no-space (scriptio-continua) C3-500 as the article's C3
convention. All C3-side downstream instruments were re-run against the
no-space base map (`c3_nospace/coords_nospace_mfw500.tsv`); W1 instruments
are untouched. Changed scripts (all now count trigrams with every space and
line break removed, and orient onto the no-space reference):
`complement_halves/{project_halves,project_subsets,bootstrap_cis}.py`,
`genre_control/genre_project.py`, `e1_apparatus/e1_project.py`, plus
`complement_halves/sp_mark_cis.py` — a repo re-creation of the sp_mark
scratchpad run (B=500, seed 20260814). In the bootstrap, C3 lines are now
counted as bare character streams (no `' '+line+' '` padding — there are no
space trigrams); the pivot-shift onto the exact whole-text estimate is
unchanged. All TSVs and figures in the three bundles are regenerated; the
pre-adoption versions remain in git history (commit 6491c9e and earlier).

## What holds, what sharpens, what weakens (C3, est [95% CI])

**1. Layer stratigraphy (shared_layers_by_family): sharpens.**
The PPL stratum inside Vāyu/Bḍ vs the Vāyu↔Bḍ common layer:

| unit | PPL layer old → new | Vāyu↔Bḍ layer old → new |
|---|---|---|
| V8 (vaṃśa core) | 39 [33,42] → **28 [25,29]** | 65 [60,77] → 64 [52,73] |
| Bḍ khaṇḍa 2 | 41 [40,47] → **29 [28,35]** | 79 [76,82] → 76 [71,79] |
| V7 (śrāddha) | 53 [29,80] → 32 [16,67] | 94 [93,95] → 86 [79,90] |

The PPL layers move down toward the constituted-PPL band while the common
layers stay high — the CI separation *widens*. The V1 cosmogony reversal
survives as before (V1 ppl 95 [92,98], still late-styled — the real
counter-case). ViP's paraphrase reversal also survives (resid earlier than
shared throughout, e.g. aṃśa 4: 29 vs ppl 50/vayubd 93/other 85).

**2. Constituted PPL internal stratigraphy: sharpens.**
Early block barely moves (I 24→28 [25,30]; ungrouped 23→25 [23,29];
II 28→29 [25,35]); the late Textgruppen move sharply later
and toward their W1 positions (Ia 36→61 [48,73], III 44→73 [58,81],
IIB 64→87 [80,91], IIA 60→93 [90,96]). Kirfel's own early/late grouping now
reads directly off the C3 axis.

**3. SP/Mārk/PPL sequence (sp_mark note): conclusions hold, numbers shift.**

| unit | old C3 | new C3 |
|---|---|---|
| PPL I / ungrouped / II | 24 / 23 / 28 | 28 [25,31] / 25 [23,29] / 29 [25,35] |
| old SP whole | 40 [40,43] | **31 [29,33]** |
| old SP adhy. 1–31 | 54 [52,59] | 36 [33,41] |
| SP pāśupata 174–183 | 92 | 99 [95,99] |
| Mārk whole | 53 [50,54] | 43 [41,44] |
| Mārk 1–80 | 60 [58,61] | 46 [44,53] |
| Mārk 81–93 (DM) | 49 [44,54] | 39 [33,47] |
| Mārk 94–141 | 31 [27,34] | **28 [25,30]** |

SP-before-Mārk stays CI-separated (31 [29,33] vs 43 [41,44]). Mārk 94–141
now sits *inside* the PPL band on C3 (28 vs 25–29) — the interleaving
refinement strengthens. Note the general pattern: purāṇic units move
5–20 points earlier on the no-space lens, i.e. closer to their W1
percentiles (the convergence improvement doing its work).

**4. E1 apparatus: direction uniform, magnitudes up.**
Apparatus strata (old → new): MBh 15: 5 → 8 [4,21]; 16: 19 → 27 [17,44];
17: 9 → 8 [1,43]; 18: 44 → **62 [39,82]** (now matching its W1 62);
13: 44 → 48 [43,54]. Every apparatus stratum still later-styled than its
constituted text; every augmented unit still moves right (aug−const:
+1/+5/+1/+12/+8). Closing parvans' constituted positions: 4/5/0/10.

**5. Vaṃśa genre control: pull confirmed, but the C3 floor argument
weakens — flag honestly.** Gen-half pulls are now −10 to −29 points
(Bhaviṣya 45 vs 74; Matsya 37 vs 56; Padma 38 vs 56; Brahma 36 vs 45;
Agni 77 vs 90). The gen-half floor among late texts drops from ~46 to ~36,
while the PPL band sits at 25–29: the closest pairs now *overlap* in CI
(Brahma gen 36 [30,38] vs PPL II 29 [25,35]). On the no-space C3 alone,
"genre cannot reach the PPL band" is no longer CI-clean. The control's
decisive lens remains W1 (unchanged: floor ~46 vs PPL 21–24, separated),
and the layer argument (V8's PPL layer earlier than V8's own vaṃśa-genre
common layer, same genre both sides) is genre-immune by construction. The
article should lean on those two, not on the C3 floor.

## Bookkeeping

- C3 percentiles quoted in the 2026-08-14 notes are the *standard-C3*
  instrument's; this note is the conversion table for the headline rows.
  Pointer addenda added to the four instrument notes.
- The noreuse sweep, MFW sweep, and metric sweep were standard-C3 runs;
  their conclusions are about axis robustness (ρ across settings) and are
  unaffected by the convention switch — the no-space mini-sweep in
  `c3_nospace/` already shows ρ(no-space, std) = 0.90–0.94 across MFW.
- Still standard-C3: the stylo cross-validation runs (R stylo has no
  no-space mode wired up) — the hero_mds wordlist validation is skipped
  under `--strip-spaces`, so the no-space C3 rests on the Python pipeline
  alone. If a stylo counterpart is ever wanted, feed it a pre-stripped
  corpus build.
