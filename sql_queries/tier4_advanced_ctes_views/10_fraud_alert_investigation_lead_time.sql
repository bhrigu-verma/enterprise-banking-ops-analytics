-- Tier 4 Query 10: Fraud Investigation Backlog & Lead Time Analysis
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
ORDER BY total_alerts_handled DESC;
