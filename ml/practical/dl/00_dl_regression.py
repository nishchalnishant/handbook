"""
DL REGRESSION — PyTorch MLP for continuous targets
Use when: predict a continuous value with a neural net (price, demand, latency, score).
Same skeleton as tabular MLP, but evaluated on MAE/RMSE/R².

WHY MLP for tabular: easy to express, works when features are heterogeneous + nonlinear.
WHY still benchmark vs XGBoost: tree models usually win on pure tabular — say this honestly.
WHY StandardScaler before MLP: keeps loss landscape well-conditioned → stable training.
WHY MSE for training, MAE for reporting: MSE is smooth (good gradients), MAE is interpretable.
"""

import json
import os

import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, Dataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# --- 1. DATASET ---
class TabularDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray):
        # float32 → matches default PyTorch weights; float64 wastes memory + slows GPU
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


# --- 2. MODEL ---
class RegressionMLP(nn.Module):
    """
    WHY depth (2-3 hidden layers): enough capacity for tabular interactions,
    shallow enough to train fast and not overfit small datasets.
    WHY Dropout 0.2: cheap regularization when dataset is small.
    WHY ReLU: default for regression; no vanishing gradient on positive side.
    """

    def __init__(self, input_dim: int, hidden=(128, 64), output_dim: int = 1):
        super().__init__()
        layers, prev = [], input_dim
        for h in hidden:
            layers += [nn.Linear(prev, h), nn.ReLU(), nn.Dropout(0.2)]
            prev = h
        # WHY no activation on final layer: regression needs raw real-valued output
        layers.append(nn.Linear(prev, output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


# --- 3. TRAIN / EVAL ---
def train_epoch(model, loader, optimizer, criterion):
    model.train()
    total, n = 0.0, 0
    for xb, yb in loader:
        xb, yb = xb.to(DEVICE), yb.to(DEVICE)
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        optimizer.step()
        total += loss.item() * len(xb)
        n += len(xb)
    return total / n


@torch.no_grad()
def evaluate(model, loader):
    model.eval()
    preds, targets = [], []
    for xb, yb in loader:
        xb = xb.to(DEVICE)
        preds.append(model(xb).cpu().numpy())
        targets.append(yb.numpy())
    return np.concatenate(preds).ravel(), np.concatenate(targets).ravel()


def train_regressor(df: pd.DataFrame, feature_cols: list[str], target_col: str,
                    epochs: int = 50, lr: float = 1e-3, batch_size: int = 64):
    X = df[feature_cols].values.astype(np.float32)
    y = df[target_col].values.astype(np.float32)

    # WHY no stratify for regression: stratify is for classification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # WHY fit scaler on train only: prevents target/feature leakage from test statistics
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    train_loader = DataLoader(TabularDataset(X_train, y_train),
                              batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(TabularDataset(X_test, y_test),
                             batch_size=batch_size, shuffle=False)

    model = RegressionMLP(input_dim=X_train.shape[1]).to(DEVICE)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    best_rmse, best_state = float("inf"), None
    for epoch in range(epochs):
        train_loss = train_epoch(model, train_loader, optimizer, criterion)
        preds, targets = evaluate(model, test_loader)
        rmse = float(np.sqrt(mean_squared_error(targets, preds)))
        if rmse < best_rmse:
            best_rmse = rmse
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}: train_mse={train_loss:.4f}  val_rmse={rmse:.4f}")

    model.load_state_dict(best_state)

    # WHY report MAE + RMSE + R²: MAE is interpretable, RMSE penalizes large errors, R² is normalized
    preds, targets = evaluate(model, test_loader)
    metrics = {
        "mae": mean_absolute_error(targets, preds),
        "rmse": float(np.sqrt(mean_squared_error(targets, preds))),
        "r2": r2_score(targets, preds),
    }
    print("Final regression metrics:", metrics)
    return model, scaler, metrics


# --- 4. SERIALIZE ---
def save_artifacts(model, scaler, feature_cols, out_dir="artifacts/dl_regression"):
    os.makedirs(out_dir, exist_ok=True)
    torch.save(model.state_dict(), f"{out_dir}/model.pt")
    joblib.dump(scaler, f"{out_dir}/scaler.joblib")
    with open(f"{out_dir}/config.json", "w") as f:
        json.dump({"feature_cols": feature_cols}, f)


def load_artifacts(out_dir="artifacts/dl_regression"):
    """Load model + scaler for inference. WHY bundle scaler: same scaling at train AND predict."""
    with open(f"{out_dir}/config.json") as f:
        cfg = json.load(f)
    scaler = joblib.load(f"{out_dir}/scaler.joblib")
    model = RegressionMLP(input_dim=len(cfg["feature_cols"]))
    model.load_state_dict(torch.load(f"{out_dir}/model.pt", map_location=DEVICE))
    model.to(DEVICE).eval()
    return model, scaler, cfg["feature_cols"]


@torch.no_grad()
def predict_one(model, scaler, feature_cols, raw: dict) -> float:
    row = pd.DataFrame([raw])[feature_cols].values.astype(np.float32)
    row = scaler.transform(row)
    tensor = torch.tensor(row, dtype=torch.float32).to(DEVICE)
    return float(model(tensor).cpu().numpy().ravel()[0])


if __name__ == "__main__":
    # df = pd.read_csv("data/train.csv")
    # model, scaler, metrics = train_regressor(df, feature_cols=NUMERIC, target_col=TARGET)
    # save_artifacts(model, scaler, NUMERIC)
    pass
