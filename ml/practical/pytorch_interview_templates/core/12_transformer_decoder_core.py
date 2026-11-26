"""Core: decoder-only Transformer LM — causal self-attention + greedy generation.

INTERVIEW GUIDE
----------------
Typical ask: "Build a GPT-style language model" -- usually posed right after
file 11's encoder classifier, explicitly to test whether the candidate
understands that causal masking is the entire difference. Main problem,
20-30 min.

Expected depth (1hr session):
  - Junior/mid: build the causal mask with
    `nn.Transformer.generate_square_subsequent_mask(T)` (line 41), pass it
    as `mask=` with `is_causal=True` into nn.TransformerEncoder, and
    implement the autoregressive generate loop with KV growing each step.
  - Senior: explain why this reuses nn.TransformerEncoderLayer (not
    TransformerDecoderLayer, which expects cross-attention/memory) and can
    discuss the O(T^2) or worse cost of the generate loop's lack of KV
    caching, plus how real GPT inference avoids recomputation.
  Fast-moving 15-25 min if file 11 was already covered, since most of the
  architecture is a copy-paste with one masking change -- the interviewer
  is really testing whether the candidate treats that as understood or
  re-derives it from scratch.

Common follow-ups:
  - "Why is this nn.TransformerEncoderLayer and not TransformerDecoderLayer?"
    (TransformerDecoderLayer in PyTorch assumes cross-attention over an
    encoder memory; a decoder-only LM has no encoder, so a causally-masked
    TransformerEncoderLayer is architecturally what GPT actually is).
  - "Walk through generate_square_subsequent_mask." (produces a TxT matrix
    that is 0 on/below the diagonal and -inf above it, so position i's
    attention scores to positions >i are masked before softmax --
    guarantees no information leaks from future tokens).
  - "Why pass both `mask=causal_mask` and `is_causal=True` (line 42)?"
    (is_causal is a hint PyTorch uses to pick a fused/optimized attention
    kernel; the explicit mask is still the source of truth -- redundant but
    harmless, and worth knowing it's not strictly required if is_causal is
    set with a standard causal pattern).
  - "This `generate` function recomputes the full forward pass every step
    (line 51-53) -- what's wrong with that at scale?" (no KV caching -- each
    new token reprocesses the entire growing context from scratch, making
    generation O(n^2) in total work instead of O(n) with cached keys/values).
  - "Why `generated[:, -seq_len:]` (line 51) instead of the full sequence?"
    (positional encoding and the model were only built/trained up to
    max_len; truncating to the last seq_len tokens acts as a sliding
    context window so indexing into `pe` never overflows).
  - "How would you add top-k/nucleus sampling instead of greedy argmax?"
    (replace `logits[:, -1, :].argmax(-1)` with sampling from a
    temperature/top-k/top-p-filtered distribution).

Gotchas to mention proactively:
  - generate() has no EOS early-stopping (unlike file 09/13's generate
    loops) -- it always runs max_new_tokens, worth flagging as an
    intentional simplification vs. an oversight.
  - No KV cache means generate() cost grows quadratically with sequence
    length purely from redundant recomputation, not from attention itself.
  - Padding tokens are embedded with padding_idx=pad_idx but no
    src_key_padding_mask is ever passed into forward_transformer_decoder_lm
    -- fine for single unpadded sequences at inference, but batched
    training with padded sequences would need one added, unlike file 11.
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


def build_transformer_decoder_lm(
    vocab_size: int, embed_dim: int, num_heads: int, num_layers: int,
    ff_dim: int, max_len: int, dropout: float, pad_idx: int,
) -> nn.ModuleDict:
    layer = nn.TransformerEncoderLayer(
        d_model=embed_dim, nhead=num_heads, dim_feedforward=ff_dim,
        dropout=dropout, batch_first=True, activation="gelu",
    )
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "decoder": nn.TransformerEncoder(layer, num_layers=num_layers),
        "lm_head": nn.Linear(embed_dim, vocab_size),
    })


def forward_transformer_decoder_lm(m: nn.ModuleDict, x: Tensor, pe: Tensor, embed_dim: int) -> Tensor:
    T = x.size(1)
    embedded = m["embedding"](x) * math.sqrt(embed_dim)
    embedded = forward_positional_encoding(pe, embedded)
    causal_mask = nn.Transformer.generate_square_subsequent_mask(T).to(x.device)
    decoded = m["decoder"](embedded, mask=causal_mask, is_causal=True)
    return m["lm_head"](decoded)


@torch.no_grad()
def generate(m: nn.ModuleDict, prompt: Tensor, max_new_tokens: int, seq_len: int, pe: Tensor, embed_dim: int) -> Tensor:
    m.eval()
    generated = prompt
    for _ in range(max_new_tokens):
        context = generated[:, -seq_len:]
        logits = forward_transformer_decoder_lm(m, context, pe, embed_dim)
        next_token = logits[:, -1, :].argmax(-1, keepdim=True)
        generated = torch.cat([generated, next_token], dim=1)
    return generated


if __name__ == "__main__":
    embed_dim = 32
    pe = build_positional_encoding(embed_dim, max_len=50)
    m = build_transformer_decoder_lm(
        vocab_size=100, embed_dim=embed_dim, num_heads=4, num_layers=2,
        ff_dim=64, max_len=50, dropout=0.1, pad_idx=0,
    )
    x = torch.randint(1, 100, (2, 10))
    print(forward_transformer_decoder_lm(m, x, pe, embed_dim).shape)  # (2, 10, 100)
    print(generate(m, x, max_new_tokens=5, seq_len=50, pe=pe, embed_dim=embed_dim).shape)  # (2, 15)
