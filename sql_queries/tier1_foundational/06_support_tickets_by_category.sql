-- Tier 1 Query 06: Support Ticket Volume by Issue Category
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
ORDER BY category ASC, total_tickets DESC;
