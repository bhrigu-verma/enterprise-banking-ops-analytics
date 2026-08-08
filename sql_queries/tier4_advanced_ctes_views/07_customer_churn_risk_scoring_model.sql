-- Tier 4 Query 07: Predictive Customer Churn Risk Scoring CTE
-- Business Context: Flags accounts exhibiting low balance, declining transactions, and open critical support tickets.

WITH ChurnSignals AS (
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        r.region_name,
        a.current_balance,
        COUNT(t.transaction_id) AS tx_count_30d,
        COUNT(st.ticket_id) AS ticket_count,
        SUM(CASE WHEN st.priority = 'Critical' THEN 1 ELSE 0 END) AS critical_tickets
    FROM customers c
    JOIN regions r ON c.region_id = r.region_id
    JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN transactions t ON a.account_id = t.account_id AND t.transaction_date >= '2025-11-01'
    LEFT JOIN support_tickets st ON c.customer_id = st.customer_id AND st.status = 'Open'
    GROUP BY c.customer_id, customer_name, r.region_name, a.current_balance
)
SELECT 
    customer_id,
    customer_name,
    region_name,
    ROUND(current_balance, 2) AS current_balance_usd,
    tx_count_30d,
    ticket_count,
    critical_tickets,
    CASE 
        WHEN current_balance < 200 AND tx_count_30d == 0 THEN 'High Churn Risk'
        WHEN critical_tickets >= 1 THEN 'Medium Churn Risk'
        ELSE 'Low Churn Risk'
    END AS churn_risk_tier
FROM ChurnSignals
WHERE current_balance < 500 OR critical_tickets >= 1
ORDER BY current_balance_usd ASC
LIMIT 50;
