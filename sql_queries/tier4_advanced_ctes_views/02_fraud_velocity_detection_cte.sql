-- Tier 4 Query 02: High-Velocity Fraud Detection CTE (>3 Transactions in 1 Day)
-- Business Context: Detects automated card-testing and account takeover attacks in real time.

WITH DailyTx AS (
    SELECT 
        account_id,
        DATE(transaction_date) AS tx_date,
        COUNT(transaction_id) AS tx_count,
        SUM(amount) AS total_daily_amount,
        COUNT(DISTINCT location_city) AS unique_cities
    FROM transactions
    GROUP BY account_id, tx_date
    HAVING tx_count >= 3
)
SELECT 
    dt.account_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    r.region_name,
    dt.tx_date,
    dt.tx_count,
    ROUND(dt.total_daily_amount, 2) AS total_daily_amount_usd,
    dt.unique_cities
FROM DailyTx dt
JOIN accounts a ON dt.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN regions r ON c.region_id = r.region_id
ORDER BY dt.tx_count DESC, total_daily_amount_usd DESC
LIMIT 50;
