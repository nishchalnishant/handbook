"""Core: Transformer encoder classifier — embed + sinusoidal pos-enc -> TransformerEncoder -> mean-pool -> classify.

INTERVIEW GUIDE
----------------
Typical ask: "Build a Transformer-based text classifier" -- often the main
problem, sometimes framed as "BERT-lite," after attention (file 10) has
already been covered or assumed known.

Expected depth (1hr session):
  - Junior/mid: wire nn.TransformerEncoder with src_key_padding_mask (line
    40), apply the embedding scale `* math.sqrt(embed_dim)` (line 38) before
    adding positional encoding, and implement masked mean-pooling correctly
    (lines 42-45).
  - Senior: justify sinusoidal vs. learned positional embeddings, explain
    why this encoder needs no causal mask (bidirectional, unlike file 12),
    and discuss mean-pool vs. CLS-token pooling tradeoffs with awareness of
    what BERT actually does.
  Typically 20-30 min; often paired with a quick "now make it causal" pivot
  into file 12 territory to test whether the candidate understands masking
  is the only real difference between the two.

Common follow-ups:
  - "Why do we need positional encoding at all?" (self-attention is
    permutation-invariant -- scores only depend on content, not position --
    so without positional info "dog bites man" and "man bites dog" produce
    identical attention patterns).
  - "Sinusoidal vs. learned positional embeddings?" (sinusoidal, used here
    via build_positional_encoding, generalizes to sequence lengths beyond
    max_len seen in training and needs no extra parameters; learned
    embeddings can fit training-distribution positions better but can't
    extrapolate past max_len without interpolation tricks).
  - "Why multiply the embedding by sqrt(embed_dim) before adding positional
    encoding (line 38)?" (keeps embedding and positional-encoding
    magnitudes comparable -- embeddings are typically initialized with
    smaller variance than the fixed sinusoidal PE values, so without
    scaling PE can dominate).
  - "Why mean-pool instead of using a CLS token like BERT?" (CLS needs an
    extra learned token position and relies on attention learning to
    aggregate into it; mean-pooling over real tokens, masked correctly
    (line 42, `(~pad_mask).unsqueeze(-1)`), is simpler and works well for
    smaller models/datasets without that extra capacity).
  - "Why is there no attention mask other than the padding mask?" (encoder
    self-attention is meant to be bidirectional for classification -- every
    token should see every other token, so no causal mask is applied,
    unlike the decoder in file 12).
  - "What happens if you forget src_key_padding_mask?" (pad tokens leak into
    attention and into the mean-pool average, corrupting the pooled
    representation, especially for short sequences with heavy padding).

Gotchas to mention proactively:
  - The mean-pool denominator uses `mask.sum(dim=1).clamp(min=1e-6)` (line
    44) -- without the clamp, an all-padding row divides by zero; worth
    flagging even though it's guarded here.
  - pad_mask here is `True` at pad positions consistent with PyTorch's
    `src_key_padding_mask` convention (True = ignore) -- easy to get
    backwards versus a boolean "valid token" mask, which would silently
    invert attention and pooling.
  - build_positional_encoding is precomputed once up to max_len and sliced
    per-batch (line 19, `pe[:, : x.size(1)]`) -- sequences longer than
    max_len will index out of range, so max_len must be sized for the
    longest expected input.
"""

import math

import torch
from torch import nn, Tensor


def build_positional_encoding(embed_dim: int, max_len: int) -> Tensor:
    pe = torch.zeros(max_len, embed_dim)
    position = torch.arange(0, max_len).unsqueeze(1).float()
    div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-math.log(10000.0) / embed_dim))
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe.unsqueeze(0)


def forward_positional_encoding(pe: Tensor, x: Tensor) -> Tensor:
    return x + pe[:, : x.size(1)]


def build_transformer_encoder_classifier(
    vocab_size: int, embed_dim: int, num_heads: int, num_layers: int,
    ff_dim: int, num_classes: int, max_len: int, dropout: float, pad_idx: int,
) -> nn.ModuleDict:
    encoder_layer = nn.TransformerEncoderLayer(
        d_model=embed_dim, nhead=num_heads, dim_feedforward=ff_dim,
        dropout=dropout, batch_first=True, activation="gelu",
    )
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "encoder": nn.TransformerEncoder(encoder_layer, num_layers=num_layers),
        "classifier": nn.Linear(embed_dim, num_classes),
    })


def forward_transformer_encoder_classifier(m: nn.ModuleDict, x: Tensor, pad_mask: Tensor, pe: Tensor, embed_dim: int) -> Tensor:
    embedded = m["embedding"](x) * math.sqrt(embed_dim)
    embedded = forward_positional_encoding(pe, embedded)
    encoded = m["encoder"](embedded, src_key_padding_mask=pad_mask)

    mask = (~pad_mask).unsqueeze(-1).float()
    summed = (encoded * mask).sum(dim=1)
    counts = mask.sum(dim=1).clamp(min=1e-6)
    pooled = summed / counts

    return m["classifier"](pooled)


if __name__ == "__main__":
    embed_dim = 32
    pe = build_positional_encoding(embed_dim, max_len=50)
    m = build_transformer_encoder_classifier(
        vocab_size=100, embed_dim=embed_dim, num_heads=4, num_layers=2,
        ff_dim=64, num_classes=2, max_len=50, dropout=0.1, pad_idx=0,
    )
    x = torch.randint(1, 100, (4, 10))
    pad_mask = torch.zeros(4, 10, dtype=torch.bool)
    print(forward_transformer_encoder_classifier(m, x, pad_mask, pe, embed_dim).shape)  # (4, 2)
