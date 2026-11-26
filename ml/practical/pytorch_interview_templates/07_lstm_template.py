"""
============================================================
TEMPLATE 7: LSTM
============================================================
Text/sequence classification using LSTM. Same structure as the RNN
template — only the recurrent cell changes. Interview-scoped.
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
CKPT_PATH = "checkpoints/lstm_best.pt"


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
    """Embedding -> LSTM -> classify from final hidden state.

    Why LSTM over vanilla RNN: gating mechanism (input/forget/output gates)
    controls what information to keep/discard/output at each step, via an
    additive cell-state update path. This additive path lets gradients flow
    over long sequences without vanishing (unlike the repeated matrix
    multiplication in vanilla RNN).

    Shape trace (B, T, E=embed_dim, H=hidden_dim, bidirectional):
        input ids:      (B, T)
        embedded:       (B, T, E)
        LSTM output:    (B, T, H*2) if bidirectional else (B, T, H)
        final hidden:   (num_layers*2, B, H) if bidirectional
        concat h_fwd,h_bwd from last layer -> (B, H*2)
        logits:         (B, num_classes)
    """
    out_dim = hidden_dim * 2 if bidirectional else hidden_dim
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "lstm": nn.LSTM(
            embed_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=bidirectional
        ),
        "classifier": nn.Linear(out_dim, num_classes),
    })


def forward_lstm(m: nn.ModuleDict, x: Tensor, lengths: Tensor, bidirectional: bool) -> Tensor:
    embedded = m["embedding"](x)
    packed = nn.utils.rnn.pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
    _, (hidden, _) = m["lstm"](packed)  # hidden: (num_layers*num_directions, B, H)

    if bidirectional:
        # Concatenate the last layer's forward and backward hidden states.
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)  # (B, H*2)
    else:
        hidden = hidden[-1]  # (B, H)

    return m["classifier"](hidden)


def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for xb, lengths, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        loss = criterion(forward_lstm(model, xb, lengths, BIDIRECTIONAL), yb)
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
        logits = forward_lstm(model, xb, lengths, BIDIRECTIONAL)
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
# When to use: sequence tasks needing longer-range memory than vanilla RNN
#   can provide (sentiment on long documents, moderate-length time series).
# Advantages: gating mitigates vanishing gradients; captures longer-range
#   dependencies than vanilla RNN.
# Disadvantages: 4x the parameters of vanilla RNN per layer (input/forget/
#   output gates + cell candidate); still sequential (no parallel time steps);
#   largely superseded by Transformers for long sequences.
# Complexity: O(T * H^2) same asymptotic as RNN but larger constant (4 gates).
# Follow-ups to expect:
#   - Walk through the LSTM gate equations (forget/input/output gates, cell
#     state update, hidden state output).
#   - Why does the cell state help gradient flow? (additive updates, not
#     multiplicative, so gradient isn't repeatedly shrunk.)
#   - LSTM vs GRU tradeoffs (Template 8) — GRU has fewer params, similar
#     performance in many tasks.
#   - Why concatenate forward/backward hidden states for bidirectional?
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Binary/Multi-label/Regression: same head-swap pattern as RNN template.
# Sequence labeling (NER, POS tagging): use LSTM output at every timestep,
#   not just final hidden state; often paired with a CRF layer on top.
# Stacked LSTM: num_layers > 1 for more capacity (with dropout between layers).
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: sequence tasks with moderate-length dependencies, common
#   production baseline before Transformers for smaller-scale problems.
# Pros: handles longer dependencies than vanilla RNN, well-understood, stable.
# Cons: more params than GRU, sequential compute, superseded by
#   Transformers on large-scale tasks.
# Time complexity: O(T * H^2) with larger constant than RNN (4 gate matmuls).
# Space complexity: O(4 * H^2) params per layer.
# Common mistakes: forgetting to clip gradients; not concatenating both
#   directions correctly in bidirectional case; ignoring pack_padded_sequence
#   causing padding to skew hidden states.
# Production checklist: gradient clipping, persist vocab/tokenizer, monitor
#   sequence length distribution drift, consider quantization for latency-
#   sensitive deployments.
# ============================================================
