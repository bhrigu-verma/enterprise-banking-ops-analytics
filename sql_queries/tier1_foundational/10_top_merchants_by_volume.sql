-- Tier 1 Query 10: Top 15 Merchant Outlets by Purchase Volume
-- Business Context: Identifies core merchant partners and spending concentration.

SELECT 
    merchant_name,
    merchant_category,
    COUNT(transaction_id) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_spend_usd,
    ROUND(AVG(amount), 2) AS avg_ticket_size
FROM transactions
WHERE merchant_name IS NOT NULL
GROUP BY merchant_name, merchant_category
ORDER BY total_spend_usd DESC
LIMIT 15;
