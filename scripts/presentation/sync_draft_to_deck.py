#!/usr/bin/env python3
"""Push the draft's on-slide text into the live Keynote deck — draft-driven.

Reads the SAME parsed on-slide lines as check_draft_conformance.py (so what
is synced is exactly what the gate checks) and applies them to the open deck:

  - body slides : located by title, default body item replaced
  - tour cards  : located by their card's first line, text item replaced
  - B3/B4       : created as Title & Bullets slides after B1 if absent
  - B9          : bullet block added as a text item on the strip-figure slide
                  (located by its presenter notes)

Layout, images, and slides outside the mapping are never touched.

⚠ SUPERSEDED 2026-07-28: THE DECK IS THE AUTHORITY. This script runs
draft → deck, which is now backwards — the hand-edited .key governs and the
draft trails it. It therefore DRY-RUNS BY DEFAULT and needs an explicit
--force-overwrite-deck to touch the deck. To go the right way (deck → draft),
read dump_keynote_text.py's output and reconcile the draft by hand; drift is
listed by check_draft_conformance.py.

Usage: python3 sync_draft_to_deck.py [--dry-run | --force-overwrite-deck]
Then save is performed via Keynote; re-run the dump + drift report after.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_draft_conformance import draft_requirements  # noqa: E402


def strip_md(s):
    return (s.replace('**', '').replace('*', '')
             .replace('`', ''))


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def ret_join(lines):
    return ' & return & '.join(f'"{esc(strip_md(l))}"' for l in lines)


# draft section prefix -> ('body', deck slide title prefix)
#                       | ('card', card first-line marker)
#                       | ('new-after', anchor title prefix, own title)
#                       | ('panel-by-note', note fragment)
MAP = {
    'Slide 5 · The corpus': ('body', 'The corpus'),
    'Slide 7 · From counts to distances': ('body', 'From counts to distances'),
    'Slide 10 · The epic zone': ('card', 'THE EPIC ZONE'),
    'Slide 11 · The old purāṇic core?': ('card', 'THE OLD PURĀṆIC CORE?'),
    'Slide 12 · The old Skandapurāṇa': ('card', 'THE OLD SKANDAPURĀṆA'),
    'Slide 13 · The sectarian & encyclopedic mass':
        ('card', 'THE SECTARIAN & ENCYCLOPEDIC MASS'),
    'Slide 14 · A purāṇa that refuses to unify':
        ('card', 'A PURĀṆA THAT REFUSES TO UNIFY'),
    'Slide 15 · The Bhāgavata': ('card', 'THE BHĀGAVATA'),
    'Slide 17 · The convergence argument':
        ('body', 'Suppose the axis were an artifact'),
    'Slide 19 · What the axis is made of': ('body', 'What the axis is made of'),
    "Slide 20 · What's the point of this?": ('body', 'What’s the point of this?'),
    'B1 · Burrows': ('body', 'B1 · Burrows'),
    'B3 · The length caveat': ('new-after', 'B1 · Burrows',
                               'B3 · The length caveat'),
    'B4 · When the lenses disagree': ('new-after', 'B3 · The length caveat',
                                      'B4 · When the lenses disagree — '
                                      'a diagnostic, not a failure'),
    'B9 · The Bhaviṣya': ('panel-by-note', 'Bhaviṣya'),
}

# on-slide lines that are rendered outside the target element (e.g. a
# standalone tagline text item that already exists) — dropped from bodies
ALREADY_ELSEWHERE = {
    'The signal is in the texts.',
}


def main():
    # THE DECK IS THE AUTHORITY (Kengo, 2026-07-28). This script pushes the
    # DRAFT into the deck, i.e. the wrong way round: the draft now lags the
    # hand-edited .key, so an unguarded run overwrites Kengo's live wording
    # with stale prose. Default to dry-run; writing needs an explicit flag.
    dry = '--dry-run' in sys.argv or '--force-overwrite-deck' not in sys.argv
    if dry and '--dry-run' not in sys.argv:
        print('REFUSING TO WRITE: the deck is the authority and this script '
              'pushes the draft into it.\nShowing a dry run instead. If you '
              'really mean to overwrite the live deck with draft text, '
              're-run with --force-overwrite-deck.\n')
    reqs = dict(draft_requirements())
    L = []
    for prefix, action in MAP.items():
        head = next((h for h in reqs if h.startswith(prefix)), None)
        if head is None:
            continue
        lines = [l for l in reqs[head] if strip_md(l) not in ALREADY_ELSEWHERE]
        body = ret_join(lines)
        if action[0] == 'body':
            t = esc(action[1])
            L.append(f'''
        repeat with sl in slides of doc
            try
                if (object text of default title item of sl as text) starts with "{t}" then
                    set object text of default body item of sl to {body}
                    set font of object text of default body item of sl to "SFProDisplay-Regular"
                    exit repeat
                end if
            end try
        end repeat''')
        elif action[0] == 'card':
            marker = esc(action[1])
            card = ret_join([action[1]] + lines)
            L.append(f'''
        repeat with sl in slides of doc
            repeat with ti in text items of sl
                if (object text of ti as text) starts with "{marker}" then
                    set object text of ti to {card}
                    set font of object text of ti to "SFProDisplay-Regular"
                    set size of object text of ti to 15
                end if
            end repeat
        end repeat''')
        elif action[0] == 'new-after':
            anchor, own_title = esc(action[1]), esc(action[2])
            L.append(f'''
        set anchorIdx to 0
        set i to 0
        repeat with sl in slides of doc
            set i to i + 1
            try
                if (object text of default title item of sl as text) starts with "{anchor}" then set anchorIdx to i
            end try
        end repeat
        set already to false
        repeat with sl in slides of doc
            try
                if (object text of default title item of sl as text) starts with "{own_title}" then set already to true
            end try
        end repeat
        if anchorIdx > 0 and not already then
            set newSl to make new slide at after slide anchorIdx of doc with properties {{base layout:slide layout "Title & Bullets" of doc}}
            tell newSl
                set object text of default title item to "{own_title}"
                set font of object text of default title item to "SFProDisplay-Bold"
                set object text of default body item to {body}
                set font of object text of default body item to "SFProDisplay-Regular"
            end tell
        end if''')
        elif action[0] == 'panel-by-note':
            frag = esc(action[1])
            first = esc(strip_md(lines[0]))
            L.append(f'''
        repeat with sl in slides of doc
            if (presenter notes of sl as text) contains "{frag}" then
                set already to false
                repeat with ti in text items of sl
                    if (object text of ti as text) starts with "{first}" then set already to true
                end repeat
                if not already then
                    tell sl to set np to make new text item with properties {{object text:{body}, position:{{1120, 150}}, width:760}}
                    set font of object text of np to "SFProDisplay-Regular"
                    set size of object text of np to 15
                end if
                exit repeat
            end if
        end repeat''')
    script = ('tell application id "com.apple.Keynote"\n'
              '    set doc to front document\n'
              + '\n'.join(L) +
              '\n    save doc\nend tell\nreturn "synced"')
    if dry:
        print(script)
        return
    r = subprocess.run(['osascript', '-e', script],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())


if __name__ == '__main__':
    main()
