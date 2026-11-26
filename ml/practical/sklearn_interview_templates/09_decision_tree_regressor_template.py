"""
============================================================
TEMPLATE 9: Decision Tree Regressor
============================================================
Regression analogue of Template 8 — captures non-linear relationships via
recursive partitioning, using variance/MSE reduction instead of Gini/entropy
impurity. Interview-scoped (~45 min).
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
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
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
MODEL_PATH = "decision_tree_regressor_pipeline.joblib"
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
        # Piecewise/non-linear target — a linear model underfits this,
        # while a tree can capture the regime change at the threshold.
        base = np.where(df["num_feature_1"] > 55, 100, 20)
        df[TARGET_COLUMN] = base + 2.0 * df["num_feature_2"].fillna(20) + rng.normal(0, 5, n)
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

    # Scaling not required for trees, kept for pipeline consistency.
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
    # criterion="squared_error" minimizes variance within each leaf — the
    # regression equivalent of Gini/entropy impurity reduction.
    model = DecisionTreeRegressor(
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        criterion="squared_error",
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
    param_grid = {
        "model__max_depth": MAX_DEPTH_GRID,
        "model__min_samples_leaf": MIN_SAMPLES_LEAF_GRID,
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
        "Decision Tree (max_depth=5)": DecisionTreeRegressor(max_depth=5, random_state=RANDOM_SEED),
        "Decision Tree (unconstrained)": DecisionTreeRegressor(random_state=RANDOM_SEED),
    }
    print("\nModel comparison (CV R2):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="r2")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # On this piecewise-nonlinear target, LinearRegression underfits while a
    # depth-limited tree captures the regime split much more accurately.


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
        {"feature": feature_names, "importance": model.feature_importances_}
    ).sort_values("importance", ascending=False)
    print("\nFeature importances (variance reduction):")
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
# When to use: regression with non-linear, piecewise, or interaction-heavy
#   relationships between features and target that a linear model cannot
#   capture.
# Mathematical intuition: recursively splits the feature space, at each node
#   choosing the split that minimizes the weighted variance (MSE) of the
#   target within the resulting child nodes; predictions are the mean target
#   value of the training samples in the leaf a new sample falls into.
# Advantages: no scaling needed, captures non-linearities/interactions,
#   interpretable, handles mixed numeric/categorical features.
# Disadvantages: predictions are step-functions (discontinuous, constant
#   within each leaf) — poor at extrapolation and smooth trends; prone to
#   overfitting; unstable to small data changes.
# Bias-variance: shallow trees underfit (high bias); deep unconstrained
#   trees overfit (high variance) — same tradeoff as the classifier.
# Assumptions: none on distribution; assumes the target is well-approximated
#   by piecewise-constant regions.
# Time complexity: O(n * d * log(n)) training.
# Space complexity: O(number of nodes).
# Scalability: fast for small/medium data; rarely used standalone in
#   production — typically the base learner for ensembles.
# Interpretability: high — can visualize the tree and read exact decision
#   rules leading to each prediction.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# DecisionTreeClassifier: classification analogue (Template 8).
# criterion="friedman_mse"/"absolute_error"/"poisson": alternative split
#   criteria for different loss/robustness tradeoffs (absolute_error is more
#   robust to outliers than squared_error).
# ccp_alpha (cost-complexity pruning): prune a fully grown tree instead of
#   relying solely on max_depth/min_samples_leaf pre-pruning.
# Ensembling (Random Forest Regressor, Gradient Boosting Regressor):
#   combine many trees to smooth out the step-function behavior and reduce
#   variance — covered in later templates.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: version alongside training data snapshot, since
#   trees are sensitive to small data perturbations.
# Feature store integration: verify upstream feature semantics/units remain
#   stable, since learned split thresholds encode specific numeric cutoffs.
# MLflow integration: log max_depth, min_samples_leaf, criterion, and the
#   full CV score distribution.
# Monitoring: watch for prediction values clustering at a small number of
#   leaf means — a sign the tree isn't capturing enough granularity, or that
#   the input distribution has shifted away from trained leaf regions.
# Data/concept drift: monitor residuals over time; single trees can degrade
#   sharply if new data falls outside previously learned split boundaries.
# Retraining strategy: retrain on a schedule aligned with observed drift;
#   consider migrating to an ensemble for production stability.
# Explainability: `decision_path` and `apply` methods expose exactly which
#   leaf/rule path produced a given prediction.
# Model registry: register with hyperparameters and CV score distribution,
#   not just the mean.
# Batch vs real-time: fast O(depth) inference suits both batch and real-time
#   serving.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: regression with non-linear/piecewise relationships or as an
#   ensemble building block.
# Avoid when: the true relationship is smooth/linear (prefer linear models),
#   or when extrapolation beyond the training range matters (trees cannot
#   extrapolate beyond leaf means).
# Advantages: no scaling needed, captures non-linearity/interactions,
#   interpretable.
# Disadvantages: step-function predictions, overfits easily, unstable,
#   cannot extrapolate.
# Time complexity: O(n * d * log(n)) training, O(depth) inference.
# Space complexity: O(number of nodes).
# Assumptions: none on distribution; piecewise-constant approximation.
# Important hyperparameters: max_depth, min_samples_leaf, min_samples_split,
#   criterion, ccp_alpha.
# Interview questions to expect: how splits minimize variance; why trees
#   can't extrapolate; how to control overfitting; MSE vs MAE criterion
#   tradeoffs; when to prefer a tree over linear regression.
# Common mistakes: unconstrained max_depth in production, expecting smooth
#   predictions/extrapolation, not comparing against a linear baseline.
# Production checklist: confirm CV score stability across folds, verify
#   hyperparameters are tuned, evaluate whether an ensemble improves
#   robustness before shipping a single tree.
# ============================================================
