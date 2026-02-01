[Home](./) | [Statistical tables](statistical-tables) | [Datasets](datasets) | [SQL & syntaxes](sql-and-syntaxes) | [Data dictionary](data-dictionary) | [Reproducibility](reproducibility)


# Data dictionary

This dictionary focuses on engineered fields and analysis-ready variables.

## Engineered fields (copy/paste from your BigQuery logic)

Field: `readmit_success_count`
Definition: Count of readmission measures that are “better than national” (or your equivalent category).
Source: Engineered from CMS readmission measure strings in BigQuery using `SAFE_CAST` and conditional logic.
Exact logic: Paste the verbatim expression in `sql-and-syntaxes.md` so a reviewer can reproduce your counts.

Field: `readmit_fail_count`
Definition: Count of readmission measures that are “worse than national” (or your equivalent category).
Source: Engineered from CMS readmission measure strings in BigQuery using `SAFE_CAST` and conditional logic.
Exact logic: Paste the verbatim expression in `sql-and-syntaxes.md` so a reviewer can reproduce your counts.

Field: `community_income`
Definition: Median community income for the ZIP code.
Source: `census_bureau_acs.zip_codes_2017_5yr`

Field: `community_population`
Definition: Community population for the ZIP code.
Source: `census_bureau_acs.zip_codes_2017_5yr`

## Analysis fields (derived in Python)

Field: `income_group`
Definition: Median split of `community_income`.
Logic: High income if income >= median; otherwise Low income.

Field: `star_group`
Definition: Binary grouping of star ratings.
Logic: 4–5 stars vs 1–3 stars.
