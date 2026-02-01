[Home](./) | [Statistical tables](statistical-tables) | [Datasets](datasets) | [SQL & syntaxes](sql-and-syntaxes) | [Data dictionary](data-dictionary) | [Reproducibility](reproducibility)


# Datasets

The analytic file is stored at `data/healthcare_data.csv`.

It contains 3,182 hospitals joined to ZIP-level community context.

## Columns (final analytic schema)

```text
hospital_name
hospital_type
star_rating
readmit_success_count
readmit_fail_count
community_income
community_population
```

## Data quality notes

There is one row with a missing `readmit_success_count` and one row with a missing `readmit_fail_count`.

The regression model in this repo uses complete cases only.

## Quick profile

```text
Hospital types:
hospital_type
Acute Care Hospitals         2706
Critical Access Hospitals     476

Income:
min=13,625
median=49,514
max=250,001

Population:
min=161
median=24,202.5
max=114,129
```
