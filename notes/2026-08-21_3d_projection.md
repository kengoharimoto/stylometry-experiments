# The 3-D projection experiment: a third axis, and what it is

**Written 2026-08-21; experiments run 2026-08-19** (during the no-reuse
precedence work — see `2026-08-19_noreuse_precedence_reframe.md` for the
session context; this note is the self-contained record of the 3-D
side).

**Origin.** Kengo's question about deck slide 44: why do Sn
(Śivapurāṇa Sanatkumārasaṃhitā) and Vi3 (Viṣṇupurāṇa aṃśa 3) sit so
close together? Answer: they aren't close — full Delta puts Vi3 around
rank 50 among Sn's neighbours; the 2-D projection flattens them
together. That prompted the idea of projecting the affinity structure
in three dimensions ("for us humans, a 2D projection of a 3D space may
still be understandable") and asking what, if anything, the third MDS
axis *means*.

## Instruments (all committed)

- Viewer: `scripts/presentation/mds3d_viewer.py` +
  `mds3d_template.html` — self-contained rotatable HTML (deck codes and
  palette, `--ref` Procrustes orientation so "Front" = the published
  2-D plane, `--highlight` rings, two-highlight tether with live
  distance readout, Front/Side/Top buttons).
- Bundle: `materials/presentation_2026/figures/mds3d/` — viewers
  `article_{W1-500,C3-500ns}_{n127,noreuse_n126}.html` (plus the first
  exploratory `noreuse_W1_n119.html`), committed 3-axis coordinates
  `coords_{W1-500,C3-500ns}_{n127,noreuse_n126}.tsv`.
- Statistics (A6 in the claims map queue): `axis3_analysis.py` →
  **`axis3_stats.tsv`** — the citable source for every number below.
  Inputs are the four article-standard Delta tables, regenerable via
  `hero_mds.py --mfw 500 --files-from <manifest> --dump-dist ...`
  (C3: `--features c --strip-spaces`; exact commands in the
  `axis3_analysis.py` docstring). Dist dumps themselves are not
  committed; coords are.

Four maps throughout: W1-500 unsandhied / C3-500 no-space sandhied ×
{with-reuse `dicsep2026_n127_ppl` (n=127), no-reuse `noreuse2026_n126`
(n=126)}.

## Findings

### 1. How much structure lies outside the published plane

Variance shares of MDS axes 1/2/3:

| map | axis 1 | axis 2 | axis 3 |
|---|---|---|---|
| W1 with-reuse | 13.4% | 8.0% | 7.3% |
| W1 no-reuse | 12.8% | 9.7% | 5.6% |
| C3 with-reuse | 10.2% | 9.5% | 6.7% |
| C3 no-reuse | 8.7% | 7.2% | 5.7% |

Axis 3 carries almost as much variance as axis 2 — the published 2-D
plane discards a non-trivial dimension.

### 2. The third axis becomes *real* only in the no-reuse build

Cross-lens Spearman ρ per axis (joint 3-axis Procrustes of C3 onto W1):

| build | axis 1 | axis 2 | axis 3 |
|---|---|---|---|
| with-reuse | 0.969 | 0.857 | 0.458 |
| no-reuse | 0.952 | 0.744 | **0.743** |

With reuse in, the two lenses disagree about axis 3 (0.46 — could be
lens-specific noise). Stripped, they agree (0.74): the composed corpus
has a genuine third stylistic dimension that both word- and
character-level features see.

### 3. Axis 3 ≈ the Bhāgavata dimension

The 13 BhP units monopolize one pole of axis 3:

- Point-biserial r(axis 3, BhP membership): no-reuse **0.76 (W1) /
  0.84 (C3)**; with-reuse 0.56 / 0.85.
- BhP mean offset from the rest, in SD of the rest: no-reuse **+3.8
  (W1) / +4.9 (C3)**; with-reuse +2.1 / +5.1.
- **Orthogonality argument** (the article-relevant payoff): excluding
  the 13 BhP units and re-aligning, axis-3 convergence drops (0.27
  with-reuse / 0.65 no-reuse) while axis-1 convergence is unchanged
  (0.973 / 0.950). The BhP's idiosyncrasy lives on its own orthogonal
  dimension, so its axis-1 (chronology) position is *not* driven by its
  distinctiveness, and the global ordering is robust to its exclusion.
- Wording guardrail intact: this is symmetric "sui generis" evidence —
  no deliberate-archaizer premise, BhP never an anchor.

### 4. Length diagnostic — where the clean statement lives

ρ(axis 3, log unit words): W1 with-reuse **0.54** (length-tinged — cf.
the B2/R1 length-artifact family), W1 no-reuse 0.06; C3 with-reuse
0.26, C3 no-reuse 0.01. The clean statement of the Bhāgavata-dimension
result therefore uses the **no-reuse build** (C3 preferred), where the
length correlation vanishes on both lenses.

### 5. The flattening exhibit: Sn–Vi3

The pair that started it, as the proximity guardrail's showcase
(2-D in-plane distance / 3-D distance / full Delta):

| map | 2-D | 3-D | Delta |
|---|---|---|---|
| W1 with-reuse | **0.043** | 0.190 | 0.917 |
| C3 with-reuse | 0.234 | 0.343 | 1.051 |
| W1 no-reuse | 0.096 | 0.152 | 0.904 |
| C3 no-reuse | 0.183 | 0.273 | 1.042 |

On the deck's W1 plane the pair looks nearly coincident (0.043); one
extra axis already separates them 4×, and the full Delta says they are
not neighbours at all. Lesson, stated as a rule: **2-D proximity in the
crowded middle of the map is not affinity** — check the distance table
(or the 3-D tether readout) before reading any pairwise closeness off
a map.

## Where this feeds the article

- Draft §9.2 "A third dimension: the Bhāgavata direction" — the
  finding, the Sn–Vi3 flattening, pointer to the 3-D supplementary
  maps.
- The 3-D viewers are supplementary material (interactive HTML);
  static 2-D projections of the extra planes can be cut from the
  committed coords if the venue needs them.
- Point (v) of the reframe narrative arc
  (`2026-08-19_noreuse_precedence_reframe.md`).

**Conventions:** article-standard 500 MFW, Burrows's Delta, classical
MDS; orientation of no-reuse maps from
`mds3d/coords_C3-500ns_noreuse_n126.tsv`; W1-noreuse per-unit
magnitudes remain gated (R1) — the 3-D statistics above are
corpus-level and unaffected; sub-3k residues flagged in any per-unit
reading off the viewers.
