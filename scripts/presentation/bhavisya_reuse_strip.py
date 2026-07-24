"""Slide 13b figure: the Bhaviṣyapurāṇa as a mosaic of datable borrowings.

One variable-width bar per chapter (width ∝ pāda-units, height = % of units
with a non-stock parallel in the 40_tools all-texts scan), coloured by the
dominant DONOR family. Dharmanibandhas (Hemādri, Kṛtyakalpataru, …) quote
*from* the Bhaviṣya, so they are excluded from donor selection; chapters
whose matches are nibandha-only get a hatched neutral ("cited, source
unknown"). Buddhist and Bṛhatsaṃhitā chapters are too narrow to read as
fills — they carry markers instead.

Data: E-texts/40_tools/reports/bhavisya_parallels/
  bhavisya_chapter_parallels.tsv  (per-chapter units / matched / pct)
  bhavisya_pairs.tsv              (unit-level pairs, incl. the Sāmba merge)
  stock_units.tsv                 (pan-corpus formulae, excluded)
Row "1.216" (4,487-unit colophon-less remainder, 16% matched) is left off
the strip and footnoted.
"""
import csv
import re
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

import figcommon as fc

REPORTS = Path.home() / 'Documents/E-texts/40_tools/reports/bhavisya_parallels'

# ── donor families (colours = dataviz reference categorical, validated) ──────
FAM_COLORS = {
    'manu':    ('#2a78d6', 'Manusmṛti & smṛtis'),
    'saura':   ('#eb6834', 'Sāmba–Brahmapurāṇa (saura)'),
    'sivadh':  ('#1baf7a', 'Śivadharma corpus'),
    'vrata':   ('#eda100', 'Matsya/Padma vrata–dāna'),
    'visnudh': ('#e87ba4', 'Viṣṇudharma'),
    'vayubd':  ('#008300', 'Vāyu–Brahmāṇḍa–Harivaṃśa'),
}
OTHER_C, NIB_C, TRACK_C = '#8a8a8a', '#c9c7ba', '#efeeea'

CITERS = re.compile(
    r'hemadri_|laksmidha_|balakrida|haribhaktivilasa|mahasubhasita|'
    r'purascaryaarnava|tarabhaktisudharnava|saktapramoda|navamimsimha|'
    r'jiva_|lakshiminarayanasamhita|merutantra|vedajnana|acintyavisvasada|'
    r'narasimhathakkura|saubhagyabhaskari')

BUDDHIST = re.compile(r'divya|sardula|manjusri|vajrasuci|kalpadruma|'
                      r'cittavisuddhi|avadana')
BRHS = re.compile(r'varahamihira')


def family(base):
    if BUDDHIST.search(base) or BRHS.search(base):
        return 'other'                      # marker-carried, not fill-carried
    if 'visnudharmottara' in base:
        return 'other'
    if 'brahmandapurana' in base or 'vayupurana' in base or 'harivamsa' in base:
        return 'vayubd'
    if 'sambapurana' in base or 'brahmapurana' in base:
        return 'saura'
    if 'sivadharma' in base or 'sivapurana_dharmasamhita' in base:
        return 'sivadh'
    if 'visnudharma' in base:
        return 'visnudh'
    if 'matsyapurana' in base or 'padmapurana' in base:
        return 'vrata'
    if ('manu_manusmrti' in base or 'yajnavalkya' in base
            or 'dharmasutra' in base):
        return 'manu'
    return 'other'


def chapter_key(ch):
    a, b = ch.split('.')
    return int(a), int(b)


# ── load ─────────────────────────────────────────────────────────────────────
chapters = {}                               # ch -> (units, matched, pct)
with open(REPORTS / 'bhavisya_chapter_parallels.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        chapters.setdefault(row['chapter'],
                            (int(row['units']), int(row['matched_nonstock']),
                             int(row['pct'])))

stock = set()
with open(REPORTS / 'stock_units.tsv') as f:
    next(f)
    stock = {line.split('\t', 1)[0] for line in f}

fam_units = defaultdict(lambda: defaultdict(set))   # ch -> fam -> unit ids
src_units = defaultdict(lambda: defaultdict(set))   # ch -> 'other' file -> ids
citer_units = defaultdict(set)
budd_units, brhs_units = defaultdict(set), defaultdict(set)
with open(REPORTS / 'bhavisya_pairs.tsv') as f:
    next(f)
    for line in f:
        uid, ch, _ratio, src, _rest = line.split('\t', 4)
        if uid in stock:
            continue
        base = src.rsplit('/', 1)[-1].lower()
        if CITERS.search(base):
            citer_units[ch].add(uid)
            continue
        if BUDDHIST.search(base):
            budd_units[ch].add(uid)
        if BRHS.search(base):
            brhs_units[ch].add(uid)
        fam = family(base)
        if fam == 'other':
            src_units[ch][base].add(uid)    # keep per-file: no pooling
        else:
            fam_units[ch][fam].add(uid)

def dominant(ch):
    """Named families pool their variant e-texts; 'other' competes only
    with its single best source file (pooling all misc texts would let
    grey win everywhere)."""
    counts = {f: len(u) for f, u in fam_units[ch].items()}
    if src_units[ch]:
        counts['other'] = max(len(u) for u in src_units[ch].values())
    if counts and max(counts.values()) >= 5:
        return max(counts, key=counts.get)
    if len(citer_units[ch]) >= 5:
        return 'nibandha'
    return 'other' if chapters[ch][2] > 0 else 'none'


# ── geometry ─────────────────────────────────────────────────────────────────
parvans = {'1': [], '4': []}
for ch in sorted((c for c in chapters if c != '1.216'), key=chapter_key):
    parvans[ch.split('.')[0]].append(ch)

fc.use_sf_pro()
fig, axes = plt.subplots(2, 1, figsize=(13.33, 7.5))
fig.subplots_adjust(left=0.055, right=0.985, top=0.80, bottom=0.10,
                    hspace=0.62)

positions = {}                              # ch -> (x0, w, ax index)
for axi, (pv, chs) in enumerate(parvans.items()):
    ax, x = axes[axi], 0.0
    for ch in chs:
        units, _m, pct = chapters[ch]
        fam = dominant(ch)
        positions[ch] = (x, units, axi)
        ax.bar(x, 100, width=units, align='edge', color=TRACK_C, lw=0)
        if fam == 'nibandha':
            ax.bar(x, pct, width=units, align='edge', color=NIB_C,
                   hatch='////', edgecolor='#9a988c', lw=0)
        elif fam != 'none':
            col = FAM_COLORS[fam][0] if fam in FAM_COLORS else OTHER_C
            ax.bar(x, pct, width=units, align='edge', color=col, lw=0)
        x += units
    total_u = sum(chapters[c][0] for c in chs)
    total_m = sum(chapters[c][1] for c in chs)
    name = 'Brāhmaparvan' if pv == '1' else 'Uttaraparvan'
    ax.set_title(f'{name} — {total_m/total_u:.0%} of {total_u:,} pāda-units '
                 f'found in other texts', loc='left', fontsize=12,
                 fontweight='bold', pad=6)
    ax.set_xlim(0, x)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 50, 100])
    ax.set_yticklabels(['0', '50', '100%'], fontsize=8, color='#666')
    ticks = [c for c in chs if chapter_key(c)[1] in (1, 50, 100, 150, 200)]
    ax.set_xticks([positions[c][0] + positions[c][1] / 2 for c in ticks])
    ax.set_xticklabels([c for c in ticks], fontsize=8, color='#666')
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(length=0)

# ── markers for the sliver donors ────────────────────────────────────────────
def mark(chs_units, sym, dy=4):
    """Mark a chapter only where the sliver donor carries real weight:
    ≥3 matched units AND ≥20% of the chapter's matched total."""
    out = []
    for ch, us in chs_units.items():
        n = len(us)
        if (n >= 3 and ch in positions
                and n >= 0.2 * max(chapters[ch][1], 1)):
            x0, w, axi = positions[ch]
            axes[axi].plot(x0 + w / 2, chapters[ch][2] + dy, sym,
                           color='#333333', ms=5, clip_on=False)
            out.append(ch)
    return sorted(out, key=chapter_key)

budd_marked = mark(budd_units, '^')
brhs_marked = mark(brhs_units, 'v')
print('Buddhist-marked:', budd_marked, ' BṛS-marked:', brhs_marked)

# ── callouts ─────────────────────────────────────────────────────────────────
def callout(axi, ch_a, ch_b, text, y=124):
    xa = positions[ch_a][0]
    xb = positions[ch_b][0] + positions[ch_b][1]
    ax = axes[axi]
    ax.annotate(text, ((xa + xb) / 2, y + 4), ha='center', fontsize=8.5,
                color='#333333', annotation_clip=False)
    ax.plot([xa, xb], [y, y], color='#999999', lw=0.8, clip_on=False)
    for xx in (xa, xb):
        ax.plot([xx, xx], [y - 4, y], color='#999999', lw=0.8, clip_on=False)

callout(0, '1.1', '1.7', 'Manusmṛti 1–3')
callout(0, '1.8', '1.15', 'no match\n(own text)')
callout(0, '1.24', '1.42', 'physiognomy · magic\n(»ŚKA · MMK · Vajrasūcī)')
callout(0, '1.52', '1.80', 'saura corpus\n(Sāmba · Brahmapur.)')
callout(0, '1.121', '1.145', '2nd saura band')
callout(0, '1.162', '1.180', 'Śivadharmaśāstra')
callout(0, '1.187', '1.192', 'ŚDhU')
callout(1, '4.4', '4.6', 'Śivadharmottara')
callout(1, '4.25', '4.40', 'vrata blocks (Matsya/Padma;\nexcerpted by the nibandhas)')
callout(1, '4.195', '4.204', 'Matsya dāna\n(MatsP 83–92)')

# ── title & legend ───────────────────────────────────────────────────────────
tot_u = sum(u for c, (u, m, p) in chapters.items())
tot_m = sum(m for c, (u, m, p) in chapters.items())
fig.suptitle('The Bhaviṣyapurāṇa, pāda by pāda, against the whole e-text '
             'library', x=0.055, y=0.975, ha='left', fontsize=17,
             fontweight='bold')
fig.text(0.055, 0.935,
         f'{tot_m/tot_u:.0%} of {tot_u:,} pāda-units match another text '
         '(ratio ≥ 0.7, stock formulae excluded) — in dated, block-wise '
         'ingredients. Bar width = chapter length; colour = dominant source.',
         fontsize=10.5, color='#444444')

handles = [plt.Rectangle((0, 0), 1, 1, color=c)
           for c, _ in FAM_COLORS.values()]
labels = [n for _, n in FAM_COLORS.values()]
handles += [plt.Rectangle((0, 0), 1, 1, color=OTHER_C),
            plt.Rectangle((0, 0), 1, 1, color=NIB_C, hatch='////',
                          ec='#9a988c'),
            plt.Rectangle((0, 0), 1, 1, color=TRACK_C),
            plt.Line2D([], [], marker='^', color='#333333', ls='none', ms=5),
            plt.Line2D([], [], marker='v', color='#333333', ls='none', ms=5)]
labels += ['other source', 'nibandha citations only', 'no match (own text)',
           'Buddhist parallel', 'Bṛhatsaṃhitā']
fig.legend(handles, labels, loc='lower center', ncol=6, fontsize=8.5,
           frameon=False, bbox_to_anchor=(0.5, 0.0),
           handlelength=1.2, columnspacing=1.1)
fig.text(0.985, 0.975, 'not shown: a 4,487-unit colophon-less remainder '
         '(16% matched)\nnibandhas (Hemādri, Kṛtyakalpataru) quote FROM the '
         'Bhaviṣya\nand are not counted as sources',
         ha='right', va='top', fontsize=7.5, color='#888888')

out = fc.FIGDIR / 'bhavisya_reuse_strip'
fig.savefig(f'{out}.png', dpi=200)
fig.savefig(f'{out}.pdf')
print('wrote', out)

# sanity dump
for pv, chs in parvans.items():
    doms = defaultdict(int)
    for c in chs:
        doms[dominant(c)] += chapters[c][0]
    print(pv, dict(sorted(doms.items(), key=lambda kv: -kv[1])))
