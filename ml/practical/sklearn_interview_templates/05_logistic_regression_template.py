"""
============================================================
TEMPLATE 5: Logistic Regression (Binary Classification)
============================================================
Predicting a binary class label. First classification template in this
series — introduces stratified splitting, classification metrics, and
class-imbalance handling on top of the regression workflow patterns from
Templates 1-4. Interview-scoped (~45 min).
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
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
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
MODEL_PATH = "logistic_regression_pipeline.joblib"
C_GRID = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]

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
        # Logit -> probability -> binary label (moderately imbalanced ~30/70).
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
    # Stratify to preserve class ratio in both splits, critical for
    # imbalanced classification.
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

    # Scaling matters for Logistic Regression: it's fit via gradient-based
    # solvers, and unscaled features slow/distort convergence.
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
def build_pipeline(preprocessor: ColumnTransformer, C: float = 1.0) -> Pipeline:
    # Logistic Regression: models log-odds as a linear function of features,
    # squashed through the sigmoid to produce class probabilities.
    # C is the inverse of regularization strength (smaller C -> stronger L2).
    model = LogisticRegression(
        C=C,
        penalty="l2",
        solver="lbfgs",
        max_iter=1000,
        class_weight="balanced",  # compensates for the ~30/70 imbalance
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
    # C controls regularization strength: smaller C -> stronger regularization
    # (simpler decision boundary), larger C -> fits training data more closely.
    param_grid = {"model__C": C_GRID}

    grid_search = GridSearchCV(pipeline, param_grid, cv=CV_FOLDS, scoring="f1", n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print(f"\nBest C: {grid_search.best_params_}")
    print(f"Best CV F1: {grid_search.best_score_:.4f}")
    return grid_search.best_estimator_


# ------------------------------------------------------------
# 12. Model Comparison
# ------------------------------------------------------------
def compare_models(X_train, y_train, preprocessor: ColumnTransformer) -> None:
    candidates = {
        "Dummy (most_frequent)": DummyClassifier(strategy="most_frequent"),
        "Dummy (stratified)": DummyClassifier(strategy="stratified", random_state=RANDOM_SEED),
        "Logistic Regression": LogisticRegression(
            max_iter=1000, class_weight="balanced", random_state=RANDOM_SEED
        ),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=RANDOM_SEED),
    }
    print("\nModel comparison (CV F1):")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        scores = cross_val_score(pipe, X_train, y_train, cv=CV_FOLDS, scoring="f1")
        print(f"  {name}: {scores.mean():.4f} +/- {scores.std():.4f}")
    # Logistic Regression is a strong, well-calibrated baseline for linearly
    # separable-ish problems; tree-based models can capture non-linear
    # interactions but may overfit without depth/leaf constraints.


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
    print("\nFeature coefficients (log-odds impact):")
    print(importance_df)
    # exp(coefficient) gives the odds ratio for a one-unit (scaled) increase.
    importance_df["odds_ratio"] = np.exp(importance_df["coefficient"])
    print("\nWith odds ratios:\n", importance_df)


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
# When to use: binary (or multinomial, via multi_class handling)
#   classification where a fast, interpretable, well-calibrated baseline is
#   needed — the default first model to try for classification tasks.
# Mathematical intuition: models P(y=1|x) = sigmoid(w^T x + b); trained by
#   maximizing log-likelihood (equivalently minimizing log-loss), typically
#   solved via gradient-based solvers (lbfgs, saga, etc.) since there's no
#   closed-form solution for the MLE.
# Advantages: fast to train/predict, naturally outputs calibrated
#   probabilities, interpretable coefficients (log-odds), regularization
#   built in (L1/L2/ElasticNet via penalty param), scales well.
# Disadvantages: assumes a linear decision boundary in (transformed) feature
#   space, struggles with complex non-linear interactions unless features
#   are engineered, sensitive to unscaled features.
# Bias-variance: regularization strength (1/C) controls bias-variance
#   tradeoff — smaller C (stronger regularization) increases bias, reduces
#   variance.
# Assumptions: linear relationship between features and log-odds,
#   observations independent, low multicollinearity for stable coefficients.
# Time complexity: O(n*d) per gradient-descent iteration x iterations.
# Space complexity: O(n*d) for the data, O(d) for the model.
# Scalability: scales well to large n and d, especially with saga solver for
#   very large/sparse datasets.
# Interpretability: high — coefficients translate directly to odds ratios.
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# Multinomial Logistic Regression: multi_class="multinomial" for >2 classes
#   (softmax instead of sigmoid).
# L1-penalized Logistic Regression: penalty="l1", solver="liblinear"/"saga"
#   for sparse/interpretable feature selection in classification.
# ElasticNet Logistic Regression: penalty="elasticnet", solver="saga".
# class_weight="balanced" or custom weights for imbalanced classes; SMOTE/
#   undersampling as data-level alternatives.
# SGDClassifier(loss="log_loss"): for online/out-of-core learning at scale.
# ============================================================


# ============================================================
# PRODUCTION IMPROVEMENTS
# ============================================================
# Pipeline/model versioning: version the fitted pipeline (preprocessing +
#   model) together, track C, penalty, and class_weight per version.
# Feature store integration: ensure feature computation logic (e.g., how
#   num_feature_1 is derived) matches exactly between training and serving.
# MLflow integration: log C, CV F1/ROC-AUC, and confusion matrix artifacts
#   per run.
# Monitoring: track prediction probability distribution over time (score
#   drift) and live precision/recall against delayed ground truth labels.
# Data/concept drift: monitor feature distributions (e.g., PSI/KS test) and
#   retrain if the input distribution or the class balance shifts materially.
# Retraining strategy: retrain on a schedule or when monitored F1/ROC-AUC on
#   fresh labeled data drops below a threshold.
# Explainability: coefficients/odds ratios are natively explainable; pair
#   with SHAP for consistency checks against more complex challenger models.
# Model registry: register with metadata including chosen classification
#   threshold (not just 0.5) tuned for business precision/recall tradeoffs.
# Batch vs real-time: extremely cheap to score — suitable for low-latency
#   real-time inference as well as large batch scoring jobs.
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: binary/multi-class classification with a need for a fast,
#   interpretable, probabilistic baseline model.
# Avoid when: the true decision boundary is highly non-linear and feature
#   engineering can't capture it — consider tree ensembles or kernel methods.
# Advantages: fast, interpretable, calibrated probabilities, well-understood,
#   regularization built in.
# Disadvantages: linear decision boundary assumption, needs feature scaling,
#   can underfit complex relationships.
# Time complexity: O(n*d) per solver iteration x iterations.
# Space complexity: O(n*d).
# Assumptions: linear log-odds relationship, independent observations, low
#   multicollinearity.
# Important hyperparameters: C (inverse regularization strength), penalty
#   (l1/l2/elasticnet), class_weight, solver, max_iter.
# Interview questions to expect: derive the sigmoid/log-loss; why use
#   log-loss instead of MSE for classification; L1 vs L2 penalty in
#   LogisticRegression; how to handle class imbalance; how to choose a
#   decision threshold other than 0.5.
# Common mistakes: using accuracy alone on imbalanced data; not scaling
#   features; leaving default class_weight=None on imbalanced problems;
#   using the default 0.5 threshold without considering business costs of
#   false positives vs false negatives.
# Production checklist: log the chosen decision threshold explicitly, store
#   class_weight/C used, validate ROC-AUC and calibration curves before
#   promoting, monitor real-world precision/recall drift post-deployment.
# ============================================================
