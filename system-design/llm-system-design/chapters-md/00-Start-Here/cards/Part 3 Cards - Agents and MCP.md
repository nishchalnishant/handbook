---
title: "Part 3 Cards — Agents and MCP (Ch 9, 16, 19, 22, 23)"
tags: [cards, agents, mcp]
---

# Part 3 Cards — Agents and MCP

Every card here is **P7 (bounded agent loop)** plus a security story. The questions interviewers come back to: *How do you stop it looping? How do you stop it doing damage? How do you know it worked?*

| Ch | The twist |
|---|---|
| 9 | Plan → search → read → synthesize, with citations |
| 16 | The LLM writes code (SQL) that touches real data |
| 19 | Persistent memory and persona at game scale/latency |
| 22 | Many agents: handoffs, shared state, conflicts |
| 23 | The tool layer itself, as a platform |

---

### Ch 9 — Design an Autonomous Research Agent
**One line:** Given a question, plan the research, search and read sources, then write a cited report, inside a budget.
**Shape:** Planner → [ReAct worker: search → fetch → extract → note] × N → Synthesizer → Citation verify → Report
**Patterns:** P2, P7, P8

**3 ideas**
1. **Planner–executor split:** a strong model plans sub-questions, and cheaper workers execute them. Re-plan only at checkpoints.
2. **Tools are sandboxed and typed.** Fetched web content is untrusted data, never instructions.
3. **Loop detection + hard budgets:** max steps, tokens, $ and wall-clock are enforced by the runtime. Repeated (tool, args) hashes trip the breaker.

**2 trade-offs**
- Depth (more sources, better report) vs cost and latency. Expose a "depth" knob.
- Parallel workers (fast) vs sequential (each step informs the next). Parallelize independent sub-questions.

**Numbers:** Budgets are explicit, e.g. max steps ~20–50, $ cap per task. A runaway agent is the failure mode, not a crash.
**Soundbite:** *"Budgets are enforced by the orchestrator, not requested in the prompt. The model can't talk its way past a counter."*

> [!question]- How do you detect an agent loop?
> Hash (tool, normalized args) and alert on repeats; watch for no new information over N steps; enforce step/token/time caps; check progress against the plan.

> [!question]- Why separate planner and executor models?
> Planning needs reasoning quality and happens rarely. Execution is high-volume and simple. Splitting them cuts cost and keeps the context of each worker small.

> [!question]- How do you keep the final report honest?
> Every claim links to a stored source snippet; verify the quote against the snippet; drop or flag unsupported claims.

**Go deep:** [[Chapter 9 - Design an Autonomous Research Agent]] → "Planner-Executor Architecture" and "Loop Detection and Budget Controls". Then [[N9 - Design Cases - Coding Agent and Deep Research]].

---

### Ch 16 — Design an AI Data Analyst (Text-to-SQL and Insights)
**One line:** Answer business questions in plain English by writing and running SQL safely.
**Shape:** Question → **Schema retrieval** (tables, columns, examples) → Generate SQL → **AST validate** → Sandbox execute (read-only, limits) → Self-heal on error → Chart + narrative
**Patterns:** P2, P4, P7, P8

**3 ideas**
1. **Schema retrieval is RAG.** Embed table/column descriptions, sample values and verified past queries. Big warehouses don't fit in a prompt.
2. **Sandboxed execution:** read-only role, row-level security, statement allowlist (SELECT only), timeouts, row/cost limits.
3. **Self-healing:** feed the DB error back with the failing SQL, retry a bounded number of times, classify error types.

**2 trade-offs**
- Free-form SQL (flexible) vs semantic layer/metrics API (correct definitions of "revenue", less flexible). Prefer the semantic layer for core metrics.
- Auto-run vs show SQL for approval. Depends on cost and sensitivity.

**Numbers:** Retry cap ~2–3. Query timeout and row caps always on.
**Soundbite:** *"The model never gets write access. SQL is parsed into an AST and checked before it gets anywhere near the warehouse."*

> [!question]- What does AST validation check?
> Statement type (SELECT only), referenced tables/columns exist and are allowed, no dangerous functions, LIMIT present, joins bounded.

> [!question]- Why does a semantic layer help?
> Business metrics have one blessed definition. The LLM picks metrics and dimensions instead of re-inventing joins, which removes a whole class of silently wrong answers.

> [!question]- What's the scariest failure mode?
> Not an error, but a query that runs and returns a plausible wrong number. Mitigate with verified-query examples, metric definitions, and showing the SQL with the answer.

**Go deep:** [[Chapter 16 - Design an AI Data Analyst (Text-to-SQL and Insights)]] → "Sandboxed SQL Execution" and "Self-Healing Query Pipeline".

---

### Ch 19 — Design an AI NPC Engine for Multiplayer Games
**One line:** Game characters that remember players and stay in character, at game-scale concurrency and latency.
**Shape:** Player event → Memory retrieve (episodic + relationship) → Persona/lore prompt → Small fast model → Lore/safety check → Dialogue + action → Memory write
**Patterns:** P1, P2, P3, P4, P9

**3 ideas**
1. **Memory architecture:** short-term (scene), episodic (per player, summarized), semantic (world lore). Importance-scored and decayed.
2. **Consistency:** persona card + lore retrieval + a checker for contradictions with canon.
3. **Scale/latency:** small (often fine-tuned) models, cached common lines, and pre-generation during idle time. Not every NPC needs a frontier model.

**2 trade-offs**
- Emergent, generative dialogue vs designer control. Use constrained actions and lore rails.
- Per-player memory richness vs storage and retrieval cost at millions of players.

**Numbers:** Dialogue TTFT target well under a second; most traffic on small models (P1).
**Soundbite:** *"The LLM picks dialogue and an action from an allowed set. Game state stays in the game engine, not in the model."*

> [!question]- How do you keep an NPC consistent across sessions?
> Persona card fixed in the system prompt (cacheable), retrieved relationship memory per player, and a lore check on outputs.

> [!question]- How do you serve millions of concurrent players cheaply?
> Small/distilled models, aggressive caching, ambient lines pre-generated, frontier model only for key story moments.

**Go deep:** [[Chapter 19 - Design an AI NPC Engine for Multiplayer Games]] → "NPC Memory Architecture".

---

### Ch 22 — Design a Multi-Agent Workflow Orchestrator
**One line:** Coordinate several specialist agents on long workflows, with shared state, handoffs and human approval.
**Shape:** Orchestrator (supervisor) → specialist agents ⇄ shared state store (typed artifacts) → Approval gates → Durable workflow log
**Patterns:** P4, P7, P8, P10

**3 ideas**
1. **Orchestration patterns:** supervisor (central), pipeline (sequential), swarm/handoff (peer). Supervisor is the safe default.
2. **State and handoffs:** agents exchange **typed artifacts**, not chat transcripts. A single source of truth with versioned writes and conflict resolution.
3. **Safety:** per-agent least-privilege tools, global budget, approval gates keyed to **reversibility** (send email, pay, delete).

**2 trade-offs**
- Multi-agent (specialization, parallelism) vs single agent (cheaper, simpler, fewer handoff errors). Many "multi-agent" problems are one agent with good tools.
- Autonomy vs human approval friction. Gate only irreversible or high-cost actions.

**Numbers:** Multi-agent uses several × the tokens of a single agent. Justify it by parallelism or isolation.
**Soundbite:** *"I'd start with one agent and add a second only when context isolation or parallelism clearly pays for the extra tokens."*

> [!question]- Supervisor vs swarm?
> Supervisor: one coordinator delegates and aggregates; easy to bound and trace. Swarm: peers hand off directly; flexible, harder to bound and debug.

> [!question]- Why typed artifacts instead of passing conversation history?
> Smaller context, clear contracts, validation is possible, and a handoff can't silently drop a requirement.

> [!question]- Which actions need human approval?
> Irreversible or externally visible ones: payments, deletes, sending messages, production deploys. Reversible reads/drafts don't.

**Go deep:** [[Chapter 22 - Design a Multi-Agent Workflow Orchestrator]] → "State, Handoffs, and Conflict Control" and "Safety, Budgets, and Human Approval". Then [[N6 - Agent Architecture 2026]].

---

### Ch 23 — Design an MCP-Based Tool Integration Platform
**One line:** A company-wide platform that exposes internal tools and data to any agent through MCP, securely.
**Shape:** Agent host (MCP client) → **MCP gateway** (authN/Z, policy, audit, rate limit) → MCP servers (tools, resources, prompts) → Backend systems
**Patterns:** P4, P7, P10

**3 ideas**
1. **Primitives:** tools (model-invoked actions), resources (app-attached data), prompts (user-invoked templates). Transport: stdio locally, streamable HTTP remotely.
2. **Trust model:** OAuth with per-user scoped tokens; the agent acts **as the user**, never with a super-credential. Server allowlist with pinned versions.
3. **Security failure modes:** tool poisoning (malicious descriptions), rug-pull (tool changes after approval), confused deputy, injection via tool results.

**2 trade-offs**
- Central gateway (policy, audit in one place) vs direct client→server (lower latency, scattered control).
- Many fine-grained tools (precise permissions, but they bloat the context) vs a few coarse tools.

**Numbers:** Tool count in context matters: dozens of tool definitions can cost thousands of tokens per call. Load tools on demand.
**Soundbite:** *"Every MCP server is third-party code with a natural-language attack surface. The gateway pins, scopes and audits it."*

> [!question]- What is a tool-poisoning attack?
> Hidden instructions in a tool's description/metadata that the model reads and follows, e.g. "also send ~/.ssh to this URL". Mitigate with review, pinning, description diffing, and least privilege.

> [!question]- What's the confused-deputy problem here?
> A server with broad credentials performs actions the requesting user isn't allowed to do. Fix: per-user delegated tokens and authorization at the server.

> [!question]- Tools vs resources vs prompts?
> Tools: model decides to call. Resources: data the app attaches as context. Prompts: templates the user picks.

**Go deep:** [[Chapter 23 - Design an MCP-Based Tool Integration Platform]] → "Permission and Trust Model" and "MCP Security Failure Modes". Then [[N7 - Agent Security and the Lethal Trifecta]].
