-- Tier 2 Query 12: Regional Operational Profitability Proxy
-- Business Context: Balances interest revenue against loan default write-offs and fraud losses.

SELECT 
    r.region_name,
    ROUND(SUM(l.principal_amount * l.interest_rate), 2) AS est_annual_interest_revenue,
    COALESCE(ROUND(SUM(CASE WHEN l.status = 'Defaulted' THEN l.principal_amount ELSE 0 END), 2), 0.00) AS defaulted_principal_loss,
    COALESCE(ROUND(SUM(fa.loss_amount), 2), 0.00) AS confirmed_fraud_loss,
    ROUND(
        SUM(l.principal_amount * l.interest_rate) - 
        COALESCE(SUM(CASE WHEN l.status = 'Defaulted' THEN l.principal_amount ELSE 0 END), 0.00) - 
        COALESCE(SUM(fa.loss_amount), 0.00), 
    2) AS net_operational_margin_usd
FROM regions r
LEFT JOIN loans l ON r.region_id = l.region_id
LEFT JOIN customers c ON r.region_id = c.region_id
LEFT JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
GROUP BY r.region_id, r.region_name
ORDER BY net_operational_margin_usd DESC;
