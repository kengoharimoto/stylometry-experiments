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

## The flattening is systematic: a census of Sn–Vi3 analogues

**Run 2026-08-21** (Kengo's question: are there other pairs like
Sn–Vi3?). Instrument: `figures/mds3d/flattened_pairs.py` →
**`flattened_pairs.tsv`** (the citable source for this section; same
four Delta-table inputs as `axis3_analysis.py`, 3-axis coords from the
committed viewers' PTS arrays). Criterion per map: in-plane distance in
the closest 2% of all pairs AND 3-D distance ≥ 3× in-plane.

**329 pairs qualify across the four maps (120 BhP, 209 non-BhP)** —
Sn–Vi3 is one mid-strength instance of a corpus-wide pattern, not an
anecdote. Two families:

**1. Bhāgavata pairs — the extreme cases**, exactly as the axis-3
result predicts: the BhP's offset is orthogonal to the published
plane, so its units acquire false 2-D neighbours. Worst offenders
(2-D / 3-D / full Delta / mutual neighbour ranks out of 125–126):

| map | pair | 2-D | 3-D | Delta | ranks |
|---|---|---|---|---|---|
| W1 with | Bh10c ~ Revākhaṇḍa | 0.036 | 0.846 | 1.235 | 109/122 |
| W1 with | Bh2 ~ Vāyu Gayā-māh. | 0.012 | 0.819 | 1.343 | 122/116 |
| C3 with | Bh2 ~ Nīlamata | 0.032 | 0.954 | 1.446 | 113/121 |

Near-coincident on the plane; among each other's most *distant* units
by full Delta.

**2. Non-BhP pairs — true Sn–Vi3 analogues** (well-measured: all units
≥ 4.5k words on their build):

- **Vāyu Gayā-māhātmya (V10) ~ ViP aṃśa 6** (W1 with-reuse): 2-D
  0.045, Delta 1.260, ranks 94/122 — stronger than Sn–Vi3 itself. V10
  recurs as a misleadingly-placed unit: K2~V10 (Delta 1.101) and
  Vā~V10 (1.017) on W1 no-reuse, ŚDhU~V10 (1.287) on C3 no-reuse.
- **Sn recurs too**: G1~Sn on C3 with-reuse (2-D 0.045, Delta 0.973,
  ranks 58/51) — the Sanatkumārasaṃhitā sits in the crowded middle on
  both lenses and picks up false 2-D neighbours generally.
- **SP1 ~ ViP aṃśa 5** (C3 no-reuse): 2-D 0.024, Delta 1.077, ranks
  93/36.
- Reference row: **Sn~Vi3** itself (W1 with-reuse) = 2-D 0.043, 3-D
  0.190, Delta 0.917, ranks 81/41.

**Caveats (keep these when citing):**

1. The most spectacular-looking row, V1~V5 on C3 no-reuse (Delta
   1.717, ranks 119/122), is **not citable**: those Vāyu-section
   residues are 983 and 648 words after the strip — deep sub-3k. The
   TSV carries a `sub3k` flag (33 of 329 rows); filter on it.
2. **The inference does not run backwards**: a large axis-3 gap does
   not prove distance — Bhaviṣya~Kāśīkhaṇḍa separate on axis 3 yet
   their full Delta (0.666) is well below the corpus median. Axis-3
   separation is evidence of 2-D flattening, not a distance measure.
3. **3-D still flattens**: V10~Vi6 is 0.52 in 3-D but 1.26 in full
   Delta. The rule from finding 5 holds in the stronger form — the
   check of record for any pairwise closeness is the Delta table; the
   3-D viewer is the intuition aid.

Article payoff: §9.2 can claim the flattening is *systematic* and
disproportionately involves BhP units (as the axis-3 result predicts),
with Sn–Vi3 as the worked example rather than the whole evidence.

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
