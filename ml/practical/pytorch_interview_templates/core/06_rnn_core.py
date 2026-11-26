"""Core: vanilla RNN classifier — embed -> pack -> RNN -> classify final hidden state.

INTERVIEW GUIDE
----------------
Typical ask: "Build a sequence classifier (e.g. sentiment) using an RNN over
variable-length text." Often the opener for the sequence-modeling portion of
an interview, immediately followed by "now do it with an LSTM/GRU" as the
main problem.

Expected depth (1hr session):
  - Junior/mid: wire embedding -> RNN -> classifier correctly, explain why
    lengths.cpu() is needed for pack_padded_sequence, and correctly squeeze
    the single-layer hidden state before the classifier.
  - Senior: explain vanishing gradients through tanh recurrence concretely
    (why gradients shrink multiplicatively over long sequences), and argue
    for when a plain RNN is still a defensible choice vs. reaching for
    LSTM/GRU by default.
  Usually 10-15 min on its own since it's a stepping stone; the real depth
  gets probed once the conversation moves to 07_lstm_core.py or
  08_gru_core.py and the interviewer asks "what's actually different here."

Common follow-ups:
  - "Why pack_padded_sequence at all -- what breaks without it?" (without
    packing, the RNN processes pad tokens as real input, contaminating the
    hidden state with meaningless embedding_padding_idx vectors and making
    the final hidden state depend on how much padding was appended rather
    than only on real tokens).
  - "Why lengths.cpu() specifically?" (pack_padded_sequence requires lengths
    on CPU even if x/the model are on GPU -- a common runtime error if
    lengths is left on the same device as the input tensor).
  - "Why does the code work with enforce_sorted=False?" (lets you pass
    lengths in arbitrary order instead of pre-sorting the batch by
    descending length, at a small performance cost from internal
    sorting/unsorting).
  - "What causes vanishing gradients in a vanilla RNN and why doesn't this
    architecture fix it?" (repeated multiplication by the same recurrent
    weight matrix and tanh derivative <= 1 at every timestep shrinks
    gradients exponentially over long sequences -- nothing in this code
    (single nn.RNN layer, no gating) addresses that).
  - "When would you still choose a plain RNN over LSTM/GRU?" (short sequences,
    latency/parameter-constrained settings, or as a fast baseline before
    justifying the added complexity of gates).
  - "Why index hidden.squeeze(0) instead of hidden[-1]?" (with a single-layer,
    unidirectional RNN, hidden has shape (1, B, H), so squeeze(0) and
    hidden[-1] are equivalent here, but hidden[-1] generalizes if num_layers
    changes and squeeze(0) doesn't).

Gotchas to mention proactively:
  - hidden.squeeze(0) silently assumes num_layers=1 and unidirectional --
    this code has no num_layers or bidirectional parameter, so it will break
    (wrong shape into classifier) the moment someone tries to extend
    build_model without also fixing this line, unlike 07/08 which index
    hidden[-1]/concatenate explicitly.
  - nn.RNN's default nonlinearity is tanh (kept explicit here), but tanh
    saturates and is the direct cause of vanishing gradients -- worth
    connecting explicitly rather than treating it as an arbitrary default.
  - padding_idx=pad_idx on the embedding zeroes that row's gradient but
    doesn't prevent the RNN itself from processing pad timesteps if you skip
    pack_padded_sequence -- padding_idx alone is not a substitute for packing.
"""

from torch import nn, Tensor


def build_model(vocab_size: int, embed_dim: int, hidden_dim: int, num_classes: int, pad_idx: int) -> nn.ModuleDict:
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "rnn": nn.RNN(embed_dim, hidden_dim, batch_first=True, nonlinearity="tanh"),
        "classifier": nn.Linear(hidden_dim, num_classes),
    })


def forward_rnn(m: nn.ModuleDict, x: Tensor, lengths: Tensor) -> Tensor:
    embedded = m["embedding"](x)
    packed = nn.utils.rnn.pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
    _, hidden = m["rnn"](packed)
    hidden = hidden.squeeze(0)
    return m["classifier"](hidden)


if __name__ == "__main__":
    import torch
    m = build_model(vocab_size=100, embed_dim=16, hidden_dim=32, num_classes=2, pad_idx=0)
    x = torch.randint(1, 100, (4, 10))
    lengths = torch.tensor([10, 8, 5, 3])
    print(forward_rnn(m, x, lengths).shape)  # (4, 2)
