"""
============================================================
TEMPLATE 2: Convolutional Neural Network (CNN)
============================================================
Image classification (multi-class). Kept minimal/interview-scoped:
core workflow only, production extras noted as comments, not code.
============================================================
"""

import random

import numpy as np
import torch
from torch import nn, Tensor
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
SEED = 42
NUM_CLASSES = 10
IMG_SIZE = 32
BATCH_SIZE = 64
EPOCHS = 10
LR = 1e-3
PATIENCE = 3
CKPT_PATH = "checkpoints/cnn_best.pt"


# ------------------------------------------------------------
# Reproducibility + device
# ------------------------------------------------------------
def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------
# Dataset
# ------------------------------------------------------------
class ImageDataset(Dataset):
    """Replace with real image paths + labels. Expects images as (H, W, C) uint8."""

    def __init__(self, images: np.ndarray, labels: np.ndarray, transform=None) -> None:
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self) -> int:
        return len(self.images)

    def __getitem__(self, idx: int) -> tuple[Tensor, int]:
        img = self.images[idx]
        if self.transform:
            img = self.transform(img)
        return img, int(self.labels[idx])


# Normalize with ImageNet stats if using pretrained backbones; here, simple
# per-channel [0,1] scaling + augmentation on train only.
train_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.RandomHorizontalFlip(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])
eval_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])


# ------------------------------------------------------------
# Model (nn.ModuleDict of built-ins + a plain forward function — no custom class)
# ------------------------------------------------------------
def build_model(num_classes: int) -> nn.ModuleDict:
    """Simple ConvNet: 3 conv blocks + classifier head.

    Shape trace (input 3x32x32):
        conv1 + pool -> (32, 16, 16)
        conv2 + pool -> (64, 8, 8)
        conv3 + pool -> (128, 4, 4)
        flatten      -> (128*4*4)
        fc           -> (num_classes)

    Why: Conv layers exploit spatial locality + weight sharing (far fewer
    params than an MLP on raw pixels). MaxPool downsamples + adds
    translation invariance. ReLU avoids vanishing gradients.
    """
    return nn.ModuleDict({
        "features": nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1), nn.BatchNorm2d(32), nn.ReLU(inplace=True), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.BatchNorm2d(64), nn.ReLU(inplace=True), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1), nn.BatchNorm2d(128), nn.ReLU(inplace=True), nn.MaxPool2d(2),
        ),
        "pool": nn.AdaptiveAvgPool2d(1),  # handles variable input sizes robustly
        "classifier": nn.Linear(128, num_classes),
    })


def forward_cnn(m: nn.ModuleDict, x: Tensor) -> Tensor:
    x = m["features"](x)
    x = m["pool"](x).flatten(1)
    return m["classifier"](x)


# ------------------------------------------------------------
# Train / validate
# ------------------------------------------------------------
def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        loss = criterion(forward_cnn(model, xb), yb)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device) -> tuple[float, float]:
    model.eval()
    total_loss, correct = 0.0, 0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = forward_cnn(model, xb)
        total_loss += criterion(logits, yb).item() * xb.size(0)
        correct += (logits.argmax(1) == yb).sum().item()
    n = len(loader.dataset)
    return total_loss / n, correct / n


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main() -> None:
    set_seed(SEED)
    device = get_device()

    # Replace with real data, e.g. torchvision.datasets.ImageFolder or CIFAR10.
    rng = np.random.default_rng(SEED)
    images = rng.integers(0, 255, size=(2000, IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)
    labels = rng.integers(0, NUM_CLASSES, size=2000)

    full_ds = ImageDataset(images, labels, transform=train_transform)
    n = len(full_ds)
    n_train = int(0.8 * n)
    train_ds, val_ds = random_split(full_ds, [n_train, n - n_train])
    val_ds.dataset.transform = eval_transform  # no augmentation at eval time

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    model = build_model(NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    best_acc = 0.0

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        print(f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), CKPT_PATH)

    # Load best checkpoint before inference
    model.load_state_dict(torch.load(CKPT_PATH, map_location=device))
    predict(model, images[:5], device)


@torch.no_grad()
def predict(model: nn.Module, raw_images: np.ndarray, device: torch.device) -> np.ndarray:
    model.eval()
    batch = torch.stack([eval_transform(img) for img in raw_images]).to(device)
    preds = forward_cnn(model, batch).argmax(1)
    print(f"Sample predictions: {preds.cpu().numpy()}")
    return preds.cpu().numpy()


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: image data with spatial structure (grids of pixels).
# Advantages: parameter sharing -> fewer params than MLP; translation
#   invariance via pooling; hierarchical feature learning (edges -> textures -> objects).
# Disadvantages: needs more data than simpler models; less effective on
#   non-grid data; limited global context per layer (receptive field grows slowly)
#   compared to attention-based models.
# Complexity: conv layer cost ~ O(H*W*Cin*Cout*K^2) per layer.
# Follow-ups to expect:
#   - Why padding='same' equivalent (padding=1 for k=3)? Preserves spatial size.
#   - Why BatchNorm2d vs BatchNorm1d? Normalizes over (N,H,W) per channel.
#   - Why AdaptiveAvgPool2d(1) instead of Flatten? Makes model input-size agnostic.
#   - Receptive field growth across layers.
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Binary:       classifier -> 1 unit, BCEWithLogitsLoss, y as float
# Multi-label:  classifier -> num_labels units, BCEWithLogitsLoss, multi-hot y
# Regression:   classifier -> 1 unit, no activation, MSELoss
# Transfer learning: see Template 3 (ResNet) — swap `features` for a
#   pretrained backbone, freeze early layers, fine-tune later layers.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: image/grid-structured data.
# Pros: efficient, strong inductive bias for images, well understood.
# Cons: needs augmentation/regularization on small datasets; global
#   context requires deep stacks or attention.
# Time complexity: O(layers * H*W*Cin*Cout*K^2).
# Space complexity: O(sum of Cin*Cout*K^2) for weights + activations.
# Common mistakes: applying augmentation to val/test set; forgetting
#   model.eval() (BatchNorm uses running stats at eval); mismatched
#   normalization between train and inference.
# Production checklist: augmentation only on train, checkpoint best val
#   metric, export to TorchScript/ONNX for serving, monitor input
#   distribution drift (e.g. image size/lighting changes in production).
# ============================================================
