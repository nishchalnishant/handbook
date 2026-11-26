"""
============================================================
TEMPLATE 12: AdaBoost (Adaptive Boosting)
============================================================
First boosting template — sequentially trains weak learners (shallow
trees/stumps), reweighting misclassified samples so each new learner
focuses on prior mistakes. Interview-scoped (~45 min).
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
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
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
MODEL_PATH = "adaboost_classifier_pipeline.joblib"
N_ESTIMATORS_GRID = [50, 100, 200]
LEARNING_RATE_GRID = [0.01, 0.1, 0.5, 1.0]

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
    preprocessor: ColumnTransformer, n_estimators: int = 100, learning_rate: float = 0.5
) -> Pipeline:
    # Base estimator is a decision stump (max_depth=1) — a classic "weak
    # learner" that on its own does barely better than chance. AdaBoost
    # combines many stumps, each weighted by its accuracy, and reweights
    # training samples after each round to emphasize prior misclassifications.
    base_estimator = DecisionTreeClassifier(max_depth=1, random_state=RANDOM_SEED)
    model = AdaBoostClassifier(
        estimator=base_estimator,
        n_estimators=n_estimators,
        learning_rate=learning_rate,
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
        "model__learning_rate": LEARNING_RATE_GRID,
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
        "AdaBoost": AdaBoostClassifier(n_estimators=100, learning_rate=0.5, random_state=RANDOM_SEED),
    }
    print("\nModel comparison (CV F1):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="f1")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # AdaBoost with stumps often needs more estimators than a Random Forest
    # to reach comparable accuracy, and n_estimators/learning_rate trade off
    # against each other (lower learning_rate needs more estimators).


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
    # AdaBoost is known to be sensitive to noisy labels/outliers, since it
    # keeps upweighting samples that remain hard to classify — worth
    # inspecting whether misclassified samples look like label noise.


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
    print("\nFeature importances (weighted by estimator accuracy):")
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
# When to use: classification/regression problems where a boosted ensemble
#   of weak learners (e.g., stumps) can incrementally correct residual
#   errors; historically strong on moderately sized, relatively clean
#   tabular datasets.
# Mathematical intuition: sequentially fits weak learners; after each round,
#   sample weights are increased for misclassified points and decreased for
#   correctly classified ones, so the next weak learner focuses more on
#   previously hard examples. Final prediction is a weighted vote/sum of all
#   weak learners, weighted by each learner's training accuracy.
# Advantages: simple, few hyperparameters to tune (n_estimators,
#   learning_rate, base estimator depth), often performs well with minimal
#   tuning on clean data, less prone to overfitting than a single deep tree.
# Disadvantages: sensitive to noisy data and outliers (keeps upweighting
#   hard-to-fit noisy points), sequential training means less parallelizable
#   than bagging ensembles, generally outperformed by Gradient Boosting/
#   modern boosting libraries on most tabular benchmarks.
# Bias-variance: increasing n_estimators reduces bias but can eventually
#   increase variance/overfit on noisy data; learning_rate controls how much
#   each estimator contributes, trading convergence speed against
#   overfitting risk.
# Assumptions: none on distribution; assumes an additive combination of weak
#   learners approximates the true decision boundary.
# Time complexity: O(n_estimators * cost of fitting one weak learner) —
#   inherently sequential, cannot parallelize across estimators.
# Space complexity: O(n_estimators * size of each weak learner).
# Scalability: sequential nature limits scalability versus bagging
#   ensembles; fine for small/medium datasets.
# Interpretability: feature_importances_ available; less interpretable than
#   a single tree due to the additive combination of many weak learners.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# AdaBoostRegressor: regression analogue, uses weighted median of weak
#   learner predictions.
# Different base estimators: SVMs, logistic regression stumps, or deeper
#   trees can replace the default decision stump.
# SAMME algorithm: the multi-class extension used internally by
#   AdaBoostClassifier for more than 2 classes.
# Gradient Boosting / HistGradientBoosting (Templates 13-14): generally
#   preferred over AdaBoost on modern tabular benchmarks due to more
#   flexible loss functions and better regularization.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: version n_estimators/learning_rate/base
#   estimator depth alongside the trained artifact.
# Feature store integration: same considerations as other tree ensembles.
# MLflow integration: log n_estimators, learning_rate, base estimator
#   max_depth, and CV metric distribution.
# Monitoring: watch for degraded performance on noisy/mislabeled production
#   data — AdaBoost is more sensitive to label noise than bagging ensembles.
# Data/concept drift: same drift-monitoring approach as other ensembles;
#   AdaBoost's sensitivity to outliers means drift involving new outlier
#   patterns can degrade it faster than Random Forest.
# Retraining strategy: retrain on schedule/drift trigger; audit training
#   data quality (label noise) before retraining, given AdaBoost's noise
#   sensitivity.
# Explainability: feature_importances_ plus per-estimator vote breakdown for
#   audit purposes.
# Model registry: register with hyperparameters and CV metric distribution.
# Batch vs real-time: fine for both; inference cost scales with
#   n_estimators but each weak learner (stump) is cheap.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: clean tabular data where a simple, low-tuning-effort boosted
#   ensemble is desired; more of a foundational/interview concept than a
#   default production choice today.
# Avoid when: data has significant label noise/outliers (prefer Gradient
#   Boosting/HistGradientBoosting with robust losses), or when training
#   must be parallelized across estimators (prefer bagging ensembles).
# Advantages: simple, few hyperparameters, decent performance on clean data,
#   less overfitting-prone than a single deep tree.
# Disadvantages: sensitive to noise/outliers, sequential (not parallelizable
#   across estimators), generally outperformed by modern boosting methods.
# Time complexity: O(n_estimators * base learner training cost), sequential.
# Space complexity: O(n_estimators * base learner size).
# Assumptions: none on distribution.
# Important hyperparameters: n_estimators, learning_rate, base estimator
#   (and its max_depth).
# Interview questions to expect: how AdaBoost reweights samples each round;
#   difference between AdaBoost and Gradient Boosting; why AdaBoost is
#   sensitive to outliers; learning_rate vs n_estimators tradeoff.
# Common mistakes: using deep trees as the base estimator (defeats the
#   "weak learner" premise and overfits faster), not tuning learning_rate
#   jointly with n_estimators, applying it to very noisy datasets.
# Production checklist: audit label quality before training, tune
#   n_estimators/learning_rate jointly via CV, compare against Gradient
#   Boosting as a stronger modern alternative.
# ============================================================
