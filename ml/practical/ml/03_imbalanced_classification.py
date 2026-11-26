"""
ML IMBALANCED CLASSIFICATION — fraud, churn, rare disease, spam
Problem: model predicts majority class always → high accuracy, useless model.

Strategies (combine 2-3 in interviews):
1. class_weight='balanced'     → easiest, no extra data
2. SMOTE oversampling          → synthetic minority samples (train only!)
3. threshold tuning            → optimize F1/precision/recall for business goal
4. use PR-AUC not ROC-AUC       → ROC is optimistic when negatives dominate
"""

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline  # wraps SMOTE inside CV safely
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET = "label"
NUMERIC_FEATURES = ["feature_a", "feature_b"]
CATEGORICAL_FEATURES = ["category_x"]


def build_preprocessor():
    return ColumnTransformer([
        ("num", StandardScaler(), NUMERIC_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ])


def build_model(strategy: str = "class_weight"):
    """
    class_weight → penalize misclassifying minority more (Logistic/RF/XGB all support)
    SMOTE        → generate synthetic minority points after preprocessing
    """
    if strategy == "class_weight":
        # WHY: zero code change to data pipeline; good first attempt
        return LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    return RandomForestClassifier(
        n_estimators=200, class_weight="balanced", random_state=42, n_jobs=-1
    )


# --- APPROACH A: class_weight only (simplest) ---
def train_with_class_weights(df: pd.DataFrame):
    from sklearn.pipeline import Pipeline

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = Pipeline([
        ("preprocess", build_preprocessor()),
        ("model", build_model("class_weight")),
    ])
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]

    print("F1:", f1_score(y_test, y_pred))
    print("PR-AUC:", average_precision_score(y_test, y_proba))  # WHY: better for imbalance
    print(classification_report(y_test, y_pred))
    return pipe


# --- APPROACH B: SMOTE (apply ONLY on training fold inside pipeline) ---
def train_with_smote(df: pd.DataFrame):
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # WHY ImbPipeline: SMOTE runs after preprocess, before model, only on train folds in CV
    pipe = ImbPipeline([
        ("preprocess", build_preprocessor()),
        ("smote", SMOTE(random_state=42)),  # NEVER apply SMOTE to test set
        ("model", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]
    print("F1:", f1_score(y_test, y_pred))
    print("PR-AUC:", average_precision_score(y_test, y_proba))
    return pipe


# --- THRESHOLD TUNING (critical for production) ---
def find_best_threshold(y_true, y_proba, metric: str = "f1"):
    """
    Default threshold=0.5 assumes balanced classes.
    WHY tune: fraud detection may want high precision (low false alarms) → threshold ↑
    """
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_proba)

    best_t, best_score = 0.5, 0
    for t in thresholds:
        preds = (y_proba >= t).astype(int)
        score = f1_score(y_true, preds) if metric == "f1" else 0
        if score > best_score:
            best_score, best_t = score, t

    print(f"Best threshold: {best_t:.3f}, {metric}: {best_score:.3f}")
    return best_t


# --- STRATIFIED K-FOLD (always for imbalanced) ---
def cross_validate_imbalanced(df: pd.DataFrame):
    from sklearn.pipeline import Pipeline

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    pipe = Pipeline([
        ("preprocess", build_preprocessor()),
        ("model", LogisticRegression(class_weight="balanced", max_iter=1000)),
    ])

    # WHY StratifiedKFold: each fold keeps class ratio
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = []
    for train_idx, val_idx in skf.split(X, y):
        pipe.fit(X.iloc[train_idx], y.iloc[train_idx])
        proba = pipe.predict_proba(X.iloc[val_idx])[:, 1]
        scores.append(average_precision_score(y.iloc[val_idx], proba))

    print(f"CV PR-AUC: {np.mean(scores):.3f} (+/- {np.std(scores):.3f})")


def save_model(pipe, path: str = "model_imbalanced.joblib"):
    joblib.dump({"model": pipe, "threshold": 0.5}, path)  # store tuned threshold too


if __name__ == "__main__":
    pass
