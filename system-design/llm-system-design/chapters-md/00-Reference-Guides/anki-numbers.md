---
title: "Key Numbers & Thresholds — LLM System Design"
tags: [llm, interview-prep, numbers, flashcards, anki]
---

# Key Numbers & Thresholds for LLM System Design

> [!tip] How to use
> These are the specific numbers interviewers expect you to know cold.
> Cover the right column, say the number aloud, then check.
> Import into Anki: copy each row as a Front | Back card.

---

## Token & Model Sizing

| Concept | Value | Why It Matters |
|---|---|---|
| 1 token ≈ | 0.75 words / ~4 characters | Token cost estimation |
| VRAM per 1B params (BF16/FP16) | ~2 GB | GPU sizing |
| 7B model VRAM (BF16) | 14–16 GB → fits 1× A10G/L4 (24GB) | Cheapest self-hosted GPU |
| 70B model VRAM (BF16) | ~140 GB → needs 2× A100 (80GB) | Large model cost |
| KV cache per token (70B model) | ~1 MB per request | Context length cost |
| Embedding size (typical) | 768 or 1536 dims (float32 = 4 bytes/dim) | Vector storage sizing |
| 1536-dim vector size | ~6 KB | Storage per document chunk |
| 1M vectors in RAM | ~6 GB | Vector DB memory budget |

---

## Latency Targets

| Metric | Target | Context |
|---|---|---|
| TTFT (interactive chat) | < 1.0s p95 | User-perceived responsiveness |
| TPOT target | 20–50ms per token | Faster than human reading speed (~200ms/token) |
| Intent classifier latency | < 10ms | Must not add to hot path |
| Guardrail ML classifier | < 20ms | DistilBERT-class model |
| LLM-as-judge (async) | Sampled — not on hot path | > 5% synchronous = latency problem |
| Code completion (IDE) | < 100ms | Local model required below this threshold |
| Speculative decoding speedup | 2–4× TPOT improvement | Requires draft model acceptance rate > 70% |

---

## Scale & Traffic

| Metric | Value | Context |
|---|---|---|
| Typical peak multiplier (consumer) | 12× average QPS | Flash sales, events |
| Capacity planning headroom | 20–40% above peak | Failover margin |
| GPU scale trigger | 60–70% utilization | Not 90% — by then you're degraded |
| Trace sampling rate (1B req/month) | 5% full traces = 50M | Storage vs. statistical significance |
| Full trace compressed size | ~30 KB | Trace storage budget |
| 5% traces × 30KB × 1B req/mo | ~1.5 TB/month trace storage | Cold storage sizing |

---

## Retrieval & RAG

| Metric | Value | Context |
|---|---|---|
| Chunk size (dense retrieval) | 200–500 tokens | Practical sweet spot |
| Chunk overlap | 15–25% | Prevents boundary splits |
| Hybrid search fusion: k in RRF | k = 60 | Standard parameter |
| Semantic cache cosine threshold | ≥ 0.92 | Tighter = fewer false hits |
| Typical semantic cache hit rate | ~40% | For FAQ-like workloads |
| Freshness TTL (policy docs) | 1 hour | High-criticality content |
| Freshness TTL (articles) | 24 hours | Standard content |
| Freshness TTL (FAQs) | 7 days | Stable content |
| Embedding drift trigger | > 5% shift from baseline centroid | Auto re-eval recommendation |

---

## Cost Optimization

| Lever | Savings | Notes |
|---|---|---|
| Semantic caching | ~40% of queries served free | Cosine threshold 0.92 |
| Small model routing (8B vs 70B) | 20× cost reduction | For simple classification queries |
| Prompt compression (LLMLingua) | 30–50% token reduction | On cache-miss long contexts |
| Quantization INT8 vs BF16 | ~50% VRAM, <1% quality loss | Standard for production serving |
| Quantization INT4 vs BF16 | ~75% VRAM, 1–3% quality loss | Edge/on-device use |
| Cost delta gate (low-risk changes) | Block if > 10% increase | Eval gate threshold |
| Cost delta gate (high-risk changes) | Block if > 2% increase | Stricter threshold |

---

## Eval & LLMOps Gates

| Threshold | Low Risk | High Risk |
|---|---|---|
| Min task success rate | ≥ 80% | ≥ 92% |
| Max policy violation rate | ≤ 0.5% | ≤ 0.1% |
| Max unsupported claim rate | ≤ 10% | ≤ 2% |
| p95 TTFT gate | ≤ 3,000ms | ≤ 2,000ms |
| Canary traffic % | 5%, auto-promote after 1h | 1%, manual, 48h minimum |
| Shadow traffic (high risk) | Optional | ≥ 24h or 100K requests |
| Human review (high risk) | Optional | Mandatory: 2+ reviewers, 50+ outputs |
| Judge-human Cohen's kappa (healthy) | ≥ 0.82 | Recalibrate if drops below 0.75 |
| Prompt version shift → task success | Can shift ± 5–15% | Why prompt versioning is critical |
| Tool schema rename → tool-call success | Can drop 10–20% | Why tool schema versioning matters |
| Temperature change → benchmark pass rate | ± 3–8% | Why inference config must be versioned |

---

## Guardrails & Safety

| Metric | Value | Notes |
|---|---|---|
| Escalation target (chatbot) | < 30% of tickets | Below = good containment |
| Confidence threshold for escalation | 0.6 (typical) | Below = defer to human |
| Red-team set (low risk) | ~100 injection/jailbreak cases | Basic gate |
| Red-team set (high risk) | ~1,000 domain-specific cases | Expanded gate |
| PII classifier target recall | ≥ 99.5% | Every missed PII is a violation |
| Guardrail latency budget | < 50ms added at p95 | Combined input + output check |

---

## Compliance & Audit

| Requirement | Value | Notes |
|---|---|---|
| GDPR right-to-deletion response | ≤ 30 days | Legal deadline |
| Financial services audit retention | 7 years | Cold storage tiering required |
| HIPAA minimum necessary standard | Access only needed data | ACL-aware retrieval mandatory |
| Trace tamper-evidence | Append-only store | No in-place updates allowed |

---

## Quick Memory Tricks

| If asked about... | Remember... |
|---|---|
| Why not 1M-token context? | $1–3/request cost + "lost in the middle" + no freshness |
| Why version prompts separately? | Single word change → ±5–15% task success |
| Why segment-level monitoring? | +3% English, −8% Spanish = global average looks fine |
| Why independent rollback? | Coupled rollbacks compound incidents |
| Why private eval set? | Benchmark distribution ≠ production distribution |
