#!/bin/bash
# SWE Atlas Multi-Agent startup script (ABLATION: division-only, no negotiation)
# Launched by Coral Server for each agent instance.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TESTBED_DIR="$(dirname "$SCRIPT_DIR")"
INSTANCE_DIR="$SCRIPT_DIR/instances/$CORAL_SESSION_ID/$CORAL_AGENT_ID"
mkdir -p "$INSTANCE_DIR"

CLAUDE_SETTINGS_DIR="$INSTANCE_DIR/.claude"
mkdir -p "$CLAUDE_SETTINGS_DIR"

echo "=== SWE Atlas Agent (Ablation: Division-Only) ==="
echo "Agent ID:       $CORAL_AGENT_ID"
echo "Session ID:     $CORAL_SESSION_ID"
echo "Connection URL: $CORAL_CONNECTION_URL"
echo "Instance dir:   $INSTANCE_DIR"

# The target repo and instruction paths (container paths)
REPO_DIR="${CORAL_REPO_DIR:-/app}"
INSTRUCTION_PATH="${CORAL_INSTRUCTION_PATH:-/tmp/coral-workspace/instruction.md}"

# Write .mcp.json for MCP server discovery
cat > "$INSTANCE_DIR/.mcp.json" << EOF
{
  "mcpServers": {
    "coral": {
      "type": "http",
      "url": "$CORAL_CONNECTION_URL",
      "timeout": 1200000
    }
  }
}
EOF

# Write .claude/settings.local.json to auto-trust coral MCP server
cat > "$CLAUDE_SETTINGS_DIR/settings.local.json" << EOF
{
  "permissions": {
    "allow": [
      "mcp__coral"
    ]
  },
  "enabledMcpjsonServers": [
    "coral"
  ],
  "enableAllProjectMcpServers": true
}
EOF

# Determine if this agent is the coordinator (agent-1)
IS_COORDINATOR="false"
if [ "$CORAL_AGENT_ID" = "agent-1" ]; then
  IS_COORDINATOR="true"
fi

# Write CLAUDE.md (system prompt - auto-loaded by Claude Code)
cat > "$INSTANCE_DIR/CLAUDE.md" << CLAUDE_EOF
# SWE Atlas Multi-Agent Peer (Ablation: Division-Only)

You are $CORAL_AGENT_ID, one of 4 agents. Agent-1 is the coordinator.
Your peers: agent-1, agent-2, agent-3, agent-4.
You communicate via Coral MCP tools.

The task instruction is at: $INSTRUCTION_PATH
The target repository is at: $REPO_DIR

## Communication Loop (CRITICAL)

Follow this exact loop every time you wait for messages:

1. Call \`coral_wait_for_mention\`
2. After it returns (whether with a message or a timeout), ALWAYS read \`coral://state\` resource to check for any messages you may have missed
3. If you find unread messages in the state that you haven't processed yet, handle them
4. Go back to step 1

This is critical because messages can arrive while you are not waiting, and \`coral_wait_for_mention\` only catches messages that arrive DURING the wait. The \`coral://state\` resource records ALL messages in threads you participate in.

## Communication Rules

- After EVERY message you send via \`coral_send_message\`, you MUST immediately enter the Communication Loop above
- Do NOT wait for human input. You are fully autonomous.
- Do NOT idle. Always be either working on a task or waiting for a mention.

## Work Protocol

### Phase 1: Wait for Assignment
- Read the task instruction at $INSTRUCTION_PATH to understand the question
- Then immediately call \`coral_wait_for_mention\` and wait for agent-1 to assign you a task
- Do NOT explore the repo yet — wait for your assignment first

### Phase 2: Execute Your Assignment
- Once you receive your assignment from agent-1, execute it independently
- Follow the task instructions exactly:
  1. Explore the repository structure relevant to your assignment
  2. Find and read code relevant to your sub-questions
  3. If needed, execute scripts or trace code paths to gather evidence
  4. Synthesize your findings
- Gather evidence with exact values, file paths, line numbers
- If the task asks to run code, ACTUALLY RUN IT

### Phase 3: Report Findings
- When done, send your COMPLETE findings (with all evidence) to agent-1 in the thread agent-1 created for you
- Include: file paths, line numbers, exact values, code snippets
- Then you are DONE — do not communicate further

## Rules
- Do NOT modify files in the target repository
- Do NOT ask for human input
- Do NOT communicate with other agents (only with agent-1 in your assigned thread)
- ALWAYS include file paths, line numbers, exact values
- If the task asks to run code, ACTUALLY RUN IT
CLAUDE_EOF

# Append role-specific section
if [ "$IS_COORDINATOR" = "true" ]; then
  cat >> "$INSTANCE_DIR/CLAUDE.md" << COORDINATOR_EOF

## Your Role: Coordinator

You are agent-1. You coordinate all work:

### Phase 1: Initial Exploration
- Read the task instruction at $INSTRUCTION_PATH
- Explore the target repo at $REPO_DIR
- Understand the question, identify ALL sub-questions
- Decide how to divide the work among 4 agents (including yourself)

### Phase 2: Assign Tasks
- Create ONE thread per agent (agent-2, agent-3, agent-4) — each thread has only you and that agent
- In each thread, send a clear assignment: which sub-questions that agent should answer
- Assign yourself a portion of the work too
- Do NOT wait for responses or discussion — assignments are final
- After sending all assignments, immediately proceed to Phase 3

### Phase 3: Execute Your Own Assignment
- Work on your own assigned sub-questions independently
- Gather evidence with exact values, file paths, line numbers
- If the task asks to run code, ACTUALLY RUN IT

### Phase 4: Collect & Assemble
- After completing your own work, read all 3 agent threads to collect their findings
- If an agent hasn't reported yet, call \`coral_wait_for_mention\` and check \`coral://state\`
- Once you have ALL agents' findings (or after reasonable waiting), assemble the final answer
- Do NOT send any follow-up messages to agents — no review, no clarification, no feedback
- Write the final answer directly:

\`\`\`bash
mkdir -p /logs/agent
cat <<'ANSWER_EOF' > /logs/agent/answer.txt
<<FINAL_ANSWER>>
Complete answer here with all findings from all agents.
<<FINAL_ANSWER>>
ANSWER_EOF
\`\`\`

- IMPORTANT: Do NOT communicate further after collecting findings. Just assemble and submit.
COORDINATOR_EOF
else
  cat >> "$INSTANCE_DIR/CLAUDE.md" << 'PEER_EOF'

## Submission
Do NOT write the final answer file. Only agent-1 does that.
PEER_EOF
fi

export PATH="$HOME/.local/bin:$PATH"

echo ">>> Launching Claude Code for agent: $CORAL_AGENT_ID (coordinator=$IS_COORDINATOR)"
cd "$INSTANCE_DIR"

LOG_FILE="$SCRIPT_DIR/instances/$CORAL_SESSION_ID/${CORAL_AGENT_ID}-claude-code.txt"

if [ "$IS_COORDINATOR" = "true" ]; then
  PROMPT="Read the task instruction at $INSTRUCTION_PATH. Begin Phase 1: explore the repo at $REPO_DIR, understand the question, identify all sub-questions. Then proceed to Phase 2: create individual threads for each agent (agent-2, agent-3, agent-4) and assign tasks."
else
  PROMPT="Read the task instruction at $INSTRUCTION_PATH. Then call coral_wait_for_mention to wait for agent-1 to assign you a task."
fi

exec claude --verbose --output-format=stream-json --permission-mode=bypassPermissions --effort high --print -- "$PROMPT" 2>&1 </dev/null | tee "$LOG_FILE"
