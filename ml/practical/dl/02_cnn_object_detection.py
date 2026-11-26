"""
DL USE CASE: Object Detection (bounding boxes)
Examples: retail shelf monitoring, autonomous driving, security cameras

WHY not plain CNN classifier: need WHERE object is, not just WHAT.
WHY Faster R-CNN / RetinaNet: two-stage (region proposal + classify) — accurate.
WHY YOLO: single-pass, real-time — use when latency matters.
Interview: mention torchvision detection models OR ultralytics YOLO wrapper.
"""

import torch
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torch.utils.data import DataLoader, Dataset
from PIL import Image

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DetectionDataset(Dataset):
    """
    Each sample returns: image tensor + target dict
    target = {"boxes": FloatTensor[N,4], "labels": IntTensor[N]}
    box format: [x_min, y_min, x_max, y_max] in pixels
    """

    def __init__(self, image_paths, annotations, transform=None):
        self.image_paths = image_paths
        self.annotations = annotations  # list of dicts with boxes + labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")
        target = self.annotations[idx]
        if self.transform:
            image = self.transform(image)
        return image, target


def build_detection_model(num_classes: int):
    """
    WHY Faster R-CNN + FPN: Feature Pyramid Network handles multi-scale objects.
    num_classes includes background class (+1).
    """
    weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
    model = fasterrcnn_resnet50_fpn(weights=weights)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes + 1)
    return model


def train_one_epoch(model, loader, optimizer):
    model.train()
    for images, targets in loader:
        images = [img.to(DEVICE) for img in images]
        targets = [{k: v.to(DEVICE) for k, v in t.items()} for t in targets]
        optimizer.zero_grad()
        loss_dict = model(images, targets)  # returns losses during training
        loss = sum(loss_dict.values())
        loss.backward()
        optimizer.step()


@torch.no_grad()
def predict(model, image_path: str, score_threshold: float = 0.5):
    model.eval()
    image = Image.open(image_path).convert("RGB")
    tensor = torchvision.transforms.functional.to_tensor(image).to(DEVICE)
    outputs = model([tensor])[0]

    # WHY threshold: filter low-confidence detections for production
    keep = outputs["scores"] > score_threshold
    boxes = outputs["boxes"][keep].cpu()
    labels = outputs["labels"][keep].cpu()
    scores = outputs["scores"][keep].cpu()
    return {"boxes": boxes, "labels": labels, "scores": scores}


# --- YOLO alternative (mention in interview) ---
def train_yolo():
    """
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")  # nano = fastest; use m/l for accuracy
    model.train(data="dataset.yaml", epochs=50, imgsz=640)
    WHY YOLO: end-to-end, real-time (~30+ FPS), simpler API than Faster R-CNN
    """
    pass
