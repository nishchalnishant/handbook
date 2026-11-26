"""
DL CLASSIFICATION — PyTorch image classification (CNN)
Use when: images (medical scans, defect detection, document classification).

WHY CNN: exploits spatial locality + translation invariance in images.
WHY ResNet-style skip connections: train deeper nets without vanishing gradients.
WHY pretrained backbone: transfer learning when data is limited (mention in interview).
"""

import json
import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, classification_report
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# --- 1. DATA AUGMENTATION ---
def get_transforms(train: bool = True):
    """
    WHY augmentation on train only: artificially expand dataset, reduce overfitting.
    WHY Normalize with ImageNet stats: required when using pretrained weights.
    """
    if train:
        return transforms.Compose([
            transforms.Resize(256),
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])


# --- 2. MODEL: simple CNN (write from scratch in interview) OR pretrained ---
class SimpleCNN(nn.Module):
    """Use when interviewer says 'build a CNN from scratch'."""

    def __init__(self, num_classes: int):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.features(x).flatten(1)
        return self.classifier(x)


def build_model(num_classes: int, pretrained: bool = True):
    """
    pretrained=True  → transfer learning (small dataset, faster convergence)
    pretrained=False → SimpleCNN from scratch (demonstrate fundamentals)
    """
    if pretrained:
        # WHY ResNet18: lightweight, well-known, good interview answer
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        model.fc = nn.Linear(model.fc.in_features, num_classes)  # replace head
        return model
    return SimpleCNN(num_classes)


# --- 3. TRAIN / EVAL ---
def train_epoch(model, loader, optimizer, criterion):
    model.train()
    total_loss, correct, total = 0, 0, 0
    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        logits = model(images)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(images)
        correct += (logits.argmax(1) == labels).sum().item()
        total += len(images)
    return total_loss / total, correct / total


@torch.no_grad()
def evaluate(model, loader, criterion):
    model.eval()
    total_loss, all_preds, all_labels = 0, [], []
    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        logits = model(images)
        loss = criterion(logits, labels)
        total_loss += loss.item() * len(images)
        all_preds.extend(logits.argmax(1).cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
    acc = accuracy_score(all_labels, all_preds)
    return total_loss / len(loader.dataset), acc, all_labels, all_preds


def train_classifier(train_dir, val_dir, num_classes: int, epochs=10, lr=1e-4, use_pretrained=True):
    train_ds = datasets.ImageFolder(train_dir, transform=get_transforms(train=True))
    val_ds = datasets.ImageFolder(val_dir, transform=get_transforms(train=False))

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=32, shuffle=False, num_workers=2)

    model = build_model(num_classes, pretrained=use_pretrained).to(DEVICE)

    # WHY CrossEntropyLoss: multi-class classification standard (includes softmax)
    criterion = nn.CrossEntropyLoss()

    # WHY freeze backbone when little data: only train classifier head first
    if use_pretrained:
        for param in model.parameters():
            param.requires_grad = False
        for param in model.fc.parameters():
            param.requires_grad = True

    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=lr)

    best_acc, best_state = 0, None
    for epoch in range(epochs):
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion)
        val_loss, val_acc, y_true, y_pred = evaluate(model, val_loader, criterion)
        if val_acc > best_acc:
            best_acc = val_acc
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
        print(f"Epoch {epoch+1}: train_acc={train_acc:.3f}, val_acc={val_acc:.3f}")

    model.load_state_dict(best_state)
    print(classification_report(y_true, y_pred))
    return model, train_ds.classes


# --- 4. SAVE / LOAD ---
def save_model(model, class_names, path_dir="artifacts_classification"):
    os.makedirs(path_dir, exist_ok=True)
    torch.save(model.state_dict(), f"{path_dir}/model.pt")
    with open(f"{path_dir}/classes.json", "w") as f:
        json.dump(class_names, f)


if __name__ == "__main__":
    pass
