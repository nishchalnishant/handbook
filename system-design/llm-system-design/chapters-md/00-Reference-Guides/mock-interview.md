---
title: "Mock Interview Template — LLM System Design"
tags: [llm, interview-prep, mock-interview, practice]
---

# LLM System Design — Mock Interview Template

> [!important] Rules of the exercise
> 1. **Pick a prompt below** (or have someone pick for you)
> 2. **Set a 35-minute timer** — that's a real interview slot
> 3. **Talk out loud** (or write on paper) — do NOT read chapter notes
> 4. After the timer: open the relevant chapter, score yourself with the rubric at the bottom
> 5. Rotate prompts — aim to do one per day during prep week

---

## Design Prompts

### Tier 1 — Foundations (aim to ace these)

**P1.** Design a customer support chatbot for an e-commerce company handling 100K conversations/day.

**P2.** Design an enterprise semantic search engine over 500K internal documents with access control.

**P3.** Design an AI coding assistant for an IDE plugin — target sub-100ms inline completions.

**P4.** Design an LLM serving platform that handles 10K QPS with mixed model tiers.

---

### Tier 2 — System Complexity (mid-level AI engineer)

**P5.** Design an autonomous research agent that decomposes complex questions, calls external APIs, and synthesizes citations — with guardrails against infinite loops and runaway costs.

**P6.** Design a production RAG platform for a legal firm: 200K contracts, strict citation grounding, multi-tenant ACL, < 2s TTFT.

**P7.** Design a multi-agent workflow orchestrator for a financial services company — the orchestrator dispatches sub-agents, handles failures, and produces an audit trail.

**P8.** Design a healthcare triage assistant — detects red-flag symptoms, PHI-compliant, integrates with EHR, deployed in a hospital system (HIPAA).

---

### Tier 3 — LLMOps & Production (senior AI engineer)

**P9.** Design the LLMOps platform for an organization with 50 product teams shipping 200 prompt/model changes per week.

**P10.** Design the cost optimization strategy for an LLM platform at 1B requests/month — current monthly bill is $2M, target is $800K.

**P11.** Design a full observability and incident response system for an LLM product serving 500K daily active users.

**P12.** Design a privacy and compliance layer for an LLM system that must satisfy GDPR, HIPAA, and SOC 2 — including right-to-deletion and audit evidence generation.

---

## Answer Framework (use this structure every time)

```
[ Step 1 — Scope ] 5 min
  □ Who are the users? What are they trying to do?
  □ Functional requirements (3–5 bullet points)
  □ Non-functional requirements: latency (TTFT/TPOT), scale (QPS/users), cost, safety
  □ Out of scope: what you're NOT designing today

[ Step 2 — Estimate ] 5 min
  □ Daily users → requests/day → peak QPS (assume 12× avg)
  □ Token budget per request (input + output)
  □ Daily token volume → monthly API cost (or GPU count)
  □ Storage: documents × avg_size → GB/TB
  □ Latency target → which model tier is feasible?

[ Step 3 — High-Level Design ] 10 min
  □ Draw the system: user → gateway → components → storage
  □ Name every component and its role
  □ Highlight the critical path (what happens on every request)
  □ Choose your pattern: RAG / fine-tune / prompt-chain / agentic — justify the choice

[ Step 4 — Deep Dives ] 10 min
  □ Pick 2 hard problems: interviewer usually has a hint in the prompt
  □ Common targets: latency bottleneck, cost, safety/guardrails, freshness, consistency, scale
  □ Show trade-offs: approach A vs B, when each wins
  □ State specific thresholds (chunk size, cache hit rate, canary %, judge kappa, etc.)

[ Step 5 — Failure Modes & Curveballs ] 5 min
  □ What happens when the model goes down?
  □ What happens when the data is stale/wrong?
  □ What is the rollback strategy?
  □ How do you detect silent quality regression?
  □ What does the audit/compliance story look like?
```

---

## Self-Scoring Rubric

After your mock, score each dimension 1–4:

| Dimension | 1 — Missed | 2 — Partial | 3 — Solid | 4 — Strong |
|---|---|---|---|---|
| **Scoping** | No requirements listed | Functional only | F + NF requirements | F + NF + out-of-scope, justified |
| **Estimation** | No numbers | Order-of-magnitude only | Token cost + storage | Full BotE: QPS, tokens, GPU, storage, cost |
| **Architecture** | Missing major components | All components named | Components + data flow | Components + data flow + failure modes |
| **Pattern choice** | No justification | "I'd use RAG" | RAG vs alternatives considered | Decision tree applied, trade-offs explicit |
| **Deep dive** | Surface level | 1 hard problem addressed | 2 hard problems with trade-offs | Specific thresholds + production numbers cited |
| **Curveballs** | Stumped | Vague answers | Reasonable approaches | Specific rollback/debug steps with metrics |

**Score guide:** 20–24 = strong hire | 14–19 = yes with gaps | 8–13 = needs prep | < 8 = go back to chapters

---

## Mini-Prompts for Daily Warm-Up (5 minutes each)

Use these to stay sharp between full mock sessions:

1. "Explain continuous batching in one minute. How does it improve GPU utilization?"
2. "You just deployed a prompt change and TTFT jumped 300ms at p95. Walk me through your debug steps."
3. "What's the difference between LLMOps and MLOps? Give me 3 concrete differences."
4. "A new 70B model scores 8% better on our benchmark but costs 3× more. How do you decide whether to upgrade?"
5. "How do you handle a GDPR deletion request when the user's data is embedded in a vector index?"
6. "Walk me through the minimum viable audit trace for a medical LLM system."
7. "What is speculative decoding? When does it help and when does it not?"
8. "An agent calls the same tool 5 times in a row. What's your loop detection and abort strategy?"
9. "How do you A/B test a new retrieval model without exposing users to degraded quality?"
10. "Your semantic cache is returning stale answers after a policy update. What went wrong and how do you fix it?"

---

## Chapter Cross-Reference

| Prompt | Primary Chapters | Deep Dive Focus |
|---|---|---|
| P1 Customer Support | Ch 6, 2, 3, 5 | Escalation logic, freshness, semantic cache |
| P2 Semantic Search | Ch 7, 3, 4 | Hybrid retrieval, reranking, ACL |
| P3 Coding Assistant | Ch 8, 4 | FIM, speculative decoding, local model |
| P4 Serving Platform | Ch 4, 2 | Continuous batching, model tiers, cost |
| P5 Research Agent | Ch 9, 22, 5 | Loop detection, cost budget, safety |
| P6 Legal RAG | Ch 21, 3, 17 | Citation grounding, ACL, chunking |
| P7 Multi-Agent | Ch 22, 23, 24 | Supervisor bottleneck, tool versioning, audit |
| P8 Healthcare Triage | Ch 20, 5, 30 | PHI, red-flags, compliance, EHR integration |
| P9 LLMOps Platform | Ch 24, 27, 28 | Artifact versioning, eval gates, rollback |
| P10 Cost Optimization | Ch 28, 4, 2 | Cache, routing, quantization, prompt compression |
| P11 Observability | Ch 29, 24 | Span tracing, drift detection, incident response |
| P12 Privacy/Compliance | Ch 30, 5, 20 | GDPR deletion, ACL retrieval, audit retention |
