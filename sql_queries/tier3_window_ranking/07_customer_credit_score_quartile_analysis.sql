-- Tier 3 Query 07: Customer Credit Score Quartile & Loan Default Risk Segmenting
-- Business Context: Segments portfolio into credit score quartiles to measure risk escalation.

WITH CustomerQuartiles AS (
    SELECT 
        customer_id,
        credit_score,
        NTILE(4) OVER (ORDER BY credit_score ASC) AS credit_quartile
    FROM customers
)
SELECT 
    cq.credit_quartile,
    MIN(cq.credit_score) AS min_credit_score,
    MAX(cq.credit_score) AS max_credit_score,
    COUNT(DISTINCT cq.customer_id) AS customer_count,
    COUNT(l.loan_id) AS loans_issued,
    SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) / COUNT(l.loan_id), 2) AS default_rate_pct
FROM CustomerQuartiles cq
LEFT JOIN loans l ON cq.customer_id = l.customer_id
GROUP BY cq.credit_quartile
ORDER BY cq.credit_quartile ASC;
