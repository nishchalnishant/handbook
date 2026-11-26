"""
============================================================
TEMPLATE 10: Attention Mechanism (Bahdanau + Scaled Dot-Product)
============================================================
Standalone attention modules, plus an attention-augmented seq2seq
decoder showing how attention fixes the fixed-context bottleneck from
Template 9. Interview-scoped: focuses on the mechanism itself.
============================================================
"""

import math

import torch
from torch import nn, Tensor
import torch.nn.functional as F


# ------------------------------------------------------------
# 1. Bahdanau (additive) attention — classic seq2seq attention
# ------------------------------------------------------------
def build_bahdanau_attention(hidden_dim: int) -> nn.ModuleDict:
    """Computes attention weights between a single decoder hidden state
    (query) and all encoder hidden states (keys/values), via a small
    feedforward network ("additive" scoring).

    Shape trace (B=batch, T=src_len, H=hidden_dim):
        decoder_hidden:   (B, H)
        encoder_outputs:  (B, T, H)
        scores:           (B, T)        [one score per source position]
        attn_weights:     (B, T)        [softmax over scores, sums to 1]
        context:          (B, H)        [weighted sum of encoder_outputs]
    """
    return nn.ModuleDict({
        "attn": nn.Linear(hidden_dim * 2, hidden_dim),
        "v": nn.Linear(hidden_dim, 1, bias=False),
    })


def forward_bahdanau_attention(m: nn.ModuleDict, decoder_hidden: Tensor, encoder_outputs: Tensor) -> tuple[Tensor, Tensor]:
    T = encoder_outputs.size(1)
    # Repeat decoder hidden state across source length to compare
    # against every encoder position.
    decoder_hidden_rep = decoder_hidden.unsqueeze(1).repeat(1, T, 1)  # (B, T, H)
    energy = torch.tanh(m["attn"](torch.cat([decoder_hidden_rep, encoder_outputs], dim=2)))  # (B, T, H)
    scores = m["v"](energy).squeeze(2)                 # (B, T)

    attn_weights = F.softmax(scores, dim=1)            # (B, T), sums to 1 over source positions
    context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs).squeeze(1)  # (B, H)
    return context, attn_weights


# ------------------------------------------------------------
# 2. Scaled dot-product attention — the Transformer building block
# ------------------------------------------------------------
def scaled_dot_product_attention(
    query: Tensor, key: Tensor, value: Tensor, mask: Tensor | None = None
) -> tuple[Tensor, Tensor]:
    """Core attention operation used throughout Transformers.

    Shape trace (B=batch, H=num_heads, Tq=query_len, Tk=key_len, d=head_dim):
        query: (B, H, Tq, d)
        key:   (B, H, Tk, d)
        value: (B, H, Tk, d)
        scores = QK^T / sqrt(d):  (B, H, Tq, Tk)
        attn_weights = softmax(scores, dim=-1): (B, H, Tq, Tk)
        output = attn_weights @ V: (B, H, Tq, d)

    Why divide by sqrt(d): without scaling, dot products grow large in
    magnitude as d increases, pushing softmax into regions with extremely
    small gradients (saturation). Scaling keeps the variance of scores
    roughly constant regardless of head_dim.
    """
    d = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d)  # (B, H, Tq, Tk)

    if mask is not None:
        # Mask out invalid positions (padding or future tokens) before
        # softmax by setting their score to -inf so softmax assigns ~0 weight.
        scores = scores.masked_fill(mask == 0, float("-inf"))

    attn_weights = F.softmax(scores, dim=-1)
    output = torch.matmul(attn_weights, value)  # (B, H, Tq, d)
    return output, attn_weights


# ------------------------------------------------------------
# 3. Multi-head attention (built from the primitive above)
# ------------------------------------------------------------
def build_multi_head_attention(embed_dim: int, num_heads: int) -> nn.ModuleDict:
    """Splits embed_dim into num_heads parallel attention heads, each
    attending in a lower-dimensional subspace, then concatenates results.

    Why multiple heads: lets the model jointly attend to information from
    different representation subspaces at different positions (e.g. one
    head might learn syntactic relations, another semantic similarity).
    """
    assert embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads"
    return nn.ModuleDict({
        "q_proj": nn.Linear(embed_dim, embed_dim),
        "k_proj": nn.Linear(embed_dim, embed_dim),
        "v_proj": nn.Linear(embed_dim, embed_dim),
        "out_proj": nn.Linear(embed_dim, embed_dim),
    })


def _split_heads(x: Tensor, batch_size: int, num_heads: int, head_dim: int) -> Tensor:
    # (B, T, embed_dim) -> (B, num_heads, T, head_dim)
    x = x.view(batch_size, -1, num_heads, head_dim)
    return x.transpose(1, 2)


def forward_multi_head_attention(
    m: nn.ModuleDict, query: Tensor, key: Tensor, value: Tensor, num_heads: int, mask: Tensor | None = None
) -> Tensor:
    B = query.size(0)
    embed_dim = query.size(-1)
    head_dim = embed_dim // num_heads

    q = _split_heads(m["q_proj"](query), B, num_heads, head_dim)
    k = _split_heads(m["k_proj"](key), B, num_heads, head_dim)
    v = _split_heads(m["v_proj"](value), B, num_heads, head_dim)

    attn_output, _ = scaled_dot_product_attention(q, k, v, mask)  # (B, num_heads, T, head_dim)

    # Merge heads back: (B, num_heads, T, head_dim) -> (B, T, embed_dim)
    attn_output = attn_output.transpose(1, 2).contiguous().view(B, -1, num_heads * head_dim)
    return m["out_proj"](attn_output)


if __name__ == "__main__":
    # Minimal smoke test demonstrating shapes end-to-end.
    torch.manual_seed(42)
    B, T, embed_dim, num_heads = 2, 5, 16, 4

    x = torch.randn(B, T, embed_dim)
    mha = build_multi_head_attention(embed_dim, num_heads)
    out = forward_multi_head_attention(mha, x, x, x, num_heads)  # self-attention: query=key=value
    print(f"Self-attention output shape: {out.shape}")  # (2, 5, 16)

    bahdanau = build_bahdanau_attention(hidden_dim=embed_dim)
    decoder_hidden = torch.randn(B, embed_dim)
    context, weights = forward_bahdanau_attention(bahdanau, decoder_hidden, x)
    print(f"Bahdanau context shape: {context.shape}, weights shape: {weights.shape}")


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: any task needing dynamic, content-based weighting over a
#   set of vectors — seq2seq (Bahdanau), Transformers (scaled dot-product),
#   or as a building block layered into custom architectures.
# Advantages: removes the fixed-context bottleneck of vanilla seq2seq;
#   provides interpretability via attention weights; parallelizable
#   (scaled dot-product, unlike RNN recurrence).
# Disadvantages: O(T^2) time/memory in sequence length for self-attention;
#   Bahdanau-style additive attention is comparatively slow (extra FFN per
#   score) vs dot-product attention.
# Complexity: scaled dot-product attention is O(T^2 * d) time and O(T^2)
#   memory for the attention matrix.
# Follow-ups to expect:
#   - Why scale by sqrt(d)? (prevents large-magnitude dot products from
#     saturating softmax gradients.)
#   - Self-attention vs cross-attention? (query/key/value all from same
#     sequence vs query from one sequence, key/value from another —
#     e.g. decoder attending to encoder outputs.)
#   - Why multiple heads instead of one large attention op? (lets different
#     heads specialize in different relational patterns; empirically improves
#     performance at similar total compute.)
#   - How is masking used differently in encoder vs decoder self-attention?
#     (encoder: mask padding only; decoder: mask padding AND future tokens
#     — causal mask, see Template 12.)
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Cross-attention: query from decoder, key/value from encoder outputs —
#   used in Transformer decoder (Template 12) and full Transformer (13).
# Causal (masked) self-attention: additional upper-triangular mask so
#   position i cannot attend to positions > i — used in GPT-style decoders.
# Additive vs dot-product attention: additive (Bahdanau) scales better to
#   different query/key dimensions; dot-product is faster/more common at scale.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: need dynamic, learned weighting over a variable-size set of
#   vectors — foundational to all modern seq2seq/Transformer architectures.
# Pros: removes fixed-context bottleneck, interpretable weights, parallelizable.
# Cons: O(T^2) compute/memory for self-attention, can be a bottleneck for
#   very long sequences (motivates sparse/linear attention variants).
# Time complexity: O(T^2 * d) for scaled dot-product attention.
# Space complexity: O(T^2) for the attention weight matrix per head.
# Common mistakes: forgetting the sqrt(d) scaling factor; applying softmax
#   over the wrong dimension; not masking padding/future tokens correctly;
#   confusing self-attention (Q=K=V source) with cross-attention.
# Production checklist: use masking correctly for padding and causality,
#   consider FlashAttention/memory-efficient attention kernels for long
#   sequences, monitor attention entropy/collapse as a debugging signal.
# ============================================================
