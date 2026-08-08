-- Tier 3 Query 09: Delinquent Payment Progression Tracking (LAG / LEAD)
-- Business Context: Monitors payment degradation sequence (On-Time -> Late 30 -> Late 60 -> Default).

SELECT 
    loan_id,
    loan_payment_id,
    payment_date,
    payment_status,
    days_overdue,
    LAG(payment_status, 1) OVER (PARTITION BY loan_id ORDER BY payment_date) AS prior_payment_status,
    LEAD(payment_status, 1) OVER (PARTITION BY loan_id ORDER BY payment_date) AS next_payment_status
FROM loan_payments
WHERE loan_id IN (SELECT DISTINCT loan_id FROM loan_payments WHERE payment_status != 'On-Time')
ORDER BY loan_id, payment_date ASC
LIMIT 100;
