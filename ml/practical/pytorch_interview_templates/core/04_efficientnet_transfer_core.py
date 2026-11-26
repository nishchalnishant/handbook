"""Core: EfficientNet-B0 transfer learning — replace classifier head, optionally freeze backbone.

INTERVIEW GUIDE
----------------
Typical ask: "Same transfer-learning task, but now with EfficientNet instead
of ResNet -- what changes?" Almost always a stretch-goal/follow-up after
03_resnet_transfer_core.py rather than a standalone opener, used to test
whether the candidate actually understands the model or just memorized one
API pattern.

Expected depth (1hr session):
  - Junior/mid: notice that the classifier head isn't a single Linear like
    ResNet's fc, correctly index model.classifier[1] and pull in_features
    from it instead of guessing a hardcoded value.
  - Senior: explain compound scaling conceptually (why B0 vs B7 differ in
    depth/width/resolution together, not just one dial) and argue for
    EfficientNet vs ResNet on accuracy-per-FLOP grounds, not "it's newer."
  Quick if the candidate already did the ResNet version (10-15 min); the
  value here is almost entirely in catching the classifier[1] indexing quirk
  and the compound-scaling explanation.

Common follow-ups:
  - "Why is it classifier[1] and not classifier like ResNet's fc?" (EfficientNet's
    classifier is nn.Sequential(Dropout, Linear) -- index 0 is dropout, index
    1 is the actual Linear layer being replaced; ResNet's fc is directly a
    Linear).
  - "What is compound scaling and why does it matter?" (EfficientNet scales
    depth, width, and input resolution together via a fixed compound
    coefficient rather than scaling one dimension at a time, which is what
    gives the B0-B7 family better accuracy/FLOP tradeoffs than naively
    stacking more ResNet layers).
  - "Why choose EfficientNet over ResNet18 here at all?" (better accuracy per
    parameter/FLOP on ImageNet-scale benchmarks; tradeoff is EfficientNet can
    be slower in wall-clock time on some hardware due to depthwise convs
    despite fewer FLOPs).
  - "Does freeze_backbone freeze the Dropout in classifier[0] too?" (dropout
    has no parameters, so requires_grad=False is a no-op there; only
    classifier[1]'s Linear weights matter, and that gets replaced anyway).
  - "If num_classes changes, does anything else in the architecture need to
    change?" (no -- same pattern as ResNet, only the final Linear's out_features
    changes since in_features is read dynamically).
  - "How would B0 vs B4 change your fine-tuning approach?" (larger variants
    have more capacity but also more risk of overfitting a small target
    dataset -- freezing more aggressively becomes more attractive).

Gotchas to mention proactively:
  - model.classifier[1].in_features -- if someone mimics the ResNet pattern
    and writes model.classifier.in_features, it breaks immediately since
    classifier is a Sequential, not a Linear; this is the single most common
    slip when porting the ResNet snippet.
  - Same BatchNorm-running-stats caveat as ResNet: requires_grad=False on all
    params does not stop BN layers from updating running mean/var while the
    model is in train() mode.
  - EfficientNet expects the same normalization stats as its own pretrained
    weights (via EfficientNet_B0_Weights.IMAGENET1K_V1.transforms()), not
    necessarily identical to the ResNet preprocessing pipeline.
"""

from torch import nn
from torchvision import models


def build_model(num_classes: int, freeze_backbone: bool) -> nn.Module:
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)

    if freeze_backbone:
        for param in model.parameters():
            param.requires_grad = False

    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model


if __name__ == "__main__":
    import torch
    m = build_model(10, freeze_backbone=True)
    x = torch.randn(2, 3, 224, 224)
    print(m(x).shape)  # (2, 10)
