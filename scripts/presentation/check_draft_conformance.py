#!/usr/bin/env python3
"""Draft-conformance gate: every on-slide line of slides_draft.md must appear
in the built deck, or the build FAILS.

This is the guarantee that the generators look at the draft on every run:
build_deck.js and build_deck_keynote.py invoke this checker after writing
their output and abort loudly on any miss, so a draft edit can never again
be silently ignored — the build breaks until the generator is synced.

The draft's "**On slide:**" blockquote is treated as the literal slide text
(wrapped lines are joined; markdown emphasis, list markers, quote/dash
variants and whitespace are normalized away before matching). Markdown table
rows and cue/backup prose are not checked.

Usage:
  python3 check_draft_conformance.py pptx   # check the built .pptx
  python3 check_draft_conformance.py key    # check keynote_text_dump.txt
Exit 0 = conformant; exit 1 = misses (listed per draft section).
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
    target = sys.argv[1] if len(sys.argv) > 1 else 'pptx'
    hay = pptx_text() if target == 'pptx' else key_text()
    misses = []
    for head, items in draft_requirements():
        for it in items:
            if norm(it) not in hay:
                misses.append((head, it))
    if misses:
        print(f'DRAFT CONFORMANCE FAILED ({target}): {len(misses)} on-slide '
              f'line(s) from slides_draft.md are missing from the deck:')
        for head, it in misses:
            print(f'  [{head}]')
            print(f'      {it}')
        sys.exit(1)
    print(f'draft conformance OK ({target}): every on-slide line is in the deck')


if __name__ == '__main__':
    main()
