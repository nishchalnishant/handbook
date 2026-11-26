"""
============================================================
TEMPLATE 3: Transfer Learning using ResNet
============================================================
Image classification via a pretrained ResNet18 backbone.
Two modes shown: (1) feature extraction (freeze backbone),
(2) fine-tuning (unfreeze + smaller LR). Interview-scoped.
============================================================
"""

import random

import numpy as np
import torch
from torch import nn, Tensor
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms, models


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
SEED = 42
NUM_CLASSES = 5
IMG_SIZE = 224            # ResNet expects 224x224 (pretrained on ImageNet)
BATCH_SIZE = 32
EPOCHS = 8
LR_HEAD = 1e-3             # LR for new classifier head
LR_BACKBONE = 1e-5         # much smaller LR when fine-tuning pretrained layers
FREEZE_BACKBONE = True     # start with feature extraction; set False to fine-tune
CKPT_PATH = "checkpoints/resnet_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------
# Dataset
# ------------------------------------------------------------
class ImageDataset(Dataset):
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


# Must match the normalization stats ResNet was pretrained with (ImageNet).
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

train_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])
eval_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224)),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])


# ------------------------------------------------------------
# Model: pretrained ResNet18 with a new head
# ------------------------------------------------------------
def build_model(num_classes: int, freeze_backbone: bool) -> nn.Module:
    """Loads ImageNet-pretrained ResNet18 and replaces the final FC layer.

    Why ResNet: residual connections (skip connections) let gradients
    flow through very deep networks, solving vanishing-gradient/degradation
    problems that plague plain deep CNNs.

    Feature extraction vs fine-tuning:
    - Feature extraction (freeze_backbone=True): treat the pretrained
      network as a fixed feature extractor; only train the new head.
      Fast, works well with small datasets.
    - Fine-tuning (freeze_backbone=False): unfreeze some/all backbone
      layers and train with a small LR so pretrained weights aren't
      destroyed by large gradient updates.
    """
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

    if freeze_backbone:
        for param in model.parameters():
            param.requires_grad = False

    # Replace classifier head; new layers are trainable by default.
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model


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
        optimizer.step()
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device) -> tuple[float, float]:
    model.eval()
    total_loss, correct = 0.0, 0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = model(xb)
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

    # Replace with real data (e.g. torchvision.datasets.ImageFolder).
    rng = np.random.default_rng(SEED)
    images = rng.integers(0, 255, size=(500, 128, 128, 3), dtype=np.uint8)
    labels = rng.integers(0, NUM_CLASSES, size=500)

    full_ds = ImageDataset(images, labels, transform=train_transform)
    n = len(full_ds)
    n_train = int(0.8 * n)
    train_ds, val_ds = random_split(full_ds, [n_train, n - n_train])
    val_ds.dataset.transform = eval_transform

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    model = build_model(NUM_CLASSES, FREEZE_BACKBONE).to(device)
    criterion = nn.CrossEntropyLoss()

    # Discriminative learning rates: new head trains faster than the
    # (optionally unfrozen) pretrained backbone.
    param_groups = [{"params": model.fc.parameters(), "lr": LR_HEAD}]
    if not FREEZE_BACKBONE:
        backbone_params = [p for n, p in model.named_parameters() if not n.startswith("fc")]
        param_groups.append({"params": backbone_params, "lr": LR_BACKBONE})
    optimizer = torch.optim.Adam(param_groups)

    best_acc = 0.0

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        print(f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), CKPT_PATH)

    model.load_state_dict(torch.load(CKPT_PATH, map_location=device))
    predict(model, images[:5], device)


@torch.no_grad()
def predict(model: nn.Module, raw_images: np.ndarray, device: torch.device) -> np.ndarray:
    model.eval()
    batch = torch.stack([eval_transform(img) for img in raw_images]).to(device)
    preds = model(batch).argmax(1)
    print(f"Sample predictions: {preds.cpu().numpy()}")
    return preds.cpu().numpy()


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: image classification with limited labeled data; reuse
#   features learned from large datasets (ImageNet) instead of training
#   from scratch.
# Advantages: much less data/compute needed; faster convergence; strong
#   baseline performance.
# Disadvantages: pretrained features may not transfer well to very
#   different domains (e.g. medical/satellite imagery); input must match
#   expected preprocessing (size, normalization).
# Complexity: same as ResNet18 forward pass (~1.8 GFLOPs at 224x224);
#   feature extraction is cheaper since backbone gradients aren't computed.
# Follow-ups to expect:
#   - Why freeze vs fine-tune, and when to choose each (dataset size/similarity
#     to source domain — see the classic "size vs similarity" 2x2 matrix).
#   - Why use a smaller LR for backbone during fine-tuning (avoid catastrophic
#     forgetting of pretrained weights).
#   - What layers to unfreeze first (later layers, closer to task-specific
#     features; early layers capture generic edges/textures).
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Binary:      model.fc -> Linear(in_features, 1), BCEWithLogitsLoss
# Multi-label: model.fc -> Linear(in_features, num_labels), BCEWithLogitsLoss, multi-hot y
# Regression:  model.fc -> Linear(in_features, 1), MSELoss
# Full fine-tuning: set freeze_backbone=False from the start (needs more data).
# Progressive unfreezing: start frozen, train head a few epochs, then
#   unfreeze last residual block (model.layer4) with a low LR, continue training.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: limited data, want to leverage ImageNet-pretrained features.
# Pros: fast convergence, strong performance with small datasets, less
#   compute than training from scratch.
# Cons: domain mismatch risk; must match input preprocessing exactly;
#   less flexibility in architecture changes.
# Time complexity: forward/backward cost of ResNet18 (~11M params).
# Space complexity: O(11M) params (~45MB fp32).
# Common mistakes: forgetting ImageNet normalization stats; not freezing
#   backbone when data is very limited (overfits fast); using same LR for
#   backbone and head during fine-tuning.
# Production checklist: pin exact torchvision weights version, persist
#   preprocessing transform with the model, export ONNX/TorchScript,
#   monitor input distribution drift (image domain, lighting, resolution).
# ============================================================
