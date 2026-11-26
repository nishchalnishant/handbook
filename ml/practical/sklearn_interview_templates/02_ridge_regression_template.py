"""
============================================================
TEMPLATE 2: Ridge Regression (L2-Regularized Linear Regression)
============================================================
Predicting a continuous target using L2-regularized linear regression.
Same workflow as Template 1; delta is regularization strength (alpha)
tuning and its bias-variance effect. Interview-scoped (~45 min).
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
from sklearn.linear_model import Ridge, LinearRegression
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
MODEL_PATH = "ridge_regression_pipeline.joblib"
ALPHA_GRID = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]

np.random.seed(RANDOM_SEED)


# ------------------------------------------------------------
# 3. Load Dataset
# ------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
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

    # Scaling is CRITICAL for Ridge: the penalty term (alpha * sum(w^2)) is
    # scale-dependent, so unscaled features get unfairly penalized/favored.
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
    # Ridge: OLS + L2 penalty (alpha * ||w||^2). Shrinks coefficients toward
    # zero (never exactly zero) — stabilizes estimates under multicollinearity.
    model = Ridge(alpha=alpha, random_state=RANDOM_SEED)
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
    # alpha controls regularization strength: higher alpha -> more shrinkage
    # -> higher bias, lower variance. GridSearchCV picks the sweet spot via CV.
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
        "Ridge (alpha=1.0)": Ridge(alpha=1.0, random_state=RANDOM_SEED),
        "Ridge (alpha=10.0)": Ridge(alpha=10.0, random_state=RANDOM_SEED),
    }
    print("\nModel comparison (CV R2):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="r2")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # Ridge tends to beat plain Linear Regression when features are
    # correlated/multicollinear, since it stabilizes coefficient estimates.


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
    print("\nFeature coefficients (shrunk toward zero relative to plain OLS):")
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
            "num_feature_2": [50.0],
            "num_feature_3": [22.0],
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
# When to use: linear regression with multicollinear features, or when
#   plain OLS overfits/has unstable coefficients due to correlated inputs.
# Mathematical intuition: minimizes ||y - Xw||^2 + alpha * ||w||^2. The L2
#   penalty shrinks coefficients toward zero, trading a bit of bias for a
#   large reduction in variance when features are correlated.
# Advantages: handles multicollinearity well, more stable than OLS, still
#   has a closed-form solution, all features retained (no sparsity).
# Disadvantages: does not perform feature selection (coefficients shrink
#   but rarely hit exactly zero), requires tuning alpha, requires feature
#   scaling to be meaningful.
# Bias-variance: increasing alpha increases bias, decreases variance —
#   directly tunable regularization/overfitting knob.
# Assumptions: same as linear regression (linearity, homoscedasticity) plus
#   the added regularization assumption that shrinkage improves generalization.
# Time complexity: O(n*d^2 + d^3) similar to OLS (closed-form via Cholesky/SVD).
# Space complexity: O(n*d).
# Scalability: use `solver="sag"/"saga"` or SGDRegressor with L2 penalty for
#   very large n or d.
# Interpretability: still interpretable via coefficients, though shrunk
#   values are less directly comparable to unregularized OLS coefficients.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# Lasso (L1) instead of Ridge (L2) for automatic feature selection.
# ElasticNet: combine L1 + L2 penalties for both selection and stability.
# RidgeCV: built-in efficient leave-one-out CV for alpha selection.
# Classification: use RidgeClassifier for L2-regularized linear classification.
# High-dimensional data (d >> n): Ridge is especially useful since OLS is
#   ill-conditioned or infeasible there.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: version the fitted pipeline artifact together
#   with the chosen alpha and CV results used to select it.
# Feature store integration: ensure the same scaling statistics used in
#   training are consistently applied at serving time.
# MLflow integration: log alpha search results, best CV R2, and the final
#   pipeline artifact for reproducibility.
# Monitoring: track live R2/MAE, feature distribution drift (especially
#   for the correlated features driving the need for regularization).
# Data/concept drift: monitor correlation structure between features over
#   time — a shift there can change the effective bias-variance tradeoff.
# Retraining strategy: retrain and re-tune alpha periodically as
#   feature correlations or target relationships shift.
# Explainability: coefficients remain interpretable; note shrinkage when
#   comparing magnitudes to an unregularized baseline.
# Model registry: register with alpha and CV score as tracked metadata.
# Batch vs real-time: cheap linear model, suitable for both batch scoring
#   and low-latency real-time inference.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: multicollinearity is present, or OLS coefficients are unstable/
#   high variance across resamples.
# Avoid when: feature selection/sparsity is needed (use Lasso instead).
# Advantages: stabilizes coefficients, handles correlated features, closed-
#   form solution, retains all features.
# Disadvantages: no automatic feature selection, needs alpha tuning, needs
#   feature scaling.
# Time complexity: ~O(n*d^2) train; O(d) predict per sample.
# Space complexity: O(n*d).
# Assumptions: linearity, homoscedasticity, regularization improves
#   generalization under multicollinearity.
# Important hyperparameters: alpha (regularization strength) — the single
#   most important knob; solver choice for large datasets.
# Interview questions to expect: derive the Ridge closed-form solution;
#   explain why Ridge never zeroes out coefficients (vs Lasso); bias-
#   variance tradeoff as alpha increases; why scaling matters for Ridge.
# Common mistakes: forgetting to scale features before fitting; not tuning
#   alpha via CV (using default value blindly); comparing Ridge and OLS
#   coefficients directly without accounting for shrinkage.
# Production checklist: alpha selected via CV logged with the model,
#   consistent scaling pipeline persisted with the model, monitored feature
#   correlation drift, versioned artifacts.
# ============================================================
