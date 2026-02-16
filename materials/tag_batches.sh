#!/usr/bin/env bash
set -euo pipefail

BATCH_SIZE=95

API_URL="https://dharmamitra.org/api-tagging/tagging-parsed/"

# Requirements: curl, jq
command -v curl >/dev/null 2>&1 || { echo "ERROR: curl not found" >&2; exit 1; }
command -v jq   >/dev/null 2>&1 || { echo "ERROR: jq not found (install jq)" >&2; exit 1; }

# We'll collect each batch's JSON response as an element in a JSON array.
# If you prefer "concatenated lines" instead of an array of responses, say so.
tmp_out="$(mktemp)"
trap 'rm -f "$tmp_out"' EXIT
: > "$tmp_out"

# Read input in batches of BATCH_SIZE lines.
# Using bash array to hold the lines.
batch=()
flush_batch() {
  local n="${#batch[@]}"
  [[ "$n" -eq 0 ]] && return 0

  # Build request JSON with jq:
  # texts: [ "line1", "line2", ... ]
  local payload
  payload="$(jq -n \
    --argjson texts "$(printf '%s\n' "${batch[@]}" | jq -R -s 'split("\n")[:-1]')" \
    '{
      texts: $texts,
      mode: "unsandhied",
      human_readable_tags: true,
      grammar_type: "western"
    }'
  )"

  # Call API
  # -sS for quiet but show errors; you can add --retry if you want.
  local resp
  resp="$(curl -sS -X POST "$API_URL" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    --data "$payload"
  )"

  # Append response JSON as one line to temp file (one JSON value per line)
  printf '%s\n' "$resp" >> "$tmp_out"

  # Reset batch
  batch=()
}

# Read stdin line-by-line, preserving UTF-8.
# Skip empty lines (optional); remove the condition if you want to send empties.
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" ]] && continue
  batch+=("$line")
  if [[ "${#batch[@]}" -ge "$BATCH_SIZE" ]]; then
    flush_batch
  fi
done

# Flush any remaining lines
flush_batch

# Combine all batch responses into a single JSON array and print once.
# If any response is not valid JSON, jq will fail loudly (good for catching errors).
jq -s '.' "$tmp_out"