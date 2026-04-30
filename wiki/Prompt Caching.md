# Prompt Caching

**Prompt caching** is a cost-optimization technique offered by [[Large Language Model]] API providers where frequently reused input tokens (such as system prompts or shared document sets) are cached across requests, resulting in significantly reduced per-token pricing for those cached portions.

---

## How It Works

When you send the same prefix across multiple requests (e.g., the same system prompt or a shared context document), the provider can cache the computed representations (KV-cache) for those tokens. Subsequent requests that include the same prefix are charged at a lower "cached" rate rather than the full input rate.

---

## Cost Savings

Cached tokens can be **50–90% cheaper** than uncached input tokens, depending on the provider. This makes a significant difference for applications that:

- Send the same system prompt with every request.
- Share a common document corpus across multiple queries.
- Use long [[Context Window|context windows]] with repetitive context structures.

For example, providers like Anthropic and OpenAI offer specific cached pricing tiers that apply when the same context prefix is reused.

---

## Best Practices

To maximize caching benefits:

- Place **stable, reusable context** (system prompts, instructions, reference documents) at the beginning of your context.
- Keep **variable content** (user queries, per-request data) after the cached prefix.
- Design prompts so the shared prefix is as large as possible and changes infrequently.

---

## Relationship to Context Strategies

Prompt caching works naturally with [[Context Window#Practical Strategies|Hierarchical Context Management]] — the stable top-level context (Level 1) in a hierarchy is the most cacheable portion.

---

## See Also

- [[Context Window]]
- [[Large Language Model]]
- [[Context Compression]]
- [[Retrieval-Augmented Generation]]
