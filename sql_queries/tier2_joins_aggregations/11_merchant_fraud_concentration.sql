-- Tier 2 Query 11: Merchant Fraud Concentration & Chargeback Risk
-- Business Context: Identifies high-risk merchants with anomalous fraudulent transaction rates.

SELECT 
    t.merchant_name,
    t.merchant_category,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.is_flagged_fraud) AS fraud_transactions,
    ROUND(100.0 * SUM(t.is_flagged_fraud) / COUNT(t.transaction_id), 2) AS fraud_rate_pct,
    ROUND(SUM(CASE WHEN t.is_flagged_fraud = 1 THEN t.amount ELSE 0 END), 2) AS total_fraud_dollar_volume
FROM transactions t
WHERE t.merchant_name IS NOT NULL
GROUP BY t.merchant_name, t.merchant_category
HAVING fraud_transactions >= 5
ORDER BY fraud_rate_pct DESC
LIMIT 20;
