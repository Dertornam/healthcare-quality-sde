---
title: Executive Summary — Socio-Economic Determinants of Healthcare Quality
layout: default
---

# Executive Summary — Socio-Economic Determinants of Healthcare Quality

I built this project to answer a practical leadership question: when a hospital has weak CMS star ratings and elevated readmission failures, am I looking at an internal operational failure, or am I seeing performance shaped by the socio-economic context of the community the hospital serves?

I used Google BigQuery Public Datasets to create a unified analytic file that connects hospital performance to ZIP-level community context. I joined `bigquery-public-data.cms_medicare.hospital_general_info` with `bigquery-public-data.census_bureau_acs.zip_codes_2017_5yr` on ZIP code. I engineered numeric fields using `SAFE_CAST` so I could run ANOVA, chi-square, and regression in Python without type issues. My final analytic file contains 3,182 hospitals joined to ZIP-level context. It includes 2,706 Acute Care hospitals and 476 Critical Access hospitals.

## What I found and why it matters

My results tell a coherent story. Hospital type is not where quality differences concentrate, but community context is where quality access and risk are most clearly stratified.

First, I do not see evidence that hospital type creates a meaningful quality gap. My ANOVA result (F = 0.11, p = 0.7376) indicates no statistically significant difference in star ratings between “Acute Care” and “Critical Access” hospitals in this dataset. I interpret this as operational consistency across these designations. In other words, the label does not look like the limiting factor.

Second, I do see a strong wealth-quality gap that is not subtle. My chi-square test shows a highly significant association between income groups and rating groups (p = 0.0000). High-income communities are disproportionately served by 4–5 star hospitals (825 facilities). Low-income communities are served by nearly double the number of 1–3 star hospitals (1,040). I also translate that pattern into an effect-size statement that executives can use immediately: high-income communities have about 2.04× higher odds of being served by a 4–5 star hospital compared to low-income communities (95% CI: 1.77 to 2.35). To me, this is the “access to quality” story. It is not only about what hospitals do. It is also about where hospitals are, and which communities get concentrated access to higher-rated facilities.

Third, when I model readmission failures directly, population burden becomes the dominant driver once I include both income and population. In my multiple regression, the model fit is modest (R² = 0.044), which tells me many other factors also matter. Still, the direction and significance are clear in this two-variable view. Income is not statistically significant when modeled alongside population (Income coef = 8.764e-07, p = 0.341). Population is strongly significant (Population coef = 1.381e-05, p < 0.001). I interpret this as density and volume pressure being the stronger driver of readmission failure counts than income once I account for both together.

The correlation structure aligns with that story. The correlation matrix shows a moderate negative correlation (-0.34) between star ratings and readmission failures. That confirms that readmission performance is a meaningful component of how “reputation” (the star rating) shows up in the data.

## What I would tell an executive team in one minute

If I am making the “so what” plain, I would say this: I do not see hospital designation as the constraint. I see quality access stratified by community income, and I see readmission failure pressure rising with population burden. That combination points toward a system problem, not only a hospital problem.

## What I recommend based on the evidence

I recommend risk-adjusted benchmarking. I do not think it is defensible to treat raw performance metrics as fully comparable across radically different community contexts. I would advocate that benchmarks be adjusted for social determinants and density context, so hospitals serving high-density, low-income areas are not structurally penalized for risk they do not control.

I recommend targeted resource allocation toward Transition of Care programs in the specific “high risk” profile that emerges from the joint view. In my interpretation, the highest pressure point is the combination of low income and high population. That is where readmission failures are most consistently elevated. I would prioritize discharge planning support, community social work linkage, and post-discharge outreach in those service areas before I would prioritize marginal inpatient equipment upgrades.

I recommend policy identification of “healthcare deserts” defined as overlap zones where low income and low star ratings co-occur. I would use this joined dataset logic to direct grants and capacity-building investments toward those zones, because the pattern is geographically and economically stratified rather than randomly distributed.

## Notes I keep in mind when I interpret the model

Readmission failures are counts with many zeros, so I expect non-constant variance in residuals in a linear regression. I use the model primarily for directionality. I confirm inference with robust standard errors. When I apply robust standard errors, the population coefficient remains strongly significant, while the income coefficient remains non-significant. I also note a nuance that matters for interpretation: income is statistically significant when modeled alone, but it explains almost none of the variation by itself (R² ≈ 0.003). That helps me explain why an income-versus-failures scatter line may slope upward slightly even when population is the real driver in the combined model.

## Bottom line

I built this project to separate “medical failure” from “context pressure.” My results push me toward the context story. The strongest signals are economic stratification in access to higher-rated hospitals and population burden as the dominant predictor of readmission failure counts in this ZIP-level joined view.
