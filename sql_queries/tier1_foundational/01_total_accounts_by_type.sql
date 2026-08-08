-- Tier 1 Query 01: Total Accounts & Balances by Account Type
-- Business Context: Provides executive overview of deposit portfolio distribution across product categories.

SELECT 
    account_type,
    COUNT(account_id) AS total_accounts,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(current_balance), 2) AS total_balance_usd,
    ROUND(AVG(current_balance), 2) AS avg_balance_usd,
    ROUND(MAX(current_balance), 2) AS max_balance_usd
FROM accounts
WHERE status = 'Active'
GROUP BY account_type
ORDER BY total_balance_usd DESC;
