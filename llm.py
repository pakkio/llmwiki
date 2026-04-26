import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

try:
    from rich.console import Console
    from rich.status import Status
    _console = Console(stderr=True)
    _rich = True
except ImportError:
    _console = None
    _rich = False

load_dotenv()

_client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_SYSTEM = "You are a helpful assistant."

# DeepSeek V4-Flash pricing (USD per token)
_PRICE_INPUT  = 0.14  / 1_000_000   # cache miss
_PRICE_CACHED = 0.028 / 1_000_000   # cache hit
_PRICE_OUTPUT = 0.28  / 1_000_000


def _compute_cost(prompt_tokens: int, completion_tokens: int, cached_tokens: int = 0) -> float:
    return (
        (prompt_tokens - cached_tokens) * _PRICE_INPUT
        + cached_tokens * _PRICE_CACHED
        + completion_tokens * _PRICE_OUTPUT
    )


_TOOL_STYLES = {
    "read_page":    ("cyan",   ""),
    "write_page":   ("green",  ""),
    "list_pages":   ("blue",   ""),
    "search_pages": ("yellow", ""),
}


def _log_tool(name: str, args: dict, result: str) -> None:
    if not _rich:
        print(f"  [{name}] {args} → {result[:80]}")
        return
    color, icon = _TOOL_STYLES.get(name, ("white", ""))
    arg_str = ", ".join(f"{k}={repr(v)[:40]}" for k, v in args.items())
    snippet = result.replace("\n", " ")[:72]
    _console.print(f"  [{color}]{icon} {name}[/{color}]({arg_str}) [dim]→ {snippet}[/dim]")


def chat(prompt: str, model: str = DEFAULT_MODEL, system: str = DEFAULT_SYSTEM) -> str:
    response = _client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def agent(
    prompt: str,
    tools: list,
    dispatch: dict,
    model: str = DEFAULT_MODEL,
    system: str = DEFAULT_SYSTEM,
    label: str = "Thinking",
    on_tool=None,
) -> tuple[str, dict]:
    """Run a tool-calling agent loop until the model stops calling tools.

    Returns (content, stats) where stats has elapsed, turns, token counts, cost_usd.
    """
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
    turn = 0
    t0 = time.time()
    total_prompt = total_completion = total_cached = 0

    while True:
        status_text = f"[bold]{label}[/bold] (turn {turn + 1})…" if _rich else f"{label}…"
        if _rich:
            with _console.status(status_text, spinner="dots"):
                response = _client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                )
        else:
            print(status_text)
            response = _client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

        u = response.usage
        total_prompt += u.prompt_tokens
        total_completion += u.completion_tokens
        details = getattr(u, "prompt_tokens_details", None)
        total_cached += getattr(details, "cached_tokens", 0) or 0

        msg = response.choices[0].message
        turn += 1

        if not msg.tool_calls:
            elapsed = time.time() - t0
            stats = {
                "elapsed": elapsed,
                "turns": turn,
                "prompt_tokens": total_prompt,
                "completion_tokens": total_completion,
                "cost_usd": _compute_cost(total_prompt, total_completion, total_cached),
            }
            if _rich:
                _console.print(
                    f"  [dim]{label} done — {turn} turn{'s' if turn != 1 else ''} · "
                    f"{elapsed:.1f}s · [green]${stats['cost_usd']:.4f}[/green] · "
                    f"{total_prompt:,} in / {total_completion:,} out tok[/dim]"
                )
            return msg.content, stats

        messages.append(msg.model_dump(exclude_unset=True))

        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = dispatch[tc.function.name](args)
            _log_tool(tc.function.name, args, str(result))
            if on_tool:
                on_tool(tc.function.name, args, str(result))
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })


if __name__ == "__main__":
    print(chat("Say hello in one sentence."))
