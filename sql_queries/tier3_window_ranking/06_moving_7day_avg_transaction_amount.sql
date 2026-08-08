-- Tier 3 Query 06: 7-Day Moving Average Transaction Volume (WINDOW Frames)
-- Business Context: Smooths daily volatility to detect true operational volume trends.

WITH DailyVolume AS (
    SELECT 
        DATE(transaction_date) AS tx_date,
        COUNT(transaction_id) AS tx_count,
        SUM(amount) AS daily_amount
    FROM transactions
    GROUP BY tx_date
)
SELECT 
    tx_date,
    tx_count,
    ROUND(daily_amount, 2) AS daily_amount_usd,
    ROUND(AVG(daily_amount) OVER (ORDER BY tx_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS moving_7day_avg_amount
FROM DailyVolume
ORDER BY tx_date ASC;
