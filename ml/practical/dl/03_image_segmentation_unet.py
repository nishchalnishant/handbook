"""
DL USE CASE: Image Segmentation (pixel-level labels)
Examples: tumor segmentation, road/lane detection, background removal

WHY U-Net: encoder-decoder + skip connections preserve spatial detail.
WHY segmentation vs detection: need exact pixel boundaries (medical, satellite).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1), nn.BatchNorm2d(out_ch), nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1), nn.BatchNorm2d(out_ch), nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.net(x)


class UNet(nn.Module):
    """
    WHY skip connections: decoder upsampling loses detail; skips fuse high-res encoder features.
    """

    def __init__(self, in_channels=3, num_classes=2):
        super().__init__()
        self.down1 = DoubleConv(in_channels, 64)
        self.down2 = DoubleConv(64, 128)
        self.down3 = DoubleConv(128, 256)
        self.pool = nn.MaxPool2d(2)
        self.up2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.up3 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec2 = DoubleConv(256, 128)
        self.dec3 = DoubleConv(128, 64)
        self.out = nn.Conv2d(64, num_classes, 1)

    def forward(self, x):
        e1 = self.down1(x)
        e2 = self.down2(self.pool(e1))
        e3 = self.down3(self.pool(e2))
        d2 = self.dec2(torch.cat([self.up2(e3), e2], dim=1))
        d3 = self.dec3(torch.cat([self.up3(d2), e1], dim=1))
        return self.out(d3)  # [B, num_classes, H, W]


class SegmentationDataset(Dataset):
    def __init__(self, images, masks):
        self.images = images
        self.masks = masks

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        return self.images[idx], self.masks[idx]  # mask: LongTensor [H,W] with class ids


def dice_loss(logits, targets, num_classes: int):
    """
    WHY Dice loss: handles class imbalance in segmentation (small foreground region).
    """
    probs = F.softmax(logits, dim=1)
    targets_onehot = F.one_hot(targets, num_classes).permute(0, 3, 1, 2).float()
    intersection = (probs * targets_onehot).sum(dim=(2, 3))
    union = probs.sum(dim=(2, 3)) + targets_onehot.sum(dim=(2, 3))
    dice = (2 * intersection + 1) / (union + 1)
    return 1 - dice.mean()


def train_epoch(model, loader, optimizer):
    model.train()
    for images, masks in loader:
        images, masks = images.to(DEVICE), masks.to(DEVICE)
        optimizer.zero_grad()
        logits = model(images)
        loss = dice_loss(logits, masks, num_classes=logits.shape[1])
        loss.backward()
        optimizer.step()


@torch.no_grad()
def predict_mask(model, image_tensor):
    model.eval()
    logits = model(image_tensor.to(DEVICE))
    return logits.argmax(dim=1)  # [B, H, W] per-pixel class
