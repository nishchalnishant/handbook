"""
DL PRODUCTION SERVING — TorchScript export + FastAPI
Interview points:
- export to TorchScript or ONNX for faster inference
- batch predictions, GPU warmup, model versioning
"""

import json

import torch
import torch.nn as nn
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from torchvision import transforms

# from dl.classification_pytorch import SimpleCNN, build_model

app = FastAPI(title="DL Inference API")
DEVICE = torch.device("cpu")  # WHY cpu in prod API unless high throughput

MODEL_PATH = "artifacts_classification/model.pt"
CLASSES_PATH = "artifacts_classification/classes.json"

# Load at startup
with open(CLASSES_PATH) as f:
    CLASS_NAMES = json.load(f)

# model = build_model(num_classes=len(CLASS_NAMES))
# model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
# model.eval()

# WHY TorchScript: removes Python GIL dependency, faster in production
# scripted = torch.jit.script(model)
# torch.jit.save(scripted, "model_scripted.pt")

TRANSFORM = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    tensor = TRANSFORM(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        # logits = model(tensor)
        # probs = torch.softmax(logits, dim=1)[0]
        pass  # fill in during interview

    # top_class = probs.argmax().item()
    # return {"label": CLASS_NAMES[top_class], "confidence": float(probs[top_class])}
    return {"label": "placeholder", "confidence": 0.0}


# Run: uvicorn dl.04_production_serving:app --port 8001
