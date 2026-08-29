# A3 + A5: minimal sufficient set and per-text anatomy (run for the Indological companion)

2026-08-29, Kengo's call: the last two open Q1 experiments, run not for
the DH draft (which stands on A1/A2 and cites neither) but as feedstock
for the Indological companion article, which will lean harder into
philological topics. Instruments and TSVs in `axis_anatomy/`
(`a3_minimal_set.py`, `a5_text_anatomy.py`); with-reuse build, article
conventions (500 features, committed article-frame coords as the
reference axis), seed 20260814.

## A3 — the axis resists compression (the plan's exhibit does not exist)

Greedy forward selection per the plan note: maximize axis agreement on
a random half of the units, evaluate honestly on the held-out half,
target holdout ρ ≥ 0.95.

**W1: no feature set reaches the bar.** The holdout peaks at **k = 7**
(holdout 0.9165, full-corpus 0.9513) with the set

> ādi, adya, rājānam, sma, jñānam, mama, dattvā

and declines from there while the select-half ρ keeps climbing to ~0.98
— textbook overfitting, exactly what the guard was for (by k = 60:
select-half 0.97, holdout 0.68, full 0.80). The trajectory is the
finding: **the drift axis cannot be compressed into a small checkable
word list without losing a real part of the ordering.** This
corroborates A1 (distributed loadings, median |ρ| ≈ 0.25) and A2 (no
class necessary, nearly every class sufficient) from a third direction:
pervasive redundancy, no privileged small basis. If a "check these by
eye" exhibit is wanted for the Indological paper, the honest form is
the seven-feature set above with both numbers stated (full 0.95,
holdout 0.92) — and the seven are philologically legible: narrative
*sma*, dialogic *mama*/*adya*, epic *rājānam*, converb *dattvā* on the
early side; itemizing *ādi*, doctrinal *jñānam* on the late side.

**C3: three trigrams suffice (holdout 0.9585, full 0.9428) — rāj, tāṃ,
ātr.** Not comparable to the W1 result in kind: a trigram aggregates
many word types (rāj = the whole rājan/rājya family plus junctions), so
"three features" here is closer to "three feature *families*". Quote
only with that caveat.

## A5 — per-text anatomy of the featured texts

Decomposition: contribution_f = z_f × ρ_f (corpus z-score ×
axis loading), per text. The loading-weighted z-sum is a faithful axis
proxy — ρ vs the real axis-1 = **0.9953 (W1) / 0.9956 (C3)** over the
127 units — so the top contributions genuinely are "why this text sits
there". TSVs: `a5_text_anatomy_{W1,C3}.tsv` (7 texts × 500 features,
sorted by |contribution|). Featured texts: PPL I, PPL ungrouped, old
SP, ŚDh, ŚDhU, merged MBh 15–18 block, merged BhP (12 skandhas; the
skandha-10 with-commentary unit excluded). With-reuse frame: the
anatomy describes the language a text *carries* — the right object for
worked examples read against the printed page.

Readable headlines (W1):

- **Old SP (pct 25):** early pull is the epic narrative machinery —
  anaphora (*tam* 5.8‰ vs corpus 3.0‰, *sa*, *tān*), *tadā*, simile
  *iva* (5.8‰ vs 2.3‰), direct-speech *vayam*/*mā*.
- **MBh 15–18 block:** court and frame-dialogue vocabulary — *rājā*
  (7.9‰ vs 1.2‰), *kuru*, *rājñaḥ*, *vaiśaṃpāyanaḥ* (the frame
  narrator, 3.8‰ vs 0.4‰), *sa*/*te* anaphora, *uktaḥ*.
- **ŚDh (pct 99):** the late position is carried by sectarian-ritual
  vocabulary (*śiva* 20.5‰ vs 0.9‰, *rudra*, *liṅgam*, *eka*) — but
  cross-reference the strike test (claims map 1.5): with every theonym
  and ritual lexeme struck the axis holds at ρ 0.99, so the position
  does not *depend* on this stratum; the anatomy names what carries it
  in the intact feature set, not what it reduces to.
- **BhP (merged, mid-map):** the early-ward pull is split between
  first-person dialogue vocabulary (*naḥ*, *vayam*, *bhavān*, *sma*,
  *iva*) and — notably — *low rates of the late prescriptive
  machinery* (*tathā* 2.0‰ vs 7.3‰, *jāyate*, *smṛtam*, *bhavati*,
  *sadā* all near zero): part of what reads early in the BhP is the
  absence of late habits, not only the presence of early ones. (State
  symmetrically per the standing guardrail; both readings of the BhP
  question pass through this fact.)

## Where this feeds

The Indological companion's worked-example boxes (A5) and, if wanted,
a seven-word "check by eye" exhibit with its honest caveat (A3). The
DH draft is unchanged; claims map §3.3/§3.4 flipped from "NOT RUN /
decision open" to done-with-verdict.
