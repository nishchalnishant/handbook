"""
============================================================
TEMPLATE 15: DistilBERT Fine-Tuning (Hugging Face Transformers)
============================================================
Text classification by fine-tuning DistilBERT — a distilled, smaller/
faster version of BERT. Nearly identical workflow to Template 14; the
interview-relevant delta is *why* distillation and its tradeoffs.
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
MODEL_NAME = "distilbert-base-uncased"
NUM_CLASSES = 2
MAX_LEN = 128
BATCH_SIZE = 16
EPOCHS = 3
LR = 2e-5
CKPT_PATH = "checkpoints/distilbert_finetune_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


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


def build_model(model_name: str, num_classes: int) -> nn.ModuleDict:
    """DistilBERT has no [CLS]-specific pretraining objective (no next-
    sentence-prediction task like BERT), but by convention still uses the
    first token's representation as the pooled sequence representation.

    Key difference from BERT: 6 layers instead of 12, no token_type_ids
    input (DistilBERT drops segment embeddings), ~40% fewer parameters,
    ~60% faster inference, trained via knowledge distillation from BERT
    (student mimics teacher's output distribution, not just hard labels).
    """
    distilbert = AutoModel.from_pretrained(model_name)
    hidden_size = distilbert.config.hidden_size
    return nn.ModuleDict({
        "distilbert": distilbert,
        "dropout": nn.Dropout(0.1),
        "classifier": nn.Linear(hidden_size, num_classes),
    })


def forward_distilbert(m: nn.ModuleDict, input_ids: Tensor, attention_mask: Tensor) -> Tensor:
    outputs = m["distilbert"](input_ids=input_ids, attention_mask=attention_mask)
    pooled = outputs.last_hidden_state[:, 0, :]  # first token representation, (B, H)
    return m["classifier"](m["dropout"](pooled))


def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for input_ids, attention_mask, labels in loader:
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        loss = criterion(forward_distilbert(model, input_ids, attention_mask), labels)
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

        logits = forward_distilbert(model, input_ids, attention_mask)
        total_loss += criterion(logits, labels).item() * input_ids.size(0)
        correct += (logits.argmax(1) == labels).sum().item()
    n = len(loader.dataset)
    return total_loss / n, correct / n


def main() -> None:
    set_seed(SEED)
    device = get_device()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    texts = [f"example sentence number {i}" for i in range(200)]
    labels = [i % NUM_CLASSES for i in range(200)]

    n_train = int(0.8 * len(texts))
    train_ds = make_text_classification_dataset(texts[:n_train], labels[:n_train], tokenizer, MAX_LEN)
    val_ds = make_text_classification_dataset(texts[n_train:], labels[n_train:], tokenizer, MAX_LEN)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    model = build_model(MODEL_NAME, NUM_CLASSES).to(device)
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


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: latency/memory-constrained deployments (mobile, edge, high-
#   QPS services) where BERT's accuracy is close to sufficient but its
#   size/speed is not.
# Advantages: ~40% smaller, ~60% faster than BERT-base, retains ~97% of
#   BERT's language understanding performance on many benchmarks.
# Disadvantages: slightly lower ceiling accuracy than full BERT; still a
#   Transformer (quadratic attention cost); distillation requires either
#   using a pre-distilled checkpoint or running your own teacher-student
#   distillation process (compute-intensive one-time cost).
# Complexity: same per-layer cost as BERT, O(T^2*d), but half the layers.
# Follow-ups to expect:
#   - What is knowledge distillation? (train a smaller "student" model to
#     match a larger "teacher" model's output distribution/logits, not
#     just ground-truth hard labels — transfers "dark knowledge.")
#   - Why remove token_type_ids/NSP objective? (found to contribute little
#     to downstream performance; simplifies/speeds up pretraining.)
#   - When would you NOT use DistilBERT? (when squeezing out maximum
#     accuracy matters more than latency/size — use full BERT/RoBERTa.)
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Same head-swap variations as BERT template (binary/multi-label/NER/QA
#   via corresponding AutoModelFor* classes).
# Further compression: combine with quantization (INT8) or pruning for
#   even smaller/faster deployment.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: need most of BERT's accuracy at a fraction of the size/latency
#   — common production default when full BERT is overkill.
# Pros: smaller, faster, minimal accuracy loss vs BERT.
# Cons: slightly lower ceiling than BERT/RoBERTa, still quadratic attention.
# Time complexity: O(T^2*d) per layer x 6 layers (vs 12 for BERT-base).
# Space complexity: ~66M params (vs ~110M BERT-base).
# Common mistakes: assuming token_type_ids are needed (DistilBERT doesn't
#   use them); same LR/masking pitfalls as BERT fine-tuning.
# Production checklist: same as BERT template — save tokenizer with model,
#   consider further quantization for edge deployment, benchmark actual
#   latency gains vs BERT for your specific hardware/sequence lengths.
# ============================================================
