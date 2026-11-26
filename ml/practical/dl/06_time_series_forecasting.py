"""
DL USE CASE: Time Series Forecasting
Examples: demand forecasting, stock prediction, sensor anomaly trends

WHY LSTM/GRU: captures temporal dependencies across timesteps.
WHY sliding window: convert series to supervised learning (X=past N steps, y=next step).
Alternative: Temporal Fusion Transformer, N-BEATS — mention for modern interviews.
"""

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from sklearn.preprocessing import MinMaxScaler

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_sequences(data: np.ndarray, window_size: int, horizon: int = 1):
    """
    WHY windowing: LSTM needs fixed-length input sequences.
    data shape: [num_samples, window_size, num_features]
    target shape: [num_samples, horizon]
    """
    X, y = [], []
    for i in range(len(data) - window_size - horizon + 1):
        X.append(data[i : i + window_size])
        y.append(data[i + window_size : i + window_size + horizon, 0])  # predict first feature
    return np.array(X), np.array(y)


class TimeSeriesDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class LSTMForecaster(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64, num_layers: int = 2, horizon: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=0.1)
        self.fc = nn.Linear(hidden_dim, horizon)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])  # WHY last timestep: summarizes full sequence


def train_forecaster(series: np.ndarray, window_size: int = 30, epochs: int = 50):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(series.reshape(-1, 1))

    X, y = create_sequences(scaled, window_size)
    split = int(0.8 * len(X))
    train_loader = DataLoader(TimeSeriesDataset(X[:split], y[:split]), batch_size=32, shuffle=True)

    model = LSTMForecaster(input_dim=1).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()

    for epoch in range(epochs):
        model.train()
        for xb, yb in train_loader:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            optimizer.zero_grad()
            loss = criterion(model(xb), yb)
            loss.backward()
            optimizer.step()
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch + 1}")

    return model, scaler


@torch.no_grad()
def forecast(model, last_window: np.ndarray, scaler: MinMaxScaler, steps: int = 10):
    """Autoregressive multi-step: feed prediction back as next input."""
    model.eval()
    window = last_window.copy()
    preds = []
    for _ in range(steps):
        x = torch.tensor(window[-30:], dtype=torch.float32).unsqueeze(0).unsqueeze(-1).to(DEVICE)
        pred = model(x).cpu().numpy()
        preds.append(pred[0, 0])
        window = np.vstack([window, pred])
    return scaler.inverse_transform(np.array(preds).reshape(-1, 1)).flatten()
