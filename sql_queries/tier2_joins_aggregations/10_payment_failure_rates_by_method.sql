-- Tier 2 Query 10: Payment Clearing Times & Failure Rates by Payment Method
-- Business Context: Evaluates payment rail reliability and clearing latency.

SELECT 
    payment_method,
    COUNT(payment_id) AS total_payments,
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS failed,
    ROUND(100.0 * SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) / COUNT(payment_id), 2) AS failure_rate_pct,
    ROUND(AVG(clearing_time_seconds), 1) AS avg_clearing_sec
FROM payments
GROUP BY payment_method
ORDER BY failure_rate_pct DESC;
