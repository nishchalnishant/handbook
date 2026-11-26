"""
============================================================
TEMPLATE 6: SGD Classifier (Linear Classification via Stochastic Gradient Descent)
============================================================
Binary classification using linear models trained with stochastic gradient
descent — supports multiple loss functions (log_loss, hinge, etc.) and
scales to very large/streaming datasets that don't fit in memory.
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
from sklearn.linear_model import SGDClassifier, LogisticRegression
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
MODEL_PATH = "sgd_classifier_pipeline.joblib"
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
        num_feature_1 = rng.normal(50, 10, n)
        num_feature_2 = rng.normal(20, 5, n)
        cat_feature_1 = rng.choice(["A", "B", "C"], n)
        df = pd.DataFrame(
            {
                "num_feature_1": num_feature_1,
                "num_feature_2": num_feature_2,
                "cat_feature_1": cat_feature_1,
            }
        )
        df.loc[df.sample(frac=0.05, random_state=RANDOM_SEED).index, "num_feature_2"] = np.nan
        logit = 0.05 * num_feature_1 - 0.08 * num_feature_2 - 2.0 + rng.normal(0, 1, n)
        prob = 1 / (1 + np.exp(-logit))
        df[TARGET_COLUMN] = (prob > 0.6).astype(int)
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

    # Scaling is critical for SGD-based solvers — gradient step sizes are
    # very sensitive to feature magnitude, unlike tree-based models.
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
    # loss="log_loss" -> equivalent to Logistic Regression but trained via
    # SGD instead of batch solvers (lbfgs). Enables partial_fit for
    # streaming/out-of-core training on datasets too large for memory.
    # penalty="l2" regularizes; alpha controls regularization strength
    # (opposite convention to LogisticRegression's C: higher alpha = more
    # regularization).
    model = SGDClassifier(
        loss="log_loss",
        penalty="l2",
        alpha=alpha,
        max_iter=1000,
        tol=1e-3,
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
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred),
        "ROC-AUC": roc_auc_score(y_test, y_proba),
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
    # alpha: regularization strength. Also commonly tuned: loss, penalty,
    # learning_rate schedule (kept fixed here for interview scope).
    param_grid = {"model__alpha": ALPHA_GRID}

    grid_search = GridSearchCV(pipeline, param_grid, cv=CV_FOLDS, scoring="f1", n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print(f"\nBest alpha: {grid_search.best_params_}")
    print(f"Best CV F1: {grid_search.best_score_:.4f}")
    return grid_search.best_estimator_


# ------------------------------------------------------------
# 12. Model Comparison
# ------------------------------------------------------------
def compare_models(X_train, y_train, preprocessor: ColumnTransformer) -> None:
    candidates = {
        "Dummy (most_frequent)": DummyClassifier(strategy="most_frequent"),
        "Logistic Regression (lbfgs)": LogisticRegression(
            max_iter=1000, class_weight="balanced", random_state=RANDOM_SEED
        ),
        "SGDClassifier (log_loss)": SGDClassifier(
            loss="log_loss", max_iter=1000, class_weight="balanced", random_state=RANDOM_SEED
        ),
        "SGDClassifier (hinge/linear SVM)": SGDClassifier(
            loss="hinge", max_iter=1000, class_weight="balanced", random_state=RANDOM_SEED
        ),
    }
    print("\nModel comparison (CV F1):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="f1")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # On small/medium datasets, batch solvers (lbfgs) often converge to a
    # similar or better optimum than SGD; SGD's advantage appears at scale
    # (large n) or when streaming/incremental learning is required.


# ------------------------------------------------------------
# 13. Error Analysis
# ------------------------------------------------------------
def error_analysis(pipeline: Pipeline, X_test, y_test) -> None:
    y_pred = pipeline.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion matrix breakdown:")
    tn, fp, fn, tp = cm.ravel()
    print(f"  True Negatives: {tn}, False Positives: {fp}")
    print(f"  False Negatives: {fn}, True Positives: {tp}")

    misclassified_mask = y_pred != y_test.values
    misclassified = X_test[misclassified_mask].copy()
    misclassified["y_true"] = y_test[misclassified_mask].values
    misclassified["y_pred"] = y_pred[misclassified_mask]
    print(f"\nMisclassified samples: {len(misclassified)} / {len(y_test)}")
    print(misclassified.head(5))


# ------------------------------------------------------------
# 14. Feature Importance
# ------------------------------------------------------------
def feature_importance(pipeline: Pipeline) -> None:
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()
    importance_df = pd.DataFrame(
        {"feature": feature_names, "coefficient": model.coef_[0]}
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
            "num_feature_1": [60.0],
            "num_feature_2": [15.0],
            "cat_feature_1": ["A"],
        }
    )
    prediction = pipeline.predict(new_sample)
    probability = pipeline.predict_proba(new_sample)[:, 1]
    print(f"\nPrediction on new sample: class={prediction[0]}, P(class=1)={probability[0]:.4f}")


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
# When to use: very large datasets (millions of rows) or streaming/online
#   learning scenarios where batch solvers (e.g., lbfgs used by
#   LogisticRegression) don't scale or new data arrives continuously.
# Mathematical intuition: same underlying linear models as Logistic
#   Regression/Linear SVM, but weights are updated incrementally using one
#   sample (or a mini-batch) at a time via stochastic gradient descent,
#   rather than computing the full-batch gradient each step.
# Advantages: memory-efficient (processes one sample/mini-batch at a time),
#   supports `partial_fit` for online/incremental learning, flexible via the
#   `loss` parameter (log_loss=logistic regression, hinge=linear SVM,
#   modified_huber, etc.), scales to very large n.
# Disadvantages: sensitive to feature scaling and learning-rate/alpha
#   choice, noisier convergence than batch solvers, typically needs more
#   careful tuning (learning_rate schedule, n_iter_no_change, tol) to match
#   batch-solver accuracy on small/medium data.
# Bias-variance: alpha (regularization strength) controls bias-variance;
#   too few iterations can leave the model underfit (hasn't converged).
# Assumptions: same as the underlying loss's model family (linear
#   log-odds for log_loss, max-margin linear separator for hinge).
# Time complexity: O(n*d) per epoch x number of epochs — independent of n
#   for each individual update, enabling online learning.
# Space complexity: O(d) — does not need to hold the full dataset in memory
#   if used with partial_fit and mini-batches/generators.
# Scalability: excellent — designed for datasets larger than available RAM.
# Interpretability: same as Logistic Regression/Linear SVM depending on loss
#   — coefficients remain directly interpretable.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# loss="hinge": linear SVM trained via SGD (SGDClassifier subsumes
#   LinearSVC's use case at scale).
# loss="modified_huber": smooth loss enabling both probability estimates
#   and robustness to outliers.
# SGDRegressor: the regression analogue (Template 7).
# partial_fit + mini-batches: true online learning loop for streaming data
#   pipelines (e.g., consuming from a Kafka topic).
# learning_rate="adaptive"/"invscaling": alternative learning-rate schedules
#   for convergence tuning.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: version each incremental partial_fit update or
#   snapshot periodically if using true online learning.
# Feature store integration: streaming features must be computed
#   consistently between the online training loop and serving path.
# MLflow integration: log alpha, loss, and rolling CV/online metrics; log
#   each partial_fit checkpoint if doing continuous training.
# Monitoring: track online learning curve (rolling loss/accuracy) instead
#   of a single static test set, since the model continues to update.
# Data/concept drift: SGD's online nature makes it naturally adaptive to
#   drift if retrained continuously — but must guard against catastrophic
#   forgetting of older patterns if drift is transient rather than permanent.
# Retraining strategy: for streaming setups, use partial_fit on new data
#   batches; for batch setups, retrain periodically like any linear model.
# Explainability: same as Logistic Regression/Linear SVM — coefficient-based.
# Model registry: register with the training loss/penalty/alpha, and a
#   pointer to the latest data checkpoint the online model has seen.
# Batch vs real-time: naturally fits real-time incremental training +
#   real-time low-latency inference use cases.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: dataset is too large for batch solvers, or online/incremental
#   learning on streaming data is required.
# Avoid when: dataset is small/medium and a batch solver (e.g.,
#   LogisticRegression's lbfgs) converges reliably and is simpler to tune.
# Advantages: memory-efficient, supports online learning via partial_fit,
#   flexible loss functions, scales to very large datasets.
# Disadvantages: sensitive to scaling and hyperparameters, noisier
#   convergence, may need more tuning than batch alternatives for comparable
#   accuracy.
# Time complexity: O(n*d) per epoch x epochs; O(d) memory per update.
# Space complexity: O(d) if used incrementally; O(n*d) if data is held
#   entirely in memory for standard `fit`.
# Assumptions: depends on chosen loss (linear log-odds for log_loss, linear
#   max-margin for hinge).
# Important hyperparameters: loss, penalty, alpha, learning_rate,
#   max_iter/tol, n_iter_no_change (early stopping).
# Interview questions to expect: SGD vs batch gradient descent tradeoffs;
#   what does `partial_fit` enable that `fit` doesn't; why alpha's meaning
#   differs from LogisticRegression's C; when would you pick SGDClassifier
#   over LogisticRegression or LinearSVC.
# Common mistakes: not scaling features; not tuning alpha/learning_rate
#   causing poor convergence; assuming SGD is always faster in wall-clock
#   time on small datasets (batch solvers can win there); ignoring
#   convergence warnings.
# Production checklist: verify convergence behavior on validation data,
#   version each partial_fit update if streaming, monitor rolling
#   performance metrics rather than a single static evaluation.
# ============================================================
