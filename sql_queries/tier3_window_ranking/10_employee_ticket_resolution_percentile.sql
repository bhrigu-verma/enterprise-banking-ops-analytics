-- Tier 3 Query 10: Staff Support Efficiency Percentile Ranking (PERCENT_RANK)
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
ORDER BY efficiency_percentile ASC;
