#!/bin/bash
set -euo pipefail

# Passive-awareness multi-agent QA runner.
# Usage:
#   bash run_config/qa/run_passive_multi_agent.sh <task-id> [<task-id> ...]
# Each task id is submitted as its own harbor job (same pattern as pilot_multi_agent.sh),
# with results under results/qa/ and job names <prefix>-<short-id>.
# Override the job-name prefix (e.g. for prompt-revision batches) via:
#   PASSIVE_JOB_PREFIX=passive2-multi-agent bash run_config/qa/run_passive_multi_agent.sh ...
PREFIX="${PASSIVE_JOB_PREFIX:-passive-multi-agent}"

# Load credentials
set -a
source "$(dirname "$0")/../../.env"
set +a

# Add multi-agent module to Python path
export PYTHONPATH="$(dirname "$0")/../../:${PYTHONPATH:-}"

if [ $# -lt 1 ]; then
  echo "Usage: bash run_config/qa/run_passive_multi_agent.sh <task-id> [<task-id> ...]"
  echo ""
  echo "Example (smoke test):"
  echo "  bash run_config/qa/run_passive_multi_agent.sh task-6905333b74f22949d97ba998"
  exit 1
fi

for TASK_ID in "$@"; do
  echo ">>> Submitting $TASK_ID (passive awareness variant)"
  harbor run \
    --yes \
    -p ./data/qa \
    --agent-import-path='multi_agent.coral_multi_agent_passive:CoralMultiAgentPassive' \
    -m "anthropic/claude-opus-4-6" \
    -e modal \
    -k 1 \
    -n 1 \
    -i "$TASK_ID" \
    --ak reasoning_effort=high \
    -o results/qa/ \
    --job-name "${PREFIX}-${TASK_ID##*d97}"
done
