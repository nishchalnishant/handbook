"""
============================================================
TEMPLATE 13: Full Transformer (Encoder-Decoder)
============================================================
Sequence-to-sequence generation (machine translation) using the full
"Attention Is All You Need" encoder-decoder Transformer, via
nn.Transformer. Combines Template 11 (encoder) + Template 12 (causal
decoder) + cross-attention between them. Interview-scoped.
============================================================
"""

import math
import random

import numpy as np
import torch
from torch import nn, Tensor
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
SEED = 42
SRC_VOCAB_SIZE = 3000
TGT_VOCAB_SIZE = 3000
EMBED_DIM = 128
NUM_HEADS = 4
NUM_ENCODER_LAYERS = 2
NUM_DECODER_LAYERS = 2
FF_DIM = 256
DROPOUT = 0.1
BATCH_SIZE = 32
EPOCHS = 10
LR = 3e-4
PAD_IDX = 0
SOS_IDX = 1
EOS_IDX = 2
MAX_GEN_LEN = 20
CKPT_PATH = "checkpoints/full_transformer_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TranslationDataset(Dataset):
    def __init__(self, src_seqs: list[list[int]], tgt_seqs: list[list[int]]) -> None:
        self.src_seqs = src_seqs
        self.tgt_seqs = tgt_seqs

    def __len__(self) -> int:
        return len(self.src_seqs)

    def __getitem__(self, idx: int) -> tuple[Tensor, Tensor]:
        return torch.tensor(self.src_seqs[idx], dtype=torch.long), torch.tensor(self.tgt_seqs[idx], dtype=torch.long)


def collate_fn(batch: list[tuple[Tensor, Tensor]], pad_idx: int) -> tuple[Tensor, Tensor]:
    src, tgt = zip(*batch)
    src_padded = pad_sequence(src, batch_first=True, padding_value=pad_idx)
    tgt_padded = pad_sequence(tgt, batch_first=True, padding_value=pad_idx)
    return src_padded, tgt_padded


def build_positional_encoding(embed_dim: int, max_len: int = 5000) -> Tensor:
    pe = torch.zeros(max_len, embed_dim)
    position = torch.arange(0, max_len).unsqueeze(1).float()
    div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-math.log(10000.0) / embed_dim))
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe.unsqueeze(0)


def forward_positional_encoding(pe: Tensor, x: Tensor) -> Tensor:
    return x + pe[:, : x.size(1)]


# ------------------------------------------------------------
# Model: encoder (bidirectional self-attn) + decoder (causal self-attn
# + cross-attn to encoder output) — the full original Transformer.
# ------------------------------------------------------------
def build_full_transformer(
    src_vocab_size: int,
    tgt_vocab_size: int,
    embed_dim: int,
    num_heads: int,
    num_encoder_layers: int,
    num_decoder_layers: int,
    ff_dim: int,
    dropout: float,
    pad_idx: int,
) -> nn.ModuleDict:
    """Shape trace (B=batch, Ts=src_len, Tt=tgt_len, E=embed_dim, V=vocab):
        src ids:          (B, Ts)
        tgt ids:          (B, Tt)
        encoder memory:   (B, Ts, E)   [bidirectional self-attention]
        decoder output:   (B, Tt, E)   [causal self-attn + cross-attn to memory]
        logits:           (B, Tt, V)

    Cross-attention is the key addition over a decoder-only model
    (Template 12): each decoder layer has a second attention block where
    queries come from the decoder's own sequence but keys/values come
    from the encoder's output — this is how the decoder "reads" the source.
    """
    return nn.ModuleDict({
        "src_embedding": nn.Embedding(src_vocab_size, embed_dim, padding_idx=pad_idx),
        "tgt_embedding": nn.Embedding(tgt_vocab_size, embed_dim, padding_idx=pad_idx),
        "transformer": nn.Transformer(
            d_model=embed_dim,
            nhead=num_heads,
            num_encoder_layers=num_encoder_layers,
            num_decoder_layers=num_decoder_layers,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True,
        ),
        "lm_head": nn.Linear(embed_dim, tgt_vocab_size),
    })


def forward_full_transformer(
    m: nn.ModuleDict, src: Tensor, tgt: Tensor, pe: Tensor, embed_dim: int, pad_idx: int
) -> Tensor:
    src_pad_mask = src == pad_idx  # (B, Ts), True = ignore
    tgt_pad_mask = tgt == pad_idx  # (B, Tt), True = ignore

    tgt_len = tgt.size(1)
    # Causal mask so decoder position i can't attend to future target tokens.
    tgt_causal_mask = nn.Transformer.generate_square_subsequent_mask(tgt_len).to(tgt.device)

    src_embedded = forward_positional_encoding(pe, m["src_embedding"](src) * math.sqrt(embed_dim))
    tgt_embedded = forward_positional_encoding(pe, m["tgt_embedding"](tgt) * math.sqrt(embed_dim))

    output = m["transformer"](
        src_embedded,
        tgt_embedded,
        tgt_mask=tgt_causal_mask,
        src_key_padding_mask=src_pad_mask,
        tgt_key_padding_mask=tgt_pad_mask,
        memory_key_padding_mask=src_pad_mask,
    )  # (B, Tt, E)

    return m["lm_head"](output)  # (B, Tt, V)


@torch.no_grad()
def generate(
    m: nn.ModuleDict, src: Tensor, max_len: int, sos_idx: int, eos_idx: int, pe: Tensor, embed_dim: int, pad_idx: int
) -> Tensor:
    """Greedy autoregressive decoding: re-run the decoder on the
    growing target prefix at each step (no KV-cache, for clarity)."""
    m.eval()
    batch_size = src.size(0)
    device = src.device
    generated = torch.full((batch_size, 1), sos_idx, dtype=torch.long, device=device)

    for _ in range(max_len):
        logits = forward_full_transformer(m, src, generated, pe, embed_dim, pad_idx)  # (B, T_cur, V)
        next_token = logits[:, -1, :].argmax(-1, keepdim=True)
        generated = torch.cat([generated, next_token], dim=1)
        if (next_token == eos_idx).all():
            break

    return generated


def train_one_epoch(model, loader, criterion, optimizer, device, pe, embed_dim, pad_idx) -> float:
    model.train()
    total_loss = 0.0
    for src, tgt in loader:
        src, tgt = src.to(device), tgt.to(device)
        tgt_input = tgt[:, :-1]   # decoder input: all but last token
        tgt_output = tgt[:, 1:]  # target: all but first token (shifted by 1)

        optimizer.zero_grad()
        logits = forward_full_transformer(model, src, tgt_input, pe, embed_dim, pad_idx)  # (B, Tt-1, V)
        loss = criterion(logits.reshape(-1, logits.size(-1)), tgt_output.reshape(-1))
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * src.size(0)
    return total_loss / len(loader.dataset)


def main() -> None:
    set_seed(SEED)
    device = get_device()

    rng = np.random.default_rng(SEED)
    src_seqs = [rng.integers(3, SRC_VOCAB_SIZE, size=rng.integers(5, 15)).tolist() for _ in range(500)]
    tgt_seqs = [rng.integers(3, TGT_VOCAB_SIZE, size=rng.integers(5, 15)).tolist() for _ in range(500)]

    ds = TranslationDataset(src_seqs, tgt_seqs)
    collate = lambda batch: collate_fn(batch, PAD_IDX)
    loader = DataLoader(ds, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate)

    model = build_full_transformer(
        SRC_VOCAB_SIZE, TGT_VOCAB_SIZE, EMBED_DIM, NUM_HEADS,
        NUM_ENCODER_LAYERS, NUM_DECODER_LAYERS, FF_DIM, DROPOUT, PAD_IDX,
    ).to(device)
    pe = build_positional_encoding(EMBED_DIM).to(device)
    criterion = nn.CrossEntropyLoss(ignore_index=PAD_IDX)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, loader, criterion, optimizer, device, pe, EMBED_DIM, PAD_IDX)
        print(f"Epoch {epoch:02d} | train_loss={train_loss:.4f}")

    torch.save(model.state_dict(), CKPT_PATH)

    sample_src = torch.tensor([src_seqs[0]], dtype=torch.long).to(device)
    generated = generate(model, sample_src, MAX_GEN_LEN, SOS_IDX, EOS_IDX, pe, EMBED_DIM, PAD_IDX)
    print(f"Generated token ids: {generated.cpu().numpy()}")


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: seq2seq tasks where source and target are genuinely
#   different sequences/modalities/languages — translation, summarization,
#   speech-to-text — the original Transformer architecture.
# Advantages: fully parallel training (unlike RNN seq2seq); encoder gives
#   bidirectional source context; cross-attention lets decoder access all
#   source positions directly (no fixed-context bottleneck as in Template 9).
# Disadvantages: more complex/heavier than encoder-only or decoder-only
#   alone; still sequential at inference (autoregressive decoding);
#   quadratic attention cost.
# Complexity: O(Ts^2*d) encoder self-attn + O(Tt^2*d) decoder self-attn +
#   O(Ts*Tt*d) cross-attn per layer.
# Follow-ups to expect:
#   - What's the difference between encoder self-attention, decoder
#     self-attention, and cross-attention (masking, Q/K/V sources)?
#   - Why shift target by one position for teacher-forced training
#     (tgt_input vs tgt_output)?
#   - When would you use encoder-decoder vs decoder-only (GPT-style)?
#     (encoder-decoder: distinct source/target with strong cross-referencing
#     needs, e.g. translation; decoder-only: open-ended generation/general
#     LM tasks, simpler and scales well.)
#   - How would you add KV-caching to speed up generation here?
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Beam search decoding instead of greedy in `generate`.
# Label smoothing in CrossEntropyLoss to reduce overconfidence.
# Shared src/tgt embeddings (weight tying) when vocabularies overlap
#   (e.g. same-language tasks) to reduce parameter count.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: true seq2seq tasks with distinct source/target sequences
#   (translation, summarization) needing full cross-attention access to
#   the source.
# Pros: parallel training, bidirectional source encoding, direct
#   cross-attention (no fixed bottleneck).
# Cons: heaviest of the three Transformer variants (encoder+decoder+cross-
#   attention), sequential autoregressive inference, quadratic attention.
# Time complexity: O(Ts^2*d + Tt^2*d + Ts*Tt*d) per layer.
# Space complexity: O(Ts^2 + Tt^2 + Ts*Tt) attention matrices per layer.
# Common mistakes: forgetting to shift target input/output for teacher
#   forcing; missing memory_key_padding_mask (source padding leaks into
#   cross-attention); confusing tgt_mask (causal) with padding masks.
# Production checklist: KV-caching for decoder inference, beam search for
#   generation quality, label smoothing, monitor BLEU/ROUGE on held-out
#   data, export considerations (dynamic shapes complicate ONNX export).
# ============================================================
