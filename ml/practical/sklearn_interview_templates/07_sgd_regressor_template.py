"""
============================================================
TEMPLATE 7: SGD Regressor (Linear Regression via Stochastic Gradient Descent)
============================================================
Regression analogue of Template 6 — fits linear models (OLS/Ridge/Lasso-
equivalent losses) incrementally via stochastic gradient descent, suited to
very large or streaming datasets. Interview-scoped (~45 min).
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
from sklearn.linear_model import SGDRegressor, LinearRegression, Ridge
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
MODEL_PATH = "sgd_regressor_pipeline.joblib"
ALPHA_GRID = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]

np.random.seed(RANDOM_SEED)


# ------------------------------------------------------------
# 3. Load Dataset
# ------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        rng = np.random.default_rng(RANDOM_SEED)
        n = 2000  # larger n to illustrate SGD's efficiency at scale
        df = pd.DataFrame(
            {
                "num_feature_1": rng.normal(50, 10, n),
                "num_feature_2": rng.normal(20, 5, n),
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

    # Scaling is essential — SGD step sizes are highly sensitive to feature
    # magnitude, more so than batch solvers like the normal equation.
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
def build_pipeline(preprocessor: ColumnTransformer, alpha: float = 1e-4) -> Pipeline:
    # loss="squared_error" + penalty="l2" -> Ridge-equivalent, trained via
    # SGD rather than the closed-form/cholesky solver. Useful when n is too
    # large to fit the full design matrix / compute X^T X efficiently.
    model = SGDRegressor(
        loss="squared_error",
        penalty="l2",
        alpha=alpha,
        max_iter=1000,
        tol=1e-3,
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
        "Linear Regression (closed-form)": LinearRegression(),
        "Ridge (closed-form)": Ridge(alpha=1.0, random_state=RANDOM_SEED),
        "SGDRegressor (squared_error)": SGDRegressor(
            loss="squared_error", max_iter=1000, random_state=RANDOM_SEED
        ),
    }
    print("\nModel comparison (CV R2):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="r2")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # At this dataset size, closed-form solvers typically match or slightly
    # beat SGD's accuracy; SGD's real advantage is memory/scalability, not
    # small-data accuracy.


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
# When to use: regression on very large datasets where the closed-form/
#   batch solvers used by LinearRegression/Ridge become too slow or memory-
#   intensive, or when online/incremental learning on streaming data is
#   required.
# Mathematical intuition: minimizes the same squared-error (+ optional L1/L2
#   penalty) objective as OLS/Ridge/Lasso, but updates weights incrementally
#   via gradient steps on one sample/mini-batch at a time instead of solving
#   the normal equation or using a full-batch iterative solver.
# Advantages: memory-efficient (no need to materialize X^T X), supports
#   `partial_fit` for true online learning, flexible loss/penalty
#   combinations approximate OLS/Ridge/Lasso/ElasticNet behavior at scale.
# Disadvantages: sensitive to feature scaling and learning-rate/alpha
#   choice, convergence is noisier and less precise than closed-form
#   solutions on small/medium data, needs more hyperparameter care.
# Bias-variance: alpha (regularization strength) and penalty type control
#   the bias-variance tradeoff, same as the batch counterparts.
# Assumptions: same linear regression assumptions as OLS/Ridge/Lasso.
# Time complexity: O(n*d) per epoch x epochs — scales linearly and doesn't
#   require the O(d^3) normal-equation solve that plain LinearRegression
#   uses internally.
# Space complexity: O(d) if used incrementally with partial_fit/mini-batches.
# Scalability: excellent for very large n; use partial_fit with a generator
#   feeding data in chunks for truly out-of-core training.
# Interpretability: same as the underlying linear model — coefficients are
#   directly interpretable.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# penalty="l1": Lasso-equivalent behavior at scale, sparse coefficients.
# penalty="elasticnet": ElasticNet-equivalent behavior at scale.
# loss="huber"/"epsilon_insensitive": robust regression losses, less
#   sensitive to outliers than squared_error.
# partial_fit + streaming batches: true online learning for continuously
#   arriving data (e.g., real-time pricing/demand models).
# learning_rate="constant"/"optimal"/"invscaling"/"adaptive": different
#   schedules for the step-size decay over training.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: snapshot/version model state periodically when
#   using continuous partial_fit updates, not just at full retrains.
# Feature store integration: streaming feature computation must exactly
#   match between the online training loop and the serving path.
# MLflow integration: log alpha, loss, penalty, and rolling validation
#   metrics; consider logging metrics per partial_fit checkpoint.
# Monitoring: track a rolling/windowed R2 or MAE instead of a single static
#   holdout metric, since the model is continuously updating.
# Data/concept drift: SGD's incremental nature adapts naturally to drift
#   when retrained continuously, but be careful about learning rate decay
#   causing the model to become unresponsive to new patterns over time.
# Retraining strategy: use partial_fit on new data chunks for streaming; for
#   batch pipelines, retrain on a schedule like any other linear model.
# Explainability: coefficient-based, same as OLS/Ridge/Lasso.
# Model registry: register with loss/penalty/alpha and last-seen-data
#   checkpoint metadata for traceability of online updates.
# Batch vs real-time: well suited for both online incremental training and
#   low-latency real-time inference.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: regression at large scale (n too big for closed-form solvers) or
#   streaming/online learning scenarios.
# Avoid when: dataset is small/medium — closed-form LinearRegression/Ridge
#   is simpler, more precise, and requires less tuning.
# Advantages: memory-efficient, supports online learning, flexible loss/
#   penalty combinations, scales to very large n.
# Disadvantages: sensitive to scaling/hyperparameters, noisier convergence,
#   needs more careful tuning than closed-form alternatives.
# Time complexity: O(n*d) per epoch x epochs.
# Space complexity: O(d) with incremental/partial_fit usage.
# Assumptions: same as OLS/Ridge/Lasso depending on penalty chosen.
# Important hyperparameters: loss, penalty, alpha, learning_rate,
#   max_iter/tol, n_iter_no_change (early stopping).
# Interview questions to expect: why/when SGDRegressor over LinearRegression/
#   Ridge; what does partial_fit enable; how learning rate schedules affect
#   convergence; tradeoffs of stochastic vs batch gradient descent.
# Common mistakes: not scaling features; picking alpha/learning_rate without
#   tuning; assuming SGD is always faster in wall-clock time even on small
#   datasets where closed-form solvers are actually faster.
# Production checklist: confirm convergence (no warnings) before deployment,
#   track rolling performance metrics for continuously-updating models,
#   version/checkpoint incremental model states.
# ============================================================
