-- Tier 1 Query 08: Monthly Transaction Volume & Dollar Value
-- Business Context: Evaluates payment network throughput and monthly seasonality.

SELECT 
    STRFTIME('%Y-%m', transaction_date) AS tx_month,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_volume_usd,
    ROUND(AVG(amount), 2) AS avg_transaction_size,
    SUM(is_flagged_fraud) AS flagged_fraud_count
FROM transactions
GROUP BY tx_month
ORDER BY tx_month ASC;
