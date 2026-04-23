# STEP 5 — Business Recommendations

Every recommendation is anchored to a number produced in Steps 2–4.
Format for each: **Finding → Business Impact → Recommendation**.

---

## Recommendation 1 — Tighten underwriting for the High-Risk segment

**Finding.** The High-Risk segment (Low income + Working/Maternity/Unemployed + Large/Jumbo loan) is **~18% of applicants** but contributes **~26% of all defaults** at a **~11.8% default rate** — roughly **3× the Low-Risk segment** (~3.5%).

**Business Impact.** On a book of 300K applicants and an average loan of ~600K, every 1-pt reduction in this segment's default rate avoids roughly **$40M–$55M in expected annual losses**.

**Recommendation.** Introduce an additional underwriting gate for this segment:
1. Require at least one EXT_SOURCE score ≥ 0.5 (since EXT_SOURCE_1/2/3 account for **~80% of model weight** — Step 3 finding).
2. Cap loan-to-income at 3.0× for applicants in the Low income band.
3. Route any Jumbo loan in this segment to manual review.

---

## Recommendation 2 — Reprice, don't reject, the Medium-Risk segment

**Finding.** The Medium-Risk segment holds **~63% of applicants** and produces **~66% of defaults** at **~8.5%** — only marginally worse than the book-wide rate of **8.1%**.

**Business Impact.** Outright rejection would shrink originations by two-thirds. Differential pricing can preserve volume while covering expected loss.

**Recommendation.** Add a **+150–250 bps risk premium** on interest rate for Medium-Risk applicants whose loan term exceeds 10 years (Step 2 Q5 showed 10-20y and 20y+ jumbo cohorts default at 2–3× the <5y cohort). This converts the segment from marginally break-even to reliably profitable without cutting approval volume.

---

## Recommendation 3 — Grow the Low-Risk segment through targeted acquisition

**Finding.** The Low-Risk segment (High/Upper-Mid income + Pensioner/Businessman/Student/State-servant + Small/Medium loans) has a **~3.5% default rate**, less than half the portfolio average of **8.1%**, but represents only **~19% of applicants**.

**Business Impact.** Doubling this segment's share from 19% → 30% would pull the overall portfolio default rate from 8.1% down to **~7.0%**, meaningfully improving capital adequacy ratios and freeing reserves for growth.

**Recommendation.** Launch a pre-approved offer campaign to `Pensioner` and `State servant` applicants with `AMT_INCOME_TOTAL` above the 75th percentile, with loan amounts capped at the "Medium" band. Market through existing payroll / pension-disbursement relationships and price 50 bps below standard rate to win the relationship.
