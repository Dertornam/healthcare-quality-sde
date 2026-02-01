# SQL and syntaxes

## BigQuery SQL join query

Use this query in the BigQuery console (ensure the **Data Location** is set to **US**).  
This script joins clinical and census datasets while handling data type conversions to ensure the Python environment receives clean, numerical data.

```sql
SELECT 
    h.hospital_name,
    h.hospital_type,
    -- Engineering Star Rating: Converting categorical ratings to Integers
    SAFE_CAST(h.hospital_overall_rating AS INT64) as star_rating,

    -- Engineering Readmission Success: Quantitative count of "Better than National" measures
    SAFE_CAST(h.readmission_measures_better_count AS INT64) as readmit_success_count,

    -- Engineering Readmission Failure: Quantitative count of "Worse than National" measures
    SAFE_CAST(h.readmission_measures_worse_count AS INT64) as readmit_fail_count,

    -- Population Health Metrics: Median Income and Total Population
    c.median_income as community_income,
    c.total_pop as community_population
FROM `bigquery-public-data.cms_medicare.hospital_general_info` h
JOIN `bigquery-public-data.census_bureau_acs.zip_codes_2017_5yr` c 
    ON h.zip_code = c.geo_id
WHERE h.hospital_overall_rating != 'Not Available'
  AND h.readmission_measures_worse_count IS NOT NULL
  AND c.median_income IS NOT NULL
LIMIT 5000
```

## Python analysis script

This script produces the visuals and statistical tests featured in the report.  
It assumes the file is uploaded to Google Colab as `healthcare_data.csv`.

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import statsmodels.api as sm

# 1. LOAD & CLEAN DATA
df = pd.read_csv('healthcare_data.csv').dropna()

# 2. VISUALIZATION: EXECUTIVE CORRELATION MATRIX
plt.figure(figsize=(10, 8))
corr = df[['star_rating', 'readmit_success_count', 'readmit_fail_count', 'community_income', 'community_population']].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, cmap='RdBu_r', center=0, fmt='.2f')
plt.title('Correlation Matrix: Clinical vs. Socioeconomics')
plt.show()

# 3. STATISTICAL TEST: ANOVA (OPERATIONS)
# Comparing Star Ratings across Hospital Types
types = df['hospital_type'].unique()
groups = [df[df['hospital_type'] == t]['star_rating'] for t in types]
f_stat, p_val_anova = stats.f_oneway(*groups)
print(f"ANOVA P-Value: {p_val_anova:.4f} (Result: {'Significant' if p_val_anova < 0.05 else 'Not Significant'})")

# 4. STATISTICAL TEST: CHI-SQUARE (INCOME VS RATING)
income_median = df['community_income'].median()
df['income_group'] = df['community_income'].apply(lambda x: 'High' if x >= income_median else 'Low')
df['rating_group'] = df['star_rating'].apply(lambda x: '4-5 Stars' if x >= 4 else '1-3 Stars')
contingency = pd.crosstab(df['income_group'], df['rating_group'])
chi2, p_val_chi, dof, ex = stats.chi2_contingency(contingency)
print(f"Chi-Square P-Value: {p_val_chi:.4f}")

# 5. MODELING: MULTIPLE LINEAR REGRESSION
# Predicting Readmission Failures using Income and Population
X = sm.add_constant(df[['community_income', 'community_population']])
y = df['readmit_fail_count']
model = sm.OLS(y, X).fit()
print(model.summary())

# 6. VISUALIZATION: POPULATION VS CLINICAL FAILURE
plt.figure(figsize=(12, 7))
sns.scatterplot(data=df, x='community_income', y='readmit_fail_count', hue='hospital_type', alpha=0.5)
sns.regplot(data=df, x='community_income', y='readmit_fail_count', scatter=False, color='red')
plt.title('Income Impact on Readmission Failures')
plt.show()
```
