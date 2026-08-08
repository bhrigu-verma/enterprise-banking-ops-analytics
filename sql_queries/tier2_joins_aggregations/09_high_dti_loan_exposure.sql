-- Tier 2 Query 09: High Debt-to-Income (>40%) Loan Portfolio Exposure
-- Business Context: Audits high-risk lending exposure to ensure capital adequacy compliance.

SELECT 
    r.region_name,
    COUNT(l.loan_id) AS high_dti_loans,
    ROUND(SUM(l.principal_amount), 2) AS total_exposure_usd,
    ROUND(AVG(c.dti_ratio), 4) AS avg_dti,
    ROUND(AVG(c.credit_score), 1) AS avg_credit_score,
    SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaults
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
JOIN regions r ON l.region_id = r.region_id
WHERE c.dti_ratio > 0.40
GROUP BY r.region_name
ORDER BY total_exposure_usd DESC;
