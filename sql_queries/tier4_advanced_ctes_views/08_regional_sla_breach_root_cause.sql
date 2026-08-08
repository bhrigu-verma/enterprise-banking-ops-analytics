-- Tier 4 Query 08: Regional SLA Breach Root Cause Decomposition
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
ORDER BY sla_breach_pct DESC;
