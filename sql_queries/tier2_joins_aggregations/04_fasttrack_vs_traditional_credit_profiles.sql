-- Tier 2 Query 04: FastTrack vs. Traditional Onboarding Risk Profile Comparison
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
GROUP BY c.is_digital_fasttrack;
