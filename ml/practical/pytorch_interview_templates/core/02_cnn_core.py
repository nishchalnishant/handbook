"""Core: simple ConvNet (3 conv blocks + adaptive-pool classifier head).

INTERVIEW GUIDE
----------------
Typical ask: "Build a small CNN image classifier from scratch." Usually the
main problem in the first 25-30 min, right after an MLP warm-up, since it's
the natural next step once shapes and BatchNorm placement are established.

Expected depth (1hr session):
  - Junior/mid: get the conv/pool/BN/ReLU block order right, compute the
    spatial dims through each MaxPool2d(2) by hand, explain AdaptiveAvgPool2d(1)
    vs a Flatten+Linear head.
  - Senior: derive the receptive field growing through the 3 blocks, justify
    kernel_size=3/padding=1 as the "same" convolution default, and reason
    about when this shallow net would underfit vs. needing a deeper/resnet-style
    design.
  Takes 20-30 min including the arithmetic; commonly followed by "now add a
  residual connection" or a pivot into 03_resnet_transfer_core.py.

Common follow-ups:
  - "What's the output spatial size after each conv/pool?" (formula:
    floor((W - K + 2P)/S) + 1; here padding=1, kernel=3, stride=1 keeps
    spatial size, then MaxPool2d(2) halves it -- 32 -> 16 -> 8 -> 4).
  - "What's the receptive field at the end of the features block?" (grows
    with each 3x3 conv and doubles in stride terms with each pool; walk
    through it layer by layer rather than quoting a number from memory).
  - "Why convolutions instead of a plain MLP on flattened pixels?" (parameter
    sharing + translation equivariance + local connectivity -- an MLP would
    need a separate weight per pixel per input plus lose spatial structure).
  - "Why AdaptiveAvgPool2d(1) instead of flattening the feature map?" (makes
    the classifier input size independent of input image resolution, avoids
    a huge Linear layer, and acts as implicit regularization).
  - "What happens if you increase stride instead of using MaxPool2d?" (also
    downsamples but learns the downsampling filter -- a live tradeoff
    discussion, not a right/wrong answer).
  - "How would padding='valid' change the output shape here?" (spatial dims
    shrink every conv instead of staying fixed, changing the arithmetic above).

Gotchas to mention proactively:
  - BatchNorm2d normalizes over (N, H, W) per channel, not per-sample --
    breaks with batch_size=1 in train mode, same failure mode as the MLP case.
  - forward_cnn hardcodes the channel dim (128) into classifier's in_features;
    changing the number of conv blocks/channels means updating build_model's
    Linear(128, ...) too.
"""

from torch import nn, Tensor


def build_model(num_classes: int) -> nn.ModuleDict:
    return nn.ModuleDict({
        "features": nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1), nn.BatchNorm2d(32), nn.ReLU(inplace=True), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.BatchNorm2d(64), nn.ReLU(inplace=True), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1), nn.BatchNorm2d(128), nn.ReLU(inplace=True), nn.MaxPool2d(2),
        ),
        "pool": nn.AdaptiveAvgPool2d(1),
        "classifier": nn.Linear(128, num_classes),
    })


def forward_cnn(m: nn.ModuleDict, x: Tensor) -> Tensor:
    x = m["features"](x)
    x = m["pool"](x).flatten(1)
    return m["classifier"](x)


if __name__ == "__main__":
    import torch
    m = build_model(10)
    x = torch.randn(4, 3, 32, 32)
    print(forward_cnn(m, x).shape)  # (4, 10)
