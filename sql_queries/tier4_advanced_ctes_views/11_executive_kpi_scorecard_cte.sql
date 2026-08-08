-- Tier 4 Query 11: Executive KPI Scorecard Synthesis CTE
-- Business Context: Consolidates Financial, Operational, Customer, and Risk KPIs into a single board report table.

WITH FinancialKPIs AS (
    SELECT 
        SUM(current_balance) AS total_deposits,
        (SELECT SUM(principal_amount) FROM loans WHERE status IN ('Active', 'Approved')) AS active_loan_principal,
        (SELECT SUM(principal_amount) FROM loans WHERE status = 'Defaulted') AS defaulted_loan_principal
    FROM accounts
),
RiskKPIs AS (
    SELECT 
        SUM(loss_amount) AS total_fraud_loss,
        COUNT(alert_id) AS confirmed_fraud_count
    FROM fraud_alerts
    WHERE status = 'Confirmed Fraud'
),
OpsKPIs AS (
    SELECT 
        AVG(resolution_time_hours) AS avg_ticket_res_time,
        AVG(customer_satisfaction_score) AS avg_csat
    FROM support_tickets
)
SELECT 
    ROUND(f.total_deposits, 2) AS total_deposits_usd,
    ROUND(f.active_loan_principal, 2) AS total_active_loans_usd,
    ROUND(f.defaulted_loan_principal, 2) AS total_defaulted_loans_usd,
    ROUND(100.0 * f.defaulted_loan_principal / f.active_loan_principal, 2) AS portfolio_default_rate_pct,
    ROUND(r.total_fraud_loss, 2) AS total_fraud_loss_usd,
    r.confirmed_fraud_count,
    ROUND(o.avg_ticket_res_time, 2) AS avg_ticket_res_hours,
    ROUND(o.avg_csat, 2) AS overall_csat_score
FROM FinancialKPIs f, RiskKPIs r, OpsKPIs o;
