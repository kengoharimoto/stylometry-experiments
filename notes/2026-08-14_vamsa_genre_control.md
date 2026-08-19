# Vaṃśa genre control: does list/genealogy style mimic archaism?

> **DROPPED AS CIRCULAR 2026-08-19 (Kengo's call) — do not cite this
> control or resurrect content-split genre controls.** Kirfel: the vaṃśa
> genre IS the shared ancient inheritance, so the gen-half Δ below
> conflates register with the age of borrowed text, on every build (the
> 2026-08-19 residue re-derivation makes it vivid: the Vāyu's manu-vaṃśa
> section keeps 178 words of genealogy of its own). The genealogy
> objection is answered strip-first instead — see claims map §6.4 and
> `2026-08-19_noreuse_precedence_reframe.md`. The measurements below
> remain valid as measurements; their genre interpretation does not.

2026-08-14. The last open control from the complement-halves work: the PPL
layer and V8 sit early on the drift axis — but vaṃśa material is a
particle-poor, name-heavy genre, so could genre alone produce that placement?
Bundle: `materials/presentation_2026/figures/genre_control/`
(`build_genre_split.py`, `genre_project.py`, `plot_genre.py`, TSVs, figure);
split corpora in `corpus/genre_control_{sandhied,src,unsandhied}/`.

## Two controls

**Observational (natural units, no marker circularity).** The dedicated vaṃśa
books of two late texts vs their same-text siblings on the base maps:
BhP skandha 9 sits at percentile 29 vs sibling-skandha median 49 (W1;
32 vs 40 C3); ViP aṃśa 4 at 42 vs sibling median 69 (W1; 55 vs 74 C3).
Genre pull ≈ 8–27 points.

**Marker split (systematic).** Panel of 13 texts spanning the axis; each
split into genealogy-like lines (marker stems putr/vaṃś/jajñ/ajāyat/duhit/
manvantar/... with ±1-line smoothing; the mapping to source level verified
lossless — every unmatched source line is a header/blank that `clean_line`
drops) vs the rest; both halves projected into the fixed sweet-spot maps
with line-bootstrap CIs (B=200). Est [95% CI], W1:

| text | gen | rest | Δ |
|---|---|---|---|
| MBh 1 Ādi | 10 [6,16] | 13 [11,14] | −3 |
| Harivaṃśa † | 21 | 21 | 0 |
| Matsya † | 37 [33,42] | 62 [60,63] | −25 |
| Mārkaṇḍeya | 30 [28,34] | 39 [36,41] | −9 |
| Brahma † | 29 [28,33] | 48 [47,51] | −19 |
| Agni | 72 [60,83] | 95 [91,95] | −23 |
| Bhaviṣya | 58 [52,61] | 81 [78,82] | −23 |
| Garuḍa 1 | 76 [63,84] | 95 [90,97] | −19 |
| BhP 9 | 36 [28,46] | 28 [25,30] | +8 |
| Kūrma 1 | 52 [40,60] | 78 [67,82] | −25 |
| Padma A | 46 [41,48] | 59 [57,59] | −13 |
| V8 vaṃśas † | 24 [21,28] | 26 [22,28] | −2 |
| V6 pṛthu–praj. † | 46 [36,52] | 48 [43,54] | −2 |

(C3 same shape, pulls −11…−24 for the late texts; TSVs have both.)

## Findings

1. **The genre effect is real: ≈ 15–25 percentile points** for mid/late
   texts, ≈ 0 for texts already at the epic end. Any *absolute* earliness
   claim for genealogical material must be discounted by this much.
2. **But genre alone never reaches the PPL band.** Among late texts whose
   genealogies are NOT pañcalakṣaṇa transmissions (Agni, Bhaviṣya, Garuḍa,
   Kūrma, Padma), the genealogy half bottoms out at percentile 46 (W1) —
   far above the constituted-PPL band (22–38). The only genealogy halves
   that do reach the band belong to PPL witnesses (Matsya 37, Brahma 29,
   V8 24) — i.e., exactly the texts whose genealogy sections *transmit* the
   old stratum. What looks like the genre reaching the band is the
   transmission reaching the band.
3. **V8 is internally genre-homogeneous**: its marker-classified verses vs
   its rest differ by 2 points (24 vs 26). Its earliness is a property of
   the whole section, narrative connective tissue included — not of
   list-style verses within it.
4. The caveat inherits a caveat: the marker split's Δ is an *upper bound*
   on the genre effect, since the marker words themselves are frequent
   features (mechanical dependence). Even this upper bound cannot produce
   the PPL-layer placement.

## Consequence

The genre objection is now bounded and survives only as a discount factor,
not an alternative explanation: subtract ~20 points of genre pull from the
PPL layer's ~21–41 placement and it still sits well clear of where any
late-text genealogy lands. The stratigraphic reading (old PPL stratum inside
late compositions) stands. BhP 9's modest position (36,
+8 vs its genre-mixed remainder) is consistent with the Bhāgavata's
distinctive archaic-leaning profile rather than with a generic genre
artifact.

---

**2026-08-16 instrument update:** the article adopted the no-space
(scriptio-continua) C3 convention and this instrument's C3 side was
re-run against the no-space base map. C3 percentiles quoted above are
the standard-C3 values; see `2026-08-16_nospace_c3_adoption_rerun.md`
for the conversion of the headline rows (conclusions hold; layer
separations sharpen; the C3 genre-floor margin narrows). W1 numbers
are unchanged.
