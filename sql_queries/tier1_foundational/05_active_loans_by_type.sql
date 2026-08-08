-- Tier 1 Query 05: Loan Portfolio Breakdown by Loan Product
-- Business Context: Analyzes principal balance and interest rates across loan products.

SELECT 
    loan_type,
    COUNT(loan_id) AS total_loans,
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_loans,
    SUM(CASE WHEN status = 'Defaulted' THEN 1 ELSE 0 END) AS defaulted_loans,
    ROUND(SUM(principal_amount), 2) AS total_principal_usd,
    ROUND(AVG(interest_rate) * 100, 2) AS avg_interest_rate_pct
FROM loans
GROUP BY loan_type
ORDER BY total_principal_usd DESC;
