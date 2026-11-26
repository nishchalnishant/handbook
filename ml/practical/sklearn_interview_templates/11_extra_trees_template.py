"""
============================================================
TEMPLATE 11: Extra Trees (Extremely Randomized Trees)
============================================================
Ensemble closely related to Random Forest, but adds randomized split
thresholds (not just randomized feature subsets) for further variance
reduction and faster training. Interview-scoped (~45 min).
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
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
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
MODEL_PATH = "extra_trees_classifier_pipeline.joblib"
N_ESTIMATORS_GRID = [100, 200, 400]
MAX_DEPTH_GRID = [5, 10, None]

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
                "num_feature_3": rng.normal(0, 1, n),
                "cat_feature_1": rng.choice(["A", "B", "C"], n),
            }
        )
        df.loc[df.sample(frac=0.05, random_state=RANDOM_SEED).index, "num_feature_2"] = np.nan
        logit = (
            0.05 * (df["num_feature_1"] - 50)
            - 0.1 * (df["num_feature_2"] - 20)
            + np.where(df["cat_feature_1"] == "A", 1.0, -0.5)
            + rng.normal(0, 0.5, n)
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
    preprocessor: ColumnTransformer, n_estimators: int = 200, max_depth: int | None = 10
) -> Pipeline:
    # Extra Trees differs from Random Forest in two ways: (1) it typically
    # uses the whole training set per tree (bootstrap=False by default)
    # rather than bootstrap resampling, and (2) split thresholds are chosen
    # randomly rather than optimally searched, trading a bit of bias for
    # lower variance and faster training.
    model = ExtraTreesClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        max_features="sqrt",
        class_weight="balanced",
        n_jobs=-1,
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
        "model__n_estimators": N_ESTIMATORS_GRID,
        "model__max_depth": MAX_DEPTH_GRID,
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
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_SEED),
        "Random Forest": RandomForestClassifier(
            n_estimators=200, max_depth=10, n_jobs=-1, random_state=RANDOM_SEED
        ),
        "Extra Trees": ExtraTreesClassifier(
            n_estimators=200, max_depth=10, n_jobs=-1, random_state=RANDOM_SEED
        ),
    }
    print("\nModel comparison (CV F1):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="f1")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # Extra Trees is often competitive with Random Forest and trains faster
    # since it skips the per-split optimal-threshold search.


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
    print("\nFeature importances (mean decrease in impurity, averaged over trees):")
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
            "num_feature_1": [55.0],
            "num_feature_2": [18.0],
            "num_feature_3": [0.2],
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
# When to use: same general use cases as Random Forest — strong tabular
#   baseline — when you additionally want faster training or slightly lower
#   variance at a small bias cost.
# Mathematical intuition: like Random Forest, an ensemble of trees trained
#   on random feature subsets; but split thresholds within each candidate
#   feature are drawn randomly rather than exhaustively optimized, and
#   (by default) trees are trained on the full dataset rather than
#   bootstrap resamples. The added randomness further decorrelates trees.
# Advantages: often faster to train than Random Forest (no per-split
#   threshold search), can further reduce variance/overfitting, similarly
#   minimal preprocessing required.
# Disadvantages: extra randomness can slightly increase bias per tree,
#   still less interpretable than a single tree, impurity-based importances
#   share the same high-cardinality bias as Random Forest.
# Bias-variance: shifts further toward the low-variance end of the
#   bias-variance tradeoff compared to Random Forest, due to random
#   threshold selection.
# Assumptions: none on distribution.
# Time complexity: O(n_estimators * n * d) training — cheaper per split
#   than Random Forest since no threshold search is performed.
# Space complexity: O(n_estimators * nodes per tree).
# Scalability: parallelizable, often faster wall-clock training than RF at
#   equal n_estimators.
# Interpretability: same as Random Forest — feature importances available,
#   individual predictions less transparent than a single tree.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# ExtraTreesRegressor: regression analogue.
# bootstrap=True: enables bootstrap resampling per tree (closer to Random
#   Forest behavior) if the default full-dataset-per-tree behavior
#   underperforms on a given dataset.
# Compare against Random Forest and Gradient Boosting (Template 13) as part
#   of standard model-selection practice for tabular problems.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: same considerations as Random Forest — version
#   n_estimators/max_depth/max_features with the trained artifact.
# Feature store integration: same as Random Forest.
# MLflow integration: log n_estimators, max_depth, max_features, and CV
#   metric distribution; note in the run whether bootstrap was enabled.
# Monitoring: same latency/accuracy tracking as Random Forest.
# Data/concept drift: same monitoring approach as Random Forest.
# Retraining strategy: same as Random Forest; Extra Trees' faster training
#   time makes more frequent full retrains more feasible if drift is common.
# Explainability: same feature_importances_/permutation importance approach
#   as Random Forest.
# Model registry: same as Random Forest.
# Batch vs real-time: same considerations as Random Forest; faster training
#   time is an advantage for frequent batch retraining pipelines.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: same as Random Forest, especially when training speed matters
#   or when Random Forest is overfitting despite tuning.
# Avoid when: same caveats as Random Forest (interpretability, strict
#   latency/memory constraints).
# Advantages: faster training than Random Forest, can further reduce
#   variance, minimal preprocessing.
# Disadvantages: slightly higher bias per tree than Random Forest, same
#   interpretability/importance-bias caveats.
# Time complexity: O(n_estimators * n * d) training (no threshold search).
# Space complexity: O(n_estimators * nodes per tree).
# Assumptions: none on distribution.
# Important hyperparameters: n_estimators, max_depth, max_features,
#   bootstrap, min_samples_leaf, class_weight.
# Interview questions to expect: how Extra Trees differs from Random Forest
#   (random thresholds + full dataset per tree vs bootstrap + optimal
#   thresholds); why this trades bias for variance/speed; when it might
#   underperform Random Forest.
# Common mistakes: assuming Extra Trees always outperforms Random Forest —
#   always compare both via CV rather than picking one by default.
# Production checklist: same as Random Forest — confirm hyperparameters
#   tuned via CV, benchmark training/inference time against Random Forest
#   to justify the choice.
# ============================================================
