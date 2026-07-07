#!/usr/bin/env bash
#
# Launcher for process_epic_puranas_unsandhied_local.py
#
# Runs the int8 CTranslate2 ByT5-Sanskrit model locally (no network) to unsandhi
# corpus/epic_puranas/ into corpus/epic_puranas_unsandhied/.
#
# int8 GEMM on the RTX PRO 6000 (Blackwell / sm_120) fails with the cuBLAS that
# CTranslate2 4.8.1 loads by default (CUBLAS_STATUS_NOT_SUPPORTED). Preloading
# the CUDA 12.9 cuBLAS (installed into the venv) fixes it, so we LD_PRELOAD it
# here before Python starts.
#
# Usage:  scripts/unsandhi_local.sh
# Env overrides: CUDA_VISIBLE_DEVICES (default 0), CT2_BATCH_SIZE, etc.
set -euo pipefail

BYT5=/mnt/code/byt5-analyzer
VENV="$BYT5/.venv-ct2"
CUBLAS_LIB="$VENV/lib/python3.13/site-packages/nvidia/cublas/lib"

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "error: venv not found at $VENV" >&2
  exit 1
fi

export LD_PRELOAD="${LD_PRELOAD:+$LD_PRELOAD:}$CUBLAS_LIB/libcublasLt.so.12:$CUBLAS_LIB/libcublas.so.12"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$VENV/bin/python" "$SCRIPT_DIR/process_epic_puranas_unsandhied_local.py" "$@"
