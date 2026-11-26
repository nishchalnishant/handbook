"""
============================================================
scikit-learn — Standard Workflow (classical ML, tabular classification)
============================================================
End-to-end pattern for a tabular classification problem: split before
touching statistics, preprocess numeric/categorical columns separately,
bundle preprocessing + model into one Pipeline so CV/search refit both
per fold, cross-validate, optionally tune, evaluate once on held-out
test data, then persist.

Pipeline:
  raw df -> train/test split (stratified) -> ColumnTransformer
  (impute+scale numeric, impute+one-hot categorical) -> Pipeline(preprocess, model)
  -> StratifiedKFold CV -> (optional) GridSearchCV -> fit on train
  -> evaluate once on test -> joblib.dump

WHY split before fitting anything:
  - Any statistic learned from the full dataset (scaler mean/std, imputer
    median, encoder categories) that later touches test data is leakage —
    it silently makes held-out performance optimistic.
  - Wrapping preprocessing in a Pipeline is what makes cross_val_score/
    GridSearchCV correct: each fold refits preprocessing on that fold's
    train split only, not on the whole training set.

# ============================================================
# Standard Workflow
# ============================================================
# 1. Load           — read data into a DataFrame
# 2. EDA            — df.info(), value_counts, isna().sum() (not modeling yet)
# 3. Split          — train_test_split(stratify=y) BEFORE any fitting
# 4. Preprocess     — ColumnTransformer split by numeric vs categorical dtype
# 5. Pipeline       — bundle preprocessing + model as one estimator
# 6. Cross-validate — StratifiedKFold + cross_val_score on train only
# 7. Tune           — GridSearchCV/RandomizedSearchCV with the same cv splitter
# 8. Final fit/eval — fit best pipeline on train, evaluate ONCE on test
# 9. Persist        — joblib.dump the fitted pipeline
# ============================================================
"""

import numpy as np
import pandas as pd

# pip install scikit-learn pandas numpy joblib imbalanced-learn
from sklearn.model_selection import (
    train_test_split, StratifiedKFold, cross_val_score, GridSearchCV,
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
TEST_SIZE = 0.2
RANDOM_STATE = 42
N_SPLITS = 5
MODEL_PATH = "model.pkl"


# ------------------------------------------------------------
# APPROACH A: Manual preprocessing (show you understand the internals)
# ------------------------------------------------------------
class LogTransformer(BaseEstimator, TransformerMixin):
    """Custom transformer example — drops into any Pipeline like a built-in step."""

    def __init__(self, cols=None):
        self.cols = cols

    def fit(self, X, y=None):
        return self  # no state to learn, but must return self

    def transform(self, X):
        X = X.copy()
        cols = self.cols or X.columns
        X[cols] = np.log1p(X[cols])
        return X


def make_manual_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """Split columns by dtype and build per-type impute+encode pipelines by hand."""
    numeric_features = X.select_dtypes(include="number").columns.tolist()
    categorical_features = X.select_dtypes(exclude="number").columns.tolist()

    return ColumnTransformer([
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), numeric_features),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]), categorical_features),
    ])


# ------------------------------------------------------------
# APPROACH B: Production pattern — same idea, wired as one reusable pipeline
# ------------------------------------------------------------
def build_pipeline(X: pd.DataFrame, model=None) -> Pipeline:
    preprocessor = make_manual_preprocessor(X)
    model = model or RandomForestClassifier(class_weight="balanced", random_state=RANDOM_STATE)
    return Pipeline([
        ("preprocess", preprocessor),
        ("clf", model),
    ])


# ------------------------------------------------------------
# APPROACH C: Advanced patterns (mention verbally, not exercised in main())
# ------------------------------------------------------------
# Imbalanced classes — resampling must happen INSIDE cross-validation:
#   from imblearn.over_sampling import SMOTE
#   from imblearn.pipeline import Pipeline as ImbPipeline
#   imb_pipe = ImbPipeline([("smote", SMOTE(random_state=42)), ("clf", RandomForestClassifier())])
#   imb_pipe.fit(X_train, y_train)   # SMOTE only ever sees training folds during CV
#
# Nested pipeline hyperparameter naming (step__substep__param):
#   param_grid = {
#       "clf__n_estimators": [100, 200, 300],
#       "preprocess__num__imputer__strategy": ["mean", "median"],
#   }
#
# Model comparison — swap the estimator, keep the same cv splitter:
#   for model in [LogisticRegression(max_iter=1000), RandomForestClassifier()]:
#       cross_val_score(build_pipeline(X_train, model), X_train, y_train, cv=cv)
#
# RandomizedSearchCV when GridSearchCV is too slow:
#   from sklearn.model_selection import RandomizedSearchCV
#   RandomizedSearchCV(pipe, param_distributions=param_grid, n_iter=20, cv=cv)


def _make_demo_data(n=500, random_state=RANDOM_STATE) -> pd.DataFrame:
    rng = np.random.RandomState(random_state)
    df = pd.DataFrame({
        "age": rng.normal(40, 12, n).round(1),
        "income": rng.exponential(50000, n).round(0),
        "city": rng.choice(["NYC", "SF", "Austin", None], size=n, p=[0.4, 0.3, 0.25, 0.05]),
        "target": rng.binomial(1, 0.3, n),
    })
    df.loc[rng.choice(n, size=n // 20, replace=False), "age"] = np.nan
    return df


def main() -> None:
    # 1. Load
    df = _make_demo_data()
    X, y = df.drop(columns=["target"]), df["target"]

    # 2. EDA (do this before modeling)
    print(y.value_counts(normalize=True))
    print(X.isna().sum())

    # 3. Split FIRST
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE,
    )

    # 4-5. Preprocessing + model bundled into one pipeline
    pipe = build_pipeline(X_train)

    # 6. Cross-validate on train only
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="f1_macro", n_jobs=-1)
    print(f"CV f1_macro: {scores.mean():.3f} +/- {scores.std():.3f}")

    # 7. Hyperparameter search — same cv splitter as above for comparability
    param_grid = {
        "clf__n_estimators": [100, 200],
        "clf__max_depth": [None, 10],
    }
    search = GridSearchCV(pipe, param_grid, cv=cv, scoring="f1_macro", n_jobs=-1)
    search.fit(X_train, y_train)
    best_pipe = search.best_estimator_
    print("Best params:", search.best_params_)

    # 8. Final fit + evaluate ONCE on held-out test set
    best_pipe.fit(X_train, y_train)
    preds = best_pipe.predict(X_test)
    proba = best_pipe.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, preds))
    print("ROC-AUC:", roc_auc_score(y_test, proba))

    # 9. Persist
    joblib.dump(best_pipe, MODEL_PATH)
    reloaded = joblib.load(MODEL_PATH)
    print("Reloaded pipeline predicts:", reloaded.predict(X_test[:5]))


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use this workflow:
#   - Any tabular classification/regression task with mixed numeric/categorical
#     features — the standard "give me an ML pipeline" interview ask.
#
# Pipeline vs. manual preprocessing:
#   - A bare ColumnTransformer/Pipeline is not optional in interviews: it's
#     what makes cross_val_score/GridSearchCV refit preprocessing correctly
#     per fold. Doing preprocessing by hand before CV is the #1 leakage bug.
#
# Critical failure modes (diagnose -> fix):
#   - Optimistic CV/test scores -> check whether scaler/imputer/encoder was
#     fit on the full dataset before splitting; fix by wrapping in Pipeline.
#   - OneHotEncoder crashes at inference -> unseen category not in training
#     folds; fix with handle_unknown="ignore".
#   - Accuracy looks great but model is useless -> check class balance
#     (y.value_counts(normalize=True)); switch to F1/PR-AUC, use
#     class_weight="balanced" or SMOTE inside an imblearn Pipeline.
#   - GridSearchCV too slow -> narrow the grid or switch to RandomizedSearchCV.
#
# Metrics:
#   - Balanced/imbalanced classification: f1_macro, roc_auc_score, PR-AUC.
#   - Always evaluate on the held-out test set exactly once, after model
#     selection is finalized via CV — repeated test-set peeking is itself
#     a form of leakage (overfitting to the test set via human choices).
#
# ============================================================
# VARIATIONS
# ============================================================
# - Regression: swap classifier for regressor, scoring="neg_mean_squared_error"
#   or "r2", drop stratify (or use bins on the target for stratified regression).
# - Multi-class: same code, most sklearn metrics accept average="macro"/"weighted".
# - Imbalanced classes: class_weight="balanced" first (cheapest fix); SMOTE via
#   imblearn.Pipeline only if that's insufficient.
# - Feature selection: insert SelectKBest/RFE as another ColumnTransformer/
#   Pipeline step so it's refit per fold too.
#
# ============================================================
# SUMMARY
# ============================================================
# - Use when: tabular data, need a defensible, leakage-free baseline pipeline.
# - Key decisions: split before fitting anything; wrap preprocessing+model in
#   one Pipeline; use the same cv splitter everywhere for comparability.
# - Key failure modes: preprocessing leakage, unseen categories at inference,
#   accuracy on imbalanced data, resampling before split.
# - Evaluation: CV score during model selection, single held-out test
#   evaluation at the end.
# - Production stack: same Pipeline object, persisted with joblib, reloaded
#   and called with .predict()/.predict_proba() directly — no separate
#   preprocessing code path to keep in sync.
# - Common mistakes: fit_transform on test data, forgetting random_state,
#   comparing models across different CV folds, scaling one-hot columns.
