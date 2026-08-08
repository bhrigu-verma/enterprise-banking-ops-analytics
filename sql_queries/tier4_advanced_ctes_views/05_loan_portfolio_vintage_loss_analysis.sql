-- Tier 4 Query 05: Loan Vintage Loss Analysis by Onboarding Quarter
-- Business Context: Evaluates default loss curve evolution by origination cohort.

WITH VintageCohorts AS (
    SELECT 
        STRFTIME('%Y-Q', start_date) AS origination_quarter,
        COUNT(loan_id) AS total_loans_originated,
        SUM(principal_amount) AS origination_volume,
        SUM(CASE WHEN status = 'Defaulted' THEN principal_amount ELSE 0 END) AS defaulted_volume
    FROM loans
    GROUP BY origination_quarter
)
SELECT 
    origination_quarter,
    total_loans_originated,
    ROUND(origination_volume, 2) AS origination_volume_usd,
    ROUND(defaulted_volume, 2) AS defaulted_volume_usd,
    ROUND(100.0 * defaulted_volume / origination_volume, 2) AS cumulative_loss_pct
FROM VintageCohorts
ORDER BY origination_quarter ASC;
