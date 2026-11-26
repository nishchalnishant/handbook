"""
DL USE CASE: GAN (Generative Adversarial Network)
Examples: synthetic training data, image augmentation, style transfer intro

WHY GAN: generator + discriminator compete → realistic synthetic samples.
WHY harder to train than diffusion: mode collapse, instability — mention Stable Diffusion as modern alt.
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Generator(nn.Module):
    """Maps random noise z → fake image."""

    def __init__(self, latent_dim=100, img_channels=3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 256 * 4 * 4), nn.ReLU(),
            nn.Unflatten(1, (256, 4, 4)),
            nn.ConvTranspose2d(256, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.ReLU(),
            nn.ConvTranspose2d(128, 64, 4, 2, 1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.ConvTranspose2d(64, img_channels, 4, 2, 1), nn.Tanh(),
        )

    def forward(self, z):
        return self.net(z)


class Discriminator(nn.Module):
    """Classifies real vs fake image."""

    def __init__(self, img_channels=3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(img_channels, 64, 4, 2, 1), nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2),
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 1), nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)


def train_gan(dataloader: DataLoader, latent_dim: int = 100, epochs: int = 50):
    G = Generator(latent_dim).to(DEVICE)
    D = Discriminator().to(DEVICE)
    opt_G = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
    opt_D = torch.optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))
    criterion = nn.BCELoss()

    for epoch in range(epochs):
        for real, _ in dataloader:
            real = real.to(DEVICE)
            batch_size = real.size(0)
            real_labels = torch.ones(batch_size, 1, device=DEVICE)
            fake_labels = torch.zeros(batch_size, 1, device=DEVICE)

            # --- Train Discriminator ---
            z = torch.randn(batch_size, latent_dim, device=DEVICE)
            fake = G(z)
            d_loss = criterion(D(real), real_labels) + criterion(D(fake.detach()), fake_labels)

            opt_D.zero_grad()
            d_loss.backward()
            opt_D.step()

            # --- Train Generator (fool discriminator) ---
            g_loss = criterion(D(fake), real_labels)
            opt_G.zero_grad()
            g_loss.backward()
            opt_G.step()

        print(f"Epoch {epoch + 1}: D_loss={d_loss.item():.3f}, G_loss={g_loss.item():.3f}")

    return G, D
