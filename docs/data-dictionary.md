# Data dictionary

This dictionary documents the engineered fields used in the analysis.

| Field Name | Type | Description | Engineering Logic |
|---|---:|---|---|
| `star_rating` | INT64 | The overall quality score (1–5) of the hospital. | `SAFE_CAST` used to convert string labels into integers for ANOVA. |
| `readmit_success_count` | INT64 | Number of clinical measures where the hospital performed better than the national average. | Aggregated count converted from string to INT for correlation. |
| `readmit_fail_count` | INT64 | Number of clinical measures where the hospital performed worse than the national average. | Targeted metric for Regression analysis; converted via `SAFE_CAST`. |
| `community_income` | FLOAT64 | Median household income for the hospital’s primary service Zip Code. | Joined from Census Bureau ACS data to represent SDE. |
| `community_population` | INT64 | Total population of the Zip Code. | Used as a control variable in Multiple Regression. |

## SAFE_CAST logic used for the readmission counts

The analysis relies on the CMS-provided readmission count fields and converts them into numerical form:

```sql
SAFE_CAST(h.readmission_measures_better_count AS INT64) as readmit_success_count,
SAFE_CAST(h.readmission_measures_worse_count  AS INT64) as readmit_fail_count
```
