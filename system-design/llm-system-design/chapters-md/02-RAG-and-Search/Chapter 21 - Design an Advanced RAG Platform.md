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
> - **Cross-references:** Chapter 3 (vector infrastructure), Chapter 5 (evaluation), Chapter 7 (enterprise search), Chapter 17 (grounding)

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
- With ANN overhead, metadata, replicas: `5-8TB`

#### Query Throughput

- Queries/day: 20M
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
- **Reranker:** cross-encoder or late-interaction model (ColBERT) to re-score the top-100 fused candidates and return the top-12 most relevant passages. Cross-encoders attend jointly to query and passage tokens, producing ranking accuracy 15–25 percentage points higher than bi-encoder retrieval alone, at the cost of O(k) forward passes — making the candidate pool size a critical cost lever.
- **Context Packer:** Deduplicates near-duplicate passages using MinHash or sentence-level embedding similarity, orders evidence by relevance and recency, and enforces a hard token budget so the context window. Poor context packing — not retrieval — is the most common root cause of diluted or contradictory evidence reaching the model.
- **Answer Generator:** Calls the LLM with the packed evidence and a structured instruction to cite every factual claim with a chunk ID from the provided evidence set. Structured Output / Constrained Decoding|Structured output (JSON with claim-citation pairs) makes downstream grounding verification deterministic rather than dependent on regex parsing of free text.
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

> **Why an intent classifier that routes queries to different retrieval strategies:** A lightweight intent classifier (fine-tuned BERT or even a rules-based heuristic over token patterns) adds fewer than 20 ms to the query path but can raise e...

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

> **Why a deterministic context-packing strategy placing key evidence first and last:** Studies on "lost in the middle" attention patterns show that LLMs using GPT-4-class models retrieve information from the start and end of long contexts with ...

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

> **Why measure each RAG stage separately rather than only end-to-end accuracy:** RAG pipelines have at least four independent failure modes — parse failure (document content not indexed), retrieval failure (correct document not ranked in ...

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

- **GraphRAG|GraphRAG:** Build an entity and relation graph alongside the vector index, where nodes are named entities (products, policies, people, APIs) and edges are typed relations extracted by an NER + relation extraction model. For multi-hop questions like "which customers are affected by the deprecation of API v2?", graph traversal finds paths that pure vector search cannot — a vector search for "affected customers" will not naturally surface the API-to-customer-contract edge that answers the question.

  > **Why:** Vector similarity finds semantically related passages, but it cannot follow a chain of relationships across documents.

- **HyDE (Hypothetical Document Embeddings):** Prompt the LLM to generate a short hypothetical answer or document before retrieval, then embed that hypothetical and use it as the retrieval query instead of the raw question. This works because the hypothetical answer is written in the same vocabulary and style as real corpus documents, closing the query-document vocabulary gap that causes vague questions to retrieve off-topic results.

  > **Why:** User queries are often 5–15 tokens of natural language; corpus documents are 200–500 tokens of domain-specific prose.

- **Parent-child retrieval:** Index child passages of 128–256 tokens for high-precision embedding recall (short passages have less noise and closer alignment between embedding and content), but when a child passage is selected by the reranker, fetch its parent section (512–1024 tokens) to pack into the prompt. This two-level structure provides the best of both worlds: retrieval precision from small chunks and generation quality from full context.

  > **Why:** Embedding a 1,024-token section dilutes the embedding with multiple topics, reducing retrieval recall for any individual claim in the section.

- **ColBERT-style late interaction:** Rather than encoding query and passage into a single vector each (bi-encoder) or concatenating them for a single score (cross-encoder), ColBERT retains token-level embeddings for both query and passage and computes relevance as the sum of maximum-similarity scores across query tokens. This captures fine-grained term-level matching that bi-encoders miss, at a cost of 32 bytes × sequence-length per passage rather than 1,536 bytes per passage.

  > **Why:** Cross-encoder reranking is 15–25% more accurate than bi-encoder retrieval but requires O(k) forward passes at inference time, making it 50–100x more expensiv...

- **Contextual compression:** After reranking, pass each selected passage through an extraction prompt that identifies the 2–4 sentences most directly relevant to the query and discards the rest before packing. This can reduce average packed token count by 30–50% for dense passages, freeing budget for more diverse evidence or a more detailed system prompt.

  > **Why:** Reranking selects the right passages but does not trim them — a highly ranked 300-token passage may contain only 50 tokens of directly relevant content.

- **Multi-vector documents:** Index the same document under multiple vector representations — the title embedding, the summary embedding, body chunk embeddings, table cell embeddings, and entity name embeddings — and search all of them at query time. This ensures that a query for a concept mentioned only in a table caption or document title is not missed because the body-chunk embedding did not capture it.

  > **Why:** A single embedding per chunk cannot represent all retrieval surfaces equally well.

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

