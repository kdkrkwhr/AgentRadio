# AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration

![AgentRadio](main.png)

This repository contains the code and data to reproduce the experiments of the paper *AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration*.

**AgentRadio** is an asynchronous message-passing layer that equips coding-agent harnesses with three primitives — `create_thread`, `send_message`, and `wait_for_mention`. The last one runs as a **background task** of the harness, so teammates' messages surface between an agent's work steps without interrupting the foreground. Each agent stays *passively aware* of its peers and folds new findings into its ongoing task, instead of choosing between working and listening.

We evaluate on **SWE-Atlas QnA** (124 long-horizon codebase-understanding tasks over 11 production repositories, 1,306 rubrics), under a five-phase protocol of division of labor and negotiation, with four Claude Code agents. The ladder of configurations isolates each layer:

| Configuration | What it adds | Task acc. (Opus 4.6) | Task acc. (DeepSeek V4 Pro) |
|---|---|---|---|
| **B0** single agent | — | 32.3 % | 29.0 % |
| **B1** best of six single runs | 6× budget, no coordination | 37.9 % | 31.4 % |
| **L1** four agents + division | division of labor | 39.5 % | 31.4 % |
| **L2** + negotiation | joint planning + cross-review (blocking receive) | 51.6 % | 39.5 % |
| **L3** + passive awareness (**AgentRadio**) | background `wait_for_mention` | **62.1 %** | **50.8 %** |

The step from L2 to L3 changes **only** the communication mode. It wins 15 tasks and loses 2 with Opus 4.6 (exact McNemar test, p = 0.0023) and wins 17 while losing 3 with DeepSeek (p = 0.0026). Four Opus 4.6 agents under AgentRadio (62.1 %) surpass the strongest single-agent leaderboard entry, Claude Code with the newer Opus 4.8 (57.2 %).

## Repository layout

```
data/qa/                          124 SWE-Atlas QnA tasks (harbor dataset scale-ai/swe-atlas-qna)
multi_agent/
  coral_multi_agent.py            L2 adapter: division + negotiation (blocking receive)
  coral_multi_agent_ablation.py   L1 adapter: division only
  coral_multi_agent_passive.py    L3 adapter: full AgentRadio (passive awareness)
  startup.sh / startup_ablation.sh / startup_passive.sh
                                  per-agent bootstrap + protocol prompts (CLAUDE.md)
  coral-agent*.toml               message-server agent definitions
  passive_scripts/                MCP-over-HTTP shell primitives (create_thread /
                                  send_message / wait_for_mention / read_resource)
  coral-server.jar                message server (download from Releases, see below)
  monitor_coral_log.sh            live thread/message monitor for running containers
run_config/qa/
  claude-token                    OAuth token helper
  full_run.sh                     B0 baseline batch runner (all 124 tasks)
  run_passive_multi_agent.sh      L3 batch runner
verify_local.py                   rubric verifier (LLM judge), run locally on a trial dir
```

Every task directory under `data/qa/` carries the instruction, the pinned execution environment, and the rubric set used by the verifier.

## Setup

Runs execute in Docker containers on [Modal](https://modal.com), orchestrated by [Harbor](https://github.com/laude-institute/harbor). One task = one container running the message server plus four Claude Code agents.

### 1. Docker Desktop

Install from https://www.docker.com/products/docker-desktop/ and verify with `docker run hello-world`.

### 2. uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Harbor (pinned to 0.6.4)

Newer Harbor releases (0.7+) have breaking API changes that make these adapters fail. Pin the versions:

| Component | Working version |
|-----------|-----------------|
| harbor | **0.6.4** |
| modal | **1.4.2** |

```bash
uv tool uninstall harbor 2>/dev/null || true
uv tool install 'harbor[modal]==0.6.4'
harbor --version   # must show 0.6.4
```

### 4. Modal

```bash
pip install 'modal==1.4.2'
modal --version    # must show 1.4.2
modal setup        # opens browser to log in
```

### 5. Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | sh
claude --version
```

You need a **Claude Max subscription** for the agents. The verifier additionally needs an **Anthropic API key**.

### 6. Message server JAR

The 106 MB server JAR is hosted as an anonymized artifact (too large for a git blob).
The `confirm=t` parameter bypasses the large-file scan interstitial so `curl` gets the
binary directly:

```bash
curl -L -o multi_agent/coral-server.jar \
  "https://drive.usercontent.google.com/download?id=1F0KcnOM0EgRcSXDLuRGgMriMGK4HSzBJ&export=download&confirm=t"
```

The adapters upload this JAR into each task container. Nothing needs to run locally, so no local JDK is required.

### 7. Token helper and .env

```bash
cp run_config/qa/claude-token ~/.local/bin/claude-token
chmod +x ~/.local/bin/claude-token
cp .env.example .env      # then fill in your Anthropic API key
```

## Before each run: refresh the OAuth token

The Claude Code OAuth token rotates. Each container gets a static snapshot at launch, and a stale token kills all four agents with 401 mid-run. Refresh before every session:

```bash
claude /login    # opens browser

security find-generic-password -s "Claude Code-credentials" -w | python3 -c "
import json, sys, os
data = json.loads(sys.stdin.read())
oauth = data.get('claudeAiOauth', {})
with open(os.path.expanduser('~/.claude/.credentials.json'), 'w') as f:
    json.dump({'claudeAiOauth': oauth}, f, indent=2)
print(f'Token refreshed. Expires at: {oauth.get(\"expiresAt\")}')
"

~/.local/bin/claude-token --check
source .env
```

## Running the four configurations

All commands run from the repository root, after `source .env`. Task IDs are the directory names under `data/qa/` (repeat `-i` to batch; drop `-i` entirely to run all 124). `-n` is the number of concurrent tasks (one task = four agents for L1–L3).

### B0 — single agent (baseline)

```bash
source .env

harbor run \
  -p ./data/qa \
  -a claude-code \
  -m "anthropic/claude-opus-4-6" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "baseline-ba998" \
  -y
```

### L1 — four agents + division of labor

Agent-1 explores briefly, partitions the question, and each agent solves its share independently. Answers are merged without review.

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_ablation:CoralMultiAgentAblation' \
  -m "anthropic/claude-opus-4-6" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "division-ba998" \
  -y
```

### L2 — + negotiation (blocking receive)

The full five-phase protocol — joint exploration, negotiated partition to unanimity, live execution, cross-review, assembled submission — with `wait_for_mention` running in the **foreground**, so agents stop working in order to listen.

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent:CoralMultiAgent' \
  -m "anthropic/claude-opus-4-6" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "divneg-ba998" \
  -y
```

### L3 — + passive awareness (full AgentRadio)

Same protocol, but `wait_for_mention` runs as a **background task**: agents keep working and messages surface between steps. Claude Code gets no MCP config — all communication goes through the thin shell wrappers in `passive_scripts/`.

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_passive:CoralMultiAgentPassive' \
  -m "anthropic/claude-opus-4-6" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "passive-ba998" \
  -y
```

`run_config/qa/run_passive_multi_agent.sh` wraps the same command as a batch runner, one harbor job per task id.

## Running with DeepSeek-V4-Pro

The multi-agent configurations (L1–L3) can be run with **DeepSeek-V4-Pro** agents instead of Opus 4.6, reproducing the DeepSeek column of the results table. Everything about the protocol, prompts, startup scripts, and resume guard is identical; only the LLM backend changes.

Claude Code speaks only the Anthropic Messages API, while DeepSeek is served through OpenRouter (OpenAI-compatible only). We bridge the two with a **LiteLLM translation proxy hosted once on Modal**. The task containers install nothing — they just point `ANTHROPIC_BASE_URL` at the proxy's public URL. 

The rubric verifier is unchanged: it still uses your Anthropic judge (`OPENAI_API_KEY` / `EVAL_MODEL`). DeepSeek is only the *agent* backend.

### One-time proxy setup

```bash
# 1. An OpenRouter API key with deepseek-v4-pro access (https://openrouter.ai/keys)
#    is stored as a Modal secret — it never leaves your Modal account.
modal secret create openrouter-deepseek OPENROUTER_API_KEY=sk-or-...

# 2. Deploy the proxy. This prints your personal URL.
modal deploy multi_agent/deepseek_litellm_modal.py
# -> https://<your-user>--deepseek-litellm-proxy-serve.modal.run

# 3. Put that URL in .env so the adapters can find it:
echo 'export AGENTRADIO_PROXY_URL=https://<your-user>--deepseek-litellm-proxy-serve.modal.run' >> .env
source .env
```

The proxy stays warm (`min_containers=1`); redeploy only after editing it. To stop billing when idle: `modal app stop deepseek-litellm-proxy` (a later `modal deploy` brings it back).

### L1 / L2 / L3 with DeepSeek

Identical to the Opus commands above, but the import path points at the DeepSeek adapter and `-m "deepseek-v4-pro"` routes through the proxy. `source .env` must have exported `AGENTRADIO_PROXY_URL`. Task IDs and `-i` batching work exactly as above.

#### DeepSeek B0 — single agent (baseline)

The DeepSeek baseline uses a thin subclass of the built-in `claude-code` agent (it forces the proxy endpoint and drops the OAuth token the built-in agent would otherwise re-mint), so it takes `--agent-import-path` rather than `-a claude-code`.

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.claude_code_deepseek:ClaudeCodeDeepseek' \
  -m "deepseek-v4-pro" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "deepseek-baseline-ba998" \
  -y
```

#### DeepSeek L1 — division only

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_ablation_deepseek:CoralMultiAgentAblationDeepseek' \
  -m "deepseek-v4-pro" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "deepseek-division-ba998" \
  -y
```

#### DeepSeek L2 — + negotiation

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_deepseek:CoralMultiAgentDeepseek' \
  -m "deepseek-v4-pro" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "deepseek-divneg-ba998" \
  -y
```

#### DeepSeek L3 — + passive awareness

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_passive_deepseek:CoralMultiAgentPassiveDeepseek' \
  -m "deepseek-v4-pro" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "deepseek-passive-ba998" \
  -y
```

The shared proxy injection (which swaps the LLM backend while inheriting all multi-agent logic, startup scripts, and the resume guard) lives in `multi_agent/deepseek_proxy.py`; the B0 baseline subclass is `multi_agent/claude_code_deepseek.py`.

### Resume a cancelled or failed job

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
harbor job resume -p results/qa/<job-name> -f CancelledError -f RuntimeError
```

### Live monitoring (optional, separate terminal)

```bash
bash multi_agent/monitor_coral_log.sh   # renders coral://state from the running container
```

## Scoring

Each trial writes the team's answer to `<trial>/agent/answer.txt`. Score it with the benchmark's LLM judge:

```bash
source .env
python3 verify_local.py <task-id> <trial-dir>
# e.g.
python3 verify_local.py task-6905333b74f22949d97ba998 \
  results/qa/divneg-ba998/task-6905333b74f22949d97ba998__XXXXX
```

This writes `<trial>/verifier/reward.txt` (1 only when every rubric passes) and `evaluation_results.json` (per-rubric scores). `pip install openai` if missing.

## Trial output structure

```
task-xxx__randomId/
├── config.json / result.json / trial.log
├── agent/
│   ├── answer.txt                # final answer (written by agent-1)
│   ├── coral-server.log          # threads and messages
│   └── agent-{1..4}-claude-code.txt
└── verifier/
    ├── reward.txt
    └── evaluation_results.json
```

## Troubleshooting

- **401 errors mid-run** — the OAuth token snapshot went stale. Refresh (see above), then `harbor job resume -p results/qa/<job-name> -f NonZeroAgentExitCodeError`.
- **`claude: not found` in coral-server.log** — the startup scripts export `PATH="$HOME/.local/bin:$PATH"`; check that Claude Code installed inside the container.
- **Alpine-based tasks** — some tasks use Alpine images; the adapters auto-detect this and install an Alpine-compatible JDK.
- **Inspecting communication** —
  `grep "sent message\|created thread" <trial>/agent/coral-server.log | sed 's/\x1b\[[0-9;]*m//g'`

## Acknowledgements

The task data is the [SWE-Atlas QnA](https://github.com/scaleapi/SWE-Atlas) benchmark (harbor dataset `scale-ai/swe-atlas-qna`) by Scale AI. Runs are orchestrated with [Harbor](https://github.com/laude-institute/harbor) on [Modal](https://modal.com). 

## License

Apache 2.0. See [LICENSE](LICENSE).
