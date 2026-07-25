#!/usr/bin/env python3
"""Negative control for the Matsyapurāṇa source seam at adhyāya 176/177.

corpus/epic_puranas/matsyapurana_adhyaya-1-176_pu.txt is GRETIL (Hellwig);
matsyapurana_adhyaya-177-291_pu.txt is cleaned from the web e-text at
/mnt2/kengo/E-texts/00_inbox/New/matsya.txt. If the two DIGITIZATIONS carry a
detectable "source signature" (orthography, segmentation, typo profile), a
within-Matsya layer analysis could mistake the seam for a stylistic break.

Test: both sources cover adhyāyas 1-175. Clean the web e-text's 1-175 with the
SAME pipeline as 177-291, then try to classify chunks by SOURCE using the
project's sandhied-C3-style features (char 3-grams, top-500 MFW, Burrows-style
z-scores, nearest-centroid Delta), leave-one-chapter-out so the paired copies
of the held-out chapter are never in the training centroids. Because the
underlying TEXT is (near-)identical, accuracy above chance can only come from
digitization artifacts. ~50% accuracy = seam is safe for that feature set.

Conditions:
  raw        letters + spaces as they come out of each pipeline
  nasal      + homorganic nasal -> anusvāra on both sides
  nasal+nospace  + spaces removed (pure character stream)
  +ortho     + orthographic normalization of the variants that diagnose the
             sources (ṣṭh/ṣṭ, post-r gemination, ttv/tv, cch/ch, avagraha
             stripped) -- applied identically to both sides

Usage: python3 sanity_check_matsya_seam.py [--chunk 3000] [--mfw 500]
"""
import argparse
import re
import sys
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from clean_matsyapurana_177_291 import clean_chapter, INFILE  # noqa: E402

CORPUS = SCRIPT_DIR.parent / 'corpus' / 'epic_puranas'
GRETIL_FILE = CORPUS / 'matsyapurana_pu.txt'  # chs 1-175 therein are GRETIL
OVERLAP = range(1, 176)


def to_letters(text):
    """Approximate build_epic_puranas_sandhied: verse markers/digits/punct out,
    letters + avagraha + single spaces kept, lowercase."""
    text = re.sub(r'//[^/]*?//|Matsya-Purāṇa \d+|Mang\.\d+', ' ', text)
    text = re.sub(r"[^a-zāīūṛṝḷṃḥñṅṇṭḍśṣ' ]", ' ', text.lower())
    return re.sub(r'\s+', ' ', text).strip()


def harmonize_ortho(s):
    """Collapse orthographic variants that differ between the digitizations
    (found empirically by the 3-gram diagnostic; lossy but symmetric)."""
    s = s.replace("'", '').replace('’', '')
    s = s.replace('ṣṭh', 'ṣṭ')
    s = re.sub(r'r([kgcjṭḍtdpbmyvls])\1', r'r\1', s)   # varddh/kāryya/dharmma
    s = s.replace('ttv', 'tv').replace('cch', 'ch')
    return s


def harmonize_nasal(s):
    s = re.sub(r'ñ(?=\s?ch)', 'ṃ', s)
    s = s.replace('ñch', 'ṃś')
    return re.sub(r'ñ(?=\s?[cj])|ṇ(?=\s?[ṭḍ])|n(?=\s?[tdn])|m(?=\s?[bp])|ṅ(?=\s?[kg])',
                  'ṃ', s)


def load_sources():
    gre_raw = GRETIL_FILE.read_text(encoding='utf-8')
    gre = {}
    for m in re.finditer(r'Matsya-Purāṇa (\d+)\n(.*?)(?=Matsya-Purāṇa \d|\Z)',
                         gre_raw, re.S):
        gre[int(m.group(1))] = to_letters(m.group(2))

    web_raw = Path(INFILE).read_text(encoding='utf-8')
    web = {}
    for m in re.finditer(r'title: (\d+)\s*\n\s*---\n(.*?)(?=\ntitle: \d+|\Z)',
                         web_raw, re.S):
        num = int(m.group(1))
        if num in OVERLAP:
            body = clean_chapter(num, m.group(2), lambda w: None)
            web[num] = to_letters('\n'.join(body))
    return gre, web


def chunks_of(s, size):
    out = [s[i:i + size] for i in range(0, len(s), size)]
    return [c for c in out if len(c) >= size // 2]


def run_condition(gre, web, transform, chunk_size, mfw, label):
    # chunk per chapter, tagged (chapter, source)
    data = []  # (chapter, source, chunk_text)
    for ch in OVERLAP:
        if ch not in gre or ch not in web:
            continue
        for c in chunks_of(transform(gre[ch]), chunk_size):
            data.append((ch, 0, c))
        for c in chunks_of(transform(web[ch]), chunk_size):
            data.append((ch, 1, c))

    # top-MFW char 3-grams over everything
    from collections import Counter
    counts = Counter()
    for _, _, c in data:
        for i in range(len(c) - 2):
            counts[c[i:i + 2 + 1]] += 1
    vocab = [g for g, _ in counts.most_common(mfw)]
    vidx = {g: i for i, g in enumerate(vocab)}

    X = np.zeros((len(data), len(vocab)))
    for r, (_, _, c) in enumerate(data):
        n = len(c) - 2
        for i in range(n):
            j = vidx.get(c[i:i + 3])
            if j is not None:
                X[r, j] += 1
        X[r] /= max(n, 1)
    chap = np.array([d[0] for d in data])
    src = np.array([d[1] for d in data])

    correct = total = 0
    for ch in np.unique(chap):
        test, train = chap == ch, chap != ch
        mu, sd = X[train].mean(0), X[train].std(0) + 1e-12
        Z = (X - mu) / sd
        c0 = Z[train & (src == 0)].mean(0)
        c1 = Z[train & (src == 1)].mean(0)
        for r in np.where(test)[0]:
            pred = int(np.abs(Z[r] - c1).mean() < np.abs(Z[r] - c0).mean())
            correct += pred == src[r]
            total += 1
    acc = correct / total
    print(f'{label:16s} chunks={total:4d}  source-classification '
          f'accuracy={acc:.3f}  (chance=0.5)')
    return acc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chunk', type=int, default=3000)
    ap.add_argument('--mfw', type=int, default=500)
    args = ap.parse_args()

    gre, web = load_sources()
    both = sorted(set(gre) & set(web))
    print(f'overlap chapters used: {len(both)} '
          f'({both[0]}-{both[-1]}), chunk={args.chunk}, mfw={args.mfw}')
    run_condition(gre, web, lambda s: s, args.chunk, args.mfw, 'raw')
    run_condition(gre, web, harmonize_nasal, args.chunk, args.mfw, 'nasal')
    run_condition(gre, web, lambda s: harmonize_nasal(s).replace(' ', ''),
                  args.chunk, args.mfw, 'nasal+nospace')
    run_condition(gre, web,
                  lambda s: harmonize_ortho(harmonize_nasal(s)).replace(' ', ''),
                  args.chunk, args.mfw, '+ortho')


if __name__ == '__main__':
    main()
