-- Tier 4 Query 09: Liquidity Stress & Deposit Flight Sensitivity Analysis
-- Business Context: Simulates liquidity impact if top 5% deposit account holders withdraw funds.

WITH DepositPercentiles AS (
    SELECT 
        account_id,
        current_balance,
        NTILE(20) OVER (ORDER BY current_balance DESC) AS balance_ventile -- Ventile 1 = Top 5%
    FROM accounts
    WHERE status = 'Active'
)
SELECT 
    CASE WHEN balance_ventile = 1 THEN 'Top 5% Account Holders' ELSE 'Remaining 95%' END AS segment,
    COUNT(account_id) AS account_count,
    ROUND(SUM(current_balance), 2) AS total_deposits_usd,
    ROUND(AVG(current_balance), 2) AS avg_balance_usd,
    ROUND(100.0 * SUM(current_balance) / (SELECT SUM(current_balance) FROM accounts WHERE status = 'Active'), 2) AS pct_of_bank_deposits
FROM DepositPercentiles
GROUP BY segment
ORDER BY total_deposits_usd DESC;
