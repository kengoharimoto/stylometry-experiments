#!/usr/bin/env python3
"""Q3-C3 (axis-anatomy plan): what does the y-axis correlate with?

y is real and shared (B5: cross-lens rho 0.82-0.84; arch negligible), so
it deserves a name. Candidate covariates, computed per unit from the
unsandhied token stream, in the plan's order of prior plausibility:
sectarian register (Saiva / Vaisnava / goddess lexica; theonym and ritual
vocabulary), discourse form (speech-frame density, vocatives, optative and
imperative shares, quotative iti), and the boring confounds (log length).
Each is Spearman-correlated with raw and arch-detrended y on both lenses
(x shown for contrast). C4: the same within families that hold x roughly
constant. Meter mix is skipped: source lineation is edition-specific, so
syllable counting per line does not identify metre reliably.

2026-08-21 (--noreuse): the identical design on the no-reuse build
(residue corpus, manifest noreuse2026_n126, y from the article-oriented
mds3d coords). Differences: detrending is an inline quadratic fit of y
on x (no b5 residual file exists for this build); the arch R^2 and the
cross-lens rho_y are printed (committed source for draft §9.1); a
robustness column drops sub-3k-word residues; y is flipped if needed so
the BhP pole is low (the with-reuse convention). Outputs suffixed
_noreuse.
"""
import csv
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
NOREUSE = '--noreuse' in sys.argv
if NOREUSE:
    MANIFEST = ROOT / 'manifests/noreuse2026_n126.txt'
    CORPUS = ROOT / 'corpus/epic_puranas_unsandhied_noreuse'
    _MDS3D = ROOT / 'materials/presentation_2026/figures/mds3d'
    COORDS = {'W1': _MDS3D / 'coords_W1-500_noreuse_n126.tsv',
              'C3': _MDS3D / 'coords_C3-500ns_noreuse_n126.tsv'}
    DETREND = None      # inline quadratic detrend below
    SUFFIX = '_noreuse'
else:
    MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
    CORPUS = ROOT / 'corpus/epic_puranas_unsandhied'
    COORDS = {'W1': ROOT / 'materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv',
              'C3': ROOT / 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv'}
    DETREND = HERE / 'b5_arch_residuals.tsv'
    SUFFIX = ''

SAIVA = set('''śiva śivaḥ śivam śivasya śivāya śivena rudra rudraḥ rudrasya
rudram hara haraḥ haram śaṃkara śaṃkaraḥ śaṃkaram maheśvara maheśvaraḥ
maheśvaram mahādeva mahādevaḥ mahādevam īśāna īśānaḥ śambhu śambhuḥ śambhum
umā umāṃ gaurī pārvatī pārvatīṃ liṅga liṅgam liṅge tryambaka paśupatiḥ
śūlapāṇiḥ nīlakaṇṭha kapardin bhairava bhairavaḥ'''.split())
VAISNAVA = set('''viṣṇu viṣṇuḥ viṣṇum viṣṇoḥ hari hariḥ harim hareḥ kṛṣṇa
kṛṣṇaḥ kṛṣṇam kṛṣṇasya vāsudeva vāsudevaḥ vāsudevam nārāyaṇa nārāyaṇaḥ
nārāyaṇam keśava keśavaḥ keśavam govinda govindaḥ janārdana janārdanaḥ
madhusūdana madhusūdanaḥ hṛṣīkeśa hṛṣīkeśaḥ acyuta acyutaḥ dāmodara
puruṣottama puruṣottamaḥ cakrapāṇiḥ'''.split())
GODDESS = set('''devī devīṃ devyāḥ devyā caṇḍī caṇḍikā caṇḍikāṃ durgā durgāṃ
kālī ambikā ambikāṃ bhagavatī bhagavatīṃ śakti śaktiḥ śaktim kātyāyanī
caṇḍa muṇḍa mahiṣāsura'''.split())
SPEECH = set('uvāca ūcuḥ āha āhuḥ abravīt abruvan provāca prāha avadat'.split())
VOCATIVE = set('''rājan mahārāja bhārata kaunteya pārtha tāta vibho prabho
mahābāho devi bhagavan brahman bho rājendra nṛpa nṛpaśreṣṭha dvijāḥ
viprāḥ munayaḥ maharṣe'''.split())

# names/ritual lists shared with the exclusion test (kept in sync by hand)
import importlib.util as _il
_spec = _il.spec_from_file_location(
    'excl', ROOT / 'materials/presentation_2026/figures/mfw_sweep/exclusion_test.py')
NAMES_RITUAL = None  # loaded lazily below without executing the test itself


def rates(toks):
    n = len(toks)
    c = Counter(toks)
    def rt(s):
        return 1000 * sum(c[w] for w in s) / n
    opt = sum(v for w, v in c.items()
              if ((w.endswith('et') and len(w) >= 4 and w not in ('cet', 'ced'))
                  or w.endswith('yāt') or w.endswith('eyuḥ') or w == 'syāt'))
    imp = sum(v for w, v in c.items()
              if (w.endswith('ntu') or (w.endswith('tu') and len(w) >= 4)))
    tot = SAIVA | VAISNAVA | GODDESS
    s, v_, g = rt(SAIVA), rt(VAISNAVA), rt(GODDESS)
    denom = s + v_ + g
    return {'saiva': s, 'vaisnava': v_, 'goddess': g,
            'sect_total': rt(tot),
            'saiva_polarity': (s - v_) / denom if denom > 0 else 0.0,
            'speech': rt(SPEECH), 'vocative': rt(VOCATIVE),
            'iti': 1000 * c['iti'] / n,
            'optative': 1000 * opt / n, 'imperative': 1000 * imp / n,
            'log_len': float(np.log(n))}


manifest = {l.strip().removesuffix('.txt') for l in
            MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}
names, covs, nwords = [], [], []
for p in sorted(CORPUS.glob('*.txt')):
    if p.stem in manifest:
        toks = p.read_text(encoding='utf-8').lower().split()
        names.append(p.stem)
        covs.append(rates(toks))
        nwords.append(len(toks))
nwords = np.array(nwords)
COVS = list(covs[0])

xy = {}
for lens, path in COORDS.items():
    with open(path, encoding='utf-8') as f:
        xy[lens] = {r['text']: (float(r['x']), float(r['y']))
                    for r in csv.DictReader(f, delimiter='\t')}
if NOREUSE:
    # y sign convention: cross-lens-consistent, devotional pole low.
    # (The with-reuse "BhP-low" rule fails here — on this build the
    # BhP's in-plane y position is lens-dependent because its
    # idiosyncrasy is banked on axis 3, cf. axis3_stats.tsv.)
    yW = np.array([xy['W1'][n][1] for n in names])
    yC = np.array([xy['C3'][n][1] for n in names])
    if spearmanr(yW, yC).statistic < 0:
        print('flipping C3 y for cross-lens sign agreement')
        for n in names:
            xy['C3'][n] = (xy['C3'][n][0], -xy['C3'][n][1])
        yC = -yC
    sect = np.array([c['sect_total'] for c in covs])
    if spearmanr(sect, yW).statistic > 0:
        print('flipping both y so the devotional pole is low')
        for lens in ('W1', 'C3'):
            for n in names:
                xy[lens][n] = (xy[lens][n][0], -xy[lens][n][1])
    print(f'cross-lens rho_y (raw, in-plane) = '
          f'{spearmanr(yW, yC).statistic:.3f}')
    det = {n: [0.0, 0.0] for n in names}
    for li, lens in enumerate(('W1', 'C3')):
        x = np.array([xy[lens][n][0] for n in names])
        y = np.array([xy[lens][n][1] for n in names])
        coef = np.polyfit(x, y, 2)
        fit = np.polyval(coef, x)
        ss = 1 - ((y - fit) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        print(f'{lens}: arch R^2 (y ~ quadratic x) = {ss:.3f}')
        for n, r in zip(names, y - fit):
            det[n][li] = float(r)
    bhp = np.array([n.startswith('bhagavatapurana') for n in names])
    for lens in ('W1', 'C3'):
        y = np.array([xy[lens][n][1] for n in names])
        print(f'{lens}: BhP mean in-plane y {y[bhp].mean():+.3f} vs rest '
              f'{y[~bhp].mean():+.3f} (SD rest {y[~bhp].std():.3f})')
else:
    det = {}
    with open(DETREND, encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            det[r['text']] = (float(r['y_detrended_W1']), float(r['y_detrended_C3']))

M = {k: np.array([c[k] for c in covs]) for k in COVS}
mask3k = nwords >= 3000
out_rows = []
hdr3k = '  y_3k' if NOREUSE else ''
print(f'{"covariate":<16}', end='')
for lens in ('W1', 'C3'):
    print(f'  {lens}: y_raw  y_det      x{hdr3k}', end='')
print()
for k in COVS:
    line = f'{k:<16}'
    row = {'covariate': k}
    for li, lens in enumerate(('W1', 'C3')):
        x = np.array([xy[lens][n][0] for n in names])
        y = np.array([xy[lens][n][1] for n in names])
        yd = np.array([det[n][li] for n in names])
        a = spearmanr(M[k], y).statistic
        b = spearmanr(M[k], yd).statistic
        c_ = spearmanr(M[k], x).statistic
        row[f'{lens}_y_raw'], row[f'{lens}_y_det'], row[f'{lens}_x'] = a, b, c_
        line += f'   {a:>6.2f} {b:>6.2f} {c_:>6.2f}'
        if NOREUSE:
            a3 = spearmanr(M[k][mask3k], y[mask3k]).statistic
            row[f'{lens}_y_raw3k'] = a3
            line += f' {a3:>6.2f}'
    out_rows.append(row)
    print(line)

# combined rank-OLS (the write-up's "about half the rank variance")
def rank(v):
    return np.argsort(np.argsort(v)).astype(float)
for lens in ('W1', 'C3'):
    y = rank(np.array([xy[lens][n][1] for n in names]))
    X = np.column_stack([rank(M[k]) for k in
                         ('sect_total', 'optative', 'speech', 'vaisnava',
                          'log_len')] + [np.ones(len(names))])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r2 = 1 - ((y - X @ beta) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    print(f'{lens}: combined rank-OLS R^2 '
          f'(sect_total+optative+speech+vaisnava+log_len) = {r2:.3f}')

ks3k = [f'{l}_y_raw3k' for l in ('W1', 'C3')] if NOREUSE else []
with open(HERE / f'q3_y_covariates{SUFFIX}.tsv', 'w', encoding='utf-8') as f:
    ks = ['covariate'] + [f'{l}_{s}' for l in ('W1', 'C3')
                          for s in ('y_raw', 'y_det', 'x')] + ks3k
    f.write('\t'.join(ks) + '\n')
    for r in out_rows:
        f.write('\t'.join(str(r[k]) if k == 'covariate' else f'{r[k]:.4f}'
                          for k in ks) + '\n')

# per-unit covariate dump (for C4 and the article's appendix)
with open(HERE / f'q3_unit_covariates{SUFFIX}.tsv', 'w', encoding='utf-8') as f:
    f.write('text\twords\t' + '\t'.join(COVS) + '\n')
    for n, c, w in zip(names, covs, nwords):
        f.write(n + f'\t{w}\t' + '\t'.join(f'{c[k]:.4f}' for k in COVS) + '\n')

# C4: within families holding x roughly constant
FAMS = {'MBh parvans': lambda n: n.startswith('mahabharata_') and 'appendix' not in n,
        'Ram kandas': lambda n: n.startswith('ramayana'),
        'BhP skandhas': lambda n: n.startswith('bhagavatapurana_skandha') and 'comment' not in n,
        'SiP samhitas': lambda n: n.startswith('sivapurana_')}
print('\nC4 within-family (W1 raw y):')
for fam, pred in FAMS.items():
    idx = [i for i, n in enumerate(names) if pred(n)]
    if len(idx) < 5:
        continue
    y = np.array([xy['W1'][names[i]][1] for i in idx])
    print(f'  {fam} (n={len(idx)}):')
    for k in ('saiva_polarity', 'sect_total', 'speech', 'optative', 'iti'):
        v = np.array([M[k][i] for i in idx])
        if np.all(v == v[0]):
            continue
        print(f'    rho(y, {k:<15}) = {spearmanr(y, v).statistic:>6.2f}')
print('\n  SiP samhitas by y (W1), with covariates:')
sip = sorted([i for i, n in enumerate(names) if names[i].startswith('sivapurana_')],
             key=lambda i: xy['W1'][names[i]][1])
for i in sip:
    n = names[i]
    print(f'    {n:<42} y {xy["W1"][n][1]:>7.3f}  saiva {M["saiva"][i]:>5.1f} '
          f'speech {M["speech"][i]:>4.1f} opt {M["optative"][i]:>5.1f}')
print(f'\nwrote q3_y_covariates{SUFFIX}.tsv, q3_unit_covariates{SUFFIX}.tsv')
