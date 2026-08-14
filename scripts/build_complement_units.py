#!/usr/bin/env python3
"""Build the complement ("shared") halves of selected units: the material the
noreuse build removed, as standalone unit files.

For each target unit this writes corpus/complements_sandhied/<unit>_shared.txt
(lines of the sandhied original whose cstream is absent from the sandhied
noreuse file — exactly the lines build_noreuse_corpus.py dropped) and
corpus/complements_src/<unit>_shared.txt (the corresponding raw source lines,
recovered by walking the source against the kept file, which is a verbatim
subsequence). The unique residues need no build: they ARE the noreuse files.

W1-level complements are then produced by the unsandhi pipeline:
  EPIC_INPUT_DIR=corpus/complements_src EPIC_OUTPUT_DIR=corpus/complements_unsandhied \
      CUDA_VISIBLE_DEVICES=1 scripts/unsandhi_local.sh

Downstream: materials/presentation_2026/figures/complement_halves/project_halves.py
places both halves in the fixed sweet-spot MDS maps.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KEEP = set("abcdefghijklmnopqrstuvwxyzāīūṛṝḷḹṃḥśṣṇṭḍṅñ'")
def cstream(s):
    return ''.join(c for c in s.lower() if c in KEEP).replace("'", '')

UNITS = ([f'vayupurana_{s}_iast' for s in
          ['01_frame-and-cosmogony', '02_pashupata-yoga', '03_kalpas-and-shiva-lineages',
           '04_bhuvana-vinyasa', '05_jyotis-and-purvardha-close',
           '06_prthu-and-prajapati-lineages', '07_shraddha-kalpa',
           '08_manu-candra-vishnu-vamsha', '09_upasamhara', '10_gaya-mahatmya']]
         + ['vayupurana_revakhanda']
         + [f'brahmandapurana_khanda-{k}_u' for k in '123']
         + [f'visnupurana_amsa-{a}_u' for a in '123456'])

SAN = ROOT / 'corpus/epic_puranas_sandhied'
SAN_NR = ROOT / 'corpus/epic_puranas_sandhied_noreuse'
OUT_SAN = ROOT / 'corpus/complements_sandhied'
SRC = ROOT / 'corpus/epic_puranas'
SRC_NR = ROOT / 'corpus/epic_puranas_noreuse'
OUT_SRC = ROOT / 'corpus/complements_src'

def main():
    OUT_SAN.mkdir(exist_ok=True)
    OUT_SRC.mkdir(exist_ok=True)
    print(f'{"unit":<48}{"san shared":>11}{"san resid":>10}{"src shared":>11}')
    for u in UNITS:
        src = (SAN / f'{u}.txt').read_text(encoding='utf-8').splitlines()
        kset = {cstream(l) for l in
                (SAN_NR / f'{u}.txt').read_text(encoding='utf-8').splitlines()}
        comp = [l for l in src if cstream(l) not in kset]
        (OUT_SAN / f'{u}_shared.txt').write_text('\n'.join(comp) + '\n',
                                                 encoding='utf-8')
        ws = sum(len(l.split()) for l in comp)
        wr = sum(len(l.split()) for l in src) - ws

        rsrc = (SRC / f'{u}.txt').read_text(encoding='utf-8').splitlines()
        rkept = (SRC_NR / f'{u}.txt').read_text(encoding='utf-8').splitlines()
        scomp, j = [], 0
        for l in rsrc:
            if j < len(rkept) and l == rkept[j]:
                j += 1
            else:
                scomp.append(l)
        assert j == len(rkept), f'{u}: kept not a subsequence of source'
        (OUT_SRC / f'{u}_shared.txt').write_text('\n'.join(scomp) + '\n',
                                                 encoding='utf-8')
        print(f'{u:<48}{ws:>11}{wr:>10}{sum(len(l.split()) for l in scomp):>11}')

if __name__ == '__main__':
    main()
