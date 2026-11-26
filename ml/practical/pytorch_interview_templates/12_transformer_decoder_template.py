"""
============================================================
TEMPLATE 12: Transformer Decoder (causal, GPT-style, from scratch)
============================================================
Autoregressive next-token language modeling using a decoder-only
Transformer (causal self-attention only, no cross-attention — the
architecture family behind GPT). Interview-scoped.
============================================================
"""

import math
import random

import numpy as np
import torch
from torch import nn, Tensor
from torch.utils.data import Dataset, DataLoader


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
SEED = 42
VOCAB_SIZE = 5000
SEQ_LEN = 32
EMBED_DIM = 128
NUM_HEADS = 4
NUM_LAYERS = 2
FF_DIM = 256
DROPOUT = 0.1
BATCH_SIZE = 32
EPOCHS = 10
LR = 3e-4
PAD_IDX = 0
CKPT_PATH = "checkpoints/transformer_decoder_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------
# Dataset: fixed-length chunks of token ids, next-token targets
# ------------------------------------------------------------
class LMDataset(Dataset):
    """Each sample is a (input_chunk, target_chunk) pair where target is
    input shifted by one position — standard next-token-prediction setup."""

    def __init__(self, token_ids: list[int], seq_len: int) -> None:
        self.token_ids = token_ids
        self.seq_len = seq_len

    def __len__(self) -> int:
        return len(self.token_ids) - self.seq_len

    def __getitem__(self, idx: int) -> tuple[Tensor, Tensor]:
        chunk = self.token_ids[idx : idx + self.seq_len + 1]
        x = torch.tensor(chunk[:-1], dtype=torch.long)
        y = torch.tensor(chunk[1:], dtype=torch.long)
        return x, y


def build_positional_encoding(embed_dim: int, max_len: int) -> Tensor:
    pe = torch.zeros(max_len, embed_dim)
    position = torch.arange(0, max_len).unsqueeze(1).float()
    div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-math.log(10000.0) / embed_dim))
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe.unsqueeze(0)


def forward_positional_encoding(pe: Tensor, x: Tensor) -> Tensor:
    return x + pe[:, : x.size(1)]


# ------------------------------------------------------------
# Model
# ------------------------------------------------------------
def build_transformer_decoder_lm(
    vocab_size: int,
    embed_dim: int,
    num_heads: int,
    num_layers: int,
    ff_dim: int,
    max_len: int,
    dropout: float,
    pad_idx: int,
) -> nn.ModuleDict:
    """Decoder-only Transformer for autoregressive language modeling.

    Shape trace (B=batch, T=seq_len, E=embed_dim, V=vocab_size):
        input ids:      (B, T)
        embedded:       (B, T, E)
        decoder output: (B, T, E)   [causally-masked self-attention]
        logits:         (B, T, V)

    Why causal masking: at position i, the model must only attend to
    positions <= i — otherwise it could "see the future" token it's
    supposed to predict, making training trivial but useless at inference
    (where future tokens don't exist yet).

    Note: uses nn.TransformerEncoder internally (PyTorch naming is
    historical) with a causal attention mask — this is exactly the
    decoder-only setup GPT uses (no cross-attention to a separate encoder,
    unlike the full encoder-decoder Transformer in Template 13).
    """
    layer = nn.TransformerEncoderLayer(
        d_model=embed_dim,
        nhead=num_heads,
        dim_feedforward=ff_dim,
        dropout=dropout,
        batch_first=True,
        activation="gelu",
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

    # Causal mask: (T, T) upper-triangular of -inf above the diagonal,
    # so position i's attention scores to positions > i become -inf
    # (softmax -> 0). is_causal path in PyTorch builds this internally.
    causal_mask = nn.Transformer.generate_square_subsequent_mask(T).to(x.device)

    decoded = m["decoder"](embedded, mask=causal_mask, is_causal=True)  # (B, T, E)
    return m["lm_head"](decoded)  # (B, T, V)


@torch.no_grad()
def generate(m: nn.ModuleDict, prompt: Tensor, max_new_tokens: int, seq_len: int, pe: Tensor, embed_dim: int) -> Tensor:
    """Greedy autoregressive generation, one token at a time."""
    m.eval()
    generated = prompt
    for _ in range(max_new_tokens):
        context = generated[:, -seq_len:]  # truncate to model's max context
        logits = forward_transformer_decoder_lm(m, context, pe, embed_dim)  # (B, T, V)
        next_token_logits = logits[:, -1, :]  # only need the last position's prediction
        next_token = next_token_logits.argmax(-1, keepdim=True)
        generated = torch.cat([generated, next_token], dim=1)
    return generated


def train_one_epoch(model, loader, criterion, optimizer, device, pe, embed_dim) -> float:
    model.train()
    total_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        logits = forward_transformer_decoder_lm(model, xb, pe, embed_dim)  # (B, T, V)
        loss = criterion(logits.reshape(-1, logits.size(-1)), yb.reshape(-1))
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device, pe, embed_dim) -> float:
    model.eval()
    total_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = forward_transformer_decoder_lm(model, xb, pe, embed_dim)
        total_loss += criterion(logits.reshape(-1, logits.size(-1)), yb.reshape(-1)).item() * xb.size(0)
    return total_loss / len(loader.dataset)


def main() -> None:
    set_seed(SEED)
    device = get_device()

    rng = np.random.default_rng(SEED)
    token_ids = rng.integers(1, VOCAB_SIZE, size=20000).tolist()

    n_train = int(0.9 * len(token_ids))
    train_ds = LMDataset(token_ids[:n_train], SEQ_LEN)
    val_ds = LMDataset(token_ids[n_train:], SEQ_LEN)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    model = build_transformer_decoder_lm(
        VOCAB_SIZE, EMBED_DIM, NUM_HEADS, NUM_LAYERS, FF_DIM,
        SEQ_LEN, DROPOUT, PAD_IDX,
    ).to(device)
    pe = build_positional_encoding(EMBED_DIM, SEQ_LEN).to(device)
    criterion = nn.CrossEntropyLoss(ignore_index=PAD_IDX)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    best_val_loss = float("inf")

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device, pe, EMBED_DIM)
        val_loss = evaluate(model, val_loader, criterion, device, pe, EMBED_DIM)
        print(f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), CKPT_PATH)

    model.load_state_dict(torch.load(CKPT_PATH, map_location=device))

    # Inference example: greedy-generate continuation from a short prompt.
    prompt = torch.tensor([token_ids[:5]], dtype=torch.long).to(device)
    generated = generate(model, prompt, max_new_tokens=10, seq_len=SEQ_LEN, pe=pe, embed_dim=EMBED_DIM)
    print(f"Generated token ids: {generated.cpu().numpy()}")


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: autoregressive generation tasks — language modeling, text
#   generation, code completion (the architecture family behind GPT).
# Advantages: simple, uniform architecture (no separate encoder); trains
#   in parallel via causal masking (unlike RNN, no sequential recurrence
#   needed during training); scales extremely well with data/params.
# Disadvantages: inference is inherently sequential (one token at a time);
#   quadratic attention cost in sequence length; no bidirectional context
#   (each position only sees the past).
# Complexity: O(T^2 * d) per layer for attention (same as encoder), but
#   generation requires T sequential forward passes (or KV-caching to
#   amortize).
# Follow-ups to expect:
#   - Why causal masking, and how is it implemented? (upper-triangular
#     mask added to attention scores before softmax, or `is_causal=True`.)
#   - Why is generation sequential even though training is parallel?
#     (at inference, token t+1 depends on the model's own prediction at
#     t, which doesn't exist until computed — unlike training where the
#     full ground-truth sequence is already available.)
#   - What is KV-caching and why does it matter for inference speed?
#     (cache previously computed key/value projections so each new token
#     doesn't require recomputing attention over the whole prefix.)
#   - Decoder-only vs encoder-decoder — when would you pick each?
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Temperature/top-k/top-p sampling: replace greedy argmax in `generate`
#   with stochastic sampling for more diverse generations.
# KV-caching: cache key/value tensors across generation steps instead of
#   recomputing full attention each step (major production speedup).
# Prefix/instruction tuning: fine-tune on (prompt, completion) pairs with
#   loss masked on the prompt portion only.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: autoregressive sequence generation (language modeling, text/
#   code completion) is the task.
# Pros: parallel training via masking, scales well, simple uniform stack.
# Cons: sequential (or cache-dependent) inference, quadratic attention
#   cost, unidirectional context only.
# Time complexity: O(T^2 * d) per layer at training; O(T) sequential
#   steps at naive inference (O(1) per step with KV-cache).
# Space complexity: O(T^2) attention matrix per layer; O(T*d) KV-cache
#   per layer during cached generation.
# Common mistakes: forgetting the causal mask (lets model cheat during
#   training, useless at inference); off-by-one errors in input/target
#   shifting; not truncating context to the model's max sequence length
#   during generation.
# Production checklist: implement KV-caching for real-time generation,
#   add sampling strategies (temperature/top-k/top-p) beyond greedy,
#   cap max generation length, monitor for repetition/degeneration.
# ============================================================
