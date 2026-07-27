#!/usr/bin/env python3
"""Pretty-print a raw coral://state dump (as saved by monitor_coral_log.sh).

Usage: python3 format_coral_state.py <raw-state-file>  (writes <raw>.pretty.txt)

Renders each thread as a readable conversation:
  ═══ thread name (participants) ═══
  [HH:MM:SS] sender -> @mentions:
      message text (original line breaks preserved, indented)
"""
import json
import re
import sys


def main(path):
    raw = open(path, errors="ignore").read()

    out = []

    # session time (first line of # General)
    m = re.search(r"ISO-8601: ([0-9T:.\-]+Z?)", raw)
    if m:
        out.append(f"state pulled at (session clock): {m.group(1)}")

    # agents block
    m = re.search(r"# Agents.*?```json\n(.*?)\n```", raw, re.S)
    if m:
        try:
            agents = json.loads(m.group(1))
            out.append("\nAGENTS:")
            for a in agents:
                out.append(
                    f"  - {a.get('agentName')}  connected={a.get('agentConnected')}"
                    f"  waiting={a.get('agentWaitingForMention', a.get('waiting', '?'))}"
                )
        except Exception:
            pass

    # threads block: last ```json ... ``` under "# Threads and messages"
    m = re.search(r"# Threads and messages.*?```json\n(.*?)\n```", raw, re.S)
    if not m:
        out.append("\n(no threads section found)")
    else:
        try:
            threads = json.loads(m.group(1))
        except Exception as e:
            out.append(f"\n(threads JSON parse failed: {e})")
            threads = []
        # sort threads by first message timestamp so the reading order is chronological
        def first_ts(t):
            msgs = t.get("messages") or []
            return msgs[0].get("messageTimestamp", "") if msgs else "9999"
        for t in sorted(threads, key=first_ts):
            name = t.get("threadName", "?")
            parts = ",".join(t.get("participatingAgents", []))
            state = t.get("state", "?")
            msgs = t.get("messages") or []
            out.append("")
            out.append("═" * 100)
            out.append(f"THREAD: {name}   [owner={t.get('owningAgentName')}, {state}, {len(msgs)} msgs, participants: {parts}]")
            out.append("═" * 100)
            for msg in msgs:
                ts = (msg.get("messageTimestamp") or "")[11:19]
                sender = msg.get("sendingAgentName", "?")
                mentions = msg.get("mentionAgentNames") or []
                mtxt = (" -> @" + ",@".join(mentions)) if mentions else ""
                out.append(f"\n[{ts}] {sender}{mtxt}:")
                text = msg.get("messageText", "")
                for line in text.split("\n"):
                    out.append("    " + line)

    dst = re.sub(r"\.txt$", "", path) + ".pretty.txt"
    with open(dst, "w") as f:
        f.write("\n".join(out) + "\n")
    print(dst)


if __name__ == "__main__":
    main(sys.argv[1])
