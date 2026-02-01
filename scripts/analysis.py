"""
Reproducible pipeline for:
- ANOVA: star_rating by hospital_type
- Chi-square: income_group x star_group
- OLS regression: readmit_fail_count ~ community_income + community_population
- Robust SE (HC3)
- Income-only model

Inputs:
- data/healthcare_data.csv

Outputs:
- stats/*.txt and stats/correlation_matrix.csv
- docs/assets/img/*.png (plots)
"""

from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "healthcare_data.csv"
STATS_DIR = ROOT / "stats"
IMG_DIR = ROOT / "docs" / "assets" / "img"

STATS_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

def save_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")

def main() -> None:
    df = pd.read_csv(DATA_PATH)

    # ---------- ANOVA ----------
    ac = df[df["hospital_type"] == "Acute Care Hospitals"]["star_rating"].dropna()
    ca = df[df["hospital_type"] == "Critical Access Hospitals"]["star_rating"].dropna()
    f_stat, p_val = stats.f_oneway(ac, ca)

    anova_text = f"""ANOVA: star_rating by hospital_type (Acute Care vs Critical Access)

Group means:
- Acute Care Hospitals: {ac.mean():.4f}
- Critical Access Hospitals: {ca.mean():.4f}

F-statistic: {f_stat:.4f}
p-value: {p_val:.4f}
n (Acute Care): {ac.shape[0]}
n (Critical Access): {ca.shape[0]}
"""
    save_text(STATS_DIR / "anova_star_by_hospital_type.txt", anova_text)

    # Boxplot: hospital_type vs star_rating
    plt.figure()
    sns.boxplot(data=df, x="hospital_type", y="star_rating")
    plt.title("Hospital Type vs. Overall Quality Rating")
    plt.xlabel("hospital_type")
    plt.ylabel("star_rating")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "01_boxplot_hospital_type_vs_rating.png", dpi=200)
    plt.close()

    # ---------- Chi-square ----------
    income_median = df["community_income"].median()
    df["income_group"] = np.where(df["community_income"] >= income_median, "High income", "Low income")
    df["star_group"] = np.where(df["star_rating"] >= 4, "4-5 stars", "1-3 stars")

    ct = pd.crosstab(df["income_group"], df["star_group"])
    chi2, p, dof, _ = stats.chi2_contingency(ct)

    a = ct.loc["High income", "4-5 stars"]
    b = ct.loc["High income", "1-3 stars"]
    c = ct.loc["Low income", "4-5 stars"]
    d = ct.loc["Low income", "1-3 stars"]
    or_ = (a / b) / (c / d)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    ci_low = math.exp(math.log(or_) - 1.96 * se)
    ci_high = math.exp(math.log(or_) + 1.96 * se)

    chi_text = f"""Chi-square: income_group x star_group

Income median split (median income = {income_median:.0f})

Contingency table:
{ct.to_string()}

Chi-square statistic: {chi2:.4f}
Degrees of freedom: {dof}
p-value: {p:.6e}

Odds ratio (High vs Low for 4-5 stars): {or_:.4f}
95% CI: [{ci_low:.4f}, {ci_high:.4f}]
"""
    save_text(STATS_DIR / "chi_square_income_vs_star_group.txt", chi_text)

    # Scatter: income vs readmit_fail_count
    plt.figure()
    sns.regplot(
        data=df,
        x="community_income",
        y="readmit_fail_count",
        scatter_kws={"alpha": 0.25},
        line_kws={"linewidth": 2},
    )
    plt.title("How Neighborhood Income Predicts Hospital Readmission Failures")
    plt.xlabel("Median Community Income ($)")
    plt.ylabel('Count of Worse-than-Average Readmission Measures')
    plt.tight_layout()
    plt.savefig(IMG_DIR / "02_income_predicts_readmission_failures.png", dpi=200)
    plt.close()

    # ---------- Correlation matrix ----------
    corr_cols = ["star_rating", "readmit_success_count", "readmit_fail_count", "community_income", "community_population"]
    corr = df[corr_cols].corr()
    corr.to_csv(STATS_DIR / "correlation_matrix.csv", index=True)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f")
    plt.title("Executive Correlation Matrix: Health Outcomes vs. Socioeconomics")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "03_correlation_matrix.png", dpi=200)
    plt.close()

    # Scatter: income vs failures by hospital type
    plt.figure()
    sns.scatterplot(
        data=df,
        x="community_income",
        y="readmit_fail_count",
        hue="hospital_type",
        alpha=0.35
    )
    sns.regplot(
        data=df,
        x="community_income",
        y="readmit_fail_count",
        scatter=False
    )
    plt.title("Impact of Community Wealth on Clinical Readmission Failures")
    plt.xlabel("Median Community Income ($)")
    plt.ylabel('Count of "Worse Than National" Measures')
    plt.tight_layout()
    plt.savefig(IMG_DIR / "04_income_vs_failures_by_hospital_type.png", dpi=200)
    plt.close()

    # Bar: mean star rating by hospital type
    mean_star = df.groupby("hospital_type")["star_rating"].mean().sort_values(ascending=False)
    plt.figure()
    mean_star.plot(kind="barh")
    plt.title("Average Hospital Quality Rating by Ownership Type")
    plt.xlabel("Mean Star Rating (1-5 Scale)")
    plt.ylabel("Hospital Ownership Type")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "05_avg_rating_by_hospital_type.png", dpi=200)
    plt.close()

    # ---------- Regression ----------
    reg_df = df[["readmit_fail_count", "community_income", "community_population"]].dropna()
    y = reg_df["readmit_fail_count"]
    X = sm.add_constant(reg_df[["community_income", "community_population"]])
    model = sm.OLS(y, X).fit()
    save_text(STATS_DIR / "ols_readmit_fail_income_population.txt", model.summary().as_text())

    # Robust SE (HC3)
    robust = model.get_robustcov_results(cov_type="HC3")
    save_text(STATS_DIR / "ols_readmit_fail_income_population_robust_hc3.txt", robust.summary().as_text())

    # Income-only model
    X1 = sm.add_constant(reg_df[["community_income"]])
    model_income = sm.OLS(y, X1).fit()
    save_text(STATS_DIR / "ols_readmit_fail_income_only.txt", model_income.summary().as_text())

if __name__ == "__main__":
    main()
