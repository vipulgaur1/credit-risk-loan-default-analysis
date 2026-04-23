/*==================================================================
STEP 2 - SQL ANALYSIS
Project : Credit Risk & Loan Default Analysis
Table   : application_clean  (exported from Step 1)
Dialect : Standard SQL (tested in SQLite / PostgreSQL / MySQL 8+)

Load instructions (SQLite example):
    sqlite3 credit.db
    .mode csv
    .import data/application_clean.csv application_clean
==================================================================*/


/*------------------------------------------------------------------
Q1. DEFAULT RATE BY INCOME BRACKET
    AMT_INCOME_TOTAL is binned into 4 quartile bands: Low, Lower-Mid,
    Upper-Mid, High  (already created in Step 1 as INCOME_BAND).
------------------------------------------------------------------*/
SELECT  INCOME_BAND,
        COUNT(*)                                       AS total_applicants,
        SUM(TARGET)                                    AS defaulters,
        ROUND(100.0 * SUM(TARGET) / COUNT(*), 2)       AS default_rate_pct
FROM    application_clean
GROUP BY INCOME_BAND
ORDER BY default_rate_pct DESC;


/*------------------------------------------------------------------
Q2. DEFAULT RATE BY EMPLOYMENT TYPE (NAME_INCOME_TYPE)
------------------------------------------------------------------*/
SELECT  NAME_INCOME_TYPE,
        COUNT(*)                                       AS total_applicants,
        SUM(TARGET)                                    AS defaulters,
        ROUND(100.0 * SUM(TARGET) / COUNT(*), 2)       AS default_rate_pct
FROM    application_clean
GROUP BY NAME_INCOME_TYPE
ORDER BY default_rate_pct DESC;


/*------------------------------------------------------------------
Q3. TOP 10 LOAN PURPOSES WITH HIGHEST DEFAULT RATE
    (uses NAME_CASH_LOAN_PURPOSE if available, else NAME_CONTRACT_TYPE)
    Filter to groups with >= 500 applicants to avoid noise.
------------------------------------------------------------------*/
SELECT  NAME_CONTRACT_TYPE                              AS loan_purpose,
        COUNT(*)                                        AS total_applicants,
        SUM(TARGET)                                     AS defaulters,
        ROUND(100.0 * SUM(TARGET) / COUNT(*), 2)        AS default_rate_pct
FROM    application_clean
GROUP BY NAME_CONTRACT_TYPE
HAVING  COUNT(*) >= 500
ORDER BY default_rate_pct DESC
LIMIT 10;


/*------------------------------------------------------------------
Q4. WINDOW FUNCTION
    Rank income brackets by default rate WITHIN each employment type.
------------------------------------------------------------------*/
WITH agg AS (
    SELECT  NAME_INCOME_TYPE,
            INCOME_BAND,
            COUNT(*)                                    AS total_applicants,
            SUM(TARGET)                                 AS defaulters,
            ROUND(100.0 * SUM(TARGET)/COUNT(*), 2)      AS default_rate_pct
    FROM    application_clean
    GROUP BY NAME_INCOME_TYPE, INCOME_BAND
)
SELECT  NAME_INCOME_TYPE,
        INCOME_BAND,
        total_applicants,
        defaulters,
        default_rate_pct,
        RANK() OVER (
            PARTITION BY NAME_INCOME_TYPE
            ORDER BY default_rate_pct DESC
        ) AS risk_rank_within_employment
FROM    agg
ORDER BY NAME_INCOME_TYPE, risk_rank_within_employment;


/*------------------------------------------------------------------
Q5. COHORT: DEFAULT RATE BY LOAN AMOUNT BAND x CREDIT TERM
    CREDIT_TERM_YEARS is bucketed: <5y, 5-10y, 10-20y, 20y+
------------------------------------------------------------------*/
WITH cohort AS (
    SELECT
        LOAN_AMT_BAND,
        CASE
            WHEN CREDIT_TERM_YEARS < 5                 THEN '<5y'
            WHEN CREDIT_TERM_YEARS BETWEEN 5  AND 10   THEN '5-10y'
            WHEN CREDIT_TERM_YEARS BETWEEN 10 AND 20   THEN '10-20y'
            ELSE '20y+'
        END AS term_bucket,
        TARGET
    FROM application_clean
)
SELECT  LOAN_AMT_BAND,
        term_bucket,
        COUNT(*)                                       AS total_applicants,
        SUM(TARGET)                                    AS defaulters,
        ROUND(100.0 * SUM(TARGET)/COUNT(*), 2)         AS default_rate_pct
FROM    cohort
GROUP BY LOAN_AMT_BAND, term_bucket
ORDER BY LOAN_AMT_BAND, term_bucket;
