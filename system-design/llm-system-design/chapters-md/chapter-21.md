---
title: "Chapter 21: Design an Advanced RAG Platform"
tags: [llm, system-design, rag, retrieval, graphrag, reranking, grounding, case-study]
chapter: 21
part: case-studies
---

# Chapter 21: Design an Advanced RAG Platform

## Context

> [!info] Quick Reference
> - **Pattern:** Production RAG platform with query planning, hybrid retrieval, reranking, context packing, and grounding verification
> - **Scale:** 100M documents, 1B chunks, 20M queries/day, p95 < 2.5s for answer generation
> - **Key Techniques:** query rewriting, parent-child retrieval, BM25 + dense + graph retrieval, cross-encoder reranking, citation verification, freshness and ACL enforcement
> - **Primary Concerns:** retrieval recall, answer faithfulness, latency, access control, index freshness, cost
> - **Cross-references:** [[chapter-03|Chapter 3]] (vector infrastructure), [[chapter-05|Chapter 5]] (evaluation), [[chapter-07|Chapter 7]] (enterprise search), [[chapter-17|Chapter 17]] (grounding)

**Problem statement:** Design a reusable RAG platform that multiple product teams can use to answer questions over large, permissioned, frequently changing enterprise corpora with citations and measurable faithfulness.

### Real-World Examples

- A support assistant retrieves the right product manual only 70% of the time because single-shot vector search misses exact SKU names. Adding query classification, BM25 fusion, and cross-encoder reranking raises answer faithfulness from 78% to 93%.
- A legal assistant uses a long-context model with entire contracts but still misses relevant clauses buried in appendices. Switching to parent-child retrieval with citation verification catches clauses at section boundaries and reduces unsupported claims by 60%.

### Design Contract

Before proposing components, lock down the system contract:

| Dimension | Target | Why It Matters |
|---|---:|---|
| Corpus | 100M documents / 1B chunks | forces sharding, incremental indexing, and index lifecycle design |
| Query traffic | 20M queries/day, 2,500-3,000 peak QPS capacity | retrieval and reranking must scale independently |
| Freshness | p95 < 15 minutes from source update to searchable | stale RAG is a correctness bug, not just a UX issue |
| Security | 0 unauthorized chunks in prompt or response | ACL enforcement must happen before generation |
| Faithfulness | unsupported-claim rate < 2% | final answer must be evidence-constrained |
| Latency | p95 < 2.5s interactive answer path | query rewrite, retrieval, rerank, and verification need strict budgets |
| Debuggability | full trace for every sampled or failed request | teams need to know whether ingestion, retrieval, packing, or generation failed |

This contract prevents a common weak interview answer: "use embeddings and a vector DB." At production scale, the differentiator is not vector search itself; it is how the platform preserves structure, permissions, freshness, and evidence quality under latency and cost constraints.

---

## Step 1: Understand the Problem and Establish Design Scope

### Simulated Dialogue

**Interviewer:** Design an advanced RAG platform.  
**Candidate:** I will separate this into ingestion quality, retrieval recall, context assembly, generation, verification, and observability. [[glossary#RAG (Retrieval-Augmented Generation)|RAG]] failures usually look like model failures, but the root cause is often bad parsing, missing permissions, stale indexes, or weak reranking.

**Candidate:** What scale and freshness do we need?  
**Interviewer:** 100M documents, roughly 1B chunks. 20M user queries/day. New and updated documents must be searchable within 15 minutes.

**Candidate:** Are documents permissioned?  
**Interviewer:** Yes. Users must never see content they cannot access. ACL enforcement is mandatory before generation.

**Candidate:** What answer quality target matters most?  
**Interviewer:** Faithfulness. Every factual claim should be traceable to retrieved evidence. Unsupported claims should be blocked or rewritten.

### Functional Requirements

- Ingest documents from multiple sources and preserve structure, metadata, ACLs, and freshness timestamps.
- Support hybrid retrieval: lexical, dense vector, metadata filters, and graph/entity traversal.
- Rewrite and decompose complex queries into retrievable sub-queries.
- Rerank and pack evidence into a bounded token budget.
- Generate answers with citations and verify claims against evidence.
- Expose evaluation, tracing, and debugging tools for product teams.

### Non-Functional Requirements

- **Latency:** p95 < 2.5s for interactive answer generation.
- **Faithfulness:** unsupported-claim rate < 2% on audited samples.
- **Recall:** evidence recall@20 > 0.90 on golden query sets.
- **Security:** zero unauthorized chunk exposure.
- **Freshness:** updated content searchable within 15 minutes.
- **Cost:** retrieval + rerank + generation under a per-query budget.

### Back-of-the-Envelope Estimation

#### Corpus and Index Size

- Documents: 100M
- Avg chunks/document: 10
- Total chunks: `1B`
- Embedding dim: 768 float16 = `1.5KB/vector`
- Raw vector footprint: `1B * 1.5KB ~= 1.5TB`
- With ANN overhead, metadata, replicas: `5-8TB`

#### Query Throughput

- Queries/day: 20M
- Average QPS: `20M / 86,400 ~= 231`
- Peak multiplier: 8x
- Peak QPS: `~1,850`
- Capacity target with failover: `2,500-3,000 QPS`

#### Latency Budget

| Stage | Budget | Notes |
|---|---:|---|
| Auth + ACL context | 50ms | group expansion cached |
| Query rewrite/decomposition | 100ms | small model or rules |
| Hybrid retrieval | 180ms | lexical + vector parallel |
| Graph/entity expansion | 80ms | only for multi-hop queries |
| Reranking | 250ms | top 100 to top 12 |
| Context packing | 40ms | token budget + dedupe |
| Generation TTFT | 900ms | streaming |
| Claim verification | 300ms | sampled or full by risk tier |

---

## Step 2: Propose High-Level Design and Get Buy-In

### Core Architecture Components

- **Source Connectors:** Crawl SaaS apps, file stores, wikis, ticketing systems, and databases via change-data-capture events or polling. Each connector normalizes source-specific metadata (owner, ACL list, last-modified timestamp) into a canonical envelope before handing off to the processor, so downstream stages never need to know the origin system.
- **Document Processor:** Layout-aware parsing extracts text, tables, headings, images, and embedded links while preserving reading order. OCR fallback handles scanned PDFs; metadata normalization unifies author, date, and access-control fields across source schemas so the chunker can annotate every passage with provenance.
- **Chunking Service:** Emits both parent sections (512–1024 tokens) and child passages (128–256 tokens) from the same document. Storing both levels in parallel is the foundation of parent-child retrieval: the system retrieves precise child chunks for high recall, then fetches the enclosing parent section when more context is needed for generation.
- **Index Builder:** Writes each chunk to three indexes simultaneously — lexical (Elasticsearch/OpenSearch for BM25 and field boosting), vector (HNSW-based ANN for semantic similarity), and entity graph (edges linking named entities across documents). Atomic alias swaps let a new index version go live without downtime, and the prior alias remains available for instant rollback.
- **Query Planner:** Classifies the incoming query into one of five execution strategies (exact lookup, semantic, comparison, multi-hop, freshness-sensitive) using a lightweight intent classifier that adds fewer than 20 ms of overhead. Choosing the wrong strategy is one of the top causes of irrelevant retrieval results, making this the highest-leverage single component in the pipeline.
- **Retrieval Orchestrator:** Fans out simultaneously to BM25, dense vector, and graph indexes, then merges candidates using reciprocal rank fusion before applying ACL filters. Parallelizing retrieval across all three indexes keeps total retrieval latency under 180 ms even at 3,000 QPS, because each index query takes 50–80 ms and they run concurrently.
- **Reranker:** Applies a [[glossary#Cross-Encoder Reranking|cross-encoder]] or late-interaction model (ColBERT) to re-score the top-100 fused candidates and return the top-12 most relevant passages. Cross-encoders attend jointly to query and passage tokens, producing ranking accuracy 15–25 percentage points higher than bi-encoder retrieval alone, at the cost of O(k) forward passes — making the candidate pool size a critical cost lever.
- **Context Packer:** Deduplicates near-duplicate passages using MinHash or sentence-level embedding similarity, orders evidence by relevance and recency, and enforces a hard token budget so the LLM prompt never exceeds the [[glossary#Context Window|context window]]. Poor context packing — not retrieval — is the most common root cause of diluted or contradictory evidence reaching the model.
- **Answer Generator:** Calls the LLM with the packed evidence and a structured instruction to cite every factual claim with a chunk ID from the provided evidence set. [[glossary#Structured Output / Constrained Decoding|Structured output]] (JSON with claim-citation pairs) makes downstream grounding verification deterministic rather than dependent on regex parsing of free text.
- **Grounding Verifier:** Splits the generated answer into atomic claims, maps each claim to its cited span, and labels it as supported, contradicted, or not-found. Unsupported claims are either rewritten to hedge appropriately or removed entirely before the response is returned, keeping the platform-level unsupported-claim rate below 2%.
- **RAG Observability:** Records the full trace for every sampled or failed request: query rewrites, retrieval candidates with scores, ACL filter outcomes, reranking deltas, packed token counts, generation latency, and verifier labels. Without per-stage traces, product teams cannot distinguish ingestion bugs from retrieval bugs from generation bugs — all three look like "the answer was wrong."

### Pipeline A: Ingestion and Indexing

1. Source connector detects create/update/delete event.
2. Processor extracts text, tables, images, headings, links, ACLs, and timestamps.
3. Chunker emits parent sections and child passages.
4. Embedding service generates vectors with model version tags.
5. Entity extractor updates graph nodes and relations.
6. Index builder writes lexical, vector, graph, and metadata stores.
7. Index QA checks coverage, parse failures, duplicate chunks, and ACL completeness.
8. Alias swap promotes index version; rollback alias remains available.

### Pipeline B: Query and Answer

1. Gateway authenticates user and resolves ACL context.
2. Query planner classifies query type: exact lookup, semantic, analytical, comparison, or multi-hop.
3. Query rewrite generates normalized terms, synonyms, acronyms, and sub-queries.
4. Retrieval orchestrator runs BM25, dense retrieval, filters, and optional graph expansion in parallel.
5. Candidates are fused with reciprocal rank fusion and reranked.
6. Context packer selects diverse, recent, permissioned evidence.
7. Generator answers with citation IDs.
8. Grounding verifier checks claims against cited spans.
9. Trace is stored for debugging and evaluation.

### Request Flow Walkthrough

Example query: "What changed in the refund policy for enterprise customers last quarter?"

1. **Gateway:** authenticates the user and expands group memberships into an ACL filter.
2. **Query planner:** classifies this as freshness-sensitive and comparison-oriented.
3. **Query rewrite:** creates sub-queries for "refund policy," "enterprise customers," and "last quarter change log."
4. **Hybrid retrieval:** BM25 catches exact policy titles; dense retrieval catches semantically related policy pages; metadata filters constrain date range.
5. **Graph expansion:** follows links from current policy to change-log entries and policy-owner notes.
6. **Reranking:** scores candidate passages by query relevance and source authority.
7. **Context packing:** includes current policy, prior policy, relevant changelog, and effective-date metadata.
8. **Generation:** produces a concise answer with citations per claim.
9. **Verification:** checks each factual claim against cited spans; unsupported claims are removed or rewritten.
10. **Trace:** stores query rewrites, candidate IDs, scores, packed evidence, claim labels, and latency/cost breakdown.

### Developer-Facing Interfaces

Expose RAG as an internal platform API, not as a pile of product-specific retrieval code.

```json
{
  "query": "What changed in the refund policy for enterprise customers last quarter?",
  "user_context": {
    "tenant_id": "acme",
    "user_id": "u_123",
    "groups": ["legal", "enterprise-support"]
  },
  "constraints": {
    "freshness": "prefer_latest",
    "require_citations": true,
    "max_latency_ms": 2500,
    "risk_tier": "medium"
  },
  "retrieval_plan": {
    "strategy": "hybrid_graph",
    "top_k": 100,
    "rerank_to": 12
  }
}
```

Return both answer and provenance:

```json
{
  "answer": "Enterprise refund requests now require director approval for annual contracts over $250K.",
  "citations": [
    {"claim_id": "c1", "doc_id": "policy_944", "chunk_id": "ch_17", "span": "director approval..."}
  ],
  "verification": {
    "unsupported_claims": 0,
    "contradictions": 0
  },
  "trace_id": "rag_trace_789"
}
```

### Mermaid Architecture Diagram

```mermaid
flowchart LR
  user[User] --> gateway[Gateway Auth + ACL]
  gateway --> planner[Query Planner]
  planner --> rewrite[Query Rewrite]
  rewrite --> lexical[BM25 Index]
  rewrite --> vector[Vector Index]
  rewrite --> graph[Entity Graph]
  lexical --> fusion[Score Fusion]
  vector --> fusion
  graph --> fusion
  fusion --> acl[ACL Filter]
  acl --> rerank[Cross-Encoder Reranker]
  rerank --> packer[Context Packer]
  packer --> llm[Answer Generator]
  llm --> verifier[Grounding Verifier]
  verifier --> response[Cited Answer]

  sources[Source Systems] --> processor[Document Processor]
  processor --> chunker[Chunker]
  chunker --> embed[Embedding Service]
  chunker --> entity[Entity Extractor]
  embed --> vector
  chunker --> lexical
  entity --> graph
  processor --> docstore[Document Store]
  verifier --> traces[RAG Traces + Eval]
```

---

## Step 3: Design Deep Dive

### 1) Query Planning and Retrieval Strategy

The platform should not run the same retrieval path for every query. Exact identifiers, vague natural-language questions, multi-document comparisons, and multi-hop questions need fundamentally different execution plans. Routing them all through a single dense-vector retrieval path is the single most common cause of recall failures in production RAG systems — exact product codes and error IDs are often out-of-vocabulary for embedding models, while multi-hop questions require linking evidence across documents rather than ranking a single candidate pool.

> **Why an intent classifier that routes queries to different retrieval strategies:** A lightweight intent classifier (fine-tuned BERT or even a rules-based heuristic over token patterns) adds fewer than 20 ms to the query path but can raise evidence recall@20 by 10–18 percentage points by routing queries to the retrieval strategy that matches their structure. At 20M queries/day, an 18% recall improvement translates directly into millions of additional queries getting correct answers.

| Query Type | Example | Best First Stage | Extra Step |
|---|---|---|---|
| Exact lookup | "ERR-4827 timeout" | BM25 with field boosting on product ID and error code fields | Boost exact-match fields to weight 10x over body text so rare identifiers surface at rank 1 instead of rank 30 |
| Semantic how-to | "How do I rotate keys?" | Dense retrieval + BM25 fusion (RRF) for vocabulary-independent recall | Rerank top-30 sections with a cross-encoder to surface procedural content over conceptual pages |
| Comparison | "Compare policy A and B" | Parent-chunk retrieval to fetch full section context for each named entity | Pack both policy sections side by side with section headers intact so the LLM can diff them without losing structural cues |
| Multi-hop | "Which customers use the deprecated API?" | Graph traversal from the API entity node to customer-relationship edges | Decompose into sub-queries ("which API is deprecated?", "which customers have contracts referencing that API?") and execute them sequentially |
| Freshness-sensitive | "latest refund policy" | Metadata date filter applied before vector scoring, not as a post-filter | Pin results to the top-3 most recently indexed document versions before reranking to prevent an older high-scoring document from outranking a newer update |

Recommended design:

1. Use a fast classifier — a fine-tuned DistilBERT or even keyword heuristics — to choose a retrieval plan in under 20 ms, because incorrect plan selection propagates errors through every downstream stage.
2. Generate 2–5 query rewrites (synonym expansion, acronym normalization, sub-query decomposition) only for semantic and multi-hop query types where a single surface form is likely to miss relevant passages with different vocabulary.
3. Retrieve broadly (top-100 candidates per index), fuse with reciprocal rank fusion, and then rerank narrowly to top-12, so the reranker sees a diverse candidate pool without receiving so many candidates that its latency budget is exceeded.
4. Store the retrieval plan in the trace alongside the selected strategy, candidate counts per index, and fusion scores, so that when an answer is wrong, engineers can determine within seconds whether the failure was upstream (wrong plan or missed candidate) or downstream (correct candidate, wrong packing or generation).

### 2) Context Packing and Grounding

RAG quality often collapses after retrieval because the prompt includes redundant or weak evidence. A naive approach stuffs the top-k chunks into the context window in rank order — but this typically includes 3–5 near-duplicate passages that waste tokens, buries the most relevant span in the middle of the window (the position LLMs attend to least reliably), and omits structural cues like section headings that help the model interpret the evidence correctly.

> **Why a deterministic context-packing strategy placing key evidence first and last:** Studies on "lost in the middle" attention patterns show that LLMs using GPT-4-class models retrieve information from the start and end of long contexts with 30–40% higher accuracy than from the middle. A deterministic packing strategy — placing the highest-confidence evidence first and last, and filling middle positions with supporting context — exploits this pattern without changing the model or retrieval logic.

Context packing rules:

- Reserve token budget by evidence type: allocate slots for definitions (what a term means), procedures (step-by-step instructions), exceptions (edge cases), and examples (concrete instances) rather than filling all slots with the top-ranked passages, which are often all the same type and leave gaps the LLM fills with hallucination.
- Keep parent section titles with child chunks: including the enclosing heading ("§3.2 Refund Policy — Enterprise Tier") costs roughly 10–15 tokens but gives the LLM critical disambiguation context that prevents it from applying a consumer-tier rule to an enterprise query.
- Prefer diverse sources over five near-duplicate passages: use MinHash or cosine similarity at the sentence level to detect passages that differ by fewer than 15% of tokens, and keep only the highest-scoring representative from each cluster — this routinely frees 20–30% of the token budget for genuinely different evidence.
- Keep citation IDs stable through generation and verification: assign chunk IDs before the prompt is assembled and do not re-sort evidence after IDs are embedded in the prompt, because changing the order after ID assignment causes the verifier to look up the wrong spans.
- Include freshness and source authority metadata when conflicts exist: if two passages give different values for the same fact, surfacing their timestamps and source trust scores (e.g., "official policy document, updated 3 days ago" vs. "wiki page, updated 11 months ago") gives the LLM and verifier the information needed to prefer the authoritative value.

Grounding verifier:

1. Split the generated answer into atomic claims using dependency parsing or an LLM-based claim-decomposition prompt that identifies each independently verifiable assertion — e.g., "director approval is required" and "threshold is $250K" are two separate claims even if written in one sentence.
2. Map each claim to one or more cited spans from the packed context, using string overlap, semantic similarity, or a small entailment model; this step catches cases where the LLM paraphrased the evidence correctly but also added an embellishment that has no span.
3. Label each claim as supported (entailed by cited span), contradicted (cited span states the opposite), or not-found (no cited span covers the claim); the label drives the remediation action rather than a single binary pass/fail for the whole answer.
4. Rewrite hedged alternatives for unsupported claims ("The policy may require director approval — verify with your account manager") before returning, rather than silently removing them, so the user is informed that the system could not find evidence rather than receiving a truncated answer with no explanation.
5. Escalate to "I do not have enough evidence to answer" when critical claims — those covering the core assertion of the query — fail verification, because a partial answer that confirms peripheral details while omitting the main fact is more misleading than a transparent non-answer.

### 3) RAG Evaluation and Operations

Evaluation must measure each stage separately because a failure at ingestion is invisible to retrieval metrics, a failure at retrieval is invisible to generation metrics, and a failure at generation is indistinguishable from a retrieval failure without per-stage instrumentation. End-to-end accuracy metrics alone lead teams to optimize the wrong stage — the most common mistake is fine-tuning the generator when the actual problem is that the correct evidence was not retrieved in the first place.

> **Why measure each RAG stage separately rather than only end-to-end accuracy:** RAG pipelines have at least four independent failure modes — parse failure (document content not indexed), retrieval failure (correct document not ranked in top-k), packing failure (correct chunk retrieved but dropped or buried), and generation failure (correct evidence present but claim not grounded). Each mode requires a different fix: a parse failure needs a better PDF parser, not a better LLM. Without stage-level metrics, teams burn weeks improving the wrong component.

| Metric | Stage | Target | What Failure Looks Like |
|---|---|---:|---|
| Parse coverage | ingestion | > 99% docs parsed or explicitly failed with error code | Silently empty chunks appear in the index, causing zero-evidence responses for queries over the affected documents; often discovered only when users report that a specific document is never cited |
| Evidence recall@20 | retrieval | > 0.90 against a golden query-document set | Golden queries return fewer than 9 of 10 expected documents in the top-20 candidates; check whether failures cluster around specific document types, time ranges, or ACL groups |
| MRR/NDCG | ranking | Baseline established on domain-specific query log; track week-over-week delta | A drop in NDCG of more than 3 points without a model change indicates a data distribution shift in newly ingested documents |
| Context precision | packing | > 0.75 relevant tokens in packed prompt | Token budget consumed by off-topic passages; measure by annotating packed prompts on a 500-query sample and computing the fraction of tokens that appear in a human-verified relevant span |
| Unsupported-claim rate | generation | < 2% on audited weekly sample of 1,000 answers | Any claim with no corresponding cited span passes through the verifier; re-examine the verifier's entailment threshold and consider lowering it from 0.7 to 0.6 cosine similarity |
| Citation accuracy | verification | > 95% of cited spans actually contain the claimed information | A citation points to a chunk that discusses a related but different policy; often caused by chunk boundaries splitting a sentence so the key fact lands in the next sibling chunk |
| Freshness lag | indexing | p95 < 15 min from source update to searchable chunk | Lag spikes during business-hours indexing bursts; add backpressure to the embedding queue and monitor queue depth rather than only the alias-swap timestamp |

### Production Bottlenecks and Mitigations

- **Reranker saturation:** At 3,000 QPS, a 250 ms cross-encoder over top-100 candidates can consume 4–6 GPU-seconds per query, making the reranker the most expensive per-query component. Cache rerank results for identical or near-identical query+candidate sets using a 64-bit fingerprint of the sorted candidate IDs; typical cache hit rates of 15–25% on enterprise corpora reduce reranker load proportionally. Route low-risk queries (e.g., FAQ lookups flagged by the query planner) to a cheaper bi-encoder re-scorer that runs in under 30 ms at the cost of 8–12% ranking quality.
- **ACL filter removes all candidates:** When a user queries content they lack permission to see, naively applying the ACL filter post-retrieval yields zero candidates and an uninformative "no results found" response. Over-retrieve 2–3x the normal top-k before filtering so that even after ACL removal there are 12–15 permissioned candidates to rerank. Track zero-evidence queries as a separate counter from true no-result queries (topics genuinely absent from the corpus) so that access-control gaps surface in monitoring before users escalate them as bugs.
- **Stale indexes:** Connector polling intervals and queue backlogs mean that source updates can sit unindexed for 20–60 minutes during high-ingestion windows, violating the 15-minute freshness SLA. Use change-data-capture events (Kafka, Pub/Sub) rather than polling as the primary mechanism, and run a daily reconciliation job that compares source inventory checksums against indexed document counts to catch connectors that silently fell behind.
- **Context dilution:** Even with a 128K-token context window, filling it with 100 near-duplicate passages reduces generation accuracy because the LLM attends to the noise equally with the signal. Enforce evidence diversity by computing pairwise cosine similarity across reranked candidates and dropping any passage with similarity > 0.92 to an already-selected passage, even if the context window has room. A diverse 8-passage prompt routinely outperforms a 20-passage prompt drawn from a single high-scoring document cluster.
- **Embedding model migration:** Switching embedding models (e.g., from text-embedding-ada-002 to a fine-tuned domain model) invalidates all existing index vectors, requiring a full re-index that can take days for 1B chunks. Run the new model in a shadow index in parallel before cutting over; compare evidence recall@20 on a golden query set between the old and new indexes before promoting the alias, and keep the old index live for 48 hours post-swap to enable rapid rollback without re-ingestion.

### Advanced Techniques

- **[[glossary#GraphRAG|GraphRAG]]:** Build an entity and relation graph alongside the vector index, where nodes are named entities (products, policies, people, APIs) and edges are typed relations extracted by an NER + relation extraction model. For multi-hop questions like "which customers are affected by the deprecation of API v2?", graph traversal finds paths that pure vector search cannot — a vector search for "affected customers" will not naturally surface the API-to-customer-contract edge that answers the question.

  > **Why:** Vector similarity finds semantically related passages, but it cannot follow a chain of relationships across documents. Graph traversal is O(depth × branching-factor) rather than O(corpus-size), making it the only practical approach for questions that require joining facts from documents that share no vocabulary.

- **HyDE (Hypothetical Document Embeddings):** Prompt the LLM to generate a short hypothetical answer or document before retrieval, then embed that hypothetical and use it as the retrieval query instead of the raw question. This works because the hypothetical answer is written in the same vocabulary and style as real corpus documents, closing the query-document vocabulary gap that causes vague questions to retrieve off-topic results.

  > **Why:** User queries are often 5–15 tokens of natural language; corpus documents are 200–500 tokens of domain-specific prose. The embedding space for these two distributions partially overlaps, and HyDE effectively translates the query into the document distribution, improving recall by 8–15% on knowledge-base questions with technical vocabulary without requiring any query-time latency beyond a fast LLM call.

- **Parent-child retrieval:** Index child passages of 128–256 tokens for high-precision embedding recall (short passages have less noise and closer alignment between embedding and content), but when a child passage is selected by the reranker, fetch its parent section (512–1024 tokens) to pack into the prompt. This two-level structure provides the best of both worlds: retrieval precision from small chunks and generation quality from full context.

  > **Why:** Embedding a 1,024-token section dilutes the embedding with multiple topics, reducing retrieval recall for any individual claim in the section. But generating an answer from a 128-token child chunk often leaves out the surrounding context the LLM needs to reason correctly. Parent-child retrieval decouples these two concerns, and teams that adopt it typically report 10–20% improvement in answer completeness without any change to the retrieval model.

- **ColBERT-style late interaction:** Rather than encoding query and passage into a single vector each (bi-encoder) or concatenating them for a single score (cross-encoder), ColBERT retains token-level embeddings for both query and passage and computes relevance as the sum of maximum-similarity scores across query tokens. This captures fine-grained term-level matching that bi-encoders miss, at a cost of 32 bytes × sequence-length per passage rather than 1,536 bytes per passage.

  > **Why:** Cross-encoder reranking is 15–25% more accurate than bi-encoder retrieval but requires O(k) forward passes at inference time, making it 50–100x more expensive per query. ColBERT late interaction achieves 80–90% of cross-encoder accuracy at roughly 5x the cost of bi-encoder retrieval, making it the right operating point for high-recall, cost-sensitive production workloads.

- **Contextual compression:** After reranking, pass each selected passage through an extraction prompt that identifies the 2–4 sentences most directly relevant to the query and discards the rest before packing. This can reduce average packed token count by 30–50% for dense passages, freeing budget for more diverse evidence or a more detailed system prompt.

  > **Why:** Reranking selects the right passages but does not trim them — a highly ranked 300-token passage may contain only 50 tokens of directly relevant content. Contextual compression converts high-recall retrieval into high-precision context, which is especially valuable for models with limited context windows or when packing evidence from many sources simultaneously.

- **Multi-vector documents:** Index the same document under multiple vector representations — the title embedding, the summary embedding, body chunk embeddings, table cell embeddings, and entity name embeddings — and search all of them at query time. This ensures that a query for a concept mentioned only in a table caption or document title is not missed because the body-chunk embedding did not capture it.

  > **Why:** A single embedding per chunk cannot represent all retrieval surfaces equally well. A query for "quarterly revenue" will match a financial table's summary embedding but may miss a chunk whose body discusses methodology with only a parenthetical mention of the revenue figure. Multi-vector indexing adds index storage overhead (approximately 5x for five embedding types) but raises recall@20 by 5–12% for structured documents with distinct title, summary, and table regions.

---

## Step 4: Wrap Up

### Final Design Summary

The design treats RAG as a multi-stage retrieval and verification system, not a prompt pattern. Ingestion preserves structure and permissions, query planning selects the retrieval path, hybrid retrieval maximizes recall, reranking improves precision, context packing controls token quality, and grounding verification blocks unsupported claims.

### Wrap-Around Concerns

- **Risk:** unauthorized evidence reaches the prompt. Mitigation: enforce ACLs before reranking and again before packing.
- **Risk:** long context hides weak retrieval. Mitigation: measure evidence recall and context precision separately.
- **Risk:** product teams cannot debug failures. Mitigation: store full traces with query rewrites, retrieved candidates, scores, citations, and verifier labels.

---

## Step 5: Interviewer Curveballs

### Interviewer Follow-ups & Frequently Asked Questions (FAQ)

Q: Why not put all documents into a 1M-token context model?  
**The Ideal Answer:** Long-context models reduce some retrieval engineering complexity for small, well-scoped document sets — for example, analyzing a single 200-page contract — but they do not solve the fundamental problems of a production enterprise RAG platform. At 100M documents and 1B chunks, no context window can hold the entire corpus, so retrieval remains mandatory. ACL enforcement cannot be satisfied by stuffing all documents into the prompt — a user must never see content they are not permitted to access, and the only reliable enforcement point is filtering before context assembly. Freshness is also unsolved: even a 1M-token model cannot continuously update its context as documents change. Cost scales linearly with context length: processing 100K tokens costs roughly 100x more than processing 1K tokens at current API pricing, and at 20M queries/day the budget impact is prohibitive. Finally, "lost in the middle" attention degradation means that evidence quality decreases non-linearly as context grows — a 1M-token context is not 1,000x more effective than a 1K-token context. The right architecture uses retrieval to find the specific evidence relevant to each query, then uses long context selectively for queries (such as document summarization or comparison) where the full document is genuinely needed.

**Deep Dive & Trade-offs:**
- At 100M documents and 1B chunks, the corpus dwarfs any context window by orders of magnitude, so retrieval is not an optimization but a hard requirement; long context only removes retrieval for narrowly scoped single-document tasks.
- ACL enforcement must filter before context assembly — stuffing all documents into a prompt structurally cannot enforce per-user permissions, making the long-context approach a security non-starter for enterprise data.
- Cost scales roughly linearly with context length (100K tokens costs ~100x a 1K-token call), so at 20M queries/day a max-context strategy is prohibitively expensive even where it is technically feasible.
- "Lost in the middle" attention degradation means quality does not scale with context size; a 1M-token context is not 1,000x more effective than a focused 1K-token context, so selective retrieval also wins on answer quality, not just cost.

**The Interviewer's Rubric:** A strong answer recognizes that long context and retrieval solve different problems and names the specific dimensions — scale, ACL, freshness, cost, and attention degradation — where a max-context approach fails for a production platform. The rubric penalizes answers that treat a large context window as a wholesale replacement for retrieval, or that miss the security and cost implications entirely.

Q: The answer is wrong but the cited documents are relevant. What failed?  
**The Ideal Answer:** This failure pattern — relevant documents cited, incorrect answer produced — is diagnostic of a packing or generation failure rather than a retrieval failure, and it is important to distinguish between several sub-cases. First, check whether the exact span supporting the correct answer was included in the packed context or was dropped during the diversity or token-budget enforcement step. Second, check whether conflicting evidence was included alongside the correct evidence — if the prompt contains two passages with contradictory values, the LLM will often produce a plausible-sounding blend that is factually wrong. Third, check whether the grounding verifier's entailment threshold is too permissive, allowing a claim to be labeled "supported" by a span that merely discusses the same topic without actually asserting the claimed value. The fix requires claim-level evaluation: annotate the packed context with the ground-truth span for each expected claim, and measure whether the LLM reads the correct value from that span in isolation — this isolates generation faithfulness from retrieval quality.

**Deep Dive & Trade-offs:**
- Distinguish three sub-cases: the supporting span was dropped during diversity or token-budget enforcement, conflicting evidence was packed alongside the correct evidence, or the grounding verifier's entailment threshold is too permissive.
- When two contradictory passages are packed together, the model often emits a plausible blend that is factually wrong; deduplication and conflict detection at packing time matter as much as retrieval recall.
- A grounding verifier that labels a claim "supported" because a span merely shares the topic — rather than asserting the specific value — produces false confidence; tightening the entailment threshold trades recall of supported claims against precision.
- The diagnostic fix is claim-level evaluation: annotate the ground-truth span per expected claim and test whether the model reads the right value from that span in isolation, separating generation faithfulness from retrieval quality.

**The Interviewer's Rubric:** A strong answer immediately classifies this as a packing or generation failure rather than a retrieval failure and enumerates the specific sub-cases with a concrete isolation test. The rubric penalizes answers that conflate citation relevance with answer correctness or that propose re-tuning retrieval when the evidence was already present.

Q: Your RAG system misses newly updated policies. How do you debug?  
**The Ideal Answer:** Freshness failures require tracing the document's journey through every stage of the ingestion pipeline. Start by checking the source connector: verify that the update event was emitted by the source system and received by the connector within the expected window, because connectors based on polling can miss rapid successive updates if two changes land between poll cycles. Next, check the processing queue: confirm the document entered the parsing and chunking queue and was not silently dropped due to a transient error or malformed metadata. Check the embedding job: large documents generate many chunks and can cause embedding queue backpressure that delays write-through to the vector index. Check the alias swap: a new document may be fully indexed in the write alias but not yet visible under the read alias if the swap hasn't run. Finally, check cache layers: if query results are cached by query hash, a user querying the same question within the cache TTL will see stale results even after the index is updated. Freshness SLA violations almost always originate in connectors or queues, not in the vector search itself.

**Deep Dive & Trade-offs:**
- Trace the document stage by stage: source connector, processing/parsing queue, embedding job, alias swap, and cache layers — each is a distinct point where an update can stall or be silently dropped.
- Polling-based connectors can miss rapid successive updates when two changes land between poll cycles; event-driven connectors avoid this but require the source system to emit reliable change events.
- Large documents generate many chunks and can cause embedding-queue backpressure, delaying write-through; a freshly indexed document may also be live in the write alias but invisible under the read alias until the swap runs.
- Query-hash result caches can serve stale answers within the TTL even after the index updates, so cache invalidation on document change must be part of the freshness contract.

**The Interviewer's Rubric:** A strong answer treats freshness as a pipeline-tracing problem and walks each stage from connector to cache rather than jumping straight to the vector index. The rubric rewards naming connectors and queues as the most common culprits and penalizes answers that assume the search layer is at fault without ruling out ingestion and caching.

Q: How do you handle a query that spans multiple security domains where the user only has access to some?  
**The Ideal Answer:** This is one of the hardest correctness problems in enterprise RAG, and naive implementations get it wrong in ways that are both a security violation and a quality regression. The correct approach is to apply ACL filters per-chunk before any candidates are surfaced to the reranker or packer, not at the response level. This means the retrieval orchestrator must expand the user's group memberships into a full permission set before fanning out to indexes — typically via a cached group-expansion service that resolves nested group hierarchies and avoids N+1 permission lookups per query. The answer should then be generated only from permissioned chunks, with no leakage of unpermissioned content into the prompt even as negative context. If the system detects that the query spans a domain where the user has no access, the response should state "I do not have access to information in [domain] that may be relevant to your question" — informing the user of the limitation rather than silently returning a partial answer that omits critical evidence. Audit logging must record which chunks were filtered for every query, so compliance teams can verify that ACL enforcement operated correctly for any given request.

**Deep Dive & Trade-offs:**
- Apply ACL filters per-chunk before candidates reach the reranker or packer, never at the response level; filtering late risks unpermissioned content leaking into the prompt even as negative context.
- Expand the user's group memberships into a full permission set before fan-out, ideally via a cached group-expansion service that resolves nested hierarchies and avoids N+1 permission lookups per query.
- When the query spans a domain the user cannot access, explicitly inform them ("I do not have access to information in [domain]...") rather than silently returning a partial answer that omits critical evidence — silent omission is both a quality regression and a trust failure.
- Record which chunks were filtered per query in the audit log so compliance can verify enforcement after the fact; without this, ACL correctness is unprovable.

**The Interviewer's Rubric:** A strong answer enforces ACLs per-chunk before context assembly and recognizes that silent partial answers are a quality failure in addition to the security risk. The rubric penalizes response-level filtering, leaking unpermissioned content as negative context, and omitting the audit-logging requirement.

Q: Your vector index recall drops after a major corpus update. How do you investigate?  
**The Ideal Answer:** A sudden drop in retrieval recall@20 after a large ingestion batch is most commonly caused by one of three issues. First, index shard imbalance: if the new documents were all routed to a subset of shards due to a partitioning bug, those shards become hotspots with degraded ANN accuracy because HNSW graph quality degrades when a shard's local graph is rebuilt incrementally with a large skewed batch. Fix by monitoring per-shard document counts and recall metrics separately. Second, embedding model version mismatch: if some documents were embedded with the old model and some with the new model before a migration was fully completed, the vector space is now a mixture of two distributions and nearest-neighbor search gives unreliable results. Fix by enforcing a model version tag on every chunk and rejecting cross-version comparisons at query time until re-indexing is complete. Third, tokenization changes: if the chunker's sentence boundary or token-count logic changed, new chunks may be significantly longer or shorter than expected, shifting the embedding distribution. Bisect by running the golden query set against the index snapshot just before the ingestion batch and comparing recall to the post-batch index.

**Deep Dive & Trade-offs:**
- Shard imbalance from a partitioning bug routes new documents to a subset of shards, degrading ANN accuracy because HNSW graph quality drops when a shard's graph is rebuilt incrementally with a large skewed batch; monitor per-shard counts and recall separately.
- A partial embedding-model migration leaves the vector space as a mixture of two distributions, making nearest-neighbor search unreliable; enforce a model-version tag per chunk and reject cross-version comparisons until re-indexing completes.
- Tokenization or sentence-boundary changes in the chunker shift chunk lengths and therefore the embedding distribution, silently moving recall even when nothing else changed.
- Bisect by replaying the golden query set against the pre-batch index snapshot versus the post-batch index to localize the regression to the ingestion event.

**The Interviewer's Rubric:** A strong answer offers a ranked differential — shard imbalance, version mismatch, tokenization drift — each with a concrete detection method, rather than a single guess. The rubric rewards the snapshot-bisection technique and per-shard observability, and penalizes answers that blame the embedding model generically without proposing how to confirm it.

Q: How do you A/B test a new retrieval model without exposing users to degraded quality?  
**The Ideal Answer:** Shadow evaluation and offline replay are the two standard approaches, and they should be used in sequence before any user-facing rollout. In shadow evaluation, route every live query to both the current and new retrieval models simultaneously, collect candidate sets from both, but serve only the current model's results to users. Score both candidate sets against the user's eventual engagement signal (click, thumbs-up, follow-up query) to estimate relative quality without any quality risk. For a more rigorous comparison, build a replay dataset of 10,000–50,000 historical queries with human-annotated relevant documents and compute recall@20 and NDCG for both models offline before any live traffic exposure. Once both offline and shadow metrics confirm the new model is non-inferior on 95% confidence intervals, roll out to 5% of traffic using a feature flag, monitor retrieval recall and downstream answer faithfulness for 24–48 hours, and expand gradually. Keep the old index live until the rollout reaches 100% so that rollback requires only a flag flip rather than a re-index.

**Deep Dive & Trade-offs:**
- Shadow evaluation routes every live query to both models but serves only the current one, scoring both candidate sets against eventual engagement signals to estimate relative quality at zero user risk.
- Offline replay over 10,000–50,000 historical queries with human-annotated relevance gives rigorous recall@20 and NDCG comparisons before any live exposure; run it first, then shadow, then a gated rollout.
- Gate the 5% canary on both offline and shadow metrics being non-inferior at 95% confidence, then expand gradually while watching retrieval recall and downstream answer faithfulness for 24–48 hours.
- Keep the old index live to 100% rollout so rollback is a flag flip rather than a costly re-index — the rollback path must be cheaper than the failure it guards against.

**The Interviewer's Rubric:** A strong answer sequences offline replay, shadow evaluation, and a metric-gated canary rather than jumping straight to live A/B exposure. The rubric rewards specifying the confidence bar for promotion and a cheap flag-flip rollback, and penalizes rollouts that risk user-facing quality before any offline or shadow validation.

Q: How would you reduce the cost of the reranker at 20M queries/day without significantly hurting quality?  
**The Ideal Answer:** At 20M queries/day and a 250 ms cross-encoder reranker over top-100 candidates, the reranker alone can cost hundreds of GPU-hours per day. The most impactful cost reduction strategies, in order of implementation complexity, are: (1) Cache rerank results keyed on a fingerprint of the sorted candidate chunk IDs — identical candidate sets from repeated queries hit the cache; enterprise corpora typically yield 15–25% cache hit rates on popular topics. (2) Reduce the candidate pool from top-100 to top-50 or top-30: precision loss is typically less than 3% NDCG while halving the reranker's compute per query. (3) Use a cheaper early-exit reranker that applies the full cross-encoder only to candidates where the bi-encoder score difference is below a confidence threshold — high-confidence top-1 results bypass the cross-encoder entirely. (4) Classify queries by risk tier: informational or FAQ queries route to a bi-encoder re-scorer (30 ms, 1/10th the cost), while high-stakes or ambiguous queries route to the full cross-encoder. (5) Adopt ColBERT-style late interaction as the primary ranker: it achieves 80–90% of cross-encoder accuracy at 5x bi-encoder cost rather than 50–100x, cutting the cost per query by an order of magnitude while retaining most precision gains.

**Deep Dive & Trade-offs:**
- Rerank caching keyed on a fingerprint of the sorted candidate chunk IDs captures repeated candidate sets — enterprise corpora typically yield 15–25% hit rates on popular topics for near-zero quality cost.
- Shrinking the candidate pool from top-100 to top-50 or top-30 roughly halves reranker compute for typically under 3% NDCG loss; the precision/cost curve flattens quickly past the top candidates.
- Confidence-based early exit applies the full cross-encoder only when bi-encoder score gaps are narrow, and risk-tier routing sends FAQ-style queries to a 30 ms bi-encoder re-scorer while reserving the cross-encoder for high-stakes or ambiguous queries.
- ColBERT-style late interaction is the structural lever: ~80–90% of cross-encoder accuracy at 5x bi-encoder cost rather than 50–100x, cutting per-query cost by an order of magnitude.

**The Interviewer's Rubric:** A strong answer orders the levers by implementation complexity and quantifies the quality cost of each, distinguishing cheap caching and pool-trimming from the architectural shift to late interaction. The rubric rewards explicit precision/cost trade-offs with numbers and penalizes blanket "use a smaller model" answers that ignore the quality impact.

Q: A product team wants to add their own document collection to the RAG platform. What do you require of them?  
**The Ideal Answer:** Treating the RAG platform as a multi-tenant service requires a clear onboarding contract that protects both data quality and platform stability. The ingesting team must supply: (1) a source connector or a structured push API call for each document, with a guaranteed event or polling endpoint for create/update/delete changes; (2) an ACL mapping in a canonical format (user-ID or group-ID allowlists per document) — the platform does not infer permissions from document content; (3) metadata fields conforming to the platform schema: document ID, source system, content type, author, last-modified timestamp, and tenant namespace — missing required fields cause the document to be quarantined, not silently ingested with defaults; (4) a representative golden query set of at least 200 question-document pairs that the platform uses to establish a retrieval recall baseline for the new collection and to detect future regressions; (5) a designated owner and an on-call escalation path, because the platform can alert when ingestion failure rates spike but cannot diagnose source-system outages without domain knowledge. In return, the platform provides a per-collection dashboard with parse coverage, freshness lag, retrieval recall, and query volume metrics, giving the product team visibility into the health of their data without requiring them to understand the internals of the indexing pipeline.

**Deep Dive & Trade-offs:**
- Require a source connector or push API with reliable create/update/delete change signals, plus an explicit ACL mapping in canonical form — the platform never infers permissions from document content.
- Enforce a metadata schema (doc ID, source system, content type, author, last-modified, tenant namespace) and quarantine documents with missing required fields rather than ingesting them with silent defaults that corrupt downstream filtering.
- Demand a golden query set of at least 200 question-document pairs to establish a per-collection recall baseline and catch future regressions, plus a designated owner and on-call path since the platform can detect failures but not diagnose source-system outages.
- In exchange the platform offers a per-collection dashboard (parse coverage, freshness lag, recall, query volume), making the contract a two-way SLA rather than a one-sided requirement.

**The Interviewer's Rubric:** A strong answer frames onboarding as a multi-tenant contract that protects platform stability and data quality, specifying connector, ACL, schema, golden set, and ownership requirements. The rubric rewards quarantine-on-missing-metadata and the reciprocal observability dashboard, and penalizes answers that let the platform infer ACLs or accept unvalidated data.

---

## Practical Implementation

### Code Block 1: Parent-Child Chunker with ACL Annotation

This chunker produces both parent sections and child passages from a structured document object, and annotates every chunk with the document's ACL list, last-modified timestamp, and source system. The parent-child relationship is stored via a `parent_id` field so the context packer can fetch the enclosing section when a child chunk is selected.

```python
import hashlib
from dataclasses import dataclass, field
from typing import Optional
import tiktoken

ENCODER = tiktoken.get_encoding("cl100k_base")

@dataclass
class Chunk:
    chunk_id: str
    parent_id: Optional[str]
    doc_id: str
    text: str
    token_count: int
    level: str          # "parent" | "child"
    section_title: str
    acl: list[str]
    source_system: str
    last_modified: str  # ISO-8601
    metadata: dict = field(default_factory=dict)

def _make_id(doc_id: str, suffix: str) -> str:
    return hashlib.sha256(f"{doc_id}::{suffix}".encode()).hexdigest()[:16]

def chunk_document(
    doc_id: str,
    sections: list[dict],   # [{"title": str, "text": str}]
    acl: list[str],
    source_system: str,
    last_modified: str,
    parent_token_limit: int = 800,
    child_token_limit: int = 200,
) -> list[Chunk]:
    """
    For each section, emit one parent chunk and N child chunks.
    Children carry a parent_id pointing to their enclosing section chunk.
    Both levels carry full ACL and provenance metadata.
    """
    chunks: list[Chunk] = []

    for section in sections:
        title = section["title"]
        text = section["text"]
        tokens = ENCODER.encode(text)

        parent_id = _make_id(doc_id, f"parent::{title}")
        # Truncate parent to token limit while keeping whole sentences.
        parent_text = ENCODER.decode(tokens[:parent_token_limit])
        parent_chunk = Chunk(
            chunk_id=parent_id,
            parent_id=None,
            doc_id=doc_id,
            text=f"{title}\n\n{parent_text}",
            token_count=min(len(tokens), parent_token_limit) + len(ENCODER.encode(title)),
            level="parent",
            section_title=title,
            acl=acl,
            source_system=source_system,
            last_modified=last_modified,
        )
        chunks.append(parent_chunk)

        # Slide a child window across the full section text.
        stride = child_token_limit // 2   # 50% overlap for boundary coverage
        for i, start in enumerate(range(0, len(tokens), stride)):
            child_tokens = tokens[start : start + child_token_limit]
            if not child_tokens:
                break
            child_id = _make_id(doc_id, f"child::{title}::{i}")
            child_chunk = Chunk(
                chunk_id=child_id,
                parent_id=parent_id,
                doc_id=doc_id,
                text=ENCODER.decode(child_tokens),
                token_count=len(child_tokens),
                level="child",
                section_title=title,
                acl=acl,
                source_system=source_system,
                last_modified=last_modified,
                metadata={"window_index": i, "stride": stride},
            )
            chunks.append(child_chunk)

    return chunks
```

### Code Block 2: Hybrid Retrieval with Reciprocal Rank Fusion

This retrieval orchestrator fans out to BM25 and dense vector indexes in parallel, merges candidate lists using RRF, applies an ACL filter, and returns the top-k candidates with a unified score. The RRF constant `k=60` is the standard value that provides robustness to rank outliers across lists of different lengths.

```python
import asyncio
from dataclasses import dataclass

@dataclass
class Candidate:
    chunk_id: str
    doc_id: str
    text: str
    acl: list[str]
    score: float
    source: str   # "bm25" | "dense" | "graph"

async def bm25_search(query: str, top_k: int, index_client) -> list[Candidate]:
    """Query BM25 index and return ranked candidates."""
    results = await index_client.search(query=query, top_k=top_k, search_type="lexical")
    return [
        Candidate(
            chunk_id=r["chunk_id"], doc_id=r["doc_id"], text=r["text"],
            acl=r["acl"], score=r["bm25_score"], source="bm25"
        )
        for r in results
    ]

async def dense_search(query_embedding: list[float], top_k: int, vector_client) -> list[Candidate]:
    """Query HNSW vector index and return ranked candidates."""
    results = await vector_client.search(vector=query_embedding, top_k=top_k)
    return [
        Candidate(
            chunk_id=r["chunk_id"], doc_id=r["doc_id"], text=r["text"],
            acl=r["acl"], score=r["cosine_similarity"], source="dense"
        )
        for r in results
    ]

def reciprocal_rank_fusion(
    ranked_lists: list[list[Candidate]],
    k: int = 60,
) -> list[Candidate]:
    """
    Merge multiple ranked lists using RRF.
    RRF score = sum over lists of 1 / (k + rank_in_list).
    Higher k reduces the weight of top-rank advantage; k=60 is empirically robust.
    """
    scores: dict[str, float] = {}
    chunk_map: dict[str, Candidate] = {}

    for ranked_list in ranked_lists:
        for rank, candidate in enumerate(ranked_list, start=1):
            cid = candidate.chunk_id
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
            chunk_map[cid] = candidate

    merged = sorted(chunk_map.values(), key=lambda c: scores[c.chunk_id], reverse=True)
    for c in merged:
        c.score = scores[c.chunk_id]
    return merged

def apply_acl_filter(candidates: list[Candidate], user_groups: set[str]) -> list[Candidate]:
    """
    Retain only chunks where the user's group set intersects the chunk's ACL.
    An empty ACL list means the chunk is public (accessible to all).
    """
    filtered = []
    for c in candidates:
        if not c.acl or user_groups.intersection(c.acl):
            filtered.append(c)
    return filtered

async def hybrid_retrieve(
    query: str,
    query_embedding: list[float],
    user_groups: set[str],
    top_k_per_source: int = 100,
    final_top_k: int = 20,
    index_client=None,
    vector_client=None,
) -> list[Candidate]:
    """
    Fan out to BM25 and dense indexes in parallel, fuse with RRF,
    apply ACL filter, and return top final_top_k permissioned candidates.
    """
    bm25_task = bm25_search(query, top_k_per_source, index_client)
    dense_task = dense_search(query_embedding, top_k_per_source, vector_client)
    bm25_results, dense_results = await asyncio.gather(bm25_task, dense_task)

    fused = reciprocal_rank_fusion([bm25_results, dense_results])
    permissioned = apply_acl_filter(fused, user_groups)
    return permissioned[:final_top_k]
```

### Code Block 3: Grounding Verifier with Claim-Level Labeling

This verifier splits a generated answer into atomic claims and maps each claim to cited evidence spans. Claims with no supporting span are labeled `unsupported` and removed from the final answer, while contradicted claims trigger a warning flag in the trace.

```python
import re
from dataclasses import dataclass
from enum import Enum
from anthropic import Anthropic

client = Anthropic()

class ClaimLabel(str, Enum):
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    NOT_FOUND = "not_found"

@dataclass
class ClaimVerification:
    claim: str
    label: ClaimLabel
    cited_chunk_id: str | None
    cited_span: str | None
    confidence: float

DECOMPOSE_PROMPT = """Split the following answer into atomic claims.
Each claim must be independently verifiable from a single evidence span.
Return a JSON array of strings, one per claim.

Answer:
{answer}"""

VERIFY_PROMPT = """Given this evidence and claim, label the claim as:
- "supported": the evidence directly entails the claim
- "contradicted": the evidence states the opposite
- "not_found": the evidence does not address the claim

Evidence (chunk_id={chunk_id}):
{evidence_text}

Claim: {claim}

Return JSON: {{"label": "...", "span": "...", "confidence": 0.0-1.0}}
where "span" is the exact evidence substring that supports/contradicts, or null."""

def decompose_into_claims(answer: str) -> list[str]:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": DECOMPOSE_PROMPT.format(answer=answer)}],
    )
    import json
    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    text = re.sub(r"^```json\s*|```$", "", text, flags=re.MULTILINE).strip()
    return json.loads(text)

def verify_claim_against_chunk(
    claim: str,
    chunk_id: str,
    evidence_text: str,
) -> ClaimVerification:
    import json
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": VERIFY_PROMPT.format(
                chunk_id=chunk_id, evidence_text=evidence_text, claim=claim
            ),
        }],
    )
    text = response.content[0].text.strip()
    text = re.sub(r"^```json\s*|```$", "", text, flags=re.MULTILINE).strip()
    result = json.loads(text)
    return ClaimVerification(
        claim=claim,
        label=ClaimLabel(result["label"]),
        cited_chunk_id=chunk_id if result["label"] != "not_found" else None,
        cited_span=result.get("span"),
        confidence=result.get("confidence", 0.0),
    )

def verify_answer(
    answer: str,
    evidence: list[dict],   # [{"chunk_id": str, "text": str}]
    support_threshold: float = 0.7,
) -> tuple[str, list[ClaimVerification]]:
    """
    Decompose the answer into claims, verify each against all evidence chunks,
    remove unsupported claims, and return the filtered answer plus verification records.
    """
    claims = decompose_into_claims(answer)
    verifications: list[ClaimVerification] = []

    for claim in claims:
        best: ClaimVerification | None = None
        for chunk in evidence:
            result = verify_claim_against_chunk(claim, chunk["chunk_id"], chunk["text"])
            if result.label == ClaimLabel.SUPPORTED and (
                best is None or result.confidence > best.confidence
            ):
                best = result
        if best is None:
            # No chunk supported this claim; mark not_found
            best = ClaimVerification(
                claim=claim, label=ClaimLabel.NOT_FOUND,
                cited_chunk_id=None, cited_span=None, confidence=0.0,
            )
        verifications.append(best)

    # Rebuild answer retaining only supported claims
    supported_claims = [
        v.claim for v in verifications
        if v.label == ClaimLabel.SUPPORTED and v.confidence >= support_threshold
    ]
    filtered_answer = " ".join(supported_claims) if supported_claims else (
        "I do not have sufficient evidence to answer this question reliably."
    )
    return filtered_answer, verifications
```

---

## Exercises

### Design Exercises

**Exercise 1 — Multi-Tenant Namespace Isolation**

A single RAG platform must serve five business units, each with their own document collections, ACL policies, and latency SLAs. Business unit A needs sub-second responses for a customer-facing chatbot; business unit B runs batch analyst queries that are latency-tolerant but need very high recall. Design the platform's tenant isolation model, including how you would separate indexes, share infrastructure, enforce per-tenant token budgets, and prevent a noisy-tenant ingestion burst from degrading query latency for other tenants. Address how you would handle a request where a user has access rights in two different business units and their query requires evidence from both.

**Exercise 2 — Index Migration Without Downtime**

Your team is migrating from `text-embedding-ada-002` (1,536 dimensions) to a fine-tuned domain model (768 dimensions). The corpus has 1B chunks. Design a migration plan that: keeps the current system serving queries with no quality regression during migration; validates that the new model has equal or better recall@20 before cutover; supports rollback within 5 minutes if a quality regression is detected post-cutover; and completes without exceeding 2x normal infrastructure cost. Describe your dual-index strategy, the alias management approach, and the specific metrics you would monitor during the migration window.

### Implementation Exercises

**Exercise 3 — Freshness-Aware Context Packer**

Implement a context packer that, given a list of reranked candidate chunks each with a `last_modified` ISO timestamp, a `relevance_score` float, and a `token_count` int, selects the optimal subset within a `max_tokens` budget. The packer must: prefer more recent chunks when relevance scores are within 0.05 of each other; deduplicate near-identical passages (cosine similarity > 0.92) keeping only the more recent one; place the highest-relevance chunk first and the second-highest last (exploiting LLM primacy/recency bias); and return the ordered list with a trace showing why each chunk was included or excluded.

**Exercise 4 — Retrieval Recall Regression Detector**

Write a Python script that: loads a golden query set from a JSON file (each entry: `{"query": str, "relevant_chunk_ids": list[str]}`); queries a live retrieval endpoint for each query and retrieves the top-20 candidates; computes recall@5, recall@10, recall@20, and mean reciprocal rank (MRR); compares results against a stored baseline file; prints a table of per-query regressions where recall@20 dropped by more than 0.10 versus baseline; and exits with a non-zero status code if more than 5% of queries show a regression, suitable for use as a CI gate.

### Debug Exercise

**Exercise 5 — Diagnose a Faithfulness Regression**

Your weekly evaluation run shows that the platform's unsupported-claim rate jumped from 1.4% to 4.8% between Monday and Friday. The retrieval recall@20 metric is unchanged at 0.91. The grounding verifier version did not change. Walk through your complete debugging methodology: which metrics you would examine first and why, what queries you would use to slice the data, how you would distinguish a generation regression from a packing regression from a corpus quality regression, what tooling you would use to inspect individual failing traces, and what the three most likely root causes are in order of probability. For each root cause, describe the specific evidence you would look for in the traces and the remediation action.

## End of Chapter

- **Key takeaway:** An advanced RAG platform is a pipeline of independently-failing stages — query planning, hybrid retrieval, reranking, context packing, generation, and grounding verification — and its quality is gated by the weakest stage, not the model. The defining discipline is *attribution*: faithfulness regressions are usually a packing or corpus problem, not a generation problem, so every stage must emit traces (retrieved chunk IDs, rerank scores, packed token budget, unsupported-claim rate) that let you localize a regression to one stage. GraphRAG and query planning add recall on multi-hop questions but only pay off when single-pass retrieval is the measured bottleneck.
- **What to practice:** Size the context-packing budget: given a 32K-token context window, a system prompt of 800 tokens, a target of leaving 4K tokens for generation, and reranked chunks averaging 350 tokens each, compute how many chunks fit and the recall ceiling that imposes. Then estimate the cost and p95 latency added by a cross-encoder rerank of top-100 candidates versus top-25, and the faithfulness lift required to justify it.
- **Interview drill:** Your platform's unsupported-claim rate jumps from 1.4% to 4.8% in a week while retrieval recall@20 holds at 0.91 and the grounding verifier is unchanged. Walk through localizing the regression: which traces you slice first, how you distinguish a generation regression from a context-packing regression from a corpus-quality regression, the three most likely root causes in probability order, and the specific trace evidence and remediation for each.

---

<!-- nav-footer -->
[[chapter-20|← Chapter 20]] | [[README|Contents]] | [[chapter-22|Chapter 22 →]]
