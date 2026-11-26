"""
============================================================
TEMPLATE 14: BERT Fine-Tuning (Hugging Face Transformers)
============================================================
Text classification by fine-tuning a pretrained BERT encoder via the
Hugging Face `transformers` library. Interview-scoped: focuses on the
fine-tuning workflow, not reimplementing BERT internals (see Template 11
for from-scratch Transformer encoder internals).
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
MODEL_NAME = "bert-base-uncased"
NUM_CLASSES = 2
MAX_LEN = 128
BATCH_SIZE = 16
EPOCHS = 3
LR = 2e-5  # small LR: fine-tuning a pretrained model, not training from scratch
FREEZE_BACKBONE = False
CKPT_PATH = "checkpoints/bert_finetune_best.pt"


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
# Model: pretrained BERT encoder + classification head on [CLS] token
# ------------------------------------------------------------
def build_model(model_name: str, num_classes: int, freeze_backbone: bool) -> nn.ModuleDict:
    """Shape trace (B=batch, T=max_len, H=hidden_size=768 for bert-base):
        input_ids/attention_mask: (B, T)
        last_hidden_state:        (B, T, H)
        [CLS] pooled output:      (B, H)   [position 0's representation]
        logits:                   (B, num_classes)

    Why fine-tune instead of training from scratch: BERT's pretraining
    (masked language modeling on huge corpora) already learned rich
    general-purpose language representations — fine-tuning adapts them to
    the downstream task with far less labeled data/compute than training
    an encoder from scratch (Template 11).
    """
    bert = AutoModel.from_pretrained(model_name)
    if freeze_backbone:
        for param in bert.parameters():
            param.requires_grad = False

    hidden_size = bert.config.hidden_size
    return nn.ModuleDict({
        "bert": bert,
        "dropout": nn.Dropout(0.1),
        "classifier": nn.Linear(hidden_size, num_classes),
    })


def forward_bert(m: nn.ModuleDict, input_ids: Tensor, attention_mask: Tensor) -> Tensor:
    outputs = m["bert"](input_ids=input_ids, attention_mask=attention_mask)
    cls_output = outputs.last_hidden_state[:, 0, :]  # [CLS] token representation, (B, H)
    return m["classifier"](m["dropout"](cls_output))


def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for input_ids, attention_mask, labels in loader:
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        logits = forward_bert(model, input_ids, attention_mask)
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

        logits = forward_bert(model, input_ids, attention_mask)
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
    logits = forward_bert(model, input_ids, attention_mask)
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
# When to use: text classification/tagging/QA tasks where labeled data is
#   limited but leveraging general-purpose pretrained language
#   representations is possible — the standard production approach for
#   most NLP classification tasks.
# Advantages: strong performance from pretraining transfer; far less
#   labeled data/compute needed than training a Transformer from scratch;
#   mature tooling (Hugging Face) for tokenization/checkpoints/deployment.
# Disadvantages: large model size/latency vs simpler models; fine-tuning
#   full model risks catastrophic forgetting with tiny datasets or
#   aggressive LR; less controllable/interpretable than simpler baselines.
# Complexity: same as Transformer encoder (Template 11), O(T^2*d) per
#   layer, but with 12 layers/768 hidden dim for bert-base (~110M params).
# Follow-ups to expect:
#   - Why use [CLS] token representation for classification? (BERT is
#     pretrained with next-sentence-prediction using [CLS], so it learns
#     to aggregate sequence-level meaning there.)
#   - Why such a small learning rate (2e-5) vs training from scratch
#     (1e-3)? (avoid destroying pretrained weights — large updates can
#     cause catastrophic forgetting.)
#   - Freezing vs fully fine-tuning the backbone — tradeoffs?
#   - What is BERT's pretraining objective? (masked language modeling +
#     next sentence prediction.)
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Binary/Multi-label: swap final Linear + loss (BCEWithLogitsLoss for
#   multi-label, sigmoid instead of softmax at inference).
# Token classification (NER): apply classifier to every token's hidden
#   state instead of just [CLS], use `AutoModelForTokenClassification`.
# Question answering: use `AutoModelForQuestionAnswering` with start/end
#   position heads instead of a single classification head.
# Layer-wise LR decay: smaller LR for early layers, larger for later
#   layers/head — common fine-tuning trick for better stability.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: NLP classification/tagging tasks where a pretrained encoder
#   can be fine-tuned — default production choice over from-scratch
#   Transformers for most text classification problems.
# Pros: strong transfer learning, mature ecosystem, less data/compute needed.
# Cons: larger/slower than task-specific small models, requires care with
#   LR/freezing to avoid catastrophic forgetting.
# Time complexity: O(T^2*d) per encoder layer x 12 layers (bert-base).
# Space complexity: ~110M params (bert-base) — consider DistilBERT
#   (Template 15) for lighter deployment.
# Common mistakes: using too-large learning rate (destroys pretrained
#   weights); forgetting attention_mask (padding leaks into attention);
#   mismatched tokenizer/model pairs; not setting model.eval() at inference
#   (dropout still active otherwise).
# Production checklist: save/load both model weights and tokenizer
#   together, consider ONNX export or `torch.compile` for inference speed,
#   monitor for distribution shift in production text vs fine-tuning data.
# ============================================================
