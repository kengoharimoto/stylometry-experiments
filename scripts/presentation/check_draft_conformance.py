#!/usr/bin/env python3
"""Draft-drift report: which on-slide lines of slides_draft.md are no longer
in the deck.

THE DECK IS THE AUTHORITY (Kengo, 2026-07-28). The .key is hand-edited and
governs; slides_draft.md is a RECORD of it, not its source. So a line that
is in the draft but not in the deck means THE DRAFT IS STALE — it is not a
build error, and it must not abort a build. This reverses the 2026-07-26
rule, when the draft was the source and any miss failed the build.

Reconciling drift is an editorial call, not a find-and-replace: Kengo
retitles and rewrites in Keynote, and figure-only backup slides carry no
readable text at all, so a "missing" line may simply live as an image plus
a spoken cue. Read the drift, then decide per line.

The draft's "**On slide:**" blockquote is treated as the literal slide text
(wrapped lines are joined; markdown emphasis, list markers, quote/dash
variants and whitespace are normalized away before matching). Markdown table
rows and cue/backup prose are not checked.

Usage:
  python3 check_draft_conformance.py pptx            # against the built .pptx
  python3 check_draft_conformance.py key             # against keynote_text_dump.txt
  python3 check_draft_conformance.py key --strict    # exit 1 on drift
Exit 0 unless --strict is passed (drift is reported either way).
"""
import html
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MAT = ROOT / 'materials/presentation_2026'
DRAFT = MAT / 'slides_draft.md'


def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('**', '').replace('*', '').replace('`', '')
    s = (s.replace('’', "'").replace('‘', "'")
          .replace('“', '"').replace('”', '"')
          .replace('–', '—').replace('->', '→'))
    s = s.lower()
    s = re.sub(r'[^\w\s→]', ' ', s)      # punctuation-insensitive
    return re.sub(r'\s+', ' ', s).strip()


def draft_requirements():
    """[(section, [line, ...]), ...] — joined, literal on-slide lines."""
    txt = DRAFT.read_text(encoding='utf-8')
    out = []
    for part in re.split(r'^### ', txt, flags=re.M)[1:]:
        head = part.splitlines()[0].strip()
        m = re.search(r'\*\*On slide:\*\*\s*\n((?:>.*\n?)+)', part)
        if not m:
            continue
        items, cur = [], ''
        for raw in m.group(1).splitlines():
            t = raw.lstrip('>').rstrip()
            t = t.strip()
            if not t:
                if cur:
                    items.append(cur)
                cur = ''
                continue
            if t.startswith('|'):
                continue
            new_item = bool(re.match(r'^(-|\d+\.)\s', t))
            t = re.sub(r'^(-|\d+\.)\s+', '', t)
            if new_item or not cur:
                if cur:
                    items.append(cur)
                cur = t
            else:
                cur += ' ' + t
        if cur:
            items.append(cur)
        items = [i for i in items if norm(i)]
        if items:
            out.append((head, items))
    return out


def pptx_text():
    deck = MAT / 'chronology_stratification.pptx'
    buf = []
    with zipfile.ZipFile(deck) as z:
        for n in z.namelist():
            if re.match(r'ppt/slides/slide\d+\.xml$', n):
                xml = z.read(n).decode('utf-8')
                buf += [html.unescape(t) for t in
                        re.findall(r'<a:t>([^<]*)</a:t>', xml)]
    return norm(' '.join(buf))


def key_text():
    dump = MAT / 'keynote_text_dump.txt'
    keep, in_field = [], False
    for l in dump.read_text(encoding='utf-8').splitlines():
        if l.startswith(('TITLE: ', 'BODY: ', 'TEXTITEM: ', 'TABLEROW: ')):
            keep.append(l.split(': ', 1)[1])
            in_field = True
        elif l.startswith(('NOTES: ', 'SLIDE ', '=' * 10)) or not l.strip():
            in_field = False
        elif in_field:
            keep.append(l)          # continuation line of a multi-par field
    return norm(' '.join(keep))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    strict = '--strict' in sys.argv
    target = args[0] if args else 'pptx'
    hay = pptx_text() if target == 'pptx' else key_text()
    misses = []
    for head, items in draft_requirements():
        for it in items:
            if norm(it) not in hay:
                misses.append((head, it))
    if misses:
        print(f'DRAFT DRIFT ({target}): {len(misses)} on-slide line(s) in '
              f'slides_draft.md are not in the deck. The deck is the '
              f'authority — these are stale draft lines to reconcile, not '
              f'build errors:')
        for head, it in misses:
            print(f'  [{head}]')
            print(f'      {it}')
        if strict:
            sys.exit(1)
        return
    print(f'no draft drift ({target}): every on-slide line is in the deck')


if __name__ == '__main__':
    main()
