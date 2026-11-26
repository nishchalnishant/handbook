"""
============================================================
TEMPLATE 1: Linear Regression
============================================================
Predicting a continuous target from numerical + categorical features
using Ordinary Least Squares Linear Regression, wrapped in a full
production-style Scikit-learn Pipeline. Interview-scoped (~45 min).
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

from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    GridSearchCV,
    learning_curve,
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.dummy import DummyRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ------------------------------------------------------------
# 2. Configuration (plain variables, no config class)
# ------------------------------------------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
DATA_PATH = "data.csv"          # replace with real dataset path
TARGET_COLUMN = "target"
MODEL_PATH = "linear_regression_pipeline.joblib"

np.random.seed(RANDOM_SEED)


# ------------------------------------------------------------
# 3. Load Dataset
# ------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    """Load raw data from CSV. Swap this out for real data source (SQL, S3, etc.)."""

    df = pd.read_csv(path)
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
    print("\nTarget distribution:\n", df[TARGET_COLUMN].describe())
    numeric_df = df.select_dtypes(include=np.number)
    print("\nCorrelation matrix:\n", numeric_df.corr())
    # Simple outlier check via IQR on the target.
    q1, q3 = df[TARGET_COLUMN].quantile([0.25, 0.75])
    iqr = q3 - q1
    outliers = df[(df[TARGET_COLUMN] < q1 - 1.5 * iqr) | (df[TARGET_COLUMN] > q3 + 1.5 * iqr)]
    print(f"\nOutliers in target (IQR method): {len(outliers)}")


# ------------------------------------------------------------
# 5. Train/Test Split
# ------------------------------------------------------------
def split_data(df: pd.DataFrame):
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    # Regression target -> no stratification. Split BEFORE any preprocessing
    # to avoid data leakage (fit imputers/scalers only on train data).
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )
    return X_train, X_test, y_train, y_test


# ------------------------------------------------------------
# 6 & 7. Feature Engineering + Preprocessing Pipeline
# ------------------------------------------------------------
def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_features = X.select_dtypes(include=np.number).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()

    # Impute + scale numerical columns. Scaling matters for Linear Regression
    # when using regularized variants (Ridge/Lasso) or comparing coefficients.
    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    # Impute + one-hot encode categorical columns. handle_unknown="ignore"
    # prevents crashes when unseen categories appear at inference time.
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
def build_pipeline(preprocessor: ColumnTransformer) -> Pipeline:
    # LinearRegression: closed-form OLS solution (via SVD), no hyperparameters
    # to tune besides fit_intercept. Fast, interpretable, sensitive to
    # multicollinearity and outliers.
    model = LinearRegression()
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ])
    return pipeline


def train(pipeline: Pipeline, X_train, y_train) -> Pipeline:
    # Fit the ENTIRE pipeline on training data only — preprocessing and
    # model training happen together, preventing leakage from test data.
    pipeline.fit(X_train, y_train)
    return pipeline


# ------------------------------------------------------------
# 10. Evaluation
# ------------------------------------------------------------
def evaluate(pipeline: Pipeline, X_train, y_train, X_test, y_test) -> dict:
    y_pred = pipeline.predict(X_test)
    metrics = {
        "MAE": mean_absolute_error(y_test, y_pred),
        "MSE": mean_squared_error(y_test, y_pred),
        "RMSE": mean_squared_error(y_test, y_pred) ** 0.5,
        "R2": r2_score(y_test, y_pred),
    }
    print("\nTest metrics:")
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")


    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=CV_FOLDS, scoring="r2")
    print(f"\nCV R2 mean +/- std: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
    return metrics




# ------------------------------------------------------------
# 11. Hyperparameter Tuning
# ------------------------------------------------------------
def tune_hyperparameters(X_train, y_train, preprocessor: ColumnTransformer) -> Pipeline:
    # Plain LinearRegression has almost no hyperparameters worth tuning, so
    # we tune its regularized cousin (Ridge) here to demonstrate the workflow
    # — same pipeline shape, swap in "model__alpha".
    ridge_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", Ridge(random_state=RANDOM_SEED)),
    ])
    param_grid = {"model__alpha": [0.01, 0.1, 1.0, 10.0, 100.0]}

    grid_search = GridSearchCV(
        ridge_pipeline, param_grid, cv=CV_FOLDS, scoring="r2", n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    print(f"\nBest alpha: {grid_search.best_params_}")
    print(f"Best CV R2: {grid_search.best_score_:.4f}")
    return grid_search.best_estimator_


# ------------------------------------------------------------
# 12. Model Comparison
# ------------------------------------------------------------
def compare_models(X_train, y_train, preprocessor: ColumnTransformer) -> None:
    candidates = {
        "Dummy (mean)": DummyRegressor(strategy="mean"),
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(random_state=RANDOM_SEED),
        "Decision Tree": DecisionTreeRegressor(random_state=RANDOM_SEED),
    }
    print("\nModel comparison (CV R2):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="r2")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # Linear Regression tends to win when the true relationship is roughly
    # linear and features aren't wildly collinear; tree models win when
    # relationships are non-linear/interaction-heavy.


# ------------------------------------------------------------
# 13. Error Analysis
# ------------------------------------------------------------
def error_analysis(pipeline: Pipeline, X_test, y_test) -> None:
    y_pred = pipeline.predict(X_test)
    residuals = y_test - y_pred

    print("\nResidual stats:")
    print(f"  mean={residuals.mean():.4f}, std={residuals.std():.4f}")
    print(f"  min={residuals.min():.4f}, max={residuals.max():.4f}")

    worst_idx = residuals.abs().sort_values(ascending=False).head(5).index
    print("\nTop 5 worst predictions:")
    print(pd.DataFrame({"y_true": y_test.loc[worst_idx], "y_pred": y_pred[y_test.index.get_indexer(worst_idx)]}))


# ------------------------------------------------------------
# 14. Feature Importance
# ------------------------------------------------------------
def feature_importance(pipeline: Pipeline) -> None:
    # Linear Regression coefficients are directly interpretable once
    # features are standardized: larger |coefficient| = larger effect
    # on the target holding other features fixed.
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    feature_names = preprocessor.get_feature_names_out()
    coefficients = model.coef_

    importance_df = pd.DataFrame(
        {"feature": feature_names, "coefficient": coefficients}
    ).sort_values("coefficient", key=np.abs, ascending=False)
    print("\nFeature coefficients (sorted by magnitude):")
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
            "num_feature_2": [22.0],
            "cat_feature_1": ["A"],
        }
    )
    prediction = pipeline.predict(new_sample)
    print(f"\nPrediction on new sample: {prediction[0]:.4f}")


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
# When to use: baseline/benchmark for regression tasks, or when the
#   relationship between features and target is approximately linear and
#   interpretability matters (e.g., understanding feature effects).
# Mathematical intuition: fits y = Xw + b by minimizing sum of squared
#   residuals (OLS). Closed-form solution via the normal equation or SVD:
#   w = (X^T X)^-1 X^T y.
# Advantages: fast to train, highly interpretable coefficients, no
#   hyperparameters to tune, well-understood statistical properties.
# Disadvantages: assumes linear relationship, sensitive to outliers,
#   sensitive to multicollinearity (unstable coefficients), cannot capture
#   non-linear interactions without manual feature engineering.
# Bias-variance: high bias (strong linearity assumption), low variance
#   (stable across resamples) — underfits non-linear data.
# Assumptions: linearity, independence of errors, homoscedasticity
#   (constant error variance), no/low multicollinearity, normally
#   distributed residuals (for inference, not prediction).
# Time complexity: O(n * d^2 + d^3) for the normal equation (n samples,
#   d features); scikit-learn uses SVD-based least squares, ~O(n*d^2).
# Space complexity: O(n*d) for the data, O(d^2) for intermediate matrices.
# Scalability: struggles with very high-dimensional or very large n without
#   using SGDRegressor (mini-batch) as an alternative solver.
# Interpretability: very high — coefficients directly show per-feature effect.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# Regularized variants: Ridge (L2) to handle multicollinearity, Lasso (L1)
#   for feature selection, ElasticNet for a mix of both.
# Polynomial regression: add PolynomialFeatures before LinearRegression to
#   capture non-linear relationships while keeping a linear model form.
# Large datasets: use SGDRegressor with partial_fit for out-of-core/online
#   learning instead of the closed-form solver.
# Robust regression: use HuberRegressor or RANSACRegressor when outliers
#   are expected to heavily skew OLS coefficients.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: tag saved joblib artifacts with a version
#   (e.g., git SHA or semantic version) and store alongside training metadata.
# Feature store integration: fetch numeric/categorical features from a
#   centralized feature store to guarantee training/serving consistency.
# MLflow integration: log params, metrics, and the pipeline artifact via
#   mlflow.sklearn.log_model for reproducibility and experiment tracking.
# Monitoring: track prediction distribution, input feature distributions,
#   and live R2/MAE against a rolling validation set.
# Data/concept drift: use statistical tests (KS test, PSI) on incoming
#   feature distributions; monitor residual drift over time.
# Retraining strategy: scheduled retraining (e.g., weekly) or triggered by
#   drift/performance degradation thresholds.
# Explainability: coefficients already offer built-in explainability;
#   supplement with SHAP for standardized, comparable attributions.
# Model registry: register promoted models in a registry (MLflow Model
#   Registry, SageMaker Model Registry) with stage transitions (staging/prod).
# Batch vs real-time: linear models are cheap enough for real-time serving;
#   batch scoring is trivial via pipeline.predict on a dataframe.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: relationship is roughly linear, interpretability is valued,
#   need a fast baseline before trying more complex models.
# Avoid when: relationship is strongly non-linear, heavy multicollinearity
#   exists without regularization, or outliers dominate the data.
# Advantages: fast, interpretable, no tuning required, well-understood.
# Disadvantages: linearity assumption, outlier-sensitive, multicollinearity
#   instability.
# Time complexity: ~O(n*d^2) train; O(d) predict per sample.
# Space complexity: O(n*d) training data, O(d) model parameters.
# Assumptions: linearity, independent errors, homoscedasticity, low
#   multicollinearity.
# Important hyperparameters: fit_intercept (rarely tuned); none in practice
#   for plain OLS — regularization strength (alpha) matters for Ridge/Lasso.
# Interview questions to expect: derive the normal equation; explain
#   multicollinearity's effect on coefficient variance; L1 vs L2
#   regularization; when OLS assumptions are violated, what breaks.
# Common mistakes: not scaling features before regularized variants; fitting
#   on the full dataset before splitting (leakage); ignoring multicollinearity
#   diagnostics (VIF); using R2 alone without residual analysis.
# Production checklist: pipeline fit only on train data, joblib-persisted
#   full pipeline (not just the model), versioned artifacts, monitored
#   input/output distributions, documented assumptions for stakeholders.
# ============================================================
