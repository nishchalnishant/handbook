"""
DL IMBALANCED CLASSIFICATION — weighted loss + WeightedRandomSampler
Use when: rare class in images or tabular DL (fraud, defect, disease).

WHY NOT oversample images in memory: expensive; weighted sampling is cleaner.
WHY class weights in loss: penalize minority misclassification directly.
WHY F1 / per-class recall: accuracy is misleading with 99% negative class.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import classification_report, f1_score
from sklearn.utils.class_weight import compute_class_weight
from torch.utils.data import DataLoader, WeightedRandomSampler

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class SimpleCNN(nn.Module):
    def __init__(self, num_classes: int):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Linear(128, num_classes)

    def forward(self, x):
        return self.classifier(self.features(x).flatten(1))


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
    all_preds, all_labels = [], []
    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        logits = model(images)
        all_preds.extend(logits.argmax(1).cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
    return 0, 0, all_labels, all_preds


# --- WEIGHTED LOSS ---
def get_class_weights(labels: np.ndarray) -> torch.Tensor:
    """
    WHY: minority class gets higher weight → model pays more for missing fraud cases.
    Formula: weight_c = n_samples / (n_classes * n_samples_c)
    """
    classes = np.unique(labels)
    weights = compute_class_weight("balanced", classes=classes, y=labels)
    return torch.tensor(weights, dtype=torch.float32).to(DEVICE)


class WeightedCrossEntropy(nn.Module):
    def __init__(self, class_weights: torch.Tensor):
        super().__init__()
        self.criterion = nn.CrossEntropyLoss(weight=class_weights)

    def forward(self, logits, targets):
        return self.criterion(logits, targets)


# --- WEIGHTED SAMPLER (alternative/complement to weighted loss) ---
def make_weighted_sampler(labels: np.ndarray) -> WeightedRandomSampler:
    """
    WHY sampler: oversample minority class each epoch without duplicating dataset on disk.
    Use EITHER weighted loss OR sampler — combining both can over-correct (mention this).
    """
    class_counts = np.bincount(labels)
    class_weights = 1.0 / class_counts
    sample_weights = class_weights[labels]
    return WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)


# --- FOCAL LOSS (advanced — mention for object detection / extreme imbalance) ---
class FocalLoss(nn.Module):
    """
    WHY Focal Loss: down-weights easy examples, focuses on hard minority cases.
    Paper: Lin et al. — good talking point for CV interviews.
    """

    def __init__(self, gamma=2.0, alpha=None):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha

    def forward(self, logits, targets):
        ce = F.cross_entropy(logits, targets, reduction="none", weight=self.alpha)
        pt = torch.exp(-ce)
        return ((1 - pt) ** self.gamma * ce).mean()


# --- TRAINING WITH IMBALANCE ---
def train_imbalanced(train_loader, val_loader, labels_train: np.ndarray, num_classes: int, epochs=20):
    model = SimpleCNN(num_classes).to(DEVICE)
    class_weights = get_class_weights(labels_train)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    best_f1, best_state = 0, None
    for epoch in range(epochs):
        train_epoch(model, train_loader, optimizer, criterion)
        _, _, y_true, y_pred = evaluate(model, val_loader, criterion)
        f1 = f1_score(y_true, y_pred, average="macro")  # WHY macro: treats all classes equally
        if f1 > best_f1:
            best_f1 = f1
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
        print(f"Epoch {epoch+1}: macro F1={f1:.3f}")

    model.load_state_dict(best_state)
    print(classification_report(y_true, y_pred))
    return model


# --- THRESHOLD TUNING FOR BINARY CNN (e.g. defect yes/no) ---
@torch.no_grad()
def predict_proba(model, loader):
    model.eval()
    probas, labels = [], []
    for images, y in loader:
        images = images.to(DEVICE)
        logits = model(images)
        proba = torch.softmax(logits, dim=1)[:, 1]  # positive class
        probas.extend(proba.cpu().numpy())
        labels.extend(y.numpy())
    return np.array(labels), np.array(probas)


if __name__ == "__main__":
    pass
