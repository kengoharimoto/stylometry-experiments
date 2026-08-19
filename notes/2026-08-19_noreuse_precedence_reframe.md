# No-reuse precedence: reframing decision + verified evidence

**Date:** 2026-08-19. **Decision (Kengo):** the article gives precedence
to the no-reuse maps as the better estimate of the **chronology of
original compositions**. Rationale: the purāṇas kept being upgraded —
text incorporated from elsewhere carries the *source's* language, so a
with-reuse position reflects the mixture of layers present in the text,
while the reuse-stripped residue approaches what the compilers
themselves wrote. Narrative arc for the article: (1) the with-reuse
timeline we started from, (2) the reuse-excluded rerun, (3) the
consequences of the difference, (4) why the no-reuse version is the more
useful chronology, (5) the 3-D structure (below).

**Status of numbers in this note: exploratory-grade.** Computed from
`hero_mds.py --dump-dist` tables (article-standard 500 MFW, Delta,
classical MDS) — NOT yet from the fixed-map Gower + line-bootstrap
instrument. Re-derive before print (work queue below).

## Instruments

- `scripts/presentation/hero_mds.py --dump-dist` (added 2026-08-19,
  commit 091c6dc): exact map Delta in stylo table format.
- Four maps: W1-500 unsandhied / C3-500 no-space sandhied ×
  {with-reuse `dicsep2026_n127_ppl`, no-reuse `noreuse2026_n126`}.
  No-reuse corpus = RATIO-70 strip, symmetric drop, kirfel one-directional
  source (2026-08-13 build).
- 3-D viewers: `scripts/presentation/mds3d_viewer.py` →
  `materials/presentation_2026/figures/mds3d/article_*.html`; 2-D
  "Front" = published plane (hero orientation / Procrustes).

## Ordering stability with vs without reuse (axis-1 percentiles, 126 shared units)

Spearman ρ of the two axis-1 orderings: **W1 0.908, C3 0.982**.
The clock survives the strip (the old B8 lesson); individual units move.

### Early-ward movers (with-reuse → no-reuse percentile, W1-500)

The **large compilations look later with their borrowed skin on**; the
residue (= compilers' own diction) sits earlier. All residues here are
large — these moves are trustworthy:

| unit | pct shift | residue words |
|---|---|---|
| Saura | 71 → 49 | 24,834 |
| Bhaviṣya | 69 → 46 | 211,387 |
| Vāyu-Revākhaṇḍa | 62 → 39 | (10k-unit scale) |
| Padma | 54 → 33 | 344,712 |
| Nārada 2 | 56 → 38 | — |
| Garuḍa 2 | 86 → 70 | — |
| Devīpurāṇa | 86 → 69 | — |
| Kūrma 2 | 94 → 77 | — |
| Kāśīkhaṇḍa | 73 → 57 | — |
| SkP-Revākhaṇḍa | 55 → 42 | 37,889 |

### Late-ward movers — CAUTION, mostly sub-3k residues

V8 22→76 (residue 1,064 w), V5 70→99 (648), V1 77→97 (983),
V6 47→82 (1,421), Vi2 66→89 (1,642), Vi5 27→62 (2,796), Vi6 74→93
(945), MBh17 0→22 (1,004), MBh18 5→25 (1,708), V4 68→86 (5,062).
Every one except V4 is inside the **sub-3k uncertainty region** — the
old-core carriers keep almost nothing once the shared pañcalakṣaṇa-type
material is stripped (which is itself the point: their text mostly *is*
the shared inheritance), but their residue positions must not be
over-read. In figures: grey them out or mark open-symbol.

C3 shows the same pattern muted (ρ 0.982; biggest mover V6 +19).

## The Śivadharma case — measured

Reuse partners (`reuse_pairs.tsv`, ratio-80 line containment of the
smaller text): ŚDhU ↔ ŚiP-Dharmasaṃhitā 0.260, Bhaviṣya ↔ ŚDhU 0.224,
Bhaviṣya ↔ ŚDhŚ 0.245, Padma ↔ ŚDhU 0.155, ŚDhU ↔ Umāsaṃhitā 0.129,
ŚDhU ↔ SkP-Revākhaṇḍa 0.115, Saura ↔ ŚDhŚ 0.048.

Positions: ŚDhŚ/ŚDhU sit at the **late extreme** of axis 1 in both
builds (W1 pct 99/98 with-reuse → 94/94 no-reuse; C3 94/90 unchanged).
**Direction note:** the incorporators (Bhaviṣya, Padma, Saura,
Revākhaṇḍa) appear *later* with reuse included and move *early-ward*
when stripped — i.e. the borrowed Śivadharma/māhātmya mass drags them
toward the late pole, not the early one. The principle (borrowed text
carries the source's language; strip → composition chronology) is
confirmed; the sign of the drag depends on where the borrowed material
sits, and for the Śivadharma-incorporators it is late-ward. Kengo to
confirm the intended framing of this example before it goes in the
article.

## 3-D structure (computed 2026-08-19, same tables)

Axis shares (W1 with-reuse): 13.4/8.0/7.3%; (W1 no-reuse):
12.8/9.7/5.6%; (C3 with-reuse): 10.2/9.5/6.7%; (C3 no-reuse):
8.7/7.2/5.7%.

- **Cross-lens convergence by axis** (joint 3-axis Procrustes, Spearman):
  with-reuse: axis1 0.969, axis2 0.857, axis3 0.458.
  no-reuse: axis1 0.952, axis2 0.744, **axis3 0.743**.
- **Axis 3 ≈ the Bhāgavata direction**: the 13 BhP units monopolize one
  pole — offset from the rest +3.8 SD (W1) / +5.0 SD (C3) in the
  no-reuse build; point-biserial with BhP membership 0.76/0.84 (0.56/0.85
  with-reuse). Excluding BhP, axis-3 convergence drops (0.27 with-reuse /
  0.65 no-reuse) while axis-1 convergence is unchanged (0.973/0.950) —
  the BhP's idiosyncrasy is an *orthogonal dimension*, so its axis-1
  position is not driven by its distinctiveness, and the ordering is
  robust to its exclusion. (Wording guardrail intact: this is symmetric
  "sui generis" evidence, no archaizer premise.)
- With-reuse W1 axis 3 is length-tinged (ρ +0.54 vs log words); the
  clean statement of the BhP-dimension result uses C3 + the no-reuse
  build (length ρ ≈ 0 both lenses there).
- Flattening example for the proximity guardrail: Sn–Vi3 full Delta
  0.917 (W1-500 with-reuse), in-plane 2-D distance 0.043, 3-D 0.190 —
  2-D proximity in the crowded middle is not affinity.

## Red flags / work queue before the reframed draft can cite no-reuse numbers

1. **Length correlation revived in no-reuse W1**: axis1 ρ +0.44, axis2
   +0.59 vs log residue words (with-reuse: −0.07/−0.24; C3 no-reuse
   axis1 +0.07). Likely a retention confound (how much a text was copied
   correlates with both residue size and age) — but the B2-style
   exchangeable/heterogeneity/drift null battery MUST be re-run on the
   no-reuse build before it becomes the headline map.
2. Fixed-map Gower + line-bootstrap instrument re-run on no-reuse
   W1-500/C3-500ns → CI-grade percentiles for the movers tables.
3. Decide which validation exhibits are re-derived on no-reuse (E1
   apparatus, PPL Textgruppen bands, genre control) vs kept on
   with-reuse with an explicit bridge argument.
4. Sub-3k residue policy in all no-reuse figures (grey-out rule).
5. C3's far greater stability (0.982 vs 0.908) is itself an exhibit:
   the phonic/orthographic texture of a text is less reuse-sensitive
   than its word profile — candidate for the "consequences" section.

## Article restructure sketch (variant B / DH draft)

Present order of the chronology argument becomes: (i) with-reuse maps —
the tradition as transmitted, language mixture of all layers; (ii)
no-reuse maps — the compilers' own diction; (iii) consequences: global
order stable (0.91/0.98), compilations move early-ward, old-core
carriers dissolve into sub-3k uncertainty; Viṣṇu–Bhāgavata affinity
(2026-07-30 note) as the flagship revealed-affinity case; (iv) why
no-reuse is the better composition chronology (upgraded-purāṇa
argument); (v) 3-D: axis 3 = BhP dimension; flattening guardrail.
"Language age ≠ book age" sharpens into: with-reuse = age of the
language *present*, no-reuse = age of the language *composed*.
