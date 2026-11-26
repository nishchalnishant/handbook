"""
============================================================
TEMPLATE 4: EfficientNet Transfer Learning
============================================================
Same transfer-learning pattern as ResNet (Template 3), swapped to
EfficientNet-B0. Kept short since the workflow is identical — only the
backbone/head-replacement and preprocessing differ.
============================================================
"""

import random

import numpy as np
import torch
from torch import nn, Tensor
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms, models


# Config (plain constants)
SEED = 42
NUM_CLASSES = 5
IMG_SIZE = 224            # EfficientNet-B0 default input size
BATCH_SIZE = 32
EPOCHS = 8
LR_HEAD = 1e-3
LR_BACKBONE = 1e-5
FREEZE_BACKBONE = True
CKPT_PATH = "checkpoints/efficientnet_best.pt"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


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


def build_model(num_classes: int, freeze_backbone: bool) -> nn.Module:
    """EfficientNet-B0 with a replaced classifier head.

    Why EfficientNet over ResNet: uses compound scaling (jointly scales
    depth/width/resolution via a single coefficient) to get better
    accuracy-per-FLOP than hand-designed nets like ResNet. Uses MBConv
    blocks (depthwise separable convs + squeeze-excitation) for efficiency.
    """
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)

    if freeze_backbone:
        for param in model.parameters():
            param.requires_grad = False

    # EfficientNet's head is `classifier` (Sequential[Dropout, Linear]), not `fc`.
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model


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


def main() -> None:
    set_seed(SEED)
    device = get_device()

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

    param_groups = [{"params": model.classifier.parameters(), "lr": LR_HEAD}]
    if not FREEZE_BACKBONE:
        backbone_params = [p for n, p in model.named_parameters() if not n.startswith("classifier")]
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
# When to use: need better accuracy/compute tradeoff than ResNet, e.g.
#   edge/mobile deployment or latency-sensitive inference.
# Advantages: compound scaling gives strong accuracy at lower FLOPs/params
#   vs ResNet; family of models (B0-B7) lets you trade accuracy for speed.
# Disadvantages: more sensitive to input resolution (each variant expects
#   a specific size); MBConv/depthwise convs can be slower on some hardware
#   despite fewer FLOPs (memory-bound, not compute-bound).
# Complexity: EfficientNet-B0 ~0.39 GFLOPs vs ResNet18 ~1.8 GFLOPs at
#   similar/better accuracy.
# Follow-ups to expect:
#   - What is compound scaling? (jointly scale depth/width/resolution
#     with fixed ratios found via grid search, vs scaling one dimension alone)
#   - What is squeeze-and-excitation? (channel-wise attention recalibrating
#     feature maps)
#   - Why might EfficientNet be slower in practice despite fewer FLOPs?
#     (depthwise convs are memory-bandwidth bound, less GPU-parallelism-friendly)
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Binary/Multi-label/Regression: same head-replacement pattern as
#   Template 3 — swap model.classifier[1] output units + loss function.
# Larger variants: models.efficientnet_b3/b4/... for more capacity,
#   at the cost of larger required input resolution and compute.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: need strong accuracy per FLOP, mobile/edge-constrained inference.
# Pros: compound scaling family, efficient MBConv blocks, strong ImageNet transfer.
# Cons: input resolution sensitive; depthwise convs can be memory-bound on GPU.
# Time complexity: ~0.39 GFLOPs (B0) vs 1.8 GFLOPs (ResNet18).
# Space complexity: ~5M params (B0), smaller than ResNet18's 11M.
# Common mistakes: using wrong input resolution for the chosen variant;
#   forgetting classifier head is `classifier[1]`, not `fc`.
# Production checklist: match input resolution to the specific EfficientNet
#   variant used, pin torchvision weights version, export ONNX/TorchScript,
#   benchmark actual latency on target hardware (FLOPs don't always predict wall-clock).
# ============================================================
