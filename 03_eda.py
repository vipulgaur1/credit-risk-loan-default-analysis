"""
STEP 3 - EXPLORATORY DATA ANALYSIS (EDA)
Project: Credit Risk & Loan Default Analysis

Produces:
    1. Distribution of TARGET (default vs non-default)
    2. Correlation heatmap of top 15 numerical features vs TARGET
    3. Default rate by income bracket - bar chart
    4. Default rate by employment type - bar chart
    5. Loan amount vs default rate - scatter
    6. Top 3 features driving default risk (printed to console)

All charts are saved to outputs/ as PNG for the Power BI & README.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/application_clean.csv")

# ------------------------------------------------------------------
# 1. Distribution of TARGET
# ------------------------------------------------------------------
plt.figure(figsize=(6, 4))
counts = df["TARGET"].value_counts().sort_index()
ax = sns.barplot(x=counts.index, y=counts.values, hue=counts.index,
                 palette=["#2E86AB", "#E63946"], legend=False)
for i, v in enumerate(counts.values):
    ax.text(i, v + 2000, f"{v:,}\n({v/len(df)*100:.1f}%)",
            ha="center", fontsize=10)
plt.xticks([0, 1], ["Non-Default (0)", "Default (1)"])
plt.title("Distribution of TARGET")
plt.ylabel("Applicants")
plt.tight_layout()
plt.savefig("outputs/01_target_distribution.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 2. Correlation heatmap - top 15 features (by |corr| with TARGET)
# ------------------------------------------------------------------
num = df.select_dtypes(include=np.number)
corr_target = num.corr()["TARGET"].drop("TARGET").abs().sort_values(ascending=False)
top15 = corr_target.head(15).index.tolist()

plt.figure(figsize=(10, 8))
sns.heatmap(num[top15 + ["TARGET"]].corr(),
            annot=True, fmt=".2f", cmap="coolwarm", center=0,
            cbar_kws={"shrink": 0.8})
plt.title("Correlation Heatmap - Top 15 Features vs TARGET")
plt.tight_layout()
plt.savefig("outputs/02_correlation_heatmap.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 3. Default rate by income bracket
# ------------------------------------------------------------------
order = ["Low", "Lower-Mid", "Upper-Mid", "High"]
dr_income = (df.groupby("INCOME_BAND")["TARGET"].mean() * 100).reindex(order)

plt.figure(figsize=(7, 4))
ax = sns.barplot(x=dr_income.index, y=dr_income.values,
                 hue=dr_income.index, palette="Reds_r", legend=False)
for i, v in enumerate(dr_income.values):
    ax.text(i, v + 0.1, f"{v:.2f}%", ha="center")
plt.title("Default Rate by Income Bracket")
plt.ylabel("Default rate (%)")
plt.xlabel("Income band")
plt.tight_layout()
plt.savefig("outputs/03_default_by_income.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 4. Default rate by employment type
# ------------------------------------------------------------------
dr_emp = (df.groupby("NAME_INCOME_TYPE")["TARGET"].mean() * 100) \
           .sort_values(ascending=False)

plt.figure(figsize=(8, 4))
ax = sns.barplot(x=dr_emp.values, y=dr_emp.index,
                 hue=dr_emp.index, palette="Reds_r", legend=False)
for i, v in enumerate(dr_emp.values):
    ax.text(v + 0.1, i, f"{v:.2f}%", va="center")
plt.title("Default Rate by Employment Type")
plt.xlabel("Default rate (%)")
plt.tight_layout()
plt.savefig("outputs/04_default_by_employment.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 5. Loan amount vs default rate (scatter with binned mean)
# ------------------------------------------------------------------
df["LOAN_BIN"] = pd.cut(df["AMT_CREDIT"], bins=25)
scatter = df.groupby("LOAN_BIN").agg(
    avg_loan=("AMT_CREDIT", "mean"),
    default_rate=("TARGET", "mean"),
    n=("TARGET", "size")
).reset_index()
scatter["default_rate"] *= 100

plt.figure(figsize=(8, 5))
sns.scatterplot(data=scatter, x="avg_loan", y="default_rate",
                size="n", sizes=(30, 350), legend=False, color="#E63946")
plt.title("Loan Amount vs Default Rate")
plt.xlabel("Average AMT_CREDIT (binned)")
plt.ylabel("Default rate (%)")
plt.tight_layout()
plt.savefig("outputs/05_loan_vs_default.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 6. Which 3 features drive most of default risk?
#    Simple proxy: train a logistic regression on top-20 numeric
#    features and rank by absolute standardized coefficient.
# ------------------------------------------------------------------
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

top20 = corr_target.head(20).index.tolist()
X = df[top20].copy()
y = df["TARGET"]

X_scaled = StandardScaler().fit_transform(X)
lr = LogisticRegression(max_iter=1000, class_weight="balanced")
lr.fit(X_scaled, y)

importance = pd.Series(np.abs(lr.coef_[0]), index=top20) \
               .sort_values(ascending=False)
top3 = importance.head(3)
pct_of_total = top3.sum() / importance.sum() * 100

print("\n==== KEY DRIVERS OF DEFAULT RISK ====")
print(importance.head(10).round(3))
print(f"\nTop-3 features explain {pct_of_total:.1f}% of total model weight:")
for f, w in top3.items():
    print(f"  - {f:30s}  weight={w:.3f}")

importance.to_csv("outputs/feature_importance.csv")
print("\nAll EDA charts saved to outputs/")
