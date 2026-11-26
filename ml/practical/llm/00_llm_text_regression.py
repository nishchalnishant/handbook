"""
LLM TEXT REGRESSION — predict a continuous score from text
Use when: review rating, essay score, support ticket priority, NPS from comment.

WHY reuse AutoModel + regression head: same tokenizer pipeline as classification,
just swap the head from N-way softmax to 1 linear unit.
WHY MSE loss: standard for continuous targets; L1 (MAE) is alternative if heavy-tailed.
WHY DistilBERT base: small enough for interview laptops, strong enough for real demos.
WHY freeze lower layers (optional): reduces overfitting on small labeled text datasets.
"""

import numpy as np
import torch
import torch.nn as nn
from datasets import Dataset
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from transformers import (
    AutoModel,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "distilbert-base-uncased"
MAX_LENGTH = 256


# --- 1. CUSTOM MODEL (encoder + regression head) ---
class TextRegressor(nn.Module):
    """
    WHY AutoModel (not AutoModelForSequenceClassification): we need a 1-dim regression head,
    not a classification head. We attach our own linear layer on top of [CLS] pooled output.
    """

    def __init__(self, model_name: str = MODEL_NAME, dropout: float = 0.1):
        super().__init__()
        self.backbone = AutoModel.from_pretrained(model_name)
        hidden = self.backbone.config.hidden_size
        self.dropout = nn.Dropout(dropout)
        # WHY 1 output neuron: predicts one continuous number
        self.regressor = nn.Linear(hidden, 1)

    def forward(self, input_ids, attention_mask, labels=None):
        # WHY [CLS] token (index 0): pooled sentence representation by convention
        pooled = self.backbone(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:, 0]
        logits = self.regressor(self.dropout(pooled)).squeeze(-1)
        loss = None
        if labels is not None:
            # WHY MSELoss: smooth, well-behaved gradients for continuous targets
            loss = nn.functional.mse_loss(logits, labels.float())
        return {"loss": loss, "logits": logits}


# --- 2. TOKENIZATION + METRICS ---
def tokenize(batch, tokenizer):
    return tokenizer(batch["text"], truncation=True, max_length=MAX_LENGTH)


def compute_metrics(eval_pred):
    preds, labels = eval_pred
    preds = np.asarray(preds).ravel()
    labels = np.asarray(labels).ravel()
    return {
        "mae": float(mean_absolute_error(labels, preds)),
        "rmse": float(np.sqrt(mean_squared_error(labels, preds))),
        "r2": float(r2_score(labels, preds)),
    }


# --- 3. TRAIN ---
def train(train_df, val_df, text_col: str = "text", target_col: str = "score"):
    """
    train_df/val_df: pandas DataFrames with text_col (str) and target_col (float).
    """
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = TextRegressor(MODEL_NAME)

    train_ds = Dataset.from_pandas(train_df[[text_col, target_col]]).map(
        lambda x: tokenize(x, tokenizer), batched=True
    )
    val_ds = Dataset.from_pandas(val_df[[text_col, target_col]]).map(
        lambda x: tokenize(x, tokenizer), batched=True
    )

    # WHY rename target column to 'labels': Trainer auto-feeds 'labels' into model.forward
    train_ds = train_ds.rename_column(target_col, "labels")
    val_ds = val_ds.rename_column(target_col, "labels")

    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="./checkpoints/text_regression",
            eval_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            num_train_epochs=3,
            load_best_model_at_end=True,
            metric_for_best_model="rmse",  # WHY RMSE: matches production SLA style metric
            greater_is_better=False,        # WHY False: lower RMSE is better
            fp16=torch.cuda.is_available(),
        ),
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model("./models/text_regressor")
    tokenizer.save_pretrained("./models/text_regressor")
    return trainer


# --- 4. INFERENCE ---
def predict_score(text: str, model_path: str = "./models/text_regressor") -> float:
    from transformers import AutoModel
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = TextRegressor(model_path)
    model.load_state_dict(torch.load(f"{model_path}/model.safetensors", map_location="cpu"))
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=MAX_LENGTH)
    with torch.no_grad():
        out = model(**inputs)
    return float(out["logits"].cpu().numpy()[0])


if __name__ == "__main__":
    pass
