"""
DL USE CASE: Autoencoder for Anomaly Detection
Examples: manufacturing defects, fraud patterns, sensor failures

WHY autoencoder: learns to reconstruct NORMAL data; high reconstruction error = anomaly.
WHY unsupervised: anomalies are rare and hard to label.
"""

import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import DataLoader, TensorDataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Autoencoder(nn.Module):
    def __init__(self, input_dim: int, latent_dim: int = 16):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, latent_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, input_dim),
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)


def train_autoencoder(normal_data: np.ndarray, epochs: int = 50):
    """
    WHY train only on normal data: anomalies never seen → high reconstruction error at inference.
    """
    X = torch.tensor(normal_data, dtype=torch.float32)
    loader = DataLoader(TensorDataset(X), batch_size=64, shuffle=True)
    model = Autoencoder(input_dim=X.shape[1]).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()

    for epoch in range(epochs):
        model.train()
        for (batch,) in loader:
            batch = batch.to(DEVICE)
            optimizer.zero_grad()
            loss = criterion(model(batch), batch)
            loss.backward()
            optimizer.step()
    return model


@torch.no_grad()
def anomaly_scores(model, data: np.ndarray) -> np.ndarray:
    model.eval()
    X = torch.tensor(data, dtype=torch.float32).to(DEVICE)
    reconstructed = model(X)
    # WHY MSE per sample: higher error = more anomalous
    return ((X - reconstructed) ** 2).mean(dim=1).cpu().numpy()


def detect_anomalies(model, data: np.ndarray, threshold_percentile: float = 95):
    scores = anomaly_scores(model, data)
    threshold = np.percentile(scores, threshold_percentile)
    return scores, scores > threshold
