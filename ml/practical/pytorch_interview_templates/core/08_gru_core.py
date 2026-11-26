"""Core: GRU classifier — embed -> pack -> GRU -> classify final hidden state.

INTERVIEW GUIDE
----------------
Typical ask: "Now implement the same classifier with a GRU instead of an
LSTM, and explain why you'd choose one over the other." Almost always a
follow-up/comparison question after 07_lstm_core.py rather than a cold open,
used as the stretch goal in the last 10-15 min of the sequence-modeling
portion.

Expected depth (1hr session):
  - Junior/mid: notice the code is structurally identical to the LSTM version
    except GRU returns a single hidden state (no cell state) from
    m["gru"](packed), and get the bidirectional hidden[-2]/hidden[-1]
    concatenation right by pattern-matching from the LSTM version.
  - Senior: articulate the update/reset gate mechanics, quantify why GRU has
    fewer parameters than LSTM (no separate output gate, no cell state), and
    give a real recommendation for when to prefer GRU over LSTM rather than
    "they're basically the same."
  Quick if LSTM was just covered (10-15 min) since most of the code is
  identical; the interview value is almost entirely in the "why/when" of the
  GRU vs LSTM tradeoff discussion.

Common follow-ups:
  - "What's the key structural difference vs LSTM in this code?" (`_, hidden
    = m["gru"](packed)` returns just hidden, no cell state tuple -- GRU
    folds the cell/hidden state distinction into a single hidden state using
    an update gate instead of separate forget/input gates).
  - "Explain the update gate and reset gate." (update gate controls how much
    of the previous hidden state to keep vs. replace with the new candidate
    state -- doing the job of LSTM's forget+input gates combined; reset gate
    controls how much of the previous hidden state feeds into computing the
    new candidate state).
  - "Why does GRU have fewer parameters than LSTM?" (3 gates times weight
    matrices vs. LSTM's forget/input/output/cell-candidate needing effectively
    4 sets of gate weights, and no separate cell state to maintain --
    roughly 3/4 the parameters for the same hidden_dim).
  - "When would you prefer GRU over LSTM in practice?" (smaller datasets
    where LSTM's extra parameters risk overfitting, latency-sensitive
    settings, or shorter sequences where LSTM's extra cell-state machinery
    doesn't pay for itself; LSTM is still the safer default on tasks with
    very long-range dependencies given the dedicated cell-state highway).
  - "Is the bidirectional concatenation logic here any different from the
    LSTM version?" (no -- hidden[-2]/hidden[-1] indexing and the
    out_dim = hidden_dim * 2 if bidirectional logic in build_model are
    identical in structure to 07_lstm_core.py, since both GRU and LSTM
    return hidden with shape (num_layers * num_directions, B, H)).
  - "Would you expect GRU to train faster than LSTM here?" (yes, modestly --
    fewer parameters and no cell-state bookkeeping means less compute per
    timestep, though the difference is often small relative to embedding
    size and sequence length in practice).

Gotchas to mention proactively:
  - Unlike LSTM, GRU's forward returns a single hidden tensor, not a tuple --
    porting code from 07_lstm_core.py by copy-paste and forgetting to drop
    the `, _` cell-state unpacking is the most common transcription bug here.
  - hidden[-2]/hidden[-1] bidirectional indexing assumes the same
    (num_layers*num_directions, B, H) layout as LSTM -- correct here, but
    worth stating explicitly rather than assuming it transfers by analogy
    without checking GRU's docs.
  - bidirectional is passed independently to both build_model and
    forward_gru, same as the LSTM file -- if only one call site is updated
    when experimenting, shapes mismatch at the classifier.
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
        "gru": nn.GRU(embed_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=bidirectional),
        "classifier": nn.Linear(out_dim, num_classes),
    })


def forward_gru(m: nn.ModuleDict, x: Tensor, lengths: Tensor, bidirectional: bool) -> Tensor:
    embedded = m["embedding"](x)
    packed = nn.utils.rnn.pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
    _, hidden = m["gru"](packed)

    if bidirectional:
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
    else:
        hidden = hidden[-1]

    return m["classifier"](hidden)


if __name__ == "__main__":
    m = build_model(vocab_size=100, embed_dim=16, hidden_dim=32, num_layers=1, num_classes=2, pad_idx=0, bidirectional=True)
    x = torch.randint(1, 100, (4, 10))
    lengths = torch.tensor([10, 8, 5, 3])
    print(forward_gru(m, x, lengths, bidirectional=True).shape)  # (4, 2)
