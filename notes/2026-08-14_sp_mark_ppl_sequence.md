# PPL I → old Skandapurāṇa / Mārkaṇḍeya: testing the sequence theory

2026-08-14 (evening). Kengo's theory: the earliest authors who cited "THE
purāṇa" meant something close to **Kirfel's PPL Textgruppe I**, before
multiple purāṇas were known; the Mārkaṇḍeya and the old Skandapurāṇa
followed as the earliest purāṇa-titled compositions, the SP possibly
slightly earlier. Line-bootstrap CIs (B=200) on the fixed sweet-spot maps
(`sp_mark_{W1,C3}_500.tsv` in the scratchpad; est [95% CI]):

| unit | W1 | C3 |
|---|---|---|
| PPL Textgruppe I | 23 [21,26] | 24 [22,26] |
| PPL ungrouped | 24 [21,27] | 23 [22,25] |
| PPL Textgruppe II | 38 [33,46] | 28 [26,30] |
| old SP (whole) | 26 [24,26] | 40 [40,43] |
| old SP adhy. 1–31 | 31 [28,34] | 54 [52,59] |
| SP pāśupata 174–183 | 94 | 92 |
| Mārk (whole) | 36 [34,39] | 53 [50,54] |
| Mārk 1–80 (Jaimini frame + tales) | 45 [40,48] | 60 [58,61] |
| Mārk 81–93 (Devīmāhātmya) | 30 [28,34] | 49 [44,54] |
| Mārk 94–141 (pañcalakṣaṇa block) | 27 [23,28] | 31 [27,34] |

**This also corrects an error propagated earlier today**: the
"three debates" note called Mārk 1–80 "the earliest-styled non-PPL purāṇic
composition (W1 30)" — a CI misattributed from the genre-control run on the
whole-Mārk unit. Mārk 1–80 is in fact the *latest* Mārkaṇḍeya layer.

## Verdict on the theory

1. **Stage 1 (THE purāṇa ≈ PPL I) is supported.** PPL I + ungrouped hold
   linguistic priority (22–26 on both lenses, CI-backed), the reference
   sweep gives the singular Vāyu-prokta genealogical citations, and on C3
   the PPL early block is separated from every purāṇa-titled unit.
2. **SP before Mārk holds at whole-text level, CI-separated on both
   lenses** (26 vs 36 on W1, 40 vs 53 on C3) — the "SP possibly slightly
   earlier" hunch is supported, contra the received ~6th–7th-c. dating of
   the SP relative to the Mārkaṇḍeya.
3. **Refinement: at layer level the sequence interleaves.** Mārk 94–141 —
   precisely the pañcalakṣaṇa-content block, which Pargiter-era criticism
   took as the original core — is as early as the SP on W1 and *earlier*
   on C3 (31 vs 40). The stylometrically coherent statement is: the
   earliest purāṇa-titled stratum consists of the old SP's core and Mārk's
   final third, both adjacent to the PPL band; Mārk's Jaimini frame (1–80)
   and the Devīmāhātmya are later layers of the same title, and the SP's
   pāśupata chapters (174–183, at 92–94!) are a late-styled layer inside
   the SP — every one of these "early purāṇas" is itself stratified.
4. **Confound to flag in the article: transmission conservatism.** The old
   SP survives in 9th-century Nepalese transmission; every rival purāṇa's
   text passed through many more centuries of scribal leveling. Part of
   the SP's early look may be *less textual modernization*, not earlier
   composition. (The same argument cuts the other way for the PPL: Kirfel
   constituted from the oldest witnesses, so its priority is if anything
   understated relative to vulgate-transmitted rivals.) The
   layer-consistency of the result (SP's own pāśupata block styles late
   despite identical transmission) shows the axis is not *merely*
   measuring transmission age — the confound bounds, it does not explain.
5. "Before multiple purāṇas were known": keep the library-sweep nuance —
   plural purāṇāni is already in Manu 3.232; the singular-corpus concept
   persists alongside it in the vidyāsthāna register into Amara. The
   theory should say the singular usage is the *older stratum of usage*,
   not that plurality was unknown until late.

---

**2026-08-16 instrument update:** the article adopted the no-space
(scriptio-continua) C3 convention and this instrument's C3 side was
re-run against the no-space base map. C3 percentiles quoted above are
the standard-C3 values; see `2026-08-16_nospace_c3_adoption_rerun.md`
for the conversion of the headline rows (conclusions hold; layer
separations sharpen; the C3 genre-floor margin narrows). W1 numbers
are unchanged.
