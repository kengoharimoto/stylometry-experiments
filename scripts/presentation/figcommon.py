"""Shared machinery for the presentation figures (F2-F4).

Mirrors the computations in hero_mds.py (word/3-gram profiles, distance
metrics, classical MDS, hero orientation, Procrustes alignment) so the
companion figures are guaranteed to live in the same layout as the committed
hero plot. hero_mds.py itself is left untouched.
"""
import csv
import re
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
STRATA = ROOT / 'materials/presentation_2026/chronology_strata.tsv'
FIGDIR = ROOT / 'materials/presentation_2026/figures'

PALETTE = {                       # 1 MBh · 2 Rām · 3 old core · 4 old SP ·
    1: '#1f5fa8', 2: '#7ba7d4',   # 5 sectarian & encyclopedic · 6 ŚiP · 7 Bhāgavata ·
    3: '#1a7a3a', 4: '#7a4ba8',   # 8 BhP+comm · 9 Śāstra
    5: '#e08a1e', 6: '#c23b3b', 7: '#e0bf1e', 8: '#7f7f7f', 9: '#3bbfbf',
}
GROUP_ORDER = list(PALETTE)

METRIC_NAMES = {'delta': 'Burrows’s Delta', 'wurzburg': 'Cosine Delta',
                'argamon': 'Argamon’s Delta', 'eder': 'Eder’s Delta',
                'cosine': 'cosine distance', 'euclidean': 'Euclidean distance',
                'manhattan': 'Manhattan distance', 'canberra': 'Canberra distance',
                'minmax': 'min-max distance'}


def load_strata():
    strata, labels_map, notes = {}, {}, {}
    with open(STRATA, encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            strata[row['text']] = int(row['stratum'])
            labels_map[row['text']] = row['label']
            notes[row['text']] = row.get('note', '') or ''
    return strata, labels_map, notes


def word_counts(path):
    return Counter(path.read_text(encoding='utf-8').lower().split())


def trigram_counts(path):
    txt = re.sub(r'\s+', ' ', path.read_text(encoding='utf-8').lower()).strip()
    return Counter(txt[i:i + 3] for i in range(len(txt) - 2))


def load_profiles(features='w', mfw=None):
    """Return (names, X, Z) for feature set 'w' (W1) or 'c' (C3)."""
    w1 = features == 'w'
    mfw = mfw or (80 if w1 else 5000)
    corpus = ROOT / ('corpus/epic_puranas_unsandhied' if w1
                     else 'corpus/epic_puranas_sandhied')
    count_fn = word_counts if w1 else trigram_counts
    names, counts = [], []
    for p in sorted(corpus.glob('*.txt')):
        names.append(p.stem)
        counts.append(count_fn(p))
    raw = Counter()
    for c in counts:
        raw.update(c)
    feats = [w for w, _ in raw.most_common(mfw)]
    totals = [sum(c.values()) for c in counts]
    X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])
    Z = (X - X.mean(0)) / X.std(0)
    return names, feats, X, Z


def distance_matrix(X, Z, metric):
    n, mfw = X.shape
    D = np.zeros((n, n))
    rank_w = (mfw - np.arange(mfw)) / mfw

    def d(i, j):
        a, b, za, zb = X[i], X[j], Z[i], Z[j]
        if metric == 'delta':     return np.abs(za - zb).mean()
        if metric == 'argamon':   return np.linalg.norm(za - zb)
        if metric == 'eder':      return (np.abs(za - zb) * rank_w).sum()
        if metric == 'wurzburg':  return 1 - za @ zb / (np.linalg.norm(za) * np.linalg.norm(zb))
        if metric == 'cosine':    return 1 - a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
        if metric == 'euclidean': return np.linalg.norm(a - b)
        if metric == 'manhattan': return np.abs(a - b).sum()
        if metric == 'canberra':
            s = np.abs(a) + np.abs(b)
            return np.nan_to_num(np.abs(a - b) / np.where(s == 0, 1, s)).sum()
        if metric == 'minmax':    return 1 - np.minimum(a, b).sum() / np.maximum(a, b).sum()

    for i in range(n):
        for j in range(i + 1, n):
            D[i, j] = D[j, i] = d(i, j)
    return D


def cmdscale(D, k=2):
    n = len(D)
    J = np.eye(n) - 1 / n
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1][:k]
    return V[:, idx] * np.sqrt(np.maximum(w[idx], 0))


def hero_layout():
    """The committed hero layout: W1 delta MDS, oriented epics-left-and-low.

    Returns (names, Y, D) with D the W1-delta distance matrix.
    """
    strata, _, _ = load_strata()
    names, _, X, Z = load_profiles('w', 80)
    D = distance_matrix(X, Z, 'delta')
    Y = cmdscale(D)
    epic = np.array([strata[n] == 1 for n in names])
    bhag = np.array([strata[n] == 7 for n in names])   # Bhāgavata (was 8)
    if Y[epic, 0].mean() > Y[~epic, 0].mean():
        Y[:, 0] = -Y[:, 0]
    if Y[bhag, 1].mean() > 0:      # Bhāgavata low: stable anchor for vertical
        Y[:, 1] = -Y[:, 1]
    return names, Y, D


def procrustes_align(Y, Yref):
    """Rotate/reflect (and center) Y onto Yref; returns (Y_aligned, similarity).

    Similarity is the Procrustes correlation statistic in [0, 1].
    """
    A = Yref - Yref.mean(0)
    B = Y - Y.mean(0)
    U, s, Vt = np.linalg.svd(B.T @ A)
    Ya = B @ (U @ Vt)
    sim = s.sum() / (np.linalg.norm(A) * np.linalg.norm(B))
    return Ya, sim
