# 01-Foundations

This folder establishes the shared vocabulary, decision frameworks, and infrastructure primitives that every other part of the book assumes. Chapter 1 gives the repeatable interview/design methodology; Chapter 2 gives the top-level pattern-selection framework (prompt chaining vs. RAG vs. agentic); Chapter 3 and Chapter 4 cover the two infrastructure pillars almost every pattern depends on (retrieval/vector infra and model serving); Chapter 5 covers the safety and evaluation layer that wraps around all of them. Later chapters (RAG case studies, agent platforms, fine-tuning, real-time/edge, regulated domains, LLMOps) each specialize or combine these five foundations rather than re-deriving them — so this folder is the load-bearing reference for terms like TTFT/TPOT, cross-encoder reranking, continuous batching, and risk-tiered guardrails used throughout the rest of the book.

---

## Chapter 1: A Framework for LLM System Design Interviews

**Problem:** Build a repeatable 5-step framework for answering any LLM system design prompt with production-grade depth in ~40-45 minutes.

**Core pattern — the 5-step response skeleton:**
1. Scope (6 clarifying questions: risk class, grounding contract, freshness SLA, latency SLO, cost envelope, fallback contract) →
2. Estimation (QPS, token volume, cost, VRAM) →
3. High-level design (Gateway → Policy Layer → Orchestrator → Retrieval Stack → Model Router → Serving Runtime → Cache Hierarchy → Safety Stack → Observability) →
4. Deep dive on 2-3 hardest sub-problems →
5. Wrap-up + FAQ.
- Key architecture named: Client/Gateway, Policy Layer, Orchestrator (routes to direct/RAG/tool/agentic), Retrieval Stack (hybrid + cross-encoder rerank), Model Router, Serving Runtime (continuous batching + KV cache), Cache Hierarchy (retrieval/semantic/response cache), Safety Stack (input/runtime/output), Observability.

**Pros:**
- Forces scoping before architecture — prevents interviews/designs from drifting into unstructured feature lists.
- Ties every component to a measurable metric, surfacing components that can't justify their own existence.
- Bakes in partial-failure thinking (retrieval degrades while model tier stays healthy) rather than binary up/down thinking.

**Cons / tradeoffs:**
- Discipline-heavy: requires getting through scoping in the first 5 of 10 minutes, which is easy to blow past under interview pressure.
- Six mandatory clarifying questions add overhead if the problem is already narrowly scoped by the interviewer.

**When to use:** Any LLM system design interview or greenfield production design. Not really an "architecture" so no direct opposite use case — it's a process, meant to be applied before every chapter's specific pattern choice.

---

## Chapter 2: The LLM Stack and Core Patterns

**Problem:** Choose between prompt chaining, RAG, and agentic orchestration for a multi-pattern production platform (16M requests/day, 50/35/15% pattern split) under latency, cost, and safety constraints.

**Core pattern — three execution paths behind one Intent/Complexity Router:**
- **Prompt Chaining Runtime**: step-level schema contracts, chain-level token/step/timeout guards, deterministic validation hooks between steps, small models for classification/extraction steps.
- **RAG Runtime**: Hybrid Retrieval (BM25 + dense) → Cross-Encoder Reranker → Context Packer.
- **Agent Runtime**: planner/executor loop, Tool Registry, State Store, Step Budget Controller (loop/hallucination-loop detection).
- All three feed a shared **Model Router** (managed vs. self-hosted tiers) → **Serving Runtime** (continuous batching + KV/prefix cache) → **Safety Runtime** → Observability, which feeds back into the Intent Router for drift detection.
- Also covers **MCP** (Model Context Protocol) as the standard protocol layer for tool-using systems: Host, Client, Server, Tools, Resources, Prompts.

**Pros:**
- Prompt chaining: p95 under 2.5s, 5–10x cheaper than agentic; fully deterministic, schema-validated steps.
- RAG: reduces hallucination 40–70% vs. prompt-only for knowledge-intensive tasks; provides auditable citations.
- Agentic: only pattern that handles genuine multi-hop reasoning and real-world side effects (API writes) that can't be pre-enumerated.
- Model routing 70-80% of traffic to fast/balanced tiers cuts serving cost 50-70% with minimal quality loss on simple intents.
- Rule-based dynamic routing (vs. static map or learned router) is recommended default: auditable, no training data needed, correctable in minutes.

**Cons / failure modes:**
- Prompt chaining breaks when required knowledge changes faster than prompt release cycles, or needs more context than fits the window.
- RAG: retrieval misses cause confident-but-wrong answers; index drift silently degrades quality with no visible error signal.
- Agentic: unbounded tail latency without hard timeouts; a looping agent can consume 50,000+ tokens and dozens of round-trips, or exhaust a 100K-token budget in under 10 minutes without step budgets.
- Router misclassification drift: a router calibrated on week-1 traffic can reach 15-20% misclassification by week-8 if not recalibrated; false-downgrade (complex query → cheap tier) produces silently wrong answers since the request still "succeeds."
- Static route maps can misroute 15-30% of traffic overnight after a product/phrasing change.
- Provider rate limiting: a 12x burst (2,220 QPS vs. 185 QPS provisioned) triggers 429 storms if retry logic isn't jittered.

**When to use / not:**
- Start with prompt chaining by default; escalate to RAG only if freshness (hours-days) or citations are required; escalate to agentic only when multi-hop tool orchestration with real side effects is unavoidable (burden of proof = a documented failure case, not preference).
- Learned router models are reserved for orgs with 60+ days of labeled data and an already-hit quality ceiling from rules — not a starting point.

---

## Chapter 3: Data Pipelines and Vector Infrastructure

**Problem:** Design scalable ingestion, embedding, indexing, and hybrid retrieval infrastructure that stays relevant under fast-changing enterprise corpora (5M docs, 300M+ chunks, 500 QPS retrieval, p95 < 120ms).

**Core pattern — two pipelines sharing a versioned index:**
- **Ingestion:** Source Connectors (CDC/crawlers/webhooks, dedup via content hash) → Parser Layer (format-specific: PyMuPDF/BeautifulSoup/python-docx) → Chunking Engine (fixed/semantic/parent-child, tags doc_id/section_path/parent_id/acl_groups) → Embedding Service (batched, $800/day cost circuit breaker) → Index Manager (dual-write HNSW + BM25/Elasticsearch) → Index Lifecycle Controller (blue-green alias swap).
- **Retrieval:** Query Rewriter → BM25 Retriever + ANN Retriever in parallel → Score Fusion (RRF) → ACL Filter → Cross-Encoder Reranker → Context Packer.

**Pros:**
- Hybrid + rerank lifts Recall@10 from 0.55-0.65 (BM25 alone) or 0.70-0.80 (dense alone) to 0.85-0.92 — the default enterprise baseline.
- Parent-child chunking improves citation precision by 10-20% and lets precise (256-512 token) retrieval units expand to full-context (1,500-2,000 token) parents at generation time.
- Blue-green alias swap gives instant rollback (single alias re-point) vs. in-place upsert, which has no safe rollback path once vectors are overwritten.
- Incremental HNSW allows new docs to become searchable within seconds without a full rebuild.
- Matryoshka embeddings enable a 3-5x faster coarse pass (128-dim) before fine reranking on full 1536-dim vectors.

**Cons / failure modes:**
- Parent-child chunking costs ~1.8x storage overhead and adds parent/child sync complexity.
- Cross-encoder reranking adds ~60ms at 500 QPS and requires a dedicated GPU pool (4-8 GPUs) — becomes the throughput bottleneck if undersized.
- Scanned PDFs silently produce empty chunks without OCR; naive line-by-line table extraction destroys column structure; fixed-token chunking splits code functions mid-body.
- ANN recall degrades below 0.80 as the index grows if `ef_construction`/`M` aren't tuned.
- Stale embeddings/index drift is invisible in serving metrics — surfaces only via citation audits or user reports days later.
- Full re-index of 375M chunks at 500 chunks/sec takes ~8.7 days, requiring parallelization.

**When to use:** Hybrid + rerank and parent-child chunking are recommended defaults for enterprise production RAG. BM25-only suits exact-match/ID lookups; dense-only suits pure paraphrase/cross-lingual search; fixed-size chunking is acceptable only for MVP or highly homogeneous corpora. Pre-filter ACLs below 1K groups; post-filter + over-retrieve above that.

---

## Chapter 4: Serving, Scaling, and Optimizing LLMs

**Problem:** Serve LLMs with low, predictable TTFT/TPOT, bounded cost/query, and graceful degradation under 15x traffic spikes (20M requests/day, 7B/34B/70B tiers).

**Core pattern — multi-tier serving stack:**
- Load Balancer + API Gateway → Request Classifier → Model Router (self-hosted tier vs. managed API fallback) → per-tier Serving Runtime (Continuous Batch Scheduler + KV Cache Manager + streaming output) → Autoscaler (queue depth, GPU utilization, TTFT p95, error rate signals) → Cache Hierarchy (prefix/KV cache in VRAM, semantic response cache in Redis).
- Optimization techniques named specifically: continuous batching, chunked prefill, disaggregated prefill/decode, PagedAttention, KV cache quantization (INT8), sliding window attention, multi-query/grouped-query attention, speculative decoding, tensor parallelism, LoRA adapter serving.

**Pros:**
- Continuous batching raises GPU utilization from 30-50% (static) to 60-80%, directly cutting the GPU count needed for a given RPS.
- KV cache INT8 quantization: 50% memory reduction, <0.5% quality degradation on MMLU/HumanEval — doubles effective batch size.
- PagedAttention reduces wasted VRAM from fragmentation by 15-40%, enabling 10-30% more concurrent requests.
- Speculative decoding: 2-3x throughput improvement when draft-model acceptance rate exceeds 70%.
- Prefix/KV caching cuts TTFT by 200-400ms for shared system prompts (2K+ tokens).
- Self-hosted breaks even vs. managed API at ~2M output tokens/day/GPU, saving 60-80% per-token at scale.

**Cons / failure modes:**
- GPU OOM on long-context requests: KV cache for a 70B model at 4K context is ~20.5GB/request; batch of 32 requires ~656GB, exceeding single-node capacity.
- Static batching causes 2-5x TTFT inflation under load; disaggregated prefill/decode needs very high engineering investment (separate fleets, inter-node KV transfer) — justified only at tens of thousands of QPS.
- Sliding window attention can catastrophically fail long-range QA tasks if the answer falls outside the window.
- Autoscaler thrashing if scale-down cooldown and smoothing windows aren't enforced (5-15 min replica churn, cold-start TTFT spikes).
- Provider 429 storms during failover if managed-API overflow isn't rate-limited to ~80% of provider limits with jittered backoff.
- Managed API cost dominates at scale ($30/1M input, $60/1M output tokens for GPT-4-class) vs. $8-12/1M output tokens self-hosted.

**When to use:** Self-hosted only pays off at high, stable volume (>1M tokens/day per model per this book's guidance) with mature ML infra ops (2-4 dedicated engineers); managed APIs suit early-stage, bursty, or unpredictable-volume routes. Priority-queue scheduling (SLO-based preemption, 5s starvation guard) is recommended over FCFS or pure shortest-job-first.

---

## Chapter 5: Evaluation, Guardrails, and Safety

**Problem:** Reduce hallucinations, policy violations, and sensitive-data leakage while preserving utility and staying within a <200ms combined safety latency budget (500 avg / 5,000 peak QPS).

**Core pattern — layered guardrails + 3-mode eval pipeline:**
- **Input Guard** (prompt injection detector, PII scanner, topic classifier, policy enforcer, run in parallel) → **Risk Tier Router** (light/medium/heavy depth by risk class) → model invocation → **Output Guard** (groundedness checker, output PII scanner, policy compliance checker) → **Audit Logger** (immutable, trace-ID tagged) → **Dashboard/Alerting**.
- **Eval Pipeline**: offline (pre-deployment, 2K-5K labeled examples, quality gate blocks >2% regression), online (1-5% sampled production traffic, LLM-as-judge), red-team (quarterly, 500-1,000 adversarial prompts).
- **Policy Engine**: versioned policy-as-code, deployed atomically with model version.

**Pros:**
- Risk-tiered depth avoids paying 80-150ms of LLM-based output verification on low-risk traffic that doesn't need it.
- Rule-based checks run at <5ms/request with near-zero false negatives on known PII/keyword patterns — cheap enough to apply to 100% of traffic.
- Calibrated LLM-as-judge reaches kappa ≈ 0.7-0.8 agreement with human raters (vs. ≈0.5 uncalibrated) using anchor examples.
- Risk-tiered abstention (return "I don't have sufficient information" below a confidence threshold) is safer than low-confidence generation in regulated domains.
- Selectively applying output verifier only to high-risk routes cuts guardrail cost by ~70%.

**Cons / failure modes:**
- Input-only guarding is blind to hallucination and output PII leakage introduced during generation; output-only guarding pays full model invocation cost even for requests that get blocked and misses malicious input the model partially complies with.
- False-positive overblocking: healthcare chatbot example overblocked benign prompts until threshold calibration improved utility by 35% — target is <3% false-positive rate.
- Guardrail latency inflating p95 if input classifiers aren't parallelized or heavy checks run universally instead of risk-tiered.
- Faithfulness/LLM-as-judge scoring costs $0.003-0.01 and 500ms-2s per judgment — not viable at 100% real-time coverage, only sampled (1-5%) or offline.
- Indirect prompt injection via retrieved documents or tool results is especially dangerous in RAG/agent pipelines since it arrives through a "trusted" content path.
- Classifier threshold drift as input distribution shifts causes block-rate changes with no policy change — needs monthly recalibration.
- Red-team exercises are expensive (a banking assistant example passed offline eval but failed red-team jailbreak testing in staging) — jailbreak success rates on untuned systems run 5-20%.

**When to use:** Full input+output guarding (120-230ms overhead) is reserved for finance/healthcare/legal-grade high-risk routes; input-only suffices for low-risk internal Q&A; async output (log+review, zero added latency) suits batch/offline generation where post-hoc remediation is acceptable. Never rely on the model itself as the final security boundary — the policy engine and tool gateway must enforce permissions outside the prompt.

---

## Cross-Cutting Themes

- **Small-model-first routing dominates cost control.** Chapters 1, 2, and 4 all recommend routing the majority of traffic (70-80%) to the cheapest model/path that meets the SLO, reserving large-tier models or agentic escalation for the minority of genuinely complex requests — this is the single largest cost lever across the book (50-70% cost reduction cited repeatedly).
- **Caching hierarchy (semantic + KV/prefix + response) recurs in Chapters 1, 2, and 4** as the default first-line latency/cost optimization: semantic cache hit rates of 20-40% for FAQ-like traffic, KV/prefix caching cutting TTFT 200-500ms on shared system prompts, with the consistent caveat that threshold/TTL miscalibration risks serving stale or wrong-but-similar answers.
- **Cross-encoder reranking on top of hybrid (BM25+dense) retrieval is the repeated "default enterprise baseline"** in Chapters 1, 2, and 3, consistently cited as lifting Recall@5-10 by 5-12 points at a cost of ~60-100ms added latency and a dedicated GPU pool.
- **Blue-green/alias-swap versioning with instant rollback recurs for both indexes (Ch. 3) and model deployments (Ch. 4)** — in-place mutation without a rollback path is called out as high-risk in both chapters, in favor of keeping the old version hot and re-pointing an alias.
- **Continuous batching + KV caching are treated as non-optional baseline infrastructure, not optimizations**, in Chapters 1, 2, and 4 — without them GPU utilization on realistic traffic falls to 30-50%.
- **Latency budgets are consistently per-route/per-pattern, not global** (Ch. 1, 2, 4): a single blended SLO is called out repeatedly as masking regressions in either fast (prompt-chain, direct) or slow (agentic, RAG) paths.
- **Silent degradation is the recurring failure archetype**: stale embeddings/index drift (Ch. 3), router misclassification drift (Ch. 2), and guardrail threshold drift (Ch. 5) all share the same shape — infrastructure metrics stay green while quality quietly degrades, requiring dedicated freshness/drift metrics rather than relying on latency or error-rate alerts.
- **Step/token budget enforcement with loop detection is required wherever agentic or multi-step execution appears** (Ch. 1, 2) — hallucination loops can consume 10-50x expected tokens or exhaust 100K-token budgets in minutes without hard, orchestrator-enforced (not prompt-instructed) limits.
