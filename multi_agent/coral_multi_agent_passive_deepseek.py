"""L3 (full AgentRadio, passive awareness) driven by DeepSeek-V4-Pro via the
Modal LiteLLM proxy.

Subclasses the Opus L3 adapter and only swaps the LLM backend (see
`deepseek_proxy.py`). Passive-awareness orchestration (background
wait_for_mention, no MCP config, shell wrappers), startup script, and resume
guard are inherited unchanged.

Deploy the proxy first (`modal deploy multi_agent/deepseek_litellm_modal.py`)
and set AGENTRADIO_PROXY_URL in .env, then run harbor directly:
  export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
  harbor run -p ./data/qa \
    --agent-import-path='multi_agent.coral_multi_agent_passive_deepseek:CoralMultiAgentPassiveDeepseek' \
    -m "deepseek-v4-pro" -e modal -k 1 -n 1 \
    -i "task-6905333b74f22949d97ba998" --ak reasoning_effort=high \
    -o results/qa/ --job-name "deepseek-passive-ba998" -y
"""

from multi_agent.coral_multi_agent_passive import CoralMultiAgentPassive
from multi_agent.deepseek_proxy import DeepseekProxyMixin


class CoralMultiAgentPassiveDeepseek(DeepseekProxyMixin, CoralMultiAgentPassive):
    """L3 passive awareness, backed by deepseek-v4-pro through the Modal proxy."""

    @staticmethod
    def name() -> str:
        return "coral-multi-agent-passive-deepseek"
