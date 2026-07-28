"""
Custom Harbor agent: 4 Claude Code instances + Coral Server — PASSIVE AWARENESS variant.

Same orchestration as CoralMultiAgent, but:
  - Coral MCP is NOT exposed to Claude Code (startup_passive.sh writes no .mcp.json).
  - Agents talk to Coral through per-instance shell scripts (curl + python3, MCP over
    Streamable HTTP) with the agent's connection URL baked into thin wrappers.
  - Agents receive messages via a background watcher (wait_for_mention.sh run as a
    background Bash task) while continuing foreground work.

Usage:
  harbor run -p ./data/qa \
    --agent-import-path='multi_agent.coral_multi_agent_passive:CoralMultiAgentPassive' \
    -m "anthropic/claude-opus-4-6" \
    -e modal -k 1 -n 1 \
    -i "task-xxx" \
    --ak reasoning_effort=high \
    -o results/qa/ \
    --job-name "passive-multi-agent-pilot"
"""

import json
import os
import shlex
from pathlib import Path

from harbor.agents.installed.base import BaseInstalledAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext

from multi_agent.resume_guard import upload_guarded_startup

# Files to upload into the container
MULTI_AGENT_DIR = Path(__file__).parent
CORAL_SERVER_JAR = MULTI_AGENT_DIR / "coral-server.jar"
STARTUP_SH = MULTI_AGENT_DIR / "startup_passive.sh"
CORAL_AGENT_TOML = MULTI_AGENT_DIR / "coral-agent-passive.toml"
PASSIVE_SCRIPTS_DIR = MULTI_AGENT_DIR / "passive_scripts"
PASSIVE_SCRIPTS = [
    "coral_mcp_lib.sh",
    "coral_json.py",
    "wait_for_mention.sh",
    "send_message.sh",
    "create_thread.sh",
    "read_resource.sh",
]


class CoralMultiAgentPassive(BaseInstalledAgent):
    """Harbor agent: Coral Server + 4 Claude Code instances with passive awareness."""

    SUPPORTS_ATIF: bool = False

    @staticmethod
    def name() -> str:
        return "coral-multi-agent-passive"

    def get_version_command(self) -> str | None:
        return None

    def parse_version(self, stdout: str) -> str:
        return "0.1.0"

    async def install(self, environment: BaseEnvironment) -> None:
        # 1. System deps + JDK 24 (root)
        await self.exec_as_root(
            environment,
            command=(
                "set -e && "
                "echo '>>> [install] Installing system dependencies...' && "
                "if command -v apk &> /dev/null; then"
                "  apk add --no-cache curl ca-certificates jq bash python3 && "
                '  curl -fsSL "https://api.adoptium.net/v3/binary/latest/24/ga/alpine-linux/x64/jdk/hotspot/normal/eclipse" '
                "  -o /tmp/jdk24.tar.gz && "
                "  mkdir -p /opt/java && "
                "  tar -xzf /tmp/jdk24.tar.gz -C /opt/java --strip-components=1 && "
                "  rm /tmp/jdk24.tar.gz && "
                "  ln -sf /opt/java/bin/java /usr/local/bin/java && "
                "  echo '>>> [install] JDK 24 installed (Alpine)';"
                " elif command -v apt-get &> /dev/null; then"
                "  apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq curl ca-certificates jq python3 > /dev/null 2>&1 && "
                "  echo '>>> [install] Downloading JDK 24 from Adoptium...' && "
                '  curl -fsSL "https://api.adoptium.net/v3/binary/latest/24/ga/linux/x64/jdk/hotspot/normal/eclipse" '
                "  -o /tmp/jdk24.tar.gz && "
                "  mkdir -p /opt/java && "
                "  tar -xzf /tmp/jdk24.tar.gz -C /opt/java --strip-components=1 && "
                "  rm /tmp/jdk24.tar.gz && "
                "  ln -sf /opt/java/bin/java /usr/local/bin/java;"
                " elif command -v yum &> /dev/null; then"
                "  yum install -y curl ca-certificates jq python3 && "
                '  curl -fsSL "https://api.adoptium.net/v3/binary/latest/24/ga/linux/x64/jdk/hotspot/normal/eclipse" '
                "  -o /tmp/jdk24.tar.gz && "
                "  mkdir -p /opt/java && "
                "  tar -xzf /tmp/jdk24.tar.gz -C /opt/java --strip-components=1 && "
                "  rm /tmp/jdk24.tar.gz && "
                "  ln -sf /opt/java/bin/java /usr/local/bin/java;"
                " fi && "
                "java -version && "
                "python3 --version && "
                "echo '>>> [install] JDK + python3 done'"
            ),
            env={"DEBIAN_FRONTEND": "noninteractive"},
        )

        # 2. Install Claude Code (agent user)
        await self.exec_as_agent(
            environment,
            command=(
                "set -e && "
                "echo '>>> [install] Installing Claude Code...' && "
                "curl -fsSL https://claude.ai/install.sh | bash -s -- && "
                'echo \'export PATH="$HOME/.local/bin:$PATH"\' >> ~/.bashrc && '
                'export PATH="$HOME/.local/bin:$PATH" && '
                "claude --version && "
                "echo '>>> [install] Claude Code done'"
            ),
        )

        # 3. Upload coral server JAR + startup files + communication scripts
        WS = "/tmp/coral-workspace"
        AGENT_DIR = f"{WS}/swe-atlas-agent"

        await self.exec_as_agent(
            environment,
            command=f"mkdir -p {AGENT_DIR}/passive_scripts",
        )

        uploads = [
            (CORAL_SERVER_JAR, f"{WS}/coral-server.jar"),
            (STARTUP_SH, f"{AGENT_DIR}/startup_passive.sh"),
            (CORAL_AGENT_TOML, f"{AGENT_DIR}/coral-agent.toml"),
        ] + [
            (PASSIVE_SCRIPTS_DIR / name, f"{AGENT_DIR}/passive_scripts/{name}")
            for name in PASSIVE_SCRIPTS
        ]

        for local_path, remote_path in uploads:
            if not local_path.exists():
                raise RuntimeError(f"Required file not found: {local_path}")
            await environment.upload_file(local_path, remote_path)

        # Make startup + scripts executable
        await self.exec_as_agent(
            environment,
            command=(
                f"chmod +x {AGENT_DIR}/startup_passive.sh "
                f"{AGENT_DIR}/passive_scripts/*.sh"
            ),
        )

        # Overwrite the container startup with the resume-guarded version:
        # if claude exits before the team answer exists, relaunch with --continue.
        await upload_guarded_startup(
            self, environment,
            STARTUP_SH,
            f"{AGENT_DIR}/startup_passive.sh",
        )

        await self.exec_as_agent(
            environment,
            command=f"echo '>>> [install] All files uploaded to {WS}'",
        )

    async def run(
        self, instruction: str, environment: BaseEnvironment, context: AgentContext
    ) -> None:
        # Auth env for Claude Code (passed through to startup_passive.sh)
        env = {}
        oauth_token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
        api_key = (
            os.environ.get("ANTHROPIC_API_KEY")
            or os.environ.get("ANTHROPIC_AUTH_TOKEN")
            or ""
        )
        if oauth_token:
            env["CLAUDE_CODE_OAUTH_TOKEN"] = oauth_token
        if api_key:
            env["ANTHROPIC_API_KEY"] = api_key
        if self.model_name:
            env["ANTHROPIC_MODEL"] = self.model_name.split("/")[-1]
        env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
        env["IS_SANDBOX"] = "1"

        WS = "/tmp/coral-workspace"
        AGENT_DIR = f"{WS}/swe-atlas-agent"

        # 1. Write instruction.md (strip the answer submission part - only agent-1 handles that)
        # Remove everything from "5. When you are confident" onwards
        lines = instruction.split("\n")
        filtered = []
        for line in lines:
            if line.strip().startswith("5. When you are confident"):
                break
            filtered.append(line)
        cleaned_instruction = "\n".join(filtered).rstrip()

        escaped = shlex.quote(cleaned_instruction)
        await self.exec_as_agent(
            environment,
            command=f"echo {escaped} > {WS}/instruction.md",
            env=env,
        )

        # 2. Start Coral Server with health check
        await self.exec_as_agent(
            environment,
            command=(
                f"echo '>>> [run] Starting Coral Server...' && "
                f"java -jar {WS}/coral-server.jar "
                f"--auth.keys=test "
                f"--network.bind_port=5555 "
                f"--network.allow_any_host=true "
                f"--session.defaultWaitTimeout=300000 "
                f"--registry.include_debug_agents=true "
                f"--registry.local_agents={AGENT_DIR} "
                f"> {WS}/coral-server.log 2>&1 & "
                f"CORAL_PID=$! && "
                f"echo '>>> [run] Coral Server PID: '$CORAL_PID && "
                f"for i in $(seq 1 30); do "
                f"  if curl -s http://localhost:5555/api/v1/local/namespace "
                f'    -H "Authorization: Bearer test" > /dev/null 2>&1; then '
                f"    echo '>>> [run] Coral Server ready after '$i' checks'; "
                f"    break; "
                f"  fi; "
                f"  if ! kill -0 $CORAL_PID 2>/dev/null; then "
                f"    echo '>>> [run] ERROR: Coral Server died!'; "
                f"    cat {WS}/coral-server.log | tail -30; "
                f"    exit 1; "
                f"  fi; "
                f"  echo '>>> [run] Waiting for Coral Server... ('$i'/30)'; "
                f"  sleep 2; "
                f"done"
            ),
            env=env,
            timeout_sec=120,
        )

        # 3. Create session - Coral auto-launches 4 agents via startup_passive.sh
        session_json = json.dumps({
            "agentGraphRequest": {
                "agents": [
                    {
                        "id": {
                            "name": "swe-atlas-agent",
                            "version": "0.1.0",
                            "registrySourceId": {"type": "local"},
                        },
                        "name": f"agent-{i}",
                        "provider": {"type": "local", "runtime": "executable"},
                        "description": "SWE Atlas peer agent"
                        + (" (assembler)" if i == 1 else ""),
                        "options": {},
                        "blocking": False,
                    }
                    for i in range(1, 5)
                ],
                "groups": [["agent-1", "agent-2", "agent-3", "agent-4"]],
            },
            "namespaceProvider": {
                "type": "create_if_not_exists",
                "namespaceRequest": {
                    "name": "swe-atlas",
                    "deleteOnLastSessionExit": False,
                },
            },
            "execution": {
                "mode": "immediate",
                "runtimeSettings": {"ttl": 86400000},
            },
        })
        escaped_json = shlex.quote(session_json)

        await self.exec_as_agent(
            environment,
            command=(
                f"echo '>>> [run] Creating session with 4 agents...' && "
                f"curl -s -X POST http://localhost:5555/api/v1/local/session "
                f'-H "Authorization: Bearer test" '
                f'-H "Content-Type: application/json" '
                f"-d {escaped_json} "
                f"> {WS}/session-response.json && "
                f"echo '>>> [run] Session created:' && "
                f"cat {WS}/session-response.json && echo ''"
            ),
            env=env,
        )

        # 4. Copy logs to /logs/agent/ FIRST so they survive Ctrl+C
        await self.exec_as_agent(
            environment,
            command=(
                "mkdir -p /logs/agent && "
                f"cp {WS}/coral-server.log /logs/agent/ 2>/dev/null || true && "
                "echo '>>> [run] Initial logs saved to /logs/agent/'"
            ),
            env=env,
        )

        # 5. Wait for answer.txt (agents are running autonomously)
        # Logs are copied every minute; on timeout logs are saved before exit
        await self.exec_as_agent(
            environment,
            command=(
                "echo '>>> [run] Agents launched. Waiting for answer.txt...' && "
                "for i in $(seq 1 720); do "  # 720 * 10s = 2 hours
                "  if [ -f /logs/agent/answer.txt ]; then "
                "    echo '>>> [run] Answer found after '$((i*10))' seconds!'; "
                "    head -5 /logs/agent/answer.txt; "
                "    break; "
                "  fi; "
                # Every 60 seconds: copy logs + show diagnostics
                "  if [ $((i % 6)) -eq 0 ]; then "
                f"    cp {WS}/coral-server.log /logs/agent/ 2>/dev/null || true; "
                f"    find {WS}/swe-atlas-agent/instances/ -name '*-claude-code.txt' "
                f"      -exec cp {{}} /logs/agent/ \\; 2>/dev/null || true; "
                "    echo '>>> [run] '$((i*10/60))' min | claude procs: '$(ps aux | grep 'claude' | grep -v grep | wc -l)' | logs synced'; "
                "    echo '>>> [run] coral-server.log tail:'; "
                f"    tail -5 {WS}/coral-server.log 2>/dev/null || true; "
                "  fi; "
                "  sleep 10; "
                "done && "
                # On timeout: save all logs before exiting
                "if [ ! -f /logs/agent/answer.txt ]; then "
                "  echo '>>> [run] TIMEOUT: No answer after 2 hours'; "
                f"  cp {WS}/coral-server.log /logs/agent/ 2>/dev/null || true; "
                f"  find {WS}/swe-atlas-agent/instances/ -name '*-claude-code.txt' "
                f"    -exec cp {{}} /logs/agent/ \\; 2>/dev/null || true; "
                "  echo '>>> [run] Logs saved. Diagnostics:'; "
                "  echo '  claude procs: '$(ps aux | grep 'claude' | grep -v grep | wc -l); "
                f"  echo '  instances:'; ls -la {WS}/swe-atlas-agent/instances/ 2>/dev/null || echo '    none'; "
                f"  echo '  coral-server.log last 20 lines:'; tail -20 {WS}/coral-server.log 2>/dev/null || true; "
                "fi"
            ),
            env=env,
            timeout_sec=7200,
        )

        # 6. Final save of coral session state + agent claude-code logs
        await self.exec_as_agent(
            environment,
            command=(
                "echo '>>> [run] Saving logs and session state...' && "
                "mkdir -p /logs/agent/coral-state && "
                "cp /tmp/coral-session-dumps/*.json /logs/agent/coral-state/ 2>/dev/null || "
                "  echo '  No session dumps found' && "
                f"cp {WS}/coral-server.log /logs/agent/ 2>/dev/null || true && "
                # Copy per-agent claude-code.txt logs
                f"find {WS}/swe-atlas-agent/instances/ -name '*-claude-code.txt' "
                f"  -exec cp {{}} /logs/agent/ \\; 2>/dev/null || true && "
                "echo '>>> [run] Done'"
            ),
            env=env,
        )

    def populate_context_post_run(self, context: AgentContext) -> None:
        pass
