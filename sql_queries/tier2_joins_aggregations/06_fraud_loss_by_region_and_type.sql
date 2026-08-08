-- Tier 2 Query 06: Fraud Loss Concentration by Region and Fraud Type
-- Business Context: Guides cybersecurity and fraud prevention budget allocation.

SELECT 
    r.region_name,
    fa.fraud_type,
    COUNT(fa.alert_id) AS confirmed_alerts,
    ROUND(SUM(fa.loss_amount), 2) AS total_loss_usd,
    ROUND(AVG(fa.risk_score), 1) AS avg_risk_score
FROM fraud_alerts fa
JOIN accounts a ON fa.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN regions r ON c.region_id = r.region_id
WHERE fa.status = 'Confirmed Fraud'
GROUP BY r.region_name, fa.fraud_type
ORDER BY total_loss_usd DESC;
