---
title: "ML Coding Patterns — AI Engineer Interview"
tags: [llm, coding, interview-prep, python, ml-patterns]
---

# ML Coding Patterns for AI Engineer Interviews

> [!important] How to use this file
> Every pattern has: the interview question, a clean Python implementation, complexity notes, and common follow-up twists.
> **Practice rule:** implement from memory, then compare. Don't just read — code it.

---

## Pattern 1 — Cosine Similarity

**Interview question:** *"Implement cosine similarity between two embedding vectors."*

```python
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Returns cosine similarity in [-1, 1].
    1.0 = identical direction, 0.0 = orthogonal, -1.0 = opposite.
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))

# Batch version (query vs corpus)
def cosine_similarity_batch(query: np.ndarray, corpus: np.ndarray) -> np.ndarray:
    """
    query: shape (D,)
    corpus: shape (N, D)
    returns: shape (N,) — similarity of query to each doc
    """
    query_norm = query / (np.linalg.norm(query) + 1e-8)
    corpus_norm = corpus / (np.linalg.norm(corpus, axis=1, keepdims=True) + 1e-8)
    return corpus_norm @ query_norm
```

**Complexity:** O(D) per pair, O(N·D) for batch | **Space:** O(N) for scores
**Follow-ups:** "What if vectors are already L2-normalized?" → just `np.dot(a, b)`. "How do you do this at 1M scale?" → FAISS/HNSW ANN index, not brute-force.

---

## Pattern 2 — Scaled Dot-Product Attention

**Interview question:** *"Implement the core attention mechanism from Q, K, V matrices."*

```python
import numpy as np

def scaled_dot_product_attention(
    Q: np.ndarray,  # (seq_len, d_k)
    K: np.ndarray,  # (seq_len, d_k)
    V: np.ndarray,  # (seq_len, d_v)
    mask: np.ndarray = None  # (seq_len, seq_len) boolean, True = mask out
) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns: (output, attention_weights)
    output shape: (seq_len, d_v)
    attention_weights shape: (seq_len, seq_len)
    """
    d_k = Q.shape[-1]

    # Step 1: compute raw scores
    scores = Q @ K.T / np.sqrt(d_k)  # (seq_len, seq_len)

    # Step 2: apply causal mask (decoder) — mask future positions
    if mask is not None:
        scores = np.where(mask, -1e9, scores)

    # Step 3: softmax over key dimension
    scores_shifted = scores - scores.max(axis=-1, keepdims=True)  # numerical stability
    exp_scores = np.exp(scores_shifted)
    attention_weights = exp_scores / exp_scores.sum(axis=-1, keepdims=True)

    # Step 4: weighted sum of values
    output = attention_weights @ V  # (seq_len, d_v)

    return output, attention_weights

# Build causal (autoregressive) mask
def causal_mask(seq_len: int) -> np.ndarray:
    """True = mask out (future positions)."""
    return np.triu(np.ones((seq_len, seq_len), dtype=bool), k=1)
```

**Why divide by √d_k?** Without scaling, dot products grow with d_k, pushing softmax into near-zero gradient regions (vanishing gradients). Dividing by √d_k keeps variance stable.

**Follow-ups:**
- "What does the causal mask do?" → Prevents position i from attending to positions > i (autoregressive generation)
- "How does Flash Attention differ?" → Computes attention in tiles to avoid materializing the full O(n²) score matrix; saves HBM bandwidth, same mathematical output
- "What is KV cache?" → During generation, K and V for previously computed tokens are cached; only the new token's Q is computed at each step

---

## Pattern 3 — BM25 Scoring

**Interview question:** *"Implement BM25 scoring for a query against a document corpus."*

```python
import math
from collections import Counter
from typing import List

class BM25:
    def __init__(self, corpus: List[List[str]], k1: float = 1.5, b: float = 0.75):
        """
        corpus: list of tokenized documents (list of word lists)
        k1: term frequency saturation (1.2–2.0, typically 1.5)
        b: length normalization (0=off, 1=full, typically 0.75)
        """
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.avgdl = sum(len(doc) for doc in corpus) / self.corpus_size

        # Build IDF index
        self.doc_freqs = []
        self.idf = {}
        df = Counter()

        for doc in corpus:
            freq = Counter(doc)
            self.doc_freqs.append(freq)
            for term in freq:
                df[term] += 1

        # IDF with smoothing: log((N - n + 0.5) / (n + 0.5) + 1)
        for term, n in df.items():
            self.idf[term] = math.log((self.corpus_size - n + 0.5) / (n + 0.5) + 1)

    def score(self, query: List[str], doc_idx: int) -> float:
        score = 0.0
        doc = self.doc_freqs[doc_idx]
        dl = sum(doc.values())  # document length

        for term in query:
            if term not in doc:
                continue
            tf = doc[term]
            idf = self.idf.get(term, 0)
            # BM25 TF component with length normalization
            tf_norm = (tf * (self.k1 + 1)) / (
                tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            )
            score += idf * tf_norm
        return score

    def rank(self, query: List[str], top_k: int = 10) -> List[tuple]:
        """Returns list of (doc_idx, score) sorted descending."""
        scores = [(i, self.score(query, i)) for i in range(self.corpus_size)]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
```

**Key insight:** BM25 saturates TF (adding a 100th occurrence of a word barely helps) and penalizes long documents. Dense retrieval misses exact term matches (product codes, names, IDs) — that's why hybrid = BM25 + dense.

**Follow-up:** "How do you combine BM25 and dense scores?" → **Reciprocal Rank Fusion (RRF):** `score = Σ 1/(k + rank_i)` where k=60. Rank-based, no normalization needed.

---

## Pattern 4 — Sliding Window Chunker

**Interview question:** *"Write a function to chunk a long document into overlapping windows for RAG indexing."*

```python
from typing import List

def chunk_text(
    text: str,
    chunk_size: int = 400,       # tokens (approximated by words here)
    overlap: int = 80,            # ~20% overlap
    separator: str = "\n\n"       # try to split on paragraph boundaries
) -> List[dict]:
    """
    Returns list of chunks with metadata.
    In production: use a real tokenizer (tiktoken) for token-accurate sizing.
    """
    # Split on natural boundaries first
    paragraphs = text.split(separator)
    words = []
    para_boundaries = []  # track which word index starts a new paragraph

    for para in paragraphs:
        para_boundaries.append(len(words))
        words.extend(para.split())

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        # Try to align end to a paragraph boundary for cleaner chunks
        best_end = end
        for boundary in para_boundaries:
            if start < boundary <= end:
                best_end = boundary

        chunk_words = words[start:best_end]
        chunks.append({
            "chunk_id": chunk_id,
            "text": " ".join(chunk_words),
            "start_word": start,
            "end_word": best_end,
            "word_count": len(chunk_words),
        })

        chunk_id += 1
        start = best_end - overlap  # slide back by overlap
        if start <= 0:
            break

    return chunks

# Production version uses tiktoken for exact token counts:
# import tiktoken
# enc = tiktoken.encoding_for_model("gpt-4o")
# tokens = enc.encode(text)
# then chunk the token list and decode each chunk
```

**Follow-ups:**
- "How do you chunk FAQs differently?" → Keep Q+A pairs atomic — never split a question from its answer
- "How do you chunk legal docs?" → Split at numbered clause boundaries, not fixed size
- "What metadata do you attach?" → `source_id`, `page`, `section`, `last_updated`, `freshness_ttl`, `acl_tags`

---

## Pattern 5 — LLM API Retry with Exponential Backoff

**Interview question:** *"Write a resilient wrapper for an LLM API call that handles rate limits and transient errors."*

```python
import time
import random
from typing import Callable, Any
import openai

def llm_call_with_retry(
    fn: Callable,
    *args,
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable_errors: tuple = (
        openai.RateLimitError,
        openai.APITimeoutError,
        openai.InternalServerError,
    ),
    **kwargs
) -> Any:
    """
    Exponential backoff with jitter for LLM API calls.
    Non-retryable errors (AuthenticationError, InvalidRequestError) raise immediately.
    """
    for attempt in range(max_retries + 1):
        try:
            return fn(*args, **kwargs)

        except retryable_errors as e:
            if attempt == max_retries:
                raise  # exhausted retries

            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)  # ±10% jitter to avoid thundering herd
            wait = delay + jitter

            print(f"Attempt {attempt+1} failed: {e}. Retrying in {wait:.1f}s...")
            time.sleep(wait)

        except Exception:
            raise  # non-retryable — fail fast

# Usage
def call_openai(prompt: str) -> str:
    client = openai.OpenAI()
    response = llm_call_with_retry(
        client.chat.completions.create,
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        timeout=30,
    )
    return response.choices[0].message.content

# Streaming version
def call_openai_streaming(prompt: str):
    client = openai.OpenAI()
    stream = llm_call_with_retry(
        client.chat.completions.create,
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

**Follow-ups:** "How do you handle timeouts differently from rate limits?" → Timeout = retry immediately with longer timeout. Rate limit = honour the `Retry-After` header if present. "What's thundering herd?" → All clients retrying at exactly the same time — jitter prevents it.

---

## Pattern 6 — Semantic Cache

**Interview question:** *"Implement a simple semantic cache for LLM responses."*

```python
import numpy as np
from dataclasses import dataclass, field
from typing import Optional
import time

@dataclass
class CacheEntry:
    query_embedding: np.ndarray
    response: str
    created_at: float = field(default_factory=time.time)
    ttl_seconds: float = 3600  # 1 hour default

    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl_seconds

class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.92, max_size: int = 10_000):
        self.threshold = similarity_threshold
        self.max_size = max_size
        self.entries: list[CacheEntry] = []

    def _embed(self, text: str) -> np.ndarray:
        # In production: call an embedding model API
        # Here: placeholder returning random vector
        raise NotImplementedError("Replace with real embedding call")

    def get(self, query: str) -> Optional[str]:
        query_emb = self._embed(query)
        best_score = -1.0
        best_entry = None

        for entry in self.entries:
            if entry.is_expired():
                continue
            score = float(np.dot(query_emb, entry.query_embedding) /
                         (np.linalg.norm(query_emb) * np.linalg.norm(entry.query_embedding) + 1e-8))
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_score >= self.threshold and best_entry:
            return best_entry.response
        return None  # cache miss

    def put(self, query: str, response: str, ttl_seconds: float = 3600):
        if len(self.entries) >= self.max_size:
            # Evict oldest entry (LRU would be better in production)
            self.entries.pop(0)

        query_emb = self._embed(query)
        self.entries.append(CacheEntry(
            query_embedding=query_emb,
            response=response,
            ttl_seconds=ttl_seconds,
        ))
```

**Key numbers:** Threshold 0.92 balances hit rate vs false positives. ~40% hit rate on FAQ-like workloads. TTL varies: 1h for policy content, 7d for stable FAQs.

**Follow-up:** "How do you invalidate cache when source docs change?" → Store `source_id` per entry, purge all entries tied to that source when the doc is updated.

---

## Pattern 7 — LLM-as-Judge Eval Loop

**Interview question:** *"Write an evaluation loop that uses an LLM to score model outputs on a golden test set."*

```python
import json
from dataclasses import dataclass
from typing import List, Callable
import openai

@dataclass
class EvalCase:
    question: str
    context: str
    ground_truth: str
    model_output: str = ""

@dataclass
class EvalResult:
    case: EvalCase
    score: float          # 0.0 – 1.0
    reasoning: str
    passed: bool          # score >= threshold

JUDGE_PROMPT = """You are evaluating a RAG system's answer.

Question: {question}
Context provided to the model: {context}
Ground truth answer: {ground_truth}
Model's answer: {model_output}

Score the model's answer on these dimensions (each 0-3):
1. Faithfulness: Is every claim in the answer supported by the context?
2. Correctness: Does it match the ground truth?
3. Completeness: Does it cover all key points from the ground truth?

Respond ONLY with valid JSON:
{{"faithfulness": <0-3>, "correctness": <0-3>, "completeness": <0-3>, "reasoning": "<one sentence>"}}"""

def judge_single(client: openai.OpenAI, case: EvalCase, threshold: float = 0.7) -> EvalResult:
    prompt = JUDGE_PROMPT.format(
        question=case.question,
        context=case.context[:2000],  # truncate to control judge cost
        ground_truth=case.ground_truth,
        model_output=case.model_output,
    )
    response = client.chat.completions.create(
        model="gpt-4o",  # stronger model as judge
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0,  # deterministic judge
    )
    result = json.loads(response.choices[0].message.content)
    # Normalize to 0-1
    score = (result["faithfulness"] + result["correctness"] + result["completeness"]) / 9.0
    return EvalResult(
        case=case,
        score=score,
        reasoning=result["reasoning"],
        passed=score >= threshold,
    )

def run_eval(
    cases: List[EvalCase],
    model_fn: Callable[[str, str], str],  # (question, context) -> answer
    judge_client: openai.OpenAI,
    threshold: float = 0.7,
) -> dict:
    results = []
    for case in cases:
        case.model_output = model_fn(case.question, case.context)
        result = judge_single(judge_client, case, threshold)
        results.append(result)

    pass_rate = sum(r.passed for r in results) / len(results)
    avg_score = sum(r.score for r in results) / len(results)
    failures = [r for r in results if not r.passed]

    return {
        "pass_rate": pass_rate,
        "avg_score": avg_score,
        "total": len(results),
        "failed": len(failures),
        "failures": failures,
        "gate_passed": pass_rate >= threshold,
    }
```

**Follow-ups:** "How do you prevent judge position bias?" → Randomize order of ground truth vs model output in pairwise evals. "How do you track judge drift?" → Compute Cohen's kappa against a held-out human-labeled set quarterly.

---

## Pattern 8 — Token Budget Checker

**Interview question:** *"Write a function that validates a prompt fits within a model's context window and estimates cost."*

```python
import tiktoken
from dataclasses import dataclass

@dataclass
class TokenBudget:
    model: str
    context_window: int
    input_cost_per_1k: float   # USD
    output_cost_per_1k: float  # USD

MODEL_CONFIGS = {
    "gpt-4o":       TokenBudget("gpt-4o",       128_000, 0.005, 0.015),
    "gpt-4o-mini":  TokenBudget("gpt-4o-mini",  128_000, 0.00015, 0.0006),
    "gpt-4-turbo":  TokenBudget("gpt-4-turbo",  128_000, 0.01, 0.03),
}

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def check_budget(
    system_prompt: str,
    user_message: str,
    context_chunks: list[str],
    model: str = "gpt-4o-mini",
    max_output_tokens: int = 500,
    safety_margin: float = 0.9,  # use only 90% of window
) -> dict:
    config = MODEL_CONFIGS[model]
    effective_window = int(config.context_window * safety_margin)

    system_tokens = count_tokens(system_prompt, model)
    user_tokens = count_tokens(user_message, model)
    context_tokens = sum(count_tokens(c, model) for c in context_chunks)
    total_input = system_tokens + user_tokens + context_tokens

    fits = (total_input + max_output_tokens) <= effective_window
    input_cost = (total_input / 1000) * config.input_cost_per_1k
    output_cost = (max_output_tokens / 1000) * config.output_cost_per_1k

    return {
        "fits_in_window": fits,
        "total_input_tokens": total_input,
        "available_for_output": effective_window - total_input,
        "estimated_cost_usd": round(input_cost + output_cost, 6),
        "breakdown": {
            "system": system_tokens,
            "user": user_tokens,
            "context": context_tokens,
        }
    }
```

---

## Pattern 9 — Simple RAG Pipeline

**Interview question:** *"Implement a minimal end-to-end RAG pipeline."*

```python
import numpy as np
from typing import List
import openai

class SimpleRAG:
    def __init__(self, client: openai.OpenAI):
        self.client = client
        self.chunks: List[str] = []
        self.embeddings: np.ndarray = None

    def _embed(self, texts: List[str]) -> np.ndarray:
        response = self.client.embeddings.create(
            input=texts,
            model="text-embedding-3-small",
        )
        return np.array([r.embedding for r in response.data])

    def index(self, documents: List[str]):
        """Chunk, embed, and store documents."""
        # Simple fixed-size chunker (use Pattern 4 for production)
        self.chunks = []
        for doc in documents:
            words = doc.split()
            for i in range(0, len(words), 400):
                self.chunks.append(" ".join(words[i:i+400]))
        self.embeddings = self._embed(self.chunks)

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """Find top-k most relevant chunks."""
        query_emb = self._embed([query])[0]
        # Cosine similarity (embeddings are L2-normalized from OpenAI)
        scores = self.embeddings @ query_emb
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.chunks[i] for i in top_indices]

    def answer(self, query: str, top_k: int = 3) -> dict:
        """Full RAG: retrieve + generate with citation."""
        retrieved = self.retrieve(query, top_k)
        context = "\n\n---\n\n".join(
            f"[Source {i+1}]\n{chunk}" for i, chunk in enumerate(retrieved)
        )
        system_prompt = (
            "Answer the question using ONLY the provided context. "
            "If the answer is not in the context, say 'I don't have enough information.' "
            "Cite sources as [Source N]."
        )
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
            ],
            temperature=0.1,
        )
        return {
            "answer": response.choices[0].message.content,
            "retrieved_chunks": retrieved,
            "usage": response.usage.model_dump(),
        }
```

---

## Pattern 10 — ROUGE-L Score (Recall-Oriented Evaluation)

**Interview question:** *"Implement ROUGE-L for evaluating summarization quality."*

```python
def lcs_length(a: list, b: list) -> int:
    """Longest Common Subsequence length."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

def rouge_l(reference: str, hypothesis: str) -> dict:
    """
    Compute ROUGE-L precision, recall, F1.
    reference: ground truth summary
    hypothesis: model-generated summary
    """
    ref_tokens = reference.lower().split()
    hyp_tokens = hypothesis.lower().split()

    if not ref_tokens or not hyp_tokens:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    lcs = lcs_length(ref_tokens, hyp_tokens)
    precision = lcs / len(hyp_tokens)
    recall = lcs / len(ref_tokens)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}
```

**When to use:** Summarization tasks where word order matters. For QA tasks, prefer exact match or LLM-as-judge. For retrieval, use nDCG@k.

---

## Pattern 11 — Intent Router (Complexity Classifier)

**Interview question:** *"Implement a simple query router that routes to small vs large model based on complexity."*

```python
from enum import Enum
import re

class ModelTier(Enum):
    SMALL = "gpt-4o-mini"    # simple/short queries
    LARGE = "gpt-4o"          # complex/multi-step queries

SIMPLE_PATTERNS = [
    r"^(what is|what's|define|who is|when did|where is)\b",
    r"^(yes|no|true|false|ok|sure|thanks)",
    r"^.{0,50}$",  # very short queries likely simple
]

COMPLEX_SIGNALS = [
    r"(compare|contrast|explain.*why|analyze|evaluate|design|architect)",
    r"(step.by.step|walk me through|how would you|trade.off)",
    r".{500,}",  # long queries suggest complex multi-part questions
]

def classify_complexity(query: str) -> ModelTier:
    """Rule-based router — replace with a fine-tuned classifier in production."""
    query_lower = query.lower().strip()

    # Check complex signals first (higher priority)
    for pattern in COMPLEX_SIGNALS:
        if re.search(pattern, query_lower):
            return ModelTier.LARGE

    # Check simple patterns
    for pattern in SIMPLE_PATTERNS:
        if re.search(pattern, query_lower):
            return ModelTier.SMALL

    # Default to small — prefer cost efficiency, escalate on low confidence
    return ModelTier.SMALL

def route_request(query: str, client) -> dict:
    tier = classify_complexity(query)
    response = client.chat.completions.create(
        model=tier.value,
        messages=[{"role": "user", "content": query}],
    )
    return {
        "answer": response.choices[0].message.content,
        "model_used": tier.value,
        "tokens": response.usage.total_tokens,
    }
```

**Production note:** Replace rule-based with a fine-tuned DistilBERT-class classifier (~10ms inference). Track routing accuracy by comparing small-model outputs where large-model was available. Target: 70-80% of traffic on small model.

---

## Pattern 12 — Simple Rate Limiter (Token Bucket)

**Interview question:** *"Implement a token bucket rate limiter for LLM API calls."*

```python
import time
import threading
from dataclasses import dataclass, field

@dataclass
class TokenBucket:
    """
    Token bucket rate limiter.
    Allows burst up to `capacity`, then rate-limits to `rate` tokens/second.
    """
    capacity: float        # max tokens (burst size)
    rate: float            # tokens added per second
    tokens: float = field(init=False)
    last_refill: float = field(init=False)
    lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def __post_init__(self):
        self.tokens = self.capacity
        self.last_refill = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        added = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + added)
        self.last_refill = now

    def consume(self, tokens: int = 1, block: bool = True) -> bool:
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            if not block:
                return False
            # Calculate wait time and sleep
            wait = (tokens - self.tokens) / self.rate
        time.sleep(wait)
        return self.consume(tokens, block=False)

# Usage: 60 requests/min with burst of 10
limiter = TokenBucket(capacity=10, rate=1.0)  # 1 token/second = 60/min

def rate_limited_llm_call(prompt: str, client) -> str:
    limiter.consume(1)  # blocks if at rate limit
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    ).choices[0].message.content
```

---

## Pattern 13 — Streaming Response Handler

**Interview question:** *"Handle a streaming LLM response and build the full output incrementally."*

```python
import openai
import time
from dataclasses import dataclass

@dataclass
class StreamResult:
    content: str
    ttft_ms: float      # time to first token
    total_ms: float     # total duration
    token_count: int    # approximate

def stream_with_metrics(prompt: str, client: openai.OpenAI) -> StreamResult:
    start = time.monotonic()
    ttft = None
    content_parts = []
    token_count = 0

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            if ttft is None:
                ttft = (time.monotonic() - start) * 1000  # ms
            content_parts.append(delta)
            token_count += 1
            # In a web app: yield delta to the client here (SSE/WebSocket)
            print(delta, end="", flush=True)

    total = (time.monotonic() - start) * 1000
    return StreamResult(
        content="".join(content_parts),
        ttft_ms=ttft or total,
        total_ms=total,
        token_count=token_count,
    )
```

---

## Quick Reference: When to Use Which Eval Metric

| Metric | Use For | Not Good For |
|---|---|---|
| Exact Match | Closed-form QA, structured output | Open-ended generation |
| ROUGE-L | Summarization | Factual accuracy |
| BLEU | Translation | RAG grounding |
| nDCG@k | Retrieval ranking quality | Generation quality |
| BERTScore | Semantic similarity | Exact factual claims |
| LLM-as-Judge | All open-ended tasks | When judge cost is prohibitive |
| Human eval | Ground truth calibration | At scale (expensive) |
| Task success rate | End-to-end goal completion | Intermediate step quality |
| Faithfulness (RAGAS) | RAG hallucination detection | Non-RAG tasks |

---

## Interview Coding Tips

1. **Always handle the zero/empty case first** — interviewers notice
2. **State time + space complexity** before starting to code
3. **For NumPy:** say "in production I'd use FAISS for ANN at scale" after writing brute-force
4. **For LLM calls:** always mention retries, timeouts, and cost estimation
5. **After coding:** trace through a small example out loud
6. **Testing:** write one assert before they ask — shows production instinct
