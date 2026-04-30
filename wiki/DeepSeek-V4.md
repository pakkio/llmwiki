# DeepSeek-V4

**DeepSeek-V4** is a family of large language models released by DeepSeek on April 24, 2026, as a preview. The release introduces two model variants — [[DeepSeek-V4-Pro]] and [[DeepSeek-V4-Flash]] — both supporting a 1M-token [[Context Window]] as the default standard. DeepSeek-V4 is open-sourced with weights available on Hugging Face.

---

## Key Highlights

- **1M context length** is now the default across all official DeepSeek services.
- **Novel attention architecture**: Token-wise compression combined with [[DeepSeek Sparse Attention]] (DSA) for drastically reduced compute and memory costs.
- **Dual variants**: A full-sized Pro model and an efficient Flash model with similar reasoning capabilities.
- **Dual mode support**: Both Thinking and Non-Thinking modes (see [[Thinking Mode]]).
- **API compatibility**: Supports both OpenAI ChatCompletions and [[Anthropic API]] formats.
- **Agent-optimized**: Seamless integration with leading AI agents such as [[Claude Code]], OpenClaw, and OpenCode.

---

## Variants

| Variant | Total Parameters | Active Parameters | Primary Strengths |
|---|---|---|---|
| [[DeepSeek-V4-Pro]] | 1.6T | 49B | World-class reasoning, rich world knowledge, SOTA agentic coding |
| [[DeepSeek-V4-Flash]] | 284B | 13B | Fast response, cost-effective, on-par with Pro on simple agent tasks |

---

## Innovations

### Structural Innovation

DeepSeek-V4 introduces **token-wise compression** combined with **DeepSeek Sparse Attention (DSA)**. This achieves world-leading long-context efficiency, reducing both compute and memory costs for 1M-length sequences compared to standard [[Attention Mechanism|attention]].

### Agent Capabilities

DeepSeek-V4 is optimized for agentic use cases, achieving open-source state-of-the-art (SOTA) on agentic coding benchmarks. It already powers DeepSeek's in-house agentic coding workflows.

---

## API Availability

The API is live immediately. Users keep their existing `base_url` and only need to update the model name:

- `deepseek-v4-pro` — routes to [[DeepSeek-V4-Pro]]
- `deepseek-v4-flash` — routes to [[DeepSeek-V4-Flash]]

Both models support 1M context and dual Thinking/Non-Thinking modes.

**⚠️ Deprecation notice**: `deepseek-chat` and `deepseek-reasoner` will be fully retired and inaccessible after **July 24, 2026, 15:59 UTC**. (Currently they route to `deepseek-v4-flash` non-thinking/thinking respectively.)

---

## Use via Chat

Available at [chat.deepseek.com](https://chat.deepseek.com) via:
- **Expert Mode** — full access to DeepSeek-V4-Pro
- **Instant Mode** — fast responses via DeepSeek-V4-Flash

---

## Resources

- 📄 Tech Report: [DeepSeek-V4 PDF](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf)
- 🤗 Open Weights: [DeepSeek-V4 Collection on Hugging Face](https://huggingface.co/collections/deepseek-ai/deepseek-v4)

---

## See Also

- [[DeepSeek-V4-Pro]]
- [[DeepSeek-V4-Flash]]
- [[DeepSeek Sparse Attention]]
- [[Context Window]]
- [[Large Language Model]]
- [[Thinking Mode]]
- [[Transformer]]
