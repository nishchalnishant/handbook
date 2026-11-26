# Scikit-learn Interview Templates

66 self-contained, runnable Python templates covering interview-scoped ML algorithms/workflows, for AI Engineer (SDE-2) coding rounds.

## Shared conventions (apply to every file)

- No classes anywhere. Plain top-level UPPER_CASE constants (`RANDOM_SEED`, `TEST_SIZE`, `CV_FOLDS`, `DATA_PATH`, `TARGET_COLUMN`, `MODEL_PATH`, hyperparameter grids) instead of a Config class. Comments carry explanatory weight instead of structure.
- Every file starts with the identical 8-step "General ML Model Development Workflow" comment header.
- `load_data()` tries `pd.read_csv(DATA_PATH)` and falls back to a synthetic dataset (seeded via `np.random.default_rng(RANDOM_SEED)`) on `FileNotFoundError`, so every file runs standalone with no external data.
- The synthetic data in each file is **deliberately shaped** to demonstrate that algorithm's specific strength/weakness (e.g. Decision Tree templates use threshold/regime-based targets that linear models underfit; ensemble templates use interaction-based targets that need ensembling to generalize). This is not boilerplate — check it if you want to see *why* the template picked that algorithm's teaching example.
- Preprocessing always goes through `ColumnTransformer` + `Pipeline`, never applied outside the pipeline (avoids data leakage). Categorical encoding always uses `OneHotEncoder(handle_unknown="ignore")`.
- Standard 18-part section order: imports → config → load data → EDA → split → feature engineering → preprocessing pipeline → model construction → training → evaluation → hyperparameter tuning (GridSearchCV) → model comparison (vs Dummy + prior algorithms) → error analysis → feature importance → save (joblib) → load → predict on new sample → `main()`.
- Every file closes with four fixed comment blocks: **INTERVIEW EXPLANATION**, **VARIATIONS**, **PRODUCTION IMPROVEMENTS**, **SUMMARY**.
- Every file verified with `python3 -c "import ast; ast.parse(...)"` immediately after being written.

## What actually differs file-to-file

Only these things change between templates — everything else above is fixed:
1. Synthetic data generator shape (tailored per algorithm)
2. Model construction + its specific hyperparameters/grids
3. Comparison baselines chosen (always includes Dummy + relevant prior algorithms)
4. Content of the four closing comment blocks

## Progress (66 total)

Linear models: 1 Linear Regression ✅ · 2 Ridge ✅ · 3 Lasso ✅ · 4 ElasticNet ✅ · 5 Logistic Regression ✅ · 6 SGD Classifier ✅ · 7 SGD Regressor ✅

Trees: 8 Decision Tree Classifier ✅ · 9 Decision Tree Regressor ✅

Ensembles: 10 Random Forest ✅ · 11 Extra Trees ✅ · 12 AdaBoost ✅ · 13 Gradient Boosting ✅ · 14 HistGradientBoosting · 15 Voting Classifier · 16 Voting Regressor · 17 Stacking Classifier · 18 Stacking Regressor · 19 Bagging

SVM: 20 Linear SVM · 21 Kernel SVM · 22 SVR

Neighbors: 23 KNN Classifier · 24 KNN Regressor

Naive Bayes: 25 Gaussian NB · 26 Multinomial NB · 27 Bernoulli NB

Clustering: 28 K-Means · 29 MiniBatch K-Means · 30 DBSCAN · 31 Agglomerative · 32 Mean Shift · 33 Spectral Clustering · 34 Gaussian Mixture Models

Dimensionality reduction: 35 PCA · 36 Kernel PCA · 37 Truncated SVD · 38 t-SNE · 39 UMAP

Anomaly detection: 40 Isolation Forest · 41 Local Outlier Factor · 42 One-Class SVM · 43 Elliptic Envelope

Similarity search: 44 Nearest Neighbors · 45 Cosine Similarity Search

Model selection / tuning: 46 Cross Validation · 47 GridSearchCV · 48 RandomizedSearchCV · 49 Learning Curves · 50 Validation Curves

Feature engineering/selection: 51 ColumnTransformer · 52 FeatureUnion · 53 Polynomial Features · 54 SelectKBest · 55 RFE · 56 Permutation Importance

End-to-end / production pipelines: 57 E2E Classification · 58 E2E Regression · 59 Multi-Class Classification · 60 Imbalanced Classification · 61 Time-Series Feature Engineering · 62 Batch Inference · 63 Real-Time Inference · 64 Model Monitoring Skeleton · 65 Drift Detection Skeleton · 66 Complete Production ML Template

## Heads-up: templates that will deviate from the standard structure

- **38 (t-SNE), 39 (UMAP)**: visualization/embedding techniques, not predictive models — no train/test split, no GridSearchCV in the usual sense, no `predict()` on new samples in the typical way (t-SNE has no `.transform`; UMAP does). Evaluation section will be replaced with embedding-quality discussion instead of classification/regression metrics.
- **28–34 (clustering)**: unsupervised — no `y` target from the source data, no stratified split, evaluation uses silhouette/Davies-Bouldin/ARI instead of accuracy/F1, "prediction on new sample" means cluster assignment, not a label.
- **40–43 (anomaly detection)**: often no clean ground-truth labels; evaluation framed around contamination rate / precision-recall on injected anomalies.
- **46–50 (model selection/tuning)**: these ARE the technique being demonstrated (e.g. Learning Curves, Validation Curves) rather than wrapping a specific model — the file's centerpiece is the diagnostic technique itself, applied to a representative model.
- **51–56 (feature engineering/selection)**: centerpiece is the transformer/selection technique, not a specific estimator; structure will bend to show before/after feature counts and downstream model performance impact rather than the usual full 18-part flow.
- **57–66 (end-to-end / production pipelines)**: broader in scope than a single algorithm — expect additional structure not present elsewhere (e.g. batch vs real-time serving code paths for 62/63, monitoring/drift-check functions for 64/65, a consolidated "template of templates" for 66). These will still follow the workflow header and no-classes rule but the 18-part section list won't map 1:1.

## Related paused work

A parallel PyTorch template batch (30 templates, deep learning architectures) is paused in a sibling folder `../pytorch_interview_templates/` at template 15/30, resuming only when explicitly requested. That batch uses a Config-class convention — intentionally different style from this sklearn batch's no-classes rule.
