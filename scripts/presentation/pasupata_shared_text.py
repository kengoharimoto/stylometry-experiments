#!/usr/bin/env python3
"""Do the SP-Pāśupata and Vāyu-Pāśupata sections share text, or just register?

Both land at the far right of the map near the Śaiva material. Delta cannot
tell "same school" from "copied the same verses", so this checks the second
possibility directly with a fuzzy text-overlap measure (word 3-gram Jaccard /
containment on the unsandhied text, so sandhi variation is normalized away),
against calibrating controls, plus longest-verbatim-run detection.

Result: they share virtually no text (≈0.002, control-level; longest shared run
four words) — so their convergence is doctrinal register, not borrowing.
"""
import re
import difflib
from pathlib import Path

C = Path(__file__).resolve().parents[2] / 'corpus/epic_puranas_unsandhied'
SP = 'skandapurana_pasupata_adhyaya174-183_u'
V = 'vayupurana_02_pashupata-yoga_iast'


def toks(stem):
    t = (C / f'{stem}.txt').read_text(encoding='utf-8').lower()
    return re.findall(r'[a-zāīūṛṝḷṅñṭḍṇśṣ]+', t)


def ngrams(ws, n=3):
    return set(tuple(ws[i:i + n]) for i in range(len(ws) - n + 1))


def overlap(a, b, n=3):
    A, B = ngrams(toks(a), n), ngrams(toks(b), n)
    inter = len(A & B)
    return inter / len(A | B), inter / min(len(A), len(B))


PAIRS = [
    ('SP-Pāśupata ↔ Vāyu-Pāśupata (the question)', SP, V),
    ('SP-Pāśupata ↔ parent Skandapurāṇa  (check)', SP, 'skandapurana'),
    ('Vāyu-Pāśupata ↔ parent Vāyupurāṇa   (check)', V, 'vayupurana'),
    ('SP-Pāśupata ↔ ŚiP Vāyavīya         (Śaiva)', SP, 'sivapurana_vayaviyasamhita_au'),
    ('SP-Pāśupata ↔ Brahmāṇḍa          (control)', SP, 'brahmandapurana'),
    ('SP-Pāśupata ↔ MBh 6              (control)', SP, 'mahabharata_06-bhismaparvan'),
]
print(f"{'pair':46} 3-gram Jaccard  containment")
for lab, a, b in PAIRS:
    j, c = overlap(a, b)
    print(f"{lab:46}  {j:8.4f}       {c:6.3f}")

sp, v = toks(SP), toks(V)
sm = difflib.SequenceMatcher(None, sp, v, autojunk=False)
runs = sorted(sm.get_matching_blocks(), key=lambda m: -m.size)
print("\nlongest verbatim shared runs:")
for m in runs[:5]:
    if m.size >= 3:
        print(f"  len {m.size}: {' '.join(sp[m.a:m.a + m.size])}")
tot = sum(m.size for m in sm.get_matching_blocks())
print(f"total aligned overlap: {tot} tokens "
      f"({tot / len(v) * 100:.1f}% of V-Pāś, {tot / len(sp) * 100:.1f}% of SP-Pāś)")
