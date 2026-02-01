---
title: Socio-Economic Determinants of Healthcare Quality
layout: default
---

**Tools:** Google BigQuery (SQL), Python (Pandas, Scipy, Statsmodels, Seaborn)

<style>
.port-btn{
  display:inline-block;
  padding:.6rem 1rem;
  margin:.25rem .4rem 0 0;
  border-radius:8px;
  background:#0366d6;
  color:#fff !important;
  text-decoration:none !important;
  border:1px solid rgba(0,0,0,.08);
  box-shadow:0 1px 2px rgba(0,0,0,.05);
  font-weight:600;
}
.port-btn:hover{ filter:brightness(0.95); }
</style>

<div style="margin: 1rem 0;">
  <a class="port-btn" href="{{ '/statistical-tables' | relative_url }}">Statistical Tables</a>
  <a class="port-btn" href="{{ '/datasets' | relative_url }}">Datasets</a>
  <a class="port-btn" href="{{ '/sql-and-syntaxes' | relative_url }}">SQL & Syntax</a>
  <a class="port-btn" href="{{ '/data-dictionary' | relative_url }}">Data Dictionary</a>
  <a class="port-btn" href="{{ '/reproducibility' | relative_url }}">Reproducibility</a>
</div>

---

## Introduction & Project Objective
The goal of this project was to determine if hospital performance—specifically overall star ratings and readmission failures—is driven by internal operational efficiency or external socio-economic factors. We aimed to answer the “So What?” for hospital administrators: Are poor ratings a failure of medicine or a reflection of community poverty?

## Methodology
**Data Acquisition:** Data was extracted from Google BigQuery Public Datasets. We utilized the cms_medicare.hospital_general_info table for clinical/operational data and the census_bureau_acs.zip_codes_2017_5yr table for socio-economic metrics.  
**Data Engineering:** A SQL INNER JOIN was performed on the zip_code field. We utilized SAFE_CAST to transform clinical strings (e.g., “Better than Average”) into quantitative counts (readmission_measures_worse_count) and cleaned the dataset by removing “Not Available” entries.  
**Statistical Framework:**  
**ANOVA:** To test variance in quality across hospital ownership types.  
**Chi-Square:** To test the association between income levels and star ratings.  
**Multiple Linear Regression:** To quantify the predictive power of income and population size on readmission failures.

## Key Findings & Interpretation
# A. Operational Consistency (ANOVA)  
**Results: F-Statistic:** 0.11, P-Value: 0.7376.  
**Interpretation:** Because the p-value is significantly higher than 0.05, we fail to reject the null hypothesis.  
**Conclusion:** There is no statistically significant difference in quality ratings between “Acute Care” and “Critical Access” hospitals. Operational quality is consistent across these categories, suggesting that a hospital’s primary designation does not inherently limit its quality potential.

# B. The Wealth-Quality Gap (Chi-Square)  
**Results:** P-Value: 0.0000.  
**Interpretation:** The test showed a highly significant association between income groups and rating groups.  
**Conclusion:** High-income communities are disproportionately served by 4-5 star hospitals ($825$ facilities), while low-income communities are served by nearly double the amount of 1-3 star hospitals ($1,040$). This proves that quality is geographically and economically stratified.

# C. Predictive Drivers (Multiple Regression)  
**Results:** R-squared: 0.044, Income Coef: 8.764e-07 ($p=0.341$), Population Coef: 1.381e-05 ($p<0.001$).  
**Interpretation:** While community income is a standalone factor, when modeled alongside population size, population density becomes the dominant predictor of readmission failures.  
**Conclusion:** Large-scale hospitals in densely populated areas face significantly higher counts of readmission failures. This suggests that the volume of patients and the complexity of urban discharge planning are major clinical bottlenecks.

## Visual Highlights
**Correlation Matrix:** Revealed a moderate negative correlation (-0.34) between star ratings and readmission failures, confirming that readmission performance is a primary component of a hospital’s reputation.  
**Regression Trend:** The scatter plot visualized a “floor” where hospitals in communities with income below $50,000 had significantly higher clusters of maximum readmission failures (6-7 measures).

## Final Recommendations (The “So What?”)
**Risk-Adjusted Benchmarking:** CMS and healthcare regulators should move away from raw performance metrics. Benchmarks must be risk-adjusted for the Social Determinants of Health (SDE) of the hospital’s specific zip code to avoid unfairly penalizing facilities in high-density, low-income areas.  
**Strategic Resource Allocation:** Hospitals in “High Fail” clusters (low-income, high-population) should prioritize investments in Transition of Care (ToC) programs, such as mobile health units and community social workers, rather than just internal clinical equipment.  
**Policy Reform:** Policymakers should use this data to identify “Healthcare Deserts” where low-income and low-star ratings overlap, directing federal grants to these specific regions to break the cycle of poverty-driven clinical failure.

## Dataset Profile & Data Quality Notes
The final analytic file contains 3,182 hospitals joined to ZIP-level community context. It includes 2,706 Acute Care Hospitals and 476 Critical Access Hospitals.
Community income ranges from $13,625 to $250,001, with a median of $49,514. Community population ranges from 161 to 114,129, with a median of 24,202.5.
There is one row with a missing readmission success count and one row with a missing readmission failure count. Those rows were excluded from the regression model so the coefficient estimates reflect complete-case results.

## Additional Quantification of the Visual Story
The boxplot pattern you visualized is consistent with a near-zero practical difference in average star ratings by hospital type. In this dataset, Acute Care Hospitals average 3.25 stars and Critical Access Hospitals average 3.23 stars, which aligns with the “no meaningful gap” interpretation in the ANOVA.

The correlation matrix relationship between readmission failures and star ratings shows up as a clear step-down when you summarize stars by failure count. Hospitals with 0 “worse-than-national” readmission measures average 3.52 stars, while hospitals with 3 failures average 2.44 stars, and hospitals with 5 failures average 1.94 stars.

The Chi-Square finding can also be expressed as an odds statement that is easy for executives to grasp. High-income communities have about 2.04× higher odds of being served by a 4–5 star hospital compared to low-income communities (95% CI: 1.77 to 2.35), which reinforces the stratification conclusion using an effect-size lens.

## Model Diagnostics & Robustness Checks
Because readmission failures are counts with many zeros, the linear regression will naturally show non-constant variance in residuals, which is what you would expect when modeling a “pile-up at zero” outcome. A heteroskedasticity test flags this pattern, so the clean way to interpret the model is to focus on directionality and confirm significance with robust standard errors.

When robust standard errors are applied, the population coefficient remains strongly significant, while the income coefficient remains non-significant. This supports the same core conclusion: population burden dominates once you put income and population into the same equation.

Income is statistically significant when modeled alone, but it explains almost none of the variation by itself (R-squared ≈ 0.003). This is a useful nuance because it explains why the income-versus-failures scatter line slopes upward slightly, even though “poverty drives worse outcomes” is the common narrative; the upward slope is largely a population-size artifact in this joined ZIP-level view.

## Interaction Insight: Where Risk Concentrates Most
When you stratify by population quartile, the “high risk” profile becomes more precise. In the highest population quartile, low-income communities average about 1.12 readmission failures, while high-income communities average about 0.98, which is consistent with the idea that density amplifies the operational and social complexity of discharge planning.

This is the practical “pressure point” your visuals are hinting at. It is not just poverty or just size. It is the combination of low income and high population that produces the most consistent elevation in failures.

## Practical Interpretation of the Population Coefficient
The population coefficient (1.381e-05 per person) sounds abstract until you scale it. An increase of 10,000 community residents is associated with about +0.138 additional “worse-than-national” readmission measures, holding income constant, which accumulates quickly in large service areas.

That translates well to operations language. Bigger catchment areas tend to mean more handoffs, more fragmented outpatient follow-up, more transportation constraints, and more variability in caregiver support, which can make readmission prevention harder even when inpatient care is strong.

## Portfolio-Ready Reproducibility Add-On (Based on What You Already Built)
Your current report is already “executive readable,” and the visuals reinforce it. The strongest next addition for a portfolio reviewer is a short reproducibility appendix that ties artifacts together end-to-end.
