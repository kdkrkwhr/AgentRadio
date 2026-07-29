"""LiteLLM proxy hardening hooks (loaded as /tmp/custom_callbacks.py on Modal).

Two protections, both observed to matter for DeepSeek multi-agent runs:

1. Hide `currentUnixTime` from the wait tools (pre-call).
   LLMs cannot know the real time, so they hallucinate values. In the
   message-server build shipped here the field is an int interpreted as
   epoch-ms, so a
   second-level value replays the whole thread history (duplicate redelivery)
   and a millisecond value overflows and crashes deserialization. Omitting the
   field entirely makes the server default to its own clock — the only correct
   call, which the model cannot make on its own.

2. Rewrite upstream in-band errors into real HTTP errors (post-call).
   DeepSeek (via OpenRouter) sometimes returns an infrastructure error as a
   NORMAL 200 completion whose text is e.g. "Connect timeout, please try again
   later." Claude Code treats any plain-text final message as the model's
   answer and ends the session permanently. Detecting such responses and
   aborting them makes Claude Code retry instead of dying.

Loaded via litellm config:
  litellm_settings:
    callbacks: custom_callbacks.proxy_handler_instance
"""

from litellm.integrations.custom_logger import CustomLogger

WAIT_TOOL_MARKERS = ("wait_for_mention", "wait_for_agent_message", "wait_for_message")
FIELD = "currentUnixTime"

# Conservative: only ever matched against SHORT tool-free full responses.
INBAND_ERROR_MARKERS = (
    "connect timeout, please try again later",
    "server is busy, please try again later",
)
MAX_ERROR_TEXT_LEN = 160   # in-band errors are one-liners
DECIDE_TEXT_LEN = 220      # once we've seen this much text, it's a real answer
DECIDE_CHUNKS = 60         # or this many chunks


class UpstreamInBandError(Exception):
    """Raised to abort a stream that is an upstream error disguised as text."""


def _strip_from_schema(schema):
    if not isinstance(schema, dict):
        return
    props = schema.get("properties")
    if isinstance(props, dict):
        props.pop(FIELD, None)
    req = schema.get("required")
    if isinstance(req, list) and FIELD in req:
        schema["required"] = [r for r in req if r != FIELD]


def _looks_like_inband_error(text: str) -> bool:
    t = (text or "").strip().lower()
    if not t or len(t) > MAX_ERROR_TEXT_LEN:
        return False
    return any(m in t for m in INBAND_ERROR_MARKERS) or t.rstrip(".!") == "connect timeout"


def _chunk_text_and_tool(item):
    """Extract (text_delta, saw_tool) from a stream chunk; tolerate any shape."""
    text, tool = "", False
    try:
        choices = getattr(item, "choices", None)
        if choices is None and isinstance(item, dict):
            choices = item.get("choices")
        for ch in choices or []:
            delta = getattr(ch, "delta", None)
            if delta is None and isinstance(ch, dict):
                delta = ch.get("delta")
            if delta is None:
                continue
            t = getattr(delta, "content", None)
            if t is None and isinstance(delta, dict):
                t = delta.get("content")
            if isinstance(t, str):
                text += t
            tc = getattr(delta, "tool_calls", None)
            if tc is None and isinstance(delta, dict):
                tc = delta.get("tool_calls")
            if tc:
                tool = True
        # anthropic-style dict events
        if isinstance(item, dict) and not choices:
            d = item.get("delta") or {}
            if isinstance(d, dict) and isinstance(d.get("text"), str):
                text += d["text"]
            cb = item.get("content_block") or {}
            if isinstance(cb, dict) and cb.get("type") == "tool_use":
                tool = True
    except Exception:
        pass
    return text, tool


class ProxyHardening(CustomLogger):
    # --- protection 1: strip currentUnixTime from wait tool schemas ---
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        try:
            tools = data.get("tools") if isinstance(data, dict) else None
            if isinstance(tools, list):
                for t in tools:
                    if not isinstance(t, dict):
                        continue
                    name = t.get("name") or (t.get("function") or {}).get("name") or ""
                    if any(m in str(name) for m in WAIT_TOOL_MARKERS):
                        _strip_from_schema(t.get("input_schema"))
                        _strip_from_schema((t.get("function") or {}).get("parameters"))
        except Exception:
            pass
        return data

    # --- protection 2a: in-band error rewrite, streaming ---
    async def async_post_call_streaming_iterator_hook(self, user_api_key_dict, response, request_data):
        buffered = []
        text = ""
        decided = False  # True => proven real answer, stream through
        async for item in response:
            if decided:
                yield item
                continue
            buffered.append(item)
            t, tool = _chunk_text_and_tool(item)
            text += t
            if tool or len(text) >= DECIDE_TEXT_LEN or len(buffered) >= DECIDE_CHUNKS:
                decided = True
                for b in buffered:
                    yield b
                buffered = []
        if not decided:
            if _looks_like_inband_error(text):
                print(f"[hardening] aborting in-band upstream error stream: {text[:120]!r}")
                raise UpstreamInBandError(text.strip()[:200])
            for b in buffered:
                yield b

    # --- protection 2b: in-band error rewrite, non-streaming ---
    async def async_post_call_success_hook(self, data, user_api_key_dict, response):
        try:
            choices = getattr(response, "choices", None) or []
            if len(choices) == 1:
                msg = getattr(choices[0], "message", None)
                content = getattr(msg, "content", None) if msg else None
                tool_calls = getattr(msg, "tool_calls", None) if msg else None
                if not tool_calls and isinstance(content, str) and _looks_like_inband_error(content):
                    from fastapi import HTTPException
                    print(f"[hardening] rejecting in-band upstream error response: {content[:120]!r}")
                    raise HTTPException(status_code=502, detail=f"upstream in-band error: {content.strip()[:200]}")
        except Exception as e:
            if type(e).__name__ == "HTTPException":
                raise
        return response


proxy_handler_instance = ProxyHardening()
