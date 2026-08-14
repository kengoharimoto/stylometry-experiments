# MFW sweeps on the parallels-removed build; cross-build robustness

2026-08-14. Third part of today's robustness series (see
`2026-08-14_mfw_robustness_W1_C3.md` and `2026-08-14_distance_metrics_W1_C3.md`).
The same W1 (MFW 30–5000) and C3 (MFW 250–12000) delta-MDS sweeps, re-run on
the noreuse build: `corpus/epic_puranas_sandhied_noreuse` /
`corpus/epic_puranas_unsandhied_noreuse`, manifest `noreuse2026_n126`
(126 texts; differs from `dicsep2026_n127_ppl` only by dropping `vayu_ba`).
Bundle: `materials/presentation_2026/figures/mfw_sweep_noreuse/`
(`analyze_noreuse.py` reproduces all tables).

## Same shape as the reuse-in build, with a narrower W1 plateau

- **C3**: x stable across 250–12000 (ρ vs 5000 ≥ 0.92); agreement with the
  W1-80 hero peaks at MFW 500 (0.85) and declines past 5000 (0.70 at 12000);
  y is the MFW-sensitive dimension below 3000. Identical story to the main
  build, marginally noisier at 250.
- **W1**: the stability plateau is narrower — 80–500 (ρ vs 80 ≥ 0.94; 800
  drops to 0.90) and the cliff comes earlier: 1500 is already 0.57 (vs 0.83
  with reuse in), 3000–5000 ≈ 0.33. Expected: removing parallels shrinks each
  unit's token count, so the function-word inventory is exhausted sooner and
  content words take over earlier.
- **W1×C3 convergence**: ridge W1 120–500 × C3 500–5000 (ρ ≈ 0.85–0.87),
  peaking at W1-300 × C3-1000 (0.872); W1-500 × C3-500 gives 0.852. Slightly
  lower and flatter than the main build's 0.894, consistent with the smaller
  units.

## Cross-build: the sweet-spot axis is reuse-independent

ρ of x between the noreuse and reuse-in builds on the 126 shared texts:

| | | | |
|---|---|---|---|
| C3-500 **0.983** | C3-1000 **0.990** | C3-5000 0.965 | C3-12000 0.917 |
| W1-80 **0.979** | W1-200 **0.977** | W1-500 0.914 | W1-1500 0.185 |

At the recommended settings the chronological ordering is essentially
unchanged by removing the parallels — the axis is not driven by shared or
reused verses. (W1-30/50 are also unstable across builds, 0.40/0.69: another
reason not to go below ~80 words.)

**The collapsed W1 regime anti-correlates across builds** (−0.62 at 3000,
−0.86 at 5000). Once the axis is content-dominated, it is largely organized
by the reused material itself — present in one build, absent in the other —
and the near-degenerate epic-left sign anchor (epic mean x ≈ 0 there) lets
the whole axis flip. A vivid confirmation that W1 beyond ~1500 measures
something other than drift, in either build.

## Bottom line

Every robustness axis checked today points the same way: the drift reading of
dim 1 survives MFW (within the plateaus), distance measure (any standardized
one), and parallels removal. Recommended settings stand: W1 ~200–500,
C3 ~500–1000.
