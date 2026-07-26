#!/usr/bin/env python3
"""Dump all text content of the Keynote deck to a diffable file.

Reads the FRONT document in Keynote (open the deck first, or pass --open to
open materials/presentation_2026/chronology_stratification.key) and writes
every slide's layout name, title, body, free text items, and presenter notes
to materials/presentation_2026/keynote_text_dump.txt.

Purpose: the .key is hand-edited from now on (build_deck_keynote.py is the
frozen scaffold). Re-run this after editing sessions and diff the dump (it is
committed to git) to see what changed textually; for layout-only changes,
export slide images and compare visually.

Usage: python3 scripts/presentation/dump_keynote_text.py [--open]
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
KEY = ROOT / 'materials/presentation_2026/chronology_stratification.key'
OUT = ROOT / 'materials/presentation_2026/keynote_text_dump.txt'

SEP_S, SEP_F = '␞', '␟'   # record separators unlikely in slide text

script = f'''
tell application id "com.apple.Keynote"
    {f'open POSIX file "{KEY}"' if '--open' in sys.argv else ''}
    set doc to front document
    set acc to ""
    set i to 0
    repeat with sl in slides of doc
        set i to i + 1
        set acc to acc & "{SEP_S}SLIDE " & i & "{SEP_F}" & (name of base layout of sl) & linefeed
        try
            set acc to acc & "{SEP_F}TITLE: " & (object text of default title item of sl as text) & linefeed
        end try
        try
            set acc to acc & "{SEP_F}BODY: " & (object text of default body item of sl as text) & linefeed
        end try
        repeat with ti in text items of sl
            set acc to acc & "{SEP_F}TEXTITEM: " & (object text of ti as text) & linefeed
        end repeat
        repeat with tb in tables of sl
            repeat with r in rows of tb
                set rowvals to ""
                repeat with c in cells of r
                    try
                        set rowvals to rowvals & (value of c as text) & " | "
                    end try
                end repeat
                set acc to acc & "{SEP_F}TABLEROW: " & rowvals & linefeed
            end repeat
        end repeat
        set acc to acc & "{SEP_F}NOTES: " & (presenter notes of sl as text) & linefeed
    end repeat
    return acc
end tell
'''

r = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stderr.strip())
txt = (r.stdout.replace(SEP_S, '\n' + '=' * 70 + '\n')
       .replace(SEP_F, '\n'))
OUT.write_text(txt, encoding='utf-8')
n = txt.count('=' * 70)
print(f'wrote {OUT.relative_to(ROOT)} ({n} slides)')
