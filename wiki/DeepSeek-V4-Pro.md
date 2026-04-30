# DeepSeek-V4-Pro

**DeepSeek-V4-Pro** is the larger variant of the [[DeepSeek-V4]] model family, featuring 1.6 trillion total parameters with 49 billion active parameters (activated via Mixture-of-Experts routing). It is designed for world-class reasoning, rich world knowledge, and advanced agentic capabilities.

---

## Specifications

| Property | Value |
|---|---|
| Total Parameters | 1.6T |
| Active Parameters | 49B |
| Context Window | 1M tokens (default) |
| Release Date | April 24, 2026 |
| Open Source | Yes (weights on Hugging Face) |

---

## Capabilities

### Reasoning
DeepSeek-V4-Pro achieves world-class reasoning performance, beating all current open models on math, STEM, and coding benchmarks, while rivaling top closed-source models.

### World Knowledge
Leads all current open models in world knowledge benchmarks, trailing only Gemini-3.1-Pro among all models.

### Agentic Capabilities
Achieves open-source state-of-the-art (SOTA) on agentic coding benchmarks. Seamlessly integrates with leading AI agents including [[Claude Code]], OpenClaw, and OpenCode. Powers DeepSeek's own in-house agentic coding workflows.

---

## Architecture

DeepSeek-V4-Pro uses the novel [[DeepSeek Sparse Attention]] (DSA) mechanism combined with token-wise compression. This architectural innovation enables the 1M-token [[Context Window]] with drastically reduced compute and memory costs compared to standard [[Attention Mechanism|attention]].

Dual modes are supported:
- **Thinking Mode** — for complex reasoning tasks
- **Non-Thinking Mode** — for faster, direct responses

---

## API Usage

```python
# Using OpenAI-compatible API
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": "..."}]
)
```

The API supports both OpenAI ChatCompletions and [[Anthropic API]] formats.

---

## See Also

- [[DeepSeek-V4]]
- [[DeepSeek-V4-Flash]]
- [[DeepSeek Sparse Attention]]
- [[Context Window]]
- [[Large Language Model]]
- [[Thinking Mode]]
