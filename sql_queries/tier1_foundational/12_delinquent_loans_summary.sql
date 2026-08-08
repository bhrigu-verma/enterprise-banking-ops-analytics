-- Tier 1 Query 12: Delinquent Loan Payment Overview
-- Business Context: Tracks late payment severity across 30, 60, and 90+ day delinquency buckets.

SELECT 
    payment_status,
    COUNT(loan_payment_id) AS payment_records,
    ROUND(SUM(amount_paid), 2) AS total_amount,
    ROUND(AVG(days_overdue), 1) AS avg_days_overdue,
    MAX(days_overdue) AS max_days_overdue
FROM loan_payments
WHERE payment_status != 'On-Time'
GROUP BY payment_status
ORDER BY avg_days_overdue DESC;
