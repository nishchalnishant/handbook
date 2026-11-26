"""
ML Interview — Import Cheat Sheet
Copy-paste the block you need at the top of your solution.
"""

# --- Data ---
import pandas as pd
import numpy as np

# --- Sklearn: preprocessing ---
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# --- Sklearn: models ---
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier

# --- Sklearn: metrics ---
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,           # regression
    accuracy_score, precision_score, recall_score, f1_score,     # classification
    confusion_matrix, classification_report, roc_auc_score,
    balanced_accuracy_score,
)

# --- Imbalanced data ---
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline  # use instead of sklearn Pipeline when SMOTE inside

# --- Production ---
import joblib
import pickle
import json
from pathlib import Path

# --- Optional: visualization (mention in interview, don't always need) ---
# import matplotlib.pyplot as plt
# import seaborn as sns
