-- Tier 1 Query 02: Customer Credit Score Band Distribution
-- Business Context: Segments customer base by FICO score risk tier (Super Prime, Prime, Near Prime, Subprime).

SELECT 
    CASE 
        WHEN credit_score >= 750 THEN '1. Super Prime (750+)'
        WHEN credit_score >= 670 THEN '2. Prime (670-749)'
        WHEN credit_score >= 580 THEN '3. Near Prime (580-669)'
        ELSE '4. Subprime (<580)'
    END AS credit_tier,
    COUNT(customer_id) AS customer_count,
    ROUND(100.0 * COUNT(customer_id) / (SELECT COUNT(*) FROM customers), 2) AS pct_of_total,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    ROUND(AVG(dti_ratio), 4) AS avg_dti_ratio
FROM customers
GROUP BY credit_tier
ORDER BY credit_tier ASC;
