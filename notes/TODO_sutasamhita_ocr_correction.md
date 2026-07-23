# TODO: Morphology-based OCR correction of the full Sūtasaṃhitā e-text

For a Claude Code session (Fable 5, Max plan — no API cost) to run overnight
or whenever convenient. Written 2026-07-23 after a validated pilot.

## Task

Correct the OCR noise in the complete Sūtasaṃhitā mūla e-text using Sanskrit
morphology, sandhi, lexicon, and meter. Text-only work — no PDF reading
needed except for flagged lines.

- **Input:**  `~/Documents/E-texts/00_inbox/New/sutasamhita_madras_mula_iast_clean.txt`
  (11,580 lines, IAST, all 4 khaṇḍas; from GCV OCR of the Madras ed.
  2015.483774 with Vidyāraṇya's Tātparyadīpikā, mūla separated by glyph height)
- **Output:** `~/Documents/E-texts/00_inbox/New/sutasamhita_madras_mula_iast_CORRECTED.txt`
  (same line structure, same verse numbers, corrections applied)
- **Progress file:** `~/Documents/E-texts/00_inbox/New/.sutasamhita_correction_progress`
  (last completed input line number — makes the job resumable/interruptible)

## OCR error profile (what to fix)

Systematic, from the low-res scan:
- anusvāra dropped everywhere: `satoṣa`→`saṃtoṣa`, `dhana`→`dhanaṃ`, `sasāra`→`saṃsāra`
- visarga dropped, esp. line-final: `budhai`→`budhaiḥ`, `tapa`→`tapaḥ`
- conjunct/akṣara misreads: `ma/bha` (`sitamasmā`→`sitabhasmā`), `pa/ṣa`
  (`vipavṛkṣa`→`viṣavṛkṣa`), `va/ba`, `cā drāyaṇa`→`cāndrāyaṇa`,
  `uyate`→`ucyate`, `ma trābhyāso`→`mantrābhyāso`
- spurious spaces inside words; daṇḍas gone (leave them gone — corpus style)
- verse-number digits sometimes mangled — correct only when obvious from
  sequence; never invent

Meter is the strongest check: mostly anuṣṭubh (8-syllable pādas, two per
line); some triṣṭubh/jagatī passages. A fix that breaks the syllable count
is wrong.

## Method (per chunk of ~50–60 lines)

1. Read the next chunk from the input.
2. Correct each line. Rules:
   - Fix only what morphology/meter/lexicon determines. Do NOT normalize
     orthographic variants the edition itself uses (b/v, geminates after r).
   - Keep line boundaries, spacing style, verse numbers, colophons.
   - **When uncertain, keep the OCR reading and append `⟨?⟩` to the line.**
     The pilot showed confidence is well-calibrated: every confident fix was
     right; all 3 genuine errors were in self-flagged spots. Do not guess at
     flagged spots — that is the whole safety design.
3. Append the corrected chunk to the output file; update the progress file.
4. Every ~20 chunks, spot-check 3 random corrected lines against the source
   PDF page (`[page N]` markers in the input give the page; PDF at
   `~/Documents/Books and Arrticles on iCloud/2015.483774.sutasamhita.pdf`,
   readable page-by-page with the Read tool).

## Validation reference (pilot, 2026-07-23)

Pilot region: input lines 2370–2426 (Jñānayogakhaṇḍa adhyāya 13 end + 14,
niyama chapter), scored against the independently typed witness
`~/Documents/E-texts/1_sanskr/6_sastra/3_phil/yoga/unknown_sutasamhita_jnanayogakhanda.txt`
(Ramya / Haṭha Yoga Project, Balamanorama ed.):
- raw OCR: 94.6% mean char similarity, 1/56 lines exact
- corrected: 97.7% mean, 46/56 exact; 2 residuals were witness typos
  (`kīrtikā`, `rāgadyapetaṃ`), 2 were edition orthography (b/v, geminate),
  3 were flagged-uncertain guesses (true readings: `tantrasaṃbandhavarjitaḥ`,
  `sarvāṅgoddhūlanaṃ`, `kecit tad vratam ity ūcuḥ`).

After the full run, repeat this scoring on the whole Jñānayoga witness
overlap (563 matched lines) as the acceptance check; then review `⟨?⟩` lines
against page images.

## After completion

- Report: number of lines changed, number flagged `⟨?⟩`, witness score.
- The corrected text stays in E-texts (it is a reference e-text, not a
  stylometric_works corpus unit). If the ŚiP/SkMP corpus later wants
  khaṇḍa-level units from it, that is a separate decision.
- Related session state: memory file `project_chronology_presentation.md`
  and `reference_pdf_to_vision_json.md` (provenance of the input file).
