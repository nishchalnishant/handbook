# Interview ML/DL/LLM Cheat Sheet

## Folder map

| Folder | Files | Covers |
|--------|-------|--------|
| `ml/` | 01 regression, 02 classification, 03 imbalanced, 04 FastAPI serving | Tabular sklearn end-to-end + serving |
| `dl/` | 00 MLP regression, 01 CNN, 02 classification, 03 imbalanced (weighted loss + focal), 04 LSTM NLP, 05 seq2seq, 06 time series, 07 autoencoder, 08 GAN, 09 tabular MLP, 10 FastAPI serving | PyTorch vision + tabular + imbalance |
| `llm/` | 00 text regression, 00 imbalanced, 01 classification, 02 NER, 03 summarization, 04 generation LoRA, 05 RAG, 06 LoRA, 07 agents, 08 function calling, 09 MCP, 10 prompt engineering, 11 RAGAS eval, 12 FastAPI serving | HuggingFace + PEFT + production |

## End-to-end flow (say this out loud in interviews)

1. **Problem framing** — regression vs classification? metric? business cost of FP vs FN?
2. **EDA** — missing values, leakage, class balance, feature types
3. **Train/val/test split** — stratify for classification; time-based split for temporal data
4. **Preprocessing inside Pipeline** — fit on train only
5. **Baseline model** — linear/logistic first, then boost trees / neural net
6. **Evaluate** — right metric (MAE, F1, PR-AUC for imbalance)
7. **Tune** — hyperparams + threshold (imbalanced)
8. **Serialize** — joblib / torch.save / save_pretrained
9. **Serve** — FastAPI, health check, batch inference, monitoring

## Model selection quick reference

| Scenario | First choice | Why |
|----------|-------------|-----|
| Tabular regression | XGBoost / LightGBM | SOTA on structured data |
| Tabular classification | XGBoost / Logistic | interpretable baseline → strong model |
| Imbalanced tabular | class_weight + PR-AUC | accuracy lies |
| Image classification | ResNet + transfer learning | needs less data |
| Text classification | DistilBERT fine-tune | fast, accurate, cheap inference |
| Text generation | Llama + LoRA | full fine-tune too expensive |
| High-throughput LLM | vLLM + quantization | production scale |

## Key imports to memorize

```python
# ML
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import f1_score, mean_absolute_error, average_precision_score
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
import joblib

# DL
import torch, torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models

# LLM
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import Dataset
```

## Install

```bash
pip install -r requirements.txt
```
