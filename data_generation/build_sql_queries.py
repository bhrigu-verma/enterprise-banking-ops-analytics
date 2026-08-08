#!/usr/bin/env python3
"""
Generates 48 SQL queries across 4 tiers with business annotations.
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sql_queries"))

queries = {
    "tier1_foundational": {
        "01_total_accounts_by_type.sql": """-- Tier 1 Query 01: Total Accounts & Balances by Account Type
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
ORDER BY total_balance_usd DESC;""",

        "02_customer_credit_score_distribution.sql": """-- Tier 1 Query 02: Customer Credit Score Band Distribution
-- Business Context: Segments customer base by FICO score risk tier (Super Prime, Prime, Near Prime, Subprime).

SELECT 
    CASE 
        WHEN credit_score >= 750 THEN '1. Super Prime (750+)'
        WHEN credit_score >= 670 THEN '2. Prime (670-749)'
        WHEN credit_score >= 580 THEN '3. Near Prime (580-669)'
        ELSE '4. Subprime (<580)'
    END AS credit_tier,
    COUNT(customer_id) AS customer_count,
    ROUND(100.0 * COUNT(customer_id) / (SELECT COUNT(*) FROM customers), 2) AS pct_of_total,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    ROUND(AVG(dti_ratio), 4) AS avg_dti_ratio
FROM customers
GROUP BY credit_tier
ORDER BY credit_tier ASC;""",

        "03_high_value_transactions.sql": """-- Tier 1 Query 03: High-Value Transactions Above $5,000 Threshold
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
LIMIT 100;""",

        "04_regional_branch_counts.sql": """-- Tier 1 Query 04: Regional Branch and Staffing Footprint
-- Business Context: Tracks operational capacity and physical presence across geographic regions.

SELECT 
    r.region_id,
    r.region_name,
    r.regional_director,
    COUNT(b.branch_id) AS total_branches,
    SUM(b.total_staff) AS total_staff_members,
    ROUND(AVG(b.total_staff), 1) AS avg_staff_per_branch
FROM regions r
LEFT JOIN branches b ON r.region_id = b.region_id
GROUP BY r.region_id, r.region_name, r.regional_director
ORDER BY total_branches DESC;""",

        "05_active_loans_by_type.sql": """-- Tier 1 Query 05: Loan Portfolio Breakdown by Loan Product
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
ORDER BY total_principal_usd DESC;""",

        "06_support_tickets_by_category.sql": """-- Tier 1 Query 06: Support Ticket Volume by Issue Category
-- Business Context: Identifies top operational friction points impacting customer experience.

SELECT 
    category,
    priority,
    COUNT(ticket_id) AS total_tickets,
    ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_hours,
    ROUND(AVG(customer_satisfaction_score), 2) AS avg_csat,
    SUM(escalation_flag) AS escalated_tickets
FROM support_tickets
GROUP BY category, priority
ORDER BY category ASC, total_tickets DESC;""",

        "07_fraud_alerts_by_status.sql": """-- Tier 1 Query 07: Fraud Alert Status & Loss Summary
-- Business Context: Measures risk mitigation efficacy and total confirmed financial fraud losses.

SELECT 
    fraud_type,
    status,
    COUNT(alert_id) AS alert_count,
    ROUND(SUM(loss_amount), 2) AS total_loss_usd,
    ROUND(AVG(loss_amount), 2) AS avg_loss_usd,
    ROUND(AVG(risk_score), 1) AS avg_risk_score
FROM fraud_alerts
GROUP BY fraud_type, status
ORDER BY total_loss_usd DESC;""",

        "08_monthly_transaction_volumes.sql": """-- Tier 1 Query 08: Monthly Transaction Volume & Dollar Value
-- Business Context: Evaluates payment network throughput and monthly seasonality.

SELECT 
    STRFTIME('%Y-%m', transaction_date) AS tx_month,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_volume_usd,
    ROUND(AVG(amount), 2) AS avg_transaction_size,
    SUM(is_flagged_fraud) AS flagged_fraud_count
FROM transactions
GROUP BY tx_month
ORDER BY tx_month ASC;""",

        "09_average_loan_interest_rates.sql": """-- Tier 1 Query 09: Average Interest Rates & Risk Scores by Product
-- Business Context: Ensures loan pricing aligns with risk models across lending categories.

SELECT 
    p.product_name,
    p.category,
    COUNT(l.loan_id) AS count_issued,
    ROUND(AVG(l.interest_rate) * 100, 2) AS avg_rate_pct,
    ROUND(AVG(l.initial_risk_score), 1) AS avg_risk_score,
    ROUND(AVG(l.approval_turnaround_days), 2) AS avg_turnaround_days
FROM products p
JOIN loans l ON p.product_id = l.product_id
GROUP BY p.product_name, p.category
ORDER BY count_issued DESC;""",

        "10_top_merchants_by_volume.sql": """-- Tier 1 Query 10: Top 15 Merchant Outlets by Purchase Volume
-- Business Context: Identifies core merchant partners and spending concentration.

SELECT 
    merchant_name,
    merchant_category,
    COUNT(transaction_id) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_spend_usd,
    ROUND(AVG(amount), 2) AS avg_ticket_size
FROM transactions
WHERE merchant_name IS NOT NULL
GROUP BY merchant_name, merchant_category
ORDER BY total_spend_usd DESC
LIMIT 15;""",

        "11_onboarding_channel_breakdown.sql": """-- Tier 1 Query 11: Onboarding Channel Distribution & Credit Profiles
-- Business Context: Compares customer acquisition channels against baseline credit scores.

SELECT 
    onboarding_channel,
    is_digital_fasttrack,
    COUNT(customer_id) AS total_customers,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(dti_ratio), 4) AS avg_dti_ratio,
    ROUND(AVG(annual_income), 2) AS avg_annual_income
FROM customers
GROUP BY onboarding_channel, is_digital_fasttrack
ORDER BY total_customers DESC;""",

        "12_delinquent_loans_summary.sql": """-- Tier 1 Query 12: Delinquent Loan Payment Overview
-- Business Context: Tracks late payment severity across 30, 60, and 90+ day delinquency buckets.

SELECT 
    payment_status,
    COUNT(loan_payment_id) AS payment_records,
    ROUND(SUM(amount_paid), 2) AS total_amount,
    ROUND(AVG(days_overdue), 1) AS avg_days_overdue,
    MAX(days_overdue) AS max_days_overdue
FROM loan_payments
WHERE payment_status != 'On-Time'
GROUP BY payment_status
ORDER BY avg_days_overdue DESC;"""
    },

    "tier2_joins_aggregations": {
        "01_customer_account_loan_summary.sql": """-- Tier 2 Query 01: Multi-Table Customer Financial Summary (Customers + Accounts + Loans)
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
LIMIT 50;""",

        "02_regional_loan_default_rates.sql": """-- Tier 2 Query 02: Regional Loan Default Rates & Loss Exposure
-- Business Context: Pinpoints regional credit risk concentrations and default volume.

SELECT 
    r.region_id,
    r.region_name,
    r.digital_fasttrack_enabled,
    COUNT(l.loan_id) AS total_loans_issued,
    SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaulted_loans,
    ROUND(100.0 * SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) / COUNT(l.loan_id), 2) AS default_rate_pct,
    ROUND(SUM(CASE WHEN l.status = 'Defaulted' THEN l.principal_amount ELSE 0 END), 2) AS defaulted_principal_loss_usd
FROM regions r
JOIN loans l ON r.region_id = l.region_id
GROUP BY r.region_id, r.region_name, r.digital_fasttrack_enabled
ORDER BY default_rate_pct DESC;""",

        "03_branch_employee_ticket_resolution.sql": """-- Tier 2 Query 03: Branch Employee Staffing & Customer Support Efficiency
-- Business Context: Correlates branch headcount with support ticket resolution SLAs and CSAT scores.

SELECT 
    b.branch_id,
    b.branch_name,
    r.region_name,
    b.total_staff,
    COUNT(DISTINCT st.ticket_id) AS total_tickets_handled,
    ROUND(AVG(st.resolution_time_hours), 2) AS avg_resolution_hours,
    ROUND(AVG(st.customer_satisfaction_score), 2) AS avg_csat_score,
    SUM(st.escalation_flag) AS escalated_tickets
FROM branches b
JOIN regions r ON b.region_id = r.region_id
JOIN support_tickets st ON b.branch_id = st.branch_id
GROUP BY b.branch_id, b.branch_name, r.region_name, b.total_staff
ORDER BY avg_csat_score ASC;""",

        "04_fasttrack_vs_traditional_credit_profiles.sql": """-- Tier 2 Query 04: FastTrack vs. Traditional Onboarding Risk Profile Comparison
-- Business Context: Quantifies credit score and DTI degradation in the FastTrack digital cohort.

SELECT 
    c.is_digital_fasttrack,
    COUNT(c.customer_id) AS customer_count,
    ROUND(AVG(c.credit_score), 1) AS avg_credit_score,
    ROUND(AVG(c.dti_ratio), 4) AS avg_dti_ratio,
    ROUND(AVG(c.annual_income), 2) AS avg_annual_income,
    ROUND(AVG(l.approval_turnaround_days), 2) AS avg_loan_turnaround_days,
    ROUND(100.0 * SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) / COUNT(l.loan_id), 2) AS loan_default_rate_pct
FROM customers c
LEFT JOIN loans l ON c.customer_id = l.customer_id
GROUP BY c.is_digital_fasttrack;""",

        "05_card_spend_by_product_tier.sql": """-- Tier 2 Query 05: Card Product Spend & Fee Revenue Correlation
-- Business Context: Analyzes transaction throughput and annual fee yield across card tiers.

SELECT 
    p.product_name,
    p.subcategory AS card_tier,
    p.annual_fee,
    COUNT(DISTINCT c.card_id) AS cards_issued,
    COUNT(t.transaction_id) AS total_transactions,
    ROUND(SUM(t.amount), 2) AS total_spend_usd,
    ROUND(AVG(t.amount), 2) AS avg_spend_per_tx
FROM products p
JOIN cards c ON p.product_id = c.product_id
JOIN transactions t ON c.card_id = t.card_id
GROUP BY p.product_name, p.subcategory, p.annual_fee
ORDER BY total_spend_usd DESC;""",

        "06_fraud_loss_by_region_and_type.sql": """-- Tier 2 Query 06: Fraud Loss Concentration by Region and Fraud Type
-- Business Context: Guides cybersecurity and fraud prevention budget allocation.

SELECT 
    r.region_name,
    fa.fraud_type,
    COUNT(fa.alert_id) AS confirmed_alerts,
    ROUND(SUM(fa.loss_amount), 2) AS total_loss_usd,
    ROUND(AVG(fa.risk_score), 1) AS avg_risk_score
FROM fraud_alerts fa
JOIN accounts a ON fa.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN regions r ON c.region_id = r.region_id
WHERE fa.status = 'Confirmed Fraud'
GROUP BY r.region_name, fa.fraud_type
ORDER BY total_loss_usd DESC;""",

        "07_loan_turnaround_by_region_and_channel.sql": """-- Tier 2 Query 07: Loan Underwriting Turnaround Time by Region & Channel
-- Business Context: Exposes operational bottlenecks following the FastTrack digital rollout.

SELECT 
    r.region_name,
    c.onboarding_channel,
    COUNT(l.loan_id) AS loans_processed,
    ROUND(AVG(l.approval_turnaround_days), 2) AS avg_turnaround_days,
    ROUND(MAX(l.approval_turnaround_days), 2) AS max_turnaround_days,
    r.target_sla_days,
    ROUND(AVG(l.approval_turnaround_days) - r.target_sla_days, 2) AS sla_variance_days
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
JOIN regions r ON l.region_id = r.region_id
GROUP BY r.region_name, c.onboarding_channel, r.target_sla_days
ORDER BY sla_variance_days DESC;""",

        "08_customer_csat_by_onboarding_type.sql": """-- Tier 2 Query 08: Customer Satisfaction (CSAT) & Ticket Escalations by Channel
-- Business Context: Measures post-onboarding friction in digital vs. branch customers.

SELECT 
    c.onboarding_channel,
    st.category AS ticket_category,
    COUNT(st.ticket_id) AS ticket_count,
    ROUND(AVG(st.customer_satisfaction_score), 2) AS avg_csat,
    SUM(st.escalation_flag) AS escalated_count,
    ROUND(100.0 * SUM(st.escalation_flag) / COUNT(st.ticket_id), 2) AS escalation_pct
FROM support_tickets st
JOIN customers c ON st.customer_id = c.customer_id
GROUP BY c.onboarding_channel, st.category
ORDER BY escalation_pct DESC;""",

        "09_high_dti_loan_exposure.sql": """-- Tier 2 Query 09: High Debt-to-Income (>40%) Loan Portfolio Exposure
-- Business Context: Audits high-risk lending exposure to ensure capital adequacy compliance.

SELECT 
    r.region_name,
    COUNT(l.loan_id) AS high_dti_loans,
    ROUND(SUM(l.principal_amount), 2) AS total_exposure_usd,
    ROUND(AVG(c.dti_ratio), 4) AS avg_dti,
    ROUND(AVG(c.credit_score), 1) AS avg_credit_score,
    SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaults
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
JOIN regions r ON l.region_id = r.region_id
WHERE c.dti_ratio > 0.40
GROUP BY r.region_name
ORDER BY total_exposure_usd DESC;""",

        "10_payment_failure_rates_by_method.sql": """-- Tier 2 Query 10: Payment Clearing Times & Failure Rates by Payment Method
-- Business Context: Evaluates payment rail reliability and clearing latency.

SELECT 
    payment_method,
    COUNT(payment_id) AS total_payments,
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS failed,
    ROUND(100.0 * SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) / COUNT(payment_id), 2) AS failure_rate_pct,
    ROUND(AVG(clearing_time_seconds), 1) AS avg_clearing_sec
FROM payments
GROUP BY payment_method
ORDER BY failure_rate_pct DESC;""",

        "11_merchant_fraud_concentration.sql": """-- Tier 2 Query 11: Merchant Fraud Concentration & Chargeback Risk
-- Business Context: Identifies high-risk merchants with anomalous fraudulent transaction rates.

SELECT 
    t.merchant_name,
    t.merchant_category,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.is_flagged_fraud) AS fraud_transactions,
    ROUND(100.0 * SUM(t.is_flagged_fraud) / COUNT(t.transaction_id), 2) AS fraud_rate_pct,
    ROUND(SUM(CASE WHEN t.is_flagged_fraud = 1 THEN t.amount ELSE 0 END), 2) AS total_fraud_dollar_volume
FROM transactions t
WHERE t.merchant_name IS NOT NULL
GROUP BY t.merchant_name, t.merchant_category
HAVING fraud_transactions >= 5
ORDER BY fraud_rate_pct DESC
LIMIT 20;""",

        "12_regional_operating_margin_proxy.sql": """-- Tier 2 Query 12: Regional Operational Profitability Proxy
-- Business Context: Balances interest revenue against loan default write-offs and fraud losses.

SELECT 
    r.region_name,
    ROUND(SUM(l.principal_amount * l.interest_rate), 2) AS est_annual_interest_revenue,
    COALESCE(ROUND(SUM(CASE WHEN l.status = 'Defaulted' THEN l.principal_amount ELSE 0 END), 2), 0.00) AS defaulted_principal_loss,
    COALESCE(ROUND(SUM(fa.loss_amount), 2), 0.00) AS confirmed_fraud_loss,
    ROUND(
        SUM(l.principal_amount * l.interest_rate) - 
        COALESCE(SUM(CASE WHEN l.status = 'Defaulted' THEN l.principal_amount ELSE 0 END), 0.00) - 
        COALESCE(SUM(fa.loss_amount), 0.00), 
    2) AS net_operational_margin_usd
FROM regions r
LEFT JOIN loans l ON r.region_id = l.region_id
LEFT JOIN customers c ON r.region_id = c.region_id
LEFT JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
GROUP BY r.region_id, r.region_name
ORDER BY net_operational_margin_usd DESC;"""
    },

    "tier3_window_ranking": {
        "01_customer_transaction_running_balance.sql": """-- Tier 3 Query 01: Customer Transaction History with Window Running Totals
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
LIMIT 100;""",

        "02_top_3_branches_per_region_by_deposits.sql": """-- Tier 3 Query 02: Top 3 Branches Per Region Ranked by Deposit Balances (DENSE_RANK)
-- Business Context: Drives regional performance awards and branch benchmarking.

WITH BranchBalances AS (
    SELECT 
        r.region_name,
        b.branch_id,
        b.branch_name,
        SUM(a.current_balance) AS total_deposit_balance
    FROM branches b
    JOIN regions r ON b.region_id = r.region_id
    JOIN accounts a ON b.branch_id = a.branch_id
    GROUP BY r.region_name, b.branch_id, b.branch_name
)
SELECT 
    region_name,
    branch_name,
    ROUND(total_deposit_balance, 2) AS total_deposit_balance,
    DENSE_RANK() OVER (PARTITION BY region_name ORDER BY total_deposit_balance DESC) AS regional_rank
FROM BranchBalances
QUALIFY regional_rank <= 3
ORDER BY region_name, regional_rank;""",

        "03_month_over_month_fraud_loss_growth.sql": """-- Tier 3 Query 03: Month-over-Month Fraud Loss Growth Rate (LAG Window Function)
-- Business Context: Tracks velocity and trajectory of confirmed fraud financial losses.

WITH MonthlyFraud AS (
    SELECT 
        STRFTIME('%Y-%m', alert_date) AS alert_month,
        SUM(loss_amount) AS current_month_loss
    FROM fraud_alerts
    WHERE status = 'Confirmed Fraud'
    GROUP BY alert_month
)
SELECT 
    alert_month,
    ROUND(current_month_loss, 2) AS loss_usd,
    ROUND(LAG(current_month_loss, 1) OVER (ORDER BY alert_month), 2) AS prior_month_loss_usd,
    ROUND(
        100.0 * (current_month_loss - LAG(current_month_loss, 1) OVER (ORDER BY alert_month)) / 
        LAG(current_month_loss, 1) OVER (ORDER BY alert_month), 
    2) AS mom_growth_pct
FROM MonthlyFraud
ORDER BY alert_month ASC;""",

        "04_loan_approval_turnaround_rank_by_region.sql": """-- Tier 3 Query 04: Regional Ranking of Loan Approval Turnaround Times (ROW_NUMBER / NTILE)
-- Business Context: Identifies regions with severe underwriting latency spikes.

SELECT 
    r.region_name,
    l.loan_id,
    l.loan_type,
    l.approval_turnaround_days,
    ROW_NUMBER() OVER (PARTITION BY r.region_id ORDER BY l.approval_turnaround_days DESC) AS turnaround_rank,
    NTILE(4) OVER (PARTITION BY r.region_id ORDER BY l.approval_turnaround_days ASC) AS turnaround_quartile
FROM loans l
JOIN regions r ON l.region_id = r.region_id
ORDER BY r.region_name, l.approval_turnaround_days DESC;""",

        "05_customer_ticket_frequency_lag.sql": """-- Tier 3 Query 05: Customer Support Ticket Repeat Contact Latency (LEAD/LAG)
-- Business Context: Measures customer friction by calculating time elapsed between repeated tickets.

SELECT 
    customer_id,
    ticket_id,
    ticket_date,
    category,
    LAG(ticket_date, 1) OVER (PARTITION BY customer_id ORDER BY ticket_date) AS prior_ticket_date,
    ROUND(
        (JULIANDAY(ticket_date) - JULIANDAY(LAG(ticket_date, 1) OVER (PARTITION BY customer_id ORDER BY ticket_date))) * 24.0, 
    1) AS hours_since_last_ticket
FROM support_tickets
ORDER BY customer_id, ticket_date ASC
LIMIT 100;""",

        "06_moving_7day_avg_transaction_amount.sql": """-- Tier 3 Query 06: 7-Day Moving Average Transaction Volume (WINDOW Frames)
-- Business Context: Smooths daily volatility to detect true operational volume trends.

WITH DailyVolume AS (
    SELECT 
        DATE(transaction_date) AS tx_date,
        COUNT(transaction_id) AS tx_count,
        SUM(amount) AS daily_amount
    FROM transactions
    GROUP BY tx_date
)
SELECT 
    tx_date,
    tx_count,
    ROUND(daily_amount, 2) AS daily_amount_usd,
    ROUND(AVG(daily_amount) OVER (ORDER BY tx_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS moving_7day_avg_amount
FROM DailyVolume
ORDER BY tx_date ASC;""",

        "07_customer_credit_score_quartile_analysis.sql": """-- Tier 3 Query 07: Customer Credit Score Quartile & Loan Default Risk Segmenting
-- Business Context: Segments portfolio into credit score quartiles to measure risk escalation.

WITH CustomerQuartiles AS (
    SELECT 
        customer_id,
        credit_score,
        NTILE(4) OVER (ORDER BY credit_score ASC) AS credit_quartile
    FROM customers
)
SELECT 
    cq.credit_quartile,
    MIN(cq.credit_score) AS min_credit_score,
    MAX(cq.credit_score) AS max_credit_score,
    COUNT(DISTINCT cq.customer_id) AS customer_count,
    COUNT(l.loan_id) AS loans_issued,
    SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) / COUNT(l.loan_id), 2) AS default_rate_pct
FROM CustomerQuartiles cq
LEFT JOIN loans l ON cq.customer_id = l.customer_id
GROUP BY cq.credit_quartile
ORDER BY cq.credit_quartile ASC;""",

        "08_first_vs_last_transaction_by_account.sql": """-- Tier 3 Query 08: First vs. Most Recent Account Activity (FIRST_VALUE / LAST_VALUE)
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
LIMIT 50;""",

        "09_loan_payment_delinquency_lead_days.sql": """-- Tier 3 Query 09: Delinquent Payment Progression Tracking (LAG / LEAD)
-- Business Context: Monitors payment degradation sequence (On-Time -> Late 30 -> Late 60 -> Default).

SELECT 
    loan_id,
    loan_payment_id,
    payment_date,
    payment_status,
    days_overdue,
    LAG(payment_status, 1) OVER (PARTITION BY loan_id ORDER BY payment_date) AS prior_payment_status,
    LEAD(payment_status, 1) OVER (PARTITION BY loan_id ORDER BY payment_date) AS next_payment_status
FROM loan_payments
WHERE loan_id IN (SELECT DISTINCT loan_id FROM loan_payments WHERE payment_status != 'On-Time')
ORDER BY loan_id, payment_date ASC
LIMIT 100;""",

        "10_employee_ticket_resolution_percentile.sql": """-- Tier 3 Query 10: Staff Support Efficiency Percentile Ranking (PERCENT_RANK)
-- Business Context: Benchmarks resolution times across customer service leads.

WITH EmpResolution AS (
    SELECT 
        e.employee_id,
        e.first_name || ' ' || e.last_name AS employee_name,
        b.branch_name,
        AVG(st.resolution_time_hours) AS avg_res_hours
    FROM employees e
    JOIN branches b ON e.branch_id = b.branch_id
    JOIN support_tickets st ON b.branch_id = st.branch_id
    GROUP BY e.employee_id, employee_name, b.branch_name
)
SELECT 
    employee_name,
    branch_name,
    ROUND(avg_res_hours, 2) AS avg_res_hours,
    ROUND(PERCENT_RANK() OVER (ORDER BY avg_res_hours ASC) * 100, 2) AS efficiency_percentile
FROM EmpResolution
ORDER BY efficiency_percentile ASC;""",

        "11_cumulative_loan_default_loss_by_region.sql": """-- Tier 3 Query 11: Cumulative Regional Loan Default Losses Over Time
-- Business Context: Tracks cumulative default loss capital burn across quarters.

WITH MonthlyDefaults AS (
    SELECT 
        r.region_name,
        STRFTIME('%Y-%m', l.start_date) AS loan_month,
        SUM(l.principal_amount) AS monthly_default_loss
    FROM loans l
    JOIN regions r ON l.region_id = r.region_id
    WHERE l.status = 'Defaulted'
    GROUP BY r.region_name, loan_month
)
SELECT 
    region_name,
    loan_month,
    ROUND(monthly_default_loss, 2) AS monthly_loss_usd,
    ROUND(SUM(monthly_default_loss) OVER (PARTITION BY region_name ORDER BY loan_month ASC), 2) AS cumulative_loss_usd
FROM MonthlyDefaults
ORDER BY region_name, loan_month ASC;""",

        "12_account_balance_decile_distribution.sql": """-- Tier 3 Query 12: Account Balance Decile Distribution (NTILE 10)
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
ORDER BY balance_decile DESC;"""
    },

    "tier4_advanced_ctes_views": {
        "01_fasttrack_business_impact_cohort_cte.sql": """-- Tier 4 Query 01: FastTrack Digital Rollout Root Cause Analysis CTE
-- Business Context: Proves the core business story: FastTrack onboarding in Regions 2 & 5 caused SLA breaches, ticket spikes, and fraud losses.

WITH PreFastTrack AS (
    SELECT 
        r.region_name,
        COUNT(c.customer_id) AS customer_count,
        AVG(l.approval_turnaround_days) AS avg_turnaround,
        SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) * 1.0 / COUNT(l.loan_id) AS default_rate,
        COUNT(st.ticket_id) AS ticket_count,
        SUM(fa.loss_amount) AS fraud_loss
    FROM regions r
    JOIN customers c ON r.region_id = c.region_id
    LEFT JOIN loans l ON c.customer_id = l.customer_id
    LEFT JOIN support_tickets st ON c.customer_id = st.customer_id
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
    WHERE c.onboard_date < '2024-07-01'
    GROUP BY r.region_name
),
PostFastTrack AS (
    SELECT 
        r.region_name,
        COUNT(c.customer_id) AS customer_count,
        AVG(l.approval_turnaround_days) AS avg_turnaround,
        SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) * 1.0 / COUNT(l.loan_id) AS default_rate,
        COUNT(st.ticket_id) AS ticket_count,
        SUM(fa.loss_amount) AS fraud_loss
    FROM regions r
    JOIN customers c ON r.region_id = c.region_id
    LEFT JOIN loans l ON c.customer_id = l.customer_id
    LEFT JOIN support_tickets st ON c.customer_id = st.customer_id
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
    WHERE c.onboard_date >= '2024-07-01'
    GROUP BY r.region_name
)
SELECT 
    post.region_name,
    ROUND(pre.avg_turnaround, 2) AS pre_turnaround_days,
    ROUND(post.avg_turnaround, 2) AS post_turnaround_days,
    ROUND(100.0 * (post.avg_turnaround - pre.avg_turnaround) / pre.avg_turnaround, 1) AS turnaround_increase_pct,
    ROUND(pre.default_rate * 100, 2) AS pre_default_pct,
    ROUND(post.default_rate * 100, 2) AS post_default_pct,
    ROUND(COALESCE(pre.fraud_loss, 0), 2) AS pre_fraud_loss_usd,
    ROUND(COALESCE(post.fraud_loss, 0), 2) AS post_fraud_loss_usd
FROM PostFastTrack post
JOIN PreFastTrack pre ON post.region_name = pre.region_name
ORDER BY turnaround_increase_pct DESC;""",

        "02_fraud_velocity_detection_cte.sql": """-- Tier 4 Query 02: High-Velocity Fraud Detection CTE (>3 Transactions in 1 Hour)
-- Business Context: Detects automated card-testing and account takeover attacks in real time.

WITH HourlyTx AS (
    SELECT 
        account_id,
        STRFTIME('%Y-%m-%d %H:00:00', transaction_date) AS tx_hour,
        COUNT(transaction_id) AS tx_count,
        SUM(amount) AS total_hourly_amount,
        COUNT(DISTINCT location_city) AS unique_cities
    FROM transactions
    GROUP BY account_id, tx_hour
    HAVING tx_count >= 3
)
SELECT 
    ht.account_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    r.region_name,
    ht.tx_hour,
    ht.tx_count,
    ROUND(ht.total_hourly_amount, 2) AS total_hourly_amount_usd,
    ht.unique_cities
FROM HourlyTx ht
JOIN accounts a ON ht.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN regions r ON c.region_id = r.region_id
ORDER BY ht.tx_count DESC, total_hourly_amount_usd DESC
LIMIT 50;""",

        "03_loan_underwriting_bottleneck_drilldown.sql": """-- Tier 4 Query 03: Underwriting Bottleneck Drilldown by Credit Tier & FastTrack Flag
-- Business Context: Proves manual verification backlog accumulated in lower credit tiers.

WITH UnderwritingStats AS (
    SELECT 
        l.is_fasttrack_approval,
        CASE 
            WHEN c.credit_score >= 700 THEN '700+ (Low Risk)'
            WHEN c.credit_score >= 620 THEN '620-699 (Medium Risk)'
            ELSE '<620 (High Risk)'
        END AS risk_tier,
        COUNT(l.loan_id) AS total_loans,
        AVG(l.approval_turnaround_days) AS avg_turnaround,
        SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaults
    FROM loans l
    JOIN customers c ON l.customer_id = c.customer_id
    GROUP BY l.is_fasttrack_approval, risk_tier
)
SELECT 
    CASE WHEN is_fasttrack_approval = 1 THEN 'FastTrack Flow' ELSE 'Standard Flow' END AS flow_type,
    risk_tier,
    total_loans,
    ROUND(avg_turnaround, 2) AS avg_turnaround_days,
    defaults,
    ROUND(100.0 * defaults / total_loans, 2) AS default_rate_pct
FROM UnderwritingStats
ORDER BY flow_type, risk_tier;""",

        "04_multi_channel_customer_journey_attribution.sql": """-- Tier 4 Query 04: Customer Channel Touchpoint Attribution & Cross-Sell Rate
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
ORDER BY overall_product_density DESC;""",

        "05_loan_portfolio_vintage_loss_analysis.sql": """-- Tier 4 Query 05: Loan Vintage Loss Analysis by Onboarding Quarter
-- Business Context: Evaluates default loss curve evolution by origination cohort.

WITH VintageCohorts AS (
    SELECT 
        STRFTIME('%Y-Q', start_date) AS origination_quarter,
        COUNT(loan_id) AS total_loans_originated,
        SUM(principal_amount) AS origination_volume,
        SUM(CASE WHEN status = 'Defaulted' THEN principal_amount ELSE 0 END) AS defaulted_volume
    FROM loans
    GROUP BY origination_quarter
)
SELECT 
    origination_quarter,
    total_loans_originated,
    ROUND(origination_volume, 2) AS origination_volume_usd,
    ROUND(defaulted_volume, 2) AS defaulted_volume_usd,
    ROUND(100.0 * defaulted_volume / origination_volume, 2) AS cumulative_loss_pct
FROM VintageCohorts
ORDER BY origination_quarter ASC;""",

        "06_branch_operational_efficiency_matrix.sql": """-- Tier 4 Query 06: Branch Operational Efficiency Composite Index
-- Business Context: Combines deposit per staff, CSAT, and ticket escalation into a single operational efficiency score.

WITH BranchMetrics AS (
    SELECT 
        b.branch_id,
        b.branch_name,
        r.region_name,
        b.total_staff,
        SUM(a.current_balance) AS total_deposits,
        AVG(st.customer_satisfaction_score) AS avg_csat,
        SUM(st.escalation_flag) AS total_escalations
    FROM branches b
    JOIN regions r ON b.region_id = r.region_id
    LEFT JOIN accounts a ON b.branch_id = a.branch_id
    LEFT JOIN support_tickets st ON b.branch_id = st.branch_id
    GROUP BY b.branch_id, b.branch_name, r.region_name, b.total_staff
)
SELECT 
    branch_name,
    region_name,
    total_staff,
    ROUND(total_deposits / total_staff, 2) AS deposits_per_staff_usd,
    ROUND(avg_csat, 2) AS avg_csat_score,
    total_escalations,
    ROUND((total_deposits / total_staff / 100000.0) * avg_csat - (total_escalations * 0.5), 2) AS efficiency_composite_score
FROM BranchMetrics
ORDER BY efficiency_composite_score DESC;""",

        "07_customer_churn_risk_scoring_model.sql": """-- Tier 4 Query 07: Predictive Customer Churn Risk Scoring CTE
-- Business Context: Flags accounts exhibiting low balance, declining transactions, and open critical support tickets.

WITH ChurnSignals AS (
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        r.region_name,
        a.current_balance,
        COUNT(t.transaction_id) AS tx_count_30d,
        COUNT(st.ticket_id) AS ticket_count,
        SUM(CASE WHEN st.priority = 'Critical' THEN 1 ELSE 0 END) AS critical_tickets
    FROM customers c
    JOIN regions r ON c.region_id = r.region_id
    JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN transactions t ON a.account_id = t.account_id AND t.transaction_date >= '2025-11-01'
    LEFT JOIN support_tickets st ON c.customer_id = st.customer_id AND st.status = 'Open'
    GROUP BY c.customer_id, customer_name, r.region_name, a.current_balance
)
SELECT 
    customer_id,
    customer_name,
    region_name,
    ROUND(current_balance, 2) AS current_balance_usd,
    tx_count_30d,
    ticket_count,
    critical_tickets,
    CASE 
        WHEN current_balance < 200 AND tx_count_30d == 0 THEN 'High Churn Risk'
        WHEN critical_tickets >= 1 THEN 'Medium Churn Risk'
        ELSE 'Low Churn Risk'
    END AS churn_risk_tier
FROM ChurnSignals
WHERE current_balance < 500 OR critical_tickets >= 1
ORDER BY current_balance_usd ASC
LIMIT 50;""",

        "08_regional_sla_breach_root_cause.sql": """-- Tier 4 Query 08: Regional SLA Breach Root Cause Decomposition
-- Business Context: Pinpoints exact driver behind support resolution SLA breaches.

WITH TicketSLAs AS (
    SELECT 
        r.region_name,
        st.category,
        COUNT(st.ticket_id) AS total_tickets,
        AVG(st.resolution_time_hours) AS avg_res_hours,
        SUM(CASE WHEN st.resolution_time_hours > 24.0 THEN 1 ELSE 0 END) AS sla_breached_tickets
    FROM support_tickets st
    JOIN branches b ON st.branch_id = b.branch_id
    JOIN regions r ON b.region_id = r.region_id
    GROUP BY r.region_name, st.category
)
SELECT 
    region_name,
    category,
    total_tickets,
    ROUND(avg_res_hours, 2) AS avg_res_hours,
    sla_breached_tickets,
    ROUND(100.0 * sla_breached_tickets / total_tickets, 2) AS sla_breach_pct
FROM TicketSLAs
WHERE sla_breached_tickets > 0
ORDER BY sla_breach_pct DESC;""",

        "09_deposit_flight_and_liquidity_stress_cte.sql": """-- Tier 4 Query 09: Liquidity Stress & Deposit Flight Sensitivity Analysis
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
ORDER BY total_deposits_usd DESC;""",

        "10_fraud_alert_investigation_lead_time.sql": """-- Tier 4 Query 10: Fraud Investigation Backlog & Lead Time Analysis
-- Business Context: Evaluates fraud analyst workload and investigation turnaround times.

SELECT 
    e.employee_id,
    e.first_name || ' ' || e.last_name AS analyst_name,
    COUNT(fa.alert_id) AS total_alerts_handled,
    SUM(CASE WHEN fa.status = 'Confirmed Fraud' THEN 1 ELSE 0 END) AS confirmed_fraud_cases,
    ROUND(SUM(fa.loss_amount), 2) AS total_loss_mitigated_usd,
    ROUND(AVG(fa.risk_score), 1) AS avg_case_risk_score
FROM employees e
JOIN fraud_alerts fa ON e.employee_id = fa.investigated_by_emp_id
GROUP BY e.employee_id, analyst_name
ORDER BY total_alerts_handled DESC;""",

        "11_executive_kpi_scorecard_cte.sql": """-- Tier 4 Query 11: Executive KPI Scorecard Synthesis CTE
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
FROM FinancialKPIs f, RiskKPIs r, OpsKPIs o;""",

        "12_recommendation_impact_simulation_cte.sql": """-- Tier 4 Query 12: Business Recommendation Impact Simulation CTE
-- Business Context: Simulates financial savings from implementing conditional risk-based verification (recovering $3.2M in default write-offs and fraud losses).

WITH FastTrackLosses AS (
    SELECT 
        SUM(CASE WHEN l.status = 'Defaulted' THEN l.principal_amount ELSE 0 END) AS fasttrack_default_loss,
        SUM(fa.loss_amount) AS fasttrack_fraud_loss
    FROM customers c
    LEFT JOIN loans l ON c.customer_id = l.customer_id
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
    WHERE c.is_digital_fasttrack = 1
)
SELECT 
    ROUND(fasttrack_default_loss, 2) AS current_fasttrack_default_loss_usd,
    ROUND(fasttrack_fraud_loss, 2) AS current_fasttrack_fraud_loss_usd,
    ROUND(fasttrack_default_loss + fasttrack_fraud_loss, 2) AS total_current_loss_usd,
    ROUND((fasttrack_default_loss + fasttrack_fraud_loss) * 0.70, 2) AS projected_cost_savings_70pct_reduction,
    'Implement Conditional Review for Risk Score >65 or Loan Amount >$25k' AS recommended_action
FROM FastTrackLosses;"""
    }
}

def write_queries():
    total_written = 0
    for tier, file_map in queries.items():
        tier_dir = os.path.join(BASE_DIR, tier)
        os.makedirs(tier_dir, exist_ok=True)
        for fname, code in file_map.items():
            fpath = os.path.join(tier_dir, fname)
            with open(fpath, "w") as f:
                f.write(code.strip() + "\n")
            total_written += 1
    print(f"Successfully wrote {total_written} SQL queries across 4 tier directories.")

if __name__ == "__main__":
    write_queries()
