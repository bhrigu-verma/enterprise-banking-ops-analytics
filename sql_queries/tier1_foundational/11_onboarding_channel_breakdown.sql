-- Tier 1 Query 11: Onboarding Channel Distribution & Credit Profiles
-- Business Context: Compares customer acquisition channels against baseline credit scores.

SELECT 
    onboarding_channel,
    is_digital_fasttrack,
    COUNT(customer_id) AS total_customers,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(dti_ratio), 4) AS avg_dti_ratio,
    ROUND(AVG(annual_income), 2) AS avg_annual_income
FROM customers
GROUP BY onboarding_channel, is_digital_fasttrack
ORDER BY total_customers DESC;
