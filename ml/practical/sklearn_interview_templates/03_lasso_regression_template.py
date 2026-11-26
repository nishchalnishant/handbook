"""
============================================================
TEMPLATE 3: Lasso Regression (L1-Regularized Linear Regression)
============================================================
Predicting a continuous target using L1-regularized linear regression.
Delta vs Ridge: L1 penalty drives some coefficients to exactly zero,
performing automatic feature selection. Interview-scoped (~45 min).
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
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ------------------------------------------------------------
# 2. Configuration (plain variables, no config class)
# ------------------------------------------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
DATA_PATH = "data.csv"
TARGET_COLUMN = "target"
MODEL_PATH = "lasso_regression_pipeline.joblib"
ALPHA_GRID = [0.001, 0.01, 0.1, 1.0, 10.0]

np.random.seed(RANDOM_SEED)


# ------------------------------------------------------------
# 3. Load Dataset
# ------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        rng = np.random.default_rng(RANDOM_SEED)
        n = 500
        # Include irrelevant/noise features so Lasso's feature selection is demonstrable.
        df = pd.DataFrame(
            {
                "num_feature_1": rng.normal(50, 10, n),   # informative
                "num_feature_2": rng.normal(20, 5, n),    # informative
                "noise_feature_1": rng.normal(0, 1, n),   # irrelevant
                "noise_feature_2": rng.normal(0, 1, n),   # irrelevant
                "cat_feature_1": rng.choice(["A", "B", "C"], n),
            }
        )
        df.loc[df.sample(frac=0.05, random_state=RANDOM_SEED).index, "num_feature_2"] = np.nan
        df[TARGET_COLUMN] = (
            3.0 * df["num_feature_1"] + 2.0 * df["num_feature_2"].fillna(20) + rng.normal(0, 5, n)
        )
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


# ------------------------------------------------------------
# 5. Train/Test Split
# ------------------------------------------------------------
def split_data(df: pd.DataFrame):
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
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

    # Scaling is essential for Lasso too — the L1 penalty is scale-dependent.
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
def build_pipeline(preprocessor: ColumnTransformer, alpha: float = 1.0) -> Pipeline:
    # Lasso: OLS + L1 penalty (alpha * sum(|w|)). Drives some coefficients to
    # exactly zero -> built-in feature selection, sparse models.
    model = Lasso(alpha=alpha, random_state=RANDOM_SEED, max_iter=10000)
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
    pipeline = build_pipeline(preprocessor)
    # alpha controls sparsity: higher alpha -> more coefficients zeroed out.
    param_grid = {"model__alpha": ALPHA_GRID}

    grid_search = GridSearchCV(pipeline, param_grid, cv=CV_FOLDS, scoring="r2", n_jobs=-1)
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
        "Ridge": Ridge(alpha=1.0, random_state=RANDOM_SEED),
        "Lasso": Lasso(alpha=0.1, random_state=RANDOM_SEED, max_iter=10000),
    }
    print("\nModel comparison (CV R2):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="r2")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # Lasso tends to shine when many features are irrelevant/noisy — it
    # zeroes them out, simplifying the model and often improving generalization.


# ------------------------------------------------------------
# 13. Error Analysis
# ------------------------------------------------------------
def error_analysis(pipeline: Pipeline, X_test, y_test) -> None:
    y_pred = pipeline.predict(X_test)
    residuals = y_test - y_pred
    print("\nResidual stats:")
    print(f"  mean={residuals.mean():.4f}, std={residuals.std():.4f}")
    worst_idx = residuals.abs().sort_values(ascending=False).head(5).index
    print("\nTop 5 worst predictions:")
    print(pd.DataFrame({"y_true": y_test.loc[worst_idx], "y_pred": y_pred[y_test.index.get_indexer(worst_idx)]}))


# ------------------------------------------------------------
# 14. Feature Importance
# ------------------------------------------------------------
def feature_importance(pipeline: Pipeline) -> None:
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()
    importance_df = pd.DataFrame(
        {"feature": feature_names, "coefficient": model.coef_}
    ).sort_values("coefficient", key=np.abs, ascending=False)
    print("\nFeature coefficients (some exactly 0.0 -> auto feature selection):")
    print(importance_df)
    n_selected = np.sum(model.coef_ != 0)
    print(f"\nFeatures kept (non-zero coefficient): {n_selected}/{len(model.coef_)}")


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
            "noise_feature_1": [0.0],
            "noise_feature_2": [0.0],
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
# When to use: high-dimensional data with many irrelevant/redundant
#   features where automatic feature selection is desirable, or when a
#   sparse, interpretable model is preferred.
# Mathematical intuition: minimizes ||y - Xw||^2 + alpha * sum(|w|). The L1
#   penalty's non-differentiable corners at zero push weak coefficients
#   exactly to zero (unlike Ridge's smooth L2 penalty).
# Advantages: automatic feature selection, produces sparse/interpretable
#   models, effective in high-dimensional settings (d >> n).
# Disadvantages: unstable feature selection when features are highly
#   correlated (arbitrarily picks one of a correlated group), no closed-form
#   solution (solved via coordinate descent), requires scaling and alpha tuning.
# Bias-variance: higher alpha increases bias and sparsity, decreases variance.
# Assumptions: same linear regression assumptions, plus the belief that only
#   a subset of features are truly relevant (sparsity assumption).
# Time complexity: O(n*d) per coordinate descent iteration x iterations
#   (no closed-form; iterative solver).
# Space complexity: O(n*d).
# Scalability: works well for high-dimensional sparse data; consider
#   SGDRegressor with L1 penalty for very large n.
# Interpretability: high — the resulting sparse coefficient vector directly
#   identifies which features matter.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# ElasticNet: combine L1 + L2 to handle correlated features better than
#   pure Lasso while retaining sparsity.
# LassoCV: efficient built-in cross-validated alpha path search.
# LassoLars: uses Least Angle Regression, efficient for very sparse solutions.
# Classification: use L1-penalized LogisticRegression (penalty="l1") for
#   sparse classification.
# Online/large-scale: SGDRegressor(penalty="l1") for out-of-core learning.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: track which features were selected (non-zero
#   coefficients) per model version — feature set can change between retrains.
# Feature store integration: only serve the subset of features Lasso
#   selected, reducing feature-store query cost.
# MLflow integration: log alpha, number of selected features, and CV R2 as
#   run metrics.
# Monitoring: track how many features remain selected over time — a shrinking
#   or growing active set can be a leading indicator of drift.
# Data/concept drift: monitor whether previously-zeroed features become
#   predictive again (a data relationship change).
# Retraining strategy: retrain when the selected feature set becomes
#   unstable across folds/time windows.
# Explainability: sparse coefficients are inherently explainable; pair with
#   SHAP if comparing against non-linear challenger models.
# Model registry: register with the selected feature list as metadata.
# Batch vs real-time: cheap, sparse linear model — ideal for low-latency
#   real-time inference since fewer features need to be fetched.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: many irrelevant features exist and automatic feature selection/
#   sparsity is desired, or interpretability via a reduced feature set matters.
# Avoid when: features are highly correlated and you need stable
#   coefficient estimates (prefer Ridge or ElasticNet).
# Advantages: automatic feature selection, sparse and interpretable,
#   effective in high dimensions.
# Disadvantages: unstable selection under correlated features, iterative
#   solver (no closed form), needs alpha tuning and scaling.
# Time complexity: O(n*d) per iteration of coordinate descent.
# Space complexity: O(n*d).
# Assumptions: linearity, sparsity (only some features truly matter).
# Important hyperparameters: alpha (regularization/sparsity strength),
#   max_iter (convergence for coordinate descent), tol.
# Interview questions to expect: why does L1 zero out coefficients but L2
#   doesn't (geometric intuition: L1 ball has corners at axes); Lasso vs
#   Ridge vs ElasticNet tradeoffs; behavior under correlated features.
# Common mistakes: not scaling features; not increasing max_iter leading to
#   convergence warnings; assuming Lasso's selected features are the only
#   "true" predictors (can be unstable/arbitrary among correlated groups).
# Production checklist: log the selected feature set, ensure convergence
#   (no ConvergenceWarning) before promoting to production, versioned
#   artifacts with alpha and feature-count metadata.
# ============================================================
