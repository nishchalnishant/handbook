"""
LLM USE CASE: Fine-tuning with LoRA (instruction following, domain chatbot)
Examples: customer support bot, code assistant on internal APIs, medical Q&A

WHY LoRA: train 0.1% of params → 1 GPU, minutes not days.
WHY instruction format: teaches model to follow user commands (Alpaca/ChatML template).
"""

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "meta-llama/Llama-3.2-1B"  # or "gpt2" for local demo without auth


def format_chat(example):
    """ChatML format — WHY: standard for modern chat models."""
    return {
        "text": (
            f"<|system|>\n{example.get('system', 'You are a helpful assistant.')}\n"
            f"<|user|>\n{example['instruction']}\n"
            f"<|assistant|>\n{example['output']}"
        )
    }


def train_lora(train_df, val_df):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
    )

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],  # Llama attention; use "c_attn" for GPT-2
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)

    train_ds = Dataset.from_pandas(train_df).map(format_chat)
    val_ds = Dataset.from_pandas(val_df).map(format_chat)
    train_ds = train_ds.map(lambda x: tokenizer(x["text"], truncation=True, max_length=512), batched=True)
    val_ds = val_ds.map(lambda x: tokenizer(x["text"], truncation=True, max_length=512), batched=True)

    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="./checkpoints/lora",
            per_device_train_batch_size=2,
            gradient_accumulation_steps=8,  # WHY: effective batch=16 on small GPU
            num_train_epochs=3,
            learning_rate=2e-4,
            fp16=torch.cuda.is_available(),
            logging_steps=10,
        ),
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )
    trainer.train()
    model.save_pretrained("./adapters/lora_adapter")
    return model, tokenizer
