-- Tier 4 Query 03: Underwriting Bottleneck Drilldown by Credit Tier & FastTrack Flag
-- Business Context: Proves manual verification backlog accumulated in lower credit tiers.

WITH UnderwritingStats AS (
    SELECT 
        l.is_fasttrack_approval,
        CASE 
            WHEN c.credit_score >= 700 THEN '700+ (Low Risk)'
            WHEN c.credit_score >= 620 THEN '620-699 (Medium Risk)'
            ELSE '<620 (High Risk)'
        END AS risk_tier,
        COUNT(l.loan_id) AS total_loans,
        AVG(l.approval_turnaround_days) AS avg_turnaround,
        SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaults
    FROM loans l
    JOIN customers c ON l.customer_id = c.customer_id
    GROUP BY l.is_fasttrack_approval, risk_tier
)
SELECT 
    CASE WHEN is_fasttrack_approval = 1 THEN 'FastTrack Flow' ELSE 'Standard Flow' END AS flow_type,
    risk_tier,
    total_loans,
    ROUND(avg_turnaround, 2) AS avg_turnaround_days,
    defaults,
    ROUND(100.0 * defaults / total_loans, 2) AS default_rate_pct
FROM UnderwritingStats
ORDER BY flow_type, risk_tier;
