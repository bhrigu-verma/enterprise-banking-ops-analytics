-- Tier 2 Query 08: Customer Satisfaction (CSAT) & Ticket Escalations by Channel
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
ORDER BY escalation_pct DESC;
