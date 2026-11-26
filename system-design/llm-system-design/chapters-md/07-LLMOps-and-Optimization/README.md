# 07 — LLMOps and Optimization

This folder covers the operational and lifecycle concerns that apply *after* an LLM system is architected and deployed: how to manage change safely (Ch. 24), how to measure quality continuously and gate releases on it (Ch. 27), how to control inference spend without sacrificing quality (Ch. 28), and how to detect and resolve production incidents in systems whose core component is a non-deterministic black box (Ch. 29). The common thread across all four chapters is that **LLM systems have many independently-changing behavioral dimensions** — prompts, models, retrieval indexes, tool schemas, guardrail policies, inference parameters — and every one of these chapters builds infrastructure to version, measure, attribute cost/quality to, and safely roll back changes along each of those dimensions independently. Traditional software/MLOps assumes code and model checkpoints are the only things that change behavior; these chapters repeatedly show that assumption is false for LLM systems, and that regression, cost, and incident response must be treated as statistical problems over non-deterministic output distributions rather than deterministic pass/fail checks.

---

## Chapter 24: LLMOps and Production Lifecycle Management

**Problem:** Design the operational platform and lifecycle practices to ship, monitor, evaluate, and safely evolve LLM-backed systems across 50 product teams doing 200 prompt/model/index/tool deployments/week at 1B requests/month.

**Core pattern — artifact registries + risk-tiered eval gates + progressive delivery + independent rollback:**
- **Prompt Registry / Model Registry / Index Registry:** immutable, content-addressed (SHA-256) versioning for prompts, models (provider, snapshot date, adapter hash, tokenizer version), and retrieval indexes (doc snapshot, embedding model, chunking strategy, ACL revision) — each treated as a first-class artifact, not a side effect of a code deploy.
- **Eval Store + Release Orchestrator:** runs golden-task regression, adversarial/safety tests, and retrieval evals against a risk-tiered gate ladder before promotion; no artifact bundle reaches production without meeting its tier's thresholds.
- **Shadow → Canary → Progressive rollout:** shadow mode validates on mirrored traffic with no user impact; canary exposes 1–5% (low risk) or 1% (high risk) of traffic with auto- or manual promotion.
- **Observability Pipeline + Drift Detector:** per-version p50/p95/p99 latency, TTFT/TPOT, cost/request, cache hit rate; drift detection on embedding-distribution shift (>5% from baseline centroid triggers re-eval).
- **Incident Console + independently-revertible artifacts:** blast-radius estimation (request count, tenants, revenue exposure), one-click rollback to any prior bundle, trace replay — and critically, prompt/model/index/policy can each be rolled back **independently** without disturbing the others.
- **Governance Layer:** risk-tier assignment gates human review/approval for regulated use cases; immutable audit logs with configurable retention (7 years for financial services).
- **Artifact bundle** is the atomic unit of reproducibility: `{prompt_version, model_version, index_version, tool_schema_versions, guardrail_policy, inference_config}` + trace_id.

**Pros:**
- Independent rollback of prompt/model/index/policy avoids compounding incidents (reverting a model to fix a prompt regression, etc.).
- Risk-tiered gates let low-risk teams ship in hours via automated smoke tests while high-risk (medical/legal) changes get mandatory 2+ reviewer sign-off and 48-hour canaries — the safe path is the fast path.
- Full artifact-bundle attribution makes regulated-industry audits and incident postmortems tractable (byte-for-byte response reconstruction).
- Segment-level monitoring catches regressions that global averages hide (e.g., +3% English task-success masking −8% Spanish).

**Cons / failure modes:**
- A single-word system prompt change can shift task-success rate 5–15% and go undetected without content-addressed versioning — "same name, different bytes" is a common root cause of unreproducible incidents.
- Tool schema renames can shift tool-call success rate 10–20% with no implementation change — agentic behavior is sensitive to wording, not just logic.
- LLM-as-judge drift: judge-human correlation degrading from 0.82 to 0.71 kappa silently invalidates gate decisions.
- Prompt sprawl: without owner/changelog/dependency-graph requirements, 50+ teams accumulate hundreds of orphaned prompt versions that burn eval compute.
- Cost attribution gaps: a prompt change that doubles tool calls can cost an extra $40K/month and be invisible without per-version cost tagging at ingestion time.
- Coupled rollbacks (reverting a model also reverts an intentionally-changed prompt) are a leading cause of extended incidents.

**When to use:** Organizations with multiple teams shipping prompt/model/retrieval changes at meaningful velocity (200/week scale) where regulated or high-stakes use cases coexist with low-risk ones. Overkill for a single team shipping one prompt occasionally.

---

## Chapter 27: Evaluation at Scale

**Problem:** Design an automated eval pipeline that continuously measures quality/safety/reliability across model updates, cheaply enough to run on every PR, with alert thresholds tuned to catch genuine regressions (p < 0.01) without false-positiving on noise.

**Core pattern — eval pyramid + calibrated LLM-as-judge + statistically-rigorous regression detection + CI/CD gating:**
- **Eval pyramid:** unit evals (every commit, 100–500 samples, $0.30–$1.50) → integration evals (every PR, 500–2,000 samples) → full regression (every deployment, 5,000–20,000 samples, $15–$60) → human evals (weekly, 200–500 samples, judge calibration).
- **LLM-as-judge**, calibrated monthly against human labels via Cohen's kappa (ordinal-weighted); target kappa ≥ 0.70. Mitigates positional bias (60–70% first-option preference — fix: average both A/B orderings), verbosity bias, and self-preference bias (use a judge from a different model family than the model under test).
- **Dataset Store:** immutable, versioned golden set, difficulty-stratified (40% easy / 40% medium / 20% hard), decontaminated via embedding cosine similarity ≥ 0.95 against training data.
- **Regression Detector:** Welch's t-test or Mann-Whitney U per dimension, alert only if `p < 0.01 AND delta > threshold` (e.g., correctness −2pp, safety −0.5pp, latency p95 +15%, cost +20%); Bonferroni/Holm-Bonferroni correction across dimensions to control family-wise error rate (uncorrected FWER at 20 dimensions is 18%).
- **A/B testing:** deterministic hash-based traffic split, MDE defined before running (e.g., 2pp at alpha=0.01/power=0.90 needs ~3,200 samples/variant), 48-hour minimum run duration, guardrail metrics (safety/error rate) checked one-tailed regardless of primary-metric win.
- **CI/CD Gate + Rollback Controller:** fails PR merge on regression; automated production rollback drops MTTR from a human's 20–40 minutes to under 5.
- **Adaptive eval depth:** classifies PRs (docs-only → skip; config-only → 100 evals; prompt change → 500; model code change → 2,000; model version upgrade → full 5,000) so cost is proportional to risk surface — full regression on every PR at 50 PRs/day would cost $750/day.

**Pros:**
- LLM-as-judge is ~100x cheaper than human labeling ($0.001–$0.005/eval vs. $0.15–$0.50) at 85–92% human agreement when calibrated, vs. 65–80% uncalibrated.
- Statistical gating (p-value + effect-size threshold together) prevents both false alarms from oversized samples and missed regressions from underpowered ones.
- Stratified difficulty tiers make both catastrophic regressions (easy-tier failures) and subtle capability shifts (hard-tier) separately visible.

**Cons / failure modes:**
- BLEU/ROUGE-based scoring is a documented failure mode: an 8% BLEU improvement from cutting verbosity caused a 12-point CSAT drop because BLEU rewards brevity, not completeness.
- Public benchmarks (MMLU, HumanEval, HellaSwag) are not valid regression signals for fine-tuned application models — contamination inflates scores 5–15%, and benchmark distribution ≠ production distribution.
- 100K evals/day requires 200+ concurrent judge workers to hit a 30-minute latency budget; naive sequential scoring of 5,000 evals takes 4.2 hours.
- A code-gen model upgrade that improved HumanEval 3% simultaneously increased p99 latency 40% and cost 25% — untracked because latency/cost weren't first-class eval dimensions.

**When to use:** Any production LLM system before shipping model/prompt changes; complexity compounds and becomes necessary at ≥10K evals/day or ≥5 tracked model dimensions. Human-only evaluation is economically impossible above roughly 100K evals/day ($15K–$50K/day).

---

## Chapter 28: Cost Optimization as a Design Concern

**Problem:** Reduce cost-per-request 40–70% while preserving quality SLOs (helpfulness regression ≤ 0.2 pts) and p95 latency ≤ 3s, with per-team cost attribution for budget governance.

**Core pattern — layered cost-reduction pipeline ordered cheapest-to-most-expensive:** semantic cache → model routing/cascading → prompt compression → output length control → batching → quantized self-hosted fallback.
- **Semantic Cache:** embedding similarity (cosine ≥ 0.92 recommended threshold — balances 35–45% hit rate against <2% off-topic response rate) against a vector index (HNSW); eliminates inference entirely on a hit. Highest-leverage single component — 40% hit rate in the worked example.
- **Routing Classifier / model cascading:** lightweight classifier (MiniLM fine-tuned binary, 85–90% accuracy) routes simple queries to a small model (7B–13B, $0.10–0.20/1M tokens) vs. frontier ($3.00/1M); confidence threshold calibrated via Platt scaling against shadow-traffic error rates (cascade to frontier below 0.70 confidence, where small-model error is ~18%).
- **Prompt Compressor (LLMLingua/LLMLingua-2):** token-importance pruning on cache misses above a length threshold; 1.5x ratio is safe everywhere (<1% accuracy loss), 3–4x only for redundant RAG context.
- **Prompt distillation** (design-time, not runtime): systematic per-instruction ablation against a 200–500 query golden set; typically strips 30–50% of a prompt's instructions with zero measurable quality impact and zero runtime cost.
- **Output Length Controller:** per-route `max_tokens` caps — output tokens cost 5x input tokens per-token on frontier models.
- **Batching:** online micro-batching (1.5–2x throughput), continuous/PagedAttention batching for self-hosted (2–4x throughput, GPU utilization 55%→85%), offline batch API (50% discount) for the ~60% of traffic with no real-time constraint.
- **Quantization:** INT8 (<1% quality loss, 0.5x memory) as the safe default; AWQ INT4 preferred over GPTQ INT4 for reasoning-heavy workloads (0.5–2% quality loss vs 1–3%).
- **Speculative decoding:** reduces latency, not token cost (target model still verifies every token) — draft model size trades acceptance rate against overhead (1B draft: 70–80% acceptance, +5% overhead; 7B draft: 80–90% acceptance, +15% overhead).
- **Cost Attributor + Budget Alert Service:** per-team/route/model tagging with <5-min lag; alerts at 80% of monthly cap.
- **Cache Invalidator:** tags cache entries with model_version; eager purge within 30 min for high-risk routes, lazy (check-on-hit) for low-risk routes to avoid a cold-start thundering herd.

**Pros:**
- Worked example: a 2M query/day support platform on GPT-4o at $432K/month drops to $112K/month (−74%) combining cache + routing + compression with no measurable CSAT change.
- Cost attribution surfaced that one team's "fetch all documents" retrieval consumed 38% of spend on 9% of traffic — invisible without per-team attribution.
- AWQ INT4 quantization on a 70B model cuts VRAM from 140GB to 35GB (2×A10G instead of 2×A100) at only 0.5–2% quality loss.

**Cons / failure modes:**
- Cosine threshold below 0.90 causes users to receive off-topic cached answers (8–12% off-topic rate at 0.85); above 0.95 hit rate collapses to 15–25%, negating the cost benefit.
- Never cache user-specific responses (order status, account data) — embedding similarity is high across users but the correct answer isn't.
- Routing classifiers need ≥1,000 labeled examples per route before deployment or the calibration curve is unreliable and effective error rate can run 2–3x higher than training-set metrics suggest; recalibrate monthly as query distribution drifts.
- Compression above 4x ratio degrades complex reasoning tasks 3–5% — not safe for reasoning-heavy routes.
- Speculative decoding only helps latency-bound workloads; if GPU is already saturated (throughput-bound), it adds overhead with no benefit.
- H100 is not automatically better value than A100 for inference: 2.5x the FP16 compute at 2–3x the hourly cost, and inference is memory-bandwidth-bound, not compute-bound, at typical batch sizes.

**When to use:** Cost pressure begins to matter around $5K/month in API spend; the layered architectural investment (routing, compression, quantized self-hosting) pays off at ≥$20K/month. Below that, semantic caching alone may suffice.

---

## Chapter 29: Observability and Incident Response for LLM Systems

**Problem:** Detect any latency/quality/safety/cost regression within 5 minutes and isolate root cause to a specific pipeline component within 15 minutes, for a platform serving 5,000 QPS across multiple product surfaces.

**Core pattern — span-decomposed distributed tracing + LLM-specific metrics + SLO burn-rate alerting + structured runbooks:**
- **Trace Instrumentation SDK (OpenTelemetry)** emits six canonical span kinds per request: root, retrieval (`db_query_ms`, `top_score`), reranking, generation (`ttft_ms`, `tbt_ms`, `cache_hit`, `cost_usd`), tool call, guardrail (`verdict`, `confidence`) — separating retrieval from generation spans is what lets an on-call engineer tell "wrong chunks retrieved" from "correct chunks, bad synthesis" without code bisection.
- **Trace Collector:** tail-based sampling (100% for errors/>2x p95 latency, 10% routine) — tail-based is required because head-based sampling can't know in advance whether a request will be slow.
- **W3C `traceparent` propagation** across async boundaries (HTTP sub-calls, Celery/SQS/Kafka queues via message envelope, using `LINK` not `CHILD_OF` for queued spans since the consumer may process seconds/minutes later).
- **Metrics Pipeline (Prometheus/Thanos):** LLM-specific signals beyond standard APM — TTFT (SLO p95 <1.0s), TBT (alert if p95 >150ms for 3 min), `llm_kv_cache_hit_rate` (drop raises both TTFT and cost simultaneously), `llm_refusal_rate`, `llm_truncation_rate`, `llm_retrieval_top_score` histogram.
- **Anomaly Detector:** EWMA/Z-score baselines (not fixed thresholds, because LLM traffic has strong diurnal patterns) — alert on KV cache hit rate drop >20pp, p95 latency shift >50% from EWMA baseline, refusal rate >2x baseline for 5+ min.
- **SLO Engine (error-budget burn rate):** four severities keyed to burn rate × detection window — 14x/1h (Sev-1, page immediately), 6x/6h (Sev-2), 3x/24h (Sev-3, Slack only), 1.5x/72h (Sev-4, weekly ticket); multi-window requirement (both short and long window must breach) eliminates transient self-resolving spikes.
- **Sampled prompt/response logging + PII scrubbing:** 10% default sampling (full logging at 5K QPS/2K tokens would cost ~$57K/month in scrubber processing alone), with forced 100% capture of errors and guardrail-blocked requests; two-layer scrubbing (regex, <1ms, then NER, 5–15ms) synchronous before any write.
- **Tiered retention:** hot 7 days (SSD, <100ms query, ~$230/TB/mo) → warm 30 days (~$23/TB/mo) → cold 1 year (Glacier/Parquet, ~$4/TB/mo) → auto-delete after 1 year (GDPR erasure compliance, verified by daily audit job).
- **Four structured incident runbooks** (latency regression, quality regression, safety incident, cost spike), each with named dashboard filters, thresholds, and step-by-step diagnosis trees.
- **Post-mortems adapted for black-box root cause:** enumerate hypotheses with evidence rather than assert root cause; when the proximate cause is a silent provider-side model update, the post-mortem states "root cause unattributable" as a valid finding rather than forcing a false-precision explanation.

**Pros:**
- Worked example: span-level `db_query_ms` attribute would have surfaced a missing vector-DB index in the first dashboard view instead of a 45-minute manual bisection.
- Alert-fatigue is tracked as a first-class metric (target ≤5 pages/shift, ≤20% false-positive rate) — Google SRE data cited shows engineers receiving >10 pages/shift have measurably higher missed-incident rates.
- 10% sampling + tiered storage keeps total observability cost at ~$180/month against a $10K/month budget at 5K QPS — full logging would run ~$57K/month.
- Runbook-driven alert design ("if you can't write a runbook for it, the alert shouldn't exist") forces elimination of vanity alerts.

**Cons / failure modes:**
- Non-determinism makes baseline drift genuinely ambiguous — a refusal-rate change could be (a) users asking worse questions, (b) a silent provider-side model update, or (c) a prompt injection in a recent deploy, and per-component metrics are required to even distinguish these hypotheses, let alone resolve them.
- AWS X-Ray becomes cost-prohibitive at this scale ($215K/month at 10% tail sampling) unless sampled far more aggressively than the tail-latency capture needed for LLM incident triage requires — a platform-fit mismatch.
- LangSmith at list price runs $21K–$86K/month at 5K QPS/10% sampling — vendor choice materially changes whether observability itself becomes a cost problem.
- Broken trace propagation across async/process boundaries (the single most common distributed-tracing rollout failure) produces orphaned spans invisible in waterfall views even when local instrumentation looks complete.

**When to use:** Becomes necessary at ≥100 QPS where manual inspection breaks down; essential at ≥1K QPS where cost and quality drift become invisible without instrumentation.

---

## Cross-Cutting Themes

- **Independent artifact versioning is foundational, not optional.** Ch. 24's prompt/model/index/tool/policy registries, Ch. 27's dataset/judge-prompt versioning, and Ch. 28's model_version-tagged cache entries all exist because behavior can change along any of these axes independently of a code deploy — and every chapter's incident-response story depends on being able to isolate which axis changed.
- **Statistical rigor over deterministic pass/fail.** Ch. 24 and Ch. 27 both frame regression detection as a hypothesis test (p < 0.01, effect-size thresholds, Bonferroni correction) rather than an exact-match diff, because LLM outputs are non-deterministic — the same theme resurfaces in Ch. 29's post-mortems, which explicitly reject "the model got worse" as a falsifiable root cause.
- **Calibration against human ground truth, repeated monthly.** Ch. 24's judge-model calibration (kappa 0.82→0.71 as a drift signal) and Ch. 27's identical Cohen's-kappa calibration loop (target ≥0.70, monthly cadence) are the same mechanism applied at the LLMOps-platform level and the eval-pipeline level.
- **Progressive delivery (shadow → canary → full rollout) appears in Ch. 24 explicitly and underlies Ch. 27's A/B testing and Ch. 28's routing-classifier shadow-traffic calibration** — in all three, real production traffic is run against a candidate change before it affects users, and traffic percentage scales with risk tier.
- **Segment/dimension-level breakdown over global averages.** Ch. 24's segment-level monitoring (language, tenant, risk class), Ch. 27's difficulty-stratified golden sets, and Ch. 29's per-`product_line`/`model_version`/`region` metric labels all exist to prevent the same failure: an aggregate metric improving while a minority segment silently regresses.
- **Cost attribution requires tagging at ingestion time, not post-hoc joins.** Ch. 24 (per-artifact-version cost), Ch. 28 (per-team/route/model Cost Attributor), and Ch. 29 (`llm_cost_per_request_usd` labeled by product_line/model_id) all converge on the same design: attach the attribution key to every trace/metric/log record when it's written, because retroactive joins across billing and usage data are either impossible or too slow to catch a spike before it reaches finance.
- **KV cache hit rate as a shared leading indicator.** Ch. 28 uses it as a cost-saving cache layer; Ch. 29 treats a drop in the same metric as a first-class anomaly signal because it simultaneously raises TTFT and cost — the same underlying mechanism read from two different operational lenses (optimization vs. incident detection).
- **Rollback/mitigation speed as the dominant design objective.** Ch. 24's independently-revertible artifacts, Ch. 27's automated Rollback Controller (cutting MTTR from 20–40 min to <5 min), and Ch. 29's SLO burn-rate paging (detect within 5 min, isolate within 15 min) all optimize the same variable: time between regression onset and mitigation, treating detection latency itself as a first-class metric to minimize.
