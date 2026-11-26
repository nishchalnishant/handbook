"""
DL USE CASE: Tabular data with MLP (when interviewer asks for neural net on structured data)
Examples: credit scoring, churn, price prediction

WHY MLP not CNN/RNN: tabular has no spatial/temporal structure.
WHY still try XGBoost first: usually beats MLP on pure tabular — mention this honestly.
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, Dataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TabularDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class MLP(nn.Module):
    def __init__(self, input_dim, hidden=(128, 64), output_dim=1, task="regression"):
        super().__init__()
        layers = []
        prev = input_dim
        for h in hidden:
            layers += [nn.Linear(prev, h), nn.ReLU(), nn.Dropout(0.2)]
            prev = h
        layers.append(nn.Linear(prev, output_dim))
        self.net = nn.Sequential(*layers)
        self.task = task

    def forward(self, x):
        return self.net(x)


def train(df, feature_cols, target_col, task="regression", epochs=50):
    X = df[feature_cols].values.astype(np.float32)
    y = df[target_col].values.astype(np.float32)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train, X_val = scaler.fit_transform(X_train), scaler.transform(X_val)

    train_loader = DataLoader(TabularDataset(X_train, y_train), batch_size=64, shuffle=True)
    output_dim = 1
    model = MLP(X_train.shape[1], output_dim=output_dim, task=task).to(DEVICE)

    criterion = nn.MSELoss() if task == "regression" else nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(epochs):
        model.train()
        for xb, yb in train_loader:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            optimizer.zero_grad()
            loss = criterion(model(xb), yb if task == "regression" else yb.long().squeeze())
            loss.backward()
            optimizer.step()

    os.makedirs("artifacts/tabular_mlp", exist_ok=True)
    torch.save(model.state_dict(), "artifacts/tabular_mlp/model.pt")
    joblib.dump(scaler, "artifacts/tabular_mlp/scaler.joblib")
    with open("artifacts/tabular_mlp/config.json", "w") as f:
        json.dump({"feature_cols": feature_cols, "task": task}, f)
    return model, scaler
