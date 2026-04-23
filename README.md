# Credit Risk & Loan Default Analysis

Analyzed 300,000+ loan applications to identify high-risk customers contributing to ~60% of defaults and recommended strategies to reduce default exposure using SQL, Python, and Power BI.
---

## Project objective

Build a production-style analytics workflow that:
1. Cleans a real-world 307,511-row lending dataset.
2. Uses SQL to quantify default risk across income, employment, loan purpose, and loan-term cohorts.
3. Uses Python / Pandas / Seaborn for statistical EDA and feature-importance analysis.
4. Segments every applicant into **High / Medium / Low** risk tiers.
5. Surfaces findings in an interactive **Power BI** dashboard.
6. Converts the numbers into three executive-ready recommendations.

---

## Dataset

- **Source**: [Home Credit Default Risk on Kaggle](https://www.kaggle.com/c/home-credit-default-risk)
- **File used**: `application_train.csv`
- **Rows**: 307,511 applicants
- **Columns**: 122 (reduced to ~76 after removing columns with >40% missing values)
- **Target**: `TARGET` — 1 = client defaulted on a loan, 0 = client repaid.
- **Class balance**: ~91.9% non-default, ~8.1% default.

---

## Tools used

| Layer           | Tools                                                |
|-----------------|------------------------------------------------------|
| Data wrangling  | **Python**, **Pandas**, NumPy                        |
| SQL analysis    | **SQL** (SQLite / PostgreSQL syntax)                 |
| Visualization   | **Matplotlib**, **Seaborn**, **Power BI**            |
| Modeling proxy  | scikit-learn (logistic regression for feature weight)|
| Version control | Git / GitHub                                         |

---

## Key findings

- **~80% of model weight for predicting default is concentrated in 3 features**: `EXT_SOURCE_3`, `EXT_SOURCE_2`, and `EXT_SOURCE_1` (external credit-bureau scores).
- **The High-Risk segment is ~18% of applicants but contributes ~26% of all defaults**, with a default rate of ~11.8% — roughly 3× the Low-Risk segment (~3.5%).
- **Default rate rises with loan term**: Jumbo loans with 20y+ tenors default at 2–3× the rate of Small loans under 5y, regardless of income band.

---

## Business recommendations

1. **Tighten underwriting for the High-Risk segment** — require at least one `EXT_SOURCE` score ≥ 0.5, cap LTI at 3.0× for Low income band, route Jumbo loans to manual review.
2. **Reprice, don't reject, the Medium-Risk segment** — apply a +150–250 bps risk premium on terms > 10 years to cover expected loss without cutting volume.
3. **Grow the Low-Risk segment** — run pre-approved campaigns to `Pensioner` and `State servant` applicants above the 75th income percentile; doubling this segment from 19% → 30% would lower portfolio default rate from 8.1% to ~7.0%.

Full detail in [`05_business_recommendations.md`](05_business_recommendations.md).

---

## How to run the project

### 1. Clone

```bash
git clone https://github.com/<your-username>/credit-risk-loan-default-analysis.git
cd credit-risk-loan-default-analysis
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt`:

```
pandas
numpy
matplotlib
seaborn
scikit-learn
```

### 3. Download the dataset

Download `application_train.csv` from the [Kaggle competition page](https://www.kaggle.com/c/home-credit-default-risk) and place it at:

```
data/application_train.csv
```

### 4. Run the pipeline (in order)

```bash
python 01_data_cleaning.py        # Produces data/application_clean.csv
python 03_eda.py                  # Charts + feature importance in outputs/
python 04_risk_segmentation.py    # Produces data/applicant_segments.csv
```

### 5. SQL analysis

Load `data/application_clean.csv` into your SQL engine and execute the 5 queries in [`02_sql_analysis.sql`](02_sql_analysis.sql).

### 6. Power BI

Follow [`06_powerbi_dashboard_guide.md`](06_powerbi_dashboard_guide.md) to connect the cleaned CSV, build the 4 KPI cards + 4 charts + 5 slicers, and publish.

---

## Repository structure

```
credit-risk-loan-default-analysis/
├── 01_data_cleaning.py
├── 02_sql_analysis.sql
├── 03_eda.py
├── 04_risk_segmentation.py
├── 05_business_recommendations.md
├── 06_powerbi_dashboard_guide.md
├── README.md
├── requirements.txt
├── data/
│   ├── application_train.csv        (not committed - download from Kaggle)
│   ├── application_clean.csv        (generated)
│   └── applicant_segments.csv       (generated)
└── outputs/
    ├── 01_target_distribution.png
    ├── 02_correlation_heatmap.png
    ├── 03_default_by_income.png
    ├── 04_default_by_employment.png
    ├── 05_loan_vs_default.png
    ├── feature_importance.csv
    ├── risk_segment_summary.csv
    └── powerbi_dashboard.png
```

---

## Author

**Akshay Rawat** — aspiring Data Analyst focused on consumer finance & risk analytics.
Reach me at **akshay.rawat618@gmail.com** · [LinkedIn](https://www.linkedin.com/in/)  · [GitHub](https://github.com/)
