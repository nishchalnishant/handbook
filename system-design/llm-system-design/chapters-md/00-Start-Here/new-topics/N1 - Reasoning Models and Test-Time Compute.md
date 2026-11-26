---
title: "N1 — Reasoning Models and Test-Time Compute"
tags: [new-topic, reasoning, test-time-compute, inference]
---

# N1 — Reasoning Models and Test-Time Compute

## Card

**One line:** Models that "think" before answering trade extra output tokens (and latency) for accuracy on hard, verifiable tasks, so thinking becomes a budget you route and tune.
**Patterns:** P1 (route), P9 (latency budget), P10 (attribute cost)

**3 ideas**
1. **Test-time compute is a new scaling axis.** Accuracy on math/code/planning keeps rising with more thinking tokens. Training-time scale is no longer the only lever.
2. **Thinking is a dial, not a switch.** Use effort levels or thinking-token budgets per route: none for extraction/classification, high for planning, debugging, multi-step analysis.
3. **Hidden tokens are real tokens.** Reasoning tokens are billed as output (the expensive side) and add latency before the first visible token. Attribute them separately.

**2 trade-offs**
- Accuracy on hard tasks vs latency and cost (often 3–10× the output tokens).
- Reasoning model everywhere (simple) vs router that only sends hard queries to it (cheaper, more moving parts).

**Soundbite:** *"Thinking tokens are a budget like any other. I route only the hard, verifiable queries to high effort and measure whether the extra tokens actually buy accuracy."*

---

## 1. What changed

| Before (2023) | Now |
|---|---|
| Chain-of-thought was a *prompting trick* ("think step by step") | Reasoning is *trained in* with reinforcement learning on verifiable rewards ([[N2 - Post-Training - DPO, GRPO, RLVR, Distillation]]) |
| Quality = bigger model | Quality = bigger model **or** more thinking per query |
| Output tokens ≈ visible answer | Output tokens = hidden reasoning + visible answer |

Examples of the class: OpenAI o-series / GPT-5 thinking modes, Claude extended/adaptive thinking, Gemini thinking, DeepSeek-R1, Qwen reasoning variants. Most frontier APIs now expose a single model with a **reasoning effort** or **thinking budget** parameter instead of separate "reasoning models".

## 2. Test-time compute strategies

| Strategy | How | When |
|---|---|---|
| **Long single chain** | Model reasons internally, then answers | Default for reasoning models |
| **Self-consistency** | Sample N answers, majority vote | Short final answers (number, label) |
| **Best-of-N + verifier** | Sample N, pick best by verifier/reward model/tests | Code (run tests), math (check answer) |
| **Tree / beam search over steps** | Expand and score partial solutions (process reward model) | Research setups, rarely production |
| **Sequential revision** | Draft → critique → revise | Writing, when a checker exists |

**Rule:** extra compute pays only when you can **verify** (tests, solver, schema, judge). Without a verifier, best-of-N just picks a random good-sounding answer. This is P8.

## 3. Designing with reasoning models

- **Route by difficulty (P1).** Cheap classifier or heuristics (query length, task type, prior failure) pick effort level: `none → low → high`.
- **Separate planner from executor.** Reasoning model plans once; fast non-reasoning model executes many steps (Ch 9, Ch 22).
- **Latency (P9).** TTFT now includes thinking time. For chat UX, stream a "thinking…" state or summarized thoughts; for voice (Ch 18) keep thinking off on the hot path.
- **Prompting changes.** Give goals and constraints, not step-by-step instructions; heavy few-shot CoT can hurt. Ask for the final format explicitly.
- **Context.** Thinking tokens consume the context window and, in multi-turn tool use, some APIs require passing reasoning blocks back. Know your provider's rules.
- **Observability (P10).** Log `reasoning_tokens` separately from `output_tokens`; alert on runaway thinking (cost spikes).

## 4. When NOT to use high reasoning

- Extraction, classification, routing, short rewrites, retrieval-grounded Q&A where the answer is in context.
- Hard real-time paths (autocomplete < 300ms, voice < 500ms).
- When the bottleneck is missing knowledge (fix retrieval, not thinking).

## 5. Numbers (derive, don't memorize)

- Reasoning queries commonly use **thousands to tens of thousands** of hidden tokens.
- Output price is **3–5×** input price → a 5K-token think on a 500-token answer is ~10× the answer cost.
- Derive: `cost/query = (in × p_in) + (think + out) × p_out`. Run it per route.

---

## Recall

> [!question]- What is test-time compute and why does it matter for system design?
> Spending more inference tokens (thinking, sampling, search) per query to raise accuracy. It makes quality a per-request budget you can route and tune, instead of a fixed property of the model.

> [!question]- When does best-of-N help, and when is it wasted?
> It helps when a verifier exists (unit tests, solver, schema, calibrated judge). Without one you're picking among answers you can't rank.

> [!question]- How do reasoning models change cost and latency accounting?
> Hidden reasoning tokens are billed as output and delay the first visible token. Track them separately, budget them per route, alert on spikes.

> [!question]- How would you add a reasoning model to an existing RAG chatbot?
> Router: easy/lookup queries → fast model no thinking; multi-hop/analytical → reasoning model with capped budget. Eval both routes; measure accuracy gain per extra dollar.

> [!question]- Self-consistency vs best-of-N?
> Self-consistency votes on the final answer (needs a short comparable answer). Best-of-N scores whole candidates with a verifier.

**Related:** [[Chapter 4 - Serving, Scaling, and Optimizing LLMs]] · [[Chapter 25 - Prompt Engineering in Depth]] · [[Chapter 28 - Cost Optimization as a Design Concern]] · [[N2 - Post-Training - DPO, GRPO, RLVR, Distillation]] · [[N4 - Modern Inference Stack]]
