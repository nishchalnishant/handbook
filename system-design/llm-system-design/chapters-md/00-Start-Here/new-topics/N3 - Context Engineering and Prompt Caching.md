---
title: "N3 — Context Engineering and Prompt Caching"
tags: [new-topic, context-engineering, caching, prompting]
---

# N3 — Context Engineering and Prompt Caching

## Card

**One line:** Context engineering is deciding what goes into the window on every call (and in what order) so the model has exactly what it needs, cheaply.
**Patterns:** P2 (retrieve + pack), P3 (cache), P9 (latency)

**3 ideas**
1. **The window is a scarce resource.** More context is not better: irrelevant tokens cost money, add latency and reduce accuracy ("context rot", lost-in-the-middle).
2. **Order for caching.** Stable prefix (system, tools, examples, long docs) first; volatile parts (user turn, retrieved chunks) last. Cache reads cost ~10% of input.
3. **Manage long-running context actively:** compaction/summarization, tool-result clearing, external memory files, sub-agents with their own clean windows.

**2 trade-offs**
- Stuff the window (simple, recall) vs retrieve just-in-time (cheaper, precise, more moving parts).
- Dynamic per-request content early (relevance) vs a stable prefix (cache hits).

**Soundbite:** *"Prompt engineering is the words; context engineering is everything the model sees. I keep the prefix stable for caching and keep the rest minimal and relevant."*

---

## 1. What is in the context

```
[system prompt] [tool definitions] [few-shot examples] [long reference docs]   ← stable, cacheable
[memory / user profile] [conversation history] [retrieved chunks] [tool results] [user turn]   ← volatile
```

Each slot has a budget. Write it down like a latency budget, e.g. for a 32K target: system 2K, tools 3K, memory 1K, history 6K, retrieval 12K, answer reserve 4K.

## 2. Prompt / prefix caching

| | Provider prompt caching (API) | Prefix caching (self-hosted) |
|---|---|---|
| What | Provider stores KV for a prefix you mark or it detects | Engine reuses KV blocks for shared prefixes (vLLM APC, SGLang RadixAttention) |
| Saving | Cached reads ~**10%** of input price; often a small write premium | Skips prefill compute → lower TTFT, higher throughput |
| Lifetime | Minutes (e.g. ~5 min default, longer options) | Until evicted from GPU memory |
| Hit rule | **Exact** token prefix match | Exact token prefix match |

**Cache killers:** timestamps or user IDs in the system prompt, re-ordered tools, per-request few-shot inserted before static content, non-deterministic serialization (JSON key order).

**Routing for cache locality:** send requests sharing a prefix to the same replica (prefix-aware load balancing). This is P3 meeting P1.

## 3. Techniques for long-running agents and chats

- **Compaction:** when the window nears a threshold, summarize older turns into a state summary; keep recent turns verbatim.
- **Tool-result clearing:** drop old, bulky tool outputs once used; keep a one-line note of what was learned.
- **Structured note-taking / memory files:** the agent writes progress to a file (todo list, decisions) and re-reads it, instead of keeping everything in context.
- **Sub-agents:** delegate a search-heavy subtask to a fresh context; return only a condensed result ([[N6 - Agent Architecture 2026]]).
- **Just-in-time retrieval:** keep handles (file paths, IDs, URLs) in context; load content only when needed.
- **Tool loading on demand:** don't put 100 tool schemas in every call; search tools and load the few needed (Ch 23).

## 4. Long context vs RAG (short version)

Long windows (1M+ tokens) are real, but: cost scales with tokens per call, latency grows, accuracy degrades with distractors, and there is no ACL filtering. Use long context for one big document per session (and cache it); use RAG for large, changing, permissioned corpora. Details in [[N5 - Agentic RAG and Retrieval Upgrades]].

## 5. Packing retrieved context well

- Put the most relevant chunks at the **start and end** (lost-in-the-middle).
- Deduplicate near-identical chunks; merge adjacent chunks from the same doc.
- Include source IDs for citation; delimit with tags (`<doc id="…">`).
- Instruct how to treat retrieved text: as data, not instructions ([[N7 - Agent Security and the Lethal Trifecta]]).

---

## Recall

> [!question]- What is context engineering vs prompt engineering?
> Prompt engineering = writing instructions. Context engineering = choosing, ordering and budgeting everything in the window: instructions, tools, examples, memory, history, retrieved data, tool results.

> [!question]- Name three things that silently break prompt caching.
> Timestamps/IDs in the prefix, changing tool order or definitions, dynamic content placed before static content, non-deterministic serialization.

> [!question]- How do you keep a 2-hour agent session within the window?
> Compaction of old turns, clearing stale tool results, external notes/memory file, sub-agents for heavy subtasks, just-in-time retrieval.

> [!question]- What is "context rot"?
> Model accuracy degrades as the window fills, especially with irrelevant or distracting content, even below the max length.

> [!question]- How does prefix caching help self-hosted serving?
> Shared prefixes reuse stored KV blocks, skipping prefill: lower TTFT and more throughput. Route same-prefix requests to the same replica.

**Related:** [[Chapter 25 - Prompt Engineering in Depth]] · [[Chapter 4 - Serving, Scaling, and Optimizing LLMs]] · [[Chapter 28 - Cost Optimization as a Design Concern]] · [[N4 - Modern Inference Stack]] · [[N6 - Agent Architecture 2026]]
