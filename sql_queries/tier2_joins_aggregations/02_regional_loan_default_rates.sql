-- Tier 2 Query 02: Regional Loan Default Rates & Loss Exposure
-- Business Context: Pinpoints regional credit risk concentrations and default volume.

SELECT 
    r.region_id,
    r.region_name,
    r.digital_fasttrack_enabled,
    COUNT(l.loan_id) AS total_loans_issued,
    SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaulted_loans,
    ROUND(100.0 * SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) / COUNT(l.loan_id), 2) AS default_rate_pct,
    ROUND(SUM(CASE WHEN l.status = 'Defaulted' THEN l.principal_amount ELSE 0 END), 2) AS defaulted_principal_loss_usd
FROM regions r
JOIN loans l ON r.region_id = l.region_id
GROUP BY r.region_id, r.region_name, r.digital_fasttrack_enabled
ORDER BY default_rate_pct DESC;
