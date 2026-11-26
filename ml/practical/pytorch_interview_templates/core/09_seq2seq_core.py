"""Core: GRU seq2seq with teacher forcing + greedy generation.

INTERVIEW GUIDE
----------------
Typical ask: "Build an encoder-decoder for a translation/summarization toy
task." Usually the main problem of the session (25-35 min) after a warm-up,
since it forces a discussion of training-time vs. inference-time generation.

Expected depth (1hr session):
  - Junior/mid: implement forward_encoder passing final hidden state into
    forward_decoder, get teacher_forcing_ratio into forward_seq2seq
    (line 53: `random.random() < teacher_forcing_ratio`), and write the
    greedy generate_seq2seq loop with EOS early-stopping.
  - Senior: explain exposure bias caused by teacher forcing, propose fixes
    (scheduled sampling, ratio annealing), and reason about why a single
    fixed-size hidden vector (line 47/66, `hidden = forward_encoder(...)`)
    caps quality on long sequences.
  This one naturally bleeds into attention (file 10) as the follow-up --
  expect "now fix the bottleneck you just described."

Common follow-ups:
  - "What is teacher forcing and why use it?" (feeds ground-truth tgt token
    instead of the model's own prediction so gradients don't compound early
    errors; speeds up/stabilizes training).
  - "What's the downside of teacher forcing?" (exposure bias -- at inference
    the model only ever sees its own possibly-wrong tokens, a distribution
    it never trained on).
  - "Why does the decoder only get the encoder's *final* hidden state?"
    (fixed-length bottleneck -- all source information must be compressed
    into one vector, which degrades on long inputs; motivates attention).
  - "Greedy decoding vs. beam search?" (greedy takes argmax each step, cheap
    but can lock in a suboptimal path; beam search keeps top-k hypotheses
    and can produce higher-likelihood full sequences at higher cost).
  - "Why anneal teacher_forcing_ratio over training?" (start high for stable
    early learning, decay toward 0 so the model adapts to consuming its own
    predictions before eval time).
  - "How would you batch variable-length sequences here?" (pad + pack, or
    at minimum mask pad_idx in the loss).

Gotchas to mention proactively:
  - generate_seq2seq's `(next_token == eos_idx).all()` break only works
    cleanly for a whole batch reaching EOS simultaneously; per-sequence
    early stopping needs a finished-mask instead.
  - forward_seq2seq preallocates `outputs` for the full tgt_len and always
    runs that many steps even under teacher forcing, so it doesn't natively
    support early-stopping during training.
"""

import random

import torch
from torch import nn, Tensor


def build_encoder(vocab_size: int, embed_dim: int, hidden_dim: int, pad_idx: int) -> nn.ModuleDict:
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "gru": nn.GRU(embed_dim, hidden_dim, batch_first=True),
    })


def forward_encoder(m: nn.ModuleDict, src: Tensor) -> Tensor:
    embedded = m["embedding"](src)
    _, hidden = m["gru"](embedded)
    return hidden


def build_decoder(vocab_size: int, embed_dim: int, hidden_dim: int, pad_idx: int) -> nn.ModuleDict:
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "gru": nn.GRU(embed_dim, hidden_dim, batch_first=True),
        "out": nn.Linear(hidden_dim, vocab_size),
    })


def forward_decoder(m: nn.ModuleDict, input_token: Tensor, hidden: Tensor) -> tuple[Tensor, Tensor]:
    embedded = m["embedding"](input_token)
    output, hidden = m["gru"](embedded, hidden)
    logits = m["out"](output.squeeze(1))
    return logits, hidden


def build_seq2seq(encoder: nn.ModuleDict, decoder: nn.ModuleDict) -> nn.ModuleDict:
    return nn.ModuleDict({"encoder": encoder, "decoder": decoder})


def forward_seq2seq(m: nn.ModuleDict, src: Tensor, tgt: Tensor, teacher_forcing_ratio: float, sos_idx: int) -> Tensor:
    batch_size, tgt_len = tgt.shape
    vocab_size = m["decoder"]["out"].out_features
    device = src.device

    outputs = torch.zeros(batch_size, tgt_len, vocab_size, device=device)
    hidden = forward_encoder(m["encoder"], src)
    input_token = torch.full((batch_size, 1), sos_idx, dtype=torch.long, device=device)

    for t in range(tgt_len):
        logits, hidden = forward_decoder(m["decoder"], input_token, hidden)
        outputs[:, t] = logits
        if random.random() < teacher_forcing_ratio:
            input_token = tgt[:, t : t + 1]
        else:
            input_token = logits.argmax(1, keepdim=True)

    return outputs


@torch.no_grad()
def generate_seq2seq(m: nn.ModuleDict, src: Tensor, max_len: int, eos_idx: int, sos_idx: int) -> Tensor:
    m.eval()
    batch_size = src.size(0)
    device = src.device
    hidden = forward_encoder(m["encoder"], src)
    input_token = torch.full((batch_size, 1), sos_idx, dtype=torch.long, device=device)
    generated = []

    for _ in range(max_len):
        logits, hidden = forward_decoder(m["decoder"], input_token, hidden)
        next_token = logits.argmax(1, keepdim=True)
        generated.append(next_token)
        input_token = next_token
        if (next_token == eos_idx).all():
            break

    return torch.cat(generated, dim=1)


if __name__ == "__main__":
    enc = build_encoder(vocab_size=50, embed_dim=16, hidden_dim=32, pad_idx=0)
    dec = build_decoder(vocab_size=50, embed_dim=16, hidden_dim=32, pad_idx=0)
    m = build_seq2seq(enc, dec)
    src = torch.randint(1, 50, (4, 8))
    tgt = torch.randint(1, 50, (4, 6))
    print(forward_seq2seq(m, src, tgt, teacher_forcing_ratio=0.5, sos_idx=1).shape)  # (4, 6, 50)
