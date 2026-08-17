# Unnamed BhP quotes: verbatim-reuse sweep of the whole E-texts library

2026-08-17. Kengo's question: the named-reference history of the BhP is
late (early 2nd millennium) — do *unnamed* verbatim quotes tell a
different story? Method upgrade over the name-sweeps: shingle scan, not
grep. Everything normalized to a bare IAST letter stream (lowercase, all
whitespace/punctuation/digits stripped); every 21-mer of the BhP indexed
(GRETIL `unknown_bhagavatapurana_all.txt`, 1.31M chars, 30,987 pādas);
7,062 library files scanned at stride 10 (guarantees any common substring
≥ 30 chars ≈ half-śloka); hits extended to maximal matches. 7,881 rows.
Script + full TSV: `materials/presentation_2026/figures/library_sweeps/bhp_reuse/`.

## False-positive classes (each verified, then discounted)

1. **Śruti/Gītā embedded in the BhP itself**: Muṇḍaka 2.2.8 = BhP 1.2.21
   ("bhidyate hṛdayagranthiḥ…" — accounts for the hits in Śaṅkara,
   Udayana, Sūtasaṃhitā-ṭīkā, YV…); Taittirīya-Āraṇyaka 1.2 = BhP
   11.19.17 ("smṛtiḥ pratyakṣam aitihyam…" — Udayana quotes the Veda,
   not the BhP); Gītā 9.26 = BhP 10.81.4 (the Jñāneśvarī hits).
2. **Floating smṛti verses**: Manu 2.94 = MBh (Yayāti) = BhP 9.19.14;
   the "nārāyaṇaṃ namaskṛtya" maṅgala; metre lists (NŚ 14.107 ≈ BhP
   11.21.41).
3. **Editorial apparatus in the e-texts**: the spectacular 385-char
   "Śivadharma" match is the *editor's* `%%` note quoting BhP 5.26.6 for
   comparison; the Bhagavadajjukīya hit is an editorial NB about its
   (late) commentator quoting "Śrīmadbhāgavata" (BhP 10.51.19).
4. **Commentary bundled with mūla**: the "Śaṅkara Taittirīya-bhāṣya" hit
   (BhP 3.28.37) sits in Vidyāraṇya's 14th-c. dīpikā printed in the same
   Ānandāśrama volume; the Yogavāsiṣṭha hits (BhP 1.2.23 etc.) are in
   Ānandabodhendra's ṭīkā; Bhavabhūti/Murāri hits are in Vīrarāghava
   etc.; the Parātrīśikāvivṛti quoting "bhāgavate 'pi purāṇe" (BhP
   10.87.24, 10.2.10ff) is by **Rājānaka Lakṣmīrāma, 19th c.** — not
   Abhinavagupta.

## Directionality: the epic-purāṇic overlaps are the BhP's *sources*

MBh 263 rows (median 37 chars), HV 173, ViP 93: epic formulae ("atrāpy
udāharantīmam itihāsaṃ purātanam"), episode kinship (BhP 7.2 ← MBh
12.221ff consolation; BhP 10 kṛṣṇacarita ← HV / ViP 5). Nothing
approaching śloka-length distinctive borrowing *from* the BhP in any of
them. This refines the earlier corpus-internal finding ("BhP shares
almost zero text"): at half-śloka grain the kinship is visible, but it
is inheritance, not quotation.

## The genuine BhP-being-quoted finds, oldest first

| witness | what | assessment |
|---|---|---|
| **Māṭharavṛtti** (on SK 2) | BhP 1.8.52 "yathā paṅkena paṅkāmbhaḥ surayā vā surākṛtam / bhūtahatyāṃ tathaiv[a]…" verbatim, introduced "kiñ ca" — **unnamed**; also BhP 1.6.35 partial ("āturacittānāṃ mātrāsparśecchayā") | the verse occurs NOWHERE else in the 1-GB library — genuinely BhP-distinctive. Known crux: dated 5th–6th c. by those who date it from Paramārtha's Chinese (557–569), but the extant vṛtti is generally taken as a later expansion of what Paramārtha translated, *partly because of* quotes like this. Dating value circular; cite as the crux it is, not as an anchor |
| **Hitopadeśa** (Nārāyaṇa; 10th–14th c., before the 1373 ms) | BhP 10.22.35 "etāvaj janmasāphalyaṃ dehinām iha dehiṣu / prāṇair arthair dhiyā vācā śreya[ḥ]…" — **unnamed** ("anyac ca"); BhP 10.1.38 half-verse | real unnamed quote in a floating-verse compilation; Sternbach traced Hit.'s stock to nīti/purāṇic sources. Undatable narrowly |
| **Vidyākara, Subhāṣitaratnakoṣa** (~1100, Buddhist, Bengal) + Saduktikarṇāmṛta (1205) | the kūrma maṅgala = BhP 12.13.2, full śloka; SKM attributes it "**kasyacit**" — *of someone* | the verse circulates c. 1100 but is NOT credited to the BhP; and BhP 12.13.1–3 are themselves anthology-style benedictions, so direction is arguable both ways |
| **Sūtasaṃhitā** (mūla; before its 14th-c. commentator Mādhava) | BhP 3.10.14–17 (the ten-sarga taxonomy) absorbed verbatim, **unnamed**, in the śivamāhātmyakhaṇḍa; the ṭīkā separately quotes BhP *named* ("uktaṃ bhāgavate") | purāṇic absorption into a Śaiva compendium, pre-1300 |
| **Padmapurāṇa** (late khaṇḍas) | long verbatim blocks — 252 chars of BhP 3.23 (Kardama), BhP 11.2–3, 11.27 — mostly **unnamed**; plus the named Bhāgavatamāhātmya sphere | the clearest "unnamed quotes" in a purāṇa; strata undatable independently. Same pattern smaller in Skanda, Garuḍa; DBhP 142 rows (sibling text) |
| **Madhva sphere** (13th c.) → **Gauḍīyas** (16th c.) | Anuvyākhyāna, Jayatīrtha; then the explosion: Jīva's sandarbhas alone ~2,500 rows, Gopālabhaṭṭa, Rūpa | the named-quotation avalanche, as known |

## The negative result (the payoff)

After removing the four false-positive classes, there is **not one
BhP-distinctive quote, named or unnamed, in any securely datable author
before ~1000** in 964 MB of Sanskrit: Śaṅkara, Maṇḍana, Sureśvara,
Kumārila, Vācaspati, Udayana, Bhāsarvajña, the early ālaṃkārikas, the
Kashmir Śaiva mūla corpus, pre-nibandha dharmaśāstra — all clean.
**Yāmuna (~1050; Āgamaprāmāṇya, Ātmasiddhi, Stotraratna all present):
zero rows** — and Rāmānuja likewise (Gītā-mediated only) — reproducing
the famous early-Śrīvaiṣṇava silence.

So the unnamed-quote channel tells the same story as the named-reference
channel: the BhP's verbatim footprint in datable literature starts,
gingerly, in the anthology/compendium sphere around the 11th–13th c. and
becomes an avalanche only with Madhva and the Gauḍīyas. The argument for
a late quotation history does NOT rest on citation etiquette. The one
textual witness that could upset this — the Māṭharavṛtti — is exactly
the one whose own date is decided by how one dates the BhP.

## Caveats

- **Utpala Vaiṣṇava's Spandapradīpikā (10th c.), the standard earliest
  named quoter, is NOT in the library** — untested here; the article
  must still cite it from the literature.
- Non-Sanskrit witnesses (al-Bīrūnī 1030) out of scope by design.
- Files in non-IAST encodings (HK/Velthuis `_hk`/`_au`/ASCII variants)
  are effectively invisible to the normalizer — a small blind spot.
- Threshold 30 normalized chars ≈ half-śloka: paraphrase and
  single-pāda echoes are below the radar by design (they cannot be
  distinguished from noise at library scale).
- E-text editions vary; a quote with heavy variants (>1 pāda divergence)
  splits into shorter fragments and may fall under threshold.
