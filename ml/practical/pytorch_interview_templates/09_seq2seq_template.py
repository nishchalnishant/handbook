"""
============================================================
TEMPLATE 9: Seq2Seq (Encoder-Decoder with GRU)
============================================================
Sequence-to-sequence generation (e.g. machine translation,
summarization) using a GRU encoder-decoder with teacher forcing.
Interview-scoped.
============================================================
"""

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
HIDDEN_DIM = 256
BATCH_SIZE = 32
EPOCHS = 10
LR = 1e-3
PAD_IDX = 0
SOS_IDX = 1
EOS_IDX = 2
TEACHER_FORCING_RATIO = 0.5
MAX_GEN_LEN = 20
CKPT_PATH = "checkpoints/seq2seq_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------
# Dataset: paired source/target token sequences
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# Model
# ------------------------------------------------------------
def build_encoder(vocab_size: int, embed_dim: int, hidden_dim: int, pad_idx: int) -> nn.ModuleDict:
    """Encodes source sequence into a fixed-size context vector (final
    hidden state). This is the classic seq2seq bottleneck that attention
    (Template 10) was invented to fix."""
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "gru": nn.GRU(embed_dim, hidden_dim, batch_first=True),
    })


def forward_encoder(m: nn.ModuleDict, src: Tensor) -> Tensor:
    embedded = m["embedding"](src)          # (B, T_src, E)
    _, hidden = m["gru"](embedded)          # hidden: (1, B, H)
    return hidden


def build_decoder(vocab_size: int, embed_dim: int, hidden_dim: int, pad_idx: int) -> nn.ModuleDict:
    """Generates target sequence one token at a time, conditioned on the
    encoder's final hidden state as its initial hidden state."""
    return nn.ModuleDict({
        "embedding": nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx),
        "gru": nn.GRU(embed_dim, hidden_dim, batch_first=True),
        "out": nn.Linear(hidden_dim, vocab_size),
    })


def forward_decoder(m: nn.ModuleDict, input_token: Tensor, hidden: Tensor) -> tuple[Tensor, Tensor]:
    embedded = m["embedding"](input_token)          # (B, 1, E)
    output, hidden = m["gru"](embedded, hidden)      # output: (B, 1, H)
    logits = m["out"](output.squeeze(1))             # (B, vocab_size)
    return logits, hidden


def build_seq2seq(encoder: nn.ModuleDict, decoder: nn.ModuleDict) -> nn.ModuleDict:
    """Ties encoder + decoder together with teacher forcing during training.

    Why teacher forcing: feeding the ground-truth previous token (instead
    of the model's own prediction) during training stabilizes/speeds up
    convergence, at the cost of train/inference mismatch (exposure bias) —
    a classic interview discussion point.
    """
    return nn.ModuleDict({
        "encoder": encoder,
        "decoder": decoder,
    })


def forward_seq2seq(m: nn.ModuleDict, src: Tensor, tgt: Tensor, teacher_forcing_ratio: float, sos_idx: int) -> Tensor:
    batch_size, tgt_len = tgt.shape
    vocab_size = m["decoder"]["out"].out_features
    device = src.device

    outputs = torch.zeros(batch_size, tgt_len, vocab_size, device=device)
    hidden = forward_encoder(m["encoder"], src)

    # First decoder input is <SOS> for every sequence in the batch.
    input_token = torch.full((batch_size, 1), sos_idx, dtype=torch.long, device=device)

    for t in range(tgt_len):
        logits, hidden = forward_decoder(m["decoder"], input_token, hidden)
        outputs[:, t] = logits

        use_teacher_forcing = random.random() < teacher_forcing_ratio
        if use_teacher_forcing:
            input_token = tgt[:, t : t + 1]           # ground truth
        else:
            input_token = logits.argmax(1, keepdim=True)  # model's own prediction

    return outputs  # (B, T_tgt, vocab_size)


@torch.no_grad()
def generate_seq2seq(m: nn.ModuleDict, src: Tensor, max_len: int, eos_idx: int, sos_idx: int) -> Tensor:
    """Greedy decoding at inference time — no teacher forcing available."""
    m.eval()
    batch_size = src.size(0)
    device = src.device
    hidden = forward_encoder(m["encoder"], src)
    input_token = torch.full((batch_size, 1), sos_idx, dtype=torch.long, device=device)
    generated = []

    for _ in range(max_len):
        logits, hidden = forward_decoder(m["decoder"], input_token, hidden)
        next_token = logits.argmax(1, keepdim=True)
        generated.append(next_token)
        input_token = next_token
        if (next_token == eos_idx).all():
            break

    return torch.cat(generated, dim=1)


def train_one_epoch(model, loader, criterion, optimizer, device, teacher_forcing_ratio) -> float:
    model.train()
    total_loss = 0.0
    for src, tgt in loader:
        src, tgt = src.to(device), tgt.to(device)
        optimizer.zero_grad()
        outputs = forward_seq2seq(model, src, tgt, teacher_forcing_ratio, SOS_IDX)  # (B, T, V)
        # Flatten batch+time dims for CrossEntropyLoss; ignore pad tokens in loss.
        loss = criterion(outputs.reshape(-1, outputs.size(-1)), tgt.reshape(-1))
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * src.size(0)
    return total_loss / len(loader.dataset)


def main() -> None:
    set_seed(SEED)
    device = get_device()

    # Replace with real tokenized parallel corpus (source, target) pairs.
    rng = np.random.default_rng(SEED)
    src_seqs = [rng.integers(3, SRC_VOCAB_SIZE, size=rng.integers(5, 15)).tolist() for _ in range(500)]
    tgt_seqs = [rng.integers(3, TGT_VOCAB_SIZE, size=rng.integers(5, 15)).tolist() for _ in range(500)]

    ds = TranslationDataset(src_seqs, tgt_seqs)
    collate = lambda batch: collate_fn(batch, PAD_IDX)
    loader = DataLoader(ds, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate)

    encoder = build_encoder(SRC_VOCAB_SIZE, EMBED_DIM, HIDDEN_DIM, PAD_IDX)
    decoder = build_decoder(TGT_VOCAB_SIZE, EMBED_DIM, HIDDEN_DIM, PAD_IDX)
    model = build_seq2seq(encoder, decoder).to(device)

    # ignore_index=pad_idx excludes padding positions from the loss so the
    # model isn't penalized/rewarded for predicting padding.
    criterion = nn.CrossEntropyLoss(ignore_index=PAD_IDX)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, loader, criterion, optimizer, device, TEACHER_FORCING_RATIO)
        print(f"Epoch {epoch:02d} | train_loss={train_loss:.4f}")

    torch.save(model.state_dict(), CKPT_PATH)

    # Inference example: greedy decode a sample source sequence.
    sample_src = torch.tensor([src_seqs[0]], dtype=torch.long).to(device)
    generated = generate_seq2seq(model, sample_src, MAX_GEN_LEN, EOS_IDX, SOS_IDX)
    print(f"Generated token ids: {generated.cpu().numpy()}")


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: variable-length input -> variable-length output tasks
#   (translation, summarization, chatbots) before/without full Transformers.
# Advantages: naturally handles differing input/output lengths; conceptually
#   simple encoder/decoder split.
# Disadvantages: fixed-size context vector is an information bottleneck for
#   long sequences (motivates attention, Template 10); teacher forcing
#   creates train/inference mismatch (exposure bias); sequential decoding
#   is slow at inference.
# Complexity: O(T_src * H^2 + T_tgt * H^2) sequential steps.
# Follow-ups to expect:
#   - What's the bottleneck problem with vanilla seq2seq? (single fixed
#     context vector must encode the entire source sequence.)
#   - What is teacher forcing and its tradeoff? (faster/stabler training
#     vs exposure bias at inference — model never sees its own errors
#     during training.)
#   - How does attention fix the bottleneck? (decoder attends over all
#     encoder hidden states, not just the final one — see Template 10.)
#   - Greedy vs beam search decoding tradeoffs.
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Attention-augmented seq2seq: pass all encoder hidden states to decoder,
#   compute attention weights per decoding step (see Template 10).
# Bidirectional encoder: use bidirectional GRU/LSTM in the encoder for
#   richer source representations (combine directions before feeding decoder).
# Beam search decoding: replace greedy argmax in `generate` with a beam
#   of top-k candidate sequences, scored by cumulative log-probability.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: variable-length sequence transduction tasks (translation,
#   summarization) — largely superseded by Transformer seq2seq in production.
# Pros: simple encoder/decoder abstraction, handles variable I/O lengths.
# Cons: fixed context vector bottleneck, exposure bias from teacher
#   forcing, slow sequential decoding.
# Time complexity: O((T_src + T_tgt) * H^2).
# Space complexity: O(H^2) params for encoder+decoder GRUs.
# Common mistakes: forgetting ignore_index=pad_idx in the loss; not
#   detaching/handling hidden state shapes between encoder and decoder;
#   using teacher forcing at inference time (should always be greedy/beam).
# Production checklist: use beam search at inference for quality, cap
#   max generation length to avoid runaway loops, monitor generation
#   length distribution, prefer full Transformer seq2seq at production scale.
# ============================================================
