#!/bin/bash
set -euo pipefail

# Load credentials
set -a
source "$(dirname "$0")/../../.env"
set +a

harbor run \
  -p ./data/qa \
  -a claude-code \
  -m "anthropic/claude-opus-4-6" \
  -e modal \
  -k 1 \
  -n 4 \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "full_124_opus46"
