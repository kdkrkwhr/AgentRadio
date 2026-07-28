"""Modal-hosted LiteLLM proxy: Anthropic /v1/messages -> OpenRouter deepseek-v4-pro.

Claude Code speaks only the Anthropic Messages API; OpenRouter is OpenAI-
compatible only. This proxy translates between them so the task containers need
nothing installed — they just point ANTHROPIC_BASE_URL at this public URL.
It is a shared, always-on endpoint (min_containers=1) reused by all three
DeepSeek variants (division / div+neg / passive).

One-time setup (your OpenRouter key never leaves your Modal account):
  modal secret create openrouter-deepseek OPENROUTER_API_KEY=sk-or-...

Deploy (prints the URL to put in .env as AGENTRADIO_PROXY_URL):
  modal deploy multi_agent/deepseek_litellm_modal.py
  # -> https://<your-user>--deepseek-litellm-proxy-serve.modal.run

The agents then send ANTHROPIC_API_KEY = MASTER_KEY (below) as x-api-key.
"""

import pathlib

import modal

MASTER_KEY = "sk-litellm-local"  # gates the public proxy; agents send this as x-api-key

CONFIG = """
model_list:
  - model_name: deepseek-v4-pro
    litellm_params:
      model: openrouter/deepseek/deepseek-v4-pro
      api_key: os.environ/OPENROUTER_API_KEY
      # A hung upstream stream can otherwise pin for the whole Modal timeout and
      # stall an entire 4-agent chain. Cut it early; Claude Code retries.
      timeout: 300
      stream_timeout: 120
general_settings:
  master_key: sk-litellm-local
litellm_settings:
  drop_params: true
  request_timeout: 600
  callbacks: custom_callbacks.proxy_handler_instance
"""

# Hardening hooks (strip currentUnixTime, rewrite upstream in-band errors);
# see litellm_strip_unixtime.py for the full rationale.
STRIP_HOOK_LOCAL = pathlib.Path(__file__).parent / "litellm_strip_unixtime.py"

image = (
    modal.Image.debian_slim(python_version="3.11")
    # 1.92.0 crashes on client disconnect; 1.93.0 has the None-guard fix.
    .pip_install("litellm[proxy]==1.93.0")
    .add_local_file(STRIP_HOOK_LOCAL, "/root/litellm_strip_unixtime.py")
)

app = modal.App("deepseek-litellm-proxy")


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("openrouter-deepseek")],
    timeout=3600,
    min_containers=1,        # keep 1 warm so a run doesn't cold-start
    scaledown_window=1800,   # keep warm 30 min after the last request
)
@modal.concurrent(max_inputs=200)  # one async litellm serves many concurrent claude streams
@modal.web_server(port=4000, startup_timeout=240)
def serve():
    import pathlib
    import subprocess

    pathlib.Path("/tmp/litellm_config.yaml").write_text(CONFIG)
    hook_src = pathlib.Path("/root/litellm_strip_unixtime.py").read_text()
    pathlib.Path("/tmp/custom_callbacks.py").write_text(hook_src)
    subprocess.Popen(
        [
            "litellm",
            "--config", "/tmp/litellm_config.yaml",
            "--host", "0.0.0.0",
            "--port", "4000",
        ],
        cwd="/tmp",  # so `custom_callbacks` is importable by litellm
    )
