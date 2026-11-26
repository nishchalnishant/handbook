---
title: "Part 2 Cards — RAG and Search (Ch 6, 7, 11, 12, 15, 17, 21)"
tags: [cards, rag, search]
---

# Part 2 Cards — RAG and Search

Every card here is **P2 (retrieve → fuse → filter → rerank → pack)** plus one domain twist. Learn the twist.

| Ch | The twist |
|---|---|
| 6 | Conversation memory + escalation |
| 7 | ACL-aware retrieval at enterprise scale |
| 11 | Structured extraction + arithmetic verification |
| 12 | Personalization + business constraints |
| 15 | Cross-modal embeddings + video time indexing |
| 17 | Exact citation grounding |
| 21 | Query planning, as a platform |

---

### Ch 6 — Design a Customer Support Chatbot
**One line:** Answer support questions from the KB, take safe actions, and hand off to a human gracefully.
**Shape:** Guard → Intent router → {FAQ cache | RAG | Action tool | Human} → Groundedness check → Reply
**Patterns:** P1, P2, P4

**3 ideas**
1. **Memory tiers:** last N turns verbatim, then a rolling summary, then extracted facts (order ID, issue) in a slot store.
2. **Intent routing first.** FAQ and cache hits never touch the LLM. Actions (refunds) go through a tool with policy checks.
3. **Escalation is a feature.** Trigger on low confidence, user frustration, repeated failure, or a policy topic. Hand off with a summary.

**2 trade-offs**
- Automation rate vs CSAT. Over-containment frustrates users.
- Long verbatim history (accurate, expensive) vs summary (cheap, lossy).

**Numbers:** Cache hit **30–40%**; small model takes **70–80%**.
**Soundbite:** *"The deflection metric I'd optimize is resolved-without-recontact, not just conversations closed by the bot."*

> [!question]- What are the three memory tiers?
> Recent turns verbatim; a rolling summary of older turns; structured slots/facts extracted (IDs, entities).

> [!question]- Name 4 escalation triggers.
> Low retrieval/answer confidence, negative sentiment or frustration, N failed attempts, and regulated or high-value topics (legal, refunds over a threshold). Plus an explicit request for a human.

> [!question]- How do you stop the bot inventing policy?
> Only answer from retrieved KB chunks, run a groundedness check on the output, and refuse or escalate when coverage is missing.

**Go deep:** [[Chapter 6 - Design a Customer Support Chatbot]] → "Conversation Memory Management" and "Escalation and Fallback Design".

---

### Ch 7 — Design an Enterprise Semantic Search Engine
**One line:** Search across all company documents and return only what each user is allowed to see.
**Shape:** Connectors → Parse → Chunk + ACL tags → Hybrid index → Query: rewrite → hybrid → **ACL filter** → rerank → answer + links
**Patterns:** P2, P4, P6, P9

**3 ideas**
1. **ACL-aware retrieval:** permissions are attached to every chunk and pre-filtered in the query. Sync ACL changes fast (minutes).
2. **Parsing at scale** (PDF, slides, tables) is the hard data problem. Use layout-aware parsers and keep the structure.
3. **Relevance tuning:** query rewriting, field boosting (title, recency), and click feedback feeding the reranker.

**2 trade-offs**
- Pre-filter (secure; can hurt ANN recall on sparse permissions) vs post-filter (fast, but **leaks**). Always pre-filter, and over-fetch if needed.
- Freshness vs indexing cost: incremental/CDC vs batch re-index.

**Numbers:** Retrieve **50–200 → rerank → 3–10**.
**Soundbite:** *"Permission filtering happens before ranking and before the LLM sees anything. A leak through a summary is still a leak."*

> [!question]- Why never post-filter by ACL after generation?
> The LLM has already seen the unauthorized content, so it can leak through the summary. Filtering also has to happen before rerank, so top-k isn't wasted.

> [!question]- What do you do when ACL pre-filtering kills ANN recall?
> Partition the index by tenant/group, use filtered-HNSW support, or over-fetch and widen ef_search.

> [!question]- How do permission changes propagate?
> Subscribe to identity-provider/source change events, then update chunk ACL metadata (no re-embedding). Target freshness in minutes.

**Go deep:** [[Chapter 7 - Design an Enterprise Semantic Search Engine]] → "ACL-Aware Retrieval".

---

### Ch 11 — Design a Financial Document Extraction System
**One line:** Turn messy financial PDFs into exact, auditable structured data.
**Shape:** OCR/layout → Table detect → LLM extract (schema-constrained) → **Arithmetic + cross-field checks** → Confidence → HITL queue
**Patterns:** P8

**3 ideas**
1. **Structured output enforcement:** JSON schema and constrained decoding. Every field carries a source span (page and bbox).
2. **Verify deterministically:** totals = sum of line items, balance sheet balances, dates are valid.
3. **Confidence-routed HITL:** low-confidence fields go to reviewers, and their corrections become training data.

**2 trade-offs**
- Specialized OCR+layout model vs a vision LLM end-to-end (simpler, but harder to audit).
- Automation rate vs error rate. In finance, choose precision.

**Numbers:** Field-level accuracy target ~99%+. Review only low-confidence fields.
**Soundbite:** *"The LLM proposes values; arithmetic and schema validators decide whether they're accepted."*

> [!question]- Name 3 deterministic checks for financial extraction.
> Line items sum to the total; assets = liabilities + equity; currency and date formats are valid; cross-document consistency (same figure across pages).

> [!question]- How does the system improve over time?
> Reviewer corrections are logged, then used as fine-tune / few-shot data with an eval gate before redeploying.

**Go deep:** [[Chapter 11 - Design a Financial Document Extraction System]] → "Hallucination Prevention for Financial Data".

---

### Ch 12 — Design a Personalized E-commerce Shopping Assistant
**One line:** A conversational shopping assistant that combines what the user likes with what's actually in stock and allowed.
**Shape:** Intent + slots → Profile fetch → Hybrid catalog search + **hard filters** (stock, price, region) → Personalized rerank → LLM explanation
**Patterns:** P1, P2, P9

**3 ideas**
1. **Hard constraints are filters, not prompts.** Stock, price and region are applied in the query.
2. **Profile–catalog fusion:** user embedding plus explicit preferences boost the rerank. Session signals beat stale profiles.
3. **Evaluate personalization online** (CTR, conversion, A/B), not just offline relevance.

**2 trade-offs**
- Personalization vs filter bubble/diversity.
- LLM-generated explanations (engagement) vs latency/cost. Generate them only for the top few items.

**Numbers:** Search under a few hundred ms; the LLM only writes text around retrieved items.
**Soundbite:** *"The LLM never invents a product. It only talks about items retrieval returned, and they're filtered by inventory."*

> [!question]- Why not put "in stock only" in the prompt?
> The LLM can ignore it, and it wastes context. Deterministic filters are guaranteed and cheaper.

> [!question]- Offline vs online metrics for personalization?
> Offline: NDCG/recall on historical clicks. Online: CTR, add-to-cart, conversion, revenue per session via A/B.

**Go deep:** [[Chapter 12 - Design a Personalized E-commerce Shopping Assistant]] → "Hybrid Search with Business Constraints".

---

### Ch 15 — Design a Multimodal Asset Search System
**One line:** Search images and videos using text or image queries.
**Shape:** Ingest → per-modality encoders (CLIP-style) + captions/OCR/ASR → shared vector space + text index → Cross-modal retrieval → Rerank
**Patterns:** P2, P9

**3 ideas**
1. **Shared embedding space** (CLIP/SigLIP) gives text↔image retrieval out of the box.
2. **Enrich with text:** captions, OCR and ASR transcripts let BM25 work on visual content too.
3. **Video = temporal segments:** shot/scene detection, keyframe embeddings, and timestamped results.

**2 trade-offs**
- Embed every frame (recall) vs keyframes (cost). Choose keyframes plus transcript.
- Off-the-shelf CLIP vs domain fine-tuned (better on niche assets, costs labeling).

**Numbers:** Storage scales with segments, not files. Estimate segments/video × vector size.
**Soundbite:** *"I index video as timestamped segments, so a result is a moment, not a 2-hour file."*

> [!question]- Why add captions/OCR when you have CLIP embeddings?
> CLIP is weak on text-in-image, exact names and fine detail. A text index adds lexical precision and supports hybrid search.

> [!question]- How do you return a moment in a video?
> Segment by shot/scene, embed keyframes and transcript windows per segment, store timestamps, then merge adjacent hits.

**Go deep:** [[Chapter 15 - Design a Multimodal Asset Search System]] → "Video Search and Temporal Indexing".

---

### Ch 17 — Design a Legal Contract Review System
**One line:** Flag risky clauses against a playbook, with citations that are provably exact.
**Shape:** Parse clauses → Classify clause type → Compare to playbook/template → Risk flags → **Citation verification** → Lawyer review
**Patterns:** P2, P8

**3 ideas**
1. **Exact grounding:** every claim quotes a span, which is verified by string match against the source.
2. **Playbook comparison:** retrieve the standard clause for each type and diff the deviations.
3. **Multi-document:** align clauses across versions/contracts by type, then compare pairwise.

**2 trade-offs**
- Recall on risky clauses (missing one is costly) vs reviewer fatigue from false flags.
- Long-context whole-contract (simple) vs clause-level pipeline (auditable, cheaper).

**Numbers:** Citation-verification pass rate ~100% is the bar. Anything unverified gets dropped.
**Soundbite:** *"If a quote doesn't string-match the contract, it doesn't ship. Verification is deterministic."*

> [!question]- Describe the citation verification cascade.
> Exact string match → normalized match (whitespace, quotes) → fuzzy match above a threshold → otherwise reject or flag. Never show an unverified quote.

> [!question]- How do you compare two contract versions?
> Segment into clauses, align by clause type and semantic similarity, diff the aligned pairs, and classify the risk delta.

**Go deep:** [[Chapter 17 - Design a Legal Contract Review System]] → "Exact Grounding and Citation Verification".

---

### Ch 21 — Design an Advanced RAG Platform
**One line:** RAG as a multi-tenant platform: query planning, multiple retrieval strategies, and built-in evaluation.
**Shape:** Query → **Planner** (rewrite / decompose / route) → Hybrid retrieve → RRF → ACL → Rerank → Pack → Generate → Cite-verify → Eval hooks
**Patterns:** P1, P2, P5, P8, P9

**3 ideas**
1. **Query planning:** classify the query, then rewrite (HyDE, multi-query), decompose multi-hop questions, or route to SQL/graph/vector.
2. **Context packing:** dedupe, order by relevance (avoid lost-in-the-middle), give citations stable IDs, and respect the token budget.
3. **Eval is part of the platform:** per-tenant golden sets, retrieval and generation metrics, and regression gates on index/prompt changes.

**2 trade-offs**
- Planning adds 100–300ms and some cost, but it's worth it only for complex queries. Route simple queries straight through.
- Long context (stuff everything in) vs RAG (precise, cheaper, citable). See [[N5 - Agentic RAG and Retrieval Upgrades]].

**Numbers:** **RRF k=60**; **50–200 → 3–10**.
**Soundbite:** *"Simple queries take the fast path; only complex, multi-hop ones pay for planning."*

> [!question]- What is HyDE and when does it help?
> Generate a hypothetical answer, embed it, and retrieve with it. It helps when queries are short or phrased very differently from the documents.

> [!question]- What is "lost in the middle" and the mitigation?
> Models under-use context in the middle of long prompts. Put the best chunks first (and last), and keep the pack small.

> [!question]- How do you detect whether bad answers come from retrieval or generation?
> Per-stage spans plus separate metrics: if context recall is low, retrieval broke; if recall is fine but faithfulness is low, generation broke.

**Go deep:** [[Chapter 21 - Design an Advanced RAG Platform]] → "Query Planning and Retrieval Strategy" and "RAG Evaluation and Operations".
