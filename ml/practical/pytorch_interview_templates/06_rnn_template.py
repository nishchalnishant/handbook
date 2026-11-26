"""
============================================================
TEMPLATE 6: Recurrent Neural Network (RNN)
============================================================
Text/sequence classification using a vanilla RNN. Interview-scoped:
core workflow, minimal extras.
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
NUM_CLASSES = 2
BATCH_SIZE = 32
EPOCHS = 10
LR = 1e-3
PAD_IDX = 0
CKPT_PATH = "checkpoints/rnn_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------
# Dataset: variable-length token sequences
# ------------------------------------------------------------
class SequenceDataset(Dataset):
    """Each item is a list of token ids (already tokenized/encoded).
    Replace with a real tokenizer (e.g. torchtext, HF tokenizer, or a
    simple word->id vocab) upstream of this class."""

    def __init__(self, sequences: list[list[int]], labels: list[int]) -> None:
        self.sequences = sequences
        self.labels = labels

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, idx: int) -> tuple[Tensor, int]:
        return torch.tensor(self.sequences[idx], dtype=torch.long), self.labels[idx]


def collate_fn(batch: list[tuple[Tensor, int]], pad_idx: int) -> tuple[Tensor, Tensor, Tensor]:
    """Pads variable-length sequences in a batch to the same length so
    they can be stacked into a single tensor. Also returns true lengths
    for use with pack_padded_sequence (avoids wasting compute on padding)."""
    sequences, labels = zip(*batch)
    lengths = torch.tensor([len(s) for s in sequences], dtype=torch.long)
    padded = pad_sequence(sequences, batch_first=True, padding_value=pad_idx)
    return padded, lengths, torch.tensor(labels, dtype=torch.long)


# ------------------------------------------------------------
# Model (nn.ModuleDict of built-ins + a plain forward function — no custom class)
# ------------------------------------------------------------
def build_model(vocab_size: int, embed_dim: int, hidden_dim: int, num_classes: int, pad_idx: int) -> nn.ModuleDict:
    """Embedding -> RNN -> classify from final hidden state.

    Shape trace (batch B, seq_len T, embed_dim E, hidden H):
        input ids:        (B, T)
        after embedding:  (B, T, E)
        RNN output:       (B, T, H)   [per-timestep hidden states]
        final hidden:     (1, B, H)   -> squeeze to (B, H)
        logits:           (B, num_classes)

    Why RNN: processes sequences step-by-step, maintaining a hidden state
    that summarizes history — natural fit for variable-length sequential
    data. Vanilla RNN suffers from vanishing gradients over long sequences
    (motivates LSTM/GRU, see Templates 7-8).
    """
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "rnn": nn.RNN(embed_dim, hidden_dim, batch_first=True, nonlinearity="tanh"),
        "classifier": nn.Linear(hidden_dim, num_classes),
    })


def forward_rnn(m: nn.ModuleDict, x: Tensor, lengths: Tensor) -> Tensor:
    embedded = m["embedding"](x)  # (B, T, E)

    # pack_padded_sequence tells the RNN to skip computation on padding
    # tokens — both correctness (padding shouldn't influence hidden
    # state) and efficiency.
    packed = nn.utils.rnn.pack_padded_sequence(
        embedded, lengths.cpu(), batch_first=True, enforce_sorted=False
    )
    _, hidden = m["rnn"](packed)   # hidden: (1, B, H)
    hidden = hidden.squeeze(0)     # (B, H)
    return m["classifier"](hidden)


def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for xb, lengths, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        logits = forward_rnn(model, xb, lengths)
        loss = criterion(logits, yb)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # RNNs are prone to exploding gradients
        optimizer.step()
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device) -> tuple[float, float]:
    model.eval()
    total_loss, correct = 0.0, 0
    for xb, lengths, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = forward_rnn(model, xb, lengths)
        total_loss += criterion(logits, yb).item() * xb.size(0)
        correct += (logits.argmax(1) == yb).sum().item()
    n = len(loader.dataset)
    return total_loss / n, correct / n


def main() -> None:
    set_seed(SEED)
    device = get_device()

    # Replace with real tokenized text data.
    rng = np.random.default_rng(SEED)
    sequences = [
        rng.integers(1, VOCAB_SIZE, size=rng.integers(5, 30)).tolist() for _ in range(1000)
    ]
    labels = rng.integers(0, NUM_CLASSES, size=1000).tolist()

    full_ds = SequenceDataset(sequences, labels)
    n = len(full_ds)
    n_train = int(0.8 * n)
    train_ds, val_ds = random_split(full_ds, [n_train, n - n_train])

    collate = lambda batch: collate_fn(batch, PAD_IDX)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate)

    model = build_model(VOCAB_SIZE, EMBED_DIM, HIDDEN_DIM, NUM_CLASSES, PAD_IDX).to(device)
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


@torch.no_grad()
def predict(model: nn.Module, sequences: list[list[int]], pad_idx: int, device: torch.device) -> np.ndarray:
    model.eval()
    tensors = [torch.tensor(s, dtype=torch.long) for s in sequences]
    lengths = torch.tensor([len(s) for s in sequences])
    padded = pad_sequence(tensors, batch_first=True, padding_value=pad_idx).to(device)
    logits = forward_rnn(model, padded, lengths)
    preds = logits.argmax(1)
    print(f"Predictions: {preds.cpu().numpy()}")
    return preds.cpu().numpy()


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: sequential data (text, time series) where order matters,
#   as a baseline before LSTM/GRU/Transformer.
# Advantages: simple, low parameter count vs LSTM/GRU, intuitive.
# Disadvantages: vanishing/exploding gradients over long sequences
#   (tanh repeated multiplication shrinks/grows gradients exponentially);
#   struggles with long-range dependencies; sequential computation
#   prevents parallelization across time steps (slow vs Transformers).
# Complexity: O(T * H^2) per sequence (T=seq_len, H=hidden_dim), sequential
#   in T so cannot parallelize across time.
# Follow-ups to expect:
#   - Why do vanilla RNNs suffer from vanishing gradients? (repeated
#     multiplication by the same weight matrix/derivative through time —
#     see BPTT.)
#   - Why pack_padded_sequence? (skips computation/loss contribution from
#     padding tokens, correctness + efficiency.)
#   - How would you handle bidirectional context? (nn.RNN(bidirectional=True),
#     concatenate forward/backward hidden states.)
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Binary:      num_classes=1 output, BCEWithLogitsLoss, y as float
# Multi-label: classifier -> num_labels units, BCEWithLogitsLoss, multi-hot y
# Regression (e.g. sentiment score): classifier -> 1 unit, MSELoss
# Sequence labeling (per-token, e.g. NER): use RNN output at every
#   timestep (not just final hidden), classifier applied per position.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: simple sequence tasks, short sequences, as an RNN-family baseline.
# Pros: simple, fewer params than LSTM/GRU.
# Cons: vanishing/exploding gradients on long sequences, sequential
#   compute (no parallelism across time), largely superseded by
#   LSTM/GRU/Transformer in practice.
# Time complexity: O(T * H^2).
# Space complexity: O(H^2) params, O(T*H) activations per sequence.
# Common mistakes: not clipping gradients (exploding gradients), not using
#   pack_padded_sequence with variable-length batches, forgetting
#   padding_idx in the embedding layer.
# Production checklist: gradient clipping always on, persist vocab/tokenizer
#   with the model, handle out-of-vocab tokens at inference, monitor
#   sequence-length distribution drift.
# ============================================================
