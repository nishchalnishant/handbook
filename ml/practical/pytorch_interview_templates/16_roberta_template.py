"""
============================================================
TEMPLATE 16: RoBERTa Fine-Tuning (Hugging Face Transformers)
============================================================
Text classification by fine-tuning a pretrained RoBERTa encoder via the
Hugging Face `transformers` library. Interview-scoped: same fine-tuning
workflow as BERT (Template 14) — the interesting delta is RoBERTa's
pretraining/tokenization differences, not the training loop.
============================================================
"""

import random

import numpy as np
import torch
from torch import nn, Tensor
from torch.utils.data import TensorDataset, DataLoader
from transformers import AutoTokenizer, AutoModel


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
SEED = 42
MODEL_NAME = "roberta-base"
NUM_CLASSES = 2
MAX_LEN = 128
BATCH_SIZE = 16
EPOCHS = 3
LR = 2e-5  # small LR: fine-tuning a pretrained model, not training from scratch
FREEZE_BACKBONE = False
CKPT_PATH = "checkpoints/roberta_finetune_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------
# Dataset: tokenize upfront (whole split at once) into a TensorDataset
# ------------------------------------------------------------
def make_text_classification_dataset(texts: list[str], labels: list[int], tokenizer, max_len: int) -> TensorDataset:
    """Tokenizes the full list of texts upfront (HF tokenizers accept a
    list[str] batch directly) and packs everything into plain tensors —
    avoids a custom Dataset class while keeping DataLoader compatibility."""
    encoding = tokenizer(
        texts,
        truncation=True,
        max_length=max_len,
        padding="max_length",
        return_tensors="pt",
    )
    labels_t = torch.tensor(labels, dtype=torch.long)
    return TensorDataset(encoding["input_ids"], encoding["attention_mask"], labels_t)


# ------------------------------------------------------------
# Model: pretrained RoBERTa encoder + classification head on <s> token
# ------------------------------------------------------------
def build_model(model_name: str, num_classes: int, freeze_backbone: bool) -> nn.ModuleDict:
    """Shape trace (B=batch, T=max_len, H=hidden_size=768 for roberta-base):
        input_ids/attention_mask: (B, T)
        last_hidden_state:        (B, T, H)
        <s> pooled output:        (B, H)   [position 0's representation, RoBERTa's analogue of BERT's [CLS]]
        logits:                   (B, num_classes)

    Why RoBERTa over BERT: same architecture, but pretrained longer on
    ~10x more data, with dynamic masking (mask pattern changes each epoch
    instead of being fixed once) and no next-sentence-prediction objective
    (found to not help, or hurt, downstream performance). Uses byte-level
    BPE tokenization instead of BERT's WordPiece — a different tokenizer,
    not just different weights, so RoBERTa checkpoints and tokenizers must
    be paired, never mixed with BERT's.
    """
    roberta = AutoModel.from_pretrained(model_name)
    if freeze_backbone:
        for param in roberta.parameters():
            param.requires_grad = False

    hidden_size = roberta.config.hidden_size
    return nn.ModuleDict({
        "roberta": roberta,
        "dropout": nn.Dropout(0.1),
        "classifier": nn.Linear(hidden_size, num_classes),
    })


def forward_roberta(m: nn.ModuleDict, input_ids: Tensor, attention_mask: Tensor) -> Tensor:
    outputs = m["roberta"](input_ids=input_ids, attention_mask=attention_mask)
    cls_output = outputs.last_hidden_state[:, 0, :]  # <s> token representation, (B, H)
    return m["classifier"](m["dropout"](cls_output))


def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for input_ids, attention_mask, labels in loader:
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        logits = forward_roberta(model, input_ids, attention_mask)
        loss = criterion(logits, labels)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * input_ids.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device) -> tuple[float, float]:
    model.eval()
    total_loss, correct = 0.0, 0
    for input_ids, attention_mask, labels in loader:
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        logits = forward_roberta(model, input_ids, attention_mask)
        total_loss += criterion(logits, labels).item() * input_ids.size(0)
        correct += (logits.argmax(1) == labels).sum().item()
    n = len(loader.dataset)
    return total_loss / n, correct / n


@torch.no_grad()
def predict(model, text: str, tokenizer, max_len: int, device) -> int:
    model.eval()
    encoding = tokenizer(text, truncation=True, max_length=max_len, padding="max_length", return_tensors="pt")
    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)
    logits = forward_roberta(model, input_ids, attention_mask)
    return logits.argmax(1).item()


def main() -> None:
    set_seed(SEED)
    device = get_device()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Replace with real labeled text data.
    texts = [f"example sentence number {i}" for i in range(200)]
    labels = [i % NUM_CLASSES for i in range(200)]

    n_train = int(0.8 * len(texts))
    train_ds = make_text_classification_dataset(texts[:n_train], labels[:n_train], tokenizer, MAX_LEN)
    val_ds = make_text_classification_dataset(texts[n_train:], labels[n_train:], tokenizer, MAX_LEN)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    model = build_model(MODEL_NAME, NUM_CLASSES, FREEZE_BACKBONE).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    best_acc = 0.0

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        print(f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), CKPT_PATH)

    model.load_state_dict(torch.load(CKPT_PATH, map_location=device))

    pred = predict(model, "example sentence number 1", tokenizer, MAX_LEN, device)
    print(f"Predicted class: {pred}")


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: same as BERT — text classification/tagging/QA fine-tuning —
#   RoBERTa is usually a drop-in upgrade over BERT when compute allows,
#   often chosen as the stronger default encoder baseline.
# Advantages: outperforms BERT on most benchmarks (GLUE, SQuAD) due to
#   longer training, more data, larger batches, dynamic masking; removing
#   next-sentence-prediction simplified pretraining without hurting quality.
# Disadvantages: larger pretraining compute footprint (not relevant to
#   fine-tuning cost, but relevant to why checkpoints are large); byte-level
#   BPE tokenizer produces different token counts than BERT's WordPiece,
#   so MAX_LEN budgeting can differ slightly between the two.
# Complexity: same as BERT (Template 14), O(T^2*d) per layer, 12 layers/768
#   hidden dim for roberta-base (~125M params, slightly more than bert-base
#   due to a larger vocabulary).
# Follow-ups to expect:
#   - What concretely changed from BERT to RoBERTa? (more data, longer
#     training, larger batches, dynamic masking, dropped NSP objective,
#     byte-level BPE tokenizer.)
#   - Why drop next-sentence-prediction? (ablations showed it didn't help,
#     sometimes hurt, downstream task performance.)
#   - Why does RoBERTa use `<s>`/`</s>` instead of `[CLS]`/`[SEP]`? (different
#     tokenizer/special-token convention — must use RoBERTa's own tokenizer,
#     never mix with BERT's.)
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Binary/Multi-label: swap final Linear + loss (BCEWithLogitsLoss for
#   multi-label, sigmoid instead of softmax at inference).
# Token classification (NER): apply classifier to every token's hidden
#   state instead of just <s>, use `AutoModelForTokenClassification`.
# Question answering: use `AutoModelForQuestionAnswering` with start/end
#   position heads instead of a single classification head.
# Larger variant: "roberta-large" for more capacity at higher compute cost.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# - Layer-wise LR decay: smaller LR for early layers, larger for later
#   layers/head — common fine-tuning trick for better stability.
# - Mixed precision (torch.autocast + GradScaler) to cut fine-tuning time
#   and memory roughly in half on supported GPUs.
# - Gradient accumulation for larger effective batch sizes on limited GPU
#   memory (RoBERTa's recommended batch sizes are large).
# - Persist tokenizer alongside model weights — a mismatched tokenizer
#   silently produces garbage token ids without erroring.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: NLP classification/tagging tasks — a stronger default encoder
#   than BERT when extra pretraining compute/data quality matters.
# Pros: stronger benchmark performance than BERT, same fine-tuning workflow
#   and ecosystem support.
# Cons: slightly larger model/vocab than BERT, requires its own tokenizer
#   (not interchangeable with BERT's), same catastrophic-forgetting risk
#   if fine-tuning LR is too large.
# Time complexity: O(T^2*d) per encoder layer x 12 layers (roberta-base).
# Space complexity: ~125M params (roberta-base).
# Common mistakes: using BERT's tokenizer with a RoBERTa checkpoint (or
#   vice versa); using too-large a fine-tuning LR; forgetting attention_mask.
# Production checklist: save/load both model weights and tokenizer
#   together, consider ONNX export or `torch.compile` for inference speed,
#   monitor for distribution shift in production text vs fine-tuning data.
# ============================================================
