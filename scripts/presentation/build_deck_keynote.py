#!/usr/bin/env python3
"""Build the chronology deck as a native Keynote presentation.

Drives Keynote (>= 15, the app answering bundle id com.apple.Keynote) via
AppleScript: theme Basic White, 1920x1080, every text set to SF Pro Display.
Content mirrors materials/presentation_2026/slides_draft.md — same words as
scripts/presentation/build_deck.js, restyled to Keynote's own layouts:

  - text slides  : Title & Bullets placeholders (Apple defaults untouched)
  - big claims   : Title - Center layout
  - figure slides: Blank layout + full-bleed PNG
  - tour slides  : full-bleed PNG + a text box over the map's empty
                   bottom-left corner
  - tables (7/8) : native Keynote tables

Output: materials/presentation_2026/chronology_stratification.key
(saved via Keynote; the pptx deck remains the fallback build).

Usage: python3 scripts/presentation/build_deck_keynote.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FIG = ROOT / 'materials/presentation_2026/figures'
OUT = ROOT / 'materials/presentation_2026/chronology_stratification.key'
FONT = 'SF Pro Display'

L = []          # AppleScript lines accumulated inside the tell-document block


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def q(s):
    return '"' + esc(s) + '"'


def new_slide(layout):
    L.append(f'set sl to make new slide at end of slides of doc '
             f'with properties {{base layout:slide layout {q(layout)} of doc}}')


def set_title(text):
    L.append(f'tell sl to set object text of default title item to {q(text)}')
    L.append('tell sl to set font of object text of default title item '
             'to "SFProDisplay-Bold"')


def set_body(lines):
    body = ' & return & '.join(q(t) for t in lines)
    L.append(f'tell sl to set object text of default body item to {body}')
    L.append('tell sl to set font of object text of default body item '
             'to "SFProDisplay-Regular"')


def add_note(text):
    L.append(f'set presenter notes of sl to {q(text)}')


def add_image(path, x=0, y=0, w=1920):
    L.append(f'tell sl to make new image with properties '
             f'{{file:POSIX file {q(str(path))}, position:{{{x}, {y}}}, '
             f'width:{w}}}')


def add_text_item(text, x, y, w, size=28, bold=False, italic=False,
                  color=None, align=None):
    L.append(f'tell sl to set ti to make new text item with properties '
             f'{{object text:{q(text)}, position:{{{x}, {y}}}, width:{w}}}')
    fname = 'SFProDisplay-Bold' if bold else 'SFProDisplay-Regular'
    L.append(f'set font of object text of ti to {q(fname)}')
    L.append(f'set size of object text of ti to {size}')
    if color:
        r, g, b = color
        L.append(f'set color of object text of ti to '
                 f'{{{int(r*65535)}, {int(g*65535)}, {int(b*65535)}}}')



def add_table(rows, x, y, w, col_ws, header=True, size=20, row_h=95):
    nr, nc = len(rows), len(rows[0])
    L.append(f'tell sl to set tb to make new table with properties '
             f'{{row count:{nr}, column count:{nc}, '
             f'header row count:{1 if header else 0}, header column count:0, '
             f'position:{{{x}, {y}}}, width:{w}}}')
    for r, row in enumerate(rows, 1):
        for c, val in enumerate(row, 1):
            L.append(f'tell tb to set value of cell {c} of row {r} '
                     f'to {q(val)}')
    L.append(f'tell tb to set height of every row to {row_h}')


def fig_slide(name, notes, card=None):
    new_slide('Blank')
    add_image(FIG / f'{name}.png')
    if card:
        add_text_item('\n'.join(card), 70, 770, 560, size=19)
    if notes:
        add_note(notes)


BLUE = (0.12, 0.37, 0.66)

# ══ Slides ════════════════════════════════════════════════════════════════════

# 1 · Title
new_slide('Title')
set_title('Chronological Stratification in the Epics and Purāṇas')
L.append('tell sl to set object text of default body item to '
         + q('Evidence from Stylometric Seriation — Kengo Harimoto · '
             'DICSEP 11 · 4 August 2026'))
add_note('Thirty seconds; straight into the picture.')

# 2 · The map
fig_slide('hero_W1_delta_MDS',
          'Let the audience find their texts. Epics left, old purāṇic core '
          'upper middle, sectarian digests right, Bhāgavata below. One color '
          '= one stratum of the RECEIVED chronology, not of the computation. '
          'MBh 12 and 13 nicely to the right.')

# 3 · The claim
new_slide('Title & Bullets')
set_title('This map was drawn by counting linguistic habits — nothing else')
set_body(['no dates', 'no chronology', 'no philological judgment',
          '— none of it entered the computation; '
          'the colors were painted on afterwards'])
add_text_item('Yet the familiar relative chronology reads left to right.',
              200, 910, 1520, size=34, bold=True, color=BLUE, align='center')
add_note('The coloring is the only place received scholarship touches the '
         'plot; the geometry is blind.')

# 4 · The question
new_slide('Title & Bullets')
set_title('Two questions worth thirty minutes')
set_body(['What exactly was counted?',
          'Can the left–right axis be trusted — '
          'or is it an artifact of one method?'])
add_note('Roadmap: first how the map is made, then a guided tour, then the '
         'robustness case, then honest caveats.')

# 5 · The corpus
new_slide('Title & Bullets')
set_title('The corpus: 111 texts and sections · ≈ 4.8 million words')
set_body(['Mahābhārata by parvan (18) · Rāmāyaṇa by kāṇḍa (7)',
          'purāṇas whole, or by khaṇḍa / saṃhitā where transmission '
          'demands it',
          'machine-readable editions, cleaned — two parallel versions of '
          'every text: with and without sandhi dissolved',
          'sections differ enormously in length; short fragments are marked '
          'with smaller dots on every map'])
add_note('One line on e-text provenance; do not linger.')

# 6 · Countable habits (figure)
fig_slide('mfw_habits',
          'Left: the features are ca, tu, eva, na, sa, tathā — grammatical '
          'glue, not content. Nobody composes with their rate of tu in '
          'mind. Right: the old purāṇic core uses tu/eva/tathā/vai about '
          '1.5–3x as often as the Mahābhārata; the Bhāgavata suppresses all '
          'four. These boring words carry the signal.')

# 7 · From counts to distances
new_slide('Title & Bullets')
set_title('From counts to distances')
set_body(['for each pair of texts: how differently do they use their most '
          'common words?',
          'similar habits → small number · different habits → large number',
          'result: a 111 × 111 table of stylistic distances',
          '(Burrows’s Delta — stylometry’s standard workhorse since 2002)'])
add_table([['pair', 'distance'],
           ['MBh 7 (Droṇa) ↔ MBh 8 (Karṇa)', '0.28'],
           ['Vāyu ↔ Brahmāṇḍa', '0.28'],
           ['typical pair in this corpus', '1.04'],
           ['Rām 2 (Ayodhyā) ↔ Agni', '1.34']],
          x=1150, y=620, w=680, col_ws=[500, 180])
add_note('No formulas: an average of disagreements in word habits, in units '
         'of what is normal for this corpus. Table rows preview later tour '
         'stops.')

# 8 · Two independent lenses
new_slide('Title & Bullets')
set_title('The same corpus, measured twice')
add_table([['', 'Lens 1 — words', 'Lens 2 — letter groups'],
           ['counts', 'the 80 most frequent words',
            'the 5,000 most frequent 3-letter sequences'],
           ['input', 'sandhi dissolved (segmented)', 'raw sandhied text'],
           ['sees', 'particles, pronouns, vocabulary habits',
            'morphology, phonology']],
          x=160, y=300, w=1600, col_ws=[220, 690, 690], row_h=115)
add_text_item('Independent failure modes: nothing that could fool one lens '
              'can fool the other.', 200, 930, 1520, size=30, bold=True,
              color=BLUE, align='center')
add_note('Flag now, cash in at Act 4: any segmentation-pipeline artifact '
         'could only touch Lens 1; any orthographic/sandhi artifact only '
         'Lens 2.')

# 9 · MDS explainer
fig_slide('mds_explainer',
          'Mileage-chart analogy: given only road distances between cities '
          'you can redraw the map of India. MDS does exactly that with '
          'stylistic distances. The opening map is this with the full '
          '111×111 table. Axes mean nothing by themselves; only nearness '
          'does.')

# 10-15 · The tour
fig_slide('hero_W1_delta_MDS_hl-epic',
          'The epic zone: parvans and kāṇḍas mingle; MBh and Rām overlap. '
          'The didactic parvans 12-13 sit to the right of the battle books.',
          card=['THE EPIC ZONE',
                'parvans and kāṇḍas mingle',
                'MBh 12–13 pull right, toward the purāṇas'])
fig_slide('hero_W1_delta_MDS_hl-oldcore',
          'The old purāṇic core: Vāyu, Brahmāṇḍa, Mārkaṇḍeya, Matsya, '
          'Viṣṇu. Vāyu ↔ Brahmāṇḍa at 0.28 — Kirfel’s Vāyuproktaṃ Purāṇam, '
          'as a number.',
          card=['THE OLD PURĀṆIC CORE?',
                'Vāyu ↔ Brahmāṇḍa: 0.28 — Kirfel, as a number',
                'Viṣṇu ↔ Mārkaṇḍeya: mutual nearest neighbours',
                'Matsya’s cosmogonic chapters sit with them'])
fig_slide('hero_W1_delta_MDS_hl-oldsp',
          'The old Skandapurāṇa: mostly with the old core; the Pāśupata '
          'chapters (SP2) jump far right — doctrine added later than the '
          'narrative bulk.',
          card=['THE OLD SKANDAPURĀṆA',
                'the narrative bulk sits with the old core',
                'the Pāśupata chapters plot far right: added later'])
fig_slide('hero_W1_delta_MDS_hl-late',
          'The sectarian & encyclopedic mass: one broad stratum, no clean '
          'middle/late line; digests at the far right.',
          card=['THE SECTARIAN & ENCYCLOPEDIC MASS',
                'one broad, continuous stratum',
                'Agni · Garuḍa · Nārada crowd the far right'])
fig_slide('hero_W1_delta_MDS_hl-skmp',
          'The Skāndamahāpurāṇa, khaṇḍa by khaṇḍa: 0 of 4 khaṇḍas have '
          'their nearest neighbour inside the SkMP, in either lens; the '
          'reuse scan finds they share no text with one another. What '
          'connects them is a phrase in the colophons. The Śivapurāṇa '
          'tells the same story. Revākhaṇḍa: nearest neighbour is the '
          'other Revākhaṇḍa, transmitted with the Vāyu — ~5% shared lines.',
          card=['A PURĀṆA THAT REFUSES TO UNIFY',
                'SkMP: 0 of 4 khaṇḍas have an internal neighbour',
                'they share no text; only colophons connect them'])
fig_slide('hero_W1_delta_MDS_hl-bhp',
          'The Bhāgavata: all twelve skandhas’ nearest neighbours are '
          'internal — in both lenses. Archaic features noticed for over a '
          'century; a date never settled. The counts find two layers that '
          'do not match. The numbers do not settle its date; they deepen '
          'its puzzle.',
          card=['THE BHĀGAVATA',
                'all 12 skandhas: internal neighbours, both lenses',
                'epic-like bulk + a thin layer of Vedic particles'])

# 16 · Robustness grid
fig_slide('robustness_grid',
          'Walk the grid: top row words/unsandhied, bottom row '
          '3-grams/sandhied, three distance metrics each — six independent '
          'pipelines, one geometry. Layout agreement with the opening map: '
          '0.95-0.96 (words), 0.82-0.89 (3-grams).')

# 17 · Convergence argument
new_slide('Title & Bullets')
set_title('Suppose the axis were an artifact…')
set_body(['a flaw in sandhi segmentation → could distort the word lens only',
          'an orthographic / sandhi convention → could distort the 3-gram '
          'lens only',
          'a quirk of one distance formula → fails to explain the other '
          'five'])
add_text_item('The signal is in the texts.', 200, 890, 1520, size=40,
              bold=True, color=BLUE, align='center')
add_note('The abstract’s core argument; deliver slowly. The lenses share '
         'almost no assumptions — yet draw the same axis.')

# 18 · The second axis
new_slide('Title & Bullets')
set_title('What the second axis is not')
set_body(['the vertical axis is unstable across configurations',
          'depending on features and metric it separates by something like '
          'genre, region, or sectarian register — no labeling survives all '
          'six panels',
          'honest conclusion: one axis is chronology-like and robust; the '
          'second resists a stable name'])
add_note('Promised in the abstract; agnosticism as a feature, not a '
         'weakness. The Bhāgavata’s vertical displacement is the clearest '
         'case.')

# 19 · Confounds
new_slide('Title & Bullets')
set_title('What the axis is made of')
set_body(['“diachronic linguistic drift” — but confounded:',
          'authorial aptitude: the better the author, the fewer the '
          'metrical fillers',
          'reuse of preexisting material: shared materials pull the '
          'containers together (B8)',
          'genre: when the vocabularies are completely different, there is '
          'no telling where they land'])
add_note('Look at where the final parvans of the MBh landed — exactly the '
         'parvans whose relative dates are contested. And the '
         'Śivadharmaśāstra and Śivadharmottara: the purāṇas known to '
         'incorporate them are very much to the left. MFWs tend to be '
         'fillers; inapt authors rely on them. The Bhāgavata: an old '
         'problem, shows in our map (B7). Mode of compilation: the '
         'Bhaviṣya (B8, B9).')

# 20 · The point
new_slide('Title & Bullets')
set_title('What’s the point of this?')
set_body(['confirms things we suspected: relative age of the epics; late '
          'didactic MBh; affinities of purāṇas',
          'illuminates contentious issues: the closing parvans; MBh and '
          'Rām composed about the same time',
          'it will not date your text; it will tell you whose company it '
          'keeps',
          'and it shows where interesting things are happening: the '
          'Bhāgavata’s uniqueness, the closing parvans’ composition date, '
          'the Bhaviṣya’s provenance …'])
add_note('This is the point of the whole talk: the counts make us look at '
         'old problems from a new angle, and the charts hand scholars '
         'hints about where to dig.')

# 21 · Closing
new_slide('Blank')
add_image(FIG / 'hero_W1_delta_MDS.png', x=0, y=120, w=1920)
add_text_item('Counted habits, familiar history and familiar problems.',
              200, 20, 1520, size=34, bold=True)
add_note('End where we began — now everyone can read the map. Thanks; over '
         'to questions.')

# ── Backups ──────────────────────────────────────────────────────────────────
new_slide('Section')
set_title('Backup slides')

new_slide('Title & Bullets')
set_title('B1 · Burrows’s Delta, one level deeper')
set_body(['for each of the top-80 words: how far is each text from the '
          'corpus-average rate, in standard deviations (a z-score)?',
          'Delta(A, B) = the average disagreement of A and B across those '
          'words',
          'variants in the grid: Cosine Delta (angle instead of average); '
          'min-max and Manhattan (raw-frequency geometry)'])

fig_slide('corpus_key',
          'B2: the full 111-text key, by stratum.') \
    if (FIG / 'corpus_key.png').exists() else None

for name, note in [
    ('closing_parvans_length', 'B3/B6: the length caveat, in one figure.'),
    ('lens_disagreement', 'B4: when the lenses disagree — a diagnostic.'),
    ('consensus_tree', 'B5: majority-rule consensus, 500 replicates.'),
    ('bhp_skandha_mfw', 'B7: the Bhāgavata, book by book.'),
    ('reuse_overlay_MDS', 'B8: is the map just a borrowing web? Reuse '
                          'overlay on the hero layout.'),
    ('bhavisya_reuse_strip', 'B9: the Bhaviṣya — a text that is mostly '
                             'other texts; 53% of pāda-units matched; '
                             'donors incl. Manu, Śivadharma corpus, '
                             'Bṛhatsaṃhitā, the Buddhist ŚKA; per-block '
                             'dating is the only dating it admits.'),
    ('companion_C3_manhattan_MDS', 'B10: the same map in the 3-gram lens.'),
]:
    if (FIG / f'{name}.png').exists():
        fig_slide(name, note)

# ══ Run ═══════════════════════════════════════════════════════════════════════
# Hand-edit guard: after every build we stamp the .key's mtime. If the file on
# disk is newer than the stamp, someone edited it in Keynote since the last
# build — refuse to overwrite unless --force is given.
STAMP = OUT.with_suffix('.key.buildstamp')
if OUT.exists() and STAMP.exists() and '--force' not in sys.argv:
    if OUT.stat().st_mtime > float(STAMP.read_text()) + 5:
        sys.exit(f'REFUSING to overwrite {OUT.name}: it was modified in '
                 'Keynote after the last build (hand edits would be lost). '
                 'Re-run with --force to overwrite anyway.')
body = '\n'.join(L)
script = f'''
tell application id "com.apple.Keynote"
    set doc to make new document with properties ¬
        {{document theme:theme "Basic White", width:1920, height:1080}}
    delay 1
    tell doc
{body}
        delete slide 1
    end tell
    save doc in POSIX file "{OUT}"
    return "saved " & (count of slides of doc) & " slides"
end tell
'''
r = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip())
if OUT.exists():
    STAMP.write_text(str(OUT.stat().st_mtime))
