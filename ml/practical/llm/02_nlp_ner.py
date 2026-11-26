"""
LLM USE CASE: Named Entity Recognition (NER)
Examples: extract person/org/date from contracts, medical records, resumes

WHY token classification: each token gets a label (B-PER, I-PER, O).
WHY BIO tagging: B=beginning, I=inside, O=outside entity.
Model: bert-base-cased or dslim/bert-base-NER for pretrained head.
"""

import numpy as np
import torch
from datasets import Dataset
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    DataCollatorForTokenClassification,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "bert-base-cased"
LABEL_LIST = ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-DATE", "I-DATE"]
LABEL2ID = {l: i for i, l in enumerate(LABEL_LIST)}
ID2LABEL = {i: l for l, i in LABEL2ID.items()}


def tokenize_and_align_labels(examples, tokenizer):
    """
    WHY align labels: WordPiece splits "Apple" → "App"+"##le"; only first subtoken gets label.
    """
    tokenized = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
    labels = []
    for i, label_ids in enumerate(examples["ner_tags"]):
        word_ids = tokenized.word_ids(batch_index=i)
        aligned = []
        prev_word = None
        for word_id in word_ids:
            if word_id is None:
                aligned.append(-100)  # WHY -100: Trainer ignores these positions
            elif word_id != prev_word:
                aligned.append(label_ids[word_id])
            else:
                aligned.append(-100)  # subword token → ignore
            prev_word = word_id
        labels.append(aligned)
    tokenized["labels"] = labels
    return tokenized


def train(train_data, val_data):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForTokenClassification.from_pretrained(
        MODEL_NAME, num_labels=len(LABEL_LIST), id2label=ID2LABEL, label2id=LABEL2ID
    )

    train_ds = Dataset.from_list(train_data).map(lambda x: tokenize_and_align_labels(x, tokenizer), batched=True)
    val_ds = Dataset.from_list(val_data).map(lambda x: tokenize_and_align_labels(x, tokenizer), batched=True)

    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="./checkpoints/ner",
            eval_strategy="epoch",
            learning_rate=3e-5,
            per_device_train_batch_size=16,
            num_train_epochs=5,
        ),
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        data_collator=DataCollatorForTokenClassification(tokenizer),
    )
    trainer.train()
    trainer.save_model("./models/ner")
    return trainer


def predict_ner(text: str, model_path="./models/ner"):
    from transformers import pipeline
    return pipeline("ner", model=model_path, tokenizer=model_path, aggregation_strategy="simple")(text)
