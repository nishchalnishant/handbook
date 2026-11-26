"""
============================================================
TEMPLATE 11: Transformer Encoder (from scratch)
============================================================
Text classification using a from-scratch Transformer encoder (BERT-style
encoder-only architecture). Reuses attention primitives conceptually
introduced in Template 10. Interview-scoped.
============================================================
"""

import math
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
MAX_LEN = 64
EMBED_DIM = 128
NUM_HEADS = 4
NUM_LAYERS = 2
FF_DIM = 256
NUM_CLASSES = 2
DROPOUT = 0.1
BATCH_SIZE = 32
EPOCHS = 10
LR = 1e-3
PAD_IDX = 0
CKPT_PATH = "checkpoints/transformer_encoder_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------
# Dataset
# ------------------------------------------------------------
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
    padded = pad_sequence(sequences, batch_first=True, padding_value=pad_idx)
    pad_mask = padded == pad_idx  # True where padding -> will be masked out of attention
    return padded, pad_mask, torch.tensor(labels, dtype=torch.long)


# ------------------------------------------------------------
# Positional encoding (sinusoidal, as in "Attention Is All You Need")
# ------------------------------------------------------------
def build_positional_encoding(embed_dim: int, max_len: int) -> Tensor:
    """Injects order information since self-attention itself is
    permutation-invariant. Sinusoidal (vs learned) encoding generalizes
    to sequence lengths not seen during training."""
    pe = torch.zeros(max_len, embed_dim)
    position = torch.arange(0, max_len).unsqueeze(1).float()
    div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-math.log(10000.0) / embed_dim))
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe.unsqueeze(0)  # (1, max_len, embed_dim), not a trainable param


def forward_positional_encoding(pe: Tensor, x: Tensor) -> Tensor:
    return x + pe[:, : x.size(1)]


# ------------------------------------------------------------
# Model: use PyTorch's built-in TransformerEncoder (production-realistic)
# ------------------------------------------------------------
def build_transformer_encoder_classifier(
    vocab_size: int,
    embed_dim: int,
    num_heads: int,
    num_layers: int,
    ff_dim: int,
    num_classes: int,
    max_len: int,
    dropout: float,
    pad_idx: int,
) -> nn.ModuleDict:
    """Embedding + positional encoding -> stacked self-attention encoder
    layers -> pool -> classify.

    Shape trace (B=batch, T=seq_len, E=embed_dim):
        input ids:          (B, T)
        embedded + pos enc: (B, T, E)
        encoder output:     (B, T, E)   [contextualized representations]
        pooled (mean):      (B, E)
        logits:             (B, num_classes)

    Why encoder-only: for tasks needing a single representation of the
    whole input (classification, embeddings) rather than autoregressive
    generation — bidirectional self-attention lets every token attend to
    every other token (unlike GPT's causal masking, Template 12).
    """
    # batch_first=True keeps shapes as (B, T, E) throughout, matching
    # our other templates' conventions.
    encoder_layer = nn.TransformerEncoderLayer(
        d_model=embed_dim,
        nhead=num_heads,
        dim_feedforward=ff_dim,
        dropout=dropout,
        batch_first=True,
        activation="gelu",
    )
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "encoder": nn.TransformerEncoder(encoder_layer, num_layers=num_layers),
        "classifier": nn.Linear(embed_dim, num_classes),
    })


def forward_transformer_encoder_classifier(m: nn.ModuleDict, x: Tensor, pad_mask: Tensor, pe: Tensor, embed_dim: int) -> Tensor:
    embedded = m["embedding"](x) * math.sqrt(embed_dim)  # scale as in original paper
    embedded = forward_positional_encoding(pe, embedded)

    # src_key_padding_mask: True positions are ignored in attention —
    # prevents padding tokens from influencing real tokens' representations.
    encoded = m["encoder"](embedded, src_key_padding_mask=pad_mask)  # (B, T, E)

    # Mean-pool over non-padded positions (mask-aware pooling).
    mask = (~pad_mask).unsqueeze(-1).float()  # (B, T, 1)
    summed = (encoded * mask).sum(dim=1)
    counts = mask.sum(dim=1).clamp(min=1e-6)
    pooled = summed / counts  # (B, E)

    return m["classifier"](pooled)


def train_one_epoch(model, loader, criterion, optimizer, device, pe, embed_dim) -> float:
    model.train()
    total_loss = 0.0
    for xb, pad_mask, yb in loader:
        xb, pad_mask, yb = xb.to(device), pad_mask.to(device), yb.to(device)
        optimizer.zero_grad()
        loss = criterion(forward_transformer_encoder_classifier(model, xb, pad_mask, pe, embed_dim), yb)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device, pe, embed_dim) -> tuple[float, float]:
    model.eval()
    total_loss, correct = 0.0, 0
    for xb, pad_mask, yb in loader:
        xb, pad_mask, yb = xb.to(device), pad_mask.to(device), yb.to(device)
        logits = forward_transformer_encoder_classifier(model, xb, pad_mask, pe, embed_dim)
        total_loss += criterion(logits, yb).item() * xb.size(0)
        correct += (logits.argmax(1) == yb).sum().item()
    n = len(loader.dataset)
    return total_loss / n, correct / n


def main() -> None:
    set_seed(SEED)
    device = get_device()

    rng = np.random.default_rng(SEED)
    sequences = [rng.integers(1, VOCAB_SIZE, size=rng.integers(5, MAX_LEN)).tolist() for _ in range(1000)]
    labels = rng.integers(0, NUM_CLASSES, size=1000).tolist()

    full_ds = SequenceDataset(sequences, labels)
    n = len(full_ds)
    n_train = int(0.8 * n)
    train_ds, val_ds = random_split(full_ds, [n_train, n - n_train])

    collate = lambda batch: collate_fn(batch, PAD_IDX)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate)

    model = build_transformer_encoder_classifier(
        VOCAB_SIZE, EMBED_DIM, NUM_HEADS, NUM_LAYERS, FF_DIM,
        NUM_CLASSES, MAX_LEN, DROPOUT, PAD_IDX,
    ).to(device)
    pe = build_positional_encoding(EMBED_DIM, MAX_LEN).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    best_acc = 0.0

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device, pe, EMBED_DIM)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device, pe, EMBED_DIM)
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
# When to use: tasks needing a contextualized representation of the whole
#   input at once (classification, sentence embeddings, token tagging) —
#   the architecture family behind BERT (Template 14).
# Advantages: fully parallelizable training (unlike RNNs); bidirectional
#   context (every token sees every other token); strong transfer learning
#   via pretraining (masked language modeling).
# Disadvantages: O(T^2) self-attention cost; needs positional encoding
#   since attention alone is permutation-invariant; large pretraining data/
#   compute requirements to be competitive from scratch.
# Complexity: O(T^2 * d) per layer for self-attention, O(T * d^2) for FFN.
# Follow-ups to expect:
#   - Why scale embeddings by sqrt(embed_dim)? (matches magnitude to
#     positional encoding scale, per the original paper.)
#   - Why LayerNorm instead of BatchNorm in Transformers? (normalizes
#     across features per-sample, not per-batch — works with variable
#     batch sizes/sequence lengths and no batch-statistics dependency.)
#   - Why mean-pool (or use a CLS token) instead of using all token
#     outputs directly for classification?
#   - src_key_padding_mask vs attention mask — what's the difference?
#     (padding mask marks invalid positions; attention mask can encode
#     causality or custom attend/don't-attend patterns.)
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Binary/Multi-label/Regression: same head-swap pattern as prior templates.
# CLS-token pooling instead of mean pooling: prepend a learnable [CLS]
#   token to the input sequence, use its output representation for
#   classification (as BERT does).
# Token-level tasks (NER, POS tagging): apply classifier to every token's
#   output representation instead of pooling.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: need bidirectional contextual representations of text (or
#   any sequence) for classification/embedding tasks.
# Pros: parallel training, bidirectional context, strong pretraining transfer.
# Cons: quadratic attention cost, needs explicit positional encoding, data/
#   compute-hungry to pretrain from scratch.
# Time complexity: O(T^2 * d + T * d^2) per encoder layer.
# Space complexity: O(T^2) attention matrix + O(d^2) per-layer weights.
# Common mistakes: forgetting src_key_padding_mask (padding leaks into
#   attention); mean-pooling over padding tokens without masking; missing
#   positional encoding entirely (breaks order-sensitivity).
# Production checklist: mask-aware pooling, persist tokenizer/vocab with
#   model, consider pretrained encoders (BERT/RoBERTa) over training from
#   scratch unless data is abundant, export ONNX/TorchScript for serving.
# ============================================================
