#!/usr/bin/env python3
"""Carry slide wording from slides_draft.md into the Keynote deck — surgically.

This restores the draft->deck pipeline under the hand-edited .key regime:
the draft is the WORDING source; the deck is the LAYOUT source. The tool
parses each mapped slide's "**On slide:**" block from the draft, compares it
with what the deck currently says, and (with --apply) sets only the changed
title/body placeholder text on that one slide in the front Keynote document.
It never rebuilds, never touches text boxes, images, tables, or layout.

Scope: the placeholder text slides. Tour cards, tables, and figure slides
are reported as OUT OF SCOPE when their draft blocks change — sync those by
hand (or ask for it).

Usage:
  python3 scripts/presentation/sync_draft_to_deck.py           # report diffs
  python3 scripts/presentation/sync_draft_to_deck.py --apply   # push to deck
(The deck must be open in Keynote; pass --open to open it first.)
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DRAFT = ROOT / 'materials/presentation_2026/slides_draft.md'
KEY = ROOT / 'materials/presentation_2026/chronology_stratification.key'

# draft heading fragment -> (keynote slide number, has_title_in_body_block)
# Only slides whose on-slide text lives in title/body placeholders.
MAPPED = {
    'Slide 4 · The question': 4,
    'Slide 5 · The corpus': 5,
    'Slide 3 · The claim': 3,
    'Slide 17 · The convergence argument': 17,
    'Slide 18 · What the second axis is *not*': 18,
    'Slide 19 · What the axis is made of': 19,
    'Slide 20 · What this is — and is not': 20,
}


def on_slide_block(section):
    m = re.search(r'\*\*On slide:\*\*\n\n((?:>.*\n?)+)', section)
    if not m:
        return []
    lines = []
    for raw in m.group(1).splitlines():
        t = raw.lstrip('>').strip()
        if not t:
            continue
        t = re.sub(r'^(\d+\.|-)\s*', '', t)      # list markers
        t = t.replace('**', '').replace('*', '')  # emphasis
        lines.append(t)
    return lines


def draft_sections():
    txt = DRAFT.read_text(encoding='utf-8')
    parts = re.split(r'^### ', txt, flags=re.M)
    out = {}
    for p in parts[1:]:
        head = p.splitlines()[0].strip()
        out[head] = p
    return out


def deck_text(slide_no):
    script = f'''
    tell application id "com.apple.Keynote"
        set sl to slide {slide_no} of front document
        set tt to ""
        set bb to ""
        try
            set tt to object text of default title item of sl as text
        end try
        try
            set bb to object text of default body item of sl as text
        end try
        return tt & "␟" & bb
    end tell'''
    r = subprocess.run(['osascript', '-e', script],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr.strip())
    t, _, b = r.stdout.rstrip('\n').partition('␟')
    return t, [l for l in b.split('\r') if l.strip()] or \
              [l for l in b.split('\n') if l.strip()]


def set_deck_body(slide_no, lines):
    esc = lambda s: s.replace('\\', '\\\\').replace('"', '\\"')
    body = ' & return & '.join(f'"{esc(l)}"' for l in lines)
    script = f'''
    tell application id "com.apple.Keynote"
        set sl to slide {slide_no} of front document
        set object text of default body item of sl to {body}
        set font of object text of default body item of sl to "SFProDisplay-Regular"
    end tell'''
    r = subprocess.run(['osascript', '-e', script],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr.strip())


def main():
    if '--open' in sys.argv:
        subprocess.run(['osascript', '-e',
                        f'tell application id "com.apple.Keynote" to open '
                        f'POSIX file "{KEY}"'])
    apply = '--apply' in sys.argv
    sections = draft_sections()
    changes = 0
    for head, slide_no in MAPPED.items():
        sec = next((s for h, s in sections.items() if h.startswith(head)), None)
        if sec is None:
            print(f'!! draft section not found: {head}')
            continue
        want = on_slide_block(sec)
        # drop lines that are the slide's own title or pure lead-in phrases
        _, have = deck_text(slide_no)
        want_cmp = [w for w in want if w.rstrip(':') not in
                    ('Two questions worth thirty minutes',)]
        if [w.lower() for w in want_cmp] == [h.lower() for h in have]:
            continue
        changes += 1
        print(f'— slide {slide_no} ({head}) differs:')
        for h in have:
            if h.lower() not in [w.lower() for w in want_cmp]:
                print(f'   deck : {h}')
        for w in want_cmp:
            if w.lower() not in [h.lower() for h in have]:
                print(f'   draft: {w}')
        if apply:
            set_deck_body(slide_no, want_cmp)
            print(f'   -> applied draft wording to slide {slide_no}')
    if not changes:
        print('deck and draft agree on all mapped slides')
    elif not apply:
        print('\nrun with --apply to push draft wording into the deck '
              '(remember to save in Keynote afterwards)')


if __name__ == '__main__':
    main()
