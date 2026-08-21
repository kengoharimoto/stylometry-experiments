#!/usr/bin/env python3
"""W1-500 sensitivity test: strike proper names / ritual lexemes from the MFW
list (refilling to 500 from deeper ranks) and measure how much the drift axis
moves. Pipeline replicates hero_mds.py: relative freqs, corpus z-score,
Burrows's Delta, classical MDS; variants Procrustes-aligned to baseline.

2026-08-21: --noreuse runs the identical test on the no-reuse build
(residue corpus, manifest noreuse2026_n126, reference coords from
mds3d). --c3 runs a trigram-level analogue on the no-space sandhied
stream: a trigram is struck if it is a substring of ANY listed
name/ritual lexeme (lowercased, diacritics as written). That rule is
deliberately over-broad — it also removes generic trigrams like 'iva'
that happen to occur inside 'śiva' — so a surviving axis is a
conservative (stronger) robustness statement. Gate note: on the
no-reuse W1 build only the ordering-level rho vs baseline is citable
(R1: per-unit percentiles carry a length component); the C3-noreuse
run is the citation-grade form."""
import re
import sys
import numpy as np
from pathlib import Path
from collections import Counter
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[4]
MFW = 500
NOREUSE = '--noreuse' in sys.argv
C3 = '--c3' in sys.argv
TAG = ('C3' if C3 else 'W1') + ('_noreuse' if NOREUSE else '')

if NOREUSE:
    MANIFEST = ROOT / 'manifests/noreuse2026_n126.txt'
    CORPUS = ROOT / ('corpus/epic_puranas_sandhied_noreuse' if C3
                     else 'corpus/epic_puranas_unsandhied_noreuse')
    REFC = ROOT / ('materials/presentation_2026/figures/mds3d/'
                   + ('coords_C3-500ns_noreuse_n126.tsv' if C3
                      else 'coords_W1-500_noreuse_n126.tsv'))
else:
    MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
    CORPUS = ROOT / ('corpus/epic_puranas_sandhied' if C3
                     else 'corpus/epic_puranas_unsandhied')
    REFC = ROOT / ('materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv'
                   if C3 else
                   'materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv')

manifest = {l.strip()[:-4] if l.strip().endswith('.txt') else l.strip()
            for l in MANIFEST.read_text().splitlines()
            if l.strip() and not l.startswith('#')}
names, counts = [], []
for p in sorted(CORPUS.glob('*.txt')):
    if p.stem in manifest:
        names.append(p.stem)
        if C3:
            s = re.sub(r'\s+', '', p.read_text(encoding='utf-8').lower())
            counts.append(Counter(s[i:i + 3] for i in range(len(s) - 2)))
        else:
            counts.append(Counter(p.read_text(encoding='utf-8').lower().split()))
raw = Counter()
for c in counts:
    raw.update(c)
ranked = [w for w, _ in raw.most_common()]
totals = [sum(c.values()) for c in counts]

# ── exclusion lists ──────────────────────────────────────────────────────────
NAMES = set('''śiva śivaḥ śivam bhagavān kṛṣṇa kṛṣṇaḥ kṛṣṇam viṣṇu viṣṇuḥ
viṣṇoḥ viṣṇum devī devīm devyāḥ devi indra indraḥ brahmā īśvaraḥ īśvara
īśvaram īśa maheśvaraḥ mahādevaḥ hari hariḥ harim hareḥ rāma rāmaḥ rāmam
bhīṣmaḥ yudhiṣṭhiraḥ yudhiṣṭhira bhārata bharata sūrya candra soma agni agniḥ
vāyu vāyuḥ gaṅgā nāradaḥ nārada vyāsaḥ mārkaṇḍeyaḥ vaiśaṃpāyanaḥ śakra śakraḥ
yama nārāyaṇaḥ nārāyaṇa prajāpatiḥ rudra vasiṣṭhaḥ arka śaṃkara śaṃkaraḥ
umā gaurī pārvatī skanda skandaḥ gaṇeśa lakṣmī sītā arjunaḥ arjuna pārtha
pārthaḥ pāṇḍava pāṇḍavāḥ kaunteya bhīma bhīmaḥ droṇa droṇaḥ karṇa karṇaḥ
duryodhana duryodhanaḥ rāvaṇa rāvaṇaḥ hanumān lakṣmaṇa lakṣmaṇaḥ garuḍa
garuḍaḥ'''.split())
RITUAL = NAMES | set('''namaḥ śrāddham pūjā pūjām pūjayet liṅgam liṅga snātvā
snānam vratam vrata svāhā yajña yajñaḥ tīrtham tīrtha tīrthe om bhaktyā
bhakti mantra mantram dhyāna dhyānam mokṣa mokṣaḥ svarga svargam veda vedāḥ
śakti śaktiḥ māyā māyayā tapaḥ tapasā daitya dānava dānavāḥ asura asurāḥ
rākṣasa rākṣasāḥ nāga dharma dharmaḥ dharmam brahma brahmaṇaḥ brahmaṇā
pitṛ pitaraḥ pitṝn pitṝṇām śrī devatāḥ prasādāt jajñe'''.split())

def build_axis(feats):
    X = np.array([[c.get(w, 0) / t for w in feats] for c, t in zip(counts, totals)])
    Z = (X - X.mean(0)) / X.std(0)
    D = np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)
    n = len(names)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    vals, vecs = np.linalg.eigh(B)
    idx = np.argsort(vals)[::-1]
    Y = vecs[:, idx[:2]] * np.sqrt(np.maximum(vals[idx[:2]], 0))
    return Y

def procrustes(Y, ref):
    Yc = Y - Y.mean(0); Rc = ref - ref.mean(0)
    U, _, Vt = np.linalg.svd(Yc.T @ Rc)
    return Yc @ U @ Vt

base_feats = ranked[:MFW]
base = build_axis(base_feats)

# orient the baseline into the article frame: on C3 the raw MDS axis 1
# sits ~22-28 deg from the published drift axis (near-degenerate top
# eigenpair), so Procrustes-rotate the base plane onto the saved
# reference coords before any axis-1 comparison (2026-08-21 fix; the
# W1 frames are identical, rho 1.0, so W1 results are unchanged)
saved = {}
for l in REFC.read_text().splitlines()[1:]:
    f = l.split('\t')
    saved[f[0]] = (float(f[1]), float(f[2]))
SX = np.array([saved[n] for n in names])
base = procrustes(base, SX - SX.mean(0))
r0 = spearmanr(base[:, 0], SX[:, 0]).statistic
assert r0 > 0.9, f'baseline does not reproduce the article frame: {r0}'
print(f'[{TAG}] baseline (article-frame) vs saved reference coords: '
      f'rho = {r0:.4f}')
if NOREUSE and not C3:
    print('NOTE (R1 gate): W1-noreuse — only the ordering-level rho vs '
          'baseline below is citable; per-unit percentiles are not.')


def is_struck(feat, excl):
    if C3:
        return any(feat in w for w in excl)
    return feat in excl


tsv = open(Path(__file__).parent / f'exclusion_results_{TAG}.tsv', 'w',
           encoding='utf-8')
tsv.write('variant\tstruck_of_500\trho_axis1\trho_axis2\tmax_mover_pct\n')

for label, excl in (('names-only', NAMES), ('names+ritual', RITUAL)):
    feats = [w for w in ranked if not is_struck(w, excl)][:MFW]
    struck = [w for w in base_feats if is_struck(w, excl)]
    Y = procrustes(build_axis(feats), base)
    rho1 = spearmanr(Y[:, 0], base[:, 0]).statistic
    rho2 = spearmanr(Y[:, 1], base[:, 1]).statistic
    print(f'\n=== {label}: struck {len(struck)} of top-500, refilled to 500 ===')
    print('struck:', ' '.join(struck))
    print(f'axis-1 Spearman rho vs baseline: {rho1:.4f}   (axis-2: {rho2:.4f})')
    # biggest movers on the drift axis (percentile ranks)
    pb = np.argsort(np.argsort(base[:, 0])) / (len(names) - 1) * 100
    pv = np.argsort(np.argsort(Y[:, 0])) / (len(names) - 1) * 100
    dd = pv - pb
    order = np.argsort(-np.abs(dd))
    print('biggest movers (unit: base pct -> variant pct):')
    for i in order[:8]:
        print(f'  {names[i]}: {pb[i]:.0f} -> {pv[i]:.0f}  ({dd[i]:+.0f})')
    bhp = [i for i, n in enumerate(names) if n.startswith('bhagavatapurana')]
    print(f'BhP skandhas mean pct: {pb[bhp].mean():.1f} -> {pv[bhp].mean():.1f}')
    tsv.write(f'{label}\t{len(struck)}\t{rho1:.4f}\t{rho2:.4f}\t'
              f'{np.abs(dd).max():.1f}\n')

tsv.close()
print(f'wrote exclusion_results_{TAG}.tsv')
