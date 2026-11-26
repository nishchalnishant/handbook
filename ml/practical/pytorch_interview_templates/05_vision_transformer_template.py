"""
============================================================
TEMPLATE 5: Vision Transformer (ViT)
============================================================
Image classification using a pretrained ViT (torchvision) with a
replaced head, plus a minimal from-scratch ViT block for interviews
that ask you to implement patch embedding + attention by hand.
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
IMG_SIZE = 224
PATCH_SIZE = 16
BATCH_SIZE = 32
EPOCHS = 8
LR_HEAD = 1e-3
LR_BACKBONE = 1e-5
FREEZE_BACKBONE = True
CKPT_PATH = "checkpoints/vit_best.pt"


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


# ------------------------------------------------------------
# Pretrained ViT (what you'd actually use in production)
# ------------------------------------------------------------
def build_pretrained_vit(num_classes: int, freeze_backbone: bool) -> nn.Module:
    model = models.vit_b_16(weights=models.ViT_B_16_Weights.IMAGENET1K_V1)
    if freeze_backbone:
        for param in model.parameters():
            param.requires_grad = False
    in_features = model.heads.head.in_features
    model.heads.head = nn.Linear(in_features, num_classes)
    return model


# ------------------------------------------------------------
# Minimal from-scratch ViT (for "implement attention/patching" interviews)
# nn.ModuleDict of built-ins + plain forward functions — no custom classes.
# ------------------------------------------------------------
def build_patch_embedding(img_size: int, patch_size: int, in_channels: int, embed_dim: int) -> nn.ModuleDict:
    """Splits image into non-overlapping patches and linearly projects
    each into an embedding — the Conv2d with stride=kernel_size trick
    does patching + projection in a single op.

    Shape trace (img 224x224, patch 16, embed_dim 768):
        input:        (B, 3, 224, 224)
        after conv:   (B, 768, 14, 14)   [14 = 224/16 patches per side]
        after flatten:(B, 768, 196)
        after transpose: (B, 196, 768)   [sequence of 196 patch tokens]
    """
    m = nn.ModuleDict({
        "proj": nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size),
    })
    m.num_patches = (img_size // patch_size) ** 2
    return m


def forward_patch_embedding(m: nn.ModuleDict, x: Tensor) -> Tensor:
    x = m["proj"](x)                # (B, embed_dim, H/P, W/P)
    x = x.flatten(2)                # (B, embed_dim, num_patches)
    x = x.transpose(1, 2)           # (B, num_patches, embed_dim)
    return x


def build_vit_encoder_block(embed_dim: int, num_heads: int, mlp_ratio: int = 4, dropout: float = 0.1) -> nn.ModuleDict:
    """Pre-norm transformer block: LN -> MHSA -> residual, LN -> MLP -> residual.
    Pre-norm (vs post-norm) is more stable to train at depth without
    needing careful warmup schedules."""
    return nn.ModuleDict({
        "norm1": nn.LayerNorm(embed_dim),
        "attn": nn.MultiheadAttention(embed_dim, num_heads, dropout=dropout, batch_first=True),
        "norm2": nn.LayerNorm(embed_dim),
        "mlp": nn.Sequential(
            nn.Linear(embed_dim, embed_dim * mlp_ratio),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(embed_dim * mlp_ratio, embed_dim),
            nn.Dropout(dropout),
        ),
    })


def forward_vit_encoder_block(m: nn.ModuleDict, x: Tensor) -> Tensor:
    normed = m["norm1"](x)
    attn_out, _ = m["attn"](normed, normed, normed, need_weights=False)
    x = x + attn_out                    # residual connection
    x = x + m["mlp"](m["norm2"](x))     # residual connection
    return x


def build_vit_from_scratch(
    img_size: int = 224,
    patch_size: int = 16,
    in_channels: int = 3,
    embed_dim: int = 256,
    depth: int = 6,
    num_heads: int = 8,
    num_classes: int = 5,
) -> nn.ModuleDict:
    """Minimal ViT: patch embed -> [CLS] token + positional embed ->
    transformer encoder blocks -> classify from [CLS] token."""
    patch_embed = build_patch_embedding(img_size, patch_size, in_channels, embed_dim)
    num_patches = patch_embed.num_patches

    m = nn.ModuleDict({
        "patch_embed": patch_embed,
        "blocks": nn.ModuleList([build_vit_encoder_block(embed_dim, num_heads) for _ in range(depth)]),
        "norm": nn.LayerNorm(embed_dim),
        "head": nn.Linear(embed_dim, num_classes),
    })

    # CLS token aggregates global information for classification (like BERT's [CLS]).
    cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
    # Learned positional embeddings inject order info (patches have no
    # inherent sequence order otherwise, unlike RNNs).
    pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
    nn.init.trunc_normal_(pos_embed, std=0.02)
    nn.init.trunc_normal_(cls_token, std=0.02)
    m.cls_token = cls_token
    m.pos_embed = pos_embed
    return m


def forward_vit_from_scratch(m: nn.ModuleDict, x: Tensor) -> Tensor:
    B = x.shape[0]
    x = forward_patch_embedding(m["patch_embed"], x)      # (B, num_patches, embed_dim)
    cls_tokens = m.cls_token.expand(B, -1, -1)            # (B, 1, embed_dim)
    x = torch.cat([cls_tokens, x], dim=1)                 # (B, num_patches+1, embed_dim)
    x = x + m.pos_embed
    for block in m["blocks"]:
        x = forward_vit_encoder_block(block, x)
    x = m["norm"](x)
    cls_out = x[:, 0]                                     # take [CLS] token representation
    return m["head"](cls_out)


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

    # Use the pretrained model in practice; swap to
    # forward_vit_from_scratch(build_vit_from_scratch(...), xb) if asked to
    # implement ViT internals.
    model = build_pretrained_vit(NUM_CLASSES, FREEZE_BACKBONE).to(device)
    criterion = nn.CrossEntropyLoss()

    param_groups = [{"params": model.heads.head.parameters(), "lr": LR_HEAD}]
    if not FREEZE_BACKBONE:
        backbone_params = [p for n, p in model.named_parameters() if not n.startswith("heads")]
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
# When to use: large labeled datasets or strong pretraining available;
#   tasks benefiting from global context from the first layer (unlike CNNs,
#   which build up receptive field gradually).
# Advantages: models long-range dependencies directly via self-attention;
#   scales well with data/compute; strong transfer learning performance.
# Disadvantages: needs more data than CNNs to train from scratch (weaker
#   inductive bias — no built-in translation equivariance); quadratic
#   attention cost in number of patches.
# Complexity: self-attention is O(N^2 * d) where N = num_patches (e.g. 196
#   for 224x224 img with patch 16), d = embed_dim.
# Follow-ups to expect:
#   - Why CLS token instead of global average pooling? (both work; CLS
#     is the original design, GAP is a common simplification.)
#   - Why positional embeddings needed? (attention is permutation-invariant
#     without them — patches would have no notion of spatial order.)
#   - How does patch size affect sequence length and compute? (smaller
#     patch -> longer sequence -> higher O(N^2) attention cost.)
#   - Why pre-norm over post-norm? (training stability at depth.)
# ============================================================


# ============================================================
# VARIATIONS (brief)
# ============================================================
# Binary/Multi-label/Regression: swap model.heads.head (or the
#   build_vit_from_scratch "head" entry) output units + loss function, same as CNN/ResNet templates.
# Fine-tuning: unfreeze last few encoder blocks first (progressive
#   unfreezing), similar rationale to ResNet.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: large data/pretraining available, need global context modeling.
# Pros: strong long-range dependency modeling, scales well, transfers well.
# Cons: data-hungry from scratch, quadratic attention cost, less inductive
#   bias than CNNs for images.
# Time complexity: O(N^2 * d) attention + O(N * d^2) MLP per block, N=patches.
# Space complexity: O(N^2) for attention matrices + O(depth * d^2) for weights.
# Common mistakes: forgetting positional embeddings; using GAP and CLS
#   token inconsistently; mismatched patch size vs image size (must divide evenly).
# Production checklist: match preprocessing exactly to pretrained checkpoint,
#   consider throughput cost of attention at high resolution, export
#   TorchScript/ONNX, benchmark actual latency (attention ops can be
#   slower than conv equivalents on some hardware).
# ============================================================
