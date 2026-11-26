---
title: "Part 1 Cards — Foundations (Ch 1–5)"
tags: [cards, foundations]
---

# Part 1 Cards — Foundations

Patterns key: [[concept-map]] · Numbers: [[numbers-that-matter]]

---

### Ch 1 — A Framework for LLM System Design Interviews
**One line:** A repeatable 5-step script for any 45-minute LLM design interview.
**Shape:** Scope → Estimate → High-level (ingest pipeline + query pipeline) → Deep dive (2–3 areas) → Wrap-up (bottlenecks, evolution)
**Patterns:** All of them. This is the frame they plug into.

**3 ideas**
1. Spend the first 5–8 minutes on **scope**: users, risk class, latency SLO, cost envelope, freshness, and what happens on failure.
2. Every LLM system has **two pipelines**: offline ingestion/indexing and online query/inference. Draw both.
3. Use deep dives to show **trade-off reasoning** along the cost–latency–quality–safety axes, not a list of components.

**2 trade-offs**
- Breadth vs depth: cover the whole system shallowly first, then let the interviewer pick the deep dive.
- Quality vs latency vs cost: you can usually optimize two of the three. Say which two, and why.

**Numbers:** Time split ≈ 5 scope / 5 estimate / 10 high-level / 20 deep dive / 5 wrap-up.
**Soundbite:** *"Before I draw anything: what's the risk class and the latency budget? Those two answers pick most of the architecture."*

> [!question]- What are the 5 steps and their time split?
> Scope (5) → Estimation (5) → High-level design (10) → Deep dive (20) → Wrap-up (5).

> [!question]- Name 5 scoping questions specific to LLM systems.
> Risk class / cost of a wrong answer; latency SLO (TTFT vs total); cost per request ceiling; data freshness and sources; failure behavior (refuse, escalate, fall back). Bonus: who the users are and what permissions they have.

> [!question]- Which two pipelines does every design have?
> Offline ingestion/indexing (parse, chunk, embed, index) and online query/inference (guard, route, retrieve, generate, verify, observe).

> [!question]- What does a senior wrap-up include?
> What breaks first at 10× scale, how you'd evaluate and roll out, cost levers, and what you'd build next.

**Go deep:** [[Chapter 1 - A Framework for LLM System Design Interviews]] → "Interview Scoping for LLM Systems" and "Cost-Latency-Quality-Safety Trade-off Engine".

---

### Ch 2 — The LLM Stack and Core Patterns
**One line:** The menu of building blocks, and when to use prompt chaining, RAG, or agents.
**Shape:** Gateway → Router → {Chain | RAG | Agent} → Model tier → Guard → Observe
**Patterns:** P1, P2, P3, P4, P7, P10

**3 ideas**
1. **Use the least autonomy that works.** Fixed chain < RAG < single agent < multi-agent. Each step up adds cost, latency and failure modes.
2. **Model routing/tiering** is the main cost lever. A small model goes first; escalate on low confidence or complexity.
3. **MCP** standardizes the tool protocol layer, so tools get written once and every agent can use them.

**2 trade-offs**
- Chain (predictable, testable) vs agent (flexible, but non-deterministic and expensive).
- Frontier API (quality, zero ops) vs self-hosted open model (cost at scale, data control, ops burden).

**Numbers:** Small-first routing takes **70–80%** of traffic.
**Soundbite:** *"I start with the least autonomous pattern that meets the requirement and only add agency where the task genuinely branches."*

> [!question]- When is an agent justified over a chain?
> When the steps can't be known ahead of time: the path depends on intermediate results, there are open-ended tool choices, or a multi-step search is needed. Otherwise use a chain.

> [!question]- What signals drive the model router?
> Intent class, complexity estimate, confidence, user tier, context length, and cost budget. Fall back upward when confidence is low.

> [!question]- What does MCP solve architecturally?
> It replaces N×M tool integrations with N+M. A standard discovery and invocation protocol for tools, resources and prompts.

**Go deep:** [[Chapter 2 - The LLM Stack and Core Patterns]] → "Pattern Selection: Prompt Chaining vs RAG vs Agentic" and "Model Routing and Tiering".

---

### Ch 3 — Data Pipelines and Vector Infrastructure
**One line:** How documents become retrievable chunks, and how retrieval stays correct as data changes.
**Shape:** Source → Parse → Chunk → Enrich (metadata, ACL) → Embed → Index (BM25 + HNSW) → Alias swap
**Patterns:** P2, P6

**3 ideas**
1. **Chunking sets the recall ceiling.** Structure-aware chunking (headings, tables) beats fixed-size. Keep parent links for context expansion.
2. **Hybrid retrieval** (BM25 + dense, fused with RRF k=60) beats either one alone. BM25 catches IDs and rare terms.
3. **Index lifecycle:** build the new index in the background, then do a blue-green alias swap. Version the embedding model together with the index. Changing the embedding model means a full re-embed.

**2 trade-offs**
- Small chunks (precise, but lose context) vs large chunks (keep context, but noisy and expensive).
- HNSW (fast, memory-heavy) vs IVF-PQ / DiskANN (cheaper at billion scale, lower recall).

**Numbers:** 1536-dim = **6 KB/vector**; **RRF k=60**.
**Soundbite:** *"Retrieval quality is decided at ingestion time. I'd version the chunker and the embedding model as one artifact."*

> [!question]- Why hybrid instead of dense-only?
> Dense misses exact tokens (SKUs, error codes, names). BM25 misses paraphrases. RRF fuses their ranks without having to calibrate scores.

> [!question]- How do you upgrade the embedding model with zero downtime?
> Re-embed into a new index in parallel, shadow-evaluate recall, then do an atomic alias swap. Keep the old index for rollback.

> [!question]- Where do you store ACLs?
> As metadata on each chunk at ingestion, enforced as a pre-filter in the retrieval query, before rerank.

**Go deep:** [[Chapter 3 - Data Pipelines and Vector Infrastructure]] → "Chunking Strategies" and "Vector Index Lifecycle Management".

---

### Ch 4 — Serving, Scaling, and Optimizing LLMs
**One line:** How to serve LLMs at high throughput without blowing up p95 latency.
**Shape:** LB → Admission control → Scheduler (continuous batching) → Inference engine (paged KV) → Stream
**Patterns:** P1, P3, P9

**3 ideas**
1. **Continuous batching** inserts and evicts requests at every token step. 2–4× throughput.
2. **The KV cache is the memory bottleneck.** PagedAttention avoids fragmentation, and prefix caching reuses shared system prompts.
3. **Autoscale on queue depth and KV utilization**, not CPU. Shed load early with admission control and priority classes.

**2 trade-offs**
- Bigger batches (throughput) vs per-request latency (TTFT and inter-token latency).
- Quantize (cheaper, faster) vs quality loss (INT8 <1%, INT4 1–3%).

**Numbers:** **2 GB/B params FP16**; scale out at **60–70%** utilization; KV formula.
**Soundbite:** *"Decode is memory-bandwidth bound, so my levers are batching, KV-cache efficiency and quantization, not more FLOPs."*

> [!question]- Why is decode memory-bound but prefill compute-bound?
> Prefill processes all prompt tokens in parallel (big matmuls). Decode emits one token per step and has to re-read every weight and the KV cache for it.

> [!question]- What does PagedAttention fix?
> KV-cache fragmentation. It allocates in fixed blocks like OS virtual memory, so more concurrent sequences fit and prefixes can be shared.

> [!question]- What metric do you autoscale on?
> Queue depth / pending tokens and KV-cache utilization (plus TTFT SLO burn). GPU "utilization" alone is misleading.

> [!question]- Compute the KV cache for a 70B GQA model at 8K context.
> ≈ 0.31 MB/token × 8,192 ≈ 2.5 GB per sequence at FP16.

**Go deep:** [[Chapter 4 - Serving, Scaling, and Optimizing LLMs]] → "KV Cache Management" and "Autoscaling and Overload Protection". Then [[N4 - Modern Inference Stack]].

---

### Ch 5 — Evaluation, Guardrails, and Safety
**One line:** How you know the system is good, and how you stop it being harmful, at request time and at release time.
**Shape:** Input guard ∥ → Model → Output guard → Log → Offline eval + online judge + red team
**Patterns:** P4, P5, P8

**3 ideas**
1. **RAG eval splits into retrieval and generation:** context recall/precision, then faithfulness and answer relevance.
2. **Guardrails are layered and risk-tiered.** Cheap classifiers run in parallel, and expensive checks run only on high-risk routes.
3. **Agent/MCP security:** tool outputs are untrusted input. Indirect prompt injection is the #1 agent threat.

**2 trade-offs**
- Strict guardrails (safe, more false refusals) vs permissive (better UX, more risk). Tune per tier.
- LLM-as-judge (scalable, biased) vs human eval (accurate, slow and expensive). Calibrate the judge with humans.

**Numbers:** Judge **1–5%**, **kappa ≥ 0.7**; guardrail **< 20ms**.
**Soundbite:** *"I evaluate retrieval and generation separately, so a regression tells me which half broke."*

> [!question]- The four RAG eval metrics?
> Context precision, context recall (retrieval); faithfulness/groundedness, answer relevance (generation).

> [!question]- Known LLM-judge biases?
> Position bias, verbosity bias, self-preference. Mitigate by swapping order, using rubrics, a different model family, and kappa calibration.

> [!question]- Why must guardrails run in parallel?
> Serial checks add their latencies together. Parallel checks cost max(latency) and stay inside the TTFT budget.

**Go deep:** [[Chapter 5 - Evaluation, Guardrails, and Safety]] → "RAG Evaluation Methodology" and "Agent and MCP Security".
