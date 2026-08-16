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
"""
import csv
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
CORPUS = ROOT / 'corpus/epic_puranas_unsandhied'
COORDS = {'W1': ROOT / 'materials/presentation_2026/figures/mfw_sweep/coords_W1_mfw500.tsv',
          'C3': ROOT / 'materials/presentation_2026/figures/c3_nospace/coords_nospace_mfw500.tsv'}
DETREND = HERE / 'b5_arch_residuals.tsv'

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
names, covs = [], []
for p in sorted(CORPUS.glob('*.txt')):
    if p.stem in manifest:
        names.append(p.stem)
        covs.append(rates(p.read_text(encoding='utf-8').lower().split()))
COVS = list(covs[0])

xy = {}
for lens, path in COORDS.items():
    with open(path, encoding='utf-8') as f:
        xy[lens] = {r['text']: (float(r['x']), float(r['y']))
                    for r in csv.DictReader(f, delimiter='\t')}
det = {}
with open(DETREND, encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        det[r['text']] = (float(r['y_detrended_W1']), float(r['y_detrended_C3']))

M = {k: np.array([c[k] for c in covs]) for k in COVS}
out_rows = []
print(f'{"covariate":<16}', end='')
for lens in ('W1', 'C3'):
    print(f'  {lens}: y_raw  y_det      x', end='')
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
    out_rows.append(row)
    print(line)

with open(HERE / 'q3_y_covariates.tsv', 'w', encoding='utf-8') as f:
    ks = ['covariate'] + [f'{l}_{s}' for l in ('W1', 'C3')
                          for s in ('y_raw', 'y_det', 'x')]
    f.write('\t'.join(ks) + '\n')
    for r in out_rows:
        f.write('\t'.join(str(r[k]) if k == 'covariate' else f'{r[k]:.4f}'
                          for k in ks) + '\n')

# per-unit covariate dump (for C4 and the article's appendix)
with open(HERE / 'q3_unit_covariates.tsv', 'w', encoding='utf-8') as f:
    f.write('text\t' + '\t'.join(COVS) + '\n')
    for n, c in zip(names, covs):
        f.write(n + '\t' + '\t'.join(f'{c[k]:.4f}' for k in COVS) + '\n')

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
print('\nwrote q3_y_covariates.tsv, q3_unit_covariates.tsv')
