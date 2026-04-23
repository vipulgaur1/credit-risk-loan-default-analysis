# STEP 6 — Power BI Dashboard Layout

A single page, 16:9 landscape, titled **"Credit Risk & Loan Default Analysis — Portfolio View"**.

---

## 1. Connect the cleaned CSV to Power BI

1. Open **Power BI Desktop**.
2. **Home → Get Data → Text/CSV**, then pick `data/application_clean.csv`.
3. In the preview pane click **Transform Data** to open Power Query.
4. In Power Query:
   - Promote first row as headers (usually automatic).
   - Set `TARGET`, `AMT_INCOME_TOTAL`, `AMT_CREDIT`, `AMT_ANNUITY`, `DAYS_BIRTH` → *Whole Number / Decimal*.
   - Set `INCOME_BAND`, `NAME_INCOME_TYPE`, `LOAN_AMT_BAND`, `NAME_CONTRACT_TYPE` → *Text*.
   - Click **Close & Apply**.
5. Repeat for `data/applicant_segments.csv` (from Step 4) and create a **relationship** on `SK_ID_CURR` (Many-to-One, single direction from segments → application).
6. Create a measures table: **Home → Enter Data → "Measures"**.

---

## 2. DAX Measures (paste these into the Measures table)

```DAX
Total Applicants   = COUNTROWS(application_clean)
Total Defaulters   = CALCULATE([Total Applicants], application_clean[TARGET] = 1)
Default Rate %     = DIVIDE([Total Defaulters], [Total Applicants], 0) * 100
Avg Loan Amount    = AVERAGE(application_clean[AMT_CREDIT])
Avg Income         = AVERAGE(application_clean[AMT_INCOME_TOTAL])
High Risk Share %  =
    DIVIDE(
        CALCULATE([Total Applicants], applicant_segments[RISK_SEGMENT] = "High"),
        [Total Applicants], 0
    ) * 100
```

---

## 3. The 4 KPI cards (top row)

| # | Card title              | Measure              | Format      |
|---|-------------------------|----------------------|-------------|
| 1 | **Total Applicants**    | `[Total Applicants]` | 307,511     |
| 2 | **Overall Default Rate**| `[Default Rate %]`   | 8.07 %      |
| 3 | **Avg Loan Amount**     | `[Avg Loan Amount]`  | ₹599,026    |
| 4 | **High-Risk Share**     | `[High Risk Share %]`| 18.2 %      |

Use the **Card** visual, set font = Segoe UI 26pt bold, background = white, subtle border.

---

## 4. The 4 charts (body of the page)

| Row / Position | Chart type             | X axis / Category          | Value / Measure       | Color logic                        |
|----------------|------------------------|----------------------------|------------------------|------------------------------------|
| **Chart A** – top-left (below KPIs) | **Clustered bar chart**  | `INCOME_BAND` (Low → High)  | `Default Rate %`       | Red gradient (high = dark red) |
| **Chart B** – top-right             | **Horizontal bar chart** | `NAME_INCOME_TYPE` (sorted) | `Default Rate %`       | Red gradient |
| **Chart C** – bottom-left           | **Scatter plot**         | X = `AMT_CREDIT` (binned), Y = `Default Rate %`, Size = `Total Applicants` | Single accent color |
| **Chart D** – bottom-right          | **Matrix (heatmap)**     | Rows = `LOAN_AMT_BAND`, Cols = Credit Term Bucket (<5y / 5-10y / 10-20y / 20y+), Values = `Default Rate %` | Conditional formatting red scale |

Layout sketch:

```
+-----------------------------------------------------------+
|  KPI 1      KPI 2      KPI 3      KPI 4                   |
+-----------------------------+-----------------------------+
|   Chart A                   |   Chart B                   |
|  Default Rate by Income     |  Default Rate by Employment |
+-----------------------------+-----------------------------+
|   Chart C                   |   Chart D                   |
|  Loan Amount vs Default     |  Loan Band x Credit Term    |
+-----------------------------+-----------------------------+
```

---

## 5. Slicers / filters (left-hand filter pane)

1. **Gender** — `CODE_GENDER` (buttons: M / F).
2. **Employment Type** — `NAME_INCOME_TYPE` (drop-down, multi-select).
3. **Risk Segment** — `RISK_SEGMENT` from `applicant_segments` (High / Medium / Low tiles).
4. **Loan Amount Band** — `LOAN_AMT_BAND` (horizontal chiclet slicer).
5. **Contract Type** — `NAME_CONTRACT_TYPE` (Cash / Revolving toggle).

Pin slicers at the top of the left pane so every visual responds to them.

---

## 6. Styling & polish

- Theme: **File → Themes → "Executive"** (or import a corporate-style JSON).
- Page background: `#F7F7FA`; visual backgrounds: white.
- Title bar: single text box — **"Credit Risk & Loan Default Analysis"** with subtitle **"Home Credit Portfolio — 307,511 applicants"**.
- Add a footer text box: **"Source: Kaggle Home Credit Default Risk | Built by Akshay Rawat"**.
- Export a screenshot (`File → Export → PNG`) and save as `outputs/powerbi_dashboard.png` for the README.

---

## 7. Publish

1. Sign in: **Home → Sign in** with a Microsoft account.
2. **Publish → My workspace**.
3. Copy the public link and add it to the README (Step 7).
