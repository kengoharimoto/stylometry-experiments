#!/usr/bin/env python3
"""
apply_sandhi.py — Apply Sanskrit external sandhi to GRETIL padapāṭha texts.

Implements rules from sandhix.pl (Gonda), adapted for IAST encoding.
Convention in input files:
  - '+' marks sandhi dissolution (word boundary where sandhi would apply)
  - 's' at word-end before '+' = visarga ḥ
  - 'm' at word-end before '+' = anusvāra ṃ / final m
  - '&' = hemistich separator (removed)
"""

import os
import re
import sys


def apply_sandhi(text):
    # ------------------------------------------------------------------
    # Pre-processing
    # ------------------------------------------------------------------
    text = re.sub(r'&', '', text)       # remove hemistich markers
    text = re.sub(r'\+ ', '+', text)    # normalise: remove space after +

    # ------------------------------------------------------------------
    # VOWEL + VOWEL
    # ------------------------------------------------------------------

    # ai + a/i/u/ṛ/ṝ/e/o → ā (vowel)   [#8/1 — ayādi]
    text = re.sub(r'ai\+(a|i|u|[ṛṝ]|e|o)', r'ā \1', text)

    # au + a/i/u/ṛ/ṝ/e/o → āv(vowel)   [#8/2 — ayādi]
    text = re.sub(r'au\+(a|i|u|[ṛṝ]|e|o)', r'āv\1', text)

    # a/ā + e/ai → ai                   [#5 III/1 — vṛddhi]
    text = re.sub(r'[aā]\+(e|ai)', r'ai', text)

    # a/ā + o/au → au                   [#5 III/2 — vṛddhi]
    text = re.sub(r'[aā]\+(o|au)', r'au', text)

    # a/ā + a/ā → ā                     [#5 I/1 — savarna-dīrgha]
    text = re.sub(r'[aā]\+[aā]', r'ā', text)

    # a/ā + i/ī → e                     [#5 II/1 — guṇa]
    text = re.sub(r'[aā]\+[iī]', r'e', text)

    # a/ā + u/ū → o                     [#5 II/2 — guṇa]
    text = re.sub(r'[aā]\+[uū]', r'o', text)

    # a/ā + ṛ/ṝ → ar                    [#5 II/3 — guṇa]
    text = re.sub(r'[aā]\+[ṛṝ]', r'ar', text)

    # i/ī + i/ī → ī                     [#5 I/2 — savarna-dīrgha]
    text = re.sub(r'[iī]\+[iī]', r'ī', text)

    # i/ī + a/u/ṛ/ḷ/e/o → y(vowel)     [#6/1&4 — yaṇ]
    text = re.sub(r'[iī]\+(a|u|[ṛṝḷ]|e|o)', r'y\1', text)

    # u/ū + u/ū → ū                     [#5 I/3 — savarna-dīrgha]
    text = re.sub(r'[uū]\+[uū]', r'ū', text)

    # u/ū + a/i/ṛ/ḷ/e/o → v(vowel)     [#6/2&5 — yaṇ]
    text = re.sub(r'[uū]\+(a|i|[ṛṝḷ]|e|o)', r'v\1', text)

    # ṛ/ṝ + a/i/ḷ/e/o → r(vowel)       [#6/3&6 — yaṇ]
    text = re.sub(r'[ṛṝ]\+(a|i|[ḷ]|e|o)', r'r\1', text)

    # e/o + ā → a ā                     [#7/1 exception]
    text = re.sub(r'([eo])\+ā', r'a ā', text)

    # e/o + a → (e/o) 'a                [#7/2 — avagraha]
    text = re.sub(r'([eo])\+a', r"\1 'a", text)

    # e/o + (anything remaining) → a    [#7/1 — ayādi catch-all]
    text = re.sub(r'[eo]\+', r'a ', text)

    # ------------------------------------------------------------------
    # CONSONANT + CONSONANT  (r/s-visarga before t and c)
    # ------------------------------------------------------------------

    # r/s + t → st
    text = re.sub(r'[rs]\+t', r'st', text)

    # r/s + c → śc
    text = re.sub(r'[rs]\+c', r'śc', text)

    # ------------------------------------------------------------------
    # FINAL VOICELESS STOP → VOICED  (before vowel or voiced consonant)
    # ------------------------------------------------------------------
    _vc = r'(a|ā|i|ī|u|ū|[ṛṝ]|ḷ|e|o|g|j|ḍ|d|b|y|r|v)'

    text = re.sub(r'k\+' + _vc, r'g\1', text)
    text = re.sub(r'c\+' + _vc, r'j\1', text)
    text = re.sub(r'ṭ\+' + _vc, r'ḍ\1', text)
    text = re.sub(r'p\+' + _vc, r'b\1', text)
    # t before c handled below; exclude c here
    text = re.sub(r't\+(a|ā|i|ī|u|ū|[ṛṝ]|ḷ|e|o|g|d|b|y|r|v)', r'd\1', text)

    # ------------------------------------------------------------------
    # FINAL STOP → NASAL  (before nasal)
    # ------------------------------------------------------------------
    _nas = r'([ṅñṇnm])'

    text = re.sub(r'[kg]\+' + _nas, r'ṅ\1', text)
    text = re.sub(r'[cj]\+' + _nas, r'ñ\1', text)
    text = re.sub(r'[ṭḍ]\+' + _nas, r'ṇ\1', text)
    text = re.sub(r'd\+'   + _nas, r'n\1', text)
    text = re.sub(r'[pb]\+' + _nas, r'm\1', text)

    # ------------------------------------------------------------------
    # ASPIRATION SANDHI
    # ------------------------------------------------------------------
    text = re.sub(r'k\+h', r'ggh', text)
    text = re.sub(r'c\+h', r'jjh', text)
    text = re.sub(r'ṭ\+h', r'ḍḍh', text)
    text = re.sub(r't\+h', r'ddh', text)
    text = re.sub(r'p\+h', r'bbh', text)

    # vowel + ch → vowel cch  (doubling of initial ch)
    text = re.sub(r'ā\+ch',    r'ā cch', text)
    text = re.sub(r'([aiu])\+ch', r'\1 cch', text)
    text = re.sub(r'ṛ\+ch',   r'ṛ cch', text)

    # ------------------------------------------------------------------
    # t-ASSIMILATION
    # ------------------------------------------------------------------
    text = re.sub(r't\+([cj])', r'\1\1', text)   # t+c→cc, t+j→jj
    text = re.sub(r't\+ñ',      r'ññ',   text)
    text = re.sub(r't\+([ṭḍ])', r'\1\1', text)   # t+ṭ→ṭṭ, t+ḍ→ḍḍ
    text = re.sub(r't\+ṇ',      r'ṇṇ',   text)
    text = re.sub(r't\+l',      r'll',   text)
    text = re.sub(r't\+(n|m)',  r'n\1',  text)
    text = re.sub(r'[td]\+ś',   r'cch',  text)

    # ------------------------------------------------------------------
    # VISARGA SANDHI  (s at word-end = ḥ)
    # ------------------------------------------------------------------
    _voi = r'(a|ā|i|ī|u|ū|[ṛṝ]|e|o|g|j|ḍ|d|n|b|m|y|r|l|v|h)'

    # āḥ (ās) + vowel/voiced → ā ...
    text = re.sub(r'ās\+' + _voi, r'ā \1', text)

    # aḥ (as) + voiced C → o ...
    text = re.sub(r'as\+(g|j|ḍ|d|n|b|m|y|r|l|v|h)', r'o \1', text)

    # aḥ (as) + vowel ≠ a → a ...
    text = re.sub(r'as\+(ā|i|ī|u|ū|[ṛṝ]|e|o)', r'a \1', text)

    # aḥ (as) + a → o 'a  (avagraha)
    text = re.sub(r'as\+a', r"o 'a", text)

    # iḥ/uḥ (is/us) + vowel/voiced → ir/ur ...
    text = re.sub(r'([iu])s\+(i|ī|u|ū|[ṛṝ]|e|o|g|j|ḍ|d|n|b|m|y|l|v|h)',
                  r'\1r\2', text)

    # normalise r-visarga → s, then process as above
    text = re.sub(r'r\+', r's+', text)

    # s-visarga + vowel/voiced → r ...
    text = re.sub(r's\+(a|ā|i|ī|u|ū|[ṛṝ]|e|o|g|j|ḍ|d|n|b|m|y|l|v|h)',
                  r'r\1', text)

    # diphthong/short-vowel + r/s-visarga before r → special  [#16]
    text = re.sub(r'(ai|au)[rs]\+r', r'\1 r', text)
    text = re.sub(r'([aiu])[rs]\+r',  r'\1\1 r', text)

    # ------------------------------------------------------------------
    # n-SANDHI
    # ------------------------------------------------------------------
    # exception: n after ā/ī/ū/ṝ/e/o + vowel → no doubling
    text = re.sub(r'([āīūṝeo])n\+(a|i|u|e|o|[ṛṝ])', r'\1n\2', text)

    # general: n + vowel → nn + vowel  (doubling)
    text = re.sub(r'n\+(a|i|u|[ṛṝ]|o|e)', r'nn\1', text)

    text = re.sub(r'n\+j',  r'ñj',   text)
    text = re.sub(r'n\+ḍ',  r'ṇḍ',   text)
    text = re.sub(r'n\+ś',  r'ñch',  text)
    text = re.sub(r'n\+l',  r'/ll',  text)   # chandrabindu-l notation
    text = re.sub(r'n\+c',  r'ṃśc',  text)
    text = re.sub(r'n\+ṭ',  r'ṃṣṭ',  text)
    text = re.sub(r'n\+t',  r'ṃst',  text)

    # ------------------------------------------------------------------
    # m-SANDHI
    # ------------------------------------------------------------------
    # m + vowel (incl. long vowels — fix vs. Perl original) → m + space + vowel
    text = re.sub(r'm\+(a|ā|i|ī|u|ū|[ṛṝḷ]|e|o)', r'm \1', text)

    # m + consonant → ṃ (anusvāra)  [space kept between words]
    text = re.sub(r'm\+', r'ṃ ', text)

    # ------------------------------------------------------------------
    # Remaining s-visarga cleanup
    # ------------------------------------------------------------------
    # s + verse-end markers (|, ||, /, //) → ḥ + marker
    text = re.sub(r's\+(\|\|?|//?)', r'ḥ\1', text)

    # s + anything else → ḥ  [space kept between words]
    text = re.sub(r's\+', r'ḥ ', text)

    # ------------------------------------------------------------------
    # Remove any remaining + signs, keeping words separated
    # ------------------------------------------------------------------
    text = re.sub(r'\+', ' ', text)
    text = re.sub(r'  +', ' ', text)  # collapse double spaces

    return text


def process_file(path):
    with open(path, encoding='utf-8') as f:
        original = f.read()
    result = apply_sandhi(original)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(result)
    changed = sum(1 for a, b in zip(original.splitlines(), result.splitlines()) if a != b)
    print(f"{path}: {changed} lines changed")


FILES = [
    'unknown_vayupurana_hk.txt',
    'unknown_saurapurana.txt',
    'unknown_bhavisyapurana_parvan-1_adhyaya-183.txt',
    'unknown_skandapurana_pasupata_adhyaya174-183_u.txt',
    'unknown_brahmapurana.txt',
]

if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    paths = sys.argv[1:] or [os.path.join(base, fname) for fname in FILES]
    for path in paths:
        process_file(path)
