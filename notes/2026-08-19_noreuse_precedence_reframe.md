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

## R1 RESULTS (run 2026-08-19, `b2_null_models.py --noreuse`, 10 reps)

TSVs: `axis_anatomy/b2_models_{W1,C3}_noreuse_500.tsv` (schema now
carries a rho_logT column; the with-reuse TSVs keep the old schema).

| | axis-1 share | ratio 1/2 | ρ(axis1, t) | ρ(axis1, logT) |
|---|---|---|---|---|
| **W1 noreuse REAL** | 12.8% | 1.31 | — | **0.444** |
| W1 exchangeable | 18.5±0.4% | 4.22 | — | 0.960±0.006 |
| W1 heterogeneity | 5.1±0.1% | 2.22 | — | 0.792±0.027 |
| W1 drift | 39.7±1.2% | 3.09 | 0.974±0.010 | 0.087±0.052 |
| **C3 noreuse REAL** | 8.7% | 1.21 | — | **0.064** |
| C3 exchangeable | 6.9±0.2% | 1.14 | — | 0.164±0.120 |
| C3 heterogeneity | 2.5±0.1% | 1.09 | — | 0.116±0.085 |
| C3 drift | 40.9±1.5% | 2.81 | 0.996±0.002 | 0.065±0.038 |

**Verdict — division of labor between the lenses inverts on residues.**
On the stripped corpus the unit sizes span 648–345k words, and in the
**W1** lens pure multinomial noise alone (exchangeable null) produces an
18.5%-share axis with ρ 0.96 against log length — a stronger axis than
the real corpus's own 12.8%. The real W1-noreuse axis-1 ρ vs log length
is 0.44: partly length-contaminated, and W1-noreuse can NOT carry the
headline chronology alone. In the **C3** lens the per-unit event counts
stay in the millions even for tiny residues, so the exchangeable
artifact is weak (6.9% share, ρ 0.16) and the real axis is length-clean
(ρ 0.064). **The no-reuse chronology leads with C3; W1 confirms.**
Cross-lens agreement of the two no-reuse axis-1 orderings: ρ 0.928
(0.929 restricted to ≥3k residues) — the convergence argument carries
over to the no-reuse build.

Mitigation numbers (coords-based): restricting W1-noreuse to the 108
units with residue ≥ 3,000 words lowers |ρ| vs log length 0.44 → 0.32
and raises the with/without-reuse ordering agreement 0.908 → 0.945.
Residual 0.32 is plausibly substantive (the early-ward-moving great
compilations also have the largest residues), but the honest wording is
"partly confounded"; C3 carries the burden.

## R2 RESULTS (run 2026-08-19, `noreuse_reframe/unit_bootstrap_cis.py`, B=500, seed 20260814)

Per-unit line-bootstrap CIs of axis-1 percentile on the fixed map of each
build, same Gower instrument as `complement_halves/bootstrap_cis.py`
(units > 2,000 lines resampled in consecutive-line blocks). TSVs:
`noreuse_reframe/unit_ci_{W1,C3}_{withreuse,noreuse}.tsv`, joined in
`movers_{W1,C3}.tsv`.

**C3 (authoritative lens): 16 CI-separated moves of 126.** The
consequences exhibit for the article:

| unit | with-reuse | no-reuse | shift |
|---|---|---|---|
| Brahmāṇḍa | 62.7 [59.9, 64.3] | 44.0 [40.4, 47.2] | −18.7 |
| Brahmāṇḍa 2 | 39.7 [36.5, 40.5] | 28.0 [25.6, 34.4] | −11.7 |
| ŚiP Dharmasaṃhitā | 53.2 | 43.2 | −10.0 (CIs touch) |
| MBh 13 app. (MA13) | 80.2 [77.8, 82.5] | 72.0 [68.8, 73.6] | −8.2 |
| Mārk 1–80 / Mārk | 42.9 / 38.1 | 36.0 / 32.0 | −6.9 / −6.1 |
| Padma | 47.6 [46.8, 48.4] | 44.0 [40.0, 46.4] | −3.6 |
| Bhaviṣya | 64.3 [63.5, 66.7] | 60.8 [57.6, 63.2] | −3.5 |
| Kūrma 2 | 90.5 | 87.2 | −3.3 |
| Umāsaṃhitā | 62.7 [57.9, 65.1] | 72.0 [67.6, 76.0] | +9.3 |
| Vāyu (whole) | 71.4 [67.5, 76.2] | 80.8 [78.4, 84.8] | +9.4 |
| Vāyu-03 | 70.6 | 81.6 | +11.0 |

Sub-3k residues (V8, Vi5, V6, Vt…) get wide C3 CIs and mostly fail
CI-separation — the instrument marks them honestly uncertain.

**W1: 70 of 126 CI-separated — but the per-unit magnitudes are
artifact-inflated and NOT citable.** Consistent with R1's exchangeable
verdict (length artifact axis, ρ 0.96 vs logT): on the W1-noreuse map
essentially every sub-3k residue lands at the late pole (V5 100, V1 97,
V7 96, Vi2 90, Vi6 93…) and the large-residue units are pushed early-ward
en bloc (even MBh 3 "moves" 14→4). Direction agreement with C3 exists for
the well-measured units (Pd, Bhv, K2, MA13, Mā, Dh early-ward; V, V3, U
late-ward) — W1 confirms *signs*, C3 supplies *numbers*.

**Bottom line for the reframe: it works.** The no-reuse composition
chronology is C3-led (length-clean, ρ 0.982 to the with-reuse ordering,
cross-lens ρ 0.93 with W1-noreuse), the with-reuse map opens the story,
and the difference section cites the C3 movers table above with the
upgraded-purāṇa reading (Kengo confirmed 2026-08-19: the borrowed mass
drags a text toward wherever its sources sit — for the
Śivadharma-incorporators, late-ward; Bhaviṣya −3.5 and Padma −3.6
CI-separated early-ward on strip).

## Remaining work queue

1. ~~R1 null battery~~ → DONE, see above.
2. ~~R2 fixed-map bootstrap instrument~~ → DONE, see above.
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
