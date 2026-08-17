# BhP quotes, round 3: the semantic channel (paraphrase-level echoes)

2026-08-17. Third and last channel after the exact shingle sweep and the
fuzzy rerun: the July session's labse-mitra semantic scan
(`bhp_semantic_scan.py`; every BhP verse embedded, nearest chunks from
the 1.8M-chunk library index, k=5 per verse, results in
`bhp_semantic_hits.tsv`, 1,885 rows). No re-run needed — the existing
run's semantic-only complement (1,588 rows with no string-level
counterpart; 1,060 outside the Gauḍīya/purāṇic/epic spheres, 405 works)
was read for the early-witness question.

## Verdict: no paraphrase-level early witness either

Every semantic-only hit in a datable pre-1200 author, read side by side,
resolves to one of four non-quotation categories:

1. **The same floating verses yet again** — the top Śaṅkara-sphere hit
   (Yogasūtravivaraṇa, 0.712) is Manu 2.94 ("na jātu kāmaḥ…") verbatim,
   recovered *through OCR corruption* ("śāṃyati") that had blinded both
   string scans. Good recall, same verdict: Manu-mediated, not BhP.
2. **Genre formulae** — phalaśruti idiom (Gītābhāṣya 18.71 vs BhP
   4.23.31), devotional address idiom (Gītā mac-cittāḥ… vs BhP 10.46.4),
   stava style (Udayana's Nyāyakusumāñjali vs BhP 11.28.31).
3. **Doctrinal commonplaces** — Vedāntic deha-tādātmya prose near BhP
   4.20.5 (Sūtasaṃhitā-ṭīkā), sattva/guṇa doctrine, cosmological lists.
4. **Descriptive-register topoi + embedding hubness** — Bāṇa (36
   Harṣacarita rows!), Haravijaya, Naiṣadhīya, Divyāvadāna, Bṛhatsaṃhitā
   all land near the BhP's densest compound-heavy description verses;
   the same hub verses (8.7.15, 9.10.16, and blocks of skandha 2) hit
   their k=5 cap across unrelated works. Ornate prose embeds near ornate
   verse regardless of dependence.

The Gītagovinda (12th c.) deserves its own line: 4 semantic-only rows,
all thematic (Kṛṣṇa-with-gopīs subject matter), no verse-level
dependence surfaced — consistent with the timeline (post-1100) either
way, and evidence for nothing.

Māṭhara and Hitopadeśa have zero semantic-only rows (their quotes are
all fuzzy_known — the string channels already own them).

## Standing conclusion, now three-channel

Exact shingles, length-normalized fuzzy matching, and semantic
embeddings agree: **no BhP-distinctive presence — verbatim, variant, or
paraphrase — in any securely datable author before ~1000.** The earliest
carriers stay what they were: Māṭhara (dating-circular), the
floating-verse/anthology sphere (Hitopadeśa; Vidyākara ~1100; SKM 1205,
anonymous), purāṇic absorption, then Madhva → Gauḍīya. A further
lowering of the semantic threshold would add topical noise, not signal —
the channel is exhausted for this question. (Its one demonstrated
strength worth remembering for other problems: OCR-robust recall of
quotes both string scans miss.)
