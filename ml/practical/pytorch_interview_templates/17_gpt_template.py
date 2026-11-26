"""
============================================================
TEMPLATE 17: GPT-style Decoder-Only Language Model (from scratch)
============================================================
Autoregressive next-token prediction using a small GPT-style Transformer
decoder (causal self-attention only, no cross-attention/encoder — unlike
Template 12's encoder-decoder Transformer decoder). Interview-scoped:
core architecture + training loop, not a production-scale LLM.
============================================================
"""

import math
import random

import numpy as np
import torch
from torch import nn, Tensor
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
SEED = 42
VOCAB_SIZE = 1000
BLOCK_SIZE = 64        # max context length
EMBED_DIM = 128
NUM_HEADS = 4
NUM_LAYERS = 4
DROPOUT = 0.1
BATCH_SIZE = 32
EPOCHS = 5
LR = 3e-4
CKPT_PATH = "checkpoints/gpt_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------
# Dataset: fixed-length token windows from a token stream
# ------------------------------------------------------------
def make_language_model_dataset(token_ids: np.ndarray, block_size: int) -> TensorDataset:
    """Precomputes every (input, target) window of length `block_size` up
    front, where target is input shifted by one position — standard
    next-token-prediction framing for autoregressive LM training. Packing
    all windows into stacked tensors upfront avoids a custom Dataset class."""
    n_windows = len(token_ids) - block_size
    xs = np.stack([token_ids[i: i + block_size] for i in range(n_windows)])
    ys = np.stack([token_ids[i + 1: i + block_size + 1] for i in range(n_windows)])
    x = torch.tensor(xs, dtype=torch.long)
    y = torch.tensor(ys, dtype=torch.long)
    return TensorDataset(x, y)


# ------------------------------------------------------------
# Model: GPT-style decoder-only Transformer
# ------------------------------------------------------------
def build_causal_self_attention(embed_dim: int, num_heads: int, block_size: int, dropout: float) -> nn.ModuleDict:
    """Multi-head self-attention with a causal mask: token i can only
    attend to tokens <= i (never future tokens) — what makes this
    autoregressive/generation-safe, unlike a bidirectional encoder."""
    assert embed_dim % num_heads == 0
    m = nn.ModuleDict({
        "qkv": nn.Linear(embed_dim, 3 * embed_dim),
        "proj": nn.Linear(embed_dim, embed_dim),
        "dropout": nn.Dropout(dropout),
    })
    m.num_heads = num_heads
    m.head_dim = embed_dim // num_heads
    m.register_buffer(
        "causal_mask",
        torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size),
    )
    return m


def forward_causal_self_attention(m: nn.ModuleDict, x: Tensor) -> Tensor:
    B, T, C = x.shape
    qkv = m["qkv"](x)  # (B, T, 3C)
    q, k, v = qkv.split(C, dim=2)
    q = q.view(B, T, m.num_heads, m.head_dim).transpose(1, 2)  # (B, nh, T, hd)
    k = k.view(B, T, m.num_heads, m.head_dim).transpose(1, 2)
    v = v.view(B, T, m.num_heads, m.head_dim).transpose(1, 2)

    attn_scores = (q @ k.transpose(-2, -1)) / math.sqrt(m.head_dim)  # (B, nh, T, T)
    attn_scores = attn_scores.masked_fill(m.causal_mask[:, :, :T, :T] == 0, float("-inf"))
    attn_weights = F.softmax(attn_scores, dim=-1)
    attn_weights = m["dropout"](attn_weights)

    out = attn_weights @ v  # (B, nh, T, hd)
    out = out.transpose(1, 2).contiguous().view(B, T, C)
    return m["proj"](out)


def build_gpt_block(embed_dim: int, num_heads: int, block_size: int, dropout: float) -> nn.ModuleDict:
    """Pre-norm Transformer decoder block: LayerNorm -> self-attn ->
    residual, LayerNorm -> MLP -> residual (pre-norm is more stable to
    train than the original post-norm Transformer at this depth)."""
    return nn.ModuleDict({
        "ln1": nn.LayerNorm(embed_dim),
        "attn": build_causal_self_attention(embed_dim, num_heads, block_size, dropout),
        "ln2": nn.LayerNorm(embed_dim),
        "mlp": nn.Sequential(
            nn.Linear(embed_dim, 4 * embed_dim),
            nn.GELU(),
            nn.Linear(4 * embed_dim, embed_dim),
            nn.Dropout(dropout),
        ),
    })


def forward_gpt_block(m: nn.ModuleDict, x: Tensor) -> Tensor:
    x = x + forward_causal_self_attention(m["attn"], m["ln1"](x))
    x = x + m["mlp"](m["ln2"](x))
    return x


def build_gpt(
    vocab_size: int,
    block_size: int,
    embed_dim: int,
    num_heads: int,
    num_layers: int,
    dropout: float,
) -> nn.ModuleDict:
    """Shape trace (B=batch, T=seq_len, C=embed_dim, V=vocab_size):
        token ids:        (B, T)
        token embeddings:  (B, T, C)
        + position embeds: (B, T, C)   [learned, added elementwise]
        after N blocks:    (B, T, C)
        logits:            (B, T, V)   [per-position next-token distribution]
    """
    m = nn.ModuleDict({
        "token_embedding": nn.Embedding(vocab_size, embed_dim),
        "position_embedding": nn.Embedding(block_size, embed_dim),
        "dropout": nn.Dropout(dropout),
        "blocks": nn.ModuleList(
            [build_gpt_block(embed_dim, num_heads, block_size, dropout) for _ in range(num_layers)]
        ),
        "ln_f": nn.LayerNorm(embed_dim),
        "lm_head": nn.Linear(embed_dim, vocab_size, bias=False),
    })
    m.block_size = block_size
    return m


def forward_gpt(m: nn.ModuleDict, idx: Tensor) -> Tensor:
    B, T = idx.shape
    positions = torch.arange(T, device=idx.device).unsqueeze(0)  # (1, T)

    x = m["token_embedding"](idx) + m["position_embedding"](positions)  # (B, T, C)
    x = m["dropout"](x)
    for block in m["blocks"]:
        x = forward_gpt_block(block, x)
    x = m["ln_f"](x)
    return m["lm_head"](x)  # (B, T, V)


@torch.no_grad()
def generate(m: nn.ModuleDict, idx: Tensor, max_new_tokens: int, temperature: float = 1.0) -> Tensor:
    """Autoregressive sampling: predict next token, append, repeat.
    Context is cropped to block_size since position embeddings only
    cover up to that length."""
    m.eval()
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -m.block_size:]
        logits = forward_gpt(m, idx_cond)[:, -1, :] / temperature  # (B, V), last position only
        probs = F.softmax(logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)  # (B, 1)
        idx = torch.cat([idx, next_token], dim=1)
    return idx


def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        logits = forward_gpt(model, xb)  # (B, T, V)
        loss = criterion(logits.view(-1, logits.size(-1)), yb.view(-1))
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device) -> float:
    model.eval()
    total_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = forward_gpt(model, xb)
        loss = criterion(logits.view(-1, logits.size(-1)), yb.view(-1))
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


def main() -> None:
    set_seed(SEED)
    device = get_device()

    # Replace with real tokenized text (e.g. BPE tokenizer output).
    rng = np.random.default_rng(SEED)
    token_stream = rng.integers(0, VOCAB_SIZE, size=20000)

    n_train = int(0.9 * len(token_stream))
    train_ds = make_language_model_dataset(token_stream[:n_train], BLOCK_SIZE)
    val_ds = make_language_model_dataset(token_stream[n_train:], BLOCK_SIZE)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    model = build_gpt(VOCAB_SIZE, BLOCK_SIZE, EMBED_DIM, NUM_HEADS, NUM_LAYERS, DROPOUT).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    best_val_loss = float("inf")

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss = evaluate(model, val_loader, criterion, device)
        print(f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_ppl={math.exp(val_loss):.2f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), CKPT_PATH)

    model.load_state_dict(torch.load(CKPT_PATH, map_location=device))

    prompt = torch.tensor([[1, 2, 3]], dtype=torch.long, device=device)
    generated = generate(model, prompt, max_new_tokens=10)
    print(f"Generated token ids: {generated[0].cpu().tolist()}")


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: open-ended text generation, autoregressive language
#   modeling — the architecture underlying GPT-family models.
# Advantages: fully parallelizable training (unlike RNNs — all positions'
#   losses computed in one forward pass via the causal mask); simple,
#   uniform decoder-only architecture (no separate encoder/cross-attention
#   like Template 12/13); scales predictably with data/params/compute
#   (empirical scaling laws).
# Disadvantages: quadratic attention cost in sequence length; needs causal
#   masking discipline (a single leaked future token silently invalidates
#   training); autoregressive generation is inherently sequential (can't
#   parallelize token-by-token sampling at inference).
# Complexity: O(T^2*d) per layer (same as any Transformer attention),
#   generation is O(T) sequential forward passes (or O(1) per step with
#   KV-caching, not shown here for simplicity).
# Follow-ups to expect:
#   - Why a causal mask instead of bidirectional attention? (autoregressive
#     generation requires that predicting token i never sees tokens > i,
#     otherwise train/inference behavior mismatch — label leakage.)
#   - What's the difference between this and Template 12's Transformer
#     decoder? (this has no cross-attention/encoder — GPT is decoder-only,
#     self-attention only; Template 12's decoder attends to encoder output too.)
#   - How would you add KV-caching for faster generation? (cache K/V per
#     layer across generation steps so each new token only computes attention
#     against cached past keys/values, not recomputing the whole sequence.)
#   - Why pre-norm (LayerNorm before sublayer) instead of post-norm?
#     (more stable gradients at greater depth, standard in modern GPT variants.)
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Larger context: increase BLOCK_SIZE (attention cost grows quadratically —
#   consider sparse/linear attention variants at scale).
# Top-k / nucleus (top-p) sampling: replace plain multinomial sampling in
#   `generate` with truncated distributions for higher-quality generation.
# Weight tying: tie `lm_head.weight` to `token_embedding.weight` to save
#   params and often improve quality (common in GPT-2 and later).
# Instruction-tuning / RLHF: fine-tune this pretrained LM on instruction-
#   response pairs (SFT) then optionally align further with RLHF/DPO.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# - KV-caching at inference: avoid recomputing attention over the full
#   context at every generation step.
# - Mixed precision + gradient checkpointing for larger models on limited
#   GPU memory.
# - Learning rate warmup + cosine decay schedule (standard for Transformer
#   training stability), not shown here for brevity.
# - Real BPE/byte-pair tokenizer (e.g. tiktoken, HF tokenizers) instead of
#   random synthetic token ids.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: autoregressive text generation, from-scratch decoder-only LM
#   architecture understanding (interviews often ask you to implement the
#   causal self-attention block specifically).
# Pros: simple uniform architecture, fully parallel training, scales well
#   empirically with data/compute.
# Cons: quadratic attention cost, sequential generation, causal-mask bugs
#   are easy to introduce and hard to notice (model still "trains" but
#   leaks future information).
# Time complexity: O(T^2*d) per layer for training; O(T) sequential steps
#   (or O(1) amortized per step with KV-cache) for generation.
# Space complexity: O(N_layers * d^2) params; O(T^2) attention activation
#   memory per layer without optimizations like FlashAttention.
# Common mistakes: forgetting/misapplying the causal mask (future-token
#   leakage); position embeddings not covering generation length beyond
#   block_size; not cropping context to block_size during generation.
# Production checklist: KV-caching for serving, quantization (int8/int4)
#   for deployment, prompt-length limits enforced at the API boundary,
#   monitor generation for repetition/degeneration.
# ============================================================
