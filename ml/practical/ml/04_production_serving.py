"""
ML PRODUCTION SERVING — FastAPI + saved sklearn pipeline
Interview talking points:
- serialize full Pipeline (preprocess + model together)
- version models, log predictions, monitor drift
- health check endpoint for k8s/load balancer
"""

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# pip install fastapi uvicorn pydantic

app = FastAPI(title="ML Inference API")
MODEL_PATH = "model_classification.joblib"

# Load once at startup (WHY: avoid reloading per request)
model_bundle = joblib.load(MODEL_PATH)
pipe = model_bundle["model"] if isinstance(model_bundle, dict) else model_bundle
threshold = model_bundle.get("threshold", 0.5) if isinstance(model_bundle, dict) else 0.5


class PredictionRequest(BaseModel):
    feature_a: float
    feature_b: float
    category_x: str


class PredictionResponse(BaseModel):
    label: int
    probability: float
    threshold_used: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    row = pd.DataFrame([req.model_dump()])
    proba = float(pipe.predict_proba(row)[0, 1])
    label = int(proba >= threshold)

    # TODO in interview: log to DB / Kafka for monitoring
    return PredictionResponse(label=label, probability=proba, threshold_used=threshold)


# Run: uvicorn ml.04_production_serving:app --reload --port 8000
