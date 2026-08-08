-- Aegis Crest Financial - Enterprise Banking Operations Analytics Platform
-- Analytical Views (database/views.sql)

-- 1. VIEW: Executive Regional KPI Summary
CREATE VIEW IF NOT EXISTS v_regional_executive_kpis AS
SELECT 
    r.region_id,
    r.region_name,
    r.regional_director,
    r.digital_fasttrack_enabled,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    SUM(CASE WHEN c.is_digital_fasttrack = 1 THEN 1 ELSE 0 END) AS fasttrack_customers,
    ROUND(100.0 * SUM(CASE WHEN c.is_digital_fasttrack = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT c.customer_id), 2) AS fasttrack_customer_pct,
    COUNT(DISTINCT l.loan_id) AS total_loans,
    ROUND(AVG(l.approval_turnaround_days), 2) AS avg_approval_turnaround_days,
    ROUND(SUM(l.principal_amount), 2) AS total_loan_principal,
    SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaulted_loans,
    ROUND(100.0 * SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) / COUNT(DISTINCT l.loan_id), 2) AS loan_default_rate_pct,
    COUNT(DISTINCT t.ticket_id) AS total_support_tickets,
    ROUND(AVG(t.resolution_time_hours), 2) AS avg_ticket_resolution_hours,
    ROUND(AVG(t.customer_satisfaction_score), 2) AS avg_csat_score,
    SUM(t.escalation_flag) AS escalated_ticket_count
FROM regions r
LEFT JOIN customers c ON r.region_id = c.region_id
LEFT JOIN loans l ON c.customer_id = l.customer_id
LEFT JOIN support_tickets t ON c.customer_id = t.customer_id
GROUP BY r.region_id, r.region_name, r.regional_director, r.digital_fasttrack_enabled;

-- 2. VIEW: Customer 360 Operational Profile
CREATE VIEW IF NOT EXISTS v_customer_360 AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.credit_score,
    c.dti_ratio,
    c.annual_income,
    c.onboarding_channel,
    c.is_digital_fasttrack,
    r.region_name,
    COUNT(DISTINCT a.account_id) AS active_accounts,
    COALESCE(SUM(a.current_balance), 0.00) AS total_deposit_balance,
    COUNT(DISTINCT l.loan_id) AS total_loans_held,
    COALESCE(SUM(l.principal_amount), 0.00) AS total_loan_balance,
    COUNT(DISTINCT st.ticket_id) AS total_support_tickets,
    COUNT(DISTINCT fa.alert_id) AS total_fraud_alerts
FROM customers c
JOIN regions r ON c.region_id = r.region_id
LEFT JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN loans l ON c.customer_id = l.customer_id
LEFT JOIN support_tickets st ON c.customer_id = st.customer_id
LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id
GROUP BY c.customer_id;

-- 3. VIEW: High-Risk Digital FastTrack Cohort Audit
CREATE VIEW IF NOT EXISTS v_fasttrack_risk_audit AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    r.region_name,
    c.credit_score,
    c.dti_ratio,
    c.onboard_date,
    l.loan_id,
    l.loan_type,
    l.principal_amount,
    l.status AS loan_status,
    l.approval_turnaround_days,
    fa.alert_id AS fraud_alert_id,
    fa.fraud_type,
    fa.loss_amount
FROM customers c
JOIN regions r ON c.region_id = r.region_id
JOIN loans l ON c.customer_id = l.customer_id
LEFT JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id
WHERE c.is_digital_fasttrack = 1
  AND c.onboard_date BETWEEN '2024-07-01' AND '2024-12-31';
