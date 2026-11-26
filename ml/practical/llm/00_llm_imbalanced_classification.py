"""
LLM IMBALANCED TEXT CLASSIFICATION — rare classes in text (fraud, abuse, rare intent)
Examples: 1% toxic comments, 0.5% fraud support tickets, 3% churn signals.

WHY class weights in loss: don't change data; penalize mistakes on minority harder.
WHY weighted sampling: each batch sees balanced mix (alternative/complement to weighted loss).
WHY F1-macro + PR-AUC for selection: accuracy lies at 99/1 splits.
WHY tune decision threshold post-training: default 0.5 is wrong for imbalanced.
"""

import numpy as np
import torch
import torch.nn as nn
from datasets import Dataset
from sklearn.metrics import (
    classification_report,
    f1_score,
    precision_recall_curve,
    precision_recall_fscore_support,
    roc_auc_score,
    average_precision_score,
)
from sklearn.utils.class_weight import compute_class_weight
from torch.utils.data import WeightedRandomSampler
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "distilbert-base-uncased"
MAX_LENGTH = 128


# --- 1. WEIGHTED TRAINER (custom loss) ---
class WeightedTrainer(Trainer):
    """
    WHY custom Trainer: HF's default computes CrossEntropyLoss with no class weights.
    We override compute_loss to inject per-class weights for the loss term.
    """

    def __init__(self, *args, class_weights: torch.Tensor | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        # WHY weight=class_weights: each class contributes to loss proportional to its weight
        loss = nn.functional.cross_entropy(
            logits, labels, weight=self.class_weights
        )
        return (loss, outputs) if return_outputs else loss


# --- 2. METRICS (focus on minority class) ---
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    probs = torch.softmax(torch.tensor(logits), dim=-1)[:, -1].numpy()
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average="macro", zero_division=0)
    return {
        "f1_macro": f1,                    # WHY macro: equal weight per class
        "precision_macro": p,
        "recall_macro": r,
        "pr_auc": float(average_precision_score(labels, probs)),
        "roc_auc": float(roc_auc_score(labels, probs)),
    }


# --- 3. STRATEGY A: weighted loss ---
def get_class_weights(labels: np.ndarray) -> torch.Tensor:
    """
    WHY 'balanced' formula: weight_c = N / (n_classes * count_c)
    Inverse frequency → minority class gets higher loss contribution.
    """
    classes = np.unique(labels)
    weights = compute_class_weight("balanced", classes=classes, y=labels)
    return torch.tensor(weights, dtype=torch.float32)


def train_with_weighted_loss(train_df, val_df, text_col="text", label_col="label"):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    num_labels = int(max(train_df[label_col].max(), val_df[label_col].max()) + 1)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=num_labels)

    train_ds = Dataset.from_pandas(train_df).map(
        lambda x: tokenizer(x[text_col], truncation=True, max_length=MAX_LENGTH), batched=True
    )
    val_ds = Dataset.from_pandas(val_df).map(
        lambda x: tokenizer(x[text_col], truncation=True, max_length=MAX_LENGTH), batched=True
    )

    class_weights = get_class_weights(train_df[label_col].values)

    trainer = WeightedTrainer(
        class_weights=class_weights,
        model=model,
        args=TrainingArguments(
            output_dir="./checkpoints/imbalanced_weighted",
            eval_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            num_train_epochs=3,
            load_best_model_at_end=True,
            metric_for_best_model="f1_macro",
            fp16=torch.cuda.is_available(),
        ),
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model("./models/text_classifier_imbalanced")
    tokenizer.save_pretrained("./models/text_classifier_imbalanced")
    return trainer


# --- 4. STRATEGY B: weighted sampler (custom loop, not Trainer) ---
def make_weighted_sampler(labels: np.ndarray) -> WeightedRandomSampler:
    """
    WHY sampler: each batch sees proportional minority examples without duplicating data.
    Combine EITHER weighted loss OR weighted sampler — not both (over-correction).
    """
    class_counts = np.bincount(labels)
    class_weights = 1.0 / class_counts
    sample_weights = class_weights[labels]
    return WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)


# --- 5. THRESHOLD TUNING (do this AFTER training for the imbalanced scenario) ---
def find_best_threshold(y_true: np.ndarray, y_proba: np.ndarray, metric: str = "f1"):
    """
    WHY tune threshold: default 0.5 assumes equal class prior; minority needs lower threshold.
    Fraud/abuse use-cases often pick threshold that hits a target recall (catch most bad cases).
    """
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_proba)
    # NOTE: precision_recall_curve returns one more threshold than preds; align safely:
    best_t, best_score = 0.5, -1
    for t in thresholds:
        preds = (y_proba >= t).astype(int)
        if metric == "f1":
            score = f1_score(y_true, preds, zero_division=0)
        else:
            score = f1_score(y_true, preds, zero_division=0)  # default
        if score > best_score:
            best_score, best_t = score, float(t)
    print(f"Best threshold: {best_t:.3f}, F1={best_score:.3f}")
    return best_t, best_score


# --- 6. POST-TRAIN EVAL HELPER ---
def evaluate_with_threshold(trainer, val_df, text_col="text", label_col="label"):
    """Run predictions, then tune threshold on validation probs."""
    tokenizer = AutoTokenizer.from_pretrained(trainer.state.best_model_checkpoint)
    import torch
    texts = val_df[text_col].tolist()
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=MAX_LENGTH)
    inputs = {k: v.to(trainer.model.device) for k, v in inputs.items()}
    with torch.no_grad():
        logits = trainer.model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)[:, -1].cpu().numpy()
    y_true = val_df[label_col].values

    best_t, best_f1 = find_best_threshold(y_true, probs)
    y_pred = (probs >= best_t).astype(int)
    print(classification_report(y_true, y_pred, zero_division=0))
    return best_t, best_f1


if __name__ == "__main__":
    pass
