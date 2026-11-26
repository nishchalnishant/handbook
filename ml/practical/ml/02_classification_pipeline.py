"""
ML CLASSIFICATION — end-to-end skeleton (sklearn)
Use when: predict a discrete label (churn, fraud, spam, disease)

WHY LogisticRegression: strong linear baseline, calibrated probabilities.
WHY RandomForest: nonlinear, handles mixed feature types, feature importance.
WHY XGBoost/LightGBM: best tabular performance in most real-world datasets.
"""

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# from xgboost import XGBClassifier


TARGET = "label"
NUMERIC_FEATURES = ["feature_a", "feature_b"]
CATEGORICAL_FEATURES = ["category_x"]


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )


def build_model(name: str = "logistic"):
    """
    LogisticRegression → fast, interpretable, good when data is ~linearly separable
    RandomForest       → nonlinear, no heavy tuning needed
    XGBClassifier      → tabular winner; use when accuracy matters most
    """
    models = {
        "logistic": LogisticRegression(max_iter=1000, random_state=42),
        "rf": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
        # "xgb": XGBClassifier(n_estimators=200, learning_rate=0.05, eval_metric="logloss", random_state=42),
    }
    return models[name]


def build_pipeline(model_name: str = "logistic") -> Pipeline:
    return Pipeline([
        ("preprocess", build_preprocessor()),
        ("model", build_model(model_name)),
    ])


def train_and_evaluate(df: pd.DataFrame, model_name: str = "logistic"):
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    # WHY stratify=y: preserves class ratio in train/test (critical for imbalanced-ish data)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = build_pipeline(model_name)
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]  # binary; use [:, 1] for positive class

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }

    print(metrics)
    print(classification_report(y_test, y_pred))
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

    # WHY cross_val_score: more reliable than single holdout split
    cv_scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="f1")
    print(f"CV F1: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

    return pipe, metrics


def save_model(pipe: Pipeline, path: str = "model_classification.joblib"):
    joblib.dump(pipe, path)


def load_model(path: str = "model_classification.joblib") -> Pipeline:
    return joblib.load(path)


def predict(pipe: Pipeline, raw_input: dict) -> dict:
    row = pd.DataFrame([raw_input])
    label = pipe.predict(row)[0]
    proba = pipe.predict_proba(row)[0]
    return {"label": int(label), "probabilities": proba.tolist()}


if __name__ == "__main__":
    pass
