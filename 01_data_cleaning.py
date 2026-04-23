"""
STEP 1 - DATA LOADING & CLEANING
Project: Credit Risk & Loan Default Analysis
Dataset: Home Credit Default Risk (Kaggle) - application_train.csv

Objective:
    - Load application_train.csv
    - Inspect shape, dtypes, and nulls
    - Drop columns with > 40% missing values
    - Impute remaining nulls (median for numeric, mode for categorical)
    - Remove duplicate rows
    - Export a clean CSV for SQL + Power BI
"""

import os
import numpy as np
import pandas as pd

# ------------------------------------------------------------------
# 1. Paths
# ------------------------------------------------------------------
INPUT_PATH  = "data/application_train.csv"       # place Kaggle file here
OUTPUT_PATH = "data/application_clean.csv"       # cleaned output
os.makedirs("data", exist_ok=True)

# ------------------------------------------------------------------
# 2. Load data
# ------------------------------------------------------------------
print("Loading data ...")
df = pd.read_csv(INPUT_PATH)
print(f"Raw shape: {df.shape}")     # expected: (307511, 122)

# ------------------------------------------------------------------
# 3. Inspection
# ------------------------------------------------------------------
print("\n--- DTypes summary ---")
print(df.dtypes.value_counts())

print("\n--- Null counts (top 15) ---")
null_pct = df.isnull().mean().sort_values(ascending=False) * 100
print(null_pct.head(15).round(2))

# ------------------------------------------------------------------
# 4. Drop columns with > 40% missing values
# ------------------------------------------------------------------
cols_to_drop = null_pct[null_pct > 40].index.tolist()
print(f"\nDropping {len(cols_to_drop)} columns with >40% missing.")
df = df.drop(columns=cols_to_drop)

# ------------------------------------------------------------------
# 5. Impute remaining nulls
#    - numeric  -> median
#    - category -> mode
# ------------------------------------------------------------------
num_cols = df.select_dtypes(include=np.number).columns
cat_cols = df.select_dtypes(include="object").columns

for col in num_cols:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].median())

for col in cat_cols:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].mode()[0])

print("\nRemaining nulls after imputation:", int(df.isnull().sum().sum()))

# ------------------------------------------------------------------
# 6. Remove duplicates
# ------------------------------------------------------------------
dupes = df.duplicated().sum()
print(f"Duplicate rows: {dupes}")
df = df.drop_duplicates()

# ------------------------------------------------------------------
# 7. Feature helpers used downstream (SQL + Power BI)
# ------------------------------------------------------------------
# Income band (4 quartile bins)
df["INCOME_BAND"] = pd.qcut(
    df["AMT_INCOME_TOTAL"],
    q=4,
    labels=["Low", "Lower-Mid", "Upper-Mid", "High"]
)

# Credit term in years
df["CREDIT_TERM_YEARS"] = (df["AMT_CREDIT"] / df["AMT_ANNUITY"]).round(1)

# Loan amount band
df["LOAN_AMT_BAND"] = pd.qcut(
    df["AMT_CREDIT"],
    q=4,
    labels=["Small", "Medium", "Large", "Jumbo"]
)

# ------------------------------------------------------------------
# 8. Save cleaned file
# ------------------------------------------------------------------
df.to_csv(OUTPUT_PATH, index=False)
print(f"\nClean shape: {df.shape}")
print(f"Saved to: {OUTPUT_PATH}")
