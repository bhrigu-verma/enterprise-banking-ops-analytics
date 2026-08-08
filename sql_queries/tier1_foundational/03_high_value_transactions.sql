-- Tier 1 Query 03: High-Value Transactions Above $5,000 Threshold
-- Business Context: Filters large transaction events for BSA/AML audit compliance and liquidity monitoring.

SELECT 
    transaction_id,
    account_id,
    transaction_date,
    amount,
    transaction_type,
    channel,
    merchant_name,
    location_city
FROM transactions
WHERE amount >= 5000.00
ORDER BY amount DESC, transaction_date DESC
LIMIT 100;
