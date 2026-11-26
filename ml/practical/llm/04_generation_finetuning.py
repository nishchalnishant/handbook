"""
LLM GENERATION FINE-TUNING — Q&A, summarization, instruction following
Use when: custom chatbot, document Q&A, summarization on domain data.

WHY LoRA/PEFT: train 0.1% of params → fits on 1 GPU, faster iteration (strong interview answer).
WHY causal LM (GPT-style) not BERT: generation requires autoregressive decoding.
"""

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

# Smaller model for interview demo — mention Llama-3-8B in real prod
MODEL_NAME = "gpt2"  # or "meta-llama/Llama-3.2-1B" with HF token


def format_instruction(example):
    """
    WHY instruction template: teaches model input→output structure (Alpaca/ChatML format).
    """
    return {
        "text": f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"
    }


def train_generative(train_df, val_df):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token  # WHY: GPT-2 has no pad token by default

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
    )

    # --- LoRA CONFIG ---
    # WHY LoRA: low-rank adapters on attention layers — 100x less memory than full fine-tune
    lora_config = LoraConfig(
        r=16,                    # rank — higher = more capacity, more params
        lora_alpha=32,
        target_modules=["c_attn"],  # GPT-2 attention; use q_proj/v_proj for Llama
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()  # show ~0.1% trainable in interview

    train_ds = Dataset.from_pandas(train_df).map(format_instruction)
    val_ds = Dataset.from_pandas(val_df).map(format_instruction)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=512)

    train_ds = train_ds.map(tokenize, batched=True)
    val_ds = val_ds.map(tokenize, batched=True)

    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    # WHY mlm=False: causal LM predicts next token, not masked tokens (that's BERT)

    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="./checkpoints_generation",
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,  # WHY: simulate larger batch on small GPU
            num_train_epochs=3,
            learning_rate=2e-4,             # WHY higher LR for LoRA vs full fine-tune (2e-5)
            fp16=torch.cuda.is_available(),
            logging_steps=10,
            save_strategy="epoch",
        ),
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=collator,
    )

    trainer.train()

    # WHY save_adapter only: small files, swap adapters per task
    model.save_pretrained("./lora_adapter")
    tokenizer.save_pretrained("./lora_adapter")
    return model, tokenizer


def generate(model, tokenizer, instruction: str, max_new_tokens=128):
    prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


if __name__ == "__main__":
    pass
