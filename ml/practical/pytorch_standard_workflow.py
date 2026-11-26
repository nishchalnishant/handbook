"""
============================================================
PyTorch — Standard Workflow (supervised training, end-to-end)
============================================================
End-to-end pattern for training a neural net: build Dataset/DataLoader,
build a model, pick loss/optimizer/scheduler, run a train/val loop that
tracks the best checkpoint, then run inference with a reloaded model.

Pipeline:
  raw data -> Dataset/DataLoader -> model.to(device) -> loss + optimizer
  + scheduler -> per-epoch (train pass with backward/step, val pass with
  no_grad) -> track best val metric -> save best checkpoint -> reload
  for inference

WHY this loop structure:
  - model.train()/model.eval() toggle Dropout/BatchNorm behavior — running
    the wrong mode silently corrupts either training or evaluation.
  - optimizer.zero_grad() must run every step or gradients accumulate
    across batches (that IS a real technique for grad accumulation, but
    by default it's a bug).
  - torch.no_grad() during validation avoids building an autograd graph
    you'll never call .backward() on — pure memory/compute waste otherwise.
  - Saving the best-val checkpoint (not the last epoch) guards against
    overfitting in later epochs silently degrading the deployed model.

# ============================================================
# Standard Workflow
# ============================================================
# 1. Data       — Dataset + DataLoader (train/val split, transforms)
# 2. Model      — build_model(...) -> nn.Module / nn.ModuleDict
# 3. Loss/Optim — criterion, optimizer, optional LR scheduler
# 4. Train loop — per epoch: train pass (backward+step), val pass (no_grad)
# 5. Checkpoint — save state_dict whenever val metric improves
# 6. Inference  — reload state_dict, model.eval(), no_grad forward pass
# ============================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, random_split

# pip install torch torchvision
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
INPUT_DIM = 20
HIDDEN_DIM = 64
NUM_CLASSES = 3
BATCH_SIZE = 32
NUM_EPOCHS = 5
LR = 1e-3
CHECKPOINT_PATH = "best_model.pt"


# ------------------------------------------------------------
# APPROACH A: From-scratch — Dataset + functional model (no nn.Module subclass)
# ------------------------------------------------------------
class TensorLabelDataset(Dataset):
    """Minimal Dataset — swap for torchvision.datasets.ImageFolder etc. in real use."""

    def __init__(self, X: torch.Tensor, y: torch.Tensor):
        self.X, self.y = X, y

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, idx: int):
        return self.X[idx], self.y[idx]


def build_model(input_dim: int, hidden_dim: int, num_classes: int) -> nn.ModuleDict:
    return nn.ModuleDict({
        "fc1": nn.Linear(input_dim, hidden_dim),
        "bn1": nn.BatchNorm1d(hidden_dim),
        "fc2": nn.Linear(hidden_dim, num_classes),
        "dropout": nn.Dropout(0.3),
    })


def forward_model(m: nn.ModuleDict, x: torch.Tensor) -> torch.Tensor:
    x = F.relu(m["bn1"](m["fc1"](x)))
    x = m["dropout"](x)
    return m["fc2"](x)


def train_one_epoch(m: nn.ModuleDict, loader: DataLoader, optimizer, criterion) -> float:
    m.train()
    running_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(DEVICE), yb.to(DEVICE)
        optimizer.zero_grad()
        logits = forward_model(m, xb)
        loss = criterion(logits, yb)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * xb.size(0)
    return running_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(m: nn.ModuleDict, loader: DataLoader) -> float:
    m.eval()
    correct = 0
    for xb, yb in loader:
        xb, yb = xb.to(DEVICE), yb.to(DEVICE)
        logits = forward_model(m, xb)
        correct += (logits.argmax(1) == yb).sum().item()
    return correct / len(loader.dataset)


# ------------------------------------------------------------
# APPROACH B: Production pattern — torchvision transfer learning
# ------------------------------------------------------------
# from torchvision import datasets, transforms, models
#
# train_tf = transforms.Compose([
#     transforms.RandomResizedCrop(224),
#     transforms.RandomHorizontalFlip(),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
# ])
# train_ds = datasets.ImageFolder("data/train", transform=train_tf)
# train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=4)
#
# model = models.resnet18(weights="DEFAULT")
# model.fc = nn.Linear(model.fc.in_features, num_classes)   # only task-specific layer
# model.to(DEVICE)
# optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)  # feature extraction: freeze backbone


# ------------------------------------------------------------
# APPROACH C: Advanced patterns (mention verbally, not exercised in main())
# ------------------------------------------------------------
# Discriminative LRs (fine-tuning, lower LR for earlier layers):
#   optimizer = torch.optim.Adam([
#       {"params": model.layer1.parameters(), "lr": 1e-5},
#       {"params": model.fc.parameters(),     "lr": 1e-3},
#   ])
#
# Mixed precision (AMP) — faster training on modern GPUs:
#   scaler = torch.cuda.amp.GradScaler()
#   with torch.cuda.amp.autocast():
#       loss = criterion(forward_model(m, xb), yb)
#   scaler.scale(loss).backward(); scaler.step(optimizer); scaler.update()
#
# Gradient clipping — guards against exploding gradients (RNNs/Transformers):
#   torch.nn.utils.clip_grad_norm_(m.parameters(), max_norm=1.0)
#
# DistributedDataParallel — multi-GPU, one process per GPU (preferred over
# DataParallel): torchrun --nproc_per_node=N train.py, wrap model in DDP.
#
# LR scheduler:
#   scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)
#   scheduler.step()   # call once per epoch, after optimizer.step() calls


def _make_demo_data(n=1000):
    torch.manual_seed(42)
    X = torch.randn(n, INPUT_DIM)
    y = torch.randint(0, NUM_CLASSES, (n,))
    return TensorLabelDataset(X, y)


def main() -> None:
    # 1. Data
    dataset = _make_demo_data()
    train_ds, val_ds = random_split(dataset, [800, 200], generator=torch.Generator().manual_seed(42))
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    # 2. Model
    model = build_model(INPUT_DIM, HIDDEN_DIM, NUM_CLASSES).to(DEVICE)

    # 3. Loss / optimizer / scheduler
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

    # 4. Train / validate loop, tracking best checkpoint
    best_acc = 0.0
    for epoch in range(NUM_EPOCHS):
        train_loss = train_one_epoch(model, train_loader, optimizer, criterion)
        scheduler.step()
        val_acc = evaluate(model, val_loader)
        print(f"epoch {epoch}: train_loss={train_loss:.4f} val_acc={val_acc:.4f}")

        # 5. Checkpoint
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), CHECKPOINT_PATH)

    # 6. Inference with reloaded best checkpoint
    model.load_state_dict(torch.load(CHECKPOINT_PATH))
    model.eval()
    with torch.no_grad():
        sample = dataset.X[:1].to(DEVICE)
        pred_class = forward_model(model, sample).argmax(1).item()
    print("Sample prediction:", pred_class)


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use this workflow:
#   - Any supervised training task (classification/regression) — the
#     standard "train a model end-to-end" interview ask.
#
# nn.Module subclass vs. this ModuleDict/forward-function style:
#   - Functionally identical; this repo's convention keeps state
#     (build_model) and computation (forward_model) as separate,
#     independently testable functions rather than bundled in a class.
#
# Critical failure modes (diagnose -> fix):
#   - Loss is nan/inf -> lower LR, check for log(0), clip gradients,
#     check inputs for NaN, disable AMP to isolate.
#   - Loss never decreases -> verify optimizer.zero_grad() runs every step,
#     labels aren't misaligned with inputs, LR isn't absurdly small/large.
#   - Val accuracy ~ random guessing -> model.eval() not set (BatchNorm/
#     Dropout still in train-mode behavior during evaluation).
#   - "expected all tensors on same device" -> a tensor created inside
#     forward (e.g. torch.zeros(...)) without device=... .
#   - Great train, poor val -> overfitting: add dropout/weight_decay/
#     augmentation, reduce capacity, early stop on best val checkpoint.
#
# Metrics:
#   - Classification: accuracy, F1 (macro for imbalanced classes).
#   - Track train_loss AND val_acc/val_loss every epoch — a gap growing
#     over epochs is the overfitting signal that justifies early stopping.
#
# ============================================================
# VARIATIONS
# ============================================================
# - Transfer learning: swap build_model for a pretrained torchvision model,
#   freeze backbone first (feature extraction), optionally unfreeze with
#   discriminative LRs for fine-tuning (see APPROACH B/C above).
# - Sequence models: batch_first=True on RNN/LSTM/Transformer layers,
#   watch for shape mismatches at the Linear boundary.
# - Mixed precision: wrap forward+loss in torch.cuda.amp.autocast() and use
#   GradScaler when training on GPU at scale.
# - Multi-GPU: DistributedDataParallel (preferred) over DataParallel.
#
# ============================================================
# SUMMARY
# ============================================================
# - Use when: standard supervised training loop for any nn.Module-based model.
# - Key decisions: model.train()/eval() toggling, zero_grad() every step,
#   no_grad() during validation, checkpoint on best val metric not last epoch.
# - Key failure modes: nan losses, device mismatches, eval-mode forgotten,
#   overfitting undetected because only the last-epoch model was saved.
# - Evaluation: per-epoch val pass under no_grad(), best-checkpoint selection.
# - Production stack: state_dict() checkpointing, reload + .eval() + no_grad()
#   for inference; DDP + AMP for scaled training.
# - Common mistakes: forgetting optimizer.zero_grad(), mismatched
#   batch_first, evaluating in train() mode, no gradient clipping on RNNs.
