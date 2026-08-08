-- Tier 3 Query 03: Month-over-Month Fraud Loss Growth Rate (LAG Window Function)
-- Business Context: Tracks velocity and trajectory of confirmed fraud financial losses.

WITH MonthlyFraud AS (
    SELECT 
        STRFTIME('%Y-%m', alert_date) AS alert_month,
        SUM(loss_amount) AS current_month_loss
    FROM fraud_alerts
    WHERE status = 'Confirmed Fraud'
    GROUP BY alert_month
)
SELECT 
    alert_month,
    ROUND(current_month_loss, 2) AS loss_usd,
    ROUND(LAG(current_month_loss, 1) OVER (ORDER BY alert_month), 2) AS prior_month_loss_usd,
    ROUND(
        100.0 * (current_month_loss - LAG(current_month_loss, 1) OVER (ORDER BY alert_month)) / 
        LAG(current_month_loss, 1) OVER (ORDER BY alert_month), 
    2) AS mom_growth_pct
FROM MonthlyFraud
ORDER BY alert_month ASC;
