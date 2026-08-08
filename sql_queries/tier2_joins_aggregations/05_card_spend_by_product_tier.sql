-- Tier 2 Query 05: Card Product Spend & Fee Revenue Correlation
-- Business Context: Analyzes transaction throughput and annual fee yield across card tiers.

SELECT 
    p.product_name,
    p.subcategory AS card_tier,
    p.annual_fee,
    COUNT(DISTINCT c.card_id) AS cards_issued,
    COUNT(t.transaction_id) AS total_transactions,
    ROUND(SUM(t.amount), 2) AS total_spend_usd,
    ROUND(AVG(t.amount), 2) AS avg_spend_per_tx
FROM products p
JOIN cards c ON p.product_id = c.product_id
JOIN transactions t ON c.card_id = t.card_id
GROUP BY p.product_name, p.subcategory, p.annual_fee
ORDER BY total_spend_usd DESC;
