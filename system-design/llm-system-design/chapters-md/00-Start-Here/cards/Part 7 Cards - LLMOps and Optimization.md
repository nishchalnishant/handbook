---
title: "Part 7 Cards — LLMOps and Optimization (Ch 24, 27, 28, 29)"
tags: [cards, llmops, cost, observability]
---

# Part 7 Cards — LLMOps and Optimization

These four chapters are the **senior signal**. Any design question ends with "how do you run this in production?" and these are the answer: **P5 eval loop + P6 versioning + P10 observability + cost levers.**

---

### Ch 24 — LLMOps and Production Lifecycle Management
**One line:** Ship changes to prompts, models, indexes and tools safely and reversibly.
**Shape:** Artifact registry (prompt, model, index, tool schema, policy) → Eval gate → Shadow → Canary 1–5% → Full → Monitor → Rollback
**Patterns:** P5, P6, P10

**3 ideas**
1. **Version every artifact** independently with content hashes. A "release" is a manifest of artifact versions.
2. **Evaluation gates:** offline golden set + safety suite must pass; then online canary metrics against control.
3. **Observability + incident response:** know what changed (deploy log), roll back one artifact without dragging others.

**2 trade-offs**
- Gate strictness (safety) vs shipping velocity.
- Pinned model snapshot (stable) vs floating alias "latest" (fixes, but silent behavior change). Pin in production.

**Numbers:** Canary **1–5%**.
**Soundbite:** *"Most LLM incidents are a change nobody thought of as a deploy: a prompt edit, an index rebuild, a provider model update."*

> [!question]- Which artifacts need versioning?
> Prompts, model (and provider snapshot), embedding model, index, chunker config, tool schemas, guardrail policies, eval sets.

> [!question]- Why pin provider model versions?
> A floating alias can change behavior without any deploy on your side, causing unreproducible regressions.

**Go deep:** [[Chapter 24 - LLMOps and Production Lifecycle Management]] → "Artifact Versioning" and "Evaluation Gates".

---

### Ch 27 — Evaluation at Scale
**One line:** Make evaluation trustworthy: calibrated judges, curated golden sets, and statistics that catch real regressions.
**Shape:** Golden sets (curated + production-mined) → Judges (calibrated) + metrics → Significance tests per segment → Gate / dashboard
**Patterns:** P5, P6

**3 ideas**
1. **LLM-as-judge design:** rubric, pairwise when possible, different model family, calibrate to humans (kappa ≥ 0.7), re-calibrate on drift.
2. **Golden sets:** stratified by intent/risk, include failures from production, refresh but keep a frozen regression set.
3. **Statistical rigor:** confidence intervals, enough samples, per-segment breakdowns. A flat average can hide a segment collapsing.

**2 trade-offs**
- Eval coverage vs judge cost/latency. Sample and tier.
- Fresh eval sets (relevant) vs stable sets (comparable over time). Keep both.

**Numbers:** Judge **1–5%** of traffic; **kappa ≥ 0.7**.
**Soundbite:** *"I don't trust a judge I haven't calibrated against humans, and I don't trust an average I haven't sliced by segment."*

> [!question]- Pairwise vs pointwise judging?
> Pairwise (A vs B) is more reliable for comparing versions; pointwise (score 1–5) for absolute monitoring. Swap positions to cancel position bias.

> [!question]- How many samples to detect a regression?
> Depends on effect size and variance: compute with a power analysis. Small deltas need hundreds to thousands of examples.

> [!question]- What's Simpson's-paradox risk in LLM eval?
> Overall score improves while a key segment (language, tier, intent) regresses. Always break down by segment.

**Go deep:** [[Chapter 27 - Evaluation at Scale]] → "LLM-as-Judge Design and Calibration" and "Statistical Rigor". Then [[N8 - Evaluating Agents]].

---

### Ch 28 — Cost Optimization as a Design Concern
**One line:** The cost levers, in order of impact, and how to apply them without hurting quality.
**Shape:** Measure (cost per request/feature/tenant) → Route/cascade → Cache (exact, semantic, prefix) → Compress prompts → Batch + quantize + right-size compute
**Patterns:** P1, P3, P6, P10

**3 ideas**
1. **Lever order:** routing (50–70%) > caching > prompt trimming/compression > batch API > quantization/self-hosting.
2. **Semantic caching:** threshold ~0.92, scope by tenant, exclude personalized answers, invalidate by version.
3. **Right-size compute:** batch async work, quantize, autoscale on queue depth, spot instances for offline jobs.

**2 trade-offs**
- Cheaper model vs quality. Gate with evals per route.
- Aggressive caching vs staleness/wrong answers.

**Numbers:** Routing **50–70%** saving; output **3–5×** input price; batch **~50%** off; cache read **~10%**.
**Soundbite:** *"I attribute cost per feature and tenant first. You can't optimize spend you can't see."*

> [!question]- Rank the cost levers.
> Model routing/cascading; caching (prompt/prefix + semantic); shorter prompts/outputs; batch API for async; quantization/self-hosting at scale.

> [!question]- What is a model cascade?
> Try the cheap model first; check confidence/verifier; escalate to the expensive one only if needed.

> [!question]- When does self-hosting beat an API?
> High steady volume, strict data control, or need for custom weights. Count GPUs, ops staff and idle capacity, not just tokens.

**Go deep:** [[Chapter 28 - Cost Optimization as a Design Concern]] → "Model Routing and Cascading" and "Semantic Caching".

---

### Ch 29 — Observability and Incident Response for LLM Systems
**One line:** See inside every request, alert on quality not just errors, and have runbooks for LLM-specific incidents.
**Shape:** OTel spans per stage → Metrics (latency, tokens, cost, quality proxies) → Sampled, PII-scrubbed logs → SLO burn-rate alerts → Runbooks
**Patterns:** P10

**3 ideas**
1. **Distributed tracing:** one trace per request with spans for retrieval, rerank, LLM, tools, guardrails; propagate across queues/agents.
2. **Metrics + alerts:** TTFT/TPOT p95, error and refusal rates, cost/request, judge scores, groundedness. Alert on SLO burn rate.
3. **Logging:** sample prompts/responses, scrub PII before storage, retain per policy.

**2 trade-offs**
- Log everything (debuggable) vs cost/privacy. Sample + scrub.
- Fast online quality proxies (cheap, noisy) vs judge scores (accurate, delayed).

**Numbers:** Judge-sample **1–5%**; alert on burn rate, not single spikes.
**Soundbite:** *"LLM systems fail silently: HTTP 200, wrong answer. So quality signals have to be first-class metrics."*

> [!question]- Name 3 LLM-specific incidents and the first check.
> Quality drop → what changed (prompt/model/index deploy log). Cost spike → per-feature token attribution (loops, long outputs). Latency spike → queue depth/KV utilization or provider status.

> [!question]- What is "silent degradation"?
> Everything returns 200 OK but answers get worse: retrieval drift, provider model change, stale index. Only quality metrics catch it.

> [!question]- What are OTel GenAI semantic conventions?
> Standard span attributes for LLM calls (model, tokens in/out, operation, etc.) so tools interoperate. See [[N10 - AI Gateway, Structured Outputs, and Programmatic Prompting]].

**Go deep:** [[Chapter 29 - Observability and Incident Response for LLM Systems]] → "Distributed Tracing for LLM Pipelines" and "Incident Runbooks".
