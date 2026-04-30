# DeepSeek-V4-Flash

**DeepSeek-V4-Flash** is the efficient, cost-effective variant of the [[DeepSeek-V4]] model family. With 284 billion total parameters and 13 billion active parameters, it offers fast response times and highly economical API pricing while closely approaching [[DeepSeek-V4-Pro]] in reasoning capabilities.

---

## Specifications

| Property | Value |
|---|---|
| Total Parameters | 284B |
| Active Parameters | 13B |
| Context Window | 1M tokens (default) |
| Release Date | April 24, 2026 |
| Open Source | Yes (weights on Hugging Face) |

---

## Capabilities

### Reasoning
DeepSeek-V4-Flash's reasoning capabilities closely approach those of [[DeepSeek-V4-Pro]], making it suitable for most complex tasks.

### Agentic Tasks
Performs on par with DeepSeek-V4-Pro on simple agent tasks, making it a practical choice for many agentic workflows.

### Speed & Cost
The smaller parameter count delivers faster response times and highly cost-effective API pricing, ideal for production deployments at scale.

---

## Architecture

DeepSeek-V4-Flash uses the same [[DeepSeek Sparse Attention]] (DSA) mechanism and token-wise compression as [[DeepSeek-V4-Pro]], enabling the 1M-token [[Context Window]] with high efficiency. It supports both Thinking and Non-Thinking modes.

---

## API Usage

```python
# Using OpenAI-compatible API
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": "..."}]
)
```

The API supports both OpenAI ChatCompletions and [[Anthropic API]] formats.

---

## Current Routing

As of the release date, `deepseek-chat` (the legacy model alias) routes to `deepseek-v4-flash` in non-thinking mode, and `deepseek-reasoner` routes to `deepseek-v4-flash` in thinking mode. These legacy aliases will be fully retired on **July 24, 2026, 15:59 UTC**.

---

## See Also

- [[DeepSeek-V4]]
- [[DeepSeek-V4-Pro]]
- [[DeepSeek Sparse Attention]]
- [[Context Window]]
- [[Large Language Model]]
- [[Thinking Mode]]
