"""
LLM USE CASE: Summarization
Examples: meeting notes, news digests, legal document summaries

WHY seq2seq models (BART/T5/PEGASUS): encoder reads doc, decoder writes summary.
WHY PEGASUS for news: pretrained with gap-sentence generation objective.
WHY max_length limits: control cost and prevent rambling outputs.
"""

import torch
from datasets import Dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

MODEL_NAME = "facebook/bart-large-cnn"  # alt: "google/pegasus-xsum", "t5-small"
MAX_INPUT = 1024
MAX_TARGET = 128


def preprocess(batch, tokenizer):
    inputs = tokenizer(batch["document"], max_length=MAX_INPUT, truncation=True)
    labels = tokenizer(text_target=batch["summary"], max_length=MAX_TARGET, truncation=True)
    inputs["labels"] = labels["input_ids"]
    return inputs


def train(train_df, val_df, doc_col="document", summary_col="summary"):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    train_ds = Dataset.from_pandas(train_df).map(lambda x: preprocess(x, tokenizer), batched=True)
    val_ds = Dataset.from_pandas(val_df).map(lambda x: preprocess(x, tokenizer), batched=True)

    trainer = Seq2SeqTrainer(
        model=model,
        args=Seq2SeqTrainingArguments(
            output_dir="./checkpoints/summarization",
            eval_strategy="epoch",
            learning_rate=3e-5,
            per_device_train_batch_size=4,
            num_train_epochs=3,
            predict_with_generate=True,  # WHY: eval with actual generation, not teacher forcing
            fp16=torch.cuda.is_available(),
        ),
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    )
    trainer.train()
    trainer.save_model("./models/summarizer")
    return trainer


def summarize(text: str, model_path="./models/summarizer", max_length=128):
    from transformers import pipeline
    summarizer = pipeline("summarization", model=model_path, tokenizer=model_path)
    return summarizer(text, max_length=max_length, min_length=30, do_sample=False)[0]["summary_text"]
