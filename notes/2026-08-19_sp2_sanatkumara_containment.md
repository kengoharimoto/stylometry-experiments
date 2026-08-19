# SP2 ↔ Śivapurāṇa-Sanatkumārasaṃhitā: how much of SP2 is really in SKS?

**Date:** 2026-08-19. **Question (Kengo):** the reuse overlay showed
lines between texts sharing text; which texts share much with SP2 (the
Pāśupata-yoga section of the old Skandapurāṇa,
`skandapurana_pasupata_adhyaya174-183_u`, 686 dedup half-śloka lines)?
Recollection to test: "the ŚiP Sanatkumārasaṃhitā practically contains
all of SP2."

## Sources and method

- Pair table: `materials/presentation_2026/reuse_pairs.tsv`
  (`scripts/presentation/corpus_reuse_scan.py`: rapidfuzz ratio ≥ 80 on
  space-stripped akṣara streams, shingle-prefiltered, DF-capped;
  containment = matched fraction of the smaller text's lines).
- Threshold sweeps run in-session (same cstream convention, fuzz.ratio /
  fuzz.partial_ratio of each SP2 line against all 4,787 SKS lines).
  Noise-floor calibration from `build_noreuse_corpus.py`: unrelated
  control pairs max out at ratio 63–67.

## Findings

**1. SKS is the only substantial sharer.** reuse_pairs at ratio 80:
SKS 0.273 (187/686 SP2 lines); then a cliff — every other partner ≤
0.003 (Bhaviṣya, Garuḍa-2, Liṅga-1, MBh 12/14, Padma at 2 lines;
~20 others at 1). The Vāyu's own Pāśupata-yoga unit shares essentially
nothing verbatim (1 line) — confirming `pasupata_shared_text.py`
(2026-07): SP2/Vāyu-Pāśupata convergence on the map is register, not
borrowing.

**2. "Practically all" is not supported at wording level.** Full-ratio
sweep, fraction of SP2's 686 lines with an SKS match: ≥80 27.4%,
≥75 31.2%, ≥70 34.3%, ≥65 37.2%, ≥60 43.9%, ≥55 60.9%. The curve is
smooth — no hidden mass just under the cutoff. Below ~63 unrelated texts
also begin to "match", so the ≥55 figure includes false positives.

**3. Kengo's ~60 working threshold is supported for śloka lines.**
Manual read of the 176 pairs in the 55–68 band: above ~60, genuine
reworked parallels (nāḍī doctrine incl. the dvisaptatisahasrāṇi nāḍīnām
line, agnīṣomātmakaṃ…, the nāḍī name-list gāndhārī/vijayā, the sacred
sites kedāra…himālaye/mahālaye, sthitihetuḥ śarīriṇām); below ~58,
mostly pāda-cadence coincidence (na saṃśayaḥ / prakīrtitaḥ /
samudāhṛtaḥ line-ends gluing unrelated lines).

**4. Segmentation artifact is real but marginal.** One 63-scored pair is
verbatim containment (SP2's sarve te jvaladarka-vahni-vapuṣas… embedded
in a longer concatenated SKS line, penalized by full ratio). But
partial_ratio sweeps track full-ratio at comparable levels (≥80: 27.8%
vs 27.4%) — different half-śloka segmentation costs only a handful of
lines.

**Bottom line:** ~27% of SP2 is near-verbatim in SKS, rising to ~40–44%
genuine at the 60-threshold (the extra being clearly reworked
parallels). If SKS really absorbed all of SP2, more than half was
recomposed thoroughly enough to be invisible to fuzzy string matching.
Reverse direction: SKS ↔ full `skandapurana` containment 0.198 (960 of
SKS's 4,856 lines) — SKS's SP borrowing extends beyond the SP2 section.

**Open lead (not run):** group the unmatched SP2 lines by adhyāya —
clustering would mean SKS took a chapter subset; even scatter favors
"absorbed everything, rewrote freely."
