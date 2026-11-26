---
title: "N4 — Modern Inference Stack"
tags: [new-topic, inference, serving, gpu]
---

# N4 — Modern Inference Stack

## Card

**One line:** The techniques that make today's serving fast and cheap, grouped by the bottleneck they attack: memory bandwidth, KV cache size, or compute.
**Patterns:** P3 (KV/prefix cache), P9 (latency), P1 (right-size)

**3 ideas**
1. **Decode is memory-bound, prefill is compute-bound.** Almost every trick either shrinks bytes moved per token (quantization, GQA/MLA, MoE) or does more useful work per byte (batching, speculative decoding).
2. **KV cache is the capacity limit.** PagedAttention, GQA/MLA, FP8 KV and prefix sharing all exist to fit more concurrent sequences.
3. **Disaggregate prefill and decode** at scale: different hardware profiles, independent scaling, better TTFT/TPOT SLOs.

**2 trade-offs**
- Lower precision (FP8/FP4/INT4: faster, cheaper) vs quality loss. Eval per task.
- Bigger batch (throughput, cost) vs per-user latency (TPOT).

**Soundbite:** *"Decode is a memory-bandwidth problem, so I look first at what shrinks the bytes per token: quantization, GQA, KV cache compression, then speculative decoding to get more tokens per pass."*

---

## 1. Map: technique → bottleneck

| Technique | Attacks | One-liner |
|---|---|---|
| **FlashAttention (2/3)** | Memory traffic in attention | Tiled attention in on-chip SRAM; exact, not approximate. FA3 uses Hopper features (async, FP8) |
| **PagedAttention** | KV fragmentation | KV stored in fixed blocks like OS pages → near-zero waste, sharing across sequences |
| **Continuous batching** | GPU idle between requests | Add/remove sequences every decode step instead of fixed batches |
| **Chunked prefill** | Long prompts stalling decodes | Split prefill into chunks mixed with decode steps → smoother TPOT |
| **GQA / MQA** | KV size | Many query heads share fewer K/V heads → KV shrinks by group factor (e.g. 8×) |
| **MLA** (DeepSeek) | KV size | Compress K/V into a low-rank latent; cache the latent → much smaller KV |
| **MoE** | Compute per token | Only top-k experts active per token: huge total params, small active params. Needs all weights in memory; expert parallelism |
| **Quantization FP8 / FP4 / INT4** | Bytes per weight | FP8 is near-lossless on H100+; FP4 (Blackwell NVFP4/MXFP4) and INT4 (AWQ/GPTQ) for more savings |
| **KV cache quantization** | KV size | FP8/INT8 KV doubles concurrent sequences with small quality cost |
| **Speculative decoding** | Sequential decode | Draft proposes k tokens, target verifies in one pass; output distribution unchanged |
| **EAGLE (1/2/3)** | Draft quality | Lightweight draft head on target's hidden states; high acceptance, 2–3× speedup |
| **MTP (multi-token prediction)** | Draft quality | Model trained to predict several future tokens; heads used as built-in drafter (DeepSeek-V3) |
| **Prefix caching / RadixAttention** | Repeated prefill | Reuse KV for shared prefixes (system prompts, few-shot, chat history) |
| **Disaggregated prefill/decode** | Interference between phases | Separate prefill and decode pools; ship KV between them (DistServe, Dynamo, llm-d, Mooncake) |
| **Tensor / pipeline / expert parallelism** | Model doesn't fit / throughput | TP within node (NVLink), PP across nodes, EP for MoE experts |

## 2. Engines (name 2–3 and why)

| Engine | Strength |
|---|---|
| **vLLM** | Default open-source; PagedAttention, broad model support, prefix caching, multi-LoRA, spec decoding |
| **SGLang** | RadixAttention (prefix tree cache), fast structured output, strong for agentic/multi-call workloads |
| **TensorRT-LLM** | Peak NVIDIA performance; FP8/FP4 kernels; more build effort |
| **NVIDIA Dynamo / llm-d** | Orchestration layers for disaggregated, KV-aware routing at cluster scale |
| **llama.cpp / MLC / ExecuTorch** | Edge and local ([[Chapter 31 - Edge and On-Device LLM Deployment]]) |

## 3. Derive, don't memorize

- **Weights memory** = params × bytes/param. 70B @ FP16 = 140 GB; @ FP8 = 70 GB; @ INT4 ≈ 35 GB.
- **KV per token** = 2 × layers × kv_heads × head_dim × bytes. GQA cuts `kv_heads`; MLA replaces it with a small latent.
- **Decode speed bound** ≈ memory bandwidth / bytes read per token. Batch amortizes weight reads across users.
- **Spec decoding gain** depends on acceptance rate α and draft cost; it helps most at **low batch** (latency-bound), less at high batch (already compute-bound).

## 4. Interview flow for "make serving 2× cheaper"

1. Measure: GPU util, KV utilization, batch size, TTFT/TPOT, prefix-hit rate.
2. Quantize weights (FP8) and KV (FP8) → more sequences per GPU.
3. Turn on prefix caching + cache-aware routing.
4. Tune batching (max tokens per step, chunked prefill) against TPOT SLO.
5. Speculative decoding (EAGLE/MTP) for latency-bound routes.
6. At scale: disaggregate prefill/decode; MoE models for quality per active FLOP.
7. Gate every step on the eval suite (P5).

---

## Recall

> [!question]- Why is decode memory-bound?
> Each new token requires reading all weights and the KV cache from HBM but does little arithmetic per byte at small batch sizes.

> [!question]- GQA vs MLA?
> GQA: groups of query heads share one K/V head, shrinking KV by the group factor. MLA: K/V compressed into a low-rank latent vector that is cached, shrinking KV further.

> [!question]- Does speculative decoding change outputs?
> No. With proper rejection sampling the target model's output distribution is preserved; it only changes speed.

> [!question]- Why disaggregate prefill and decode?
> Prefill is compute-heavy and bursty, decode is memory-bound and steady. Mixing them makes long prompts hurt everyone's TPOT. Separate pools scale and tune independently.

> [!question]- What does MoE save and what doesn't it save?
> Saves compute per token (only active experts run). Doesn't save memory: all experts must be loaded. Adds routing/load-balancing and expert-parallel communication.

> [!question]- FlashAttention: approximate or exact?
> Exact. It reorders computation (tiling, online softmax) to avoid writing the full attention matrix to HBM.

**Related:** [[Chapter 4 - Serving, Scaling, and Optimizing LLMs]] · [[Chapter 28 - Cost Optimization as a Design Concern]] · [[Chapter 31 - Edge and On-Device LLM Deployment]] · [[N3 - Context Engineering and Prompt Caching]] · `00-Reference-Guides/transformer-internals.md`
