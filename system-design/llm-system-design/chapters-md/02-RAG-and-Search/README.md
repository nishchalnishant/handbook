# 02 — RAG and Search

This folder covers systems that ground LLM output in retrieved data rather than parametric memory alone: conversational RAG, enterprise semantic search, document extraction, personalized recommendation, multimodal (image/video/document) search, long-context legal review, and a general-purpose production RAG platform. The common thread is a **retrieve → filter/rank → pack → generate → verify** pipeline, where each chapter specializes one or more stages (ACL filtering, cross-modal fusion, citation verification, business-rule reranking) for a specific domain's failure modes. Nearly every chapter converges on **hybrid lexical+semantic retrieval fused via Reciprocal Rank Fusion**, a **cross-encoder (or learned) reranking stage**, and **content-type-aware chunking** as load-bearing defaults — variation between chapters is mostly in what sits before retrieval (query planning, ACL resolution, intent classification) and after generation (grounding/citation verification, hallucination checks).

---

## Chapter 6 — Design a Customer Support Chatbot

**Problem:** Design a production support chatbot that holds multi-turn conversational memory, retrieves grounded KB answers via RAG, adapts tone via sentiment, and escalates to humans when confidence is low or risk is high (500K tickets/day).

**Core pattern/architecture:**
- Session Manager (Redis, 24h TTL, HMAC-signed tokens) → Conversation Memory Store: **sliding window of last 4 turns (~600 tokens) + rolling summary (~200 tokens)**, entity map stored separately as structured JSON to survive compression.
- Intent Classifier (DistilBERT-class, ~66M params, <10ms, >92% accuracy target) routes to FAQ fast-path / RAG / tool-call / escalation.
- KB Retrieval Engine: BM25 (Elasticsearch) + ANN (Qdrant/HNSW, M=16, ef_construction=200) fused via **Reciprocal Rank Fusion (k=60)**, then freshness-decay-weighted, then **cross-encoder reranker (BAAI/bge-reranker-base)** on top-20 → top-3 chunks. Full pipeline ~140ms p50 / 200ms p99.
- Sentiment Analyzer (5-class, async sidecar ~20ms) feeds a sentiment trajectory (rolling last-5 labels) into the Escalation Engine.
- Escalation Engine: 6-signal OR-with-priority fusion (explicit request, confidence < 0.4, sentiment+turns+unresolved, high-risk topic, turn count > 10, repeated question ≥ 2).
- Safety Layer: entity-consistency check (order IDs must match tool results), action-confirmation guard, PII redaction.
- Confidence calibration: raw logprobs → logistic regression trained on 10K labeled examples, retrained monthly.

**Pros:**
- Sliding window + summary caps memory at ~1,000 tokens/turn regardless of conversation length (vs. unbounded growth with full history).
- Content-aware KB chunking (atomic Q+A, clause-level policy, section-level articles) improves Recall@3 by ~8 points over fixed-size chunking.
- Cross-encoder reranking lifts Precision@3 from 71% to 83% over RRF alone.
- Multi-class sentiment (vs. binary angry/not-angry) cuts false-positive escalations ~35%.

**Cons / failure modes:**
- Sliding window alone causes "entity amnesia" — an order ID mentioned in turn 1 is invisible by turn 6; requires a separate structured entity store as mitigation.
- Uncalibrated logprobs are overconfident by 15-20 points on domain queries; calibration degrades 8-12 points in ECE over 90 days without retraining.
- Real-world incident: memory overflow bug during a flash sale caused the bot to hallucinate order details from prior sessions.
- Real-world incident: stale cancellation policy served wrong early-termination fee to 1,200 customers before a freshness SLA violation was caught.
- Turn-count-threshold escalation alone has 40-60% false-positive rate; must be combined with an "unresolved issue" signal.

**When to use:** High-volume conversational support where cost/latency budgets rule out full-history prompts (>70% containment target, <$0.08/conversation). Hierarchical entity+summary+window memory is reserved for account-heavy/multi-order workflows where losing an entity to compression is a compliance risk.

---

## Chapter 7 — Design an Enterprise Semantic Search Engine

**Problem:** Search a 50M-document heterogeneous enterprise corpus (PDF/HTML/DOCX/XLSX) with 100%-correct document-level ACL enforcement and sub-200ms p95 latency, Recall@10 > 0.85.

**Core pattern/architecture:**
- Document Processor: format-specific parsers (PyMuPDF+table detection for native PDF, Tesseract/DocTR OCR for scanned PDF routed by confidence score <0.70, BeautifulSoup for HTML, openpyxl for XLSX row-level records).
- Chunking Engine: per-doc-type strategy (512-768 tok/25% overlap long-form, 256-512 tok/10% clause-level policy, row-group+repeated-headers for spreadsheets, AST-aware for code).
- Dual Index: Elasticsearch BM25 + Qdrant/Weaviate HNSW vector index, queried in parallel (top-200 each), merged via **RRF (k=60)**.
- **ACL Filter runs after fusion but before reranking** (never post-response) — bitset/token intersection on `acl_groups` metadata field; ACL resolver caches user→group expansion in Redis (TTL 5 min, >95% hit rate).
- Cross-encoder reranker (~110M params, ms-marco-MiniLM-L-12-v2 class, ~1.2ms/pair GPU) on ACL-filtered top-50.
- Index Lifecycle Controller: blue-green alias-swap deployment with quality gate (Recall@10/NDCG@10 regression check on 100-500 benchmark queries) before promotion; old index kept hot 24h for rollback.

**Pros:**
- Retrieval strategy progression: BM25-only Recall@10 0.55-0.65 → dense-only 0.70-0.80 → hybrid RRF 0.80-0.88 → hybrid+cross-encoder 0.85-0.92.
- Pre-filter ACL strategy gives full correctness at only +10-20ms query overhead and +10-15% index size, vs. partitioned-per-group indexes (3-10x storage).
- Incremental HNSW online insertion meets the 30-minute freshness SLA without nightly full rebuilds (a full 650M-vector rebuild takes 12-18 hours).
- Matryoshka embeddings (256-dim ANN pass + 1536-dim rerank) cut memory 6x/throughput 3x at <2% recall loss.

**Cons / failure modes:**
- Real-world incident: post-retrieval ACL filtering leaked document *existence* metadata to unauthorized users — required re-architecting to pre-filter.
- Real-world incident: table-heavy FDA submission PDFs had 40% lower retrieval accuracy than plain text; layout-aware parsing recovered 35% of lost recall.
- Reranker is a throughput bottleneck at peak QPS (adds 150ms+, can push p95 over 200ms budget) — mitigated by dynamic reranker depth (top-50 normal, top-20 peak) or skipping under extreme load.
- Scanned PDFs have 5-8% parse failure rate vs. <1% for native PDF/HTML/DOCX.
- ACL cache miss storms after maintenance windows spike p95 to 300ms+; needs staggered TTL jitter + background refresh.

**When to use:** Enterprise corpora with strict compliance/ACL requirements where a leak is a P0 incident. Partitioned per-group index sharding is only appropriate for single-tenant or very-few-group deployments due to combinatorial storage blowup; pre-filter is the default otherwise.

---

## Chapter 11 — Design a Financial Document Extraction System

**Problem:** Extract structured, schema-conformant data (line items, totals, dates) from financial documents (invoices, statements, filings) via an OCR-to-LLM pipeline with near-zero tolerance for hallucinated numbers.

**Core pattern/architecture:**
- OCR strategy selection by source quality (native-text vs. scanned vs. mixed), with layout detection (DETR-class model) identifying regions before Table Structure Recognition (TSR) reconstructs table grids.
- Constrained/grammar-based decoding forces LLM output into a valid JSON schema, eliminating a class of malformed-output failures outright.
- 5-layer hallucination prevention framework: source grounding via bounding-box traceability, cross-field arithmetic checks (e.g., line items must sum to stated total), confidence scoring, human-review routing for low-confidence extractions, and batch-level anomaly detection.
- Hallucination taxonomy differentiates failure types (fabricated value, wrong-field mapping, unit/currency confusion, transposition) to target mitigations precisely.

**Pros:**
- Cross-field arithmetic validation catches numeric hallucinations that pure confidence scoring misses (a fabricated line item can still look "confident").
- Constrained decoding removes JSON-malformation failures entirely versus free-form generation + parsing.
- Layered defense (grounding + arithmetic + confidence + human review + anomaly detection) means no single failure mode has to be caught by one mechanism.

**Cons / failure modes:**
- Production bottlenecks: OCR quality variance across document sources, table extraction failures on complex/nested tables, context overflow on long multi-page filings, cross-document KV-cache contamination when batching, schema evolution breaking existing extractors, and confidence-score drift over time.
- OCR-dependent pipelines inherit OCR's failure modes upstream — bad OCR silently degrades every downstream stage.

**When to use:** High-stakes structured extraction (financial, regulatory) where a wrong number has direct monetary/compliance consequences — justifies the extra latency/cost of multi-layer verification versus a single-pass extract-and-trust approach.

---

## Chapter 12 — Design a Personalized E-commerce Shopping Assistant

**Problem:** Serve real-time personalized product recommendations/conversational shopping assistance by fusing user profile signals, product catalog embeddings, and business constraints at low latency.

**Core pattern/architecture:**
- Two-tower model: separate user-embedding and product-embedding towers trained jointly (collaborative filtering signal) so relevance can be computed via a fast dot-product/ANN lookup rather than a per-request cross-encoder pass over the whole catalog.
- Profile-catalog fusion scoring formula blends collaborative-filtering score, semantic similarity, and recency/behavioral signals into a single ranking score.
- Business rules engine layered **on top of** ML ranking: hard filters (in-stock, region-restricted, age-gated) applied before soft boosts (margin-weighted promotion, inventory-clearance nudges) — hard/soft separation prevents business logic from silently overriding relevance in ways that are hard to debug.
- Hybrid search trade-off table balances pure semantic similarity against keyword/attribute filters (brand, size, price band).
- Revenue/CTR attribution modeling compares last-click, direct, view-through, incremental A/B, and multi-touch Shapley-value approaches for crediting recommendation impact.

**Pros:**
- Two-tower architecture decouples user and product inference, enabling precomputed product embeddings and sub-linear online scoring at catalog scale.
- Hard-filter/soft-boost separation in the business rules layer keeps ML ranking and merchandising policy independently testable.
- Multiple attribution models let the team distinguish correlation (last-click) from causal incremental lift (A/B), avoiding over-crediting the recommender.

**Cons / failure modes:**
- Business rule layers, if not kept strictly separated from ML scoring, can mask ranking regressions (a bad model still "looks fine" because hard filters/promotions dominate the visible results).
- Attribution model choice materially changes perceived recommender value — last-click and view-through can wildly overstate impact versus incremental A/B testing.

**When to use:** Real-time personalization where catalog size makes per-query cross-encoder scoring infeasible; two-tower + business rules is the standard production pattern for balancing relevance with merchandising/inventory constraints.

---

## Chapter 15 — Design a Multimodal Asset Search System

**Problem:** Search 500M+ images/video/document assets by text or image query at 10K QPS, p95 < 150ms, nDCG@10 > 0.65, unifying cross-modal retrieval in a single system.

**Core pattern/architecture:**
- Shared embedding space via CLIP-family models (SigLIP ViT-SO400M recommended production choice; OpenCLIP ViT-G/14 and EVA-CLIP as alternatives) mapping text and images into one vector space.
- Document embedding: hybrid render-to-image + text-extraction (production default, +10-15% nDCG over either alone).
- Index architecture: separate-per-modality indexes (production default) vs. unified vs. hierarchical; sharded HNSW across 16 machines/64GB RAM each for 1.62B total vectors.
- Fusion strategies: early fusion (weighted average, -3-5% R@1, cheapest), **late fusion (RRF, k=60)**, learned fusion (+8% nDCG, most expensive to train), and hybrid early+late fusion as the best balance.
- Video: hybrid uniform-sampling + TransNetV2 scene-boundary keyframe extraction (production default, capped at 15 keyframes/30s clip, +12% recall@5 vs. scene-boundary-only), indexed hierarchically at clip-level with keyframe-level drill-down.
- Multi-signal fusion weights: visual 0.50, audio-transcript 0.20, OCR-overlay 0.10, metadata 0.20.
- Reranking via CLIP-score-distillation reranker (+5-10% nDCG, <20ms added) or ColPali-style late interaction (+8-12% nDCG but 33x storage cost).

**Pros:**
- Full pipeline (CLIP + reranker) improves nDCG@10 by 22% over BM25-only text search on the stock-media benchmark.
- Hybrid early+late fusion captures cross-modal signal without the full cost of learned fusion.
- Matryoshka Representation Learning enables 128-dim ANN pass + 768-dim rerank, trading storage/compute for near-full accuracy.

**Cons / failure modes:**
- Real-world incident: stock media platform saw a 15% WoW engagement drop from a degraded text-search path before CLIP+reranker was deployed.
- ColPali/late-interaction reranking gives the largest nDCG gain (+8-12%) but at 33x storage overhead — narrow applicability.
- Early (weighted-average) fusion alone *loses* 3-5% R@1 versus not fusing — cheap but measurably worse, only appropriate under tight latency budgets.
- Video keyframe capping (15/30s clip) is a deliberate recall-vs-cost tradeoff; uncapped sampling would improve recall further but blow up index size.

**When to use:** Cross-modal (text-to-image/video, image-to-image) search at large scale. Enterprise DAM case study shows the value concretely: search session time dropped from 40 minutes to 3 minutes after adopting this architecture. ColPali-style late interaction should be reserved for scenarios where the 33x storage cost is acceptable (e.g., smaller high-value document sets), not general asset search.

---

## Chapter 17 — Design a Legal Contract Review System

**Problem:** Review 10K contracts/day (avg 80 pages / ~120K tokens) for risk clauses with 99%+/95%+ extraction accuracy, **zero hallucinated citations**, and a 7-year WORM audit trail.

**Core pattern/architecture:**
- Long-context strategy choice is itself the central design decision — options are chunked (17 calls, $1.80, 92%/96% accuracy), long-context single-pass (1 call, $0.51, 85%/97%), dual-pass (2 calls, $1.02, 93%/97%), hierarchical (10-15 calls, $1.20, 96%/98% — default for critical clauses), and hybrid tiered (96%/92% by tier, $1.50 — overall production default).
- **5-stage citation verification cascade**: exact string match (~70% resolved), normalized match (+10%), fuzzy window match ±500 chars (+8%), full-document search (+5%), reject as unverifiable (~7% residual).
- Hallucination-rate-by-mitigation-strategy table: no grounding instruction 12% hallucination rate, verbatim-quote instruction 7%, verbatim+few-shot 3%, Claude 3.5-class model 4%, full verification+recovery cascade <1% effective.
- Multi-document comparison strategies range from full-text diff (75%/98% accuracy, 5s) to clause+LLM analysis (99%/98%, 120s — reserved for M&A); clause+semantic+rule matching (97%/96%, 45s) is the production default.
- Cross-reference resolution capped at max 3 hops to bound cost/latency on deeply nested clause references.
- Precedent-based risk scoring: gradient-boosted classifier trained on historical human decisions, layered on top of static rule-based scoring.

**Pros:**
- Citation verification cascade at 15% extra processing time converts a near-miss ($2M liability exposure incident) into a caught, correctable error.
- Fine-tuned 8B-13B model for standard/boilerplate clauses saves ~$8K/day at 10K contracts/day versus routing everything to a frontier model.
- Precedent-based risk scoring improves +12 points over static rules and cuts unnecessary escalations by 30%.
- Hierarchical long-context strategy gets the highest accuracy (96%/98%) for critical-clause extraction, justifying its 10-15 calls/contract cost for the highest-risk tier.

**Cons / failure modes:**
- Real-world incident: a hallucinated indemnification clause nearly caused a $2M liability exposure in week 1 of deployment — root-caused to missing citation verification.
- Real-world incident (insurance company case): deviation catch rate was only 8% before proper verification tooling, rising to 99.2% after.
- Long-context single-pass is cheapest ($0.51, 1 call) but has the lowest accuracy (85%/97%) — a clear cost/accuracy tradeoff, not a free win.
- ~7% of citations are unverifiable even after the full 5-stage cascade and must be rejected/flagged rather than surfaced with false confidence.
- Full-text diff for multi-document comparison is fast (5s) but only 75% accurate — inadequate alone for contract redlining; needs the clause+semantic+rule layer.

**When to use:** High-stakes document review where a single hallucinated clause has outsized financial/legal consequences — justifies the extra latency and the 5-stage verification cascade over a naive single-pass extraction. Full clause+LLM multi-document analysis (120s, 99%/98%) should be reserved for M&A-tier work, not routine contract review, given its cost.

---

## Chapter 21 — Design an Advanced RAG Platform

**Problem:** Build a general-purpose production RAG platform serving 100M documents / 1B chunks / 20M queries/day at p95 < 2.5s, spanning query planning, hybrid retrieval, reranking, context packing, and grounding verification as first-class stages.

**Core pattern/architecture:**
- Query planner/intent classifier routes each query to one of ~5 strategies: exact lookup, semantic, comparison, multi-hop (GraphRAG-style entity/relation traversal), and freshness-sensitive.
- Latency budget allocated explicitly per stage: auth 50ms, query rewrite 100ms, hybrid retrieval 180ms, graph expansion 80ms, reranking 250ms, context packing 40ms, generation TTFT 900ms, verification 300ms.
- Context packing rules: token budget reserved per evidence type, deduplication via MinHash/cosine similarity (>15% overlap threshold frees 20-30% of the token budget), stable citation IDs, explicit "lost in the middle" mitigation (placing highest-relevance evidence at prompt start/end, not buried mid-context).
- Grounding verifier: decomposes the generated answer into atomic claims, then checks each claim via entailment-based span matching against retrieved evidence, labeling each supported / contradicted / not-found.
- Parent-child retrieval: child chunks (128-256 tokens) drive recall, parent chunks (512-1024 tokens) are what's actually packed into the generation context.
- Advanced techniques: GraphRAG, HyDE, ColBERT late interaction, contextual compression (30-50% token reduction before packing), multi-vector documents.

**Pros:**
- Real-world case: a support assistant's faithfulness rose from a 78% baseline to 93% via query classification + BM25/vector fusion + cross-encoder reranking (a 70%→93% framing is used for the pre/post comparison).
- Real-world case: a legal assistant's parent-child retrieval + citation verification cut unsupported claims by 60%.
- Explicit per-stage latency budgeting makes the 2.5s p95 target auditable and regression-attributable rather than an emergent property.
- Contextual compression (30-50% token reduction) directly reduces both cost and "lost in the middle" risk before packing.

**Cons / failure modes:**
- Production bottlenecks catalogued: reranker saturation under load (mitigated by a semantic cache with only 15-25% hit rate — a real ceiling, not a full fix), ACL over-retrieval requiring fetching 2-3x the target set before filtering, stale indexes (CDC vs. polling tradeoff), context dilution when candidate similarity exceeds a 0.92 threshold (near-duplicate evidence crowds out diverse evidence), and embedding-migration risk (mitigated via shadow index with a 48-hour rollback window).
- Reranking is the single most expensive stage in the latency budget (250ms) and the primary cost-reduction lever discussed in the FAQ (5 ranked mitigation options, e.g., cache, smaller reranker, dynamic depth, distillation, skip-under-load).
- Citation-relevant-but-answer-wrong is called out explicitly as a distinct failure mode from retrieval failure — requires separate diagnostic tooling from a plain recall metric.

**When to use:** General enterprise RAG platforms serving multiple query types/tenants where a single fixed retrieval strategy would underperform across the mix — the query planner's routing to specialized strategies (multi-hop via GraphRAG, freshness-sensitive re-ranking, exact lookup bypassing semantic search) is the key differentiator from a simpler single-path RAG chapter like Chapter 6 or 7.

---

## Cross-Cutting Themes

- **Hybrid lexical+semantic retrieval fused via RRF (k=60) is the default everywhere it's discussed** (Ch. 6, 7, 15, 21): pure BM25 or pure dense retrieval consistently underperforms fusion by 5-12+ Recall/nDCG points across chapters (Ch. 7: BM25-only 0.55-0.65 → hybrid 0.80-0.88 Recall@10; Ch. 15: +22% nDCG@10 over BM25-only with CLIP+reranker).
- **Cross-encoder (or learned) reranking is a near-universal second stage** after bi-encoder/BM25 retrieval (Ch. 6, 7, 15, 17, 21), consistently adding meaningful precision (Ch. 6: +12 points Precision@3; Ch. 7: +5-12% Recall@5) at the cost of being the most GPU/latency-constrained stage in the pipeline — every chapter that uses it also documents a degrade-under-load fallback (skip reranker, reduce depth, cache).
- **Content-type-aware chunking recurs as a first-order lever, not an afterthought** (Ch. 6, 7): atomic Q+A pairs, clause-level policy/legal chunks with small overlap, section-level prose with 25% overlap, and row-group spreadsheet chunks with repeated headers all appear near-identically across chapters, with measured gains (Ch. 6: +8 points Recall@3 from content-aware vs. fixed-size chunking).
- **Freshness/staleness handling via TTL-based decay or re-indexing, not hard exclusion** (Ch. 6, 7, 21): stale content is demoted via a decay multiplier rather than removed outright, to avoid zero-result scenarios; paired with webhook/CDC-triggered re-indexing for critical updates (Ch. 6 policy webhook, Ch. 7 30-min freshness SLA via incremental HNSW, Ch. 21 CDC vs. polling tradeoff).
- **Grounding/citation verification as a mandatory post-generation gate** (Ch. 6, 17, 21): from a simple grounding-score threshold (Ch. 6, <0.7 triggers regeneration) to a full 5-stage citation verification cascade (Ch. 17) to atomic-claim entailment checking (Ch. 21) — all treat "the model said something plausible" as insufficient without traceability back to retrieved evidence.
- **Blue-green/alias-swap index deployment with an automated quality gate** (Ch. 6, 7): every re-index is validated against a benchmark query set (50-500 queries) with a Recall regression threshold before the production alias is atomically swapped, and the old index is kept hot briefly for rollback.
- **ACL/permission filtering must happen before reranking/packing, never post-response** (Ch. 7, referenced in Ch. 21's ACL over-retrieval bottleneck): post-hoc filtering leaks document existence metadata even when content is withheld — pre-filtering is the correctness-preserving default despite added query-time cost.
