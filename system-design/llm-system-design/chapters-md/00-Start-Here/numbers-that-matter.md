---
title: "Numbers That Matter — 13 to Memorize, the Rest to Derive"
tags: [start-here, numbers, estimation]
---

# Numbers That Matter

The chapters have hundreds of numbers. **You need 13.** The rest you either know roughly or work out in the interview.

> Interviewers don't grade digits. They grade whether you **state an assumption, derive the number, and let it drive a decision**.

---

## Tier 1 — Memorize these 13 (this is the whole list)

| # | Number | Hook to remember it |
|---|---|---|
| 1 | **1 token ≈ 0.75 words ≈ 4 chars** | "4 letters per token" |
| 2 | **FP16 = 2 GB per 1B params** · INT4 ≈ 0.5 GB | 70B at FP16 = 140 GB, which is 2× H100-80GB |
| 3 | **KV cache/token = 2 × layers × kv_heads × head_dim × bytes** | "2 for K and V." 70B with GQA ≈ 0.3 MB/token, so 8K context ≈ 2.5 GB per request |
| 4 | **TTFT < 1s p95 for chat** · voice < 500ms · inline code < 300ms | "1 second, half a second, a third of a second" |
| 5 | **RRF k = 60** | The one magic constant in retrieval |
| 6 | **Retrieve 50–200 → rerank → keep 3–10** | "Wide net, narrow pack" |
| 7 | **Small model handles 70–80% of traffic → cost drops 50–70%** | Routing is the biggest cost lever |
| 8 | **Output tokens cost 3–5× input tokens** | Long answers are expensive; long prompts are cheap and cacheable |
| 9 | **LLM judge on 1–5% of traffic; judge–human kappa ≥ 0.7** | "Sample 1–5, trust at 0.7" |
| 10 | **Semantic cache threshold cosine ≈ 0.92; hit rate 30–40%** for FAQ-like traffic | "92 to hit" |
| 11 | **Scale out at 60–70% GPU utilization; keep 20–40% headroom** | Queueing blows up past ~80% |
| 12 | **Canary at 1–5%** of traffic | Same range as judge sampling, so they're easy to remember together |
| 13 | **Batch API ≈ 50% discount**; prompt-cache reads ≈ 10% of normal input price | "Async is half price; cached prefix is a tenth" |

---

## Tier 2 — Know the order of magnitude, not the exact figure

| Thing | Rough figure |
|---|---|
| 1536-dim float32 vector | 6 KB → 1M vectors ≈ 6 GB (before index overhead, ~1.5×) |
| LoRA trainable params | ~0.1–1% of the model |
| Quantization quality loss | INT8 < 1% · INT4 1–3% |
| Classifier latencies | intent < 10ms · guardrail < 20ms · cross-encoder rerank of 50 docs ~50–100ms |
| Speculative decoding | 2–3× decode speedup |
| Continuous batching | 2–4× throughput vs static batching |
| HNSW recall at sane settings | 95–99% |
| H100 HBM bandwidth | ~3.35 TB/s (useful for the decode formula below) |
| Prefix-cache TTFT reduction | up to ~80% on long shared prefixes |

---

## Tier 3 — Everything else in the chapters

Per-chapter figures like "4,000 tickets/hour" or "p95 of 340ms for the rerank stage" are **worked examples**. Read them to follow the reasoning, then let them go. Remember **the decision they drove**, not the number itself.

---

## Derive, don't memorize: the 5-line estimate

Use this at the start of every design, out loud, in under 2 minutes.

```
1. Traffic   DAU × req/user/day ÷ 86,400 = avg QPS;  peak ≈ 3–5× avg
2. Tokens    QPS × (input + output tokens) = tokens/sec
3. Cost      tokens/day × $/token  (split input vs output: output ×3–5)
4. Compute   decode tok/s per GPU ≈ HBM bandwidth ÷ model bytes  (× batch)
5. Storage   docs × chunks/doc × vector bytes  (+ ~1.5× index overhead)
```

### Worked example (memorize the *shape*, not the numbers)
> "Support bot, **1M DAU**, 5 messages each."
1. 5M req/day ÷ 86,400 ≈ **60 QPS avg, ~250 peak**.
2. Each request ≈ 2K input (system + RAG context) + 300 output. ≈ **11.5B tokens/day**.
3. With 75% routed to a small model, frontier spend drops ~3–4×. **That's why we route** (P1).
4. 8B model at FP16 = 16 GB. 3.35 TB/s ÷ 16 GB ≈ **~200 tok/s per stream**, and batching gives many streams. A few GPUs cover the small tier.
5. 100K KB articles × 10 chunks × 6 KB ≈ **6 GB of vectors**. Fits in memory on one node.

**Decisions that came out of it:** route small-first, cache the system prompt, single-node vector index, put the budget into reranking.

### Why "bandwidth ÷ model bytes"?
At decode time, each new token has to read **every weight once** from HBM. So a single stream's tokens/sec is capped by memory bandwidth divided by model size. Batching amortizes that read across many requests. That's why batching and quantization are the main throughput levers, and why decode is **memory-bound** while prefill is **compute-bound**. (Deep dive: [[N4 - Modern Inference Stack]].)

---

## Self-test
> [!question]- 70B model, FP16: how many H100-80GB just for weights?
> 140 GB → 2 GPUs minimum. You'll want 4 to leave room for the KV cache.

> [!question]- Why route small-first before anything else on cost?
> 70–80% of requests are easy. Moving them to a model that's 10–20× cheaper cuts the bill 50–70%. No other single lever comes close.

> [!question]- Output vs input cost ratio, and its design implication?
> Output costs 3–5× more. Cap max_tokens, prefer structured short outputs, and spend tokens on (cacheable) input context rather than verbose output.

> [!question]- When do you scale out GPUs?
> At 60–70% utilization. Past ~80%, queueing delay drives p95 TTFT up nonlinearly.

> [!question]- Single-stream decode speed of an 8B FP16 model on an H100?
> ≈ 3.35 TB/s ÷ 16 GB ≈ 200 tok/s (upper bound; memory-bound).
