# 04 — Fine-Tuning and Prompting

This folder covers the architecture patterns for adapting and steering LLM behavior across four production contexts: sub-300ms latency-critical code completion (Ch. 8), high-throughput asynchronous content generation (Ch. 10), the mechanics of prompt construction and lifecycle management (Ch. 25), and parameter-efficient model adaptation via LoRA/QLoRA/DPO (Ch. 26). The common thread: **behavior can be shaped at the prompt layer (cheap, fast to iterate, bounded ceiling) or at the weight layer (expensive, slow to iterate, higher ceiling)** — and every chapter here surfaces the specific engineering needed to make one or both approaches reliable in production, with versioning, evaluation gates, and rollback as recurring infrastructure requirements.

---

## Chapter 8 — Design an AI Coding Assistant

**Problem:** Deliver sub-300ms inline code completions plus multi-turn chat in an IDE, balancing extreme latency sensitivity against context-assembly correctness and suggestion acceptance rate.

**Core pattern — dual-path architecture (separate model fleets for inline vs. chat):**
- **IDE Extension (client):** 50ms debounce timer, local FIM prompt assembly (<30ms) from in-memory AST, single persistent WebSocket, cancels in-flight requests on new keystrokes.
- **Edge Gateway:** TLS termination, auth/rate-limiting, routes to 7B inline cluster or 34B/70B chat fleet; deployed to 8–12 edge regions (driven by developer-density telemetry, not generic CDN geography) to cut RTT (e.g., 80ms→20ms for India via Mumbai edge).
- **Inline Completion Service:** quantized 7B model, continuous batch scheduler, prefix KV cache, **speculative decoding** with a 1B draft model.
- **Chat Service:** session state + Context Assembly Service (RAG over repo index + symbol graph), routes to 70B only for architectural/cross-file queries (classified via lightweight logistic regression, <5ms overhead).
- **Repo Index Pipeline:** AST parsing (tree-sitter), symbol graph (Neo4j/in-memory), function/class-boundary chunking (128–512 tokens), per-repo HNSW index (M=32, ef_construction=200, <5ms search, 96%+ recall@10), incremental diff-based re-index (<200ms/file).
- **Telemetry Pipeline:** Kafka ingestion → Flink (real-time) + Spark (batch) → feeds a daily-trained reranking model.

**Key techniques:**
- **FIM (Fill-In-The-Middle) prompting:** `<|fim_prefix|>...<|fim_suffix|>...<|fim_middle|>` lets the model respect code after the cursor (closing brackets, signatures) — fundamentally different from left-to-right completion.
- **Speculative decoding:** 1B draft model proposes K=4 tokens/step; 7B target verifies all 4 in one forward pass. Code acceptance rate 75–85% (vs. 55–65% prose) because code is syntactically deterministic. Net 2.5–3x decode speedup (50 tokens: 175ms→70ms). Mathematically equivalent to target-model sampling — zero quality loss.
- **Prefix KV caching:** ~200-token shared system/FIM preamble cached once; saves ~15ms/request, equivalent to removing ~0.9 GPUs of fleet load at 11,500 QPS peak.
- **Context budget allocation** (2,048 tokens): FIM prefix 600 / suffix 400 / imports 300 / recent edits 200 / open tabs (BM25) 300 / symbol graph 248 — ranked by recency (exponential decay), locality, symbol relevance, and git co-edit correlation.
- **Context strategy trade-off (acceptance rate progression):** current-file-only 12–18% → FIM+current-file 22–28% → FIM+open tabs (BM25) 28–34% → FIM+open tabs+symbol graph 32–38% → full repo RAG (chat-only, adds 70–150ms, no gain over symbol graph for inline).

**Pros:**
- Context quality dominates over model size — a 7B model with perfect context beats a 70B model with irrelevant context.
- Edge deployment recovers latency budget unattainable by adding centralized GPU capacity (RTT is not compute-reducible).
- Speculative decoding gives a "free" 2.5–3x speedup with no quality tradeoff.
- Silent graceful degradation (empty completion, no error UI) preserves user trust under load.

**Cons / failure modes:**
- 40–60% of inline requests are cancelled before completion — expected, but wastes GPU prefill if not preempted server-side.
- KV cache thrashing: prefix cache hit rate can drop below 50% at fleet capacity.
- A 50ms TTFT regression measurably drops acceptance rate by ~8% (cited GitHub Copilot example) — latency is a correctness constraint, not just a UX metric.
- Monorepo cold parse of 500K files takes 8–15 minutes even parallelized across 32 workers; poor context selection (12K irrelevant tokens) can push TTFT to 4s.
- Model updates can silently collapse acceptance rate (~5% drop) — mitigated only by shadow-mode deployment before promotion.

**When to use:** Any IDE-integrated assistant needing both instant inline suggestions and deeper repo-aware chat. Use symbol-graph context for monorepos; full RAG retrieval only for chat, never inline (150ms retrieval is untenable inside a 300ms budget).

---

## Chapter 10 — Design an Automated Content Generation Pipeline

**Problem:** Process 200K+ content pieces/day through multi-stage prompt chains with automated quality scoring and human review, optimizing throughput/consistency over latency.

**Core pattern — durable multi-stage DAG with HITL gating:**
- **Job Intake API** → **DAG Orchestrator** (Temporal.io) runs per-content-type stage graphs (outline → draft → polish → format-adapt), persisting each stage's output before the next begins (no lost work on crash/retry).
- **Prompt Template Registry** (versioned, per content-type/stage, A/B traffic-split metadata) feeds **Stage Executors** (stateless worker pools, one per stage type).
- **Quality Scorer**: fine-tuned 7B judge models + rule-based checks produce a weighted composite score and risk tier.
- **HITL Review Queue**: routes by risk tier; reviewer actions (approve/reject/edit) feed back into the DAG and into training data.
- **Content Store**: append-only, write-ahead log (WAL) with async replication — avoids 5–15ms sync-replication cost per stage write.
- **Publishing Gateway**: per-channel queues with independent retry/dead-letter handling.

**Key techniques:**
- **Prompt chaining / DAG (outline→draft→polish→format):** explicit inter-stage contracts (fixed JSON/Markdown schemas), inter-stage validation gates (e.g., outline completeness, draft length ±30%, structure preservation, keyword integration), context compression between stages (don't pass full history).
- **Quality scoring rubric** (weighted): relevance to brief 0.25, fluency 0.15, brand voice 0.20, factual grounding 0.20, compliance 0.20. Composite pass threshold 0.70; risk tiers: ≥0.85 no compliance flag → LOW (auto-publish); ≥0.70 + compliance flag → HIGH (mandatory HITL); ≥0.70 no flag → MEDIUM (10% sampled HITL); <0.70 → FAIL/regenerate.
- **HITL routing at 15%** of total volume (compliance/legal/medical/financial flagged), cutting review backlog 85% while holding 99.7% compliance (cited news-wire example).
- **Prompt A/B testing lifecycle:** shadow lane (5%) → compare quality/HITL-rejection/engagement vs. baseline → gradual rollout 5%→25%→50%→100%, or automatic rollback.
- **Semantic deduplication:** cosine similarity > 0.92 on brief embeddings flags near-duplicate submissions, saving 8–12% of pipeline cost.

**Pros:**
- Migrating sync calls (8 req/sec ceiling) to async DAG reached 200K articles/day while cutting per-article cost from $0.15 to $0.06 (cited example) via batching/caching.
- Multi-stage decomposition (3–4 stages) reaches "best" quality and highest optimization granularity vs. single-prompt generation, at only 3–4x cost — marginal next to HITL labor savings.
- Append-only content store + WAL gives full audit trail and rollback with negligible added latency.
- Temporal.io's durable execution handles long workflows (up to 2h), fan-out (multi-channel), and automatic retry/backoff natively.

**Cons / failure modes:**
- Error amplification risk: a bad outline propagates into a bad draft (mitigated only by validation gates, not eliminated).
- HITL queue backlog during campaign launches (3x peak) can breach 30-min SLA for 20% of items — mitigated by temporarily raising the auto-publish threshold or activating surge reviewers.
- Prompt regression can go undetected because the quality scorer itself is calibrated on the old prompt's output distribution — requires mandatory A/B hold-outs and tracking HITL rejection rate as a leading indicator.
- Reviewer fatigue: approval rate creeps up over a shift (rubber-stamping); mitigated with 5% calibration items (known-bad content) and mandatory 2-hour breaks.
- Retry amplification: a degraded LLM API can double cost if 60% of stage calls fail the quality gate and each retries twice — requires a circuit breaker (pause stage if retry rate > 30%/10min).
- Scorer-human correlation must be monitored monthly (target Kendall's τ > 0.7); below 0.6 triggers judge-model retraining.

**When to use:** High-volume, throughput-over-latency content operations (marketing copy, news summaries, product descriptions) where consistency and compliance auditability matter more than per-request speed. Not suited to sub-second interactive use cases.

---

## Chapter 25 — Prompt Engineering in Depth

**Problem:** Build a production prompt system that stays consistent and safe across changing inputs, model updates, and teams — with versioning, injection defense, and measurable quality gates.

**Core pattern — structured prompt pipeline with pluggable retrieval and hard versioning:**
- **Prompt Builder** (single point of assembly: system + few-shot + CoT + user query + schema) → **Few-Shot Retriever** (embedding ANN over a pre-embedded **Example Pool**) → **Injection Detector** (runs *before* interpolation) → model call → **Schema Validator** (retry loop, max 2) → **Audit Logger**.
- **Prompt Registry**: single source of truth (`prompt_id`, `version`, `template`, `eval_results`, `deployment_status`, `ab_weight`, `model_id`); rollback = registry write, not code deploy.
- **A/B Controller**: deterministic hash(user_id + prompt_id) assignment; **Prompt Compressor** runs offline, zero request-time latency cost.

**Key techniques and figures:**
- **Prompting strategy trade-offs:** zero-shot 80–88% (degrades on shift); fixed few-shot 88–93% in-distribution; CoT gives 10–30% lift on multi-step reasoning but adds 0.5–2s latency and ~$6,500/month extra at 500 QPS for 100 scratchpad tokens; CoT+few-shot highest reasoning quality but highest cost/latency. CoT provides no gain (can hurt) on single-step classification.
- **Structured output (XML preferred over JSON for long generations):** reduces hallucination via "parsing commitment" — opening a tag commits the model to a schema-valid continuation, which the validator can catch.
- **Instruction ordering:** attention sink (first tokens) + recency bias (tokens just before generation) → put critical constraints first *and* repeat them immediately before the output schema.
- **Few-shot selection tiers:** zero-shot (baseline) → fixed few-shot (+4–8% accuracy, degrades under distribution shift, ~$32–65/day at 500 QPS) → **dynamic/embedding-based few-shot** (+8–15% accuracy, most robust to shift, ~$10–30/month infra) → fine-tuning (best but >1,000 labeled examples and $50–500/run needed). First 3–5 semantically relevant examples deliver ~80% of ICL benefit; diminishing returns past 5.
- **Hard negative mining:** examples with high embedding similarity but different correct labels, preventing surface-level lexical pattern matching (billing-classifier example).
- **Example ordering rule:** anchor examples first → hard negatives in the middle → most-relevant example last (recency bias maximizes its influence).
- **Prompt deployment maturity ladder:** hardcoded-in-code (minutes-to-hours rollback, no quality visibility) → config file → prompt registry (no gate, <1min rollback) → **registry + eval gate** (30–60min to deploy, blocks >2% regressions) → **registry + eval gate + A/B canary** (24–48h, best quality visibility, <1min rollback via weight update).
- **A/B statistics:** ~600 samples/variant needed for a binary metric at 5% effect size (α=0.05, power=0.80); ~200 for continuous 1–5 ratings. Minimum 24h canary exposure to capture diurnal variation.
- **Prompt injection defense (structural > classifier-only):** demarcate user content in `<user_input>` tags, run an injection-pattern classifier pre-interpolation, sanitize output to never echo system prompt, treat every multi-turn boundary (including tool results) as a potential injection surface.

**Pros:**
- Dynamic few-shot recovered a customer-support classifier from 76% (post model-update regression) back to 93% accuracy (above its original 91%) — insulates against future model churn.
- XML structured output + schema validation + retry dropped legal-extraction parse failures from 12% to 0.3% (cited example).
- Registry-based versioning makes rollback a metadata write (<1 minute) instead of a code revert (30–90 min MTTR).
- Prompt compression can cut ~20% of tokens (~$25,500/day savings at the chapter's assumed volume) and often *improves* quality by reducing attention competition.

**Cons / failure modes:**
- Zero-shot degrades sharply on distributional shift and after model updates.
- Fixed few-shot examples go stale as input distribution drifts; embedding-pool staleness requires monthly audits.
- Embedding model version mismatch between pool and live retriever silently breaks cosine similarity reliability — must re-embed the whole pool on any embedding-model change.
- Prompt sprawl: 200+ active versions with no retirement process; A/B test pollution when multiple concurrent tests share a route.
- Eval datasets themselves drift (built once, production shifts) — must be supplemented monthly with anonymized production samples.
- Retry loop is capped at 2 attempts by design — beyond that, log and return a structured error rather than partial/garbage output.

**When to use:** Any production LLM endpoint, especially ≥100 QPS where latency/token cost sensitivity is material. Use full system-prompt design (not just role prompting) whenever output must be machine-parseable or users may attempt to alter behavior; escalate up the deployment ladder as blast radius and user-facing risk increase.

---

## Chapter 26 — Fine-Tuning and Adaptation

**Problem:** Take a pretrained base model and a domain dataset, produce a task-specialized model that beats the base on target metrics, and serve many such variants without duplicating base weights per customer.

**Core pattern — parameter-efficient adapters served via multiplexing on a shared frozen base:**
- **Dataset Curator** (MinHash dedup, format normalization, quality filtering) → **Training Orchestrator** (injects LoRA config, manages mixed precision/gradient checkpointing) → **Eval Pipeline** (task-metric delta + MMLU delta gate) → **Adapter Registry** (content-hash-addressed, versioned, reproducible) → **Serving Engine** (base model resident once, LRU adapter cache, hot-swap by `adapter_id`) → optional **Merge Service** (bakes high-traffic adapters into base weights) → **Preference Data Collector** feeding DPO/ORPO training.

**Key techniques and figures:**
- **LoRA:** `W = W₀ + BA·(α/r)`; only ~0.12% of parameters trainable at r=16 on a 7B model (~8.4M params). B initialized to zero so ΔW=0 at start. r=4 (~2.1M params) suffices for style/format; r=16 (~8.4M) is the default for most instruction-tuning/domain-adaptation; r=64 (~33.6M) shows diminishing returns at 4x cost. Typically applied to Q,V projections only (K acts as an attention lookup index, less useful to adapt); Q,K,V,O doubles params for domain-knowledge injection; adding MLP up/gate approaches full-FT quality.
- **QLoRA:** 4-bit NormalFloat (NF4) quantization of frozen base + bf16 adapter training. Memory: full FT ~112GB+ (Adam states), LoRA bf16 ~40GB, QLoRA NF4 ~10–12GB for a 7B model. NF4 preferred over INT4 because it allocates precision to where weight density actually concentrates.
- **Adaptation method ladder:** full fine-tune (best quality, severe catastrophic forgetting, 100K+ examples) → LoRA (90–95% of full-FT quality, no forgetting, base frozen) → QLoRA (85–92%, single-GPU friendly) → prefix/adapter tuning (70–80%, style-only) → prompt tuning (60–75%, <1,000 examples, format-only).
- **Dataset quality over quantity:** LIMA-style finding — 1,000 curated examples can outperform 100,000 noisy ones, because fine-tuning teaches format/style/domain application, not new facts. Curation pipeline: MinHash LSH dedup (Jaccard >0.85, removes 15–30% of web-scraped data) → format normalization to one canonical schema (e.g., ChatML) → length filtering (drop prompts >4,096 tokens, responses <10 tokens or >4x median) → quality scoring (perplexity filter free/medium quality; LLM-as-judge $0.001–0.005/example, ~100x cheaper than human review; human review $0.50–1.50/example for calibration; reward-model scoring if one already exists) → explicit negative/refusal examples (red-teamed, production-log-sourced, or synthetic mutations) — without negatives, training gradients only ever push toward compliance.
- **Loss masking:** SFT loss computed only on response tokens, not prompt tokens, to avoid nudging the model toward generating prompt-like text.
- **Alignment method ladder:** RLHF (PPO; 3–4x model size in GPU memory across policy/reference/reward/value; best quality ceiling via online exploration but unstable — reward hacking, KL collapse) → DPO (2x memory, preference pairs only, 95–98% of RLHF quality, stable supervised loss, standard production choice) → ORPO (1x memory, no reference model, 90–95% of RLHF, less stable gradients near probability 0/1) → SFT-only (1x, no preference signal, format/schema tasks only).
- **Serving/adapter multiplexing:** base loaded once; per-adapter delta ~33MB (rank-16, 7B); 30 resident adapters ≈ 990MB extra VRAM. Hot-swap: cold load (NVMe+PCIe) ~13–15ms, warm (host RAM) ~2ms, cache hit 0ms; LRU eviction (top-20 resident) because production traffic is bursty per customer.
- **Merging:** justified once an adapter exceeds ~30% of traffic and is stable for 30+ days — produces a zero-overhead dense model but can't be un-merged without reloading original base weights; re-merge takes 15–30 minutes.
- **Catastrophic forgetting mitigations:** EWC (Fisher-information-weighted penalty on parameter drift), replay buffers (1–5% of new dataset drawn from prior training data), task-vector arithmetic (summing/subtracting LoRA adapters in weight space for composable specialization). LoRA's frozen base inherently limits forgetting versus full fine-tuning.
- **Promotion gate:** task metric delta ≥ +5% AND MMLU delta ≥ -2% relative to base, else reject (catches overfitting to narrow task distribution). Canary at 5% traffic for ≥24h before full promotion.

**Pros:**
- Legal-tech example: instruction-tuning Mistral-7B with 8,000 pairs (LoRA r=16) raised schema compliance from 71% (zero-shot GPT-4) to 97%, at 4x lower per-request cost.
- Code-intelligence example: 40 customer-specific adapters on one Deepseek-Coder-7B base fit in +800MB vs. 560GB for 40 full model copies — fleet drops from 12 nodes to 2.
- LoRA/QLoRA fully avoid catastrophic forgetting because base weights stay frozen.
- Distillation-based dataset creation is ~7x cheaper than manual curation ($700 vs. $5,000 per 10K examples) though it requires a quality-filtering pass to catch hallucinated examples.
- Adapter registry's content-hash addressing gives free deduplication of identical training runs and point-in-time rollback without duplicating weights.

**Cons / failure modes:**
- RLHF's infrastructure cost (3–4x model size, PPO instability, reward hacking/KL collapse) makes it unsuitable for most domain-adaptation use cases — DPO covers 95–98% of the quality at half the memory.
- ORPO's odds-ratio gradient destabilizes near probability 0/1, especially early in training.
- Full fine-tuning risks severe catastrophic forgetting and requires 100K+ examples plus 112GB+ GPU RAM to be worthwhile.
- Prompt tuning and prefix/adapter tuning have a low quality ceiling (60–80% of full FT) — not viable when deep behavioral change is required.
- Heterogeneous-adapter batches add real (if small) overhead: 8 distinct adapters × 32 layers × 2 projections = 512 extra matrix additions per batch (<0.5ms, but non-zero).
- Merging trades flexibility for speed — merged adapters can't be hot-updated without a 15–30 minute re-merge, and merging every adapter defeats the memory-efficiency point of multiplexing.

**When to use:** Fine-tuning is justified when few-shot/prompting has plateaued, latency from long few-shot prompts is unacceptable, or a behavior must be deeply internalized (e.g., strict schema compliance, proprietary domain vocabulary) — not for one-off or low-volume tasks where prompting (Ch. 25) is cheaper to iterate. Use DPO by default for preference alignment; reserve RLHF for frontier-scale alignment requiring online exploration; use ORPO only under tight GPU constraints.

---

## Cross-Cutting Themes

- **Prompting-first, fine-tuning-second discipline:** Ch. 26 explicitly cross-references Ch. 25 ("prompt engineering — must precede fine-tuning decision"). Fine-tuning is reserved for cases where few-shot accuracy has plateaued or per-request example overhead is too costly/slow — otherwise dynamic few-shot retrieval (Ch. 25) or repo/context assembly (Ch. 8) is the cheaper lever.
- **Versioned registries + eval gates as the universal safety mechanism:** Ch. 10 (Prompt Template Registry + shadow lane + gradual rollout), Ch. 25 (Prompt Registry + eval gate + canary), and Ch. 26 (Adapter Registry + MMLU/task-delta gate + canary) all converge on the same shape — version everything, gate promotion on an automated eval delta threshold, and make rollback a metadata/registry write rather than a redeploy.
- **Canary/A/B rollout as standard promotion path:** every chapter with an adaptation/prompt-change surface (8's model updates, 10's prompt A/B lifecycle, 25's A/B controller, 26's 5% canary) uses staged traffic promotion (5%→25%→50%→100% or similar) with automatic rollback on regression.
- **Latency vs. quality tradeoff recurs directly:** Ch. 8's 300ms budget forces context-selection and decoding shortcuts (speculative decoding, prefix caching); Ch. 25 quantifies CoT's 0.5–2s cost for a 10–30% reasoning gain; Ch. 26 quantifies adapter-hot-swap latency (0–15ms) as a serving constraint.
- **Human-in-the-loop / human review as a calibration and training-data source, not just a gate:** Ch. 10's HITL feedback flows into prompt tuning, scorer retraining, and RLHF/DPO preference pairs; Ch. 26's Preference Data Collector formalizes the same loop with Cohen's kappa quality control (re-annotate batches below κ=0.6).
- **Cost of adaptation scales with infrastructure complexity, not just compute:** Ch. 26 shows RLHF costing 3-4x the GPU footprint of DPO for marginal quality gain (95-98% of RLHF achievable via DPO); Ch. 10 shows 3-4x LLM cost for multi-stage chains is justified because it's marginal next to HITL labor savings; Ch. 25 shows compression and dynamic retrieval recovering cost with no quality loss.
- **Evaluation of generated/adapted output is never purely automated:** Ch. 10's quality scorer requires monthly human-correlation calibration (Kendall's τ > 0.7); Ch. 25's prompt eval requires golden datasets refreshed with production samples; Ch. 26's promotion gate requires both a task-specific held-out set and a general-capability regression check (MMLU) to catch overfitting.
