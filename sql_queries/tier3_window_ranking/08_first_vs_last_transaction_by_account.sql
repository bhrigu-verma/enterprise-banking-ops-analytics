-- Tier 3 Query 08: First vs. Most Recent Account Activity (FIRST_VALUE / LAST_VALUE)
-- Business Context: Audits account lifecycle activity and dormancy signals.

SELECT DISTINCT
    account_id,
    FIRST_VALUE(transaction_date) OVER (PARTITION BY account_id ORDER BY transaction_date ASC) AS first_tx_date,
    FIRST_VALUE(amount) OVER (PARTITION BY account_id ORDER BY transaction_date ASC) AS first_tx_amount,
    LAST_VALUE(transaction_date) OVER (PARTITION BY account_id ORDER BY transaction_date ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_tx_date,
    LAST_VALUE(amount) OVER (PARTITION BY account_id ORDER BY transaction_date ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_tx_amount
FROM transactions
ORDER BY account_id ASC
LIMIT 50;
