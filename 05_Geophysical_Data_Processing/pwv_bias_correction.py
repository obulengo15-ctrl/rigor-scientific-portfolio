# ==============================================================================
# Project: GNSS vs. ERA5 Precipitable Water Vapor (PWV) Bias Correction
# Author: Rigor Scientific Solutions
# Context: Quality control and statistical evaluation of reanalysis data 
#          against ground-truth GNSS observations in East Africa.
# ==============================================================================

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# 1. Simulated Data Ingestion (In practice, loaded via xarray/netCDF4 for ERA5)
# Creating a mock hourly time series for demonstration
dates = pd.date_range(start="2024-01-01", end="2024-01-31", freq="h")
np.random.seed(42)
gnss_pwv = np.random.normal(45, 5, len(dates)) # Ground truth (mm)
era5_pwv = gnss_pwv + np.random.normal(2.5, 1.5, len(dates)) # ERA5 with systematic bias

df = pd.DataFrame({'datetime': dates, 'GNSS_PWV': gnss_pwv, 'ERA5_PWV': era5_pwv})
df.set_index('datetime', inplace=True)

# 2. Quality Control & Temporal Alignment
# Dropping overlapping NaNs and ensuring hourly synchronization
df_clean = df.dropna()

# 3. Statistical Evaluation & Bias Correction
# Calculate systematic bias (Mean Bias Error) and RMSE
bias = np.mean(df_clean['ERA5_PWV'] - df_clean['GNSS_PWV'])
rmse = np.sqrt(np.mean((df_clean['ERA5_PWV'] - df_clean['GNSS_PWV'])**2))
pearson_r, p_value = stats.pearsonr(df_clean['GNSS_PWV'], df_clean['ERA5_PWV'])

print(f"--- ERA5 vs GNSS PWV Evaluation ---")
print(f"Mean Bias Error (MBE): {bias:.2f} mm")
print(f"Root Mean Square Error (RMSE): {rmse:.2f} mm")
print(f"Pearson Correlation (r): {pearson_r:.3f} (p < {p_value:.2e})")

# 4. Apply Linear Bias Correction
# Simple linear regression to correct ERA5 systematic overestimation
slope, intercept, _, _, _ = stats.linregress(df_clean['ERA5_PWV'], df_clean['GNSS_PWV'])
df_clean['ERA5_Corrected'] = (df_clean['ERA5_PWV'] * slope) + intercept

print("\nBias correction applied. Corrected RMSE:", 
      np.sqrt(np.mean((df_clean['ERA5_Corrected'] - df_clean['GNSS_PWV'])**2)).round(2), "mm")