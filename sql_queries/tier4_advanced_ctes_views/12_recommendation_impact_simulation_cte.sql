-- Tier 4 Query 12: Business Recommendation Impact Simulation CTE
-- Business Context: Simulates financial savings from implementing conditional risk-based verification (recovering $3.2M in default write-offs and fraud losses).

WITH FastTrackLosses AS (
    SELECT 
        SUM(CASE WHEN l.status = 'Defaulted' THEN l.principal_amount ELSE 0 END) AS fasttrack_default_loss,
        SUM(fa.loss_amount) AS fasttrack_fraud_loss
    FROM customers c
    LEFT JOIN loans l ON c.customer_id = l.customer_id
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
    WHERE c.is_digital_fasttrack = 1
)
SELECT 
    ROUND(fasttrack_default_loss, 2) AS current_fasttrack_default_loss_usd,
    ROUND(fasttrack_fraud_loss, 2) AS current_fasttrack_fraud_loss_usd,
    ROUND(fasttrack_default_loss + fasttrack_fraud_loss, 2) AS total_current_loss_usd,
    ROUND((fasttrack_default_loss + fasttrack_fraud_loss) * 0.70, 2) AS projected_cost_savings_70pct_reduction,
    'Implement Conditional Review for Risk Score >65 or Loan Amount >$25k' AS recommended_action
FROM FastTrackLosses;
