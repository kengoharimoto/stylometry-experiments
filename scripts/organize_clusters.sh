#!/usr/bin/env bash

set -euo pipefail

# List of target directory names
metrics=(
  argamon
  canberra
  cosine
  delta
  eder
  euclidean
  manhattan
  minmax
  simple
  wurzburg
)

# Create directories if they don't exist
for metric in "${metrics[@]}"; do
  mkdir -p "$metric"
done

# Move matching files
for metric in "${metrics[@]}"; do
  for file in clusters*"${metric}"*; do
    # Check that the glob actually matched a file
    if [[ -e "$file" ]]; then
      mv "$file" "$metric"/
    fi
  done
done