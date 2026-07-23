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
import matplotlib
import matplotlib.font_manager as fm


def use_sf_pro():
    """Render figures in SF Pro Display (Apple system font), matching the deck.

    IAST coverage verified full; silently keeps the default if SF Pro is absent.
    """
    for f in ('Regular', 'Bold', 'RegularItalic', 'BoldItalic',
              'Semibold', 'Medium', 'Light'):
        try:
            fm.fontManager.addfont(f'/Library/Fonts/SF-Pro-Display-{f}.otf')
        except (FileNotFoundError, OSError):
            pass
    if any('SF Pro Display' in ff.name for ff in fm.fontManager.ttflist):
        matplotlib.rcParams['font.family'] = 'SF Pro Display'


use_sf_pro()

ROOT = Path(__file__).resolve().parents[2]
STRATA = ROOT / 'materials/presentation_2026/chronology_strata.tsv'
FIGDIR = ROOT / 'materials/presentation_2026/figures'

PALETTE = {                       # 1 MBh · 2 Rām · 3 old core · 4 old SP ·
    1: '#1f5fa8', 2: '#7ba7d4',   # 5 sectarian & encyclopedic · 6 ŚiP · 7 Bhāgavata ·
    3: '#1a7a3a', 4: '#7a4ba8',   # 8 BhP+comm · 9 Śāstra · 10 Skāndamahāpurāṇa
    5: '#e08a1e', 6: '#c23b3b', 7: '#e0bf1e', 8: '#7f7f7f', 9: '#3bbfbf',
    10: '#6b4423',                # deliberately unlike the old-SP purple: the
}                                 # shared name is not a shared text
GROUP_ORDER = list(PALETTE)

METRIC_NAMES = {'delta': 'Burrows’s Delta', 'wurzburg': 'Cosine Delta',
                'argamon': 'Argamon’s Delta', 'eder': 'Eder’s Delta',
                'cosine': 'cosine distance', 'euclidean': 'Euclidean distance',
                'manhattan': 'Manhattan distance', 'canberra': 'Canberra distance',
                'minmax': 'min-max distance'}


# ── Point codes (follow the texts' own book numbering) and display names ─────
CODES = {
    'brahmandapurana': 'Bḍ', 'brahmandapurana_khanda-1_u': 'Bḍ1',
    'brahmandapurana_khanda-2_u': 'Bḍ2', 'brahmandapurana_khanda-3_u': 'Bḍ3',
    'markandeyapurana_adhyaya-1-93_u': 'Mā',
    'matsyapurana_adhyaya-1-176_pu': 'Mt',
    'vayupurana': 'V', 'vayu_ba': 'V×B', 'visnupurana_u': 'Vi',
    'brahmapurana_pu': 'Br', 'devipurana': 'Dv',
    'kurmapurana_khanda-1_u': 'K1', 'kurmapurana_khanda-2_u': 'K2',
    'lingapurana_khanda-1_u': 'L1', 'lingapurana_khanda-2_u': 'L2',
    'nilamatapurana_au': 'Nī', 'nrsimhapurana_pu': 'Nṛ',
    'vamanapurana_saromahatmya_u': 'Sr', 'vamanapurana_u': 'Vm',
    'visnudharma_pu': 'Vd',
    'visnudharmottarapurana_khanda-3_adhyaya-343-353_pu': 'Vt',
    'skandapurana': 'SP', 'skandapurana_adhyaya-1-31_pu': 'SP1',
    'skandapurana_pasupata_adhyaya174-183_u': 'SP2',
    'agnipurana_u': 'A', 'bhavisyapurana': 'Bhv',
    'devibhagavatapurana': 'DB', 'devibhagavatapurana_devigita_adhyaya-31-40': 'DG',
    'garudapurana_khanda-1_u': 'G1', 'garudapurana_khanda-2_u': 'G2',
    'garudapurana_khanda-3_u': 'G3',
    'kalikapurana': 'Kā', 'karatoyamahatmya_pu': 'Kt',
    'naradapurana_khanda-1_u': 'N1', 'naradapurana_khanda-2_u': 'N2',
    'padmapurana_a': 'Pd', 'saurapurana': 'Sau',
    'skandamahapurana_kasikhanda': 'Kś', 'skandamahapurana_himavatkhanda': 'Hm',
    'skandamahapurana_revakhanda': 'Rv', 'vayupurana_revakhanda': 'RvV',
    'skandamahapurana_sutasamhita_khanda-4': 'Sū',
    'sivapurana_dharmasamhita': 'Dh', 'sivapurana_karvanamahatmya_au': 'Kv',
    'sivapurana_rudrasamhita': 'Ru', 'sivapurana_sanatkumarasamhita': 'Sn',
    'sivapurana_satarudrasamhita_au': 'Śt', 'sivapurana_umasamhita': 'U',
    'sivapurana_vayaviyasamhita_au': 'Vā', 'sivapurana_vidyesvarasamhita_au': 'Vy',
    'bhagavatapurana_skandha-10_adhyaya-29-33_w_commentary': 'Bh10c',
    'pranavakalpa': 'Pk',
}


def code(name):
    m = re.match(r'mahabharata_(\d+)', name)
    if m:
        return f'MBh{int(m.group(1))}'
    m = re.match(r'ramayana_(\d+)', name)
    if m:
        return f'R{int(m.group(1))}'
    m = re.match(r'bhagavatapurana_skandha-(\d+)_u', name)
    if m:
        return f'Bh{int(m.group(1))}'
    m = re.match(r'vayupurana_(\d+)_', name)
    if m:
        return f'V{int(m.group(1))}'
    return CODES[name]


def display(name):
    m = re.match(r'mahabharata_(\d+)', name)
    if m:
        return f'MBh {int(m.group(1))}'
    m = re.match(r'ramayana_(\d+)', name)
    if m:
        return f'Rām {int(m.group(1))}'
    m = re.match(r'bhagavatapurana_skandha-(\d+)_u', name)
    if m:
        return f'BhP {int(m.group(1))}'
    m = re.match(r'vayupurana_(\d+)_', name)
    if m:
        return f'Vāyu §{int(m.group(1))}'
    special = {
        'bhagavatapurana_skandha-10_adhyaya-29-33_w_commentary': 'BhP 10 + comm.',
        'vayu_ba': 'Vāyu×BḍP', 'vayupurana': 'Vāyu',
        'vayupurana_revakhanda': 'Revākh. (Vāyu)',
        'skandamahapurana_revakhanda': 'Revākh. (SkMP)',
        'skandamahapurana_kasikhanda': 'Kāśīkh. (SkMP)',
        'skandamahapurana_himavatkhanda': 'Himavatkh. (SkMP)',
        'skandapurana': 'SP (old)', 'skandapurana_adhyaya-1-31_pu': 'SP (old) 1–31',
        'skandapurana_pasupata_adhyaya174-183_u': 'SP (old) Pāśupata',
        'markandeyapurana_adhyaya-1-93_u': 'Mārkaṇḍeya 1–93',
        'matsyapurana_adhyaya-1-176_pu': 'Matsya 1–176',
        'devibhagavatapurana_devigita_adhyaya-31-40': 'Devīgītā (DBhP 7.31–40)', 'devibhagavatapurana': 'DevīBhP',
        'visnudharmottarapurana_khanda-3_adhyaya-343-353_pu': 'ViDhUt (exc.)',
        'visnudharma_pu': 'Viṣṇudharma',
        'vamanapurana_saromahatmya_u': 'Saromāhātmya',
        'skandamahapurana_sutasamhita_khanda-4': 'Sūtasaṃhitā 4',
        'karatoyamahatmya_pu': 'Karatoyā', 'nilamatapurana_au': 'Nīlamata',
        'pranavakalpa': 'Praṇavakalpa',
    }
    if name in special:
        return special[name]
    base = re.sub(r'purana.*', '', name).capitalize()
    iast = {'Visnu': 'Viṣṇu', 'Kurma': 'Kūrma', 'Linga': 'Liṅga',
            'Nrsimha': 'Nṛsiṃha', 'Garuda': 'Garuḍa', 'Narada': 'Nārada',
            'Kalika': 'Kālikā', 'Devi': 'Devī', 'Bhavisya': 'Bhaviṣya',
            'Sivapurana': 'ŚiP', 'Saura': 'Saura',
            'Brahmanda': 'Brahmāṇḍa', 'Vamana': 'Vāmana'}
    base = iast.get(base, base)
    if name.startswith('sivapurana_'):
        part = name.split('_')[1].replace('samhita', '').replace('mahatmya', ' māh.')
        part_iast = {'karvana māh.': 'Kārvaṇa māh.', 'sanatkumara': 'Sanatkumāra',
                     'satarudra': 'Śatarudra', 'uma': 'Umā',
                     'vayaviya': 'Vāyavīya', 'vidyesvara': 'Vidyeśvara'}
        return 'ŚiP ' + part_iast.get(part, part.capitalize())
    m = re.search(r'khanda-(\d+)', name)
    if m:
        return f'{base} {m.group(1)}'
    return base


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
