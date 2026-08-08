-- Tier 2 Query 01: Multi-Table Customer Financial Summary (Customers + Accounts + Loans)
-- Business Context: Aggregates total relationship value per customer across deposits and credit liabilities.

SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.credit_score,
    r.region_name,
    COUNT(DISTINCT a.account_id) AS deposit_accounts,
    COALESCE(SUM(a.current_balance), 0.00) AS total_deposit_balance,
    COUNT(DISTINCT l.loan_id) AS active_loans,
    COALESCE(SUM(l.principal_amount), 0.00) AS total_loan_balance
FROM customers c
JOIN regions r ON c.region_id = r.region_id
LEFT JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN loans l ON c.customer_id = l.customer_id
GROUP BY c.customer_id, customer_name, c.credit_score, r.region_name
HAVING total_deposit_balance > 10000.00 OR total_loan_balance > 25000.00
ORDER BY total_deposit_balance DESC
LIMIT 50;
