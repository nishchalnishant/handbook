"""
============================================================
TEMPLATE 8: GRU
============================================================
Text/sequence classification using GRU. Same structure as
RNN/LSTM templates — only the recurrent cell changes.
============================================================
"""

import random

import numpy as np
import torch
from torch import nn, Tensor
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader, random_split


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
SEED = 42
VOCAB_SIZE = 5000
EMBED_DIM = 128
HIDDEN_DIM = 128
NUM_LAYERS = 1
NUM_CLASSES = 2
BIDIRECTIONAL = True
BATCH_SIZE = 32
EPOCHS = 10
LR = 1e-3
PAD_IDX = 0
CKPT_PATH = "checkpoints/gru_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


class SequenceDataset(Dataset):
    def __init__(self, sequences: list[list[int]], labels: list[int]) -> None:
        self.sequences = sequences
        self.labels = labels

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, idx: int) -> tuple[Tensor, int]:
        return torch.tensor(self.sequences[idx], dtype=torch.long), self.labels[idx]


def collate_fn(batch: list[tuple[Tensor, int]], pad_idx: int) -> tuple[Tensor, Tensor, Tensor]:
    sequences, labels = zip(*batch)
    lengths = torch.tensor([len(s) for s in sequences], dtype=torch.long)
    padded = pad_sequence(sequences, batch_first=True, padding_value=pad_idx)
    return padded, lengths, torch.tensor(labels, dtype=torch.long)


def build_model(
    vocab_size: int,
    embed_dim: int,
    hidden_dim: int,
    num_layers: int,
    num_classes: int,
    pad_idx: int,
    bidirectional: bool,
) -> nn.ModuleDict:
    """Embedding -> GRU -> classify from final hidden state.

    Why GRU over LSTM: merges LSTM's forget+input gates into a single
    "update gate" and drops the separate cell state, using only the
    hidden state. ~25% fewer parameters than LSTM, trains faster, often
    matches LSTM performance on small-to-medium datasets.

    Shape trace: identical to LSTM template, but no separate cell state
    (only hidden state is tracked/returned).
    """
    out_dim = hidden_dim * 2 if bidirectional else hidden_dim
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "gru": nn.GRU(
            embed_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=bidirectional
        ),
        "classifier": nn.Linear(out_dim, num_classes),
    })


def forward_gru(m: nn.ModuleDict, x: Tensor, lengths: Tensor, bidirectional: bool) -> Tensor:
    embedded = m["embedding"](x)
    packed = nn.utils.rnn.pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
    _, hidden = m["gru"](packed)  # hidden: (num_layers*num_directions, B, H)

    if bidirectional:
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
    else:
        hidden = hidden[-1]

    return m["classifier"](hidden)


def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for xb, lengths, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        loss = criterion(forward_gru(model, xb, lengths, BIDIRECTIONAL), yb)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device) -> tuple[float, float]:
    model.eval()
    total_loss, correct = 0.0, 0
    for xb, lengths, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = forward_gru(model, xb, lengths, BIDIRECTIONAL)
        total_loss += criterion(logits, yb).item() * xb.size(0)
        correct += (logits.argmax(1) == yb).sum().item()
    n = len(loader.dataset)
    return total_loss / n, correct / n


def main() -> None:
    set_seed(SEED)
    device = get_device()

    rng = np.random.default_rng(SEED)
    sequences = [rng.integers(1, VOCAB_SIZE, size=rng.integers(5, 30)).tolist() for _ in range(1000)]
    labels = rng.integers(0, NUM_CLASSES, size=1000).tolist()

    full_ds = SequenceDataset(sequences, labels)
    n = len(full_ds)
    n_train = int(0.8 * n)
    train_ds, val_ds = random_split(full_ds, [n_train, n - n_train])

    collate = lambda batch: collate_fn(batch, PAD_IDX)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate)

    model = build_model(
        VOCAB_SIZE, EMBED_DIM, HIDDEN_DIM, NUM_LAYERS, NUM_CLASSES, PAD_IDX, BIDIRECTIONAL
    ).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    best_acc = 0.0

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        print(f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), CKPT_PATH)

    model.load_state_dict(torch.load(CKPT_PATH, map_location=device))


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: same regime as LSTM but want fewer parameters / faster
#   training with comparable performance — good default recurrent choice
#   for small-to-medium datasets.
# Advantages: fewer params than LSTM (2 gates vs 3 + cell state), faster
#   to train, often comparable accuracy.
# Disadvantages: still sequential (no time-step parallelism); on very
#   long sequences or very large datasets, LSTM or Transformers may edge
#   out GRU.
# Complexity: O(T * H^2), smaller constant than LSTM (~3x vs ~4x gate matmuls).
# Follow-ups to expect:
#   - Walk through GRU gate equations (reset gate, update gate, candidate
#     hidden state).
#   - GRU vs LSTM: when would you pick one over the other? (GRU: faster,
#     fewer params, good default; LSTM: sometimes better on very long
#     sequences due to explicit cell state.)
#   - Why is there no separate cell state in GRU?
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Same as LSTM template: binary/multi-label/regression via head + loss
#   swap; sequence labeling via per-timestep outputs.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: default recurrent baseline balancing speed and performance.
# Pros: fewer parameters than LSTM, faster training, comparable accuracy
#   in many tasks.
# Cons: sequential compute, can underperform LSTM on very long sequences,
#   superseded by Transformers at scale.
# Time complexity: O(T * H^2).
# Space complexity: O(3 * H^2) params per layer (vs 4x for LSTM).
# Common mistakes: same as LSTM — forgetting gradient clipping,
#   mishandling bidirectional hidden state concatenation.
# Production checklist: same as LSTM — gradient clipping, persisted
#   vocab, sequence-length drift monitoring, latency benchmarking vs LSTM
#   if considering the swap for production speed.
# ============================================================
