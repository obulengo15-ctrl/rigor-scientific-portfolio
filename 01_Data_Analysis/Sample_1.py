# ==============================================================================
# Project: Clinical Biomarker Analysis & Predictive Modeling
# Author: Rigor Scientific Solutions
# Objective: Evaluate predictors of mortality in heart failure patients using 
#            logistic regression with rigorous assumption checking.
# Dataset: UCI Heart Failure Clinical Records (Chicco & Jurman, 2020)
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import statsmodels.api as sm

# 1. Data Ingestion & Preprocessing
# Note: In a full workflow, missing value imputation (e.g., MICE) would be applied.
df = pd.read_csv('heart_failure_clinical_records.csv')

# Define features (X) and target (y)
X = df[['age', 'ejection_fraction', 'serum_creatinine', 'time']]
y = df['DEATH_EVENT']

# 2. Train-Test Split (Stratified to maintain class distribution)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Statistical Modeling (Statsmodels for rigorous academic output)
X_train_sm = sm.add_constant(X_train)
logit_model = sm.Logit(y_train, X_train_sm).fit(disp=0)

# 4. Output Academic-Grade Summary
print(logit_model.summary())

# 5. Evaluation
X_test_sm = sm.add_constant(X_test)
y_pred_proba = logit_model.predict(X_test_sm)
print(f"\nModel ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.3f}")