# BhP quotes, round 2: fuzzy sweep with the E-texts toolkit

2026-08-17. Follow-up to `2026-08-17_bhp_unnamed_quotes_library_sweep.md`
(exact shingle scan). Kengo asked for the fuzzy version using the tools in
`E-texts/40_tools`. Those tools turn out to carry a whole prior BhP
project (July 31 – Aug 5: `reports/bhp_parallels/` — pāda- and
hemistich-level `bhavisya_scan.py` runs at rapidfuzz ratio ≥ 0.70,
`bhp_quotations.py` citation view, `bhp_attributions.py` named-attribution
classifier, `bhp_semantic_scan.py`).

## What was run

The July runs left `--normalise-cand-length` OFF (kept off for report
reproducibility). That is exactly the recall hole the exact sweep exposed:
a full-śloka source line (Hitopadeśa) or a pāda-per-line long-metre verse
(Subhāṣitaratnakoṣa) against a *hemistich* target unit is capped at ratio
2·min/(l₁+l₂) ≈ 0.66 — structurally below the 0.70 floor however perfect
the quote. Re-ran the identical hemistich pipeline with the flag ON
(96 workers, ~6 min, 6,381 files):

`bhavisya_scan.py --target bhph_target.txt --newline-units
--normalise-cand-length --prefix bhph --out-dir
40_tools/reports/bhp_parallels/normcut` → `normcut/bhph_pairs.tsv`
(105,795 rows; BhP's own copies now included = positive control, 99.1% of
units matched), delta vs July in `normcut/delta.md`
(`compare_scan_runs.py`): 7,500 → 27,433 units matched, 152 works newly
visible, 1 lost.

## Verdict on the question: the pre-1000 negative HOLDS under fuzz

Every fresh solid (≥ 0.85) row in a pre-1000 author resolves to mediated
material, same classes as the exact sweep:

- Sureśvara (BAU-vārttika), Maṇḍana (Brahmasiddhi), Śaṅkara-bhāṣya files:
  Muṇḍaka 2.2.8 — which the BhP uses TWICE (1.2.21 and 11.20.30) — and
  Manu 12.91 ("sarvabhūteṣu cātmānam…", introduced "manunā ca" in
  Govindānanda), Manu 2.94, and the floating "pravṛttaṃ ca nivṛttaṃ ca"
  dharma verse (= BhP 7.15.47).
- Yuktidīpikā: Manu 2.94 ("āha ca — na jātu kāmaḥ…"). Its other overlap
  ("dharmo jñānaṃ vairāgyam aiśvaryam") is the standard Sāṃkhya
  buddhi-bhāva list (SK 23) that BhP 11 absorbs — doctrine, not quote.
- Abhinavagupta, Gītārthasaṃgraha: all Gītā verses the BhP itself reuses
  (Gītā 3.5, 3.21, 9.26, 10.15 = BhP 6.1.53, 6.2.4, 10.81.4, 8.22.21).
- Udayana, Kiraṇāvalī: "caturyugasahasraṃ tu brahmaṇo dinam" cosmological
  commonplace (Manu 1.72 / Gītā 8.17 sphere).

Also killed two would-be sensations from the July attribution table, both
editorial: Māṭhara's three "strong" attributions are the *editor's*
bracketed traces (`[bhāgavatapurāṇa, 1|8|52]` — one of them to the
Devībhāgavata!); Yāmuna's "śrīmadbhāgavate yathā'ha" in the
Āgamaprāmāṇya sits inside an editorial parenthesis interrupting an
Īśvarasaṃhitā quotation (noting the BhP 11.6.46 parallel). Yāmuna's own
text remains clean.

## What fuzz genuinely adds

1. **Māṭhara, fuller and with variants**: both hemistichs of BhP 1.8.52
   at 0.94 (Māṭhara reads *tathaivemāṃ* vs BhP *tathaivaikāṃ*), plus BhP
   1.6.35 at 0.80/0.88 with the telling variant **yad ācāryānuvartanam**
   vs BhP *haricaryānuvarṇanam* (a de-Vaiṣṇavized reading!). The crux
   sharpens: two unnamed quotes, one adapted.
2. **Hitopadeśa carries 3–4 BhP verses**, not one: 10.1.38 (1.00),
   10.22.35 (0.90–0.91, reading *śreya evācaret sadā*), 10.60.15 (0.88),
   11.10.20 (0.84).
3. **The anthology kūrma verse confirmed in both collections**: SKM 0.95–
   0.96 and now the "+"-encoded Vidyākara SRK 0.85–0.93 (the July miss
   was pure unit-granularity + the exact scan had already caught it).
4. **Article-relevant surprise — BhP 9 reproduces the PPL vaṃśa stock
   verbatim**: 185 rows against Kirfel's Pāñcalakṣaṇa Textgruppe I
   (median 0.75, **35 hemistichs ≥ 0.85, many at 1.00**: "yaduṃ ca
   turvasuṃ caiva devayānī vyajāyata", "mātā bhastrā pituḥ putro…",
   "ṣaṣṭiṃ varṣasahasrāṇi…", "dhṛtarāṣṭraṃ ca pāṇḍuṃ ca viduraṃ cāpy
   ajījanat"). Direction: BhP ← the old genealogical corpus. So the BhP
   does verbatim-inherit pañcalakṣaṇa material where its content is
   vaṃśa — one more concrete piece for the BhP-sources discussion
   (alongside its MBh formulae and ViP kṛṣṇacarita kinship), and a
   counterweight to over-reading its "almost no shared text" profile:
   the sharing is there, exactly where the genre is.

## Standing conclusion (unchanged, now double-checked)

Exact and fuzzy agree: no BhP-distinctive quotation, named or unnamed,
in any securely datable author before ~1000; earliest genuine carriers
are the floating-verse/anthology sphere (Hitopadeśa, Vidyākara ~1100,
SKM 1205 — the kūrma verse *anonymous* there), purāṇic absorption
(Sūtasaṃhitā, Padma, Skanda), then Madhva → Gauḍīya avalanche. Māṭhara
remains the sole — and dating-circular — possible exception. Caveats as
before: Utpala Vaiṣṇava's Spandapradīpikā not in the library; al-Bīrūnī
out of scope; plus the July semantic scan (`bhp_semantic_hits.tsv`,
labse-mitra) exists for paraphrase-level echoes if we ever want a third
channel.
