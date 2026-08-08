-- Tier 3 Query 12: Account Balance Decile Distribution (NTILE 10)
-- Business Context: Analyzes wealth concentration across the customer deposit base.

WITH AccountDeciles AS (
    SELECT 
        account_id,
        current_balance,
        NTILE(10) OVER (ORDER BY current_balance ASC) AS balance_decile
    FROM accounts
    WHERE status = 'Active'
)
SELECT 
    balance_decile,
    COUNT(account_id) AS account_count,
    ROUND(MIN(current_balance), 2) AS min_balance,
    ROUND(MAX(current_balance), 2) AS max_balance,
    ROUND(SUM(current_balance), 2) AS total_balance_in_decile,
    ROUND(100.0 * SUM(current_balance) / (SELECT SUM(current_balance) FROM accounts WHERE status = 'Active'), 2) AS pct_of_total_deposits
FROM AccountDeciles
GROUP BY balance_decile
ORDER BY balance_decile DESC;
