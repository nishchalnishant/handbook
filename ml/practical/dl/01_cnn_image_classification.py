"""
DL USE CASE: CNN Image Classification
Examples: defect detection, medical imaging, document type classifier

WHY CNN: exploits spatial hierarchy (edges → textures → objects).
WHY transfer learning (ResNet): pretrained on ImageNet → needs less labeled data.
WHY data augmentation: artificially expands dataset, reduces overfitting.
"""

import json
import os

import torch
import torch.nn as nn
from sklearn.metrics import classification_report
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_transforms(train: bool = True):
    if train:
        return transforms.Compose([
            transforms.Resize(256),
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])


class SimpleCNN(nn.Module):
    """Use when interviewer says 'build CNN from scratch'."""

    def __init__(self, num_classes: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        return self.net(x)


def build_model(num_classes: int, pretrained: bool = True):
    if pretrained:
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model
    return SimpleCNN(num_classes)


def train_epoch(model, loader, optimizer, criterion):
    model.train()
    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        loss = criterion(model(images), labels)
        loss.backward()
        optimizer.step()


@torch.no_grad()
def evaluate(model, loader, criterion):
    model.eval()
    preds, targets = [], []
    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        logits = model(images)
        preds.extend(logits.argmax(1).cpu().tolist())
        targets.extend(labels.cpu().tolist())
    print(classification_report(targets, preds))
    return targets, preds


def train(train_dir: str, val_dir: str, num_classes: int, epochs: int = 10):
    train_ds = datasets.ImageFolder(train_dir, transform=get_transforms(True))
    val_ds = datasets.ImageFolder(val_dir, transform=get_transforms(False))
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=32, num_workers=2)

    model = build_model(num_classes).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(epochs):
        train_epoch(model, train_loader, optimizer, criterion)
        evaluate(model, val_loader, criterion)
        print(f"Epoch {epoch + 1} done")

    os.makedirs("artifacts/cnn_classifier", exist_ok=True)
    torch.save(model.state_dict(), "artifacts/cnn_classifier/model.pt")
    with open("artifacts/cnn_classifier/classes.json", "w") as f:
        json.dump(train_ds.classes, f)
    return model
