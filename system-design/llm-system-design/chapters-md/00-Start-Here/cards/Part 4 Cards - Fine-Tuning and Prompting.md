---
title: "Part 4 Cards — Fine-Tuning and Prompting (Ch 8, 10, 25, 26)"
tags: [cards, prompting, fine-tuning]
---

# Part 4 Cards — Fine-Tuning and Prompting

The decision ladder to say out loud: **prompt → few-shot → RAG → fine-tune → train**. Climb only when the rung below fails *and* you can measure the gap.

---

### Ch 8 — Design an AI Coding Assistant
**One line:** Inline completion in the editor plus chat/agent help that understands the repo.
**Shape:** Pipeline A (repo index: AST chunk → embed → symbol graph) · Pipeline B (inline: debounce → context assemble → FIM small model → cancel on keystroke) · Chat/agent on a bigger model
**Patterns:** P1, P2, P3, P9

**3 ideas**
1. **Inline completion is a latency problem:** debounce, cancel stale requests, small fill-in-the-middle model, prefix cache, speculative decoding.
2. **Context assembly:** current file around the cursor, open tabs, recently edited files, retrieved symbols from the repo graph, all within a tight token budget.
3. **Telemetry:** acceptance rate, retained-after-N-minutes rate, latency. Accepted-then-deleted code isn't a win.

**2 trade-offs**
- Bigger context (better suggestions) vs latency on every keystroke.
- Local/small model (fast, private) vs cloud (better). Route by task: inline → small, chat/agent → big.

**Numbers:** Inline **< 300ms**; chat TTFT **< 1s**.
**Soundbite:** *"For inline completion the budget is a third of a second, so every design choice is about cutting tokens and cancelling stale requests."*

> [!question]- What is FIM and why does it matter?
> Fill-in-the-middle: the model sees code before *and after* the cursor. Most edits happen mid-file, so it beats left-to-right completion.

> [!question]- Which metric proves the assistant helps?
> Retained acceptance (suggestions still present after N minutes), not raw acceptance rate. Plus task completion time in A/B tests.

> [!question]- Name 3 tricks to hit the inline latency budget.
> Debounce + cancel; small FIM model with prefix caching; speculative decoding; trim context to the highest-value snippets.

**Go deep:** [[Chapter 8 - Design an AI Coding Assistant]] → "Latency Engineering for Autocomplete" and "Telemetry and Acceptance Tracking". Then [[N9 - Design Cases - Coding Agent and Deep Research]].

---

### Ch 10 — Design an Automated Content Generation Pipeline
**One line:** Generate marketing/product content at volume with brand quality, as a DAG with quality gates.
**Shape:** Brief → DAG: outline → draft → brand/style rewrite → fact check → **quality score** → {publish | HITL review} → Feedback
**Patterns:** P4, P5, P6, P8

**3 ideas**
1. **DAG orchestration:** each step is idempotent, retryable and cached. Fan out per locale/channel.
2. **Quality scoring + HITL:** a judge scores on a rubric. High scores auto-publish, mid scores go to review, low scores regenerate.
3. **Prompt chain design:** small focused prompts beat one giant prompt. Each one is testable and versioned.

**2 trade-offs**
- Auto-publish rate vs brand risk. Thresholds per channel.
- One big prompt (fewer calls) vs a chain (more calls, but each step is controllable and debuggable).

**Numbers:** Async/batch → **~50% discount** via batch APIs.
**Soundbite:** *"Content generation is a batch job. I'd use the batch API, cache aggressively, and spend the savings on a better judge."*

> [!question]- Why a chain instead of one big prompt?
> Each step has a narrow job you can test, cache, retry and swap models for. Failures are localized.

> [!question]- How do you set the auto-publish threshold?
> Calibrate the judge score against human ratings, then pick the threshold that meets the target precision for that channel's risk.

**Go deep:** [[Chapter 10 - Design an Automated Content Generation Pipeline]] → "Quality Scoring and HITL Integration".

---

### Ch 25 — Prompt Engineering in Depth
**One line:** Prompts as production artifacts: structured, example-driven, versioned and tested.
**Shape:** System (role, rules, format) + tools + retrieved context + few-shot + user → output schema; stored in a registry with versions and evals
**Patterns:** P2, P4, P5, P6, P8

**3 ideas**
1. **Structure:** stable parts first (system, tools, examples) for prompt caching; variable parts last. Delimit sections (XML tags).
2. **Few-shot selection:** retrieve examples similar to the input, include edge cases, keep the format consistent.
3. **Versioning:** prompts live in a registry, each version passes the eval suite, rollout is canaried like code.

**2 trade-offs**
- More instructions/examples (accuracy) vs tokens, latency and cost. Cache the static part.
- Chain-of-thought (accuracy on hard tasks) vs latency/cost. Reasoning models do this internally ([[N1 - Reasoning Models and Test-Time Compute]]).

**Numbers:** Cache reads ≈ **10%** of input price. Order the prompt so the prefix stays stable.
**Soundbite:** *"A prompt change is a deploy. Same registry, same eval gate, same canary."*

> [!question]- Why order prompts static-first?
> Prompt/prefix caching only hits on an identical prefix. Static content first maximizes cache hits; dynamic content last.

> [!question]- Static vs dynamic few-shot?
> Static: same examples every time, cacheable. Dynamic: retrieved per input, more relevant, breaks caching for that segment.

> [!question]- What does a prompt registry store?
> Template, version hash, model it's tuned for, params, eval results, owner, rollout state.

**Go deep:** [[Chapter 25 - Prompt Engineering in Depth]] → "Prompt Structure and Composition" and "Prompt Versioning and Production Management". Then [[N3 - Context Engineering and Prompt Caching]] and [[N10 - AI Gateway, Structured Outputs, and Programmatic Prompting]].

---

### Ch 26 — Fine-Tuning and Adaptation
**One line:** When and how to adapt model weights: LoRA, data curation, preference tuning, and serving adapters.
**Shape:** Decide (prompt/RAG not enough?) → Curate data → SFT (LoRA/QLoRA) → Preference tune (DPO) → Eval gate → Serve (multi-LoRA)
**Patterns:** P5, P6

**3 ideas**
1. **Fine-tune for behavior/format/style, RAG for knowledge.** Knowledge changes; weights don't update cheaply.
2. **Data beats quantity:** a few thousand clean, diverse, deduped examples beat 100K noisy ones. Hold out an eval set first.
3. **LoRA:** train small low-rank adapters (~0.1–1% params); QLoRA does it on a 4-bit base. Serve many adapters on one base (multi-LoRA).

**2 trade-offs**
- Fine-tune (lower latency/cost per call, consistent format) vs prompt+RAG (no training, easy to update).
- RLHF (powerful, complex: reward model + PPO) vs DPO (simple, stable, offline). Most teams use DPO ([[N2 - Post-Training - DPO, GRPO, RLVR, Distillation]]).

**Numbers:** LoRA **~0.1–1%** of params.
**Soundbite:** *"Fine-tuning teaches the model how to answer; retrieval tells it what's true today."*

> [!question]- Name 3 good reasons to fine-tune.
> Consistent output format/style; distill a big model's behavior into a small cheap one; domain jargon/task where prompting plateaus; latency (shorter prompts).

> [!question]- What is catastrophic forgetting and the mitigation?
> Losing general skills after narrow fine-tuning. Mix in general data, use LoRA (base frozen), keep the learning rate low, eval on general benchmarks too.

> [!question]- How do you serve 100 customer-specific fine-tunes?
> One base model with hot-swappable LoRA adapters (multi-LoRA batching, e.g. S-LoRA/vLLM), with adapters loaded on demand.

**Go deep:** [[Chapter 26 - Fine-Tuning and Adaptation]] → "LoRA / QLoRA Mechanics" and "Serving Fine-Tuned Adapters".
