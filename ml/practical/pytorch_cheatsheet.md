# PyTorch Cheat Sheet

## Tensors
```python
import torch

torch.tensor([1, 2, 3])
torch.zeros(3, 4)
torch.ones(3, 4)
torch.randn(3, 4)
torch.arange(0, 10)
torch.from_numpy(np_array)
tensor.numpy()
tensor.to("cuda")          # or "cpu", "mps"
tensor.dtype
tensor.shape / tensor.size()
tensor.view(-1, 4)
tensor.reshape(-1, 4)
tensor.permute(1, 0)
tensor.squeeze() / tensor.unsqueeze(0)
torch.cat([a, b], dim=0)
torch.stack([a, b], dim=0)
```

## Autograd
```python
x = torch.randn(3, requires_grad=True)
y = x.sum()
y.backward()
x.grad
with torch.no_grad():
    ...
x.detach()
```

## Device Handling
```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
x = x.to(device)
```

## Datasets & DataLoaders
```python
from torch.utils.data import Dataset, DataLoader, random_split, TensorDataset

class MyDataset(Dataset):
    def __len__(self): ...
    def __getitem__(self, idx): ...

loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)
```

## torchvision (common)
```python
from torchvision import datasets, transforms, models

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])
datasets.ImageFolder(root, transform=transform)
models.resnet18(weights="DEFAULT")
```

## Building Models
```python
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)

model = Net()
```

## Common Layers
```python
nn.Linear(in_f, out_f)
nn.Conv2d(in_c, out_c, kernel_size=3, stride=1, padding=1)
nn.MaxPool2d(2)
nn.BatchNorm2d(num_features)
nn.Dropout(p=0.5)
nn.Embedding(num_embeddings, embedding_dim)
nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
nn.MultiheadAttention(embed_dim, num_heads)
nn.TransformerEncoderLayer(d_model, nhead)
nn.Sequential(layer1, layer2, ...)
```

## Activations
```python
nn.ReLU()
nn.Sigmoid()
nn.Tanh()
nn.Softmax(dim=1)
nn.GELU()
nn.LeakyReLU()
```

## Loss Functions
```python
nn.CrossEntropyLoss()
nn.BCELoss()
nn.BCEWithLogitsLoss()
nn.MSELoss()
nn.L1Loss()
nn.NLLLoss()
```

## Optimizers
```python
from torch.optim import SGD, Adam, AdamW, RMSprop

optimizer = Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
optimizer.zero_grad()
optimizer.step()
```

## LR Schedulers
```python
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR, ReduceLROnPlateau

scheduler = StepLR(optimizer, step_size=10, gamma=0.1)
scheduler.step()
```

## Training Loop (typical)
```python
model.to(device)
for epoch in range(num_epochs):
    model.train()
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        preds = model(xb)
        loss = criterion(preds, yb)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        for xb, yb in val_loader:
            xb, yb = xb.to(device), yb.to(device)
            preds = model(xb)
            val_loss = criterion(preds, yb)
```

## Saving / Loading
```python
torch.save(model.state_dict(), "model.pt")
model.load_state_dict(torch.load("model.pt"))
model.eval()

torch.save(model, "full_model.pt")   # saves whole object
```

## Mixed Precision (AMP)
```python
scaler = torch.cuda.amp.GradScaler()

with torch.cuda.amp.autocast():
    preds = model(xb)
    loss = criterion(preds, yb)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

## Utilities
```python
torch.manual_seed(42)
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
sum(p.numel() for p in model.parameters())   # param count
model.parameters() / model.named_parameters()
model.state_dict()
```

## Standard Workflow (image classification, end-to-end)
```python
import torch, torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Data
train_tf = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
val_tf = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

train_ds = datasets.ImageFolder("data/train", transform=train_tf)
val_ds   = datasets.ImageFolder("data/val", transform=val_tf)
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=4)
val_loader   = DataLoader(val_ds, batch_size=32, shuffle=False, num_workers=4)

# 2. Model
model = models.resnet18(weights="DEFAULT")
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.to(device)

# 3. Loss / Optimizer / Scheduler
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

# 4. Train / validate loop
best_acc = 0.0
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        preds = model(xb)
        loss = criterion(preds, yb)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * xb.size(0)
    scheduler.step()
    train_loss = running_loss / len(train_ds)

    model.eval()
    correct = 0
    with torch.no_grad():
        for xb, yb in val_loader:
            xb, yb = xb.to(device), yb.to(device)
            preds = model(xb)
            correct += (preds.argmax(1) == yb).sum().item()
    val_acc = correct / len(val_ds)

    print(f"epoch {epoch}: train_loss={train_loss:.4f} val_acc={val_acc:.4f}")

    if val_acc > best_acc:
        best_acc = val_acc
        torch.save(model.state_dict(), "best_model.pt")

# 5. Inference
model.load_state_dict(torch.load("best_model.pt"))
model.eval()
with torch.no_grad():
    output = model(single_image.unsqueeze(0).to(device))
    pred_class = output.argmax(1).item()
```

## Transfer Learning

Two common strategies: **feature extraction** (freeze backbone, train only the new head) and **fine-tuning** (unfreeze some/all layers, train with a small LR).

### Feature extraction (frozen backbone)
```python
model = models.resnet18(weights="DEFAULT")

for param in model.parameters():
    param.requires_grad = False        # freeze everything

model.fc = nn.Linear(model.fc.in_features, num_classes)  # new head is trainable by default
model.to(device)

optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)  # only optimize the head
```

### Fine-tuning (unfreeze + small LR)
```python
model = models.resnet18(weights="DEFAULT")
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.to(device)

for param in model.parameters():
    param.requires_grad = True         # unfreeze all

optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)  # smaller LR than from-scratch training
```

### Partial unfreeze (common middle ground)
```python
for param in model.parameters():
    param.requires_grad = False

for param in model.layer4.parameters():   # unfreeze only last block + head
    param.requires_grad = True
model.fc = nn.Linear(model.fc.in_features, num_classes)

optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()), lr=1e-4
)
```

### Discriminative learning rates (lower LR for earlier layers)
```python
optimizer = torch.optim.Adam([
    {"params": model.layer1.parameters(), "lr": 1e-5},
    {"params": model.layer2.parameters(), "lr": 1e-5},
    {"params": model.layer3.parameters(), "lr": 1e-4},
    {"params": model.layer4.parameters(), "lr": 1e-4},
    {"params": model.fc.parameters(),     "lr": 1e-3},
])
```

**Typical transfer learning recipe:**
1. Load a pretrained model (`weights="DEFAULT"`).
2. Replace the final layer(s) to match `num_classes`.
3. Freeze the backbone, train only the head for a few epochs (feature extraction).
4. Unfreeze some/all layers and continue training with a much smaller LR (fine-tuning).
5. Use the same normalization stats (`mean`/`std`) the pretrained model was trained with.

## Custom Autograd Function
```python
class MyReLU(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return x.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        x, = ctx.saved_tensors
        grad_input = grad_output.clone()
        grad_input[x < 0] = 0
        return grad_input

y = MyReLU.apply(x)
```

## Reproducibility
```python
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)
np.random.seed(42)
random.seed(42)

torch.backends.cudnn.deterministic = True   # slower but reproducible
torch.backends.cudnn.benchmark = False       # True = faster but picks nondeterministic algos

def seed_worker(worker_id):
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)

DataLoader(dataset, worker_init_fn=seed_worker, generator=torch.Generator().manual_seed(42))
```

## Debugging NaN / Exploding Gradients
```python
# detect NaN/Inf during forward pass
torch.autograd.set_detect_anomaly(True)   # slow — dev only, pinpoints the op that produced NaN

# check for NaN in loss or tensors
torch.isnan(loss).any()
torch.isinf(loss).any()

# inspect gradient norms per layer (catch vanishing/exploding grads)
for name, p in model.named_parameters():
    if p.grad is not None:
        print(name, p.grad.norm().item())

# clip exploding gradients
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# check for NaN weights after a bad update
any(torch.isnan(p).any() for p in model.parameters())
```

## Multi-GPU
```python
# DataParallel — simplest, single-process, splits batch across GPUs (legacy, has overhead)
model = nn.DataParallel(model).to(device)

# DistributedDataParallel — preferred, multi-process, one process per GPU
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group(backend="nccl")
torch.cuda.set_device(local_rank)
model = model.to(local_rank)
model = DDP(model, device_ids=[local_rank])

# launch with: torchrun --nproc_per_node=NUM_GPUS train.py
```

## Training Debugging Checklist
- **Loss is `nan`/`inf`**: lower LR, check for `log(0)`/division by zero, clip gradients, check input data for NaNs, disable AMP to isolate.
- **Loss not decreasing at all**: verify LR isn't too small/large, check labels aren't shuffled/misaligned with inputs, confirm `optimizer.zero_grad()` is called each step, verify loss function matches output type (e.g. logits vs. probabilities).
- **Loss decreases then diverges**: LR too high, try a scheduler or warmup, add gradient clipping.
- **Shape mismatch errors**: print `.shape` at each layer boundary; common culprits are `batch_first` mismatches in RNN/Transformer layers and forgetting `.view()`/`.flatten()` before a `Linear`.
- **Model performs great on train, poor on val**: overfitting — add dropout/weight_decay/augmentation, reduce model capacity, early stopping.
- **`RuntimeError: expected all tensors on same device`**: some tensor wasn't moved with `.to(device)` — usually a newly created tensor inside `forward` (e.g. `torch.zeros(...)` without `device=`).
- **Training is very slow**: check `num_workers` in `DataLoader`, verify data augmentation isn't happening on CPU unnecessarily, confirm GPU is actually being used (`next(model.parameters()).device`), profile with `torch.profiler`.
- **`loss.backward()` fails with "trying to backward through the graph a second time"**: a tensor is being reused across iterations without detaching, or `retain_graph=True` is needed for a legitimate multi-backward use case.
- **Val accuracy identical to random guessing**: check `model.eval()` is set (dropout/batchnorm behave differently in train mode), confirm labels/classes weren't accidentally shuffled differently than inputs.
