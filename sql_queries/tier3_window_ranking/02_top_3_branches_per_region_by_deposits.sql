-- Tier 3 Query 02: Top 3 Branches Per Region Ranked by Deposit Balances (DENSE_RANK)
-- Business Context: Drives regional performance awards and branch benchmarking.

WITH BranchBalances AS (
    SELECT 
        r.region_name,
        b.branch_id,
        b.branch_name,
        SUM(a.current_balance) AS total_deposit_balance
    FROM branches b
    JOIN regions r ON b.region_id = r.region_id
    JOIN accounts a ON b.branch_id = a.branch_id
    GROUP BY r.region_name, b.branch_id, b.branch_name
),
RankedBranches AS (
    SELECT 
        region_name,
        branch_name,
        ROUND(total_deposit_balance, 2) AS total_deposit_balance,
        DENSE_RANK() OVER (PARTITION BY region_name ORDER BY total_deposit_balance DESC) AS regional_rank
    FROM BranchBalances
)
SELECT region_name, branch_name, total_deposit_balance, regional_rank
FROM RankedBranches
WHERE regional_rank <= 3
ORDER BY region_name, regional_rank;
