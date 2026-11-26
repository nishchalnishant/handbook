"""
============================================================
TEMPLATE 13: Gradient Boosting Classifier
============================================================
Sequentially fits trees to the negative gradient (pseudo-residuals) of a
differentiable loss function. Interview-scoped (~45 min).
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
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, AdaBoostClassifier
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
MODEL_PATH = "gradient_boosting_classifier_pipeline.joblib"
N_ESTIMATORS_GRID = [100, 200, 300]
LEARNING_RATE_GRID = [0.01, 0.05, 0.1]
MAX_DEPTH_GRID = [2, 3, 4]

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
        # Non-linear interaction target with some noise — gradient boosting
        # should comfortably beat linear models and match/edge out bagging.
        logit = (
            0.04 * (df["num_feature_1"] - 50) * np.where(df["cat_feature_1"] == "A", 1, -1)
            - 0.08 * (df["num_feature_2"] - 20)
            + 0.5 * df["num_feature_3"]
            + rng.normal(0, 0.6, n)
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
    preprocessor: ColumnTransformer,
    n_estimators: int = 200,
    learning_rate: float = 0.05,
    max_depth: int = 3,
) -> Pipeline:
    # Each tree is fit on the negative gradient (pseudo-residuals) of the
    # loss w.r.t. current predictions, then added with a shrinkage factor
    # (learning_rate). max_depth is kept shallow (2-4) since boosting adds
    # many weak/moderate learners rather than a few deep ones.
    model = GradientBoostingClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        subsample=0.8,  # stochastic gradient boosting: adds regularization
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
        "model__max_depth": MAX_DEPTH_GRID,
    }

    # learning_rate and n_estimators trade off: lower learning_rate needs
    # more estimators for the same fit quality but generalizes better.
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
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=200, learning_rate=0.05, max_depth=3, random_state=RANDOM_SEED
        ),
    }
    print("\nModel comparison (CV F1):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="f1")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # Gradient Boosting typically edges out bagging ensembles on structured
    # interaction-heavy targets, at the cost of being more sensitive to
    # hyperparameters (learning_rate, n_estimators, max_depth) and slower
    # to train sequentially.


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
    print("\nFeature importances (impurity-based, averaged over boosting rounds):")
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
            "num_feature_3": [0.3],
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
# When to use: tabular data with non-linear feature interactions where
#   maximum predictive performance is desired and training time budget
#   allows sequential (not embarrassingly parallel) fitting.
# Mathematical intuition: an additive model built stage-wise; at each stage,
#   a regression tree is fit to the negative gradient of the loss function
#   w.r.t. the current ensemble's predictions (functional gradient descent
#   in prediction space). Predictions are updated as
#   F_m(x) = F_{m-1}(x) + learning_rate * h_m(x), where h_m approximates the
#   pseudo-residuals.
# Advantages: typically strong predictive performance on structured/tabular
#   data, flexible loss functions (deviance, exponential), subsample
#   parameter enables stochastic gradient boosting for regularization.
# Disadvantages: sequential training (not parallelizable across trees), more
#   hyperparameters to tune than bagging methods, prone to overfitting with
#   too many estimators/high learning_rate/deep trees, slower training than
#   HistGradientBoosting on large datasets.
# Bias-variance: n_estimators and learning_rate jointly control the
#   bias-variance tradeoff — more estimators/higher learning_rate reduces
#   bias but risks overfitting; subsample and max_depth add regularization.
# Assumptions: none on the data distribution.
# Time complexity: roughly O(n_estimators * n_samples * n_features * depth)
#   — sequential, so wall-clock time grows linearly with n_estimators.
# Space complexity: O(n_estimators * tree size).
# Scalability: slower than HistGradientBoosting (Template 14) on large
#   datasets since it doesn't use histogram-based binning.
# Interpretability: feature_importances_ available; partial dependence
#   plots commonly used for deeper interpretability.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# GradientBoostingRegressor: regression analogue with squared_error/
#   absolute_error/huber/quantile losses.
# HistGradientBoostingClassifier/Regressor (Template 14): histogram-based,
#   much faster on large datasets, native missing-value support.
# XGBoost/LightGBM/CatBoost: external libraries implementing gradient
#   boosting with additional regularization, GPU support, and categorical
#   feature handling — commonly preferred in production over sklearn's
#   GradientBoostingClassifier for large-scale tabular problems.
# Stochastic Gradient Boosting: subsample < 1.0 (used above) trains each
#   tree on a random subset of rows, reducing variance and training time.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: version n_estimators/learning_rate/max_depth/
#   subsample alongside the trained artifact; these interact strongly so
#   version them together, not independently.
# Feature store integration: consistent feature computation between
#   training and serving is critical given the model's sensitivity to
#   feature interactions.
# MLflow integration: log full hyperparameter set, CV metric distribution,
#   training wall-clock time (useful for comparing against
#   HistGradientBoosting/XGBoost alternatives).
# Monitoring: monitor prediction latency (boosted ensembles with many
#   estimators can be slow at inference) and accuracy/F1 drift over time.
# Data/concept drift: monitor input feature distributions and prediction
#   distribution; retrain when interaction structure between features and
#   target shifts.
# Retraining strategy: consider incremental retraining cost — full
#   retraining is required (no true partial_fit for GBM), so schedule
#   retraining windows accordingly.
# Explainability: SHAP values or partial dependence plots recommended over
#   raw feature_importances_ for stakeholder-facing explanations.
# Model registry: register with full hyperparameter set and training data
#   snapshot reference.
# Batch vs real-time: batch scoring preferred for very large ensembles;
#   for real-time, consider HistGradientBoosting or a distilled model for
#   lower latency.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: tabular data with complex feature interactions, and you can
#   afford sequential training / thorough hyperparameter tuning to
#   maximize performance.
# Avoid when: dataset is very large (prefer HistGradientBoosting/LightGBM
#   for speed), or fast iterative retraining/streaming updates are needed.
# Advantages: strong predictive performance, flexible loss functions,
#   built-in regularization via subsample/learning_rate/max_depth.
# Disadvantages: sequential training, many interacting hyperparameters,
#   overfitting risk, slower than histogram-based boosting on large data.
# Time complexity: O(n_estimators * n_samples * n_features * depth),
#   sequential.
# Space complexity: O(n_estimators * tree size).
# Assumptions: none on distribution.
# Important hyperparameters: n_estimators, learning_rate, max_depth,
#   subsample, min_samples_leaf.
# Interview questions to expect: how gradient boosting differs from
#   AdaBoost (gradient descent in function space vs sample reweighting);
#   role of learning_rate as shrinkage; why shallow trees are used as base
#   learners; how subsample relates to stochastic gradient boosting.
# Common mistakes: setting n_estimators too high without early stopping/
#   tuning learning_rate down, using deep trees as base learners (overfits
#   fast), ignoring subsample as a regularization lever.
# Production checklist: tune n_estimators/learning_rate jointly (consider
#   n_iter_no_change for early stopping), validate on held-out test set
#   once, log full hyperparameter set with the model artifact, benchmark
#   against HistGradientBoostingClassifier for latency/throughput.
# ============================================================
