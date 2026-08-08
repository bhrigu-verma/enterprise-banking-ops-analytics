-- Tier 1 Query 09: Average Interest Rates & Risk Scores by Product
-- Business Context: Ensures loan pricing aligns with risk models across lending categories.

SELECT 
    p.product_name,
    p.category,
    COUNT(l.loan_id) AS count_issued,
    ROUND(AVG(l.interest_rate) * 100, 2) AS avg_rate_pct,
    ROUND(AVG(l.initial_risk_score), 1) AS avg_risk_score,
    ROUND(AVG(l.approval_turnaround_days), 2) AS avg_turnaround_days
FROM products p
JOIN loans l ON p.product_id = l.product_id
GROUP BY p.product_name, p.category
ORDER BY count_issued DESC;
