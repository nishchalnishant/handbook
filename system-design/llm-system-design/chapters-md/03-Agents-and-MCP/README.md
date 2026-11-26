# 03 - Agents and MCP

This folder covers agentic LLM systems: autonomous agents that plan and act over multiple steps, agents grounded against structured backends (SQL warehouses, game world state), multiple agents coordinating on one workflow, and the protocol/platform layer (MCP) that lets agents call external tools safely. The common thread across all five case studies is **untrusted autonomy**: an LLM is given the ability to take multi-step actions or call external systems, and every chapter's core design problem is bounding that autonomy — via budgets, sandboxes, approval gates, validators, or trust tiers — so the system stays correct, safe, and cost-bounded when the model is wrong, stuck, or adversarially manipulated.

---

## Chapter 9 — Design an Autonomous Research Agent

**Problem:** Build an agent that autonomously plans, searches, and synthesizes multi-step research tasks within bounded cost/time, without hallucinating sources or looping forever.

**Core pattern — Planner-executor with Plan-then-ReAct:**
- **Planner LLM** decomposes the task into a step plan up front; **Executor Loop** runs ReAct-style (Reason→Act→Observe) per step against the plan, replanning only when a step fails.
- **Tool Registry** + **Tool Sandbox** (gVisor) execute untrusted tool calls (search, code exec, browsing) in an isolated, network/filesystem-restricted environment.
- **Loop Detector** uses 5 signals: repeated tool calls, semantic state similarity (embeddings), non-progressing step counts, action oscillation, token velocity.
- **Budget Controller** enforces a hierarchy: token budget, step budget, cost budget, wall-clock budget, per-sub-task budget — with soft (80%) and hard (100%) thresholds.
- **State Manager** (Redis + AOF persistence) makes tasks resumable; **Synthesizer LLM** produces the final grounded answer with citation verification; **Observability** gives per-step tracing and cost attribution.

**Pros:**
- Plan-then-ReAct avoids the cost of full replanning on every step while still allowing local recovery from failures.
- Multi-signal loop detection catches stuck agents that a single heuristic (e.g., just repeated-call counting) would miss.
- gVisor sandboxing contains the blast radius of arbitrary tool/code execution.
- Hierarchical budgets (soft/hard thresholds) let the system degrade gracefully (early termination) instead of hard-failing mid-task.

**Cons / failure modes:**
- Loop detection and budget tracking add engineering surface area (state management, embeddings for semantic similarity) beyond a naive ReAct loop.
- Citation grounding is necessary because synthesis models hallucinate sources when not explicitly constrained.
- Resumability requires durable state (Redis AOF) — added operational cost/complexity vs. a stateless agent.

**When to use:** Open-ended, multi-step research/investigation tasks where the step sequence can't be fully enumerated upfront. Not needed for single-shot Q&A or fully deterministic workflows (see Ch. 22's DAG pattern for those).

---

## Chapter 16 — Design an AI Data Analyst (Text-to-SQL and Insights)

**Problem:** Translate natural-language questions into safe, executable SQL over enterprise warehouses (400+ tables), with autonomous repair of failed queries, at <$0.05/query and p95 <3s (simple) / <8s (complex).

**Core pattern — Text-to-SQL agent with self-healing:**
- **Schema Selector**: embedding search (top-20) → cross-encoder rerank (top-5-10) → 1-hop FK expansion → column pruning. Compresses a 400-table/~40K-token schema into a ~2K-token budget.
- **Prompt Assembler** builds prompt from compressed DDL + dynamically retrieved few-shot examples + conversation history, truncating history first under budget pressure.
- **SQL Validator** (AST-based, pre-execution) catches ~40% of errors before any DB round-trip.
- **Sandbox Executor**: read-only replica, `SELECT`-only grants, 30s `statement_timeout`, `LIMIT 1000` injection, `EXPLAIN`-based cost check rejecting scans >500GB, per-tenant connection pools (max 5).
- **Self-Healing Engine**: classifies failures into 7 error types (column not found 35%, syntax error 20%, type mismatch 15%, table not found 10%, ambiguous column 8%, timeout 7%, permission denied 3%) and applies class-specific repair prompts, bounded to 2 retries (3 total attempts).
- **Result Formatter/Conversation Manager**: auto chart-type detection, NL summaries, 3-turn sliding window for follow-ups.

**Pros:**
- Embedding-based schema selection lifted execution success from 62% → 87% in the cited real-world example (BI platform case).
- Error-class-specific repair hits ~80% first-retry recovery vs. ~15% for blind retry, ~55% for raw error-message injection, ~72% for class-hint-only repair.
- Layered sandbox controls (AST rejection, EXPLAIN cost check, timeout, row limit, PII masking) give defense-in-depth against SQL injection and runaway cost — a single uncapped BigQuery query can otherwise process 10TB ($50/query).
- Result-sanity-check layer (cardinality, null dominance, order-of-magnitude vs. baseline) catches 94% of syntactically-valid-but-semantically-wrong queries — directly addressed a real incident where a bad JOIN inflated revenue numbers undetected for 3 weeks.

**Cons / failure modes:**
- Multi-candidate generation (3 parallel SQLs, pick first passing) reaches ~88% recovery but costs 3x tokens (~$0.126) — only justified for complex (2+ join) queries.
- EXPLAIN-based cost estimation adds 200-500ms latency and 5-10% false-positive over-estimates on indexed queries.
- Retry budget still costs ~$0.008 avg overhead per query at a 20% retry rate; ambiguous questions ("show me everything about customers") can trigger wasted 3x attempts if not pre-classified.
- Schema drift (renamed/dropped tables) causes "table not found" errors between 6-hour ingestion crawls unless DDL webhooks are wired up.

**When to use:** Interactive analytics over large, evolving warehouse schemas where full schema-in-context is infeasible. LLM-based schema selection (~90%+ precision) is only viable for async/batch queries since it doubles latency (2000ms+).

---

## Chapter 19 — Design an AI NPC Engine for Multiplayer Games

**Problem:** Deliver personality-consistent, lore-grounded NPC dialogue at p95 <500ms across 500K CCU / 75K concurrent dialogue sessions, with persistent cross-session memory and near-zero lore contradictions.

**Core pattern — Per-NPC memory + persona system with tiered edge serving:**
- **Three-tier memory:** short-term ring buffer (8KB, ~12 turns, session-scoped), long-term episodic store (16KB/pair, Redis+DynamoDB, vector-similarity retrieval, importance-weighted LRU eviction), world state (event-bus driven, unbounded but context-capped).
- **4-layer persona consistency enforcement:** system-prompt instructions (~85% catch, 0ms cost) → constrained decoding/logit banning (~95%, +2ms/token) → post-generation classifier (100M DistilBERT-class, ~98%, +40ms) → lore retrieval grounding (~92%, pre-computed per archetype). Combined: **~99.96%** violation detection (0.04% slip rate).
- **2-tier model routing:** 3B model for Tier-1 (important) NPCs (~40% of interactions), 1.5B for Tier-2 ambient NPCs (~60%) — 35% fleet cost reduction vs. all-3B.
- Speculative decoding (300M draft model, K=6) achieves 88-92% acceptance on NPC dialogue (vs. 75-85% general text), 3.5-4x decode speedup.
- Prefix KV cache per archetype (200 archetypes × ~2MB) eliminates ~200 tokens of prefill per request (~20ms savings).
- Edge deployment (6 regions, 150 GPUs) with mandatory scripted-dialogue fallback on model failure, latency SLO breach, or contradiction-detection trigger.

**Pros:**
- Real-world example: lore-grounding layer dropped lore violations from 2.3% → 0.04%, avoiding a repeat of a viral Twitch-driven 40K-refund incident.
- Persistent per-player-NPC memory increased engagement 35% and average session length by 22 minutes in the cited case.
- Priority-aware continuous batching lets Tier-1 (narrative-critical) NPCs hold their latency SLO even under GPU saturation, degrading only Tier-2 to scripted fallback.
- Anti-correlated GPU sharing between game-AI (physics/pathfinding) and dialogue workloads saves 20-30% via MPS/time-slicing.

**Cons / failure modes:**
- Importance-weighted LRU requires a reliable importance scorer — miscalibration can permanently protect trivial memories while evicting important ones.
- Persona drift over long conversations (10+ turns) requires re-injecting persona constraints every 4 turns as a mitigation.
- Speculative decoding acceptance rate drops to ~40% on novel/obscure lore topics, doubling decode latency until fallback to standard decoding kicks in.
- Edge deployment (vs. centralized) carries a 25-35% cost premium and multiplies operational complexity (6 regions × monitoring/rollout).
- Cross-tool trust issue analog: NPCs must never confirm unverified player claims as canonical fact (game server is always the source of truth) — a "skeptical but open" response pattern is required to avoid exploitable lore contradictions.

**When to use:** Real-time, persona-bound interactive dialogue at massive concurrency where latency SLOs (sub-500ms) rule out large models and full centralized serving. Full LLM-based schema/lore reasoning or 70B-class models are reserved for offline content generation, not the real-time path.

---

## Chapter 22 — Design a Multi-Agent Workflow Orchestrator

**Problem:** Coordinate multiple specialized agents (e.g., log analysis, code editing, testing, security review) on complex enterprise workflows (incident response, code migration, compliance review) without agents overwriting each other's work or burning unbounded tool calls.

**Core pattern — Supervisor-worker orchestration with DAG scheduling, typed handoffs, and approval gates:**
- **Supervisor Agent** decomposes goals, arbitrates conflicts, decides completion/replanning; **Planner** emits a typed DAG (task IDs, dependencies, per-task budgets, allowed tools, output schemas) validated before execution.
- **DAG Scheduler** dispatches ready tasks, runs independent tasks in parallel (parallelism cuts wall time 40-60% in a 12-step/6-independent-step example), handles retries with exponential backoff.
- **Shared State Store**: versioned, append-only, optimistic-locking artifact store — agents hand off **typed artifacts** (with confidence score, evidence IDs, schema version), not free-form chat transcripts.
- **Tool Gateway**: enforcement point validating args against JSON Schema, permission list, rate limits, timeouts — least-privilege tool scoping per agent role.
- **Evaluator/Critic Agent** checks artifacts against a rubric (schema compliance, confidence threshold, evidence coverage) before acceptance; conflicting artifacts route to critic then supervisor arbitration then human review if unresolved (confidence threshold e.g. 0.75/0.8).
- **Approval Service**: pauses workflow at `PENDING_APPROVAL` for any production-changing, external-communication, or money-movement action.
- **Trace Store**: full replayable timeline (dispatch, model calls, tool calls, artifacts, approvals) for audit and regression bisection.

**Pros:**
- Supervisor-worker gives a single component clear authority to arbitrate/replan/approve — ownership is always unambiguous, unlike blackboard (overwrite risk) or swarm (unauditable) patterns.
- Structural (not prompt-based) budget enforcement — step counter, per-tool rate limit (e.g., 20 calls/task), workflow dollar meter — cannot be bypassed by a hallucinating/stuck model; loops account for ~15-20% of budget overruns in early production deployments, motivating this design.
- Typed artifacts + optimistic locking (version N→N+1) prevent silent overwrites in concurrent workflows, and append-only "superseded" versioning preserves full audit history.
- Full resumability (persisted state, `WAITING_EXTERNAL` status, no in-memory workflow state) supports multi-day workflows waiting on external events (e.g., 3-day code review timeout, 30-day regulatory approval timeout) at zero idle compute cost.

**Cons / failure modes:**
- Debate/consensus multi-agent patterns cost roughly (N+0.5)x a single agent (3-5x for a 3-agent debate) — justified only for high-stakes, low-frequency decisions.
- Supervisor is a throughput bottleneck: a single-threaded supervisor with 500ms LLM round-trips sustains only ~2 workflows/sec without decomposition (mitigated by separating judgment-heavy arbitration from mechanical status aggregation, or hierarchical sub-workflow supervisors).
- DAG pattern's plan is fixed at creation — an unexpected mid-workflow finding requires a full replan/restart.
- Approval latency directly inflates workflow wall time; mitigated by batching homogeneous low-risk approvals with structured diffs (goal: approver decision in <60s).
- Swarm pattern explicitly called out as rarely appropriate in production due to runaway spawning risk exhausting budgets within minutes.

**When to use:** Enterprise workflows needing correctness/auditability over raw throughput, with knowable-upfront task graphs (code migration, compliance review, reporting). Blackboard pattern is preferred instead for open-ended research/threat-hunting where the task list can't be enumerated in advance; debate/consensus only for rare high-stakes sign-offs.

---

## Chapter 23 — Design an MCP-Based Tool Integration Platform

**Problem:** Let AI applications connect to internal/third-party tools via Model Context Protocol at enterprise scale (50K users, 2K MCP servers, 100K tool calls/hour, 10x bursts) while preventing prompt injection, confused-deputy attacks, and data exfiltration.

**Core pattern — MCP host-client-server architecture with a governance control plane on top:**
- **MCP Host** owns conversation/model calls/approval UX; **MCP Client Manager** manages per-server sessions and capability discovery; **Server Registry** tracks approved servers, versions, trust tier.
- Six MCP primitives, each a distinct trust boundary: **Tools** (actions, need risk classification + approval), **Resources** (context data, must be treated as untrusted/injectable), **Prompts** (server-supplied templates, supply-chain risk), **Roots** (filesystem/workspace boundaries, host-enforced not server-trusted), **Sampling** (server-initiated callback into the model, needs recursion depth limits), **Elicitation** (server-initiated user input request, credentials must route to credential service not model context).
- **Trust tiers** (Internal Verified, Internal Sensitive, Third-party Verified, User Local, Experimental) set default policy at server-registration time rather than per-call reasoning; **Policy Engine** + **Tool Gateway** enforce risk-scored approval (read-only auto-approved → external-write requires two confirmations, rate-limited to 1/min).
- **Sanitizer** strips hidden instructions/secrets from tool/resource results before model context; **Audit and Trace Store** is append-only/tamper-evident (hash chain) recording sanitizer input/output, model context snapshot, and approval payloads.

**Pros:**
- Intent-bound, per-call approvals (with session-scoped nonce) prevent confused-deputy reuse of a broad-scope approval for an unintended action.
- Cross-tool taint tracking (low/high/critical taint persisting across the session) blocks a legitimate-looking read-then-exfiltrate chain even when each individual tool call is separately permitted — stronger than filtering tool results alone.
- Trust-tier assignment at registration is far cheaper than reasoning about risk at every tool call, and lets operators inherit sensible per-tier defaults.
- Hierarchical, per-user-filtered discovery (8-12 enabled servers cached in Redis, ~4,000-token manifest) avoids the ~1M-token infeasibility of loading all 2,000 servers' capabilities into context.
- Canary-based server versioning (concurrent old/new versions, 24h in-flight session grace period) prevents schema-breaking upgrades from silently breaking live agent workflows.

**Cons / failure modes:**
- Schema-valid-but-semantically-misleading tool responses (e.g., a server falsely reporting zero test failures) bypass syntactic validation entirely — requires behavioral anomaly detection, cross-server consistency checks, and evidence-grounding as additional layers, none of which schema validation alone provides.
- Approval fatigue: users who get prompted for every low-risk repeated action learn to approve reflexively — mitigated by session-scoped approval aggregation (30-min window) plus escalated friction (typed confirmation string) for destructive actions.
- Cold MCP server discovery adds 50-200ms per server per session — 400-1,600ms cold-start penalty at 8 servers/user if uncached.
- Noisy tool results (e.g., a 50,000-token CI log) can consume most of the context window and increase cost ~10x per call unless clipped (default 2,000-token budget) and optionally summarized.
- Credential leakage risk if tokens are passed directly to MCP servers rather than kept behind a credential service issuing scoped session identifiers.

**When to use:** Any enterprise deployment connecting LLM agents to multiple internal/third-party systems where governance (auth, approval, audit) must be separated from the protocol itself — MCP "solves the integration shape, not the governance problem." Not a substitute for function calling; production systems compose both (function calling selects the tool, MCP handles the protocol session/auth/transport).

---

## Cross-Cutting Themes

- **Structural budget/loop enforcement, never prompt-based.** Ch. 9 (multi-signal loop detector + token/step/cost/wall-clock budget hierarchy with soft/hard thresholds), Ch. 16 (max 2 retries / 3 attempts, circuit-breaker at >50% tenant failure rate), and Ch. 22 (explicit statement: "prompt-based budget instructions... are ignored... cannot be trusted as a safety mechanism," enforcing step counters, per-tool rate limits, and dollar meters at the gateway/scheduler) all converge on the same principle: agents cannot be trusted to self-limit, so limits must live in infrastructure code.

- **Sandboxed/isolated execution of untrusted actions.** Ch. 9 (gVisor sandbox for tool/code execution), Ch. 16 (read-only replica, SELECT-only grants, statement timeout, cost-based query rejection), and Ch. 23 (network egress controls on MCP servers, roots-based filesystem boundaries) all treat agent-initiated execution as inherently untrusted and isolate its blast radius.

- **Human approval gates keyed to action reversibility/risk class.** Ch. 22's approval taxonomy (read-only → no approval; external-write/money movement → mandatory approval) and Ch. 23's identical risk tiering (read-only metadata → auto; external-write/critical → two confirmations, rate-limited) both gate approval on the same axis: reversibility and blast radius, not just "is this a write."

- **Typed, schema-validated state instead of free-form text.** Ch. 22's typed artifacts (confidence, evidence IDs, schema version) for agent handoffs and Ch. 16's SQL Validator (AST-based schema/column existence checks) both replace trust-the-model's-output with machine-checkable structure before anything downstream consumes it.

- **Error/failure classification driving targeted repair, not blind retry.** Ch. 16's 7-class SQL error taxonomy with class-specific repair prompts (blind retry ~15% recovery vs. targeted ~80%) and Ch. 22's `RETRYABLE` vs. `TERMINAL` tool-error classification at the gateway both reject undifferentiated retry in favor of diagnosing the failure mode first.

- **Confidence thresholds as hard gates on downstream/sensitive consumption.** Ch. 22 (artifacts below a confidence threshold must never feed an approval gate for a sensitive action) and Ch. 16 (result-validation heuristics — cardinality, null dominance, order-of-magnitude checks — catching 94% of semantically wrong but syntactically valid queries) both treat low-confidence or anomalous output as something that must be caught before it reaches a human or a downstream system, not silently passed along.

- **Full auditability via append-only, replayable traces.** Ch. 22's Trace Store (replay workflows against fixed artifacts to bisect regressions) and Ch. 23's tamper-evident audit store (hash chain, logging sanitizer input/output and full model context snapshots) both exist to answer "what exactly did the system see and do," a requirement driven by compliance and incident response in both chapters.

- **Orchestrator/supervisor-worker as the dominant multi-step coordination shape.** Ch. 9's planner-executor loop, Ch. 22's supervisor-worker-plus-DAG default, and Ch. 23's host-client-server split (host owns judgment/approval, servers are scoped workers) all separate a coordinating/decision-making layer from bounded, scoped execution units — rejecting flatter alternatives (blind loops, blackboards, swarms) as harder to audit or bound in production.
