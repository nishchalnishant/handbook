"""Core: BERT fine-tuning for classification — [CLS] pooled output -> dropout -> linear.
Same pattern applies to DistilBERT/RoBERTa (see 15/16): just swap the AutoModel name.

INTERVIEW GUIDE
----------------
Typical ask: "Fine-tune a pretrained transformer for text classification."
Almost never asked to write BERT from scratch in an hour — the point of
this question is testing HF API fluency and fine-tuning judgment, not
attention-mechanism internals (that's file 10/11's job).

Expected depth (1hr session):
  - Junior/mid: load AutoModel, add a classification head, get forward()
    shapes right, explain what attention_mask does.
  - Senior: also asked to justify freeze_backbone choice, discuss
    discriminative learning rates / gradual unfreezing, explain why
    [CLS] pooling vs mean-pooling vs pooler_output, and handle
    train/eval mode + dropout correctly under a data-scarce scenario.
  Usually 20-30 min of the hour; commonly paired with a discussion of
  training loop / class imbalance / small dataset strategy afterward.

Common follow-ups:
  - "Why index [:, 0, :] instead of using outputs.pooler_output?" (pooler
    adds an extra dense+tanh trained on NSP; raw [CLS] hidden state is
    often preferred and more transparent for a classifier head).
  - "When would you freeze the backbone vs fine-tune the whole thing?"
    (freeze on small datasets / to avoid catastrophic forgetting, or as
    fast baseline; full fine-tune when enough labeled data and compute).
  - "What's the difference between attention_mask and token_type_ids?"
  - "How would you handle a sequence longer than the model's max length?"
    (truncate, or use a sliding window / hierarchical approach).
  - "Why BERT over DistilBERT here?" (distillation tradeoff: ~40% smaller,
    ~60% faster, ~97% of performance).
  - "How do you avoid overfitting when fine-tuning on a small dataset?"
    (freeze more layers, lower LR, dropout, early stopping, fewer epochs).

Gotchas to mention proactively:
  - Forgetting model.eval() before inference leaves the classifier's
    dropout active, adding noise to predictions.
  - Freezing the backbone but forgetting to exclude frozen params from the
    optimizer wastes memory on unused gradient state (still correct, just
    inefficient) — mention passing only trainable params to the optimizer.
  - Tokenizer and model must match (wrong tokenizer/model_name pairing
    silently produces garbage, not an error).
"""

from torch import nn, Tensor
from transformers import AutoModel


def build_model(model_name: str, num_classes: int, freeze_backbone: bool) -> nn.ModuleDict:
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
    cls_output = outputs.last_hidden_state[:, 0, :]
    return m["classifier"](m["dropout"](cls_output))


if __name__ == "__main__":
    import torch
    m = build_model("bert-base-uncased", num_classes=2, freeze_backbone=True)
    input_ids = torch.randint(0, 1000, (2, 16))
    attention_mask = torch.ones(2, 16, dtype=torch.long)
    print(forward_bert(m, input_ids, attention_mask).shape)  # (2, 2)
