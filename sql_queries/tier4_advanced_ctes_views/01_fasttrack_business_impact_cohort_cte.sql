-- Tier 4 Query 01: FastTrack Digital Rollout Root Cause Analysis CTE
-- Business Context: Proves the core business story: FastTrack onboarding in Regions 2 & 5 caused SLA breaches, ticket spikes, and fraud losses.

WITH PreFastTrack AS (
    SELECT 
        r.region_name,
        COUNT(c.customer_id) AS customer_count,
        AVG(l.approval_turnaround_days) AS avg_turnaround,
        SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) * 1.0 / COUNT(l.loan_id) AS default_rate,
        COUNT(st.ticket_id) AS ticket_count,
        SUM(fa.loss_amount) AS fraud_loss
    FROM regions r
    JOIN customers c ON r.region_id = c.region_id
    LEFT JOIN loans l ON c.customer_id = l.customer_id
    LEFT JOIN support_tickets st ON c.customer_id = st.customer_id
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
    WHERE c.onboard_date < '2024-07-01'
    GROUP BY r.region_name
),
PostFastTrack AS (
    SELECT 
        r.region_name,
        COUNT(c.customer_id) AS customer_count,
        AVG(l.approval_turnaround_days) AS avg_turnaround,
        SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) * 1.0 / COUNT(l.loan_id) AS default_rate,
        COUNT(st.ticket_id) AS ticket_count,
        SUM(fa.loss_amount) AS fraud_loss
    FROM regions r
    JOIN customers c ON r.region_id = c.region_id
    LEFT JOIN loans l ON c.customer_id = l.customer_id
    LEFT JOIN support_tickets st ON c.customer_id = st.customer_id
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
    WHERE c.onboard_date >= '2024-07-01'
    GROUP BY r.region_name
)
SELECT 
    post.region_name,
    ROUND(pre.avg_turnaround, 2) AS pre_turnaround_days,
    ROUND(post.avg_turnaround, 2) AS post_turnaround_days,
    ROUND(100.0 * (post.avg_turnaround - pre.avg_turnaround) / pre.avg_turnaround, 1) AS turnaround_increase_pct,
    ROUND(pre.default_rate * 100, 2) AS pre_default_pct,
    ROUND(post.default_rate * 100, 2) AS post_default_pct,
    ROUND(COALESCE(pre.fraud_loss, 0), 2) AS pre_fraud_loss_usd,
    ROUND(COALESCE(post.fraud_loss, 0), 2) AS post_fraud_loss_usd
FROM PostFastTrack post
JOIN PreFastTrack pre ON post.region_name = pre.region_name
ORDER BY turnaround_increase_pct DESC;
