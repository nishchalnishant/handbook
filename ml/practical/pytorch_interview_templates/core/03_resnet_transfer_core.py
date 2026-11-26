"""Core: ResNet18 transfer learning — replace final FC, optionally freeze backbone.

INTERVIEW GUIDE
----------------
Typical ask: "Given a small labeled image dataset, use a pretrained model to
build a classifier." Usually the main problem in a 1hr session, since it's
really a discussion about transfer-learning strategy more than raw coding.

Expected depth (1hr session):
  - Junior/mid: load pretrained weights, correctly replace model.fc using
    in_features = model.fc.in_features (not a hardcoded number), and explain
    what freeze_backbone=True does via requires_grad = False.
  - Senior: justify freeze vs. fine-tune based on dataset size/similarity to
    ImageNet, propose discriminative learning rates for partial fine-tuning,
    and discuss catastrophic forgetting risk when unfreezing too aggressively
    with too high an LR.
  Core coding is quick (10 min); most of the hour goes to the freeze/fine-tune
  strategy discussion and often pivots into 04_efficientnet_transfer_core.py
  as a "now compare architectures" stretch goal.

Common follow-ups:
  - "When would you freeze the backbone vs. fine-tune the whole thing?"
    (freeze when the target dataset is small and similar to ImageNet;
    fine-tune more when it's larger or visually different, e.g. medical/satellite
    imagery).
  - "If you unfreeze everything, what LR do you use for the backbone vs. the
    new head?" (discriminative/layer-wise LRs -- much smaller LR for
    pretrained layers, larger for the freshly-initialized fc, since the head
    starts from random weights and needs bigger updates).
  - "Why replace only model.fc and not add a new layer on top?" (fc is the
    only layer whose output dim is task-specific -- everything before it is
    a generic feature extractor already trained to be useful).
  - "What is catastrophic forgetting here and how do you avoid it?" (fine-tuning
    with too high an LR overwrites the pretrained features; mitigate with
    small LR, gradual unfreezing, or freezing early layers permanently).
  - "Does freeze_backbone=True still update BatchNorm running stats?" (yes
    unless you also call .eval() on those layers or set track_running_stats
    appropriately -- requires_grad=False only stops gradient updates, not
    BN's running mean/var updates during model.train()).
  - "Would you unfreeze layers all at once or gradually?" (gradual/progressive
    unfreezing from the head backward is the more defensible answer for a
    small dataset).

Gotchas to mention proactively:
  - Setting requires_grad=False on all params still leaves BatchNorm layers
    in train() mode updating running statistics -- a common transfer-learning
    bug if the model isn't also put in eval() for those layers or the whole
    backbone during frozen training.
  - The freeze loop runs before model.fc is reassigned, so the new fc layer
    is unaffected and remains trainable by default -- worth stating explicitly
    since it's easy to assume everything got frozen.
  - Using weights=...IMAGENET1K_V1 pins a specific pretrained checkpoint;
    forgetting to match the associated preprocessing/normalization transform
    silently hurts accuracy.
"""

from torch import nn
from torchvision import models


def build_model(num_classes: int, freeze_backbone: bool) -> nn.Module:
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

    if freeze_backbone:
        for param in model.parameters():
            param.requires_grad = False

    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model


if __name__ == "__main__":
    import torch
    m = build_model(10, freeze_backbone=True)
    x = torch.randn(2, 3, 224, 224)
    print(m(x).shape)  # (2, 10)
