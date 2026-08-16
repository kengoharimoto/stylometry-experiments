# Colophon-stripped C3: the paratext contribution is real, directional, small

2026-08-16. Follow-up to the A2 bridge's flag: several strong late-pole C3
trigrams feed on chapter-colophon formulas. Here the colophon lines are
stripped and the no-space C3-500 map rebuilt
(`c3_nocolophon/nocolophon_map.py`; patterns validated against the corpus:
iti-initial lines with genre markers, fused itiśrī..., bare
chapter-number lines ending in (')dhyāyaḥ, samāpta-type enders — ~7,200
lines, 0.90% of corpus words, 79 of 127 units affected, max Vāyu
Revākhaṇḍa 5.1%).

## Result

- **The map does not depend on colophons**: ρ_x(stripped, adopted) =
  0.992; stratum ordering unchanged; poles unmoved.
- **The contamination is real and directional**: ρ(colophon fraction,
  percentile shift) = **−0.58** — colophon-heavy texts sit measurably
  later than their composition language warrants, and move earlier when
  stripped: VDhP 3.343–353 excerpt 57→42 (4.1% colophon), ŚiP
  Rudrasaṃhitā 59→48 (2.6%), Devīmāhātmya unit 39→32 (3.0%),
  Devībhāgavata 54→47 (1.7%). Zero-colophon units shift a few points
  later in the renormalized frame (relative effect). Max mover: 15
  percentiles.
- **W1 convergence improves again**: ρ vs W1-500 0.9495 → 0.9609 — the
  third time removing an editorial/paratextual layer moves C3 toward the
  independent word lens (spaces, then digraph check, now colophons).

## Reading and decision

The colophon effect is a data-hygiene issue, not a lens problem: colophons
are transmission paratext with genre-specific density (purāṇas have many
short chapters). For units quoted in the layer tables the shifts are
within ~1–2 CI widths; no headline conclusion moves. Two options for the
article:

(a) **Keep the adopted no-space C3 and cite this check** — "colophons
contribute ≤15 percentile points for the worst-affected mid-map units and
do not alter the map (ρ 0.99)"; quote colophon-sensitive single-unit C3
positions (DM 81–93, VDhP excerpt, ŚiP saṃhitās) with that caveat.

(b) **Clean the corpus** — remove colophon lines corpus-wide (sandhied
AND unsandhied, like the editorial-marker cleanup of 2026-07), re-run
stylo + both lenses + instruments once. Principled (paratext is not
composition language on either lens), but touches everything and W1
stripping needs care (the ByT5 unsandhied files are not line-aligned with
the sandhied sources everywhere).

Awaiting Kengo's call; (a) is the low-risk default, (b) is the clean one
if the article will lean on colophon-sensitive units.

## Files

`c3_nocolophon/`: nocolophon_map.py, coords_nocolophon_mfw500.tsv
(with per-unit colophon fractions).
