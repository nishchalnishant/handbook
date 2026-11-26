"""
============================================================
TEMPLATE 1: Artificial Neural Network (ANN) / MLP
============================================================
Tabular data classification (multi-class).
Interview-scoped: core workflow only; production extras
noted as comments, not code.
============================================================

# ============================================================
# General Deep Learning Workflow (PyTorch)
# ============================================================
# 1. Understand the Data
#    - Load the dataset
#    - Perform EDA
#    - Identify the target variable
#    - Check missing values, duplicates, outliers, class imbalance
# 2. Split the Data
#    - Train / Validation / Test split (stratified for classification)
# 3. Prepare the Data
#    - Scale features (fit only on train to avoid leakage)
#    - Wrap in Dataset + DataLoader
# 4. Build the Model
#    - Define nn.Module, move to device
# 5. Configure Training
#    - Loss function, optimizer, (optional) scheduler
# 6. Train the Model
#    - Train loop: zero_grad -> forward -> loss -> backward -> step
# 7. Validate + Early Stopping
#    - Evaluate on val set each epoch; checkpoint best model
# 8. Test Evaluation
#    - Evaluate once on held-out test set
# 9. Inference
#    - model.eval() + torch.no_grad()
# ============================================================
"""

import random

import numpy as np
import torch
from torch import nn, Tensor
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
SEED = 42
INPUT_DIM = 20       # number of input features
NUM_CLASSES = 3      # number of output classes
HIDDEN_DIMS = (128, 64, 32)
DROPOUT = 0.3
BATCH_SIZE = 64
EPOCHS = 50
LR = 1e-3
WEIGHT_DECAY = 1e-4
PATIENCE = 5
CKPT_PATH = "checkpoints/ann_best.pt"


# ------------------------------------------------------------
# Reproducibility + device
# ------------------------------------------------------------
def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():   # Apple Silicon
        return torch.device("mps")
    return torch.device("cpu")


# ------------------------------------------------------------
# Data preparation
# ------------------------------------------------------------
def make_tensor_dataset(X: np.ndarray, y: np.ndarray) -> TensorDataset:
    """Convert numpy arrays to a PyTorch TensorDataset (built-in; no custom class needed).
    TensorDataset wraps tensors and implements __len__/__getitem__ for DataLoader."""
    return TensorDataset(
        torch.as_tensor(X, dtype=torch.float32),
        torch.as_tensor(y, dtype=torch.long),   # long required by CrossEntropyLoss
    )


def build_dataloaders(X: np.ndarray, y: np.ndarray) -> tuple[DataLoader, DataLoader, DataLoader, StandardScaler]:
    """Stratified split -> scale -> DataLoaders.
    Fit scaler ONLY on train to avoid leakage (common interview pitfall)."""
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=SEED
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=SEED
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val   = scaler.transform(X_val)
    X_test  = scaler.transform(X_test)

    train_loader = DataLoader(make_tensor_dataset(X_train, y_train), batch_size=BATCH_SIZE, shuffle=True)
    val_loader   = DataLoader(make_tensor_dataset(X_val, y_val),     batch_size=BATCH_SIZE, shuffle=False)
    test_loader  = DataLoader(make_tensor_dataset(X_test, y_test),   batch_size=BATCH_SIZE, shuffle=False)
    return train_loader, val_loader, test_loader, scaler


# ------------------------------------------------------------
# Model (no class needed: nn.Sequential is a plain factory function call)
# ------------------------------------------------------------
def build_model(input_dim: int, hidden_dims: tuple[int, ...], num_classes: int, dropout: float) -> nn.Sequential:
    """Build a feedforward MLP using nn.Sequential — no nn.Module subclass needed
    for a simple linear stack. Returns an nn.Module-compatible object that supports
    .parameters(), .state_dict(), .train()/.eval(), etc.

    Block: Linear -> BatchNorm -> ReLU -> Dropout (repeated per hidden layer).
    Why BatchNorm: normalizes layer inputs, stabilizes/accelerates training.
    Why ReLU: avoids vanishing gradients (vs sigmoid/tanh), cheap to compute.
    Why Dropout: regularizes to prevent overfitting on tabular data.
    No activation on final layer: CrossEntropyLoss expects raw logits.

    Shape trace (B=batch, input=20, hidden=(128,64,32), classes=3):
        input:   (B, 20)
        layer1:  (B, 128)
        layer2:  (B, 64)
        layer3:  (B, 32)
        logits:  (B, 3)
    """
    layers: list[nn.Module] = []
    prev_dim = input_dim
    for h in hidden_dims:
        layers.extend([
            nn.Linear(prev_dim, h),
            nn.BatchNorm1d(h),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
        ])
        prev_dim = h
    layers.append(nn.Linear(prev_dim, num_classes))
    return nn.Sequential(*layers)


# ------------------------------------------------------------
# Train / validate
# ------------------------------------------------------------
def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device) -> tuple[float, float, float]:
    """Returns (loss, accuracy, macro_f1).
    model.eval() disables Dropout + switches BatchNorm to running stats."""
    model.eval()
    total_loss = 0.0
    all_preds, all_targets = [], []
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = model(xb)
        total_loss += criterion(logits, yb).item() * xb.size(0)
        all_preds.append(logits.argmax(1).cpu())
        all_targets.append(yb.cpu())
    all_preds   = torch.cat(all_preds).numpy()
    all_targets = torch.cat(all_targets).numpy()
    n = len(loader.dataset)
    acc = accuracy_score(all_targets, all_preds)
    f1  = f1_score(all_targets, all_preds, average="macro")
    return total_loss / n, acc, f1


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main() -> None:
    set_seed(SEED)
    device = get_device()
    print(f"Using device: {device}")

    # Replace with real data, e.g.:
    #   df = pd.read_csv("data.csv")
    #   X = df.drop(columns=["target"]).values.astype(np.float32)
    #   y = df["target"].values
    rng = np.random.default_rng(SEED)
    X = rng.normal(size=(3000, INPUT_DIM)).astype(np.float32)
    y = rng.integers(0, NUM_CLASSES, size=3000)

    train_loader, val_loader, test_loader, scaler = build_dataloaders(X, y)

    model = build_model(INPUT_DIM, HIDDEN_DIMS, NUM_CLASSES, DROPOUT).to(device)

    # CrossEntropyLoss = LogSoftmax + NLLLoss -> numerically stable for multi-class.
    criterion = nn.CrossEntropyLoss()

    # AdamW: Adam + decoupled weight decay -> better generalization than plain Adam.
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)

    best_f1 = 0.0

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc, val_f1 = evaluate(model, val_loader, criterion, device)
        print(f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.4f} | val_f1={val_f1:.4f}")

        if val_f1 > best_f1:
            best_f1 = val_f1
            torch.save(model.state_dict(), CKPT_PATH)

    # Load best checkpoint before final test evaluation.
    model.load_state_dict(torch.load(CKPT_PATH, map_location=device))
    test_loss, test_acc, test_f1 = evaluate(model, test_loader, criterion, device)
    print(f"TEST | loss={test_loss:.4f} | acc={test_acc:.4f} | f1={test_f1:.4f}")

    # Inference on new samples
    predict(model, X[:5], scaler, device)


@torch.no_grad()
def predict(model: nn.Module, X: np.ndarray, scaler: StandardScaler, device: torch.device) -> np.ndarray:
    """Always call model.eval() + torch.no_grad() for inference.
    Persist the scaler alongside the checkpoint — mismatched preprocessing
    between train and serve is a classic production bug."""
    model.eval()
    X_scaled = scaler.transform(X)
    tensor = torch.as_tensor(X_scaled, dtype=torch.float32).to(device)
    preds = model(tensor).argmax(1)
    print(f"Sample predictions: {preds.cpu().numpy()}")
    return preds.cpu().numpy()


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use:
#   Tabular / structured data with a fixed number of numeric features.
#   No spatial (image) or sequential (text/time-series) structure.
#
# Advantages:
#   - Simple, fast to train, easy to reason about.
#   - Strong baseline before trying more complex architectures.
#
# Disadvantages:
#   - No inductive bias for spatial/sequential patterns.
#   - Tree-based models (XGBoost/LightGBM) often outperform MLPs on
#     tabular data in practice.
#
# Common follow-up questions:
#   - Why BatchNorm before or after activation?
#     (Before: original paper; after: used by some practitioners — discuss tradeoffs.)
#   - How does Dropout differ at train vs eval time?
#     (Scales/disables at eval; model.eval() handles this automatically.)
#   - Why AdamW over Adam?
#     (Decoupled weight decay doesn't interact with the adaptive LR.)
#   - Why Kaiming init for ReLU?
#     (Keeps activation variance stable across layers; Xavier assumes symmetric activations.)
#   - Why CrossEntropyLoss and not softmax + NLLLoss?
#     (CrossEntropyLoss is numerically more stable; expects raw logits.)
#   - What is the double-softmax bug?
#     (Applying softmax before CrossEntropyLoss causes vanishing gradients.)
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# --- Binary classification ---
#   num_classes -> 1 output unit
#   criterion = nn.BCEWithLogitsLoss()   (sigmoid + BCE, numerically stable)
#   y dtype -> torch.float32, shape (B, 1)
#   preds = (torch.sigmoid(logits) > 0.5).long()
#
# --- Multi-class (this file) ---
#   nn.CrossEntropyLoss(), argmax over logits.
#
# --- Multi-label classification ---
#   final layer outputs num_labels logits
#   criterion = nn.BCEWithLogitsLoss()
#   y is a multi-hot float tensor, shape (B, num_labels)
#   preds = (torch.sigmoid(logits) > 0.5).long()
#
# --- Regression ---
#   final layer -> single unit, no activation
#   criterion = nn.MSELoss() or nn.SmoothL1Loss() (robust to outliers)
#   metrics: MAE / RMSE / R² instead of accuracy/F1
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# - Mixed precision (AMP):
#     scaler = torch.amp.GradScaler()
#     with torch.autocast(device_type=device.type):
#         loss = criterion(model(xb), yb)
#     scaler.scale(loss).backward()
#     scaler.step(optimizer); scaler.update()
#
# - LR scheduling (CosineAnnealingLR):
#     scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)
#     scheduler.step()  # after each epoch
#
# - Full checkpoint (resume-able):
#     torch.save({"epoch": epoch, "model": model.state_dict(),
#                 "optimizer": optimizer.state_dict()}, path)
#
# - ONNX export for serving:
#     dummy = torch.randn(1, INPUT_DIM, device=device)
#     torch.onnx.export(model, dummy, "ann.onnx",
#                       input_names=["input"], output_names=["logits"],
#                       dynamic_axes={"input": {0: "batch"}, "logits": {0: "batch"}})
#
# - TorchScript export:
#     scripted = torch.jit.script(model)
#     scripted.save("ann_scripted.pt")
#
# - Monitoring: log prediction distribution, feature distribution,
#   and live accuracy/F1 against a rolling validation set.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: tabular/structured data baselines.
# Advantages: simple, fast, strong baseline, interpretable weights.
# Disadvantages: no spatial/sequential inductive bias; tree ensembles
#   often win on tabular data; needs careful regularization.
# Time complexity: O(depth * width²) per sample (dense matmuls).
# Space complexity: O(depth * width²) for parameters.
# Common mistakes:
#   - Fitting the scaler on the full dataset (data leakage).
#   - Forgetting model.eval() / torch.no_grad() at inference.
#   - Using CrossEntropyLoss with already-softmaxed outputs (double softmax).
#   - Not shuffling training data.
# Production checklist:
#   [ ] Seed fixed, device-agnostic code
#   [ ] Scaler persisted alongside model checkpoint
#   [ ] Early stopping + best-checkpoint restore
#   [ ] Gradient clipping (clip_grad_norm_)
#   [ ] model.eval() + torch.no_grad() at inference
#   [ ] Exported to ONNX/TorchScript for serving
# ============================================================
