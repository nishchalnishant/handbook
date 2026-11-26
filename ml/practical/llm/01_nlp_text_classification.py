"""
LLM USE CASE: Text Classification (sentiment, intent, spam, ticket routing)
WHY DistilBERT: 40% smaller than BERT, 60% faster, ~97% accuracy.
WHY fine-tune vs zero-shot: domain labels (e.g. "Billing", "Tech Support") need training.
"""

import numpy as np
import torch
from datasets import Dataset
from sklearn.metrics import f1_score, precision_recall_fscore_support
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "distilbert-base-uncased"
MAX_LENGTH = 128


def tokenize(batch, tokenizer):
    return tokenizer(batch["text"], truncation=True, max_length=MAX_LENGTH)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average="weighted")
    return {"f1": f1, "precision": p, "recall": r}


def train(train_df, val_df, text_col="text", label_col="label", num_labels=2):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=num_labels)

    train_ds = Dataset.from_pandas(train_df).map(lambda x: tokenize(x, tokenizer), batched=True)
    val_ds = Dataset.from_pandas(val_df).map(lambda x: tokenize(x, tokenizer), batched=True)

    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="./checkpoints/text_classification",
            eval_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            num_train_epochs=3,
            load_best_model_at_end=True,
            metric_for_best_model="f1",
            fp16=torch.cuda.is_available(),
        ),
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model("./models/text_classifier")
    return trainer


def predict(text: str, model_path="./models/text_classifier"):
    from transformers import pipeline
    return pipeline("text-classification", model=model_path, tokenizer=model_path)(text)
