"""B0 single-agent baseline driven by DeepSeek-V4-Pro via the Modal LiteLLM proxy.

Subclasses harbor's built-in `claude-code` agent and only points it at the proxy
(Anthropic /v1/messages -> OpenRouter deepseek-v4-pro). The task container
installs nothing extra — claude just curls the public URL — so this works on
every image, including the Alpine/musl ones.

Setting ANTHROPIC_BASE_URL in the shell is not enough on its own: the built-in
agent re-mints CLAUDE_CODE_OAUTH_TOKEN, which would take precedence. This thin
subclass forces the proxy endpoint and drops the OAuth token in run().

Deploy the proxy first (`modal deploy multi_agent/deepseek_litellm_modal.py`)
and set AGENTRADIO_PROXY_URL in .env, then run harbor directly:
  export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
  harbor run -p ./data/qa \
    --agent-import-path='multi_agent.claude_code_deepseek:ClaudeCodeDeepseek' \
    -m "deepseek-v4-pro" -e modal -k 1 -n 1 \
    -i "task-6905333b74f22949d97ba998" --ak reasoning_effort=high \
    -o results/qa/ --job-name "deepseek-baseline-ba998" -y
"""

import os

from harbor.agents.installed.claude_code import ClaudeCode

from multi_agent.deepseek_proxy import PROXY_KEY, _proxy_url


class ClaudeCodeDeepseek(ClaudeCode):
    """Single-agent Claude Code backed by deepseek-v4-pro through the Modal proxy."""

    @staticmethod
    def name() -> str:
        return "claude-code-deepseek"

    async def run(self, instruction, environment, context) -> None:
        # Point the parent's env-builder (reads os.environ) at the proxy.
        os.environ["ANTHROPIC_BASE_URL"] = _proxy_url()
        os.environ["ANTHROPIC_API_KEY"] = PROXY_KEY
        os.environ.pop("CLAUDE_CODE_OAUTH_TOKEN", None)  # don't let OAuth win
        await super().run(instruction, environment, context)
