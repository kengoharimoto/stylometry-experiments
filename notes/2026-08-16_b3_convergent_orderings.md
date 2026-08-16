# B3: convergent orderings — the gradient belongs to the distance structure

2026-08-16. The axis-anatomy plan's B3, on the colophon-free corpus at
article conventions. Script `axis_anatomy/b3_convergent_orderings.py`,
per-unit orderings in `b3_orderings_{W1,C3}_500.tsv`. Four methods with
different assumptions: spectral seriation (Fiedler vector, Gaussian
affinity), 1-D isomap (k=10 geodesics), TSP/Hamiltonian-path seriation
(NN + 2-opt, best of 6 starts), and plain PCA on the z-scored features.
t-SNE/UMAP are deliberately absent (they preserve local neighbourhoods
and discard the global geometry a gradient reading lives in).

## Result — with a subtlety the plan didn't anticipate

Raw first dimension vs the sweet-spot MDS axis (|ρ|):

| method | W1 | C3 |
|---|---|---|
| PCA 1 | **0.997** | 0.636 |
| isomap 1-D | 0.924 | 0.813 |
| Fiedler | 0.779 | 0.311 |
| TSP path | 0.294 | 0.236 |

The low C3 numbers are not failures of convergence — they are the
**near-degenerate spectrum** (B1: C3 axis1/axis2 ratio 1.13) showing up
exactly as it should: with two almost-tied real dimensions, different
algorithms legitimately disagree about which comes *first*. Diagnosis:
C3's PCA 1 is the **register axis** (ρ 0.83 vs y, 0.64 vs x) and its
PCA 2 is the drift axis; the Fiedler vector likewise leans y with the
drift in the next eigenvector. The proper object of comparison for a
near-degenerate case is the method's top-2 plane, Procrustes-rotated onto
the map:

| method (aligned top-2 plane) | W1 | C3 |
|---|---|---|
| PCA | **0.997** | **0.995** |
| Fiedler | 0.946 | 0.816 |
| isomap | 0.924 | 0.848 |

**Every global method finds the drift gradient in its top plane.** PCA —
which shares nothing with Delta+MDS beyond z-scoring (L2 vs L1, no
distance matrix, no double-centering) — reproduces the axis at ≥ 0.995 on
both lenses, and its loadings are directly readable (the A1 table is
effectively its interpretation). Fiedler and isomap land at 0.82–0.95,
with the shortfall attributable to kernel/graph choices, not to the
gradient.

**The TSP failure is a finding, not a bug.** A Hamiltonian path through a
cloud with a real second dimension snake-folds (its position correlates
~0.3 with *both* axes); path seriation only tracks a gradient when the
data are effectively one-dimensional. Its failure here independently
confirms B5: the corpus genuinely has a second organized dimension.

## For the article (methods section)

State it in this order: (i) the ordering is not MDS-specific — PCA
recovers it at 0.995+ on both lenses, spectral and geodesic methods find
it in their top plane; (ii) on C3 the first-vs-second dimension flips
between methods because the register dimension is nearly as strong as the
drift dimension (ratio 1.13) — which is a *property of the corpus*
(cf. B5's cross-lens y agreement), not an instability; (iii) one-sentence
exclusions: t-SNE/UMAP discard global geometry; path seriation requires
effectively 1-D data and its failure here is diagnostic of the real
second dimension.
