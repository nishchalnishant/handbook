"""
============================================================
TEMPLATE 8: Decision Tree Classifier
============================================================
Non-linear, interpretable tree-based classifier. First tree-based template
in the series — introduces feature_importances_, max_depth/overfitting
control, and tree visualization concepts. Interview-scoped (~45 min).
============================================================
"""

# ============================================================
# General ML Model Development Workflow (Scikit-learn)
# ============================================================
# 1. Understand the Data
#    - Load the dataset
#    - Perform EDA
#    - Identify the target variable
#    - Check missing values, duplicates, outliers, class imbalance
# 2. Split the Data
#    - Separate features (X) and target (y)
#    - Perform Train/Test split
#    - Create Validation split if required
#    - Use stratified split for classification when needed
# 3. Prepare the Data
#    - Identify numerical and categorical features
#    - Build preprocessing pipelines
#        * Impute missing values
#        * Scale numerical features
#        * Encode categorical features
#        * Perform feature engineering (if required)
#    - Combine preprocessing using ColumnTransformer
#    - Create a complete Scikit-learn Pipeline
# 4. Train the Model
#    - Start with a simple baseline model
#    - Train multiple candidate models
#    - Fit the pipeline on the training data
# 5. Evaluate the Model
#    - Make predictions on validation/test data
#    - Evaluate using appropriate metrics
#    - Perform error analysis
# 6. Improve the Model
#    - Compare different models
#    - Perform Cross-Validation
#    - Tune hyperparameters
#    - Perform feature selection/engineering
#    - Handle overfitting or underfitting
# 7. Finalize the Model
#    - Select the best-performing model
#    - Evaluate once on the unseen test set
#    - Save the trained pipeline/model
# 8. Deploy & Monitor
#    - Load the saved model
#    - Make predictions on new data
#    - Monitor model performance
#    - Monitor data drift and concept drift
#    - Retrain the model when necessary
# ============================================================

# ------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

# ------------------------------------------------------------
# 2. Configuration (plain variables, no config class)
# ------------------------------------------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
DATA_PATH = "data.csv"
TARGET_COLUMN = "target"
MODEL_PATH = "decision_tree_classifier_pipeline.joblib"
MAX_DEPTH_GRID = [3, 5, 7, 10, None]
MIN_SAMPLES_LEAF_GRID = [1, 5, 10, 20]

np.random.seed(RANDOM_SEED)


# ------------------------------------------------------------
# 3. Load Dataset
# ------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        rng = np.random.default_rng(RANDOM_SEED)
        n = 1500
        df = pd.DataFrame(
            {
                "num_feature_1": rng.normal(50, 10, n),
                "num_feature_2": rng.normal(20, 5, n),
                "cat_feature_1": rng.choice(["A", "B", "C"], n),
            }
        )
        df.loc[df.sample(frac=0.05, random_state=RANDOM_SEED).index, "num_feature_2"] = np.nan
        # Non-linear decision boundary (trees can capture interactions/
        # thresholds that linear models like LogisticRegression cannot).
        logit = np.where(
            (df["num_feature_1"] > 55) & (df["num_feature_2"] < 22),
            2.0,
            -1.5,
        )
        prob = 1 / (1 + np.exp(-logit))
        df[TARGET_COLUMN] = (prob > 0.5).astype(int)
    return df


# ------------------------------------------------------------
# 4. EDA
# ------------------------------------------------------------
def run_eda(df: pd.DataFrame) -> None:
    print("Shape:", df.shape)
    print("\nDtypes:\n", df.dtypes)
    print("\nMissing values:\n", df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nDescribe:\n", df.describe())
    print("\nClass distribution:\n", df[TARGET_COLUMN].value_counts(normalize=True))
    numeric_df = df.select_dtypes(include=np.number)
    print("\nCorrelation matrix:\n", numeric_df.corr())


# ------------------------------------------------------------
# 5. Train/Test Split
# ------------------------------------------------------------
def split_data(df: pd.DataFrame):
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    # Stratify to preserve class ratio in both splits, important since
    # trees can overfit rare classes if the split skews imbalance further.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
    )
    return X_train, X_test, y_train, y_test


# ------------------------------------------------------------
# 6 & 7. Feature Engineering + Preprocessing Pipeline
# ------------------------------------------------------------
def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_features = X.select_dtypes(include=np.number).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()

    # Trees are scale-invariant (splits depend on ordering, not magnitude),
    # so StandardScaler is not strictly required, but kept here for pipeline
    # consistency and in case the pipeline is later swapped to a linear model.
    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features),
    ])
    return preprocessor


# ------------------------------------------------------------
# 8 & 9. Model Construction + Training
# ------------------------------------------------------------
def build_pipeline(
    preprocessor: ColumnTransformer, max_depth: int | None = 5, min_samples_leaf: int = 5
) -> Pipeline:
    # max_depth and min_samples_leaf are the primary overfitting controls —
    # an unconstrained tree (max_depth=None) will memorize the training set.
    model = DecisionTreeClassifier(
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        criterion="gini",
        class_weight="balanced",
        random_state=RANDOM_SEED,
    )
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ])
    return pipeline


def train(pipeline: Pipeline, X_train, y_train) -> Pipeline:
    pipeline.fit(X_train, y_train)
    return pipeline


# ------------------------------------------------------------
# 10. Evaluation
# ------------------------------------------------------------
def evaluate(pipeline: Pipeline, X_train, y_train, X_test, y_test) -> dict:
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }
    print("\nTest metrics:")
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")

    print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification report:\n", classification_report(y_test, y_pred))


    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=CV_FOLDS, scoring="f1")
    print(f"\nCV F1 mean +/- std: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
    return metrics


# ------------------------------------------------------------
# 11. Hyperparameter Tuning
# ------------------------------------------------------------
def tune_hyperparameters(X_train, y_train, preprocessor: ColumnTransformer) -> Pipeline:
    pipeline = build_pipeline(preprocessor)
    param_grid = {
        "model__max_depth": MAX_DEPTH_GRID,
        "model__min_samples_leaf": MIN_SAMPLES_LEAF_GRID,
    }

    grid_search = GridSearchCV(pipeline, param_grid, cv=CV_FOLDS, scoring="f1", n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print(f"\nBest params: {grid_search.best_params_}")
    print(f"Best CV F1: {grid_search.best_score_:.4f}")
    return grid_search.best_estimator_


# ------------------------------------------------------------
# 12. Model Comparison
# ------------------------------------------------------------
def compare_models(X_train, y_train, preprocessor: ColumnTransformer) -> None:
    candidates = {
        "Dummy (most_frequent)": DummyClassifier(strategy="most_frequent"),
        "Dummy (stratified)": DummyClassifier(strategy="stratified", random_state=RANDOM_SEED),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_SEED),
        "Decision Tree (max_depth=5)": DecisionTreeClassifier(max_depth=5, random_state=RANDOM_SEED),
        "Decision Tree (unconstrained)": DecisionTreeClassifier(random_state=RANDOM_SEED),
    }
    print("\nModel comparison (CV F1):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="f1")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # An unconstrained tree usually shows high train accuracy but similar or
    # worse CV score than a depth-limited tree — a live overfitting example.


# ------------------------------------------------------------
# 13. Error Analysis
# ------------------------------------------------------------
def error_analysis(pipeline: Pipeline, X_test, y_test) -> None:
    y_pred = pipeline.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print(f"\nTN={tn}, FP={fp}, FN={fn}, TP={tp}")

    misclassified_mask = y_pred != y_test.values
    print(f"\nMisclassified samples: {misclassified_mask.sum()} / {len(y_test)}")
    print(X_test[misclassified_mask].head())


# ------------------------------------------------------------
# 14. Feature Importance
# ------------------------------------------------------------
def feature_importance(pipeline: Pipeline) -> None:
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()
    importance_df = pd.DataFrame(
        {"feature": feature_names, "importance": model.feature_importances_}
    ).sort_values("importance", ascending=False)
    print("\nFeature importances (Gini importance):")
    print(importance_df)


# ------------------------------------------------------------
# 15. Save Model
# ------------------------------------------------------------
def save_model(pipeline: Pipeline, path: str) -> None:
    joblib.dump(pipeline, path)
    print(f"\nSaved pipeline to {path}")


# ------------------------------------------------------------
# 16. Load Model
# ------------------------------------------------------------
def load_model(path: str) -> Pipeline:
    return joblib.load(path)


# ------------------------------------------------------------
# 17. Prediction Example
# ------------------------------------------------------------
def predict_new_sample(pipeline: Pipeline) -> None:
    new_sample = pd.DataFrame(
        {
            "num_feature_1": [60.0],
            "num_feature_2": [18.0],
            "cat_feature_1": ["A"],
        }
    )
    prediction = pipeline.predict(new_sample)
    probability = pipeline.predict_proba(new_sample)[:, 1]
    print(f"\nPrediction on new sample: {prediction[0]} (P(class=1)={probability[0]:.4f})")


# ------------------------------------------------------------
# 18. Main
# ------------------------------------------------------------
def main() -> None:
    df = load_data(DATA_PATH)
    run_eda(df)

    X_train, X_test, y_train, y_test = split_data(df)

    preprocessor = build_preprocessor(X_train)
    pipeline = build_pipeline(preprocessor)
    pipeline = train(pipeline, X_train, y_train)

    evaluate(pipeline, X_train, y_train, X_test, y_test)
    compare_models(X_train, y_train, preprocessor)

    best_pipeline = tune_hyperparameters(X_train, y_train, preprocessor)
    error_analysis(best_pipeline, X_test, y_test)
    feature_importance(best_pipeline)

    save_model(best_pipeline, MODEL_PATH)
    loaded_pipeline = load_model(MODEL_PATH)
    predict_new_sample(loaded_pipeline)


if __name__ == "__main__":
    main()


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# When to use: classification problems with non-linear decision boundaries,
#   feature interactions, mixed numeric/categorical data, or when model
#   interpretability via explicit if/else rules is valuable.
# Mathematical intuition: recursively partitions the feature space by
#   choosing, at each node, the feature/threshold split that most reduces
#   impurity (Gini impurity or entropy) between the resulting child nodes.
# Advantages: no feature scaling required, handles non-linear relationships
#   and feature interactions natively, human-readable decision rules, fast
#   inference.
# Disadvantages: prone to overfitting if unconstrained, unstable (small data
#   changes can produce very different trees), biased toward features with
#   more levels/splits, poor extrapolation outside training data range.
# Bias-variance: shallow trees (low max_depth) = high bias/low variance;
#   deep unconstrained trees = low bias/high variance (overfitting).
# Assumptions: none about feature distribution/linearity; assumes recursive
#   axis-aligned splits are a reasonable model of the decision boundary.
# Time complexity: O(n * d * log(n)) for training (n samples, d features).
# Space complexity: O(nodes), bounded by max_depth/max_leaf_nodes.
# Scalability: fast on small/medium data; single trees are rarely used
#   standalone in production — usually the building block for ensembles
#   (Random Forest, Gradient Boosting) covered in later templates.
# Interpretability: very high — can be visualized and read as explicit
#   decision rules, valuable for regulated/explainable-AI contexts.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# DecisionTreeRegressor: regression analogue (Template 9), uses MSE/MAE
#   impurity instead of Gini/entropy.
# criterion="entropy"/"log_loss": alternative impurity measures to Gini.
# max_leaf_nodes / min_impurity_decrease: alternative overfitting controls
#   to max_depth/min_samples_leaf.
# ccp_alpha (cost-complexity pruning): post-hoc pruning of a fully grown
#   tree, often more principled than pre-pruning via max_depth alone.
# Ensembling (Random Forest, Extra Trees, Gradient Boosting, AdaBoost):
#   covered in Templates 10-14 — combine many trees to reduce variance.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: version the tree structure/hyperparameters;
#   trees are sensitive to training data changes, so track data snapshot
#   versions alongside model versions.
# Feature store integration: ensure split thresholds remain meaningful as
#   upstream feature definitions evolve (e.g., unit changes silently shift
#   what a learned threshold means).
# MLflow integration: log max_depth, min_samples_leaf, criterion, and the
#   full CV metric distribution (trees have higher variance across folds).
# Monitoring: watch prediction distribution and per-leaf hit rates for
#   drift — a leaf that stops receiving traffic may indicate a shifted
#   feature distribution.
# Data/concept drift: single trees are especially sensitive to distribution
#   shift since they memorize hard boundaries; monitor and retrain more
#   frequently than for regularized linear/ensemble models.
# Retraining strategy: schedule retraining aligned with observed drift;
#   consider replacing standalone trees with ensembles in production for
#   stability.
# Explainability: export decision paths per prediction (`decision_path`) for
#   case-level audit trails.
# Model registry: register with max_depth/min_samples_leaf/criterion and
#   validation metric distribution (not just mean).
# Batch vs real-time: fast enough for both; particularly well-suited to
#   low-latency real-time inference due to O(depth) prediction cost.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: non-linear boundaries, feature interactions, interpretability
#   via explicit rules is required, or as a building block for ensembles.
# Avoid when: data is small and linear separability is likely (prefer
#   Logistic Regression), or when stability across resampled training sets
#   matters (prefer ensembles).
# Advantages: no scaling needed, handles non-linearity/interactions,
#   interpretable, fast inference.
# Disadvantages: overfits easily, unstable/high-variance, poor
#   extrapolation, biased toward high-cardinality features.
# Time complexity: O(n * d * log(n)) training, O(depth) inference.
# Space complexity: O(number of nodes).
# Assumptions: none on distribution; assumes axis-aligned splits suffice.
# Important hyperparameters: max_depth, min_samples_leaf, min_samples_split,
#   criterion, class_weight, ccp_alpha.
# Interview questions to expect: how splits are chosen (Gini vs entropy);
#   how to control overfitting; why trees don't need feature scaling; how
#   trees handle categorical vs numeric splits; bias-variance of tree depth.
# Common mistakes: leaving max_depth unconstrained in production, ignoring
#   instability across CV folds, using a single tree instead of an ensemble
#   for maximum accuracy, misinterpreting feature_importances_ as causal.
# Production checklist: validate CV metric variance (not just mean) before
#   shipping, confirm max_depth/min_samples_leaf are tuned (not defaults),
#   consider whether an ensemble would be more robust for this use case.
# ============================================================
