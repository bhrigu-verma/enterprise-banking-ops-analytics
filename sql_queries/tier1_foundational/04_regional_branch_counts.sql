-- Tier 1 Query 04: Regional Branch and Staffing Footprint
-- Business Context: Tracks operational capacity and physical presence across geographic regions.

SELECT 
    r.region_id,
    r.region_name,
    r.regional_director,
    COUNT(b.branch_id) AS total_branches,
    SUM(b.total_staff) AS total_staff_members,
    ROUND(AVG(b.total_staff), 1) AS avg_staff_per_branch
FROM regions r
LEFT JOIN branches b ON r.region_id = b.region_id
GROUP BY r.region_id, r.region_name, r.regional_director
ORDER BY total_branches DESC;
