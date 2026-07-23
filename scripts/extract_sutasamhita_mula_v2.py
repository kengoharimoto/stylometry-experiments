#!/usr/bin/env python3
"""Re-extract the Sūtasaṃhitā khaṇḍa-4 mūla from the OCR text, v2.

The v1 heuristic (extract_sutasamhita_verses.py) required a verse-closer line
AND its predecessor to look verse-like; OCR footnote junk and page furniture
between pādas failed that test and silently dropped ~1,650 of ~3,500 verses
(337 gaps in the verse numbering).

v2 classifies each line independently, then anchors on the verse numbering:

  junk       [page N] markers, running headers, footnote lines, page numbers
  verse      mostly-IAST line of half-śloka shape: 13-26 syllables (anuṣṭubh
             half = 16, triṣṭubh half = 22, with OCR tolerance), no prose
             markers, usually ending || or || N ||
  colophon   iti śrī... adhyāyaḥ lines (kept — the corpus units keep them)
  prose      everything else (the Tātparyadīpikā)

A `|| N ||` closer on a verse-shaped line ends a verse; the same number on a
prose-shaped line ends a commentary block (the edition numbers both). Junk
lines are transparent. Validation prints per-adhyāya verse-number coverage.

Usage:
  python3 scripts/extract_sutasamhita_mula_v2.py \
      [--src ~/Documents/E-texts/00_inbox/New/sutasamhita_khanda4_roman.txt] \
      [--out corpus/epic_puranas/skandamahapurana_sutasamhita_khanda-4_v2.txt]
"""
import argparse
import re
from pathlib import Path

VOWEL = re.compile(r'(ai|au|[aāiīuūṛṝḷeo])')
CLOSER = re.compile(r'\|\|\s*(\d+)\s*\|\|\s*$')
IAST_OK = set("abcdefghijklmnopqrstuvwxyzāīūṛṝḷḹṃḥśṣṇṭḍṅñ'|.– —-")

PROSE = re.compile(
    r"(ityarthaḥ|tyarthaḥ|ityāha|ityādi|iti\s*\||vyākhyā|nigadavyā|nigadvyā|"
    r"tatrā''?ha|āśaṅkya|śaṅkate|\bnanu\b|\bcet\b|\bucyate\b|\bkathyate\b|tātparya|"
    r"saṃbandhaḥ|abhipret|prayojanam|adhyāyaśeṣaḥ|iti\s+bhāvaḥ|"
    r"uktakrameṇa|śrutericyate|—)"
)
HEADER = re.compile(r'(tātparyadīpikāsametā|yajñavaibhavakhaṇḍe|sūtasaṃhitā\s*\|?\s*$|'
                    r'^\[\s*page\s+\d+\s*\]|^\[\s*\d)', re.IGNORECASE)
COLOPHON = re.compile(r"[a']dhyāyaḥ\s*(\|\|\s*\d+\s*\|\|)?\s*$|^\s*iti\s+śrī")
MULTINUM = re.compile(r'\|\|\s*\d+\s*\|\|\s*\d+')
COMM_TAIL = re.compile(r"(^|\s)iti\s*$")


def syllables(s):
    return len(VOWEL.findall(s))


def iast_ratio(s):
    body = [c for c in s.lower() if not c.isspace()]
    if not body:
        return 0.0
    return sum(c in IAST_OK for c in body) / len(body)


def classify(raw):
    s = raw.strip()
    if not s:
        return 'junk'
    if HEADER.search(s):
        return 'junk'
    if s.isdigit() or len(s.replace(' ', '')) <= 2:
        return 'junk'
    core = CLOSER.sub('', s).strip()
    if iast_ratio(core) < 0.85 or re.match(r'^\d', s):
        return 'junk'                      # footnote apparatus / OCR garbage
    if COLOPHON.search(s):
        return 'prose' if re.search(r'ṭīkā|dīpikā', s) else 'colophon'
    if MULTINUM.search(s):
        return 'prose'                     # || 18 || 19 || 20 || = commentary span
    if PROSE.search(core) or COMM_TAIL.search(core):
        return 'prose'
    n = syllables(core)
    # anuṣṭubh half-śloka ~16 syl; triṣṭubh/jagatī pāda-per-line 11-12 syl
    if 10 <= n <= 26 and (s.endswith('||') or CLOSER.search(s)):
        return 'verse'
    if 14 <= n <= 18:                      # half-śloka whose closer got OCR-mangled
        return 'verse'
    return 'prose'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=str(Path.home() /
                    'Documents/E-texts/00_inbox/New/sutasamhita_khanda4_roman.txt'))
    ap.add_argument('--out', default='corpus/epic_puranas/'
                    'skandamahapurana_sutasamhita_khanda-4_v2.txt')
    args = ap.parse_args()

    lines = Path(args.src).read_text(encoding='utf-8').splitlines()
    kept, adhyayas, cur_nums = [], [], []
    pending = []       # verse-shaped lines awaiting a closer
    lead = []          # verse-ish lines seen since the last closer event: the
    in_lead = True     # mūla block, recoverable via the commentary's closer
    ALLNUM = re.compile(r'\|\|\s*(\d+)\s*(?=\|\|)')

    def looks_versish(s):
        core = CLOSER.sub('', s).strip()
        return 8 <= syllables(core) <= 30 and not PROSE.search(core) \
            and not COMM_TAIL.search(core)

    def advance(n):
        cur = cur_nums[-1] if cur_nums else 0
        if n == cur:
            return None
        if n > cur + 5 and int(str(n)[-2:] or 0) in range(cur + 1, cur + 6):
            n = int(str(n)[-2:])           # OCR stray digit: || 954 || = || 54 ||
        if n < cur - 1 and n <= 2:
            adhyayas.append(list(cur_nums))     # numbering reset w/o colophon
            cur_nums.clear()
        return n

    for raw in lines:
        kind = classify(raw)
        if kind == 'junk':
            continue                        # transparent: does not break verses
        s = ' '.join(raw.split())
        if kind == 'colophon':
            kept.append(s)
            if cur_nums:
                adhyayas.append(list(cur_nums))
            cur_nums.clear()
            pending, lead, in_lead = [], [], True
            continue
        m = CLOSER.search(s)
        if kind == 'verse':
            pending.append(s)
            if in_lead:
                lead.append(s)
            if m:
                n = advance(int(m.group(1)))
                if n is not None:
                    kept.extend(pending[-3:])   # a verse is <= 3 lines
                    cur_nums.append(n)
                pending, lead, in_lead = [], [], True
        else:                               # prose
            if in_lead and looks_versish(s):
                lead.append(s)              # possible mūla with mangled closer
            else:
                in_lead = False
            pending = []                    # strict capture needs contiguity
            nums = [int(x) for x in ALLNUM.findall(s + '||')] if '||' in s else []
            if nums and CLOSER.search(s) or (nums and MULTINUM.search(s)):
                # commentary closer: recover any covered verses never captured
                cur = cur_nums[-1] if cur_nums else 0
                want = [x for x in nums if cur < x <= cur + 6]
                if want and lead:
                    kept.extend(lead[:3 * len(want)])
                    for x in want:
                        cur_nums.append(x)
                lead, in_lead = [], True

    if cur_nums:
        adhyayas.append(cur_nums)

    Path(args.out).write_text('\n'.join(kept) + '\n', encoding='utf-8')

    total = missing = 0
    for i, nums in enumerate(adhyayas, 1):
        # windowed monotone filter: numbers must advance by 1-5; others = OCR noise
        acc, cur = [], 0
        for n in nums:
            if cur < n <= cur + 5:
                acc.append(n); cur = n
        top = acc[-1] if acc else max(nums)
        have = set(acc)
        miss = [n for n in range(1, top + 1) if n not in have]
        total += top
        missing += len(miss)
        flag = f'  missing {miss[:8]}{"…" if len(miss) > 8 else ""}' if miss else ''
        print(f'adhyāya-run {i:3}: 1–{top}  ({len(miss)} missing){flag}')
    print(f'\n{len(kept)} lines kept; ~{total} verses expected, '
          f'{missing} missing ({missing / max(total, 1):.1%})')
    print('wrote', args.out)


if __name__ == '__main__':
    main()
