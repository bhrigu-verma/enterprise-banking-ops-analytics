-- Tier 2 Query 07: Loan Underwriting Turnaround Time by Region & Channel
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
ORDER BY sla_variance_days DESC;
