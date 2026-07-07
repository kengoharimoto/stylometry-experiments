#!/usr/bin/env bash
#
# Multi-GPU launcher for process_epic_puranas_unsandhied_local.py
#
# Runs one worker process per GPU, each handling a disjoint, size-balanced shard
# of the corpus (see select_shard() in the worker). All processes share the same
# output directory and are individually resumable.
#
# Usage:
#   scripts/unsandhi_local_multi.sh [GPUS] [extra worker args...]
#     GPUS  comma-separated physical GPU ids (default "0,1")
#   e.g.  scripts/unsandhi_local_multi.sh 0,1 --force
#         scripts/unsandhi_local_multi.sh 1            # single GPU, id 1
#
# int8 GEMM on Blackwell needs the CUDA 12.9 cuBLAS preloaded (see unsandhi_local.sh).
set -uo pipefail

GPUS="${1:-0,1}"
shift || true               # remaining args forwarded to every worker (e.g. --force)
IFS=',' read -ra GA <<< "$GPUS"
N=${#GA[@]}

BYT5=/mnt/code/byt5-analyzer
VENV="$BYT5/.venv-ct2"
CUBLAS_LIB="$VENV/lib/python3.13/site-packages/nvidia/cublas/lib"
export LD_PRELOAD="${LD_PRELOAD:+$LD_PRELOAD:}$CUBLAS_LIB/libcublasLt.so.12:$CUBLAS_LIB/libcublas.so.12"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKER="$SCRIPT_DIR/process_epic_puranas_unsandhied_local.py"
LOGDIR="$SCRIPT_DIR/../logs/unsandhi"
mkdir -p "$LOGDIR"

echo "Launching $N shard(s) across GPU(s): $GPUS   extra args: $*"
pids=()
for i in "${!GA[@]}"; do
  gpu="${GA[$i]}"
  log="$LOGDIR/shard${i}.gpu${gpu}.log"
  CUDA_VISIBLE_DEVICES="$gpu" "$VENV/bin/python" "$WORKER" \
      --shard "$i" --num-shards "$N" "$@" > "$log" 2>&1 &
  pids+=($!)
  echo "  shard $i -> GPU $gpu  (pid $!, log $log)"
done

fail=0
for p in "${pids[@]}"; do
  wait "$p" || { echo "shard pid $p exited non-zero"; fail=1; }
done
echo "All shards finished (fail=$fail)."
exit $fail
