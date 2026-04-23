"""
STEP 4 - RISK SEGMENTATION
Project: Credit Risk & Loan Default Analysis

Segment every applicant into HIGH / MEDIUM / LOW risk using a
rule-based scorecard on three inputs:
    1. INCOME_BAND       (Low / Lower-Mid / Upper-Mid / High)
    2. NAME_INCOME_TYPE  (mapped to risk tier)
    3. AMT_CREDIT        (Small / Medium / Large / Jumbo)

Business-friendly, fully transparent, easy to explain to a credit
committee - which is exactly what AmEx / banks look for in entry-level
data analyst work.
"""

import pandas as pd

df = pd.read_csv("data/application_clean.csv")

# ------------------------------------------------------------------
# 1. Scoring dictionaries (higher = riskier)
# ------------------------------------------------------------------
income_score = {"Low": 3, "Lower-Mid": 2, "Upper-Mid": 1, "High": 0}

employment_score = {
    # High risk
    "Working":         3,
    "Maternity leave": 3,
    "Unemployed":      3,
    # Medium risk
    "Commercial associate": 2,
    "State servant":        2,
    # Low risk
    "Pensioner":   1,
    "Student":     0,
    "Businessman": 0,
}

loan_score = {"Small": 0, "Medium": 1, "Large": 2, "Jumbo": 3}

# ------------------------------------------------------------------
# 2. Compute risk score
# ------------------------------------------------------------------
df["score_income"]     = df["INCOME_BAND"].map(income_score)
df["score_employment"] = df["NAME_INCOME_TYPE"].map(employment_score).fillna(2)
df["score_loan"]       = df["LOAN_AMT_BAND"].map(loan_score)

df["risk_score"] = df["score_income"] + df["score_employment"] + df["score_loan"]

# ------------------------------------------------------------------
# 3. Bucket into segments
#    Score range 0-9. Split into 3 business tiers.
# ------------------------------------------------------------------
def bucket(s):
    if s <= 2:  return "Low"
    if s <= 5:  return "Medium"
    return "High"

df["RISK_SEGMENT"] = df["risk_score"].apply(bucket)

# ------------------------------------------------------------------
# 4. Segment-level KPIs
# ------------------------------------------------------------------
total_defaults = df["TARGET"].sum()

summary = df.groupby("RISK_SEGMENT").agg(
    applicants        = ("TARGET", "size"),
    defaulters        = ("TARGET", "sum"),
    default_rate_pct  = ("TARGET", lambda x: round(x.mean() * 100, 2)),
    avg_loan_amount   = ("AMT_CREDIT", "mean"),
    avg_income        = ("AMT_INCOME_TOTAL", "mean"),
).reset_index()

summary["pct_of_total_defaults"] = (
    summary["defaulters"] / total_defaults * 100
).round(2)

summary["pct_of_applicants"] = (
    summary["applicants"] / len(df) * 100
).round(2)

# Re-order High > Medium > Low
summary["RISK_SEGMENT"] = pd.Categorical(
    summary["RISK_SEGMENT"], ["High", "Medium", "Low"], ordered=True
)
summary = summary.sort_values("RISK_SEGMENT")

print("\n=== RISK SEGMENT SUMMARY ===")
print(summary.to_string(index=False))

# ------------------------------------------------------------------
# 5. Save for Power BI
# ------------------------------------------------------------------
df[[
    "SK_ID_CURR", "TARGET", "INCOME_BAND", "NAME_INCOME_TYPE",
    "LOAN_AMT_BAND", "AMT_CREDIT", "AMT_INCOME_TOTAL",
    "risk_score", "RISK_SEGMENT"
]].to_csv("data/applicant_segments.csv", index=False)

summary.to_csv("outputs/risk_segment_summary.csv", index=False)

print("\nSaved: data/applicant_segments.csv  (row-level for Power BI)")
print("Saved: outputs/risk_segment_summary.csv  (KPI table)")
