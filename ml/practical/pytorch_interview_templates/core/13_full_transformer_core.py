"""Core: full encoder-decoder Transformer (cross-attention) + greedy generation.

INTERVIEW GUIDE
----------------
Typical ask: "Build a translation model" (or any conditional seq2seq task)
using the full nn.Transformer -- typically the capstone/stretch goal of a
1hr session that already covered attention and one of the encoder/decoder
files, since it requires juggling three distinct masks correctly.

Expected depth (1hr session):
  - Junior/mid: wire nn.Transformer with separate src/tgt embeddings,
    build the causal `tgt_causal_mask` (line 42), and pass
    src_key_padding_mask/tgt_key_padding_mask/memory_key_padding_mask
    (lines 49-50) to the right arguments.
  - Senior: clearly explain what cross-attention does that self-attention
    doesn't (decoder queries attend over encoder memory keys/values),
    justify memory_key_padding_mask = src_pad_mask (line 50, since decoder
    cross-attention reads the encoder's padded output), and reason about
    when full seq2seq beats a decoder-only approach.
  Often the last 15-20 min of the hour; if time is short the interviewer
  may just ask the candidate to *describe* the three masks and their wiring
  rather than have them coded live.

Common follow-ups:
  - "What are the three masks here and what does each one do?"
    (tgt_causal_mask, line 42, blocks the decoder from attending to future
    target tokens; src_key_padding_mask, line 49, stops the encoder's
    self-attention and the decoder's cross-attention from attending to
    source padding; tgt_key_padding_mask, line 49, stops the decoder's
    self-attention from attending to target padding).
  - "Why is memory_key_padding_mask set to src_pad_mask (line 50), not
    tgt_pad_mask?" (cross-attention has the decoder as query and the
    encoder output as memory/key/value, so the mask must describe which
    memory -- i.e. source -- positions are padding, regardless of target
    padding).
  - "What is cross-attention, concretely?" (in each decoder layer, after
    causal self-attention, queries come from the decoder's own
    representations while keys/values come from the encoder's final output
    -- this is how target generation is conditioned on the full source
    sequence).
  - "When would you use this full encoder-decoder architecture instead of
    a decoder-only GPT-style model (file 12)?" (when there's a clear
    separate source/target with a fixed, bidirectionally-encodable input --
    translation, summarization with a distinct document to encode -- vs.
    decoder-only, which suits open-ended generation/completion where
    there's no clean input/output split and everything is one stream).
  - "Why do src and tgt each get their own embedding table (line 27-28)?"
    (different vocabularies in general -- e.g. two languages in
    translation -- so sharing one embedding only makes sense if
    src_vocab_size == tgt_vocab_size and the vocab is actually shared).
  - "Why does generate() re-run forward_full_transformer on the whole src
    every step (line 65)?" (no caching of encoder output or decoder KV --
    the encoder pass is redundant work since src never changes across
    steps; a production implementation would encode src once).

Gotchas to mention proactively:
  - generate() recomputes the full encoder forward pass every single
    decoding step (line 65) even though src is fixed -- worth calling out
    as wasted compute vs. encoding once and reusing memory.
  - tgt_causal_mask is rebuilt fresh each call to forward_full_transformer
    with the current tgt_len (line 41-42), so it correctly grows during
    generate()'s loop -- easy to get wrong if it were built once outside
    the loop with a stale length.
  - Mixing up src_key_padding_mask and tgt_key_padding_mask arguments (both
    are just bool tensors of similar shape) is the single easiest way to
    silently corrupt this model -- worth explicitly double-checking each
    mask against the tensor it's meant to describe (src vs. tgt) rather
    than trusting argument order.
"""

import math

import torch
from torch import nn, Tensor


def build_positional_encoding(embed_dim: int, max_len: int = 5000) -> Tensor:
    pe = torch.zeros(max_len, embed_dim)
    position = torch.arange(0, max_len).unsqueeze(1).float()
    div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-math.log(10000.0) / embed_dim))
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe.unsqueeze(0)


def forward_positional_encoding(pe: Tensor, x: Tensor) -> Tensor:
    return x + pe[:, : x.size(1)]


def build_full_transformer(
    src_vocab_size: int, tgt_vocab_size: int, embed_dim: int, num_heads: int,
    num_encoder_layers: int, num_decoder_layers: int, ff_dim: int, dropout: float, pad_idx: int,
) -> nn.ModuleDict:
    return nn.ModuleDict({
        "src_embedding": nn.Embedding(src_vocab_size, embed_dim, padding_idx=pad_idx),
        "tgt_embedding": nn.Embedding(tgt_vocab_size, embed_dim, padding_idx=pad_idx),
        "transformer": nn.Transformer(
            d_model=embed_dim, nhead=num_heads,
            num_encoder_layers=num_encoder_layers, num_decoder_layers=num_decoder_layers,
            dim_feedforward=ff_dim, dropout=dropout, batch_first=True,
        ),
        "lm_head": nn.Linear(embed_dim, tgt_vocab_size),
    })


def forward_full_transformer(m: nn.ModuleDict, src: Tensor, tgt: Tensor, pe: Tensor, embed_dim: int, pad_idx: int) -> Tensor:
    src_pad_mask = src == pad_idx
    tgt_pad_mask = tgt == pad_idx
    tgt_len = tgt.size(1)
    tgt_causal_mask = nn.Transformer.generate_square_subsequent_mask(tgt_len).to(tgt.device)

    src_embedded = forward_positional_encoding(pe, m["src_embedding"](src) * math.sqrt(embed_dim))
    tgt_embedded = forward_positional_encoding(pe, m["tgt_embedding"](tgt) * math.sqrt(embed_dim))

    output = m["transformer"](
        src_embedded, tgt_embedded, tgt_mask=tgt_causal_mask,
        src_key_padding_mask=src_pad_mask, tgt_key_padding_mask=tgt_pad_mask,
        memory_key_padding_mask=src_pad_mask,
    )
    return m["lm_head"](output)


@torch.no_grad()
def generate(
    m: nn.ModuleDict, src: Tensor, max_len: int, sos_idx: int, eos_idx: int, pe: Tensor, embed_dim: int, pad_idx: int
) -> Tensor:
    m.eval()
    batch_size = src.size(0)
    device = src.device
    generated = torch.full((batch_size, 1), sos_idx, dtype=torch.long, device=device)

    for _ in range(max_len):
        logits = forward_full_transformer(m, src, generated, pe, embed_dim, pad_idx)
        next_token = logits[:, -1, :].argmax(-1, keepdim=True)
        generated = torch.cat([generated, next_token], dim=1)
        if (next_token == eos_idx).all():
            break

    return generated


if __name__ == "__main__":
    embed_dim = 32
    pe = build_positional_encoding(embed_dim)
    m = build_full_transformer(
        src_vocab_size=100, tgt_vocab_size=100, embed_dim=embed_dim, num_heads=4,
        num_encoder_layers=2, num_decoder_layers=2, ff_dim=64, dropout=0.1, pad_idx=0,
    )
    src = torch.randint(1, 100, (2, 8))
    tgt = torch.randint(1, 100, (2, 6))
    print(forward_full_transformer(m, src, tgt, pe, embed_dim, pad_idx=0).shape)  # (2, 6, 100)
