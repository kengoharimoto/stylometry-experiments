#!/usr/bin/env python3
"""Clean the 'minor tier' epic_puranas files, each with its own small artifact set.

Per file (base IAST text sound in all):
  kasikhanda     : drop [Pt N Page N] page markers + [ ...bhāgaḥ ] headers;
                   strip leading footnote/verse numbers and stray ':'.
  rudrasamhita   : drop apparatus lines (śi0pu0 / saṃ0 / khaṃ0 citations, '•'/':'
                   -initial); drop pure-numeric verse-number lines (incl. '11 N 11'
                   pipe-as-1 encoding); strip leading footnote numbers.
  sutasamhita4   : drop apparatus footnote lines (ms sigla / prakāśita / '] '),
                   drop pure-numeric verse-number lines; strip leading ':'/'*'.
  pranavakalpa   : strip '*' pratīka (lemma) delimiters.
  devibhagavata  : strip leading '*' marker.
  umasamhita     : strip leading '*' marker.
  pasupata       : drop '%' editorial comment lines.
  skandapurana   : drop stray pure-numeric verse-number line.

Usage: python3 clean_minor_tier.py <key> <infile> <outfile>   (key = one of the above)
"""
import re
import sys

NUM_ONLY = re.compile(r'^[\s0-9|]+$')            # only digits/pipes/space -> verse-number line
LEAD_NUM = re.compile(r'^\s*\d+\s+')
LEAD_SYM = re.compile(r'^\s*[:*]\s*')

# Shared OCR-pipeline noise (present across several files):
MARKERS  = re.compile(r'[•·*]')                  # bullet / middle-dot / stray star markers
TAG      = re.compile(r'\[[a-z]+\]')             # pipeline provenance tags: [gcv], [opus]
NUMBRACK = re.compile(r'\[\s*\d+\s*\]')          # [123] number/footnote brackets
SUPPLY   = re.compile(r'\[([^\[\]]*)\]')         # [ma] supplied-akṣara brackets -> keep content
PUNCT_ONLY = re.compile(r'^[.|\s]*$')            # nothing but dots/pipes/space after cleanup


def _strip_leading(line):
    """Repeatedly strip a leading ':'/'*' marker or number; stripping one can
    expose another (e.g. "9 4 mahātmanā" -> "mahātmanā", "*540 ..." -> "...")."""
    prev = None
    while prev != line:
        prev = line
        line = LEAD_SYM.sub('', line)
        line = LEAD_NUM.sub('', line)
    return line


def _tidy(line):
    line = MARKERS.sub('', line)
    line = TAG.sub('', line)
    line = NUMBRACK.sub('', line)
    line = SUPPLY.sub(r'\1', line)
    line = line.replace('[', '').replace(']', '')   # orphan brackets
    line = _strip_leading(line)                     # after denoise, so exposed nums are stripped
    line = re.sub(r'[ \t]{2,}', ' ', line).strip()
    # A digit that survives leading-strip means an unstrippable number fragment or
    # "N." apparatus gloss (genuine verse text never begins with a bare digit here).
    if PUNCT_ONLY.match(line) or (line[:1].isdigit()):
        return ''
    return line


def kasikhanda(line):
    return _tidy(line)


def rudrasamhita(line):
    s = line.strip()
    if not s:
        return ''
    if s[0] in '•:' or re.search(r'śi0\s*pu0|saṃ0|khaṃ0', line):
        return None                              # apparatus / variant citation
    return _tidy(line)


def sutasamhita4(line):
    s = line.strip()
    if not s:
        return ''
    if re.match(r'^\s*\d', s):                    # leading digit -> apparatus footnote (drop)
        return None
    return _tidy(line)


def pranavakalpa(line):
    return _tidy(line)


def devibhagavata(line):
    return _tidy(line)


umasamhita = devibhagavata


def pasupata(line):
    if line.lstrip().startswith('%'):
        return None
    return _tidy(line)


def skandapurana(line):
    if NUM_ONLY.match(line.strip()) and line.strip():
        return None
    return _tidy(line)


HANDLERS = {
    'kasikhanda': kasikhanda, 'rudrasamhita': rudrasamhita, 'sutasamhita4': sutasamhita4,
    'pranavakalpa': pranavakalpa, 'devibhagavata': devibhagavata, 'umasamhita': umasamhita,
    'pasupata': pasupata, 'skandapurana': skandapurana,
}


def clean(key, lines):
    h = HANDLERS[key]
    out = []
    for raw in lines:
        line = raw.rstrip('\n')
        s = line.strip()
        if s.startswith('['):                    # whole-line bracket apparatus/header
            continue
        if s and NUM_ONLY.match(s):              # standalone verse-number line ("61", "93 ||")
            continue
        r = h(line)
        if r is None:
            continue
        out.append(r)
    res = []
    for ln in out:
        if ln == '' and (not res or res[-1] == ''):
            continue
        res.append(ln)
    while res and res[0] == '':
        res.pop(0)
    while res and res[-1] == '':
        res.pop()
    return res


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in HANDLERS:
        sys.exit(f'Usage: clean_minor_tier.py <{"|".join(HANDLERS)}> <infile> <outfile>')
    key = sys.argv[1]
    lines = open(sys.argv[2], encoding='utf-8').readlines()
    cleaned = clean(key, lines)
    open(sys.argv[3], 'w', encoding='utf-8').write('\n'.join(cleaned) + '\n')
    print(f'{key}: {len(lines)} -> {len(cleaned)} lines')


if __name__ == '__main__':
    main()
