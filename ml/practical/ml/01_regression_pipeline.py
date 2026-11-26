"""
ML REGRESSION — end-to-end skeleton (sklearn)
Use when: predict a continuous value (price, demand, score, time)

WHY sklearn: fast to prototype, strong baselines, production-friendly pipelines.
WHY Pipeline: prevents data leakage (preprocessing fit only on train).
"""

# --- IMPORTS (memorize these) ---
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Optional: gradient boosting libs (pick ONE in interview based on familiarity)
# from xgboost import XGBRegressor
# from lightgbm import LGBMRegressor


# --- 1. LOAD DATA ---
def load_data(path: str) -> pd.DataFrame:
    # WHY: separate I/O from logic — easy to swap CSV / parquet / DB
    return pd.read_csv(path)


# --- 2. DEFINE FEATURES & TARGET ---
TARGET = "target_column"
NUMERIC_FEATURES = ["feature_a", "feature_b", "feature_c"]
CATEGORICAL_FEATURES = ["category_x", "category_y"]


# --- 3. PREPROCESSING ---
def build_preprocessor() -> ColumnTransformer:
    """
    WHY StandardScaler on numeric: many regressors are scale-sensitive (Ridge, SVM, NN).
    WHY OneHotEncoder on categorical: tree models can handle raw cats, but OHE works universally.
    """
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )


# --- 4. MODEL CHOICE (pick based on interview context) ---
def build_model(name: str = "ridge"):
    """
    Ridge     → linear, interpretable, fast baseline, multicollinearity
    Lasso     → linear + feature selection (sparse coefficients)
    RF        → nonlinear, robust, no scaling needed (but we scale anyway in pipeline)
    GBR/XGB   → tabular SOTA, handles interactions, wins most Kaggle tabular tasks
    """
    models = {
        "ridge": Ridge(alpha=1.0),
        "lasso": Lasso(alpha=0.01),
        "rf": RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
        "gbr": GradientBoostingRegressor(n_estimators=200, random_state=42),
        # "xgb": XGBRegressor(n_estimators=200, learning_rate=0.05, random_state=42),
    }
    return models[name]


# --- 5. FULL PIPELINE ---
def build_pipeline(model_name: str = "ridge") -> Pipeline:
    return Pipeline([
        ("preprocess", build_preprocessor()),
        ("model", build_model(model_name)),
    ])


# --- 6. TRAIN / EVAL ---
def train_and_evaluate(df: pd.DataFrame, model_name: str = "ridge"):
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    # WHY stratify=None for regression (stratify is for classification)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipe = build_pipeline(model_name)
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)

    # WHY these metrics:
    # MAE  → interpretable in original units
    # RMSE → penalizes large errors (common in production SLAs)
    # R²   → variance explained (quick sanity check)
    metrics = {
        "mae": mean_absolute_error(y_test, preds),
        "rmse": float(np.sqrt(mean_squared_error(y_test, preds))),
        "r2": r2_score(y_test, preds),
    }
    print(metrics)
    return pipe, metrics


# --- 7. HYPERPARAMETER TUNING (optional but impressive in interviews) ---
def tune_hyperparameters(df: pd.DataFrame):
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    pipe = build_pipeline("ridge")
    param_grid = {
        "model__alpha": [0.01, 0.1, 1.0, 10.0],
    }

    # WHY GridSearchCV: systematic search + cross-validation reduces overfitting to one split
    search = GridSearchCV(pipe, param_grid, cv=5, scoring="neg_mean_absolute_error", n_jobs=-1)
    search.fit(X_train, y_train)
    print("Best params:", search.best_params_)
    print("Val MAE:", -search.best_score_)
    return search.best_estimator_


# --- 8. SAVE FOR PRODUCTION ---
def save_model(pipe: Pipeline, path: str = "model_regression.joblib"):
    # WHY joblib: faster than pickle for large numpy arrays inside sklearn models
    joblib.dump(pipe, path)


def load_model(path: str = "model_regression.joblib") -> Pipeline:
    return joblib.load(path)


# --- 9. INFERENCE ---
def predict(pipe: Pipeline, raw_input: dict) -> float:
    # WHY DataFrame with column names: pipeline expects named columns, not raw arrays
    row = pd.DataFrame([raw_input])
    return float(pipe.predict(row)[0])


if __name__ == "__main__":
    # df = load_data("data/train.csv")
    # pipe, metrics = train_and_evaluate(df, model_name="gbr")
    # save_model(pipe)
    pass
