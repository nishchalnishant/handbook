# scikit-learn Cheat Sheet

## Data Splitting & CV
```python
from sklearn.model_selection import (
    train_test_split, KFold, StratifiedKFold, GroupKFold,
    cross_val_score, cross_val_predict, cross_validate,
    GridSearchCV, RandomizedSearchCV
)
```

## Preprocessing
```python
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler,
    OneHotEncoder, OrdinalEncoder, LabelEncoder,
    PolynomialFeatures, Binarizer, Normalizer,
    PowerTransformer, FunctionTransformer
)
from sklearn.impute import SimpleImputer, KNNImputer
```

## Feature Selection / Extraction
```python
from sklearn.feature_selection import (
    SelectKBest, SelectPercentile, RFE, RFECV,
    VarianceThreshold, f_classif, f_regression, mutual_info_classif
)
from sklearn.decomposition import PCA, TruncatedSVD, NMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
```

## Pipeline / Compose
```python
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
```

## Linear Models
```python
from sklearn.linear_model import (
    LinearRegression, LogisticRegression,
    Ridge, Lasso, ElasticNet, SGDClassifier, SGDRegressor
)
```

## Tree / Ensemble Models
```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor,
    AdaBoostClassifier, VotingClassifier, StackingClassifier,
    BaggingClassifier
)
```

## Other Common Models
```python
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
```

## Model API (common to all estimators)
```python
model.fit(X, y)
model.predict(X)
model.predict_proba(X)     # classifiers
model.transform(X)
model.fit_transform(X)
model.score(X, y)
```

## Metrics
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve,
    mean_squared_error, mean_absolute_error, r2_score,
    silhouette_score
)
```

## Model Persistence
```python
import joblib
joblib.dump(model, "model.pkl")
model = joblib.load("model.pkl")
```

## Standard End-to-End Workflow (classical ML, tabular classification)
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# 1. Load
df = pd.read_csv("data.csv")
X, y = df.drop(columns=["target"]), df["target"]

# 2. Quick EDA (do this before modeling, not shown as code here)
# df.info(); df.describe(); df["target"].value_counts(normalize=True); df.isna().sum()

# 3. Split FIRST — before any fitting/statistics touch the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 4. Preprocessing, split by column type
numeric_features = X.select_dtypes(include="number").columns.tolist()
categorical_features = X.select_dtypes(exclude="number").columns.tolist()

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]), numeric_features),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]), categorical_features),
])

# 5. Full pipeline: preprocessing + model bundled so CV/search refit both per fold
pipe = Pipeline([
    ("preprocess", preprocessor),
    ("clf", RandomForestClassifier(class_weight="balanced", random_state=42)),
])

# 6. Cross-validate on train only, before touching test
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="f1_macro", n_jobs=-1)
print(f"CV f1_macro: {scores.mean():.3f} +/- {scores.std():.3f}")

# 7. (Optional) hyperparameter search — same cv splitter as above for comparability
param_grid = {
    "clf__n_estimators": [200, 400],
    "clf__max_depth": [None, 10, 20],
}
search = GridSearchCV(pipe, param_grid, cv=cv, scoring="f1_macro", n_jobs=-1)
search.fit(X_train, y_train)
best_pipe = search.best_estimator_

# 8. Final fit + evaluate ONCE on held-out test set
best_pipe.fit(X_train, y_train)
preds = best_pipe.predict(X_test)
proba = best_pipe.predict_proba(X_test)[:, 1]

print(classification_report(y_test, preds))
print("ROC-AUC:", roc_auc_score(y_test, proba))

# 9. Persist
joblib.dump(best_pipe, "model.pkl")
# reload: joblib.load("model.pkl").predict(new_X)
```

## Custom Transformer
```python
from sklearn.base import BaseEstimator, TransformerMixin

class LogTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, cols=None):
        self.cols = cols

    def fit(self, X, y=None):
        return self   # no state to learn, but must return self

    def transform(self, X):
        X = X.copy()
        cols = self.cols or X.columns
        X[cols] = np.log1p(X[cols])
        return X

# drop into any Pipeline like a built-in step
Pipeline([("log", LogTransformer(cols=["income"])), ("scaler", StandardScaler())])
```

## Hyperparameter Search — Nested Pipeline Param Naming
```python
# reaching into nested pipeline/columntransformer steps: step__substep__param
param_grid = {
    "clf__n_estimators": [100, 200, 300],
    "clf__max_depth": [None, 10, 20],
    "preprocess__num__imputer__strategy": ["mean", "median"],
}

grid = GridSearchCV(pipe, param_grid, cv=5, scoring="f1_macro", n_jobs=-1)
grid.fit(X_train, y_train)
grid.best_params_
grid.best_estimator_
```

## Imbalanced Data
```python
# simplest fix — no resampling needed
RandomForestClassifier(class_weight="balanced")
LogisticRegression(class_weight="balanced")

# resampling (must happen INSIDE cross-validation to avoid leakage)
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

imb_pipe = ImbPipeline([
    ("smote", SMOTE(random_state=42)),
    ("clf", RandomForestClassifier(random_state=42)),
])
imb_pipe.fit(X_train, y_train)   # SMOTE only ever sees training folds during CV
```

## Debugging / Common Mistakes Checklist
- **Data leakage from preprocessing**: never call `.fit()` or `.fit_transform()` on the full dataset before splitting — always `fit` only on train, `transform` (not `fit_transform`) on test/val. Wrap preprocessing in a `Pipeline` so `cross_val_score`/`GridSearchCV` refit it correctly per fold.
- **`fit_transform` vs `transform` confusion**: `fit_transform` on test data re-learns statistics (mean/std/categories) from test data — silently invalidates the evaluation. Only ever call `.transform()` on val/test.
- **`OneHotEncoder` fails at inference on unseen categories**: pass `handle_unknown="ignore"` (or `"infrequent_if_exist"`) or it raises at transform time on categories not seen during fit.
- **Resampling (SMOTE) before train/test split**: creates synthetic near-duplicates of test samples inside training — always split first, resample only inside the training folds via an `imblearn` Pipeline.
- **Accuracy misleading on imbalanced classes**: check `y.value_counts(normalize=True)` first; prefer F1/balanced-accuracy/PR-AUC when classes are skewed.
- **Forgetting `random_state`**: makes `train_test_split`, `KFold(shuffle=True)`, and most models non-reproducible between runs — set it everywhere for interview-repeatable results.
- **Comparing models with different CV folds**: use the same `cv` splitter (or a fixed `random_state`) across all models being compared, otherwise fold composition differs and results aren't comparable.
- **`StandardScaler` on one-hot/binary columns**: usually unnecessary and can hurt tree models not at all but may hurt distance-based models (KNN/SVM) if scaled inconsistently — scale only numeric columns via `ColumnTransformer`.
- **High train accuracy, poor test accuracy**: classic overfitting — reduce model complexity (`max_depth`, fewer estimators), add regularization (`C` in LogisticRegression/SVM, `alpha` in Ridge/Lasso), get more data, or use simpler features.
- **GridSearchCV taking too long**: switch to `RandomizedSearchCV` with a fixed `n_iter`, or narrow the grid based on a quick manual pass first.
