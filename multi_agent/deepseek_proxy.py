"""Shared plumbing for the DeepSeek-V4-Pro multi-agent variants.

Claude Code speaks only the Anthropic Messages API (`/v1/messages`). DeepSeek is
served through OpenRouter, which is OpenAI-compatible only, so a LiteLLM proxy
translates Anthropic -> OpenRouter. We host that proxy once on Modal (see
`deepseek_litellm_modal.py`); the task containers install nothing and just point
`ANTHROPIC_BASE_URL` at the proxy's public URL.

`DeepseekProxyMixin` reuses the Opus adapters unchanged and only swaps the LLM
backend: it intercepts every container `exec_as_agent` and merges the proxy
endpoint into the env. The Opus adapters' `run()` builds an env dict (OAuth
token, `ANTHROPIC_MODEL`, ...) but never sets `ANTHROPIC_BASE_URL`; merging here
covers the Coral Server start (whose child `claude` processes inherit the env)
and every other agent-user exec.

The proxy URL is per-deployment (each `modal deploy` prints
`https://<your-user>--deepseek-litellm-proxy-serve.modal.run`), so it is read
from the `AGENTRADIO_PROXY_URL` environment variable rather than hard-coded.
"""

import os

# Master key of the Modal-hosted proxy (see deepseek_litellm_modal.py). The URL
# itself gates access; this is a fixed throwaway value, not a secret.
PROXY_KEY = "sk-litellm-local"


def _proxy_url() -> str:
    url = os.environ.get("AGENTRADIO_PROXY_URL", "").strip().rstrip("/")
    if not url:
        raise RuntimeError(
            "AGENTRADIO_PROXY_URL is not set. Deploy the LiteLLM proxy with\n"
            "  modal deploy multi_agent/deepseek_litellm_modal.py\n"
            "then copy the printed https://<user>--deepseek-litellm-proxy-serve.modal.run\n"
            "URL into .env as AGENTRADIO_PROXY_URL and run `source .env`."
        )
    return url


class DeepseekProxyMixin:
    """Route the four Claude Code agents to deepseek-v4-pro via the Modal proxy.

    Mix this in front of an Opus adapter, e.g.
        class X(DeepseekProxyMixin, CoralMultiAgent): ...
    All multi-agent logic (division, negotiation, passive awareness, resume
    guard) is inherited unchanged; only the LLM endpoint is swapped.
    """

    async def exec_as_agent(
        self,
        environment,
        command: str,
        env: dict | None = None,
        cwd: str | None = None,
        timeout_sec: int | None = None,
    ):
        merged = dict(env or {})
        merged["ANTHROPIC_BASE_URL"] = _proxy_url()
        merged["ANTHROPIC_API_KEY"] = PROXY_KEY
        merged.pop("CLAUDE_CODE_OAUTH_TOKEN", None)  # OAuth would override the proxy
        return await super().exec_as_agent(
            environment, command, env=merged, cwd=cwd, timeout_sec=timeout_sec
        )
