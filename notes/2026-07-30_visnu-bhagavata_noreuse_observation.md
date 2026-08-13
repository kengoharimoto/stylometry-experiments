# Viṣṇu–Bhāgavata affinity revealed by reuse removal (W1, no-reuse corpus)

**Date:** 2026-07-30
**Data:** `corpus/epic_puranas_unsandhied_noreuse` (reuse scan RATIO 70, symmetric
drop), manifest `manifests/noreuse2026_n119.txt`, stylo run
`results_epic_puranas_unsandhied_noreuse_W1_50-80_noreuse2026_n119_20260729_201600`,
figure `materials/presentation_2026/figures/hero_W1_delta_MDS_noreuse2026_n119.png`.

## Observation

In the with-reuse W1 hero map the Bhāgavata skandhas form an isolated island
while the Viṣṇupurāṇa sits embedded in the old-purāṇic-core/sectarian mass. In
the no-reuse map the Viṣṇu aṃśas and the Bhāgavata cluster cohabit the same
area.

## Numbers (Burrows's Delta, top-80 MFW, same 119 units in both corpora)

Retention after reuse removal (words kept):

| unit | retained |
|---|---|
| visnupurana_amsa-1 | 49.7% |
| visnupurana_amsa-2 | 23.4% |
| visnupurana_amsa-3 | 61.0% |
| visnupurana_amsa-4 | 93.4% |
| visnupurana_amsa-5 | 19.9% |
| visnupurana_amsa-6 | 20.9% |
| visnupurana (whole) | 44.7% |
| bhagavatapurana skandhas | 88.6–98.7% (all thirteen units) |

- The two works barely share text *with each other*: aṃśa 5 (Kṛṣṇacarita)
  loses 80% of its words while skandha 10, treating the same material, loses
  only 6.4%. The drop is symmetric, so their mutual verbatim overlap is small —
  same story, independent wording, no copying in either direction (and no
  implication about which came first).
- With reuse, Viṣṇu's closest cross-work neighbors are its copyists:
  Mārkaṇḍeya (Δ 0.51), Brahmapurāṇa (0.58), Bhaviṣya (0.59). Without reuse
  the Brahmapurāṇa drops out of the top ten entirely and everything recedes
  to ≥ 0.68.
- Rank of the nearest Bhāgavata skandha among each Viṣṇu aṃśa's neighbors:
  15/31/32/8/16/14 (with reuse) → 3/5/13/6/3/9 (no reuse). Yet the *mean*
  Vi–Bh Delta is essentially unchanged (1.04 → 1.06, ≈ corpus mean): the
  Bhāgavata did not converge on the Viṣṇu — the pseudo-neighbors created by
  reuse fell away.
- Even with reuse, `visnupurana_u` was already skandha 10's #2 cross-work
  neighbor (0.79, after the Harivaṃśa). The affinity existed all along; it
  was buried on the Viṣṇu's side under its widely-copied material.

## Reading (Kengo)

The Viṣṇu and the Bhāgavata treat the same material, composed around the same
time but independently; the Viṣṇu's material was widely reused by other
purāṇas while the Bhāgavata's was not. The with-reuse map understated their
stylistic kinship because the Viṣṇu's profile was dominated by its borrowed
skin; on its own diction, the Viṣṇu is as close to the Bhāgavata as to
anything else. This coheres with the position that the Bhāgavata is genuinely
early in Purāṇa terms — not a later deliberate archaizer (the archaism-as-
imitation reading is not assumed here).

## Caveats

- Genre-composition skew: what survives of the Viṣṇu is precisely its
  non-shared (discursive/devotional) portions, because the genealogical
  pañcalakṣaṇa matter is what everyone copied; that skew alone pushes the
  residue toward Bhāgavata-like registers.
- Small residues: aṃśas 2, 5, 6 keep only ~1,000–3,000 words — noisy for
  MFW-80 Delta; their individual map positions should not be over-read.
- W1 Delta measures register, not date; "same time" is an interpretation of
  the register match, not a measurement.

## Reproduce

```
Rscript scripts/clusters.R --corpus-dir=corpus/epic_puranas_unsandhied_noreuse \
  --files-from=manifests/noreuse2026_n119.txt --features=w --ngram-size=1 \
  --mfw-min=50 --mfw-max=80 --mfw-incr=10
python3 scripts/presentation/hero_mds.py \
  --corpus-dir corpus/epic_puranas_unsandhied_noreuse \
  --files-from manifests/noreuse2026_n119.txt
```
