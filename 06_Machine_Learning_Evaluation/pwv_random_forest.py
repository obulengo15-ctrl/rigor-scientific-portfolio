# ==============================================================================
# Project: Machine Learning Estimation of PWV from Surface Meteorology
# Method: Random Forest Regressor with k-Fold Cross-Validation
# ==============================================================================

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

# 1. Mock Feature Matrix (Temperature, Pressure, Relative Humidity)
X = np.random.rand(500, 3) * [30, 100, 100] # T, P, RH
y = 10 + 0.5*X[:, 0] - 0.01*X[:, 1] + 0.2*X[:, 2] + np.random.normal(0, 1, 500) # Mock PWV

# 2. Preprocessing (Crucial for ML reproducibility)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Rigorous Model Evaluation (k-Fold Cross-Validation)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Calculate cross-validated R2 and RMSE
cv_r2 = cross_val_score(rf_model, X_scaled, y, cv=kf, scoring='r2')
cv_rmse = np.sqrt(-cross_val_score(rf_model, X_scaled, y, cv=kf, scoring='neg_mean_squared_error'))

print("--- 5-Fold Cross-Validation Results ---")
print(f"Mean CV R-squared: {np.mean(cv_r2):.3f} +/- {np.std(cv_r2):.3f}")
print(f"Mean CV RMSE: {np.mean(cv_rmse):.2f} +/- {np.std(cv_rmse):.2f} mm")

# 4. Final Fit and Feature Importance
rf_model.fit(X_scaled, y)
importances = rf_model.feature_importances_
features = ['Temperature', 'Pressure', 'Relative Humidity']

print("\n--- Feature Importance ---")
for name, imp in zip(features, importances):
    print(f"{name}: {imp:.3f}")