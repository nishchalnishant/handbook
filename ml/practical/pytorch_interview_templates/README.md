# PyTorch Interview Templates

30 self-contained, runnable Python templates covering interview-scoped deep learning architectures, for AI Engineer (SDE-2) coding rounds.

## Shared conventions (apply to every file)

- No classes except where PyTorch's framework requires them. This is the key deviation from the sibling sklearn batch (`../sklearn_interview_templates/`), which has zero classes anywhere — PyTorch cannot avoid two APIs:
  - **`nn.Module` subclasses** — required for autograd, `.parameters()`, `.to(device)`, `state_dict()` to work. Every model definition stays a class.
  - **`torch.utils.data.Dataset` subclasses** — `DataLoader` depends on `__len__`/`__getitem__`. Custom dataset wrappers stay classes.
  - Both are flagged in-file with a one-line `# NOTE:` comment explaining why the exception exists.
- Everything else that used to be a class is a plain function/constant:
  - `Config` (dataclass or plain class) → top-level UPPER_CASE constants (`SEED`, `BATCH_SIZE`, `LR`, `EPOCHS`, checkpoint paths, etc.).
  - Stateful helpers like `EarlyStopping` → a `make_..._state() -> dict` constructor plus a `..._step(state, ...)` function that mutates the dict in place. Same pattern everywhere: `make_early_stopping_state()` / `early_stopping_step()`.
- Every file starts with the same-style "General Deep Learning Workflow (PyTorch)" numbered comment header (10 steps: understand data → split → prepare → build model → configure training → train → validate → improve → finalize → deploy/monitor).
- Reproducibility: `set_seed()` fixes `random`/`numpy`/`torch` (+ `cudnn.deterministic` where present). `get_device()` picks `cuda` > `mps` > `cpu`.
- Training loop conventions: AdamW (or Adam) optimizer, gradient clipping via `clip_grad_norm_`, optional AMP (`torch.autocast` + `GradScaler`), best-checkpoint-by-validation-metric (not last-epoch) saved via `torch.save`/loaded via `torch.load`.
- `main()` always falls back to synthetic data (`np.random.default_rng(SEED)`) shaped to exercise that architecture, so every file runs standalone with no external dataset or download required (except the two Hugging Face templates, which pull a pretrained checkpoint from the Hub on first run).
- Every file closes with four fixed comment blocks: **INTERVIEW EXPLANATION**, **VARIATIONS**, **PRODUCTION IMPROVEMENTS**, **SUMMARY**.
- Every file verified with `python3 -c "import ast; ast.parse(...)"` immediately after being written/edited.

## What actually differs file-to-file

1. Model architecture (the actual `nn.Module` subclass/subclasses) and its forward pass.
2. Synthetic data generator shape (tabular vectors, image tensors, token sequences, etc., tailored per architecture).
3. Task-specific training details (e.g. teacher forcing for seq2seq, masking for transformers, tokenizer usage for BERT/DistilBERT).
4. Content of the four closing comment blocks.

## Progress (30 total)

Foundations: 1 ANN/MLP ✅ · 2 CNN ✅ · 3 ResNet Transfer Learning ✅ · 4 EfficientNet Transfer Learning ✅ · 5 Vision Transformer ✅

Sequence models: 6 RNN ✅ · 7 LSTM ✅ · 8 GRU ✅ · 9 Seq2Seq ✅ · 10 Attention Mechanism ✅

Transformers: 11 Transformer Encoder ✅ · 12 Transformer Decoder ✅ · 13 Full Transformer ✅ · 14 BERT (HuggingFace) ✅ · 15 DistilBERT ✅

Remaining (16-30): RoBERTa · GPT · Time Series Forecasting · Autoencoder · VAE · GAN · DCGAN · U-Net · DeepLabV3 · Faster R-CNN · YOLO Inference · Multi-modal · Siamese Network · SimCLR · Custom Production Training Template

## Heads-up: things that deviate from the standard pattern

- **`nn.Module` and `Dataset` are the only classes** in the entire batch — everything else (Config, EarlyStopping-style helpers) is function/constant-based. This is intentionally different from the sklearn batch's "zero classes, full stop" rule, because these two are non-negotiable PyTorch framework APIs, not stylistic choices.
- **14 (BERT), 15 (DistilBERT)**: use Hugging Face `transformers` (`AutoModel`/`AutoTokenizer`), which requires a thin custom `nn.Module` wrapper (e.g. pretrained backbone + classification head) — still just one class, kept per the same nn.Module exception. These also download pretrained weights on first run rather than using a from-scratch synthetic-only model.
- **9 (Seq2Seq), 11-13 (Transformer encoder/decoder/full)**: often define *two or more* small `nn.Module` classes (e.g. separate Encoder/Decoder, or Encoder/Decoder/model wrapper) rather than one — all are kept as classes under the same framework-requirement rule, not a stylistic exception.
- **16-30 (upcoming)**: expect additional structural bends similar to the sklearn batch's later sections — GAN/DCGAN/VAE need generator+discriminator (or encoder+decoder) as multiple `nn.Module`s and a non-standard training loop (alternating updates); U-Net/DeepLabV3/Faster R-CNN/YOLO are segmentation/detection tasks with different evaluation metrics (IoU, mAP) instead of accuracy/F1; SimCLR/Siamese use contrastive losses and pair/triplet-based data pipelines instead of single-sample classification.

## Related paused work

A parallel Scikit-learn template batch (66 templates) lives in the sibling folder `../sklearn_interview_templates/`, at 13/66, paused while this PyTorch batch is being converted to its final no-classes convention. That batch has zero class exceptions (no framework forces one).
