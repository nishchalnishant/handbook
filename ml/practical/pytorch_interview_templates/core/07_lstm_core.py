"""Core: LSTM classifier — embed -> pack -> LSTM -> classify final hidden state.

INTERVIEW GUIDE
----------------
Typical ask: "Extend the RNN classifier to use an LSTM, and support
bidirectional + multi-layer." Usually the main problem in the sequence-modeling
portion of the hour, right after a quick vanilla-RNN warm-up, since the
gating mechanics and the bidirectional hidden-state indexing are meaty enough
to fill 25-30 min alone.

Expected depth (1hr session):
  - Junior/mid: explain what the forget/input/output gates each do, wire
    out_dim = hidden_dim * 2 if bidirectional else hidden_dim correctly into
    the classifier, and know that LSTM returns (hidden, cell) as a tuple
    unlike plain RNN.
  - Senior: explain why the cell state is what actually fixes vanishing
    gradients (the "gradient highway" argument, not just "LSTM has gates"),
    and correctly reason through why hidden[-2]/hidden[-1] are the right
    indices for bidirectional concatenation rather than guessing.
  Commonly the full 25-30 min; frequent follow-up is "now do the same with
  GRU and tell me what you'd give up," pivoting into 08_gru_core.py.

Common follow-ups:
  - "Walk me through what each gate does." (forget gate decides what to
    erase from the cell state; input gate decides what new information to
    write; output gate decides what part of the (updated) cell state is
    exposed as the hidden state at this timestep).
  - "Why does the cell state fix vanishing gradients better than a vanilla
    RNN's hidden state?" (the cell state update is largely additive/gated --
    c_t = f_t * c_{t-1} + i_t * g_t -- rather than repeated matrix
    multiplication through a saturating nonlinearity, so gradients can flow
    through many timesteps largely unattenuated when the forget gate stays
    near 1; this is the "constant error carousel" idea).
  - "Explain hidden[-2] and hidden[-1] in the bidirectional branch." (with
    num_layers layers and bidirectional=True, hidden has shape
    (num_layers*2, B, H) ordered as [layer0_fwd, layer0_bwd, ..., layerN_fwd,
    layerN_bwd]; hidden[-2] is the last layer's forward final state,
    hidden[-1] is the last layer's backward final state, concatenated to
    hidden_dim*2).
  - "Why cat forward and backward hidden states instead of, say, averaging or
    summing them?" (concatenation preserves both directions' information
    without forcing the network to learn a shared subspace; sum/average is
    possible but discards information and is a design choice interviewers
    like to probe).
  - "What's the parameter/compute cost of bidirectional=True vs
    unidirectional?" (roughly doubles LSTM parameters and compute since it
    runs two independent LSTMs, one per direction, plus doubles the
    classifier's input dimension).
  - "Why not use GRU here instead -- what would you lose?" (GRU has fewer
    parameters and no separate cell state, trains faster, and often matches
    LSTM on many tasks, but the extra gate/cell state in LSTM can help on
    longer-range dependencies -- an empirical tradeoff, not a strict
    dominance).

Gotchas to mention proactively:
  - LSTM's forward returns (output, (hidden, cell)) -- easy to unpack
    incorrectly as (output, hidden) like the plain-RNN/GRU code and silently
    treat the tuple (hidden, cell) as the hidden state.
  - The bidirectional flag has to be passed and kept consistent between
    build_model and forward_lstm (both take bidirectional as a separate
    argument rather than being read off the module) -- easy to accidentally
    mismatch if one is refactored without the other.
  - Bidirectional LSTMs require the full sequence up front and can't be used
    in a truly online/streaming setting since the backward pass needs future
    tokens -- worth flagging if the use case is real-time inference.
"""

import torch
from torch import nn, Tensor


def build_model(
    vocab_size: int, embed_dim: int, hidden_dim: int, num_layers: int,
    num_classes: int, pad_idx: int, bidirectional: bool,
) -> nn.ModuleDict:
    out_dim = hidden_dim * 2 if bidirectional else hidden_dim
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "lstm": nn.LSTM(embed_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=bidirectional),
        "classifier": nn.Linear(out_dim, num_classes),
    })


def forward_lstm(m: nn.ModuleDict, x: Tensor, lengths: Tensor, bidirectional: bool) -> Tensor:
    embedded = m["embedding"](x)
    packed = nn.utils.rnn.pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
    _, (hidden, _) = m["lstm"](packed)

    if bidirectional:
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
    else:
        hidden = hidden[-1]

    return m["classifier"](hidden)


if __name__ == "__main__":
    m = build_model(vocab_size=100, embed_dim=16, hidden_dim=32, num_layers=1, num_classes=2, pad_idx=0, bidirectional=True)
    x = torch.randint(1, 100, (4, 10))
    lengths = torch.tensor([10, 8, 5, 3])
    print(forward_lstm(m, x, lengths, bidirectional=True).shape)  # (4, 2)
