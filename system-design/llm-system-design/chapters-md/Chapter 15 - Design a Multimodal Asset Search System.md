---
title: "Chapter 15: Design a Multimodal Asset Search System"
tags: [llm, system-design, multimodal, clip, video-search, cross-modal, case-study]
chapter: 15
part: case-studies
---

# Chapter 15: Design a Multimodal Asset Search System

## Context

> [!info] Quick Reference
> - **Pattern:** Cross-modal semantic search (image/video/document)
> - **Scale:** Large multi-modal asset corpus with real-time indexing
> - **Key Techniques:** CLIP/SigLIP shared embedding space, modality-specific indexes with score normalization, video keyframe extraction (TransNetV2 + uniform sampling), multimodal score fusion
> - **Primary Concerns:** Cross-modal calibration, temporal precision for video, document rendering strategy, index freshness
> - **Cross-references:** [[Chapter 3 - Data Pipelines and Vector Infrastructure|Chapter 3]] (vector infrastructure), [[Chapter 7 - Design an Enterprise Semantic Search Engine|Chapter 7]] (enterprise search), [[Chapter 14 - Design a Real-Time Meeting Summarizer|Chapter 14]] (audio/video signals)

**Problem statement:** Design a search system that supports cross-modal queries (text→image, image→text, text→video, image→video) over 500M assets using joint [[glossary#Embedding|embedding]] spaces, with sub-150ms retrieval [[glossary#Latency (TTFT, TPOT, Tail)|latency]] and production-grade ranking.

### Real-World Examples

- A stock media platform (Shutterstock/Getty-class) serves 10K QPS across 500M images and 50M video clips. When text queries like "sunset over mountain lake" return irrelevant results, user engagement drops 15% week-over-week. Deploying CLIP-based embeddings with a learned [[glossary#Cross-Encoder Reranking|reranker]] improves nDCG@10 by 22% over BM25-on-metadata baselines.
- An enterprise DAM (Digital Asset Management) system enables designers to search by uploading a reference image. The system retrieves visually similar assets across images and video keyframes in a unified embedding space. Without cross-modal retrieval, designers spend 40 minutes per search session manually browsing folders; with it, median search time drops to 3 minutes.

---

## Step 1: Understand the Problem and Establish Design Scope

### Simulated Dialogue

**Interviewer:** Design a multimodal search system over a large asset library.  
**Candidate:** I need to understand the modality mix, query patterns, corpus size, and latency requirements. Cross-modal search (e.g., text querying images) requires fundamentally different architecture than single-modality keyword search.

**Candidate:** What is the asset corpus?  
**Interviewer:** 500M assets total: 400M images, 80M video clips (avg 30 seconds each), 20M documents (PDFs, slides). Growing at 2M assets/week.

**Candidate:** What are the query modalities?  
**Interviewer:** Text→image (60% of queries), text→video (20%), image→image (10%), image→text/document (5%), text→document (5%). Users may also combine modalities—e.g., text query + reference image.

**Candidate:** Latency and throughput requirements?  
**Interviewer:** p95 retrieval latency < 150ms. 10K QPS at peak. Top-20 results returned per query.

**Candidate:** What ranking quality targets?  
**Interviewer:** nDCG@10 > 0.65 on human-judged relevance. Diversity: at least 3 distinct visual concepts in top-10 for broad queries.

### Functional Requirements

- **Cross-modal retrieval:** Any query modality can retrieve any asset modality. A user typing text must be able to retrieve images, video clips, or documents without separate search flows for each modality.
- **Text queries:** Return ranked images, video clips, and documents ordered by semantic relevance to the natural-language query, not just keyword overlap with metadata tags.
- **Image queries:** Return visually similar images and video keyframes using the shared CLIP embedding space, enabling "find more like this" functionality that respects content and style rather than just filename similarity.
- **Hybrid queries:** Support text + reference image with controllable weighting (e.g., α slider from "match text" to "match image"), so a user can say "find blue dresses like this one" where both the color description and the reference garment shape contribute to retrieval.
- **Faceted filtering:** Asset type, resolution, duration, license, upload date, and color palette filters applied pre-ANN-search to shrink the candidate set before embedding-space search, reducing both latency and irrelevant results.
- **Near-real-time indexing:** New assets searchable within 5 minutes of upload, so content creators see their uploads appear in search immediately after processing rather than waiting for overnight batch jobs.

### Non-Functional Requirements

- **Latency:** p95 < 150ms end-to-end from query receipt to ranked results returned to the client. This budget covers query encoding (~15ms GPU), ANN search (~15ms across shards), reranking (~40ms GPU), and result assembly (~20ms), leaving 60ms headroom.
- **[[glossary#Throughput|Throughput]]:** 10K QPS sustained at peak, with burst capacity to 15K QPS during promotional events without SLO degradation. Requires horizontal scaling of both the GPU query-encoding pool and the ANN shard replicas.
- **Corpus:** 500M assets at launch, growing 2M/week (~104M/year). Index architecture and capacity planning must accommodate 3–5 years of growth without full re-architecture, implying a target of ~1B assets before the next major design revision.
- **Freshness:** New assets indexed within 5 minutes of upload completion. This requires streaming ingestion (not batch), micro-batch index updates every 30 seconds, and a brute-force sidecar index covering the most recent 5-minute upload window.
- **Relevance:** nDCG@10 > 0.65 on human-judged cross-modal query sets. This is measured weekly on a held-out evaluation set of 10K (query, relevant-asset) pairs covering all modality combinations.
- **Availability:** 99.95% uptime for the search serving path, corresponding to < 4.4 hours downtime/year. The ingestion pipeline can tolerate brief outages (assets queue up and index on recovery) without violating this SLO.
- **Cost:** < $0.001 per query at scale. At 10K QPS and $123/hr infrastructure cost, actual cost is ~$0.0000034/query — three orders of magnitude under budget, providing room for additional reranking compute as quality needs grow.

### Back-of-the-Envelope Estimation

#### Corpus and Embedding Storage

- Assets: 500M
- Embedding dimension: 768 (CLIP ViT-L/14)
- Bytes per embedding: `768 * 4 (FP32) = 3,072 bytes` → with PQ compression: ~128 bytes/vector
- Raw embedding storage: `500M * 3,072 = 1.536 TB` (FP32, uncompressed)
- Compressed (PQ, 128 bytes): `500M * 128 = 64 GB` ← fits in RAM across a small cluster
- With video: each 30s clip → 15 keyframes → 15 embeddings per clip = `80M * 15 = 1.2B` video keyframe embeddings
- Total vectors (images + video keyframes + documents): `400M + 1.2B + 20M = 1.62B vectors`
- Compressed storage: `1.62B * 128 = 207 GB`

#### Index Architecture

- HNSW index for 1.62B vectors at 128 bytes/vector:
  - Memory: ~207 GB vectors + ~300 GB graph overhead = ~507 GB total
  - Sharded across 16 machines with 64 GB RAM each (2x replication for availability)
  - Each shard: ~100M vectors, ~32 GB memory
- Alternative: IVF-PQ index: smaller memory footprint (~150 GB) but requires nprobe tuning for recall

> **Why HNSW as the primary index:** HNSW (Hierarchical Navigable Small World) achieves O(log N) search complexity with high [[glossary#Recall|recall]] (>95% R@10 at ef_search=128) and supports incremental inserts without full rebuild — critical for the 5-minute freshness SLO. IVF-PQ offers 3x lower memory at 1.62B vectors but requires periodic nlist/nprobe retuning as the corpus grows, and does not support incremental inserts without a coarse quantizer update that temporarily degrades recall. For a system where both freshness and high recall matter, HNSW's slightly higher memory cost is justified. PQ (Product Quantization) compression is applied to the stored vectors in both cases: it divides the 768-dim vector into 16 sub-vectors of 48 dimensions each, quantizing each sub-vector to one of 256 centroids. This compresses 3,072 bytes (FP32) to 16 bytes (16 × 8-bit indices), a 192x reduction with < 3% recall loss at R@10 for this embedding dimension.

#### Query Processing

- Peak QPS: 10K
- Query embedding inference (CLIP text encoder): ~5ms per query on GPU, batch of 64 → ~312 embeddings/sec per GPU
- GPUs for query embedding: `10K / 312 ≈ 32 GPUs` → with batching optimization: ~20 GPUs
- ANN search: ~5-10ms per shard, 16 shards queried in parallel → 10ms
- Reranking (cross-encoder on top-100): ~20ms (GPU) or ~50ms (CPU)
- Total query latency budget:

| Stage | Budget | Notes |
|---|---|---|
| Query embedding (CLIP text/image encoder) | 15ms | Batched GPU inference |
| Pre-filter (metadata facets) | 5ms | Inverted index on metadata |
| ANN search (parallel across shards) | 15ms | HNSW search, nprobe-tuned |
| Fetch candidate metadata | 10ms | Cache-backed metadata store |
| Reranking (cross-encoder or fusion) | 40ms | Top-100 → top-20 |
| Result assembly + dedup | 10ms | Remove near-duplicate images |
| Post-processing (thumbnail URLs, etc.) | 5ms | CDN URL signing |
| **Total** | **100ms** | 50ms headroom under 150ms SLO |

#### Ingestion Throughput

- New assets/week: 2M → `2M / (7 * 86400) ≈ 3.3 assets/sec`
- Image embedding (CLIP ViT-L/14): ~20ms per image on GPU → single GPU handles 50/sec
- Video embedding: 15 keyframes per clip → 15 * 20ms = 300ms per video → single GPU handles ~3 videos/sec
- Total embedding compute for ingestion: 1-2 GPUs (trivial relative to serving fleet)
- Index update: micro-batch inserts into HNSW every 30 seconds

> **Why micro-batch inserts every 30 seconds rather than continuous streaming:** HNSW inserts require acquiring a write lock on the graph structure to update the navigable small world connections. Continuous single-item inserts at 3.3 assets/sec would create 3.3 lock acquisitions/sec, each blocking concurrent read queries for ~5ms — a 1.6% reduction in query throughput from lock contention alone. Batching 100 inserts every 30 seconds concentrates the write lock into one ~500ms window per 30 seconds (1.7% of time blocked), which is roughly equivalent contention but is easier to schedule during low-traffic periods. The 30-second interval also satisfies the 5-minute freshness SLO with 10x headroom, allowing retries if a batch fails.

#### Cost Per Query

- GPU fleet (query embedding + reranking): ~30 GPUs, ~$2.50/hr each = $75/hr
- Index serving fleet (CPU/RAM): 32 machines, ~$1.50/hr each = $48/hr
- Total: ~$123/hr
- Queries/hour at peak: `10K * 3600 = 36M`
- Cost/query: `$123 / 36M ≈ $0.0000034` ← well under $0.001

---

## Step 2: Propose High-Level Design and Get Buy-In

### Core Architecture Components

- **Query Gateway:** Auth, rate limiting, query parsing, modality detection (is the query text, image, or hybrid?).
- **Query Encoder Service:** Encodes text/image queries into the shared embedding space using CLIP model. Batched GPU inference.
- **Metadata Filter Engine:** Pre-filters corpus by structured facets (type, license, date range, resolution) using an inverted index. Reduces ANN search space.
- **ANN Index Service:** Sharded HNSW (or IVF-PQ) index serving 1.62B vectors. Performs approximate nearest neighbor search in the joint embedding space.
- **Reranker Service:** Cross-encoder or late-fusion model that reranks top-100 ANN results to produce final top-20. Uses richer features than dot-product similarity.
- **Asset Metadata Store:** Low-latency key-value store (Redis-backed) for asset metadata, thumbnails, and preview URLs.
- **Ingestion Pipeline:** Processes new assets: extract visual features, generate embeddings, extract metadata, update index.
- **Video Processing Service:** Keyframe extraction, scene detection, temporal segmentation, per-keyframe embedding.
- **Observability:** Query latency histograms, nDCG sampling, embedding drift detection, index freshness metrics.

### Pipeline A: Asset Ingestion Pipeline

1. New asset uploaded to object storage (S3). Event triggers ingestion.
2. **Modality router:** routes to image, video, or document processing path.
3. **Image path:** resize to 224x224, run through CLIP ViT-L/14 image encoder → 768-dim embedding. Extract EXIF metadata.
4. **Video path:** decode video, run scene detection (PySceneDetect or TransNetV2), extract keyframes at scene boundaries + uniform sampling (max 15 keyframes per 30s clip). Each keyframe → CLIP embedding. Generate temporal metadata (keyframe timestamps, scene descriptions).
5. **Document path:** render each page to image (PDF→PNG at 300dpi), run CLIP embedding on rendered pages. Extract text via OCR (Tesseract or PaddleOCR), generate text embedding for full document content.
6. Embeddings + metadata written to ingestion queue (Kafka).
7. Index updater consumes queue, performs micro-batch HNSW insertions (every 30s).
8. Asset metadata written to metadata store. Thumbnails generated and pushed to CDN.
9. Quality check: sample 0.1% of new embeddings, compute cosine similarity against known test queries. Alert if mean similarity drops (embedding model drift).

### Pipeline B: Query Serving Pipeline

1. Query arrives at gateway. Modality detected: text / image / hybrid.
2. **Text query:** encoded by CLIP text encoder → 768-dim query vector.
3. **Image query:** encoded by CLIP image encoder → 768-dim query vector.
4. **Hybrid query:** both encoders run; vectors combined via weighted average (default α=0.7 text, 0.3 image, user-adjustable).
5. Metadata filters applied: generate a candidate bitmap from inverted index on structured facets.
6. Query vector + candidate bitmap sent to ANN index service. Parallel fan-out to all shards.
7. Each shard returns top-K candidates (K=100/num_shards) with scores.
8. Merge shard results, deduplicate near-identical images (perceptual hash distance < 5).
9. Top-100 candidates sent to reranker. Reranker uses cross-modal features: query-asset similarity, asset quality score, recency, popularity, visual diversity.
10. Top-20 results assembled with metadata, thumbnails, and preview URLs. Returned to client.

### Mermaid Architecture Diagram

```mermaid
flowchart LR
  user[User Query] --> gateway[QueryGateway]
  gateway -->|text| textEnc[CLIPTextEncoder GPU]
  gateway -->|image| imgEnc[CLIPImageEncoder GPU]
  gateway -->|hybrid| textEnc
  gateway -->|hybrid| imgEnc

  textEnc --> fusion[QueryFusion weighted avg]
  imgEnc --> fusion

  fusion --> metaFilter[MetadataFilterEngine]
  metaFilter --> annSearch[ANNIndexService Sharded HNSW]

  annSearch --> shard1[Shard1]
  annSearch --> shard2[Shard2]
  annSearch --> shardN[ShardN 16 shards]

  shard1 --> merge[ResultMerger + Dedup]
  shard2 --> merge
  shardN --> merge

  merge --> reranker[RerankerService]
  reranker --> assembly[ResultAssembly]
  assembly --> metaStore[AssetMetadataStore Redis]
  assembly --> user

  upload[AssetUpload S3] --> ingest[IngestionPipeline]
  ingest --> clipEnc[CLIPEncoder]
  ingest --> videoProc[VideoProcessing Keyframes]
  ingest --> docProc[DocumentProcessing OCR + Render]
  clipEnc --> indexUpdate[IndexUpdater]
  videoProc --> clipEnc
  docProc --> clipEnc
  indexUpdate --> annSearch

  observability[Observability nDCG Latency Drift] --> annSearch
  observability --> reranker
```

---

## Step 3: Design Deep Dive

Focus areas:

1. **Multimodal Embedding Pipeline (CLIP, Video Frame Sampling, Document Rendering)**
2. **Cross-Modal Retrieval Architecture (Unified vs Separate Indexes, Fusion Strategies)**
3. **Video Search and Temporal Indexing**

### 1) Multimodal Embedding Pipeline

The embedding model is the foundation. Every asset and every query is projected into the same vector space. The quality of this projection determines retrieval relevance.

**Embedding model selection:**

| Model | Architecture | Embedding Dim | ImageNet Zero-Shot | Cross-Modal Retrieval (Flickr30k R@1) | Inference Speed (img, A100) | Training Data | License | Best For |
|---|---|---|---|---|---|---|---|---|
| CLIP ViT-L/14 (OpenAI) | ViT-L + GPT-2 text | 768 | 75.3% | 87.4% | ~8ms | 400M pairs (WIT) | MIT | General production default |
| SigLIP ViT-SO400M | ViT-SO + text tower | 1152 | 83.1% | 91.2% | ~12ms | 4B pairs (WebLI) | Apache 2.0 | Higher quality, slightly slower |
| OpenCLIP ViT-G/14 | ViT-G + text | 1024 | 80.1% | 90.8% | ~18ms | LAION-2B | MIT | Open-source high quality |
| EVA-CLIP ViT-E | ViT-E + text | 1024 | 82.0% | 89.5% | ~20ms | Merged datasets | Apache 2.0 | Research/academic |
| Custom fine-tuned CLIP | ViT-L + domain text | 768 | N/A (domain-specific) | +3-8% on domain | ~8ms | Domain data + CLIP init | Internal | Domain-specific corpus |
| BLIP-2 (retrieval mode) | ViT-G + Q-Former + LLM | 768 | 82.4% | 92.1% | ~35ms | 129M pairs | BSD-3 | When quality > speed |

**Recommendation:** Start with SigLIP ViT-SO400M for highest quality-to-speed ratio. Fine-tune on domain data (stock media pairs) with contrastive loss. Fall back to CLIP ViT-L/14 if latency budget is tight.

> **Why SigLIP over OpenAI CLIP ViT-L/14:** SigLIP replaces the softmax contrastive loss with a sigmoid pairwise loss, eliminating the in-batch normalization that causes CLIP's performance to degrade on small batch sizes. This makes SigLIP more stable to fine-tune on domain data (stock media pairs) where batch size is constrained by GPU memory. On cross-modal retrieval benchmarks (Flickr30k, MSCOCO), SigLIP-SO400M achieves R@1 scores 3–5 points above CLIP ViT-L/14 at comparable inference latency (~12ms vs ~8ms on A100). Trained on 4B (image, text) pairs from WebLI vs CLIP's 400M WIT pairs, SigLIP has substantially better coverage of diverse visual concepts. The Apache 2.0 license also avoids the ambiguity in OpenAI CLIP's MIT license regarding commercial fine-tuning.

**Fine-tuning strategy for domain adaptation:**

1. Collect 1M high-quality (text, image) pairs from the platform's search logs (query → clicked asset).
2. Initialize from pretrained SigLIP weights.
3. Fine-tune with sigmoid contrastive loss (SigLIP's native objective) for 5 epochs.
4. Hard negative mining: for each positive pair, sample 7 in-batch negatives + 1 hard negative (highest-similarity non-clicked asset).
5. Evaluation: measure R@1, R@5, R@10 on a held-out test set of 10K human-judged query-asset pairs.
6. A/B test: run fine-tuned model alongside base model on 10% of traffic. Promote if nDCG@10 improves > 2%.

**Document embedding strategy:**

Documents (PDFs, slides) are not natively handled by CLIP. Two approaches:

| Approach | How It Works | Quality | Latency | Best For |
|---|---|---|---|---|
| Render-to-image | Render each page as PNG at 300dpi, embed with CLIP image encoder | Good for visual documents — preserves layout, charts, and typography that text extraction destroys; CLIP achieves ~68% R@10 on infographic retrieval benchmarks vs 41% for text-only | 200ms/page — PDF rendering is the bottleneck; parallelizable across pages | Slides, visual-heavy PDFs, design documents, annual reports with charts |
| Text extraction + text embedding | OCR → text → CLIP text encoder (or a dedicated text encoder like text-embedding-3-large) | Good for text-heavy documents — captures semantic content even when layout is complex or multi-column; degrades on scanned PDFs where OCR accuracy drops below 95% | 50ms/page — OCR via PaddleOCR is faster than rendering; 20ms OCR + 5ms CLIP text encoding + 25ms overhead | Reports, articles, academic papers, legal documents with dense prose |
| Hybrid | Both visual and text embeddings per page; fuse at retrieval time with α * visual_score + (1-α) * text_score | Best overall — visual embedding captures layout and figures, text embedding captures prose content; ensemble consistently outperforms either alone by 10–15% nDCG@10 on mixed document corpora | 250ms/page — render + OCR + two encoder passes; parallelizable across pages and across GPUs | **Production default** for a corpus with heterogeneous document types |

**Embedding versioning and migration:**

When the embedding model is updated (fine-tuned or upgraded), all 1.62B vectors must be re-embedded. This is a massive offline job:
- 1.62B embeddings at 20ms each = `1.62B * 0.02s = 32.4M GPU-seconds ≈ 375 GPU-days`
- With a 100-GPU batch job: ~4 days for full re-embedding.
- **Shadow index strategy:** build new index in parallel with old. Run dual-read during migration (query both, merge results). Cut over when new index quality is validated. Zero-downtime migration.

> **Why shadow index instead of in-place update:** Embedding model upgrades change the vector space entirely — an old embedding from CLIP ViT-L and a new one from SigLIP are not comparable, so you cannot mix them in the same HNSW graph. The shadow index approach keeps the old index fully operational during the 4-day re-embedding job, serving 100% of queries from the old index while the new one is built. Dual-read during the final cutover window (24 hours) catches quality regressions by comparing nDCG@10 on both indexes before full promotion. The cost of running two parallel indexes (~2x RAM for 4 days) is far less than the business cost of a retrieval quality outage.

### 2) Cross-Modal Retrieval Architecture

The core architectural decision: should all modalities share one index, or should each modality have its own index?

#### Index Architecture Trade-off Table

| Architecture | How It Works | Strengths | Weaknesses | Use When |
|---|---|---|---|---|
| Unified index | All modalities in one HNSW index; query vector searches all assets | Simplest ops; natural cross-modal retrieval; one search call | Modality bias (images dominate because there are more); hard to tune per-modality relevance | Small corpus (<50M), single-modality dominant |
| Separate indexes per modality | Image index, video index, document index; query hits all, results merged | Per-modality tuning; independent scaling; easier to debug | Fan-out latency; complex merge logic; score calibration across indexes | **Production default for mixed corpus** |
| Hierarchical (coarse + fine) | Coarse unified index for candidate generation; fine per-modality index for reranking | Best recall + precision | Most complex; two-stage latency | Highest-quality requirement |

**Recommended: Separate indexes with score normalization.**

Score calibration across indexes: raw cosine similarity from different indexes is not comparable (image embeddings cluster differently than video keyframe embeddings). Normalize scores per-index to zero mean, unit variance on a calibration set of 10K queries, then merge.

> **Why separate indexes rather than unified:** A unified index of 1.62B vectors dominated by 1.2B video keyframes causes systematic modality bias — ANN search returns video keyframes 74% of the time by sheer population proportion, regardless of query intent. Separate indexes let each modality have independent nprobe/ef_search tuning for its own recall-vs-latency tradeoff, and scores can be calibrated using modality-specific statistics collected from click-through logs. Independent scaling is also operationally simpler: the image index can be resized without touching the video or document indexes.

**Fusion strategies for hybrid queries (text + image):**

| Strategy | How It Works | Quality | Latency | Complexity |
|---|---|---|---|---|
| Early fusion (vector average) | `q = α * q_text + (1-α) * q_image`, single ANN search | Moderate — the averaged vector loses modality-specific signal; on Flickr30k I→T, early fusion scores ~3–5% lower R@1 than late fusion | Lowest — single ANN search (~10ms); α is a scalar that can be adjusted at query time without retraining | Low — one index, one search call, no per-modality infrastructure |
| Late fusion (score merge) | Separate ANN searches for text and image vectors, merge by RRF or weighted score | Higher — preserves both signal types independently; each modality can retrieve candidates the other would miss | Higher — two ANN searches (~20ms), plus merge and dedup overhead; fan-out doubles internal ANN QPS | Medium — requires per-modality score normalization and merge logic; easier to debug than learned fusion |
| Learned fusion | Train a small MLP that takes both query vectors + candidate features → relevance score | Highest — MLP learns optimal weighting per query type (text-dominant vs image-dominant) from click data; +8% nDCG vs fixed-weight late fusion on stock media | Highest — requires fetching candidate features for top-100 results before scoring (~50ms added); non-trivial training infrastructure | High — requires labeled training data (query, positive, negative triplets), model versioning, and A/B test infrastructure |
| **Hybrid: early fusion for retrieval, late fusion for reranking** | Early fusion for ANN (speed), late fusion features fed to reranker | Best balance — ANN recall is adequate with averaged vector; reranker recovers lost signal using both query vectors as separate features | Medium — single ANN search (~10ms) + reranking with both vectors as features (~40ms); total comparable to simple late fusion | Medium — reranker takes both query vectors as input; one trained model replaces separate fusion and reranking stages |

**Reciprocal Rank Fusion (RRF) for late fusion:**

```text
RRF_score(d) = Σ 1 / (k + rank_i(d))
```

where `rank_i(d)` is the rank of document d in the i-th result list, and k=60 (standard constant). RRF is parameter-free, robust, and consistently outperforms raw score merging.

> **Why RRF over weighted score averaging:** Raw cosine similarity scores from two separate CLIP searches have incompatible scales — the image index might return scores in [0.25, 0.82] while the video index returns [0.18, 0.71] for the same query, and these ranges shift with corpus composition. Weighted averaging of raw scores then amplifies whichever modality happens to produce higher magnitudes. RRF bypasses this entirely by operating only on ranks, which are always integers in [1, K]. It is robust to outlier scores, requires no calibration data, and in practice matches or exceeds tuned weighted score fusion in offline nDCG experiments (see the original Cormack et al. 2009 paper and TREC evaluations).

**Deduplication:**

Near-duplicate images are common in stock media (same image with different crops, watermarks, or color grades). Dedup strategy:
- Compute perceptual hash (pHash) at indexing time. Store in a Bloom filter.
- At query time, after ANN retrieval, compute pairwise pHash distance within top-100. Remove candidates with pHash Hamming distance < 5 (keep the higher-scored one).
- For video: deduplicate keyframes within the same clip (keep only scene-boundary keyframes).

> **Why pHash rather than cosine similarity for deduplication:** Cosine similarity in CLIP space measures semantic similarity, not pixel-level duplication. Two photos of different mountain lakes can have cosine similarity of 0.92 and are semantically similar but are not duplicates — removing one would hurt result diversity wrongly. pHash measures structural pixel similarity: a 64-bit hash computed from DCT coefficients of the resized image, where Hamming distance < 5 reliably catches crops, watermark additions, minor color grading, and JPEG re-compression artifacts (typically changing < 10% of pixels). This combination — CLIP space for relevance, pHash for dedup — correctly separates semantic similarity from pixel-level near-duplication.

### 3) Video Search and Temporal Indexing

Video search is the hardest modality. A 30-second clip contains ~900 frames, each potentially showing different content. The challenge: represent the clip compactly while enabling precise temporal retrieval.

**Keyframe extraction strategies:**

| Strategy | Frames per 30s Clip | Storage Cost | Retrieval Quality | Best For |
|---|---|---|---|---|
| Uniform sampling (1fps) | 30 | High — 30 embeddings × 128 bytes = 3.84 KB/clip; 80M clips = 307 GB compressed | Good coverage but produces 3–5 near-identical embeddings per static scene, wasting index space and distorting ANN neighbor graphs | Simple baseline or when scene detection infrastructure is unavailable |
| Scene boundary detection (TransNetV2) | 3-8 | Low — avg 5 embeddings × 128 bytes = 640 bytes/clip; 80M clips = 51 GB compressed | Good for narrative content with distinct scenes; misses important moments within long, visually static scenes (e.g., talking-head interviews) | Movies, TV clips, news footage with frequent hard cuts |
| Uniform + scene boundary (hybrid) | 10-15 | Medium — avg 12 × 128 bytes = 1.54 KB/clip; 80M clips = 123 GB compressed | Best coverage-vs-cost balance: scene boundaries catch hard transitions, uniform fill catches content within static scenes; measured +12% recall@5 vs scene-boundary-only on instructional video benchmarks | **Production default** |
| Dense sampling (all frames) | 900 | Prohibitive — 900 × 128 bytes = 115 KB/clip; 80M clips = 9.2 TB compressed, plus 1000x more ANN search work | Diminishing returns after ~30 frames due to temporal autocorrelation; consecutive frames at 30fps differ by < 1% of pixel content | Not viable at scale; useful only for ground-truth construction in research |
| Clustering (embed all, cluster, keep centroids) | 5-10 | Low — same footprint as scene-boundary approach | Misses brief but important moments that don't align with cluster centroids; a 0.5-second logo reveal at frame 847 is averaged away | Academic research on efficiency; not recommended when temporal precision matters |

**Recommended:** Hybrid sampling — scene boundaries (TransNetV2, ~50ms inference per clip) + uniform 0.5fps fill. Cap at 15 keyframes per 30s clip.

> **Why TransNetV2 for scene detection rather than simple frame differencing:** Simple frame differencing (comparing consecutive frame pixel differences against a threshold) produces high false-positive rates for camera pans, zooms, and lighting changes — these look like scene changes to a pixel comparator but represent the same continuous scene. TransNetV2 is a lightweight 3D CNN trained on the RAI and ClipShots datasets specifically to distinguish hard cuts and gradual transitions. It achieves ~95% F1 on standard benchmarks vs ~78% F1 for threshold-based differencing, at only ~50ms per 30-second clip on CPU. Fewer false positives mean fewer wasted keyframe embeddings on redundant frames, keeping the per-clip embedding count close to the target of 10–15.

**Temporal indexing architecture:**

Each video clip is represented as a set of (keyframe_embedding, timestamp) pairs. This enables:

1. **Clip-level search:** aggregate keyframe scores. `clip_score = max(keyframe_scores)` or `clip_score = mean(top-3 keyframe_scores)`.
2. **Temporal search:** return specific moments. "Find the part where the speaker shows a chart" → match against individual keyframes, return the timestamp.
3. **Temporal context:** for each matching keyframe, return a 5-second window (keyframe ± 2.5s) as a preview clip.

**Video indexing data model:**

```text
Video {
  clip_id: string
  duration_sec: float
  keyframes: [
    { frame_idx: int, timestamp_sec: float, embedding: float[768], scene_label: string },
    ...
  ]
  metadata: { title, tags, resolution, codec, upload_date }
  audio_transcript: string (optional, from STT)
  text_embedding: float[768] (from title + tags + transcript)
}
```

**Multimodal video representation:**

Videos have multiple signal channels. Relying on visual keyframes alone misses:
- **Audio:** A video about "jazz music" might show a static stage. The audio is the signal, not the visual. Index audio via STT transcription + CLAP (Contrastive Language-Audio Pretraining) embeddings.
- **Text overlays:** Title cards, captions, on-screen text. Extract via OCR on keyframes.
- **Metadata:** Title, description, tags from uploader.

**Multi-signal video retrieval:**

| Signal | Embedding Model | Weight in Fusion | Latency Cost | Value |
|---|---|---|---|---|
| Visual keyframes | CLIP/SigLIP | 0.50 | ~20ms/keyframe, ~200ms per clip for 10 keyframes on GPU; batch across clips to amortize | Primary signal for visual content — captures scene composition, objects, color palette, spatial relationships that no other signal encodes |
| Audio transcript | CLIP text encoder on STT output (Whisper-base for speed) | 0.20 | ~100ms/clip for STT (Whisper-base on GPU); embedding is then free via the already-loaded CLIP text encoder | Critical for speech-heavy video: a lecture on "gradient descent" has virtually no visual signal distinguishing it from any other lecture, but the transcript is uniquely specific |
| Text overlays (OCR) | CLIP text encoder | 0.10 | ~50ms/clip for OCR via PaddleOCR on keyframes; reuse OCR output at indexing time, zero latency at query time | Important for instructional and tutorial content: on-screen code, formulas, product names, and title cards often contain the most query-relevant text in the entire clip |
| Metadata (title + tags) | CLIP text encoder | 0.20 | ~2ms — title + tags are a single short string processed by the CLIP text encoder in one forward pass at ingestion | High signal-to-noise for professionally curated assets where uploaders provide accurate descriptions; degrades for user-generated content with keyword-stuffed or missing tags |

Fusion: weighted average of per-signal scores during reranking. Weights tuned via grid search on a labeled relevance dataset.

#### Video Indexing Strategy Trade-off Table

| Strategy | Index Size (80M clips) | Query Latency | Temporal Precision | Best For |
|---|---|---|---|---|
| Single embedding per clip (mean of keyframes) | 80M vectors (10 GB compressed) | Fast (~5ms) | None (clip-level only) | Quick clip-level retrieval |
| All keyframes indexed independently | 1.2B vectors (154 GB compressed) | Slower (~15ms, more shards) | High (keyframe-level) | Temporal search within clips |
| Hierarchical: clip-level first, then keyframe drill-down | 80M + 1.2B (164 GB) | Two-stage: 5ms + 10ms | High with lower first-stage cost | **Production default** |
| Video-level embedding (ViViT/TimeSformer) | 80M vectors (10 GB) | Fast (~5ms) | None | When video has single dominant concept |

**Recommended:** Hierarchical indexing. First stage: search 80M clip-level embeddings (mean of top-3 keyframes). Second stage: for top-50 clips, search 750 keyframes (15 per clip) to identify the best-matching temporal segment. Total latency: 5ms + 10ms = 15ms for the ANN portion.

> **Why hierarchical two-stage rather than flat keyframe index:** A flat index of 1.2B keyframe vectors requires ~507 GB RAM across shards just for video, and every query must search all 1.2B vectors even for a simple "find this concept" text query where any single good keyframe suffices. The hierarchical approach amortizes: the clip-level index (80M vectors, ~10 GB) provides coarse filtering in ~5ms, and the second stage only inspects 750 keyframes (50 clips × 15 frames), a 1600x reduction in the fine-grained search space. This gives keyframe-level temporal precision at 3x lower latency than searching the full flat index, while using 94% less memory for the first-stage index that handles all QPS.

### Production Bottlenecks and Mitigations

- **Embedding model latency under load**
  - Symptom: query embedding inference becomes bottleneck at peak QPS as GPU batch queue grows.
  - Mitigation: separate GPU pools for query encoding (latency-critical) and ingestion encoding (throughput-critical). Query encoding pool with autoscaling based on p95 latency.

- **Index freshness lag**
  - Symptom: newly uploaded assets not appearing in search results for >5 minutes.
  - Mitigation: micro-batch index updates every 30s. For HNSW, new vectors appended to a "hot" segment that is merged into the main index asynchronously. Fresh uploads also indexed in a small brute-force sidecar index that is always searched alongside the main HNSW index.

- **Score miscalibration across modalities**
  - Symptom: video results consistently ranked below image results because cosine similarity distributions differ.
  - Mitigation: per-modality score normalization using running statistics from the last 10K queries. Z-score normalize before merging.

- **Embedding drift after model update**
  - Symptom: old embeddings (from previous CLIP version) are incompatible with new query embeddings.
  - Mitigation: full re-embedding with shadow index. During migration, run a lightweight linear projection to map old embeddings to new space (trained on 100K paired embeddings). This is a temporary bridge that avoids serving stale results during the 4-day re-embedding job.

- **Near-duplicate flooding in results**
  - Symptom: top-10 results are all crops/variants of the same image.
  - Mitigation: pHash-based dedup post-retrieval. Maximal Marginal Relevance (MMR) reranking to enforce diversity: `score = λ * relevance - (1-λ) * max_similarity_to_selected`.

- **Video keyframe extraction bottleneck on ingestion**
  - Symptom: video ingestion falls behind upload rate due to decode + scene detection latency.
  - Mitigation: GPU-accelerated video decoding (NVDEC). Parallelize scene detection and keyframe embedding across GPU workers. Cap keyframe count at 15 per clip regardless of duration.

### Advanced Techniques

- **Matryoshka Representation Learning (MRL):** Train embeddings where the first N dimensions are a valid lower-dimensional embedding — i.e., the first 128 dimensions of a 768-dim vector are themselves a well-trained 128-dim embedding. At query time, use 128-dim for ANN search (4x faster per distance computation, 6x less memory), then rerank only the top-100 using the full 768-dim vectors. This yields ~5% recall loss on ANN retrieval, fully compensated by retrieving 2x candidates before reranking, while the reranking stage operates at full quality. MRL is trained by summing contrastive losses at multiple prefix lengths (128, 256, 512, 768), adding ~15% to training time with no changes to inference infrastructure.

  > **Why MRL instead of just training a smaller model:** A standalone 128-dim model loses the information capacity that 768 dimensions provide — it is fundamentally more constrained. MRL gives you a 128-dim ANN index that is a strict subset of the 768-dim space, so reranking can leverage all information without switching between two separately trained models or maintaining separate embedding stores.

- **ColPali / late interaction for documents:** Instead of producing a single pooled embedding per document page, produce per-patch visual embeddings (one 128-dim vector per 16×16 image patch) and score a query against a document using MaxSim: `score(q, d) = Σ_i max_j(q_i · d_j)` where i ranges over query patches and j over document patches. This late interaction captures fine-grained visual alignment — a query about "the bar chart on slide 3" matches the specific patch containing that chart rather than being diluted into a page-level average. Measured improvement: 8–12% nDCG@10 on document retrieval benchmarks vs single-vector CLIP. Storage cost: ~196 patches per page × 128 bytes = 25 KB/page vs 768 bytes for single-vector, a 33x increase that is acceptable for the document modality (20M documents, ~800 GB total vs 24 MB single-vector).

  > **Why late interaction specifically for documents:** Documents have highly localized relevance — a query about "Q3 revenue" matches one cell in a financial table, not the entire slide. Single-vector embeddings average the visual signal across the entire page, reducing the signal-to-noise ratio for localized queries. ColPali's per-patch representation preserves this locality without requiring OCR or layout analysis, making it robust to non-standard document formats.

- **CLIP score distillation for reranking:** Train a lightweight cross-encoder (2-layer transformer, ~10M parameters) that takes concatenated CLIP features from both the query and the candidate asset as input and predicts a human-annotated relevance label (0–4 scale). Distillation from CLIP's implicit knowledge into explicit relevance scores captures non-linearities that dot-product similarity cannot: two assets equidistant from the query vector in CLIP space can have different human relevance if one matches the query's primary subject and the other only matches a background element. Measured improvement: 5–10% nDCG@10 over raw cosine similarity at < 20ms additional latency on GPU when reranking the top-100 as a batch of 100 pairs. Training data: 500K (query, asset, label) triples from human judgment tasks using a 5-point relevance scale.

---

## Practical Implementation

### Cross-Modal CLIP Embedding and Score Normalization (Python)

```python
# Encodes text and image queries into a shared CLIP embedding space,
# then normalizes raw cosine scores across modalities before merging
import torch
from transformers import CLIPProcessor, CLIPModel
import numpy as np

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def embed_query(text: str) -> np.ndarray:
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        emb = model.get_text_features(**inputs)
    return emb[0].numpy() / np.linalg.norm(emb[0].numpy())

def embed_image(pil_image) -> np.ndarray:
    inputs = processor(images=pil_image, return_tensors="pt")
    with torch.no_grad():
        emb = model.get_image_features(**inputs)
    return emb[0].numpy() / np.linalg.norm(emb[0].numpy())

def normalize_scores(scores: list[float]) -> list[float]:
    # Min-max normalize within a modality result set so scores are comparable
    arr = np.array(scores, dtype=np.float32)
    lo, hi = arr.min(), arr.max()
    if hi == lo:
        return [1.0] * len(scores)
    return ((arr - lo) / (hi - lo)).tolist()

def fuse_results(text_hits, image_hits, alpha: float = 0.5) -> list[dict]:
    # text_hits / image_hits: list of {"id": ..., "score": raw_cosine}
    text_norm  = normalize_scores([h["score"] for h in text_hits])
    image_norm = normalize_scores([h["score"] for h in image_hits])

    combined: dict[str, float] = {}
    for hit, norm in zip(text_hits,  text_norm):
        combined[hit["id"]] = combined.get(hit["id"], 0) + alpha * norm
    for hit, norm in zip(image_hits, image_norm):
        combined[hit["id"]] = combined.get(hit["id"], 0) + (1 - alpha) * norm

    return sorted([{"id": k, "score": v} for k, v in combined.items()],
                  key=lambda x: x["score"], reverse=True)
```

### Video Keyframe Extraction Pipeline (Pseudocode)

```text
# Selects semantically representative keyframes for indexing — avoids duplicates

function extract_keyframes(video_path, target_fps=1) -> list[frame]:
    frames = decode_video(video_path, fps=target_fps)   # 1 frame/sec

    keyframes = [frames[0]]
    prev_embedding = clip_encode_image(frames[0])

    for frame in frames[1:]:
        embedding = clip_encode_image(frame)

        # Drop near-duplicate frames (scene hasn't changed)
        if cosine_similarity(embedding, prev_embedding) > 0.97:
            prev_embedding = embedding
            continue

        # Scene-change boundary detected — this frame is informative
        keyframes.append(frame)
        prev_embedding = embedding

    # Deduplicate across the full set using greedy max-coverage
    # Keep at most K keyframes per minute of video
    K = ceil(video_duration_minutes(video_path) * 6)
    if len(keyframes) > K:
        keyframes = greedy_max_coverage(keyframes, K, embed_fn=clip_encode_image)

    return keyframes

function index_video(video_path, weaviate_client):
    keyframes = extract_keyframes(video_path)
    for i, frame in enumerate(keyframes):
        embedding = clip_encode_image(frame)
        weaviate_client.data_object.create(
            class_name="VideoFrame",
            data_object={"video_id": video_path, "frame_index": i,
                         "timestamp_sec": frame.timestamp},
            vector=embedding
        )
```

### Reciprocal Rank Fusion and MMR Reranking (Python)

```python
# Merges results from separate modality indexes using RRF, then applies
# Maximal Marginal Relevance to enforce diversity in the final top-K.

from typing import List, Dict
import numpy as np

def reciprocal_rank_fusion(
    result_lists: List[List[Dict]],  # each list: [{"id": str, "score": float}, ...]
    k: int = 60,
) -> List[Dict]:
    """
    Merge N ranked lists using RRF. k=60 is the standard constant from
    Cormack et al. 2009 — it dampens the influence of top-ranked items
    without completely ignoring lower-ranked ones.
    """
    rrf_scores: Dict[str, float] = {}
    for result_list in result_lists:
        for rank, item in enumerate(result_list, start=1):
            doc_id = item["id"]
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k + rank)

    merged = [{"id": doc_id, "score": score}
              for doc_id, score in rrf_scores.items()]
    return sorted(merged, key=lambda x: x["score"], reverse=True)

def maximal_marginal_relevance(
    candidates: List[Dict],         # each item has "id", "score", "embedding" (np.ndarray)
    top_k: int = 10,
    lambda_diversity: float = 0.7,  # 1.0 = pure relevance, 0.0 = pure diversity
) -> List[Dict]:
    """
    MMR greedily selects results that are both relevant to the query
    and dissimilar to already-selected results.
    lambda_diversity=0.7 is a reasonable default: penalizes near-duplicates
    (cosine sim > 0.95) while not sacrificing top-1 relevance.
    """
    selected: List[Dict] = []
    remaining = list(candidates)

    while len(selected) < top_k and remaining:
        if not selected:
            # First result: just pick the highest-relevance candidate
            best = max(remaining, key=lambda x: x["score"])
        else:
            selected_embeddings = np.stack([s["embedding"] for s in selected])

            def mmr_score(item: Dict) -> float:
                rel = item["score"]
                # Max cosine similarity to any already-selected item
                sims = selected_embeddings @ item["embedding"]  # assumes unit vectors
                max_sim = float(sims.max())
                return lambda_diversity * rel - (1 - lambda_diversity) * max_sim

            best = max(remaining, key=mmr_score)

        selected.append(best)
        remaining.remove(best)

    return selected

# --- Example usage ---
if __name__ == "__main__":
    # Simulate two modality result lists (image index + video index)
    image_results = [{"id": f"img_{i}", "score": 1.0 - i * 0.05} for i in range(20)]
    video_results = [{"id": f"vid_{i}", "score": 0.95 - i * 0.04} for i in range(20)]

    merged = reciprocal_rank_fusion([image_results, video_results])
    print("Top-5 after RRF:", [r["id"] for r in merged[:5]])

    # Add random embeddings to simulate the reranking stage
    for item in merged[:20]:
        item["embedding"] = np.random.randn(768)
        item["embedding"] /= np.linalg.norm(item["embedding"])

    diverse = maximal_marginal_relevance(merged[:20], top_k=10, lambda_diversity=0.7)
    print("Top-10 after MMR:", [r["id"] for r in diverse])
```

---

## Step 4: Wrap Up

### Final Design Summary

The design builds cross-modal retrieval on a shared CLIP-family embedding space, with modality-specific indexes for score calibration and independent scaling. Video search uses hierarchical indexing (clip-level → keyframe-level) with multi-signal fusion across visual, audio, text, and metadata channels. A reranker with diversity controls produces the final ranked list within 150ms. The ingestion pipeline processes 2M new assets/week with near-real-time index updates via micro-batch HNSW insertion and a brute-force sidecar for freshness.

### Wrap-Around Concerns

- **Risk:** Embedding model upgrade requires re-embedding 1.62B vectors (4 GPU-days with 100 GPUs). Mitigation: shadow index migration with linear projection bridge for zero-downtime transition.
- **Risk:** Cross-modal score miscalibration causes one modality to dominate results. Mitigation: per-modality score normalization with rolling statistics; monitor modality distribution in top-10 results.
- **Risk:** CLIP embeddings encode societal biases from web-scraped training data (gender, racial, cultural stereotypes). Mitigation: bias audit on retrieval results for sensitive queries; debiasing projection applied post-embedding; human review of top results for flagged query categories.
- **Risk:** Video ingestion is 10x more expensive per asset than images due to decode + keyframe extraction + multiple embeddings. Mitigation: cap keyframes, GPU-accelerated decode, tiered processing (premium videos get dense keyframes, standard get sparse).
- **Risk:** pHash deduplication is fragile against adversarial near-duplicates (watermark removal, slight color shifts). Mitigation: learned dedup model (SimCLR-based) with fine-tuning on platform-specific duplicate pairs. Higher compute but catches adversarial variants.

---

## Step 5: Interviewer Curveballs

### Interviewer Follow-ups & Frequently Asked Questions (FAQ)

Q: A user searches for "red sports car on mountain road" and the top results are all red cars in parking lots. What went wrong?

**The Ideal Answer:** CLIP's contrastive training optimizes for matching the dominant concept but often ignores compositional relationships. "Red sports car" is a strong visual concept that overwhelms the spatial relationship "on mountain road." Diagnosis: embed the query and examine the top-100 nearest neighbors—if they're all red cars regardless of background, the embedding space lacks compositional grounding. Fix: (1) at query time, decompose into sub-queries ("red sports car" + "mountain road") and intersect result sets. (2) At reranking time, use a VLM (visual-language model) like LLaVA to re-score candidates with a prompt: "Does this image show a red sports car on a mountain road? Score 1-5." This adds ~80ms per candidate but dramatically improves compositional accuracy. (3) Long-term: fine-tune CLIP with hard negatives specifically targeting compositional failures.

**Deep Dive & Trade-offs:**
- Sub-query decomposition reduces recall (intersection is smaller than union) but improves precision.
- VLM reranking is expensive (~80ms per candidate on GPU for top-100 = 8s serial; batch to 100ms with batched inference).
- CLIP's weakness on compositionality is well-documented. SigLIP is marginally better. Dedicated models (NegCLIP) improve compositionality but sacrifice general retrieval quality.

**The Interviewer's Rubric:** Checking understanding of CLIP's known weaknesses and practical mitigation strategies.

---

Q: How do you handle a query that combines text and a reference image with different intent—e.g., text says "similar style" but the image is a specific subject?

**The Ideal Answer:** The user wants assets that match the *style* of the reference image but not necessarily the *content*. Standard weighted average of text and image embeddings conflates style and content. Fix: (1) disentangle style and content in the image embedding. Use a style-extraction model (e.g., fine-tuned CLIP with style-content disentanglement via AdaIN features) to produce a separate style vector. (2) Use the text query to constrain the *content* dimension and the image to constrain the *style* dimension. (3) At the UX level, expose explicit controls: "Match content" vs "Match style" vs "Match both" sliders. Internally, this adjusts the fusion weights between different embedding components.

**Deep Dive & Trade-offs:**
- Style-content disentanglement is an active research area. Production-quality solutions use gram matrices from intermediate CNN layers (style) vs final-layer features (content).
- Without disentanglement, the system defaults to holistic similarity, which satisfies neither intent well.
- Alternatively: use the text query to filter candidates first (content match), then rerank by visual style similarity to the reference image (style match). Two-stage approach avoids the fusion problem entirely.

**The Interviewer's Rubric:** Checking ability to decompose ambiguous multi-modal queries into tractable retrieval problems.

---

Q: Your index has 1.62B vectors and you need to support 10K QPS with < 15ms ANN search. How do you shard the index?

**The Ideal Answer:** With HNSW, each query's search time is O(log N * ef_search) where ef_search controls recall. At 1.62B vectors on a single machine, search takes ~50-100ms—too slow. Shard by hash: 16 shards, ~100M vectors each. Query is broadcast to all 16 shards in parallel; each shard searches in ~5-8ms. Merge top-K from each shard (K=20 per shard, merge to global top-100). Total ANN latency: ~10ms (dominated by slowest shard). For 10K QPS with 16-shard fan-out: each shard sees `10K QPS * 1 query = 10K QPS` (fan-out doesn't multiply per-shard QPS since it's the same query). With 2x replication per shard (32 total replicas), each replica handles 5K QPS. HNSW on 100M vectors with ef_search=64 can serve ~10K QPS per machine.

**Deep Dive & Trade-offs:**
- Hash sharding: uniform distribution, but no locality—every query hits every shard (fan-out = N_shards).
- Cluster-based sharding (IVF-style): assign vectors to shards by k-means cluster. Query hits only relevant shards (fan-out = 2-4). Reduces per-shard QPS but requires shard routing, and quality degrades if cluster assignment is poor.
- Hybrid: cluster-based sharding with a fallback to all-shard broadcast for queries that don't match any cluster well.
- At 10K QPS, fan-out to 16 shards is fine (total internal QPS = 160K, well within capacity with replication).

**The Interviewer's Rubric:** Checking distributed systems knowledge applied to vector index scaling.

---

Q: How do you detect and handle embedding model drift over time?

**The Ideal Answer:** Embedding drift occurs when: (1) the model is updated (intentional), or (2) the input distribution shifts (new types of assets being uploaded). Detection: maintain a reference set of 10K canonical query-asset pairs with known relevance labels. Weekly, compute retrieval metrics (R@10, nDCG@10) on this reference set. If metrics drop > 2% week-over-week, flag drift. Additionally, monitor the distribution of cosine similarities—if the mean similarity between queries and their clicked results decreases, the embedding space is drifting. Response: (1) for model updates: full re-embedding with shadow index migration. (2) For input distribution shift: fine-tune the model on recent data (last 30 days of click-through pairs) and re-evaluate.

**Deep Dive & Trade-offs:**
- Reference set must be periodically refreshed to avoid staleness (add 500 new pairs/month, retire oldest).
- Cosine similarity monitoring is cheap (compute on every query) but noisy. Combine with weekly reference set evaluation for reliable signal.
- Re-embedding is expensive but necessary for quality. Amortize by batching re-embeddings quarterly unless drift exceeds threshold.
- A lightweight alternative to full re-embedding: train a linear adapter (768→768 matrix) on paired old-new embeddings. This "patches" old embeddings to align with new space. Quality: ~95% of full re-embedding at 0.1% of the compute cost.

**The Interviewer's Rubric:** Checking proactive quality monitoring discipline for embedding-based systems.

---

Q: A customer wants to search for "a person giving a presentation" but your system must not use facial recognition. How do you handle person-related queries?

**The Ideal Answer:** CLIP embeddings capture scene-level semantics ("person giving a presentation" matches images with podiums, slides, audiences) without performing facial recognition. The system retrieves based on visual similarity to the *concept*, not facial identity. However, risks remain: (1) CLIP can implicitly cluster by perceived demographics. (2) Reverse-image-search with a person's photo could function as a facial recognition proxy. Mitigations: (1) For image-query mode, apply a person-detection model (YOLO) to the query image; if a face is dominant (>30% of image area), warn the user and require text-only query. (2) In the reranker, downweight person-identity features and upweight scene/activity features for person-related queries. (3) Audit: periodically test retrieval results for person-related queries to ensure results vary in demographics and don't cluster by identity.

**Deep Dive & Trade-offs:**
- Complete prevention of facial-similarity-based retrieval is impossible with any visual embedding model—all visual models encode facial features to some degree.
- Blocking image queries containing faces is heavy-handed but safe for regulated contexts (GDPR, BIPA).
- Alternative: use a face-anonymization preprocessing step (blur faces in query images before embedding). This preserves scene context while removing identity signal.

**The Interviewer's Rubric:** Checking ethical and regulatory awareness in visual search systems.

---

Q: How do you ensure result diversity—not just relevance—in top-10 results?

**The Ideal Answer:** Pure relevance ranking produces near-duplicate clusters in top results (10 sunset photos that are slightly different). Apply Maximal Marginal Relevance (MMR) at reranking time: `score(d) = λ * relevance(d) - (1-λ) * max_sim(d, S)` where S is the set of already-selected results and max_sim measures the maximum similarity to any already-selected result. λ=0.7 provides a good balance. Additionally: (1) category-level diversity: if assets have category labels, enforce max 3 results per category in top-10. (2) Visual diversity: compute pairwise cosine similarity within top-10; if any pair exceeds 0.95, remove the lower-scored one. (3) Modality diversity: for cross-modal queries, ensure top-10 includes at least 2 modalities if relevant results exist in multiple modalities.

**Deep Dive & Trade-offs:**
- MMR adds O(K²) computation per query (K=20, negligible at ~0.1ms).
- λ tuning: too aggressive diversity (λ=0.3) sacrifices relevance; too little (λ=0.9) doesn't help.
- Category-based diversity requires reliable categorization—misclassification produces worse results than no diversity.
- A/B test diversity parameters against user engagement (click-through rate on position 5-10 results).

**The Interviewer's Rubric:** Checking awareness that retrieval systems must optimize for user satisfaction, not just mathematical relevance.

---

Q: Your video search returns a 30-second clip but the relevant content is only at the 15-second mark. How do you surface the right moment?

**The Ideal Answer:** This is the temporal indexing problem. With hierarchical indexing (clip-level → keyframe-level), the second stage identifies the best-matching keyframe within each top clip. The UI surfaces a timestamp-linked preview: the video starts playing from 2 seconds before the matched keyframe. Implementation: (1) each keyframe has a timestamp. (2) When a clip is returned in results, include the timestamp of the highest-scoring keyframe. (3) The video player seeks to that timestamp. (4) Generate an animated thumbnail (3-second GIF) centered on the matched keyframe for the search results page. For long videos (>5 min), return multiple matched moments as separate results, each with its own timestamp and relevance score.

**Deep Dive & Trade-offs:**
- Animated thumbnails require pre-computation at indexing time (generate GIFs for all keyframes) or on-the-fly generation at query time (adds ~200ms latency).
- Pre-computation: `80M clips * 15 keyframes * 200KB/GIF = 240 TB` of thumbnail storage. Expensive but enables instant preview.
- Compromise: pre-compute for the 15M most-searched clips (based on historical query frequency). Generate on-the-fly for the long tail.
- UX impact: showing the matched moment instead of clip start increases video result click-through by 35% (measured in A/B tests at major video platforms).

**The Interviewer's Rubric:** Checking understanding of the gap between retrieving a video clip and surfacing the *relevant part* of that clip.

---

Q: You need to support a new modality—3D models. How do you extend the system?

**The Ideal Answer:** The architecture is designed for modality extensibility. Steps: (1) **Embedding:** render 3D models from N canonical viewpoints (12 views: front/back/sides/top/bottom/45° angles) → each rendered view is a 2D image → CLIP image encoder produces 12 embeddings per 3D model. Aggregate: mean of 12 view embeddings as the model-level embedding. (2) **Indexing:** add a 3D model shard to the ANN index service. Same HNSW infrastructure, new shard type. (3) **Query support:** text→3D works natively (CLIP text encoder query against 3D model embeddings). image→3D: the query image is already in CLIP space, direct cosine similarity. 3D→3D: embed the query 3D model with the same multi-view pipeline. (4) **Score calibration:** calibrate 3D model scores against image/video scores using the standard per-modality normalization. (5) **Ingestion:** add a 3D rendering service (Blender headless or trimesh) to the ingestion pipeline. Rendering 12 views: ~2s per model on CPU. For 1M 3D models: single-machine processing in ~23 days, or 10-machine cluster in ~2.3 days.

**Deep Dive & Trade-offs:**
- Multi-view rendering is a well-established technique (used by Objaverse, ShapeNet). Quality depends on view selection and lighting.
- Alternative: use a 3D-native encoder (Point-E, OpenShape) trained to project 3D representations into CLIP space directly. Avoids rendering but requires a specialized model.
- 12 views per model = 12x more embeddings to store. Use PCA or mean pooling to reduce to a single embedding for the primary index.

**The Interviewer's Rubric:** Checking modality-extensible architecture thinking and practical integration strategy.

## Exercises

### Design

**1. Design a multimodal search system for a fashion e-commerce platform with 50M product images.**

The platform supports "shop the look" queries where a user uploads a photo of an outfit and retrieves similar purchasable items. The catalog is updated with 50K new products daily. Design the end-to-end system covering: (a) the embedding model and fine-tuning strategy using the platform's purchase-signal data, (b) the index architecture (unified vs separate for category sub-types: tops, bottoms, shoes, accessories), (c) attribute-based filtering integration (color, size, price range) without breaking ANN recall, and (d) the cold-start strategy for new products before they accumulate user engagement signals. Discuss how you would ensure that results respect regional availability constraints (a product available in Germany must not appear in US search results).

**2. Design a video highlight extraction system that surfaces the "best moments" within long-form content (30–90 minute videos).**

A media company wants to auto-generate 30-second highlight clips for 2-hour sporting events for social media. Design: (a) the keyframe sampling strategy for long videos where uniform 0.5fps produces 3,600 frames per event, (b) how to identify "highlight-worthy" moments (score peaks, crowd noise, replays) using multimodal signals, (c) the temporal indexing architecture to enable both clip-level search ("find a basketball dunk") and moment-level retrieval ("the exact frame of the dunk"), and (d) the pipeline to generate the highlight clip preview (seek offset, duration, thumbnail) as part of the search result payload.

### Implementation

**3. Implement a hybrid query handler that accepts both a text string and an optional reference image, encodes each with CLIP, and returns a fused query vector with a user-adjustable α parameter.**

The implementation should: (a) handle the text-only, image-only, and hybrid cases in a single code path, (b) normalize both embeddings to unit vectors before combining to prevent one modality from dominating due to magnitude differences, (c) validate that α ∈ [0, 1] and produce a meaningful error if the user sets α=0.5 but provides no reference image, and (d) expose the fused vector as a NumPy array ready for ANN search. Add a test that verifies the fused vector is a unit vector for all three input combinations.

**4. Implement a per-modality score normalization pipeline that takes raw cosine similarity scores from three separate ANN indexes (image, video, document), normalizes each modality's scores independently using z-score normalization, and merges the results using Reciprocal Rank Fusion.**

The implementation should: (a) accept a dictionary mapping modality names to lists of `{"id": str, "score": float}` dicts, (b) compute z-score normalization per modality using numpy (handle the edge case where a modality returns only one result, producing a standard deviation of zero), (c) apply RRF with k=60 across the three normalized lists, and (d) return the merged list sorted by descending RRF score. Write a unit test verifying that the output contains at most one entry per unique asset ID, even when the same asset appears in multiple modality result lists.

### Debug

**5. Your cross-modal search system shows nDCG@10 of 0.71 for text→image queries but only 0.41 for image→image queries, despite both using the same CLIP image encoder for embedding. Diagnose and fix the issue.**

Start by examining the distribution of cosine similarity scores for the two query types — look for evidence that image query embeddings occupy a different region of the CLIP embedding space than text query embeddings (CLIP is trained on (text, image) pairs, so text and image embeddings are aligned differently). Check whether the image→image recall drop is uniform across query image types or concentrated in specific categories (photos vs illustrations vs screenshots). Investigate whether the normalization step after `model.get_image_features()` is being applied consistently to both query images and indexed images — a missing L2 normalization on either side collapses cosine similarity to dot-product with magnitude bias. Finally, consider that CLIP's training objective aligns text and image modalities globally but image→image nearest neighbors may require a different retrieval strategy: DINOv2 or a self-supervised visual model fine-tuned on the platform's image catalog often outperforms CLIP for pure visual similarity tasks where no text query is involved. Propose a remediation that preserves the unified index architecture while improving image→image recall to > 0.65 nDCG@10.

---

## End of Chapter

- **Key takeaway:** Multimodal search is an embedding quality problem first and an infrastructure scaling problem second. CLIP-family models provide the shared embedding space; the system's value comes from index architecture (unified vs separate), score calibration across modalities, and reranking with diversity controls. Video search requires hierarchical temporal indexing—a single embedding per clip loses temporal precision.
- **What to practice:** Size an HNSW index for 1B+ vectors: compute memory, shard count, fan-out QPS, and replication factor. Calculate end-to-end query latency from embedding inference through ANN search to reranking.
- **Interview drill:** Given a new modality (audio clips, 3D models, code snippets), walk through the full integration: embedding strategy, ingestion pipeline changes, index sharding, query fusion, and score calibration.

---

<!-- nav-footer -->
[[Chapter 14 - Design a Real-Time Meeting Summarizer|← Chapter 14]] | [[README|Contents]] | [[Chapter 16 - Design an AI Data Analyst (Text-to-SQL and Insights)|Chapter 16 →]]
