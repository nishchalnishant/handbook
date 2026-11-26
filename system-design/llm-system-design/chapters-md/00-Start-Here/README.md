---
title: "Start Here — How to Study This Book Without Drowning"
tags: [start-here, study-plan, interview-prep]
---

# Start Here

The book is ~200K words. You don't read it. You **study it in 25-minute loops**, card-first.

## The one rule

> **Never open a chapter cold.** Read its 5-minute card first. Then read *one* deep section. Then close it and answer the recall questions.

## What's in this folder

| File | What it is | Time |
|---|---|---|
| [[concept-map]] | The **10 patterns** every chapter remixes. Learn these once; every chapter becomes "which 3–4 patterns, tuned how?" | 20 min |
| [[numbers-that-matter]] | Numbers sorted into 3 tiers: **memorize 13**, know the order of magnitude, ignore the rest. Plus how to *derive* instead of memorize. | 15 min |
| [[study-plan]] | 45 checkbox sessions of 25 minutes each, with spaced review built in. There's also a 2-week fast track. | — |
| `cards/` | One **5-minute card** per chapter, grouped by part. | 5 min each |
| `new-topics/` | **10 topics the book doesn't cover** (2025–26 senior-level material): reasoning models, RL post-training, context engineering, modern inference, agent security, agent evals, and more. | 15–20 min each |

### Cards (31 chapters)
- [[Part 1 Cards - Foundations]] — Ch 1–5
- [[Part 2 Cards - RAG and Search]] — Ch 6, 7, 11, 12, 15, 17, 21
- [[Part 3 Cards - Agents and MCP]] — Ch 9, 16, 19, 22, 23
- [[Part 4 Cards - Fine-Tuning and Prompting]] — Ch 8, 10, 25, 26
- [[Part 5 Cards - Real-Time and Edge]] — Ch 14, 18, 31
- [[Part 6 Cards - Regulated and Safety-Critical]] — Ch 13, 20, 30
- [[Part 7 Cards - LLMOps and Optimization]] — Ch 24, 27, 28, 29

### New topics (not in the chapters)
1. [[N1 - Reasoning Models and Test-Time Compute]]
2. [[N2 - Post-Training - DPO, GRPO, RLVR, Distillation]]
3. [[N3 - Context Engineering and Prompt Caching]]
4. [[N4 - Modern Inference Stack]]
5. [[N5 - Agentic RAG and Retrieval Upgrades]]
6. [[N6 - Agent Architecture 2026]]
7. [[N7 - Agent Security and the Lethal Trifecta]]
8. [[N8 - Evaluating Agents]]
9. [[N9 - Design Cases - Coding Agent and Deep Research]]
10. [[N10 - AI Gateway, Structured Outputs, and Programmatic Prompting]]

## The 25-minute loop

```
 5 min   Read the card. Say the soundbite out loud.
15 min   Read ONE deep section of the chapter (the card says which).
 5 min   Close everything. Open each recall question and answer it out loud before you expand it.
```

If you get a recall question wrong, put a `#review` tag next to it. Your review queue is just a search for `#review`.

## How to handle the numbers

The chapters have hundreds of numbers. **Most are there to show the reasoning, not to be memorized.** While reading:
- A number in **bold on a card** → memorize it (there are only 13; see [[numbers-that-matter]]).
- A number in a chapter → ask *"what decision did this number drive?"* Remember the decision, not the digit.
- In an interview → **state an assumption and derive**. "Assume 1M DAU, 10 requests each, so ~120 QPS average and ~1K at peak" beats reciting a figure.

## What "senior" means in the interview

Interviewers at senior level aren't checking whether you know the components. They're listening for these five things:
1. **You scope before you build.** Risk class, latency SLO, cost envelope, freshness, and what happens on failure (Ch 1).
2. **You name the trade-off and pick one.** "Hybrid retrieval costs ~40ms but recovers exact-match IDs that dense search misses. Worth it here because..."
3. **You design for silent failure.** LLM systems degrade without throwing errors. Show the eval, drift, and rollback story.
4. **You put the deterministic system in charge.** The LLM proposes; schemas, rules, budgets and approvals decide.
5. **You know what changed in 2025–26.** Reasoning models, agent security, context engineering, MCP, and RL post-training. That's the `new-topics/` folder.

## Existing reference material (use later, not first)
- [[drill-questions]] — 100+ Q&As. Use them in review sessions.
- [[mock-interview]] — full mock scripts. Use them in weeks 5–6.
- [[anki-numbers]] — the full number set. Optional; [[numbers-that-matter]] is the filtered version.
- [[cheat-sheet]] and [[glossary]] — look things up here.
- [[transformer-internals]] — read before [[N4 - Modern Inference Stack]].
