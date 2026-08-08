-- Tier 3 Query 01: Customer Transaction History with Window Running Totals
-- Business Context: Reconstructs real-time ledger balance trajectory per account.

SELECT 
    account_id,
    transaction_id,
    transaction_date,
    amount,
    transaction_type,
    SUM(CASE WHEN transaction_type IN ('Direct Deposit', 'ACH Outbound') THEN amount ELSE -amount END) 
        OVER (PARTITION BY account_id ORDER BY transaction_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_ledger_balance
FROM transactions
WHERE account_id IN (1, 2, 3, 4, 5)
ORDER BY account_id, transaction_date ASC
LIMIT 100;
