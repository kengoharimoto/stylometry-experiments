# bhavisyapurana_brahmaparvan_adhyaya-5 — excluded 2026-07-22

Bhaviṣyapurāṇa, Brahmaparvan adhyāya 5 (`strīṇāṃ śubhalakṣaṇavarṇanam`),
587 words. Removed from the 101-unit epic/purāṇa corpus, which is now 100 units.

**It is a duplicate.** The same passage is already inside `bhavisyapurana.txt`.
The two copies come from different e-texts and use opposite word-division
conventions, which is why a naive string search does not find the overlap:

| whole text | this fragment |
|---|---|
| `grahaṇāntikameva ca` | `grahaṇaṃtikam eva ca` |
| `vedānadhītya` | `vedān adhītya` |
| `āsīnamarhayetprathamaṃ` | `āsīnam arhayet prathamaṃ` |

**It is the worse copy.** Errors absent from the whole text: `divjaśārdūla`
for `dvija-`, `strīṇaṃ` for `strīṇāṃ`, `savarṇaṃ` for `savarṇāṃ`, and one line
reading `striiṇaaṃ` — undigested Harvard-Kyoto doubled vowels that were never
transliterated.

**What it did to the map.** Delta to its own parent Bhaviṣyapurāṇa was 1.270,
i.e. further apart than the corpus median pair (1.041); its nearest neighbour
was the Agnipurāṇa. It held the 2nd-highest mean Delta of all 101 units, at
axis-1 +0.587, while the whole Bhaviṣya sits at +0.202 with mean Delta ranked
97th. At 587 words it is well below the size at which a position can be read at
all (see the length control in `scripts/presentation/pasupata_length_control.py`:
a 3,280-word unit already carries ±0.26 on an axis the corpus spans in 1.53).

**Worth keeping for the caveats slide.** Identical words, two transcription
conventions, and the map cannot tell they are the same text — an unplanned
controlled demonstration of the noise floor, and a live instance of the
orthographic failure mode that Slide 8 assigns to the 3-gram lens.
