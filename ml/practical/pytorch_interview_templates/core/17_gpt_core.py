"""Core: GPT — causal self-attention blocks + autoregressive generation.

INTERVIEW GUIDE
----------------
Typical ask: "Implement a minimal GPT / decoder-only transformer from
scratch" (nanoGPT-style). This is a common "deep dive" question for
ML/research-adjacent roles — expect the full hour, or the last 30-40 min
after a warm-up.

Expected depth (1hr session):
  - Junior/mid: rarely asked to write this cold; if so, get single-head
    causal attention + one block working with correct shapes.
  - Senior/research: expected to write build_causal_self_attention,
    build_gpt_block, and build_gpt largely unprompted, explain every
    shape transition (B,T,C -> B,nh,T,hd and back), and reason about
    why each design choice (pre-norm, GELU, causal mask) exists.
  This is usually the main event of the hour, not a warm-up — budget
  15-20 min for attention alone, 15-20 min for the block/full model,
  remainder for generate() and follow-ups.

Common follow-ups:
  - "Walk me through the causal mask." (torch.tril gives a lower-triangular
    matrix of 1s; masked_fill sets future positions to -inf before
    softmax so they get exactly 0 attention weight — never masked after
    softmax, that would leak nonzero probability mass to the future.)
  - "Why pre-norm (LN before attn/mlp) instead of post-norm?" (GPT-2 and
    later models use pre-norm because it keeps gradients more stable at
    depth — post-norm needs learning rate warmup to avoid divergence).
  - "Why does position_embedding cap out at block_size?" (learned position
    embeddings only have entries for indices < block_size; a sequence
    longer than that has no embedding to look up — this is why generate()
    crops idx to the last block_size tokens before each forward pass).
  - "Why divide attention scores by sqrt(head_dim) and not sqrt(embed_dim)?"
    (scaling is per-head, since the dot product variance scales with the
    dimension actually being summed over, i.e. head_dim).
  - "What's the difference between this and BERT's encoder block?" (no
    causal mask, bidirectional attention, no autoregressive generate()).
  - "How would you add KV-caching to speed up generate()?" (recompute is
    wasteful — cache K/V per layer across steps instead of recomputing
    forward_gpt on the full growing context each iteration).

Gotchas to mention proactively:
  - generate() is O(n^2) per token because it reruns the full forward pass
    on the growing context every step — call this out as the naive
    version and mention KV-caching as the production fix.
  - masked_fill with -inf before softmax, never after — silently wrong if
    done post-softmax (nonzero probability leaks to future tokens).
  - block_size caps context length structurally (via position_embedding
    and the registered causal_mask buffer size) — not just a training
    hyperparameter, it's a hard architectural limit at inference too.
"""

import math

import torch
import torch.nn.functional as F
from torch import nn, Tensor


def build_causal_self_attention(embed_dim: int, num_heads: int, block_size: int, dropout: float) -> nn.ModuleDict:
    assert embed_dim % num_heads == 0
    m = nn.ModuleDict({
        "qkv": nn.Linear(embed_dim, 3 * embed_dim),
        "proj": nn.Linear(embed_dim, embed_dim),
        "dropout": nn.Dropout(dropout),
    })
    m.num_heads = num_heads
    m.head_dim = embed_dim // num_heads
    m.register_buffer(
        "causal_mask",
        torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size),
    )
    return m


def forward_causal_self_attention(m: nn.ModuleDict, x: Tensor) -> Tensor:
    B, T, C = x.shape
    qkv = m["qkv"](x)
    q, k, v = qkv.split(C, dim=2)
    q = q.view(B, T, m.num_heads, m.head_dim).transpose(1, 2)
    k = k.view(B, T, m.num_heads, m.head_dim).transpose(1, 2)
    v = v.view(B, T, m.num_heads, m.head_dim).transpose(1, 2)

    attn_scores = (q @ k.transpose(-2, -1)) / math.sqrt(m.head_dim)
    attn_scores = attn_scores.masked_fill(m.causal_mask[:, :, :T, :T] == 0, float("-inf"))
    attn_weights = F.softmax(attn_scores, dim=-1)
    attn_weights = m["dropout"](attn_weights)

    out = attn_weights @ v
    out = out.transpose(1, 2).contiguous().view(B, T, C)
    return m["proj"](out)


def build_gpt_block(embed_dim: int, num_heads: int, block_size: int, dropout: float) -> nn.ModuleDict:
    return nn.ModuleDict({
        "ln1": nn.LayerNorm(embed_dim),
        "attn": build_causal_self_attention(embed_dim, num_heads, block_size, dropout),
        "ln2": nn.LayerNorm(embed_dim),
        "mlp": nn.Sequential(
            nn.Linear(embed_dim, 4 * embed_dim),
            nn.GELU(),
            nn.Linear(4 * embed_dim, embed_dim),
            nn.Dropout(dropout),
        ),
    })


def forward_gpt_block(m: nn.ModuleDict, x: Tensor) -> Tensor:
    x = x + forward_causal_self_attention(m["attn"], m["ln1"](x))
    x = x + m["mlp"](m["ln2"](x))
    return x


def build_gpt(
    vocab_size: int, block_size: int, embed_dim: int, num_heads: int, num_layers: int, dropout: float,
) -> nn.ModuleDict:
    m = nn.ModuleDict({
        "token_embedding": nn.Embedding(vocab_size, embed_dim),
        "position_embedding": nn.Embedding(block_size, embed_dim),
        "dropout": nn.Dropout(dropout),
        "blocks": nn.ModuleList(
            [build_gpt_block(embed_dim, num_heads, block_size, dropout) for _ in range(num_layers)]
        ),
        "ln_f": nn.LayerNorm(embed_dim),
        "lm_head": nn.Linear(embed_dim, vocab_size, bias=False),
    })
    m.block_size = block_size
    return m


def forward_gpt(m: nn.ModuleDict, idx: Tensor) -> Tensor:
    B, T = idx.shape
    positions = torch.arange(T, device=idx.device).unsqueeze(0)

    x = m["token_embedding"](idx) + m["position_embedding"](positions)
    x = m["dropout"](x)
    for block in m["blocks"]:
        x = forward_gpt_block(block, x)
    x = m["ln_f"](x)
    return m["lm_head"](x)


@torch.no_grad()
def generate(m: nn.ModuleDict, idx: Tensor, max_new_tokens: int, temperature: float = 1.0) -> Tensor:
    m.eval()
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -m.block_size:]
        logits = forward_gpt(m, idx_cond)[:, -1, :] / temperature
        probs = F.softmax(logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, next_token], dim=1)
    return idx


if __name__ == "__main__":
    m = build_gpt(vocab_size=100, block_size=16, embed_dim=32, num_heads=4, num_layers=2, dropout=0.1)
    idx = torch.randint(0, 100, (2, 8))
    print(forward_gpt(m, idx).shape)  # (2, 8, 100)
    print(generate(m, idx, max_new_tokens=5).shape)  # (2, 13)
