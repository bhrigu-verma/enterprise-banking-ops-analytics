-- Tier 3 Query 04: Regional Ranking of Loan Approval Turnaround Times (ROW_NUMBER / NTILE)
-- Business Context: Identifies regions with severe underwriting latency spikes.

SELECT 
    r.region_name,
    l.loan_id,
    l.loan_type,
    l.approval_turnaround_days,
    ROW_NUMBER() OVER (PARTITION BY r.region_id ORDER BY l.approval_turnaround_days DESC) AS turnaround_rank,
    NTILE(4) OVER (PARTITION BY r.region_id ORDER BY l.approval_turnaround_days ASC) AS turnaround_quartile
FROM loans l
JOIN regions r ON l.region_id = r.region_id
ORDER BY r.region_name, l.approval_turnaround_days DESC;
