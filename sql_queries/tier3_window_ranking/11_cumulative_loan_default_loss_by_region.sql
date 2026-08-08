-- Tier 3 Query 11: Cumulative Regional Loan Default Losses Over Time
-- Business Context: Tracks cumulative default loss capital burn across quarters.

WITH MonthlyDefaults AS (
    SELECT 
        r.region_name,
        STRFTIME('%Y-%m', l.start_date) AS loan_month,
        SUM(l.principal_amount) AS monthly_default_loss
    FROM loans l
    JOIN regions r ON l.region_id = r.region_id
    WHERE l.status = 'Defaulted'
    GROUP BY r.region_name, loan_month
)
SELECT 
    region_name,
    loan_month,
    ROUND(monthly_default_loss, 2) AS monthly_loss_usd,
    ROUND(SUM(monthly_default_loss) OVER (PARTITION BY region_name ORDER BY loan_month ASC), 2) AS cumulative_loss_usd
FROM MonthlyDefaults
ORDER BY region_name, loan_month ASC;
