-- Tier 4 Query 04: Customer Channel Touchpoint Attribution & Cross-Sell Rate
-- Business Context: Maps customer acquisition channel to multi-product adoption.

WITH CustomerProducts AS (
    SELECT 
        c.customer_id,
        c.onboarding_channel,
        COUNT(DISTINCT a.account_id) AS deposit_count,
        COUNT(DISTINCT cd.card_id) AS card_count,
        COUNT(DISTINCT l.loan_id) AS loan_count
    FROM customers c
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN cards cd ON a.account_id = cd.account_id
    LEFT JOIN loans l ON c.customer_id = l.customer_id
    GROUP BY c.customer_id, c.onboarding_channel
)
SELECT 
    onboarding_channel,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(deposit_count), 2) AS avg_deposits_per_cust,
    ROUND(AVG(card_count), 2) AS avg_cards_per_cust,
    ROUND(AVG(loan_count), 2) AS avg_loans_per_cust,
    ROUND(AVG(deposit_count + card_count + loan_count), 2) AS overall_product_density
FROM CustomerProducts
GROUP BY onboarding_channel
ORDER BY overall_product_density DESC;
