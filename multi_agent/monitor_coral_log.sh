#!/bin/bash
set -uo pipefail

# Live-monitor the coral session state from running modal containers.
# Every interval, executes agent-1's read_resource.sh INSIDE each container to read
# coral://state (server in-memory state: all threads + messages, REAL-TIME — unlike
# coral-server.log which is JVM-buffered and lags), overwriting the local copy
# atomically each time.
#
# Usage:
#   bash multi_agent/monitor_coral_log.sh [out-dir=/tmp/coral-monitor] [interval-sec=60]
#
# Output files: <out-dir>/coral-state.<container-id>.txt  (one per container)
# Stop with Ctrl-C. Containers without a coral workspace are skipped silently.

OUT="${1:-/tmp/coral-monitor}"
INTERVAL="${2:-60}"
# NOTE: `modal container exec` caps stdout at ~88KB per invocation, sometimes returns
# empty output spuriously, and appends a newline when output lacks one. So we snapshot
# the state to a file inside the container, then fetch it back in base64 chunks
# (newline-safe) with per-chunk retries, and decode locally.
REMOTE_SNAPSHOT='bash /tmp/coral-workspace/swe-atlas-agent/instances/*/agent-1/scripts/read_resource.sh > /tmp/coral-state-pull.txt 2>/dev/null; wc -c < /tmp/coral-state-pull.txt'
CHUNK=49152   # raw bytes per chunk; base64 expands ~4/3 → ~64KB, under the 88KB cap

exec_retry() {  # exec_retry <cid> <cmd> — retries empty outputs (modal exec drops stdout randomly)
  local cid="$1" cmd="$2" out try
  for try in 1 2 3 4 5 6 7 8; do
    out=$(modal container exec "$cid" -- bash -c "$cmd" 2>/dev/null)
    if [ -n "$out" ]; then printf '%s\n' "$out"; return 0; fi
    sleep 3
  done
  return 1
}

fetch_chunk() {  # fetch_chunk <cid> <offset> <expected-raw-bytes> <dst> — decode-verified, appends
  local cid="$1" off="$2" want="$3" dst="$4" try b64
  for try in 1 2 3 4 5 6 7 8; do
    b64=$(modal container exec "$cid" -- bash -c \
      "tail -c +$((off + 1)) /tmp/coral-state-pull.txt | head -c $CHUNK | base64" 2>/dev/null)
    if [ -n "$b64" ] && printf '%s' "$b64" | python3 -c "
import base64, sys
d = base64.b64decode(sys.stdin.read())
assert len(d) == $want, f'{len(d)} != $want'
sys.stdout.buffer.write(d)
" >> "$dst" 2>/dev/null; then
      return 0
    fi
    sleep 3
  done
  return 1
}

mkdir -p "$OUT"
echo ">>> Monitoring coral://state (real-time) from modal containers every ${INTERVAL}s"
echo ">>> Local copies: $OUT/coral-state.<container-id>.txt  (overwritten each pull)"

while true; do
  CIDS=$(modal container list --json 2>/dev/null \
    | python3 -c '
import json, sys
try:
    rows = json.load(sys.stdin)
except Exception:
    sys.exit(0)
for r in rows:
    cid = r.get("Container ID") or r.get("container_id") or r.get("id") or ""
    if cid:
        print(cid)
')
  if [ -z "$CIDS" ]; then
    echo "[$(date +%H:%M:%S)] no running containers"
  fi
  for cid in $CIDS; do
    SIZE=$(exec_retry "$cid" "$REMOTE_SNAPSHOT" | tr -d ' \r\n')
    if [ -z "$SIZE" ] || ! [ "$SIZE" -gt 0 ] 2>/dev/null; then
      echo "[$(date +%H:%M:%S)] $cid: no coral state (skipped)"
      continue
    fi
    TMP="$OUT/coral-state.$cid.txt.tmp"
    : > "$TMP"
    OFFSET=0; FAIL=0
    while [ "$OFFSET" -lt "$SIZE" ]; do
      WANT=$((SIZE - OFFSET)); [ "$WANT" -gt "$CHUNK" ] && WANT=$CHUNK
      if ! fetch_chunk "$cid" "$OFFSET" "$WANT" "$TMP"; then
        FAIL=1; break
      fi
      OFFSET=$((OFFSET + CHUNK))
    done
    if [ "$FAIL" -eq 0 ]; then
      mv "$TMP" "$OUT/coral-state.$cid.txt"
      python3 "$(dirname "$0")/format_coral_state.py" "$OUT/coral-state.$cid.txt" >/dev/null 2>&1 || true
      n=$(grep -o '"messageText"' "$OUT/coral-state.$cid.txt" | wc -l | tr -d ' ')
      echo "[$(date +%H:%M:%S)] pulled $cid (${SIZE}B, messages: $n)"
    else
      rm -f "$TMP"
      echo "[$(date +%H:%M:%S)] $cid: pull failed after retries, will retry next cycle"
    fi
  done
  sleep "$INTERVAL"
done
