"""
============================================================
TEMPLATE 4: ElasticNet Regression (L1 + L2 Regularized)
============================================================
Predicting a continuous target using a combined L1+L2 penalty.
Delta vs Lasso/Ridge: balances sparsity (L1) with stability under
correlated features (L2) via the l1_ratio mixing parameter.
Interview-scoped (~45 min).
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
from sklearn.linear_model import ElasticNet, LinearRegression, Ridge, Lasso
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
MODEL_PATH = "elasticnet_pipeline.joblib"
ALPHA_GRID = [0.001, 0.01, 0.1, 1.0, 10.0]
L1_RATIO_GRID = [0.1, 0.3, 0.5, 0.7, 0.9]

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
        # Correlated informative features (group) + irrelevant noise features,
        # so ElasticNet's dual behavior (grouping + sparsity) is demonstrable.
        base = rng.normal(50, 10, n)
        df = pd.DataFrame(
            {
                "num_feature_1": base,
                "num_feature_2": base * 0.85 + rng.normal(0, 2, n),  # correlated with feature_1
                "noise_feature_1": rng.normal(0, 1, n),
                "noise_feature_2": rng.normal(0, 1, n),
                "cat_feature_1": rng.choice(["A", "B", "C"], n),
            }
        )
        df.loc[df.sample(frac=0.05, random_state=RANDOM_SEED).index, "num_feature_2"] = np.nan
        df[TARGET_COLUMN] = 2.5 * base + rng.normal(0, 5, n)
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
def build_pipeline(preprocessor: ColumnTransformer, alpha: float = 1.0, l1_ratio: float = 0.5) -> Pipeline:
    # ElasticNet: alpha*(l1_ratio*||w||_1 + 0.5*(1-l1_ratio)*||w||^2).
    # l1_ratio=1.0 -> pure Lasso; l1_ratio=0.0 -> pure Ridge.
    # Handles groups of correlated features better than pure Lasso (tends to
    # select/shrink correlated features together rather than arbitrarily).
    model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=RANDOM_SEED, max_iter=10000)
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
    # Jointly tune alpha (overall regularization strength) and l1_ratio
    # (L1 vs L2 mix) via grid search.
    param_grid = {
        "model__alpha": ALPHA_GRID,
        "model__l1_ratio": L1_RATIO_GRID,
    }

    grid_search = GridSearchCV(pipeline, param_grid, cv=CV_FOLDS, scoring="r2", n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print(f"\nBest params: {grid_search.best_params_}")
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
        "ElasticNet": ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=RANDOM_SEED, max_iter=10000),
    }
    print("\nModel comparison (CV R2):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="r2")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # ElasticNet is often a solid default when unsure whether Ridge or Lasso
    # behavior is more appropriate — it interpolates between the two.


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
    print("\nFeature coefficients:")
    print(importance_df)
    print(f"\nEffective l1_ratio used: {model.l1_ratio}")


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
            "num_feature_2": [47.0],
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
# When to use: many correlated features together with a need for some
#   sparsity — a middle ground when unsure whether Ridge or Lasso is more
#   appropriate.
# Mathematical intuition: minimizes ||y - Xw||^2 + alpha*l1_ratio*||w||_1 +
#   0.5*alpha*(1-l1_ratio)*||w||^2. Combines Lasso's sparsity with Ridge's
#   grouping effect on correlated features.
# Advantages: handles correlated feature groups better than pure Lasso
#   (tends to keep or drop them together), still yields sparse solutions,
#   more stable than Lasso in high-dimensional/correlated settings.
# Disadvantages: two hyperparameters to tune (alpha, l1_ratio) instead of
#   one, no closed-form solution, less interpretable "pure" story than
#   Ridge or Lasso alone.
# Bias-variance: alpha controls overall regularization strength (bias vs
#   variance); l1_ratio controls the sparsity/stability tradeoff.
# Assumptions: same linear regression assumptions; benefits from grouped/
#   correlated informative features existing in the data.
# Time complexity: O(n*d) per coordinate descent iteration x iterations.
# Space complexity: O(n*d).
# Scalability: same as Lasso/Ridge — efficient via coordinate descent.
# Interpretability: moderate — sparse but coefficients among correlated
#   groups are shared/shrunk together rather than arbitrarily picked.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# ElasticNetCV: efficient built-in cross-validated (alpha, l1_ratio) search.
# Pure Lasso (l1_ratio=1.0) / pure Ridge (l1_ratio=0.0) as special cases.
# Multi-task ElasticNet: for multiple correlated regression targets sharing
#   the same sparsity pattern (MultiTaskElasticNet).
# Logistic Regression with penalty="elasticnet" (requires solver="saga") for
#   the classification analogue.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: track (alpha, l1_ratio) and selected/shrunk
#   feature groups per version.
# Feature store integration: since correlated feature groups are handled
#   together, coordinate feature-store schema changes across the whole group.
# MLflow integration: log alpha, l1_ratio, and CV R2 per run for comparison.
# Monitoring: watch for correlation structure shifts between features —
#   ElasticNet's benefit over Lasso depends on that structure persisting.
# Data/concept drift: monitor coefficient stability over retrains as a
#   proxy for underlying relationship drift.
# Retraining strategy: retrain on a schedule or when CV performance degrades;
#   re-run the (alpha, l1_ratio) grid search periodically since optimal mix
#   can shift as feature correlations change.
# Explainability: sparse-ish coefficients remain reasonably interpretable;
#   pair with SHAP for stakeholder-facing explanations.
# Model registry: register with full hyperparameter metadata (alpha, l1_ratio).
# Batch vs real-time: lightweight linear model, suitable for both batch and
#   low-latency real-time serving.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: features are correlated and some sparsity is still desired, or
#   when unsure whether Ridge or Lasso alone is the better fit.
# Avoid when: you have strong prior knowledge favoring pure L1 (max sparsity)
#   or pure L2 (max stability) — then use Lasso/Ridge directly for simplicity.
# Advantages: balances sparsity and stability, handles correlated feature
#   groups gracefully, flexible via l1_ratio.
# Disadvantages: two hyperparameters to tune, no closed-form solution,
#   slightly more complex to explain than Ridge/Lasso alone.
# Time complexity: O(n*d) per iteration of coordinate descent.
# Space complexity: O(n*d).
# Assumptions: linearity; benefits from correlated informative feature groups.
# Important hyperparameters: alpha (overall regularization strength),
#   l1_ratio (L1 vs L2 mix), max_iter/tol (convergence).
# Interview questions to expect: how does ElasticNet differ from Lasso/
#   Ridge; what does l1_ratio control; why is ElasticNet often preferred
#   over Lasso for correlated features (grouping effect).
# Common mistakes: not tuning l1_ratio jointly with alpha; not scaling
#   features; misinterpreting shared coefficients among correlated features
#   as individually unimportant.
# Production checklist: log both hyperparameters, verify convergence,
#   validate coefficient stability across retrains before promoting to
#   production.
# ============================================================
