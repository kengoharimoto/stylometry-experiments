#!/usr/bin/env python3
"""A2 bridge: are the word classes behind the W1 axis equally reflected in C3?

Every token of every no-space C3 top-500 trigram is attributed to its
source: the word it sits inside (with position: whole/initial/final/
interior) or, for junction-spanning trigrams, the word contributing the
majority of its characters. Source words (sandhied surface tokens) are
classified with the SAME rule-based classifier applied to the W1-500 list
(particle/indeclinable, pronoun, narrative verb form, prescriptive verb
form, numeral-and-list machinery, content). Then the axis signal
(|rho_x|-weighted) is decomposed by class on both lenses and compared.

Classifier is provisional pending Kengo's A2 review; assignments are
dumped for that review (w1_class_assignments.tsv).
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path('/mnt/kengo/stylometry-experiments')
HERE = Path(__file__).parent
MANIFEST = ROOT / 'manifests/dicsep2026_n127_ppl.txt'
SANDHIED = ROOT / 'corpus/epic_puranas_sandhied'

# ── the classifier ───────────────────────────────────────────────────────────
INDECL = {l.strip() for l in
          (ROOT / 'materials/feature_sets/sanskrit_indeclinables_clean.txt')
          .read_text(encoding='utf-8').splitlines() if l.strip()}
INDECL |= {'caiva', 'cāpi', 'vāpi', 'naiva', 'tathaiva', 'yathaiva', 'hyeva',
           'tveva', 'caivam', 'no', 'cid', 'cit', 'svid'}
PRON = set('''sa saḥ tam taṃ tat tad te tau tān tena tasya tasmai tasmāt
tasmin tayā tayoḥ tābhiḥ tāsām teṣām teṣu taiḥ tā tāḥ tām tāṃ tasyāḥ tasyām
eṣa eṣaḥ etat etad etam ete etān etena etasya eṣā etām enam enaṃ enām enat
ayam iyam idam imam imāṃ imām ime imān anena asya asmai asmāt asmin anayā
ebhiḥ eṣām eṣu asau amum yaḥ yat yad yam yaṃ ye yau yān yena yasya yasmai
yasmāt yasmin yayā yeṣām yeṣu yaiḥ yā yāḥ yām yāṃ yasyāḥ kaḥ kim kam kaṃ ke
kena kasya kasmai kasmāt kasmin kaiḥ kā kāṃ aham mām māṃ mayā mama mahyam
mayi vayam naḥ asmān asmābhiḥ asmākam tvam tvām tvayā tava tubhyam tvayi
yūyam vaḥ yuṣmān bhavān bhavantam bhavatā svam svayam'''.split())
VERB_NARR = set('''uvāca ūcuḥ āha āhuḥ abravīt abruvan avadat provāca
prāha āsīt āsan abhavat abhavan babhūva babhūvuḥ jagāma jagmuḥ āgamat
āyayau yayau prayayau āsa cakāra cakruḥ dadau dadhau jajñe'''.split())
NUM_STEMS = ('eka', 'dvi', 'dvā', 'tri', 'catur', 'catvār', 'pañca', 'ṣaṣ',
             'ṣaḍ', 'sapta', 'aṣṭa', 'nava', 'daśa', 'śata', 'sahasra',
             'ayuta', 'koṭi')
ADI_FORMS = ('ādi', 'ādiḥ', 'ādim', 'ādau', 'ādyāḥ', 'ādyāś', 'ādayaḥ',
             'ādīni', 'ādibhiḥ', 'ādyaiḥ', 'ādikam', 'ādye')
KRAMA = {'kramāt', 'krameṇa', 'kramaśaḥ', 'kramam'}


def classify(w):
    if w in INDECL:
        return 'particle'
    if w in PRON:
        return 'pronoun'
    if w in VERB_NARR or w.endswith('tvā') or w.endswith('vīt'):
        return 'verb_narrative'
    if ((w.endswith('et') and len(w) >= 4 and w not in ('cet', 'ced'))
            or w.endswith('yāt') or w.endswith('eyuḥ') or w == 'syāt'):
        return 'verb_prescriptive'
    if (w.startswith(NUM_STEMS) or w in KRAMA or w in ADI_FORMS
            or w.endswith(ADI_FORMS[:1] + ADI_FORMS[4:])):
        return 'numeral_list'
    return 'content'


CLASSES = ['particle', 'pronoun', 'verb_narrative', 'verb_prescriptive',
           'numeral_list', 'content']

# ── W1 side: classify the 500 words, decompose the loading mass ─────────────
w1 = list(csv.DictReader(open(HERE / 'loadings_W1_500.tsv', encoding='utf-8'),
                         delimiter='\t'))
w1_share = Counter()
w1_rate = Counter()
with open(HERE / 'w1_class_assignments.tsv', 'w', encoding='utf-8') as f:
    f.write('feature\tclass\trho_x\n')
    for r in w1:
        cl = classify(r['feature'])
        w1_share[cl] += abs(float(r['rho_x']))
        w1_rate[cl] += float(r['mean_permille'])
        f.write(f"{r['feature']}\t{cl}\t{r['rho_x']}\n")
tot_w1 = sum(w1_share.values())
tot_w1r = sum(w1_rate.values())

# ── C3 side: attribute every top-500 trigram token to a source word ─────────
c3 = {r['feature']: abs(float(r['rho_x'])) for r in
      csv.DictReader(open(HERE / 'loadings_C3_500.tsv', encoding='utf-8'),
                     delimiter='\t')}
TOP = set(c3)
top_show = sorted(c3, key=c3.get, reverse=True)[:40]

manifest = {l.strip().removesuffix('.txt') for l in
            MANIFEST.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}

cls_counts = {g: Counter() for g in TOP}       # class of source word
pos_counts = {g: Counter() for g in TOP}       # position type
src_examples = {g: Counter() for g in top_show}
word_class_cache = {}

for p in sorted(SANDHIED.glob('*.txt')):
    if p.stem not in manifest:
        continue
    for line in p.read_text(encoding='utf-8').lower().splitlines():
        toks = line.split()
        if not toks:
            continue
        stream = ''.join(toks)
        ids = []
        for wi, t in enumerate(toks):
            ids.extend([wi] * len(t))
        n = len(stream)
        for i in range(n - 2):
            g = stream[i:i + 3]
            if g not in TOP:
                continue
            a, b, c = ids[i], ids[i + 1], ids[i + 2]
            if a == c:                       # all inside one word
                w = toks[a]
                start = i == 0 or ids[i - 1] != a
                end = i + 3 == n or ids[i + 3] != a
                pos = ('whole' if start and end else 'initial' if start
                       else 'final' if end else 'interior')
                src = w
            else:                            # spans a junction
                pos = 'junction'
                dom = b if (a == b or b == c) else b   # majority owner
                src = toks[dom]
            cl = word_class_cache.get(src)
            if cl is None:
                cl = classify(src)
                word_class_cache[src] = cl
            cls_counts[g][cl] += 1
            pos_counts[g][pos] += 1
            if g in src_examples:
                src_examples[g][src] += 1

# ── decomposition ────────────────────────────────────────────────────────────
c3_share = Counter()
c3_token = Counter()
pos_share = Counter()
pos_token = Counter()
for g in TOP:
    tot = sum(cls_counts[g].values())
    if tot == 0:
        continue
    for cl, k in cls_counts[g].items():
        c3_share[cl] += c3[g] * k / tot
        c3_token[cl] += k
    for ps, k in pos_counts[g].items():
        pos_share[ps] += c3[g] * k / sum(pos_counts[g].values())
        pos_token[ps] += k
tot_c3 = sum(c3_share.values())
tot_c3t = sum(c3_token.values())
tot_ps = sum(pos_share.values())
tot_pst = sum(pos_token.values())

print('axis-signal share by word class (|rho_x|-weighted) vs token share:')
print(f'{"class":<20} {"W1 signal":>10} {"W1 rate":>9} {"C3 signal":>10} {"C3 tokens":>10}')
rows = []
for cl in CLASSES:
    rows.append((cl, w1_share[cl] / tot_w1, w1_rate[cl] / tot_w1r,
                 c3_share[cl] / tot_c3, c3_token[cl] / tot_c3t))
    print(f'{cl:<20} {rows[-1][1]:>9.1%} {rows[-1][2]:>8.1%} '
          f'{rows[-1][3]:>9.1%} {rows[-1][4]:>9.1%}')

print('\nC3 axis-signal share by trigram position vs token share:')
for ps in ['final', 'junction', 'initial', 'interior', 'whole']:
    print(f'{ps:<10} signal {pos_share[ps]/tot_ps:>6.1%}   tokens {pos_token[ps]/tot_pst:>6.1%}')

with open(HERE / 'class_signal_shares.tsv', 'w', encoding='utf-8') as f:
    f.write('class\tw1_signal_share\tw1_rate_share\tc3_signal_share\tc3_token_share\n')
    for cl, a, b, c_, d in rows:
        f.write(f'{cl}\t{a:.4f}\t{b:.4f}\t{c_:.4f}\t{d:.4f}\n')

with open(HERE / 'c3_trigram_sources.tsv', 'w', encoding='utf-8') as f:
    f.write('trigram\tabs_rho_x\tjunction_share\tfinal_share\t' +
            '\t'.join(f'{cl}_share' for cl in CLASSES) + '\n')
    for g in sorted(TOP, key=c3.get, reverse=True):
        tot = sum(cls_counts[g].values()) or 1
        pt = sum(pos_counts[g].values()) or 1
        f.write(f'{g}\t{c3[g]:.4f}\t{pos_counts[g]["junction"]/pt:.3f}\t'
                f'{pos_counts[g]["final"]/pt:.3f}\t' +
                '\t'.join(f'{cls_counts[g][cl]/tot:.3f}' for cl in CLASSES) + '\n')

print('\ntop-loading trigrams and their dominant sources:')
for g in top_show[:15]:
    ex = ', '.join(f'{w}({k})' for w, k in src_examples[g].most_common(3))
    print(f'  {g!r:<8} |rho| {c3[g]:.2f}   {ex}')
print('\nwrote class_signal_shares.tsv, c3_trigram_sources.tsv, w1_class_assignments.tsv')
