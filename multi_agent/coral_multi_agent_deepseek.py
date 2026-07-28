"""L2 (division + negotiation) driven by DeepSeek-V4-Pro via the Modal LiteLLM proxy.

Subclasses the Opus L2 adapter and only swaps the LLM backend (see
`deepseek_proxy.py`). The full five-phase protocol, startup script, and resume
guard are inherited unchanged.

Deploy the proxy first (`modal deploy multi_agent/deepseek_litellm_modal.py`)
and set AGENTRADIO_PROXY_URL in .env, then run harbor directly:
  export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
  harbor run -p ./data/qa \
    --agent-import-path='multi_agent.coral_multi_agent_deepseek:CoralMultiAgentDeepseek' \
    -m "deepseek-v4-pro" -e modal -k 1 -n 1 \
    -i "task-6905333b74f22949d97ba998" --ak reasoning_effort=high \
    -o results/qa/ --job-name "deepseek-divneg-ba998" -y
"""

from multi_agent.coral_multi_agent import CoralMultiAgent
from multi_agent.deepseek_proxy import DeepseekProxyMixin


class CoralMultiAgentDeepseek(DeepseekProxyMixin, CoralMultiAgent):
    """L2 division + negotiation, backed by deepseek-v4-pro through the Modal proxy."""

    @staticmethod
    def name() -> str:
        return "coral-multi-agent-deepseek"
