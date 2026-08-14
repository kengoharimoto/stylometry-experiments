#!/usr/bin/env python3
"""W1-500 sensitivity test: strike proper names / ritual lexemes from the MFW
list (refilling to 500 from deeper ranks) and measure how much the drift axis
moves. Pipeline replicates hero_mds.py: relative freqs, corpus z-score,
Burrows's Delta, classical MDS; variants Procrustes-aligned to baseline."""
import numpy as np
from pathlib import Path
from collections import Counter
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[4]
MFW = 500

manifest = {l.strip()[:-4] if l.strip().endswith('.txt') else l.strip()
            for l in (ROOT / 'manifests/dicsep2026_n127_ppl.txt').read_text().splitlines()
            if l.strip() and not l.startswith('#')}
names, counts = [], []
for p in sorted((ROOT / 'corpus/epic_puranas_unsandhied').glob('*.txt')):
    if p.stem in manifest:
        names.append(p.stem)
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

# validate against the saved sweep coordinates
saved = {}
for l in (ROOT / 'materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv'
          ).read_text().splitlines()[1:]:
    f = l.split('\t')
    saved[f[0]] = float(f[1])
sx = np.array([saved[n] for n in names])
r0 = abs(spearmanr(base[:, 0], sx).statistic)
if spearmanr(base[:, 0], sx).statistic < 0:      # fix sign to match saved convention
    base = -base
print(f'baseline vs saved sweep coords: |rho| = {r0:.4f}')

for label, excl in (('names-only', NAMES), ('names+ritual', RITUAL)):
    feats = [w for w in ranked if w not in excl][:MFW]
    struck = [w for w in base_feats if w in excl]
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
