---
title: "SWE2 → AI Engineer Transition Guide"
tags: [llm, career, transition, behavioral, portfolio, project]
---

# SWE2 → AI Engineer Transition Guide

> [!important] The honest truth
> Interviewers hire AI Engineers who have **built** AI systems, not just read about them.
> This guide covers: how to frame your SWE2 background, what to build, and how to answer behavioral questions as an AI-specific candidate.

---

## Part 1 — Your Positioning Story

### The Narrative Frame (use this in every intro)

> *"I've been a Software Engineer 2 for [X] years, where I built [brief description of your work — APIs, data pipelines, services]. Over the past [6-12 months] I've been deliberately moving into AI Engineering — I've studied production LLM system design, built a [mini-project], and I'm now looking for a role where I can apply my software engineering rigor to AI systems at scale."*

**Key principles:**
- Lead with your SWE depth (it's a differentiator — most AI Engineers can't build reliable production systems)
- Show the intentionality of the transition (studied + built, not just "interested in AI")
- Connect your SWE skills to AI problems explicitly (see the table below)

### SWE2 Skills → AI Engineer Value

| Your SWE2 Skill | Why It's an AI Engineer Advantage |
|---|---|
| API design + REST services | LLM systems are API-first; you know how to build reliable, versioned service contracts |
| Database design | Vector DB schema design, metadata indexing, trace storage, audit logs require SQL/NoSQL fluency |
| Distributed systems | LLM serving, request queuing, horizontal scaling — same fundamentals, different workloads |
| Testing & CI/CD | Eval pipelines are just CI/CD for model quality — you already know the pattern |
| Debugging production issues | LLM systems have non-deterministic bugs; strong debugging instincts are rare and valuable |
| Code review & code quality | Prompt engineering is code; it needs versioning, review, and regression testing |
| Cost consciousness | Token costs are line items; SWEs who've dealt with infra costs understand the trade-offs |

### What to Avoid Saying

| ❌ Don't say | ✅ Say instead |
|---|---|
| "I'm really passionate about AI" | "I built [specific thing] and here's what I learned" |
| "I've been learning AI recently" | "I've been applying AI engineering practices for [timeframe]" |
| "I read a lot about LLMs" | "I implemented [pattern] and ran into [specific problem]" |
| "I want to transition into AI" | "I've already been doing AI engineering work; I'm looking for the right team" |

---

## Part 2 — AI-Specific Behavioral Questions

### Q1: "Tell me about a time you built something with LLMs."

**If you have a project (best case):**
Use STAR format. The ideal story structure:
- **Situation:** What problem were you solving? For whom? At what scale?
- **Task:** What were your specific responsibilities?
- **Action:** Walk through your technical decisions — why RAG vs fine-tuning, how you handled latency, what eval you ran
- **Result:** What was the measurable outcome? (cost reduction, quality improvement, latency improvement)

**The "I built the mini-project" answer:**
> *"I built a RAG pipeline over [domain] documentation. I used hybrid BM25 + dense retrieval with a cross-encoder reranker, routed queries by complexity to GPT-4o-mini vs GPT-4o, and implemented semantic caching. I ran an LLM-as-judge eval on a 200-question golden set and got 78% faithfulness. The most interesting problem was calibrating the cache cosine threshold — at 0.90 I was getting false hits on semantically similar but factually different questions, so I raised it to 0.93."*

**If you don't have a project yet:** → Build the project first (see Part 3).

---

### Q2: "How do you handle non-deterministic system behavior?"

**Weak answer:** "You test it more / run it multiple times."

**Strong answer:**
> *"Non-determinism in LLM systems operates at two levels. At the generation level: same prompt + temperature > 0 → different outputs. I treat this like flaky tests — use temperature=0 for deterministic critical paths, set seeds where available, and accept and measure variance where temperature is intentional. At the system level: retrieval, tool calls, and context assembly can all produce different results. I manage this with: (1) deterministic artifact versioning so I know exactly what inputs the model received, (2) eval suites that measure output distributions rather than exact strings, and (3) drift detection that alerts when the distribution shifts beyond a threshold. Non-determinism isn't a bug — it's a property you design around."*

---

### Q3: "How did you measure success for an AI feature?"

**Weak answer:** "We tracked accuracy."

**Strong answer (3-layer model):**
> *"I use three layers of metrics: model metrics, product metrics, and business metrics — and the gap between them is where most AI features fail.*
>
> *Model metrics (LLM-as-judge, task success rate on golden set, faithfulness) tell you if the model is doing what you intended. Product metrics (session length, return rate, escalation rate for a chatbot) tell you if users are getting value. Business metrics (ticket deflection rate, conversion, support cost/ticket) tell you if it's working for the company.*
>
> *I've seen features that had great model metrics but terrible product metrics — the model answered correctly but users didn't trust the answers because the UI showed no citation. Measuring all three layers early prevents that gap."*

---

### Q4: "A model upgrade passes benchmarks but regresses in production. What do you do?"

**Strong answer:**
> *"First, I'd pause the promotion and keep the old model live — the benchmark improvement is a hypothesis, not a fact. Then I'd segment the failing production traces by: intent class, query language, context length band, and user tier. Regressions are almost always concentrated in a segment, not uniformly distributed — global averages hide this. Once I identify the failing segment, I'd build a domain-specific golden set from those production traces and run both models on it. If the old model wins on this set, I go back to the model team with evidence: 'Your model improves on your benchmark distribution but regresses 12% on our legal document queries.' I'd also check if the benchmark itself is contaminated — if the training data included benchmark questions, the improvement is meaningless. I'd promote only when the new model meets or exceeds the old model on the private golden set AND on product-analytics metrics like task completion rate."*

---

### Q5: "How do you decide when to use RAG vs fine-tuning?"

**The decision tree answer:**
> *"I use a decision tree. First: is the knowledge private, real-time, or frequently updated? If yes → RAG. Fine-tuning can't update knowledge without a new training run, and it encodes behavior, not facts.*
>
> *Second: do I need strict output format/style enforcement? If yes, and I have 1K+ high-quality examples, fine-tuning is better — a model can be fine-tuned to consistently produce structured JSON or follow a brand voice in a way prompting alone can't guarantee.*
>
> *Third: cost sensitivity. Fine-tuning a small model (7B) and running it yourself is 20-50× cheaper per token than calling a frontier API — worth it for high-volume predictable tasks.*
>
> *In practice, most production systems use both: RAG for knowledge grounding + fine-tuned small models for formatting and routing. The common mistake is treating them as alternatives rather than complements."*

---

### Q6: "Tell me about a time you reduced infrastructure costs."

**Frame SWE experience as transferable:**
> *"In my SWE2 role, I [specific cost reduction story from your work]. The same principles apply to LLM cost optimization, which I've studied in depth: semantic caching (40% hit rate reduces API calls by 40%), model routing (80% of queries go to GPT-4o-mini at $0.00015/1K vs GPT-4o at $0.005/1K — 33× cheaper), prompt compression (30-50% fewer input tokens), and quantized self-hosted models for high-volume predictable workloads. I'd apply the same mindset: measure first, find the 80/20, instrument to verify."*

---

### Q7: "Where do you see AI engineering in 3 years?"

**Show you've thought about this:**
> *"The role is converging on three specializations: AI Infrastructure (the platform layer — serving, evals, LLMOps), AI Product Engineering (building application-layer RAG/agent systems), and AI Safety/Evaluation (the eval, red-teaming, and governance layer). I expect the tooling to mature significantly — today you hand-roll most eval pipelines; in 3 years there will be standard evaluation frameworks the way there are standard CI/CD platforms today. The role that survives commoditization is the one that understands the full stack — from transformer internals to product metrics — because that's what lets you make the right architectural trade-offs when the defaults don't work."*

---

## Part 3 — Portfolio Project Blueprint

### The Minimum Viable Project (2-weekend build)

**What to build:** A RAG pipeline over a real dataset with observability, evals, and cost tracking.

**Why this specific project:** It touches every interview topic — retrieval, serving, evals, cost, observability, safety — and can be demoed in a 5-minute screen share.

### Weekend 1: Core Pipeline

```
Day 1 (4 hours):
  □ Pick a dataset: arXiv papers in your domain, Hacker News posts,
    Wikipedia dumps, or docs from a tool you use
  □ Build ingestion: parse → chunk (sliding window, 400 tokens, 80 overlap)
  □ Embed with text-embedding-3-small ($0.02/1M tokens — very cheap)
  □ Store in ChromaDB (local, free) or Pinecone (free tier)
  □ Basic retrieval: top-5 chunks by cosine similarity

Day 2 (4 hours):
  □ Add BM25 retrieval (use rank_bm25 library)
  □ Implement RRF fusion (15 lines of code — see ml-coding-patterns.md)
  □ Add a reranker (Cohere Rerank API or cross-encoder from HuggingFace)
  □ Build the generation layer: retrieved context → GPT-4o-mini → answer
  □ Add streaming response with TTFT logging
```

### Weekend 2: Observability + Evals + Cost

```
Day 3 (4 hours):
  □ Build a structured trace logger:
    {request_id, query, retrieved_chunk_ids, model, prompt_tokens,
     completion_tokens, cost_usd, ttft_ms, total_ms, timestamp}
  □ Add semantic caching (see ml-coding-patterns.md Pattern 6)
  □ Add model routing: short/simple queries → GPT-4o-mini, rest → GPT-4o
  □ Build a simple cost dashboard: plot cost/request over time, cache hit rate

Day 4 (4 hours):
  □ Create a 50-question golden set (write questions, expected answers)
  □ Implement LLM-as-judge eval loop (see ml-coding-patterns.md Pattern 7)
  □ Run eval on: (a) your system, (b) naive no-retrieval baseline
  □ Record results: faithfulness score, task success rate, avg cost/query
  □ Write a README with: architecture diagram, eval results, cost breakdown
```

### What you'll be able to say

After building this, you own the story:

> *"I built a hybrid RAG pipeline over [N] documents. Hybrid retrieval (BM25 + dense + RRF fusion) improved Recall@5 by 18% over dense-only on my golden set. I added a semantic cache with a 0.93 cosine threshold that achieved a 35% hit rate on repeated question patterns, bringing avg cost/query from $0.018 to $0.012. I ran an LLM-as-judge eval (faithfulness + correctness + completeness) on 50 golden questions and got 74% pass rate, compared to 41% for a no-retrieval baseline. The most interesting failure: the cache was returning stale answers after I updated the corpus — I fixed it by tagging cache entries with source IDs and invalidating on document update."*

That answer is interview gold. It has: concrete numbers, a failure you debugged, and a production-grade fix.

---

## Part 4 — Tools to Know (Practical Literacy)

### Must Know (will be asked about)

| Tool | What It Is | Learn By |
|---|---|---|
| `openai` Python SDK | Official OpenAI client | [openai.com/docs](https://platform.openai.com/docs) |
| `tiktoken` | OpenAI's tokenizer | `pip install tiktoken` |
| `chromadb` | Local vector DB | Build the project |
| `rank_bm25` | BM25 retrieval | `pip install rank_bm25` |
| `sentence-transformers` | Embedding models (HuggingFace) | Build the project |
| `langchain` | LLM application framework | Know the concepts, not just the API |
| `ragas` | RAG evaluation metrics | `pip install ragas` |

### Should Know (bonus points)

| Tool | What It Is |
|---|---|
| `vllm` | High-throughput LLM serving |
| `llama.cpp` | CPU/edge inference for GGUF models |
| `instructor` | Structured output extraction |
| `litellm` | Unified API for multiple LLM providers |
| Weights & Biases | Experiment + eval tracking |
| MLflow | Model registry, experiment tracking |

---

## Part 5 — The 30-Day Pre-Interview Plan

```
Week 1 — Foundation
  □ Read: chapters 1, 2, 3, 4, 5 (lean versions)
  □ Do: ml-coding-patterns.md patterns 1-5 from memory
  □ Watch: "Attention is All You Need" paper walkthrough (Yannic Kilcher, YouTube)
  □ Build: Weekend 1 of the portfolio project

Week 2 — Production Systems
  □ Read: chapters 24, 27, 28, 29 (LLMOps + ops chapters)
  □ Do: ml-coding-patterns.md patterns 6-13 from memory
  □ Read: transformer-internals.md
  □ Build: Weekend 2 of the portfolio project

Week 3 — Interview Practice
  □ Drill: 20 questions from drill-questions.md cold
  □ Mock: 2 full mock interviews (mock-interview.md Tier 1 + Tier 2)
  □ Review: anki-numbers.md — cover answers, say numbers aloud
  □ Write: The project README with architecture, results, and lessons learned

Week 4 — Polish
  □ Mock: 2 Tier 3 mock interviews (LLMOps + observability)
  □ Re-drill: all ❌ questions from Week 3 drill session
  □ Practice: behavioral answers (Part 2 of this guide) out loud
  □ Final review: cheat-sheet.md + glossary.md
```

---

## Quick Reference: AI Engineer Interview Types

| Round Type | What They Test | How to Prepare |
|---|---|---|
| **ML Coding** | Implement cosine sim, attention, BM25, eval loop | ml-coding-patterns.md + practice daily |
| **LLM System Design** | RAG architecture, LLMOps, cost, observability | Chapters + mock-interview.md |
| **ML Theory** | Transformer internals, quantization, KV cache | transformer-internals.md |
| **Behavioral** | Have you actually built AI things? | Portfolio project + transition-guide.md Part 2 |
| **Take-home** | Often a real RAG or eval task | Portfolio project gives you the patterns |
| **Domain knowledge** | LLM-specific: RLHF, fine-tuning, alignment | Chapters 25, 26 |
