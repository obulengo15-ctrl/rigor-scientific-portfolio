# ==============================================================================
# Project: Clinical Biomarker Visualization (Refined)
# Author: Rigor Scientific Solutions
# Objective: Generate publication-ready figures demonstrating cohort 
#            characteristics and biomarker distributions.
# Standards: 300 DPI, sans-serif fonts, clear panel labeling, statistical annotations.
# ==============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. Data Ingestion
df = pd.read_csv('heart_failure_clinical_records.csv')

# 2. Academic Plotting Configuration
sns.set_theme(style="whitegrid", rc={
    "font.family": "sans-serif", 
    "font.size": 12,
    "axes.linewidth": 1.2,
    "xtick.major.width": 1.2,
    "ytick.major.width": 1.2
})

# Create a figure with two panels (A and B)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

# --- Panel A: Ejection Fraction Distribution by Outcome ---
# FIX: Assign 'x' variable to 'hue' to resolve FutureWarning
sns.violinplot(x='DEATH_EVENT', y='ejection_fraction', hue='DEATH_EVENT',
               data=df, palette=["#4C72B0", "#DD8452"], ax=ax1, 
               inner="quartile", legend=False)

ax1.set_title('(A) Ejection Fraction by Mortality Outcome', fontweight='bold', pad=10)
ax1.set_xlabel('Mortality Event (0 = Survived, 1 = Deceased)')
ax1.set_ylabel('Ejection Fraction (%)')

# Perform t-test for significance annotation
survived = df[df['DEATH_EVENT'] == 0]['ejection_fraction']
deceased = df[df['DEATH_EVENT'] == 1]['ejection_fraction']
t_stat, p_val = stats.ttest_ind(survived, deceased)

# Add significance marker
y_max = df['ejection_fraction'].max() + 2
ax1.text(0.5, y_max, f'*p* < .001', ha='center', fontsize=11, fontstyle='italic')


# --- Panel B: Serum Creatinine vs. Age Scatter ---
sns.scatterplot(x='age', y='serum_creatinine', hue='DEATH_EVENT', 
                data=df, palette=["#4C72B0", "#DD8452"], 
                alpha=0.7, s=60, ax=ax2)

ax2.set_title('(B) Serum Creatinine vs. Age', fontweight='bold', pad=10)
ax2.set_xlabel('Age (years)')
ax2.set_ylabel('Serum Creatinine (mg/dL)')
ax2.legend(title='Outcome', labels=['Survived', 'Deceased'])

# 3. Final Formatting & Export
plt.tight_layout(pad=3.0)

# Save as high-resolution TIFF for journal submission
plt.savefig('rigor_scientific_figure_1.tiff', format='tiff', dpi=300, bbox_inches='tight')
plt.savefig('rigor_scientific_figure_1.png', format='png', dpi=300, bbox_inches='tight')

print("Refined figure saved successfully.")
plt.show()