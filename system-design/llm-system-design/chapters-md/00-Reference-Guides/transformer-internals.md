---
title: "Transformer Internals — AI Engineer Deep Dive"
tags: [llm, transformer, attention, internals, theory, interview-prep]
---

# Transformer Internals — From First Principles

> [!tip] Why this matters for AI Engineer interviews
> System design rounds assume you can explain *why* architectural choices work.
> "Use Flash Attention" is a system design answer. "Flash Attention recomputes attention in tiles during the backward pass to avoid storing the O(n²) attention matrix, trading compute for HBM bandwidth" is an AI Engineer answer.

---

## 1. The Transformer in One Sentence

A Transformer is a function that maps a sequence of token embeddings to a new sequence of contextually-enriched embeddings, using attention to let each position gather information from every other position simultaneously.

---

## 2. Tokenization — Before the Model Sees Anything

**What it does:** Converts raw text into integer IDs. The model never sees characters or words — only token IDs.

**Byte-Pair Encoding (BPE) — the dominant approach:**

1. Start with character-level vocabulary
2. Count the most frequent adjacent byte pair (e.g., `t` + `h` → `th`)
3. Merge it into a new token; add to vocabulary
4. Repeat until vocabulary size is reached (GPT-4: ~100K tokens)

```
"tokenization" → ["token", "ization"]  → [15432, 1938]
"LLMOps"       → ["LL", "MO", "ps"]   → [2424, 6534, 591]
```

**Why it matters for interviews:**
- 1 token ≈ 0.75 words / ~4 characters (English prose)
- Code tokenizes less efficiently — Python uses ~1.5 tokens/word
- Non-English languages often use 3-5× more tokens per word than English
- A prompt that's 1,000 English words → ~1,333 tokens

**Tokenizer quirks:**
- Leading spaces matter: `" hello"` and `"hello"` are different tokens
- Numbers tokenize erratically: "100,000" may be 3-5 tokens
- This is why prompt compression can save 30-50% tokens — it exploits tokenization patterns

---

## 3. Embeddings — Turning IDs into Vectors

Each token ID maps to a learned dense vector (the embedding). For GPT-4o: d_model = 12,288.

```
Input:  [15432, 1938, 591]           # token IDs
Lookup: embedding_matrix[token_id]   # shape: (vocab_size, d_model)
Output: shape (seq_len, d_model)     # each token is now a vector
```

**Positional encoding** is added to inject sequence order information (since attention is order-agnostic):

```python
# Sinusoidal positional encoding (original Transformer)
PE[pos, 2i]   = sin(pos / 10000^(2i/d_model))
PE[pos, 2i+1] = cos(pos / 10000^(2i/d_model))

# Modern LLMs use Rotary Position Embedding (RoPE)
# RoPE encodes position by rotating Q and K vectors before attention
# Advantage: generalizes better to longer sequences than seen in training
```

---

## 4. Self-Attention — The Core Mechanism

**The key insight:** Each token's representation is a weighted average of all other tokens' values, where the weights reflect how relevant each token is.

### Step-by-step walkthrough

Given input X of shape (seq_len, d_model):

```
Step 1: Project to Q, K, V
  Q = X @ W_Q    # (seq_len, d_k)   "what am I looking for?"
  K = X @ W_K    # (seq_len, d_k)   "what do I contain?"
  V = X @ W_V    # (seq_len, d_v)   "what do I communicate if attended to?"

Step 2: Compute attention scores
  scores = Q @ K.T / sqrt(d_k)   # (seq_len, seq_len)

Step 3: Why divide by sqrt(d_k)?
  - Dot products of d_k-dimensional vectors have variance d_k
  - Without scaling: large d_k → very large dot products → softmax saturates
  - Saturated softmax → near-zero gradients → model stops learning
  - Dividing by sqrt(d_k) keeps variance at 1 regardless of d_k

Step 4: Apply causal mask (decoder-only models like GPT)
  - Position i can only attend to positions ≤ i
  - Set future positions to -∞ before softmax → they become 0 after softmax
  - This is what makes autoregressive generation possible

Step 5: Softmax → attention weights (sum to 1 per row)
  attention = softmax(scores)      # (seq_len, seq_len)

Step 6: Weighted sum of values
  output = attention @ V           # (seq_len, d_v)
```

### Concrete example

For the sentence "The cat sat":
- When processing "sat", Q_sat · K_cat may be high (verb attends to subject)
- attention["sat"]["cat"] ≈ 0.6, attention["sat"]["The"] ≈ 0.1, attention["sat"]["sat"] ≈ 0.3
- output["sat"] = 0.6 × V_cat + 0.1 × V_The + 0.3 × V_sat
- "sat" now encodes context about the cat

---

## 5. Multi-Head Attention

**Why multiple heads?** Single attention = one type of relationship per layer. Multiple heads allow the model to attend to different relationship types simultaneously (syntax, semantics, coreference, etc.).

```
d_model = 12288  (GPT-4 class)
n_heads = 96
d_k = d_model / n_heads = 128   (each head works in 128-dim subspace)

Each head: separate W_Q, W_K, W_V matrices
All heads computed in parallel
Outputs concatenated → projected back to d_model

MultiHead(Q,K,V) = Concat(head_1,...,head_h) @ W_O
```

**Interpretability:** Different heads learn different patterns — some attend to the previous token, some to syntactic heads, some to co-reference chains. This is observable and has been studied extensively.

---

## 6. KV Cache — How Inference Efficiency Works

**The problem:** During generation, we compute K and V for every token at every layer at every step. For a 1,000 token context generating 500 tokens → we'd recompute K,V 500 times for the 1,000 tokens.

**The solution:** Cache K and V for all previously computed positions.

```
Generating token t+1:
  - Q for position t+1: computed fresh (new token)
  - K for positions 0..t: CACHED from previous steps
  - V for positions 0..t: CACHED from previous steps
  - Only attend: Q_new × [K_cached | K_new]

Cost without KV cache: O(n²) per token (recompute everything)
Cost with KV cache:    O(n) per token (just the new position)
```

**Memory cost of KV cache:**
```
Per token, per layer:
  2 × d_model × sizeof(dtype)
  = 2 × 12288 × 2 bytes (BF16)
  = ~49 KB per token per layer

GPT-4 class (96 layers):
  = 49KB × 96 ≈ 4.7 MB per token in context

1,000 token context = ~4.7 GB of KV cache
This is why context window length is a GPU memory problem, not just a compute problem.
```

**PagedAttention (vLLM):** Instead of allocating KV cache contiguously per request, uses a paged memory system (like OS virtual memory) — allows multiple requests to share GPU memory dynamically without fragmentation. Enables 2-4× more concurrent requests.

---

## 7. Feed-Forward Network (FFN)

After attention, each position passes through a 2-layer MLP independently:

```
FFN(x) = max(0, x @ W1 + b1) @ W2 + b2

Typical sizes:
  d_model = 4096 (Llama-class 7B)
  d_ffn   = 4 × d_model = 16384

Parameters:
  2 × d_model × d_ffn = 2 × 4096 × 16384 ≈ 134M params per layer
  × 32 layers = 4.3B params just in FFN layers (of 7B total)
```

**Why is FFN so big?** FFN is where the model stores factual "memory" — key-value associations learned during training (like a lookup table). Attention routes to the right memory; FFN retrieves it.

---

## 8. Layer Normalization

Applied before attention and FFN (Pre-LayerNorm, used in modern LLMs):

```python
LayerNorm(x) = γ × (x - μ) / (σ + ε) + β

μ = mean of x over d_model dimension
σ = std of x over d_model dimension
γ, β = learned scale and shift parameters
ε = 1e-5 (numerical stability)
```

**Why LayerNorm not BatchNorm?**
- BatchNorm normalizes across the batch dimension — requires fixed batch size
- LayerNorm normalizes across the feature dimension — works with variable sequence lengths
- Transformers process sequences of variable length → BatchNorm doesn't apply

---

## 9. Quantization — What Actually Happens

**Goal:** Reduce model size and memory bandwidth at inference, with minimal quality loss.

### BF16 (Brain Float 16) — default for training and inference

```
FP32:  1 sign | 8 exponent | 23 mantissa bits  (32 bits, range ±3.4×10³⁸)
BF16:  1 sign | 8 exponent |  7 mantissa bits  (16 bits, same range as FP32)
FP16:  1 sign | 5 exponent | 10 mantissa bits  (16 bits, range ±65,504)
```

BF16 keeps the same exponent range as FP32 (handles the large/small values in training), just truncates mantissa precision. This is why BF16 is preferred over FP16 for training — FP16 overflows more easily.

### INT8 Post-Training Quantization

```
For each weight matrix W:
  scale = max(|W|) / 127
  W_int8 = round(W / scale).astype(int8)

At inference:
  output = (W_int8 @ input) × scale   # dequantize after matmul

Quality loss: <1% on most benchmarks
Memory savings: 50% vs BF16
Speed: 1.5-2× faster (INT8 matmul is faster on modern GPUs)
```

### INT4 / NF4 (used in QLoRA, on-device models)

Quantizes to 4 bits — 75% smaller than BF16. Quality loss: 1-3%.

**NF4 (NormalFloat4):** Uses non-uniform quantization levels designed for the near-normal distribution of neural network weights. Better quality than uniform INT4 at same bit-width.

**GGUF (used in llama.cpp):** File format for mixed-precision quantization — different layers quantized at different precisions (e.g., attention layers at higher precision than FFN).

### When quantization fails

- Outlier weights: some weights have extreme values that distort the quantization scale → LLM.int8() handles this with mixed-precision matmul
- Quantization of KV cache: risky — small errors in cached K,V accumulate over long generations

---

## 10. Flash Attention — Why It Matters

**Standard attention problem:** The full (seq_len × seq_len) attention matrix must be materialized in HBM (GPU high-bandwidth memory). For seq_len=8K: 8K×8K×2 bytes = 128MB per head per layer — a major memory bottleneck.

**Flash Attention solution:**
1. Process attention in tiles that fit in SRAM (fast on-chip memory)
2. Compute softmax statistics incrementally using the "online softmax" trick
3. Never write the full attention matrix to HBM
4. Recompute attention during backward pass instead of storing it

```
Standard attention: O(n²) HBM reads/writes
Flash Attention:    O(n) HBM reads/writes (constant factor for each block)

Wall-clock speedup: 2-4× for forward pass, 5-9× for backward pass
Memory savings: up to 20× for long sequences
Mathematical output: identical to standard attention (no approximation)
```

**Flash Attention 2 & 3:** Better work partitioning across GPU warps, reduced non-matmul FLOPs, async memory operations.

---

## 11. Speculative Decoding

**Problem:** Autoregressive generation is sequential — can't parallelize across output tokens. The large model generates 1 token per forward pass.

**Solution:** Use a small draft model to propose K tokens cheaply, then have the large target model verify all K in one forward pass.

```
Step 1: Draft model generates K=5 candidate tokens sequentially (cheap)
Step 2: Target model runs ONE forward pass over input + 5 candidates
Step 3: Accept/reject each candidate token:
  - If target model agrees with draft → accept, move forward
  - If disagreement → reject from that position, sample from target's distribution
Step 4: Guaranteed output quality = as if target model generated alone
```

**When it works:** Draft acceptance rate >70% — requires draft model to agree with target most of the time. Best for: greedy/low-temperature generation, code completion, structured output.

**When it doesn't work:** High-temperature creative generation — target model disagrees too often, negating the speedup.

**Draft model selection:** Must be same tokenizer as target. Typically 5-10× smaller (e.g., 7B draft for 70B target, or 1B draft for 7B target).

---

## 12. Mixture of Experts (MoE)

Modern frontier models (GPT-4, Mixtral, Gemini) use MoE to increase parameter count without increasing inference cost proportionally.

```
Standard dense model: ALL params used for every token
MoE model: Only top-K of N expert FFNs activated per token

Mixtral 8×7B:
  8 expert FFNs, 2 activated per token
  Total params: ~47B (8 × 7B)
  Active params per token: ~13B (2 × 7B, minus shared layers)
  Inference cost: similar to a 13B dense model
  Quality: similar to a 47B dense model
```

**Router:** A small learned network decides which experts handle each token. Routing is per-token, not per-request.

**Challenge:** Load balancing — if all tokens route to the same 2 experts, other experts never train. Auxiliary loss terms enforce balanced routing during training.

---

## Key Numbers to Memorize

| Concept | Value | Why |
|---|---|---|
| GPT-4o d_model | ~12,288 | Attention head width calculation |
| Llama-3 8B d_model | 4,096 | Common open-source reference |
| 1B params (BF16) | ~2 GB VRAM | Sizing rule: 2 GB/B |
| KV cache per token (70B, 80 layers) | ~4.7 MB | Context length → VRAM budget |
| Flash Attention speedup | 2-4× forward | Memory bandwidth reduction |
| Speculative decoding speedup | 2-4× TPOT | Only when acceptance rate >70% |
| INT8 quality loss | <1% | Safe for production serving |
| INT4 quality loss | 1-3% | Acceptable for edge/on-device |
| BPE vocab size (GPT-4) | ~100K tokens | Lookup table size |

---

## Interview Questions on Internals — Quick Reference

| Question | Key Answer |
|---|---|
| Why divide attention by √d_k? | Prevent softmax saturation from high-variance dot products |
| What does the causal mask do? | Prevents attending to future tokens (enables autoregressive generation) |
| What is KV cache? | Cache K,V for past tokens so only new token Q is computed each step |
| Why does longer context use more VRAM? | KV cache grows linearly with context length |
| What is Flash Attention? | Tiled computation that avoids materializing O(n²) attention matrix in HBM |
| How does speculative decoding work? | Draft model proposes K tokens; target verifies all K in 1 forward pass |
| BF16 vs FP16 for training? | BF16 has same exponent range as FP32; FP16 overflows more easily |
| What does FFN do vs attention? | Attention: gathers context across positions. FFN: stores + retrieves factual associations |
| What is MoE? | Only a subset of expert FFNs activated per token; scales params without proportional inference cost |
| Why LayerNorm not BatchNorm? | LN normalizes per-sequence feature dimension; BN requires fixed batch size |
