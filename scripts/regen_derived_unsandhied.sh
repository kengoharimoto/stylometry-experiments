#!/usr/bin/env bash
# Regenerate the derived single-line unsandhied corpora after the colophon
# cleanup (2026-08-16). The ByT5 input filter now drops colophon lines
# itself; inputs are the already-stripped source/sandhied-level variants.
# Run AFTER the base epic_puranas_unsandhied regeneration completes.
set -euo pipefail
cd "$(dirname "$0")/.."
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-1}"

run () {  # run <input_dir> <output_dir> <changed-list-file>
  local in="$1" out="$2" list="$3"
  echo "=== $in -> $out ($(wc -l < "$list") files)"
  while read -r f; do rm -f "$out/$f"; done < "$list"
  EPIC_INPUT_DIR="$PWD/$in" EPIC_OUTPUT_DIR="$PWD/$out" \
    scripts/unsandhi_local.sh
}

# changed-file lists were computed from the strip commit (0b666a9)
run corpus/epic_puranas_noreuse corpus/epic_puranas_unsandhied_noreuse \
    /tmp/claude-1003/-mnt-kengo-stylometry-experiments/8356a08a-7247-46ba-9375-28d37afc5c42/scratchpad/changed_noreuse.txt
run corpus/complements_src corpus/complements_unsandhied \
    /tmp/claude-1003/-mnt-kengo-stylometry-experiments/8356a08a-7247-46ba-9375-28d37afc5c42/scratchpad/changed_complements.txt
run corpus/genre_control_src corpus/genre_control_unsandhied \
    /tmp/claude-1003/-mnt-kengo-stylometry-experiments/8356a08a-7247-46ba-9375-28d37afc5c42/scratchpad/changed_genre.txt
echo "ALL DERIVED REGENERATION DONE"
