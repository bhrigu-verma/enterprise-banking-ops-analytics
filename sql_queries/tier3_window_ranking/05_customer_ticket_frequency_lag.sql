-- Tier 3 Query 05: Customer Support Ticket Repeat Contact Latency (LEAD/LAG)
-- Business Context: Measures customer friction by calculating time elapsed between repeated tickets.

SELECT 
    customer_id,
    ticket_id,
    ticket_date,
    category,
    LAG(ticket_date, 1) OVER (PARTITION BY customer_id ORDER BY ticket_date) AS prior_ticket_date,
    ROUND(
        (JULIANDAY(ticket_date) - JULIANDAY(LAG(ticket_date, 1) OVER (PARTITION BY customer_id ORDER BY ticket_date))) * 24.0, 
    1) AS hours_since_last_ticket
FROM support_tickets
ORDER BY customer_id, ticket_date ASC
LIMIT 100;
