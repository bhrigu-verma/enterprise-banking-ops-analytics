-- Tier 1 Query 07: Fraud Alert Status & Loss Summary
-- Business Context: Measures risk mitigation efficacy and total confirmed financial fraud losses.

SELECT 
    fraud_type,
    status,
    COUNT(alert_id) AS alert_count,
    ROUND(SUM(loss_amount), 2) AS total_loss_usd,
    ROUND(AVG(loss_amount), 2) AS avg_loss_usd,
    ROUND(AVG(risk_score), 1) AS avg_risk_score
FROM fraud_alerts
GROUP BY fraud_type, status
ORDER BY total_loss_usd DESC;
