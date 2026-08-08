-- Tier 2 Query 03: Branch Employee Staffing & Customer Support Efficiency
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
ORDER BY avg_csat_score ASC;
