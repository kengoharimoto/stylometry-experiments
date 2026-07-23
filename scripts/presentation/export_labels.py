#!/usr/bin/env python3
"""Export point codes + display names + strata as JSON for the deck builder.

Labels come from figcommon (shared with the figures), so they cannot drift.
Output: materials/presentation_2026/corpus_labels.json
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRATA = ROOT / 'materials/presentation_2026/chronology_strata.tsv'
OUT = ROOT / 'materials/presentation_2026/corpus_labels.json'

from figcommon import code, display  # noqa: E402

rows = []
with open(STRATA, encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        rows.append({'text': row['text'], 'stratum': int(row['stratum']),
                     'label': row['label'], 'code': code(row['text']),
                     'display': display(row['text'])})
OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'wrote {OUT} ({len(rows)} texts)')
