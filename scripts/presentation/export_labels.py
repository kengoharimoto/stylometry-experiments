#!/usr/bin/env python3
"""Export point codes + display names + strata as JSON for the deck builder.

The code()/display() functions are copied verbatim from hero_mds.py (which is
a script, not importable); keep them in sync if the hero figure's labels
change. Output: materials/presentation_2026/corpus_labels.json
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRATA = ROOT / 'materials/presentation_2026/chronology_strata.tsv'
OUT = ROOT / 'materials/presentation_2026/corpus_labels.json'

CODES = {
    'brahmandapurana': 'Bḍ', 'brahmandapurana_khanda-1_u': 'Bḍ1',
    'brahmandapurana_khanda-2_u': 'Bḍ2', 'brahmandapurana_khanda-3_u': 'Bḍ3',
    'markandeyapurana_adhyaya-1-93_u': 'Mā',
    'matsyapurana_adhyaya-1-32_pu': 'Mt1', 'matsyapurana_adhyaya-176_pu': 'Mt2',
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
    'bhavisyapurana_brahmaparvan_adhyaya-5': 'Bhv5',
    'devibhagavatapurana': 'DB', 'devibhagavatapurana_u': 'DBu',
    'garudapurana_khanda-1_u': 'G1', 'garudapurana_khanda-2_u': 'G2',
    'garudapurana_khanda-3_u': 'G3',
    'kalikapurana': 'Kā', 'karatoyamahatmya_pu': 'Kt',
    'naradapurana_khanda-1_u': 'N1', 'naradapurana_khanda-2_u': 'N2',
    'padmapurana_a': 'Pd', 'saurapurana': 'Sau',
    'skandamahpurana_kasikhanda': 'Kś', 'skandapurana_himavatkhanda_au': 'Hm',
    'skandapurana_revakhanda': 'Rv', 'vayupurana_revakhanda': 'RvV',
    'sutasamhita_khanda-4_iast': 'Sū',
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
        'skandapurana_revakhanda': 'Revākh. (SkMP)',
        'skandamahpurana_kasikhanda': 'Kāśīkh. (SkMP)',
        'skandapurana_himavatkhanda_au': 'Himavatkh. (SkMP)',
        'skandapurana': 'SP (old)', 'skandapurana_adhyaya-1-31_pu': 'SP (old) 1–31',
        'skandapurana_pasupata_adhyaya174-183_u': 'SP (old) Pāśupata',
        'markandeyapurana_adhyaya-1-93_u': 'Mārkaṇḍeya 1–93',
        'matsyapurana_adhyaya-1-32_pu': 'Matsya 1–32',
        'matsyapurana_adhyaya-176_pu': 'Matsya 176',
        'bhavisyapurana_brahmaparvan_adhyaya-5': 'Bhaviṣya (adh. 5)',
        'devibhagavatapurana_u': 'DevīBhP (u)', 'devibhagavatapurana': 'DevīBhP',
        'visnudharmottarapurana_khanda-3_adhyaya-343-353_pu': 'ViDhUt (exc.)',
        'visnudharma_pu': 'Viṣṇudharma',
        'vamanapurana_saromahatmya_u': 'Saromāhātmya',
        'sutasamhita_khanda-4_iast': 'Sūtasaṃhitā 4',
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


rows = []
with open(STRATA, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        rows.append({'text': row['text'], 'stratum': int(row['stratum']),
                     'label': row['label'], 'code': code(row['text']),
                     'display': display(row['text'])})
OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'wrote {OUT} ({len(rows)} texts)')
