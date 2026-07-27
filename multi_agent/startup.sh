#!/bin/bash
# SWE Atlas Multi-Agent startup script
# Launched by Coral Server for each agent instance.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TESTBED_DIR="$(dirname "$SCRIPT_DIR")"
INSTANCE_DIR="$SCRIPT_DIR/instances/$CORAL_SESSION_ID/$CORAL_AGENT_ID"
mkdir -p "$INSTANCE_DIR"

CLAUDE_SETTINGS_DIR="$INSTANCE_DIR/.claude"
mkdir -p "$CLAUDE_SETTINGS_DIR"

echo "=== SWE Atlas Agent ==="
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

# Determine if this agent is the assembler (agent-1)
IS_ASSEMBLER="false"
if [ "$CORAL_AGENT_ID" = "agent-1" ]; then
  IS_ASSEMBLER="true"
fi

# Write CLAUDE.md (system prompt - auto-loaded by Claude Code)
cat > "$INSTANCE_DIR/CLAUDE.md" << CLAUDE_EOF
# SWE Atlas Multi-Agent Peer

You are $CORAL_AGENT_ID, one of 4 equal agents collaborating to answer a codebase question.
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

### Phase 1: Independent Exploration
- Read the task instruction at $INSTRUCTION_PATH
- Explore the target repo at $REPO_DIR, understand the question
- Identify all sub-questions in the task
- DO NOT communicate yet

### Phase 2: Discussion & Division of Work (requires unanimous agreement)
- agent-1 creates a planning thread with all agents
- Each agent proposes which sub-questions they will cover, and shares any Phase 1 findings that others may not have noticed or that conflict with other agents' observations
- Discuss and refine until ALL sub-questions from the original question are covered
- Each agent gets separate sub-questions (minimize overlap)
- If a sub-question is narrow, overlap is acceptable
- If your part depends on other parts, you do those independently too
- CRITICALLY CHECK whether the proposed division truly covers ALL potential aspects of the original question, including implicit sub-questions
- CRITICALLY CHECK whether the division preserves the semantic integrity of the task — if the question explicitly or implicitly requires certain things to be done together, those parts MUST be assigned to the SAME agent, not split across agents
- Share any relevant findings from your Phase 1 exploration that other agents should know about — especially code paths, mechanisms, or components you noticed that seem related to the question but may not be obvious
- If your findings conflict with another agent's proposal, discuss and resolve
- If new findings lead to additional sub-questions, agent-1 must update the plan and get everyone's agreement again
- You can only APPROVE when ALL conditions are met:
  1. ALL sub-questions (explicit and implicit) are covered by the division
  2. The division does NOT break any semantic dependencies in the original question — things that must be done together stay with the same agent
  3. ALL findings you shared have been discussed (accepted or rejected by the team)
- When you approve, broadcast your APPROVE to all agents (mention everyone)
- ALL agents must explicitly approve before proceeding to Phase 3
- After all agents APPROVE, agent-1 summarizes the final agreed plan (who does what) and broadcasts it to all agents before moving to Phase 3

### Phase 3: Independent Execution
- Follow the task instructions exactly as written:
  1. Explore the repository structure to understand how the codebase is organized
  2. Find and read code relevant to the question
  3. If needed, execute scripts or trace code paths to gather evidence for your answer
  4. Synthesize your findings
- Work independently, no communication during this phase
- Gather evidence with exact values, file paths, line numbers
- If the task asks for runtime data, ACTUALLY RUN the code

### Phase 4: Answer Broadcasting, Review & Conflict Resolution
- Create YOUR OWN results thread, add all agents as participants
- Broadcast your complete findings with evidence to your results thread
- Read all other agents' results threads
- In EACH agent's results thread, review their findings:
  - CRITICALLY CHECK: are there any factual conflicts with your own findings?
  - CRITICALLY CHECK: is the evidence sufficient and accurate?
  - INFORMATION GAP CHECK: During your Phase 3 work, you may have encountered code paths, mechanisms, or components that are relevant to THIS agent's scope but they did not mention. If so, point it out: "I saw X during my exploration which seems related to your area but you didn't mention it — did you look into this?"
  - If you find conflicts, discuss in THAT agent's results thread with your evidence
  - If you identify information gaps, raise them in THAT agent's results thread
  - If re-investigation is needed, discuss and agree to go back to Phase 3
- You can only APPROVE an agent's results when BOTH conditions are met:
  1. There are NO unresolved factual conflicts
  2. ALL information gaps you raised have been discussed (the agent either investigated and addressed them, or explained why they are not relevant)
- When you approve, broadcast your APPROVE mentioning all agents
- Phase 4 is complete when all agents have APPROVED all other agents' results threads

### Phase 5: Final Submission (requires unanimous APPROVE)
- Only after ALL results are approved in Phase 4, agent-1 creates a final-answer thread with all agents
- agent-1 writes the COMPLETE draft answer to a temporary file (not a summary - the FULL answer with all details)
- agent-1 broadcasts the path to this temporary file so all agents can read it
- All agents read the full draft and CRITICALLY CHECK:
  - Does it cover EVERY sub-question from the original task?
  - Does it include ALL specific details from YOUR findings (exact values, file paths, line numbers)?
  - Are there any factual errors or omissions?
  - Only APPROVE if the draft truly contains everything - do not approve a partial or summarized answer
- When you approve, broadcast your APPROVE mentioning all agents
- If any REQUEST_CHANGES, specify what is missing and go back to Phase 2 (discuss in the planning thread)
- If all APPROVE, agent-1 copies the temporary file to the final answer location

## Rules
- Do NOT modify files in the target repository
- Do NOT ask for human input
- Do NOT idle - always be working or waiting for mention
- ALWAYS include file paths, line numbers, exact values
- If the task asks to run code, ACTUALLY RUN IT
CLAUDE_EOF

# Append role-specific section
if [ "$IS_ASSEMBLER" = "true" ]; then
  cat >> "$INSTANCE_DIR/CLAUDE.md" << ASSEMBLER_EOF

## Your Additional Role: Assembler

You are agent-1. In addition to being a peer, you:
- Create the planning thread (Phase 2) and the final-answer thread (Phase 5)
- You are the ONLY one who writes the final answer file

### Phase 2 Assembler Duties
- When broadcasting the proposed division of work, ask all agents to critically check:
  "Please critically check:
  1. Does this division truly cover ALL potential aspects and implicit sub-questions of the original task?
  2. Does the division preserve semantic dependencies — things the task requires to be done together are assigned to the same agent?
  Only APPROVE if you believe nothing is missing and no semantic dependencies are broken."

### Phase 5 Assembler Duties
- Write the COMPLETE draft answer to /tmp/swe-atlas-draft-answer.txt first
- This draft must be the FULL answer with ALL details - not a summary
- When broadcasting the draft, tell all agents:
  "Please read the full draft at /tmp/swe-atlas-draft-answer.txt and CRITICALLY CHECK:
  1. Does it cover EVERY sub-question from the original task?
  2. Does it include ALL specific details from YOUR findings (exact values, file paths, line numbers)?
  3. Are there any factual errors or omissions?
  Only APPROVE if the draft truly contains everything from your findings. If anything is missing, specify what needs to be added."
- Only after ALL agents vote APPROVE, copy the draft to the final location:

\`\`\`bash
mkdir -p /logs/agent
cp /tmp/swe-atlas-draft-answer.txt /logs/agent/answer.txt
\`\`\`

- NEVER submit before ALL agents vote APPROVE
ASSEMBLER_EOF
else
  cat >> "$INSTANCE_DIR/CLAUDE.md" << 'PEER_EOF'

## Submission
Do NOT write the final answer file. Only agent-1 does that.
PEER_EOF
fi

export PATH="$HOME/.local/bin:$PATH"

echo ">>> Launching Claude Code for agent: $CORAL_AGENT_ID (assembler=$IS_ASSEMBLER)"
cd "$INSTANCE_DIR"

LOG_FILE="$SCRIPT_DIR/instances/$CORAL_SESSION_ID/${CORAL_AGENT_ID}-claude-code.txt"

if [ "$IS_ASSEMBLER" = "true" ]; then
  PROMPT="Read the task instruction at $INSTRUCTION_PATH. Begin Phase 1: explore the repo at $REPO_DIR, understand the question, identify all sub-questions. Then proceed to Phase 2: create a planning thread with all agents (agent-1, agent-2, agent-3, agent-4)."
else
  PROMPT="Read the task instruction at $INSTRUCTION_PATH. Begin Phase 1: explore the repo at $REPO_DIR, understand the question, identify all sub-questions. Then call coral_wait_for_mention to wait for agent-1 to create the planning thread."
fi

exec claude --verbose --output-format=stream-json --permission-mode=bypassPermissions --effort high --print -- "$PROMPT" 2>&1 </dev/null | tee "$LOG_FILE"
