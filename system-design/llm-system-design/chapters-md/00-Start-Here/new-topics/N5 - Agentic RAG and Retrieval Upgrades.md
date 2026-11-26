---
title: "N5 — Agentic RAG and Retrieval Upgrades"
tags: [new-topic, rag, retrieval]
---

# N5 — Agentic RAG and Retrieval Upgrades

## Card

**One line:** RAG moved from "retrieve top-k once" to retrieval as a tool the model calls iteratively, plus better indexing (contextual chunks, late interaction, graphs).
**Patterns:** P2 (retrieve), P7 (bounded loop), P8 (verify)

**3 ideas**
1. **Fix chunks before models.** Contextual retrieval (prepend a doc-level summary to each chunk before embedding/BM25) cuts retrieval failures substantially at index time, cheaply with prompt caching.
2. **Agentic RAG:** the model decides whether, what and how many times to search, rewrites queries, and checks sufficiency. Bounded by steps and budget.
3. **Pick the index for the question type:** dense + BM25 hybrid (default), late interaction/ColBERT (precision), GraphRAG (global "themes across corpus" questions), long context (one big doc).

**2 trade-offs**
- Single-shot RAG (fast, predictable) vs agentic (better on multi-hop, slower and costlier).
- GraphRAG (global sensemaking) vs indexing cost and staleness.

**Soundbite:** *"I start with hybrid retrieval plus reranking and contextual chunks, and only make it agentic when eval shows multi-hop questions failing."*

---

## 1. Contextual retrieval

Problem: a chunk like "Revenue grew 3% over the previous quarter" loses which company and which quarter.
Fix: at index time, for each chunk, an LLM writes 1–2 sentences of context from the full document; prepend it before embedding and BM25 indexing.
Cost: one LLM call per chunk, but the full doc is a cacheable prefix → cheap. Combine with reranking for the largest gain.

Related tricks: **late chunking** (embed the whole doc with a long-context embedder, then pool per chunk), **parent-child / small-to-big** (match small chunks, return the parent section), **HyDE** (embed a hypothetical answer), **query rewriting/decomposition**.

## 2. Late interaction (ColBERT, ColPali)

| | Bi-encoder (dense) | Late interaction | Cross-encoder (reranker) |
|---|---|---|---|
| Representation | 1 vector per doc | 1 vector **per token** | Joint query+doc |
| Scoring | Dot product | MaxSim: each query token finds its best doc token, sum | Full attention |
| Quality | Good | Better on detail/precise terms | Best |
| Cost | Cheapest | More storage (mitigate with compression, PLAID) | Too slow for first stage |

**ColPali / ColQwen:** late interaction over **page images** → retrieve PDFs, slides, scans without OCR. Strong for visually rich docs ([[Chapter 15 - Design a Multimodal Asset Search System]], [[Chapter 11 - Design a Financial Document Extraction System]]).

## 3. GraphRAG

- **Build:** LLM extracts entities + relations → knowledge graph → community detection (Leiden) → LLM summaries per community.
- **Query:** *local* (entity neighborhood + chunks) for specific questions; *global* (map-reduce over community summaries) for "what are the main themes…".
- **When:** corpus-wide sensemaking, relationship-heavy domains (investigations, legal, research).
- **Cost:** expensive indexing, incremental updates are hard. Lighter variants (LightRAG, LazyGraphRAG) defer work to query time.

## 4. Agentic RAG

```
question → [plan / rewrite] → search tool(s) → read → enough? ──no──► refine query / new source (≤ N steps)
                                                         └─yes─► answer with citations → verify claims
```

- Tools: vector search, keyword search, SQL, web search, graph lookup. Model picks.
- **Bounded (P7):** max retrieval rounds (e.g. 3–5), token and time budget.
- **Self-RAG / CRAG ideas:** grade retrieved docs for relevance; if poor, rewrite or fall back to another source.
- Deep research is the extreme version ([[N9 - Design Cases - Coding Agent and Deep Research]]).

## 5. Long context vs RAG

| Choose long context when | Choose RAG when |
|---|---|
| One/few documents per session | Large corpus (GBs+) |
| Need whole-document reasoning | Data changes often |
| Can cache the doc as a prefix | Per-user permissions (ACL filter) |
| Low QPS | High QPS, cost-sensitive |

Often both: RAG to pick the right 50–200K tokens, long context to reason over them.

## 6. Evaluating retrieval

Retrieval: recall@k, MRR, nDCG on a labeled set. Generation: faithfulness/groundedness, answer relevance, citation accuracy. Break down by question type (single-hop, multi-hop, global). Tools: RAGAS-style metrics, calibrated judges ([[Chapter 27 - Evaluation at Scale]]).

---

## Recall

> [!question]- What is contextual retrieval and why is it cheap?
> Prepend LLM-generated document context to each chunk before indexing. Cheap because the document is a cached prefix across its chunks' calls.

> [!question]- How does ColBERT score a document?
> MaxSim: for each query token embedding, take its max similarity over the document's token embeddings; sum across query tokens.

> [!question]- When is GraphRAG worth it?
> Global questions over a whole corpus ("main themes", "how are these entities connected") where top-k chunks can't answer. Not worth it for simple factual lookup.

> [!question]- How do you stop agentic RAG from looping?
> Max retrieval rounds, budget caps, dedupe repeated queries, a sufficiency check, and fallback to "I couldn't find it".

> [!question]- Long context made RAG obsolete. Agree?
> No. Cost and latency per call, accuracy degradation with distractors, freshness and ACLs still favor retrieval. Use long context on top of retrieval.

**Related:** [[Chapter 3 - Data Pipelines and Vector Infrastructure]] · [[Chapter 7 - Design an Enterprise Semantic Search Engine]] · [[Chapter 21 - Design an Advanced RAG Platform]] · [[N3 - Context Engineering and Prompt Caching]] · [[N9 - Design Cases - Coding Agent and Deep Research]]
