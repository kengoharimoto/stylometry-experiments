#!/bin/bash

jq -r '
  .[][]
  | .grammatical_analysis
  | map(.unsandhied)
  | join(" ")
' 