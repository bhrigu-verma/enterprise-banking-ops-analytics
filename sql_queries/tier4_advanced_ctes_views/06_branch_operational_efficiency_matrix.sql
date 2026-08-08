-- Tier 4 Query 06: Branch Operational Efficiency Composite Index
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
ORDER BY efficiency_composite_score DESC;
