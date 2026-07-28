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
                                  # shared name is not a shared text
    11: '#d4589e',                # epic Appendix I (rose)
    12: '#0f8bb0',                # Harivaṃśa (azure: epic-family blue, nearest
                                  # neighbours ΔE 12.6/13.0 — point labels carry it)
    13: '#87104a',                # Śivadharma (deep maroon, ≥15 from ŚiP red)
}
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
    'markandeyapurana': 'Mā', 'markandeyapurana_adhyaya-1-80_u': 'Mā1',
    'markandeyapurana_adhyaya-81-93_devimahatmya_u': 'MāD',
    'markandeyapurana_adhyaya-94-141_u': 'Mā9',
    'matsyapurana_pu': 'Mt',
    'vayupurana': 'V', 'vayu_ba': 'V×B', 'visnupurana_u': 'Vi',
    'visnupurana_amsa-1_u': 'Vi1', 'visnupurana_amsa-2_u': 'Vi2',
    'visnupurana_amsa-3_u': 'Vi3', 'visnupurana_amsa-4_u': 'Vi4',
    'visnupurana_amsa-5_u': 'Vi5', 'visnupurana_amsa-6_u': 'Vi6',
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
    # 111-unit additions: dict entries must win over the mahabharata_(\d+)
    # regex, which would misread the appendix filenames as parvans
    'harivamsa': 'HV',
    'mahabharata_02-appendix-21_sisupala': 'MA2',
    'mahabharata_07-appendix-08_sodasarajika': 'MA7',
    'mahabharata_12-appendix-29_moksadharma': 'MA12',
    'mahabharata_13-appendix-15_umamahesvara': 'MA13',
    'mahabharata_14-appendix-04_vaisnavadharma': 'MA14',
    'harivamsa_appendix-29-30_mathura': 'HA29',
    'harivamsa_appendix-31': 'HA31',
    'harivamsa_appendix-41': 'HA41',
    'harivamsa_appendix-42_pradurbhava': 'HA42',
    'sivadharmasastra': 'ŚDh',
    'sivadharmottara': 'ŚDhU',
}

EXTRA_DISPLAY = {
    'harivamsa': 'Harivaṃśa',
    'mahabharata_02-appendix-21_sisupala': 'MBh 2 App. 21 (Śiśupāla)',
    'mahabharata_07-appendix-08_sodasarajika': 'MBh 7 App. 8 (Ṣoḍaśarājika)',
    'mahabharata_12-appendix-29_moksadharma': 'MBh 12 App. 29 (Mokṣadh.)',
    'mahabharata_13-appendix-15_umamahesvara': 'MBh 13 App. 15 (Umāmah.)',
    'mahabharata_14-appendix-04_vaisnavadharma': 'MBh 14 App. 4 (Vaiṣṇavadh.)',
    'harivamsa_appendix-29-30_mathura': 'HV App. 29–30 (Mathurā)',
    'harivamsa_appendix-31': 'HV App. 31',
    'harivamsa_appendix-41': 'HV App. 41',
    'harivamsa_appendix-42_pradurbhava': 'HV App. 42 (prādurbh.)',
    'sivadharmasastra': 'Śivadharmaśāstra',
    'sivadharmottara': 'Śivadharmottara',
}


def code(name):
    if name in CODES:
        return CODES[name]
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
    if name in EXTRA_DISPLAY:
        return EXTRA_DISPLAY[name]
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
        'visnupurana_amsa-1_u': 'Viṣṇu aṃśa 1', 'visnupurana_amsa-2_u': 'Viṣṇu aṃśa 2',
        'visnupurana_amsa-3_u': 'Viṣṇu aṃśa 3', 'visnupurana_amsa-4_u': 'Viṣṇu aṃśa 4',
        'visnupurana_amsa-5_u': 'Viṣṇu aṃśa 5', 'visnupurana_amsa-6_u': 'Viṣṇu aṃśa 6',
        'markandeyapurana': 'Mārkaṇḍeya',
        'markandeyapurana_adhyaya-1-80_u': 'Mārkaṇḍeya 1–80',
        'markandeyapurana_adhyaya-81-93_devimahatmya_u': 'Devīmāhātmya (Mā 81–93)',
        'markandeyapurana_adhyaya-94-141_u': 'Mārkaṇḍeya 94–141',
        'matsyapurana_pu': 'Matsya',
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


def repel_labels(fig, ax, texts, anchors, dot_r=7.0, leader_px=26,
                 max_iter=1000, leader_color='#999999'):
    """Nudge point labels apart until none overlap; draw leader lines.

    texts: ax.text objects already placed at their start positions (data
    coords, ha/va center). anchors: (n, 2) data coordinates of the points the
    labels belong to. Labels repel each other and every point (a label may sit
    next to its own point but not on top of another); pushes act along the
    vector between box centers, which converges where single-axis separation
    deadlocks. Deterministic: identical inputs give the identical layout, so
    color-variant figures stay aligned. A thin leader line ties a label to its
    point once it has drifted more than leader_px. Prints any pair still
    colliding at the iteration cap.
    """
    anchors = np.asarray(anchors)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    dot_disp = ax.transData.transform(anchors)
    pos = np.array([t.get_position() for t in texts])
    for _ in range(max_iter):
        boxes = [t.get_window_extent(renderer).expanded(1.02, 1.02)
                 for t in texts]
        disp = np.array([ax.transData.transform(p) for p in pos])
        shift = np.zeros_like(disp)
        moved = False
        for i in range(len(texts)):
            bi = boxes[i]
            ci = np.array([(bi.x0 + bi.x1) / 2, (bi.y0 + bi.y1) / 2])
            for j in range(i + 1, len(texts)):
                bj = boxes[j]
                ox = min(bi.x1, bj.x1) - max(bi.x0, bj.x0) + 1
                oy = min(bi.y1, bj.y1) - max(bi.y0, bj.y0) + 1
                if ox > 0 and oy > 0:
                    moved = True
                    cj = np.array([(bj.x0 + bj.x1) / 2, (bj.y0 + bj.y1) / 2])
                    v = ci - cj
                    if np.hypot(*v) < 1e-6:
                        v = dot_disp[i] - dot_disp[j]  # coincident: use anchors
                    if np.hypot(*v) < 1e-6:
                        v = np.array([1.0, 0.0])
                    u = v / np.hypot(*v)
                    m = min(ox, oy) / 2
                    shift[i] += u * m; shift[j] -= u * m
            for k, dd in enumerate(dot_disp):
                if k == i:
                    continue           # a label may sit near its own dot
                if (bi.x0 - dot_r < dd[0] < bi.x1 + dot_r and
                        bi.y0 - dot_r < dd[1] < bi.y1 + dot_r):
                    moved = True
                    v = ci - dd
                    u = (v / np.hypot(*v) if np.hypot(*v) > 1e-6
                         else np.array([0.0, 1.0]))
                    shift[i] += u * 1.2
        if not moved:
            break
        disp += np.clip(shift, -3, 3)
        pos = np.array([inv.transform(p) for p in disp])
        for t, p in zip(texts, pos):
            t.set_position(tuple(p))
    else:
        boxes = [t.get_window_extent(renderer) for t in texts]
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                if boxes[i].overlaps(boxes[j]):
                    print(f'  unresolved overlap: {texts[i].get_text()} / '
                          f'{texts[j].get_text()}')

    for t, (x, y) in zip(texts, anchors):
        bb = t.get_window_extent(renderer)
        lab_d = np.array([(bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2])
        pt_d = ax.transData.transform((x, y))
        if np.hypot(*(lab_d - pt_d)) > leader_px:
            lx, ly = inv.transform(lab_d)
            ax.plot([x, lx], [y, ly], color=leader_color, lw=0.7,
                    zorder=2, alpha=0.8)


def label_start_positions(fig, ax, anchors, rise_px=13):
    """Data-coord start positions rise_px above each point (for repel_labels)."""
    fig.canvas.draw()
    inv = ax.transData.inverted()
    disp = ax.transData.transform(np.asarray(anchors))
    return np.array([inv.transform(p + (0, rise_px)) for p in disp])


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
