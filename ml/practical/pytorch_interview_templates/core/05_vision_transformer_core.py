"""Core: ViT from scratch — patch embed + [CLS] token + pos embed + pre-norm encoder blocks.

INTERVIEW GUIDE
----------------
Typical ask: "Implement a Vision Transformer from scratch (patchify, add a
class token, run through transformer blocks)." This is a senior-leaning main
problem, usually 35-45 min of the hour on its own since it touches
convolution-as-patchify, attention, and normalization placement all at once.

Expected depth (1hr session):
  - Junior/mid: get the patch embedding shape transformations right (B,C,H,W)
    -> (B, embed_dim, num_patches) -> (B, num_patches, embed_dim) via
    forward_patch_embedding, and correctly prepend the cls_token before
    adding pos_embed in forward_vit_from_scratch.
  - Senior: justify implementing patch embedding as a strided Conv2d
    (kernel_size=patch_size, stride=patch_size) instead of manual
    reshape+Linear, explain why norm1/norm2 are applied before attn/mlp
    (pre-norm) rather than after, and discuss why ViT needs much more
    pretraining data than a CNN of similar size.
  Frequently the whole hour; a common stretch goal is "add dropout on the
  patch/pos embeddings" or "swap pre-norm for post-norm and explain the
  training stability difference."

Common follow-ups:
  - "Why is patch embedding implemented as a Conv2d instead of flatten+Linear?"
    (mathematically equivalent to an unfold + Linear projection per patch,
    but the strided conv gets you the patchify-and-project in one fused,
    efficient op -- kernel_size=patch_size, stride=patch_size means each
    patch is seen exactly once with no overlap).
  - "What is the CLS token for and why prepend it before adding positional
    embeddings?" (a learnable token with no inherent spatial location that
    aggregates global information via self-attention across all patches;
    forward_vit_from_scratch concatenates it first so pos_embed's shape
    (num_patches + 1) has a slot reserved for it -- get the order wrong and
    the positional embedding misaligns with the patches).
  - "Why does ViT need more training data than a CNN?" (CNNs have a built-in
    inductive bias -- locality and translation equivariance from convolution
    -- while ViT's attention is a much less constrained function class that
    has to learn spatial structure from data rather than getting it for free;
    this is why ViT underperforms CNNs on small datasets like CIFAR without
    heavy pretraining or augmentation).
  - "Why use a learned pos_embed (nn.Parameter) instead of sinusoidal
    positional encodings?" (learned embeddings are simpler and work well
    empirically at fixed resolution; sinusoidal generalizes better to unseen
    sequence lengths, but ViT's num_patches is typically fixed per training
    config anyway, so that advantage matters less here).
  - "Why pre-norm (norm before attn/mlp) instead of post-norm?" (pre-norm --
    as used in build_vit_encoder_block/forward_vit_encoder_block -- keeps a
    clean residual/highway path from input to output, giving more stable
    gradients and removing the need for learning-rate warmup tricks that
    post-norm transformers required originally).
  - "What happens if img_size isn't divisible by patch_size?" (num_patches =
    (img_size // patch_size) ** 2 silently floors and drops pixels at the
    edges rather than erroring -- worth flagging as a silent correctness bug).

Gotchas to mention proactively:
  - m.cls_token.expand(B, -1, -1) creates a view, not a copy -- fine here
    since it's only read, but would be a bug if code later mutated it in
    place expecting per-sample independence.
  - forward_vit_encoder_block applies attention with query=key=value=normed
    (self-attention) and passes need_weights=False purely for a speed/memory
    win -- if someone needed attention maps for visualization they'd have to
    change that flag, which changes the return signature.
  - trunc_normal_(std=0.02) initialization for cls_token/pos_embed matters --
    initializing these as zeros (as torch.zeros allocates before the
    trunc_normal_ call overwrites them) or with too large a std can visibly
    hurt early training convergence.
"""

import torch
from torch import nn, Tensor


def build_patch_embedding(img_size: int, patch_size: int, in_channels: int, embed_dim: int) -> nn.ModuleDict:
    m = nn.ModuleDict({
        "proj": nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size),
    })
    m.num_patches = (img_size // patch_size) ** 2
    return m


def forward_patch_embedding(m: nn.ModuleDict, x: Tensor) -> Tensor:
    x = m["proj"](x)        # (B, embed_dim, H/P, W/P)
    x = x.flatten(2)        # (B, embed_dim, num_patches)
    return x.transpose(1, 2)  # (B, num_patches, embed_dim)


def build_vit_encoder_block(embed_dim: int, num_heads: int, mlp_ratio: int = 4, dropout: float = 0.1) -> nn.ModuleDict:
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
    x = x + attn_out
    return x + m["mlp"](m["norm2"](x))


def build_vit_from_scratch(
    img_size: int = 224, patch_size: int = 16, in_channels: int = 3,
    embed_dim: int = 256, depth: int = 6, num_heads: int = 8, num_classes: int = 5,
) -> nn.ModuleDict:
    patch_embed = build_patch_embedding(img_size, patch_size, in_channels, embed_dim)
    num_patches = patch_embed.num_patches

    m = nn.ModuleDict({
        "patch_embed": patch_embed,
        "blocks": nn.ModuleList([build_vit_encoder_block(embed_dim, num_heads) for _ in range(depth)]),
        "norm": nn.LayerNorm(embed_dim),
        "head": nn.Linear(embed_dim, num_classes),
    })
    cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
    pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
    nn.init.trunc_normal_(pos_embed, std=0.02)
    nn.init.trunc_normal_(cls_token, std=0.02)
    m.cls_token = cls_token
    m.pos_embed = pos_embed
    return m


def forward_vit_from_scratch(m: nn.ModuleDict, x: Tensor) -> Tensor:
    B = x.shape[0]
    x = forward_patch_embedding(m["patch_embed"], x)
    cls_tokens = m.cls_token.expand(B, -1, -1)
    x = torch.cat([cls_tokens, x], dim=1)
    x = x + m.pos_embed
    for block in m["blocks"]:
        x = forward_vit_encoder_block(block, x)
    x = m["norm"](x)
    return m["head"](x[:, 0])


if __name__ == "__main__":
    m = build_vit_from_scratch(img_size=32, patch_size=8, embed_dim=64, depth=2, num_heads=4, num_classes=10)
    x = torch.randn(2, 3, 32, 32)
    print(forward_vit_from_scratch(m, x).shape)  # (2, 10)
