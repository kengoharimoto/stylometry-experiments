# A2: class decomposition — the drift is written everywhere in the language

2026-08-16. The axis-anatomy plan's A2, run on the colophon-free corpus at
the article conventions, with the pre-computation hand review replaced by
a perturbation sensitivity check (per the day's decision).
`axis_anatomy/a2_decomposition.py`, results `a2_decomposition.tsv`.
Method: for each feature class, build the Delta+MDS axis from (a) the
class members alone and (b) the top-500 with the class removed, refilled
from the frequency ranking; report |ρ| of that axis against the article's
sweet-spot axis.

## W1-500 (words)

| class | n | alone | removed+refilled |
|---|---|---|---|
| particle/indeclinable | 49 | 0.889 | 0.994 |
| pronoun | 60 | 0.824 | 0.985 |
| narrative verb | 22 | 0.692 | 0.994 |
| prescriptive verb | 5 | 0.604 | 0.996 |
| numeral/list | 27 | 0.809 | 0.998 |
| content | 337 | 0.941 | 0.979 |
| closed-class union | 163 | 0.947 | 0.941 |

**No class is necessary** (removal ≥ 0.94 always — even deleting the
entire closed-class band, or all 337 content forms). **Every substantial
class suffices approximately**: particles alone 0.89, pronouns alone 0.82,
content alone 0.94, the closed union 0.95 — and even the five
prescriptive optatives alone reach 0.60. The axis is massively redundant:
the same ordering is recoverable from nearly any linguistically coherent
slice of the feature space.

## C3-500 (no-space trigrams)

By mechanical position class (majority position of each trigram's tokens):

| class | n | alone | removed+refilled |
|---|---|---|---|
| word-interior | 345 | **0.972** | 0.742 |
| word-initial | 42 | 0.882 | 0.736 |
| junction-spanning | 65 | **0.141** | 0.966 |
| word-final | 46 | 0.112 | 0.918 |

By majority source-word class: content-sourced alone 0.81, removed 0.97;
particle-sourced (7 trigrams) alone 0.06.

**C3's drift signal lives word-internally.** Interior trigrams alone
reproduce the axis at 0.97; junction and word-final trigrams alone barely
order the corpus at all (0.11–0.14) despite carrying loading mass in
proportion to their tokens (the A2-bridge result) — their variation is
dominated by something other than drift, and an axis built on boundary
phonology alone collapses. This sharpens the bridge finding: the two
lenses converge not just on different word classes but on different
*structural levels* — W1 on whole-form habits (any class), C3 on
word-internal morphology.

## The review question, settled

Flipping all 12 boundary-case classifications (tad/yat/te/ye/kim/nāma/
param/svayam/punar/sma → particle) moves no ρ by more than **0.031**.
The hand review could not have changed any conclusion; Kengo reviews only
the class table that eventually appears in the article.

## For the article (Q1's answer, now complete)

The drift axis is not a particle-habit gradient, not a lexical artifact,
not any single class's property: it is *pervasive, redundant usage
change* — recoverable from function words alone, content forms alone,
pronouns alone, or word-interior trigram morphology alone. This is
precisely the signature the Q2 story requires (many small habits shifting
together, B2's autocorrelated-drift model), and it is the strongest
possible answer to "what if your features are cherry-picked": there is no
way to slice the top-500 that destroys the ordering, short of restricting
to boundary phonology.
