# E1 apparatus experiment: the CE-excluded material is uniformly later-styled

2026-08-14. The experiment proposed in `CLOSING_PARVANS_length_artifact_brief.md`
§5 (E1) and left unrun by `2026-07-15_closing_parvans_length_diagnostics.md`:
add the Critical-Edition-excluded apparatus material back into MBh 15–18 and
see whether the books swing rightward; MBh 13 (massively expanded) as the
opposite-gradient control.

## Material

The GRETIL CE e-text (`.txt.orig`, "id<TAB>text") carries the apparatus
subset: star-passage lines (`*` in the id) and some Appendix I blocks (`@`).
Counts (source words): MBh 15 — 976 (8% of constituted), 16 — 708 (22%),
17 — 197 (14%), 18 — 1,330 (57%), 13 — 68,535 (84%). **Caveat: this is the
e-text's apparatus subset, not Belvalkar's full print apparatus** (the e-text
has no `@` blocks at all for 15 and 17); magnitudes are lower bounds.

Build: `figures/e1_apparatus/build_e1_units.py` — augmented units
(constituted + cleaned apparatus, apparatus cleaned with
`extract_mbh_appendix.clean_text`) and apparatus-only units, at source and
sandhied levels; ByT5 for W1. Corpora: `corpus/e1_apparatus_{src,sandhied,
unsandhied}/`. Projection + line-bootstrap CIs (B=200) into the fixed
W1-500/C3-500 maps: `e1_project.py`, results `e1_apparatus_{W1,C3}_500.tsv`.

## Result (drift percentile; est [95% CI])

| unit | const | apparatus W1 | apparatus C3 | augmented W1 | Δ |
|---|---|---|---|---|---|
| MBh 15 | 2 | 16 [10,21] | 5 [0,13] | 3 [1,7] | +2 |
| MBh 16 | 2 | 21 [21,31] | 19 [11,30] | 6 [1,13] | +4 |
| MBh 17 | 0 | 26 [24,40]* | 9 [0,21]* | 1 [1,1] | +1 |
| MBh 18 | 5 | **62 [46,76]** | 44 [24,53] | 22 [21,28] | **+17** |
| MBh 13 | 33 | **55 [53,59]** | 44 [40,46] | 45 [42,47] | **+13** |

(*197 words — thin.) C3 shows the same directions throughout
(augmented Δ: +2/+3/+1/+13/+6).

## Reading

1. **E1's prediction is confirmed in direction, uniformly**: every apparatus
   stratum is later-styled than its constituted text, on both feature
   systems, and every augmented unit moves rightward. The epic-pole position
   of the closing parvans is in part a property of the *constituted* text —
   the CE's exclusions systematically strip later-styled material.
2. **The apparatus is not one thing, and the gradient is itself evidence the
   instrument works.** The few star passages of 15–17 land at 16–26 (near-
   contemporary narrative variants); MBh 18's x-passages (the phalaśruti
   zone) land at 62 — squarely purāṇic — and drag the book from 5 to 22; and
   the MBh 13 control behaves exactly as predicted: its enormous expansion
   overlay is later-styled (55 vs 33) and pulls the augmented book to 45.
   Apparatus lateness tracks apparatus *character* (narrative variant vs
   Brahmanical overlay).
3. For the paper: rerunning with Belvalkar's full print apparatus (App. I
   of 15 especially) would raise the magnitudes; the e-text subset already
   suffices for the directional claim with CIs.

## CORRECTION (same day, after Kengo's challenge)

The reading in the first version of this note — and in the 2026-07-15
note's §5 gloss "what the axis sees at the pole is absence of expository
overlay, not antiquity" — overclaimed. Two corrections:

1. **E1 does not arbitrate between "early composition" and "looks early".**
   Accretions being later-styled than the archetype text is exactly what a
   correctly functioning *age* axis would show on layers of known relative
   date. E1 validates the axis as a layer-dating instrument (a genuinely
   useful result); it does not show the pole is anything other than age.
2. **Mechanism (c) of the brief (the filler-density/genre explanation) is
   refuted by direct measurement.** The closing parvans' tu/eva/tathā/vai
   density is 23–32 per 1k words — *above* the Rām core (Ayodhyā 21), so
   the premise "pure narrative lacks the filler" is factually wrong for
   these books. And low filler does not drive pole position anyway:
   corpus-wide corr(filler density, drift pct) = 0.27, and the
   lowest-density texts include Śivadharmottara (10.3/1k, pct 97),
   Śivadharmaśāstra (15.4/1k, 98), Praṇavakalpa (16.4/1k, 95) — extreme
   *late* pole. The BhP skandhas (9–15/1k) sit mid-map.

### Addendum: expansion propensity vs position, all 18 parvans

Apparatus fraction (star+appendix words / constituted words in the e-text)
against W1-500 drift percentile: Spearman ρ = **0.40** (n = 18). The
didactic books both attracted the most accretion and sit latest (13:
84%@32, 14: 66%@18, 1: 64%@11, 12: 24%@28); the closing parvans 15–17
attracted little and sit at the pole (8–22%@0–2); several late battle books
are nearly as unexpanded and nearly as early (9: 14%@3, 10: 8%@7, 8:
52%@6). Outlier: Virāṭa (141%@10) — its enormous apparatus is
recension *divergence* (N/S retellings of the same episodes), not overlay,
which marks the limit of apparatus fraction as an editing proxy.

**Revised reading**: what survives of 2026-07-15 is D1 (the individual
positions of the sub-3k units are unresolvable) and D4 (the merged block's
pole position is a real signal). With mechanism (c) dead, the merged
closing-parvans block's position means what it says: the *language* of the
constituted closing parvans genuinely patterns with the old epic stratum.
Combined with E1 (their accretions are late-styled and thin), the stylometry
is consistent with an early-fixed narrative kernel appended to the MBh late
*as books* — which is also where the comparative evidence points (Lüders'
independent Yādava-destruction cycle in the Ghata-Jātaka; Jacobi). The
received "late epilogue" verdict concerns their status as books; the
stylometry speaks to the age of their language, and the two are compatible
without the thinness gloss. Standing caveats: language age ≠ book age
(transmission can preserve or level), and individual sub-3k positions
remain uncertain regions per D1.
