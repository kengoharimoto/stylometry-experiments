#!/usr/bin/env python3
"""Do the two Revākhaṇḍas share text, or just register?

The Revākhaṇḍa of the Skāndamahāpurāṇa and the distinct Revākhaṇḍa transmitted
in the Vāyupurāṇa sit at Delta 0.445 — far tighter than the corpus median of
1.044, and the tightest cross-stratum pair on the map. Delta cannot tell "two
Narmadā-māhātmyas in the same register" from "one copied the other's verses",
so this measures the second possibility directly: word 3-gram overlap on the
unsandhied text (so sandhi variation is normalised away), plus the longest
verbatim shared run, against controls at both ends.

The key calibration is Vāyu ↔ Brahmāṇḍa: Kirfel's single *Vāyuproktaṃ Purāṇam*,
the corpus's tightest pair at Delta 0.289, and a known case of massive shared
text. It fixes what "these two share verses" actually looks like on this scale.
"""
import re
from pathlib import Path

C = Path(__file__).resolve().parents[2] / 'corpus/epic_puranas_unsandhied'
RS = 'skandamahapurana_revakhanda'
RV = 'vayupurana_revakhanda'

_cache = {}


def toks(stem):
    if stem not in _cache:
        t = (C / f'{stem}.txt').read_text(encoding='utf-8').lower()
        _cache[stem] = re.findall(r'[a-zāīūṛṝḷṅñṭḍṇśṣ]+', t)
    return _cache[stem]


def grams(ws, n):
    return set(tuple(ws[i:i + n]) for i in range(len(ws) - n + 1))


def overlap(a, b, n=3):
    A, B = grams(toks(a), n), grams(toks(b), n)
    inter = len(A & B)
    if not inter:
        return 0.0, 0.0
    return inter / len(A | B), inter / min(len(A), len(B))


def longest_shared_run(a, b, cap=200):
    """Largest n for which the two texts share an n-gram (binary search)."""
    wa, wb = toks(a), toks(b)
    lo, hi, best = 1, min(cap, len(wa), len(wb)), 0
    sample = None
    while lo <= hi:
        mid = (lo + hi) // 2
        shared = grams(wa, mid) & grams(wb, mid)
        if shared:
            best, sample = mid, next(iter(shared))
            lo = mid + 1
        else:
            hi = mid - 1
    return best, sample


PAIRS = [
    ('Revā (SkMP) ↔ Revā (Vāyu)          THE QUESTION', RS, RV),
    ('Vāyu ↔ Brahmāṇḍa      known shared-verse pair', 'vayupurana', 'brahmandapurana'),
    ('Revā (SkMP) ↔ Kāśīkhaṇḍa   same work, check', RS, 'skandamahapurana_kasikhanda'),
    ('Revā (Vāyu) ↔ Vāyupurāṇa      its host, check', RV, 'vayupurana'),
    ('Revā (SkMP) ↔ Brahmāṇḍa           control', RS, 'brahmandapurana'),
    ('Revā (SkMP) ↔ MBh 6               control', RS, 'mahabharata_06-bhismaparvan'),
]

print(f"{'pair':50} 3-gram Jaccard  containment")
for lab, a, b in PAIRS:
    j, c = overlap(a, b)
    print(f'{lab:50}  {j:8.4f}       {c:6.3f}')

print('\nlongest verbatim shared run (words):')
for lab, a, b in PAIRS[:4]:
    n, sample = longest_shared_run(a, b)
    txt = ' '.join(sample[:14]) + ('…' if sample and len(sample) > 14 else '')
    print(f'  {lab.split("  ")[0]:44} {n:3d}   {txt}')

print(f'\nsizes: Revā(SkMP) {len(toks(RS)):,} words · '
      f'Revā(Vāyu) {len(toks(RV)):,} words')


def coverage(a, b, n=8):
    """Fraction of a's running words inside an n-gram that also occurs in b."""
    wa, wb = toks(a), toks(b)
    B = set(tuple(wb[i:i + n]) for i in range(len(wb) - n + 1))
    cov = bytearray(len(wa))
    for i in range(len(wa) - n + 1):
        if tuple(wa[i:i + n]) in B:
            cov[i:i + n] = b'\x01' * n
    return sum(cov) / len(wa)


print('\nverbatim coverage (share of running words inside an 8-word window'
      ' that also occurs in the other text):')
for a, b, lab in [
        (RS, RV, 'Revā (SkMP) covered by Revā (Vāyu)'),
        (RV, RS, 'Revā (Vāyu) covered by Revā (SkMP)'),
        ('vayupurana', 'brahmandapurana', 'Vāyu covered by Brahmāṇḍa'),
        ('brahmandapurana', 'vayupurana', 'Brahmāṇḍa covered by Vāyu'),
        (RS, 'brahmandapurana', 'Revā (SkMP) covered by Brahmāṇḍa  (control)')]:
    print(f'  {lab:46} {100 * coverage(a, b):5.1f}%')
