"""Resume-guard for the multi-agent variants (division, div+neg, passive).

Problem: an agent's claude process can exit before the team's final answer
exists — either killed by a transient API error surfaced as a final message,
or by the model ending its turn with plain text (no tool call), which
`claude -p` treats as conversation over. In a multi-agent session nothing restarts
the process, so the agent is permanently gone; when it is agent-1 (the
assembler) the whole task is doomed.

Fix: rewrite the startup script's launch line into a guarded loop — after
claude exits, if /logs/agent/answer.txt does not exist yet, relaunch with
`--continue` (resumes the same session: each agent runs in its own
INSTANCE_DIR cwd, so --continue picks up exactly its own conversation) and a
prompt telling it to carry on with the protocol. The loop is uncapped and
runs until the answer exists; the harness-level task timeout bounds it.

The startup scripts on disk are NOT modified; the adapters transform the text
at install() time and upload the guarded version over the container path.
"""

from pathlib import Path

LAUNCH_LINE = (
    'exec claude --verbose --output-format=stream-json '
    '--permission-mode=bypassPermissions --effort high --print -- "$PROMPT" '
    '2>&1 </dev/null | tee "$LOG_FILE"'
)

GUARD_BLOCK = r'''# --- resume-guard: relaunch claude if it exits before the team answer exists ---
ANSWER_FILE=/logs/agent/answer.txt
RESUME_GUARD_PROMPT='Your session was resumed because your process exited before the team final answer was written to /logs/agent/answer.txt (it still does not exist). Continue your role in the multi-agent protocol from where you left off: re-check the shared state / messages as your instructions describe, actually SEND anything you drafted but never sent, respond to pending items, and keep participating until the final answer file exists. If you are agent-1 (the assembler), finish the remaining phases and write the final answer to /logs/agent/answer.txt exactly as originally instructed.'
claude --verbose --output-format=stream-json --permission-mode=bypassPermissions --effort high --print -- "$PROMPT" 2>&1 </dev/null | tee "$LOG_FILE"
RELAUNCH=0
while [ ! -f "$ANSWER_FILE" ]; do
  RELAUNCH=$((RELAUNCH+1))
  echo ">>> [resume-guard] claude exited but no team answer yet - relaunch #$RELAUNCH" >> "$LOG_FILE"
  sleep 15
  claude --verbose --output-format=stream-json --permission-mode=bypassPermissions --effort high --continue --print -- "$RESUME_GUARD_PROMPT" 2>&1 </dev/null | tee -a "$LOG_FILE"
done
echo ">>> [resume-guard] exiting (answer_exists=$([ -f "$ANSWER_FILE" ] && echo yes || echo no), relaunches=$RELAUNCH)" >> "$LOG_FILE"'''


def make_guarded_startup(original_text: str) -> str:
    """Replace the single exec-claude launch line with the guarded loop."""
    if LAUNCH_LINE not in original_text:
        raise ValueError(
            "resume-guard: expected claude launch line not found in startup "
            "script — the original script changed; update LAUNCH_LINE."
        )
    return original_text.replace(LAUNCH_LINE, GUARD_BLOCK)


async def upload_guarded_startup(agent, environment, local_script: Path, container_path: str) -> None:
    """Transform local_script and upload it over container_path (chmod +x)."""
    import tempfile

    guarded = make_guarded_startup(local_script.read_text())
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as f:
        f.write(guarded)
        tmp = f.name
    await environment.upload_file(tmp, container_path)
    await agent.exec_as_agent(environment, command=f"chmod +x {container_path}")
