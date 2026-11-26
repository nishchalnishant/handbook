"""Core: Bahdanau attention + scaled dot-product attention + multi-head attention.

INTERVIEW GUIDE
----------------
Typical ask: "Implement attention from scratch" -- often phrased as three
escalating parts in one session: additive attention, then scaled
dot-product, then multi-head. This is frequently the main event of a 1hr
interview since it has enough depth to fill the whole hour on its own.

Expected depth (1hr session):
  - Junior/mid: get scaled_dot_product_attention right (matmul, scale by
    sqrt(d), mask, softmax, matmul with value) and wire up
    build_multi_head_attention's four Linear projections correctly.
  - Senior: explain _split_heads/transpose reshaping (line 49-51), justify
    the sqrt(d) scaling with a variance argument, and discuss additive vs.
    dot-product attention cost/expressiveness tradeoffs from real
    experience, not just definitions.
  Expect 35-45 min here if it's the core problem, since each of the three
  functions invites its own line of follow-ups; often followed by "now plug
  this into an encoder" (file 11).

Common follow-ups:
  - "Why divide by sqrt(d) in scaled_dot_product_attention (line 31)?"
    (dot products of d-dim vectors grow with variance ~d; without scaling,
    large-d scores push softmax into a saturated regime with near-one-hot
    outputs and vanishing gradients -- scaling keeps variance ~1).
  - "Bahdanau (additive) vs. dot-product attention -- why did the field move
    to dot-product?" (additive attention concatenates query+key and passes
    through a learned tanh MLP -- line 20's `torch.tanh(m["attn"](cat(...)))`
    -- more expressive per-pair but O(1) matmuls of small dims per pair vs.
    dot-product's single batched matmul, which is far more parallelizable
    on GPU/TPU; that efficiency is why Transformers use dot-product).
  - "Why multi-head instead of one large attention head?" (splitting embed_dim
    into num_heads subspaces, line 49-51, lets each head attend to different
    representation subspaces/positions jointly -- one head can't easily
    represent multiple distinct relations at once).
  - "Walk me through the mask argument." (mask==0 positions get -inf before
    softmax, line 33, so they get ~0 probability -- used for padding and,
    in decoders, causality).
  - "Why does scaled_dot_product_attention divide by sqrt(query.size(-1))
    and not sqrt(embed_dim)?" (it must use head_dim, since scaling should
    match the actual dimensionality of the vectors being dot-producted --
    correct here because heads are split before this call).
  - "What's the parameter/compute cost of multi-head vs single-head
    attention at the same embed_dim?" (same total params/FLOPs as one
    embed_dim-sized head -- heads just reshape, they don't add width).

Gotchas to mention proactively:
  - masked_fill uses float("-inf"); if every position in a row is masked
    (e.g. a fully-padded row) this produces all -inf -> softmax gives NaN,
    worth flagging as an edge case to guard against.
  - _split_heads relies on `.transpose(1, 2)` before a later `.view`, which
    requires `.contiguous()` first (done at line 66 in
    forward_multi_head_attention) -- forgetting that call on a transposed
    tensor throws a runtime error, a classic multi-head-attention bug.
  - forward_bahdanau_attention repeats decoder_hidden across T with
    `.repeat` (line 19) instead of relying on broadcasting -- correct but
    wasteful; worth noting broadcasting would avoid the memory copy.
"""

import math

import torch
from torch import nn, Tensor
import torch.nn.functional as F


def build_bahdanau_attention(hidden_dim: int) -> nn.ModuleDict:
    return nn.ModuleDict({
        "attn": nn.Linear(hidden_dim * 2, hidden_dim),
        "v": nn.Linear(hidden_dim, 1, bias=False),
    })


def forward_bahdanau_attention(m: nn.ModuleDict, decoder_hidden: Tensor, encoder_outputs: Tensor) -> tuple[Tensor, Tensor]:
    T = encoder_outputs.size(1)
    decoder_hidden_rep = decoder_hidden.unsqueeze(1).repeat(1, T, 1)
    energy = torch.tanh(m["attn"](torch.cat([decoder_hidden_rep, encoder_outputs], dim=2)))
    scores = m["v"](energy).squeeze(2)
    attn_weights = F.softmax(scores, dim=1)
    context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs).squeeze(1)
    return context, attn_weights


def scaled_dot_product_attention(
    query: Tensor, key: Tensor, value: Tensor, mask: Tensor | None = None
) -> tuple[Tensor, Tensor]:
    d = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    attn_weights = F.softmax(scores, dim=-1)
    output = torch.matmul(attn_weights, value)
    return output, attn_weights


def build_multi_head_attention(embed_dim: int, num_heads: int) -> nn.ModuleDict:
    assert embed_dim % num_heads == 0
    return nn.ModuleDict({
        "q_proj": nn.Linear(embed_dim, embed_dim),
        "k_proj": nn.Linear(embed_dim, embed_dim),
        "v_proj": nn.Linear(embed_dim, embed_dim),
        "out_proj": nn.Linear(embed_dim, embed_dim),
    })


def _split_heads(x: Tensor, batch_size: int, num_heads: int, head_dim: int) -> Tensor:
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

    attn_output, _ = scaled_dot_product_attention(q, k, v, mask)
    attn_output = attn_output.transpose(1, 2).contiguous().view(B, -1, num_heads * head_dim)
    return m["out_proj"](attn_output)


if __name__ == "__main__":
    B, T, embed_dim, num_heads = 2, 5, 16, 4
    x = torch.randn(B, T, embed_dim)
    mha = build_multi_head_attention(embed_dim, num_heads)
    print(forward_multi_head_attention(mha, x, x, x, num_heads).shape)  # (2, 5, 16)
