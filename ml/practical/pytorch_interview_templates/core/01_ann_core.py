"""Core: feedforward MLP (Linear -> BatchNorm -> ReLU -> Dropout, repeated).

INTERVIEW GUIDE
----------------
Typical ask: "Build an MLP classifier from scratch for tabular/simple data."
Framed as a warm-up problem in the first 10-15 min, or as the base case
before pivoting to a harder architecture.

Expected depth (1hr session):
  - Junior/mid: write build+forward, explain why BatchNorm/Dropout placement
    matters, get the shapes right on first try.
  - Senior: also asked to justify hidden_dims choice, discuss overfitting
    signals, and reason about BatchNorm vs LayerNorm tradeoffs live.
  Rarely the whole hour on its own -- usually a 10-15 min opener before a
  follow-up ("now add residual connections", "now make it work for
  regression instead of classification").

Common follow-ups:
  - "Why BatchNorm before or after ReLU?" (here: before -- normalize the
    pre-activation, standard practice, though after-activation works too).
  - "What breaks with batch_size=1?" (BatchNorm needs >1 sample per batch
    in train mode; use LayerNorm or eval() as workaround).
  - "How would you add residual/skip connections here?"
  - "How do you handle class imbalance?" (class weights in loss, not model).
  - "Convert this to a regression head" (drop final activation, change loss).

Gotchas to mention proactively:
  - Dropout/BatchNorm behave differently in train() vs eval() -- call out
    model.eval() before inference or dropout stays active.
  - nn.Sequential can't do skip connections -- would need ModuleList/ModuleDict
    if asked to extend this.
"""

from torch import nn


def build_model(input_dim: int, hidden_dims: tuple[int, ...], num_classes: int, dropout: float) -> nn.Sequential:
    layers: list[nn.Module] = []
    prev_dim = input_dim
    for h in hidden_dims:
        layers.extend([
            nn.Linear(prev_dim, h),
            nn.BatchNorm1d(h),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
        ])
        prev_dim = h
    layers.append(nn.Linear(prev_dim, num_classes))
    return nn.Sequential(*layers)


if __name__ == "__main__":
    import torch
    m = build_model(20, (128, 64), 3, 0.2)
    x = torch.randn(8, 20)
    print(m(x).shape)  # (8, 3)
