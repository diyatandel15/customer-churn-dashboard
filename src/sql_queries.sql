-- ============================================================
-- Customer Churn Analysis - Business SQL Queries
-- Table: customers
-- Columns: customer_id, age, tenure, monthly_charges,
--          total_charges, contract_type, payment_method, churn
-- ============================================================


-- Query 1: Overall churn rate
SELECT
    COUNT(*)                                          AS total_customers,
    SUM(churn)                                        AS churned_customers,
    ROUND(SUM(churn) * 100.0 / COUNT(*), 2)           AS churn_rate_pct
FROM customers;


-- Query 2: Churn rate by contract type
SELECT
    contract_type,
    COUNT(*)                                          AS total_customers,
    SUM(churn)                                        AS churned_customers,
    ROUND(SUM(churn) * 100.0 / COUNT(*), 2)           AS churn_rate_pct
FROM customers
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;


-- Query 3: Average revenue from churned vs retained customers
SELECT
    CASE WHEN churn = 1 THEN 'Churned' ELSE 'Retained' END AS customer_status,
    COUNT(*)                                          AS customer_count,
    ROUND(AVG(monthly_charges), 2)                    AS avg_monthly_charges,
    ROUND(AVG(total_charges), 2)                      AS avg_total_charges,
    ROUND(SUM(total_charges), 2)                      AS total_revenue
FROM customers
GROUP BY churn
ORDER BY customer_status;


-- Query 4: Churn rate by payment method
SELECT
    payment_method,
    COUNT(*)                                          AS total_customers,
    SUM(churn)                                        AS churned_customers,
    ROUND(SUM(churn) * 100.0 / COUNT(*), 2)           AS churn_rate_pct
FROM customers
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;


-- Query 5: High-value customers at risk (top 10 by total_charges, month-to-month)
SELECT
    customer_id,
    age,
    tenure,
    monthly_charges,
    total_charges,
    contract_type,
    payment_method,
    churn
FROM customers
WHERE contract_type = 'Month-to-month'
  AND total_charges > (
      SELECT AVG(total_charges) FROM customers
  )
ORDER BY total_charges DESC
LIMIT 10;


-- Query 6: Tenure bucket analysis
SELECT
    CASE
        WHEN tenure < 12  THEN '0-11 months'
        WHEN tenure < 24  THEN '12-23 months'
        WHEN tenure < 36  THEN '24-35 months'
        ELSE '36+ months'
    END                                               AS tenure_bucket,
    COUNT(*)                                          AS total_customers,
    SUM(churn)                                        AS churned_customers,
    ROUND(SUM(churn) * 100.0 / COUNT(*), 2)           AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2)                    AS avg_monthly_charges
FROM customers
GROUP BY tenure_bucket
ORDER BY MIN(tenure);


-- Query 7: Age group churn analysis
SELECT
    CASE
        WHEN age < 30 THEN '18-29'
        WHEN age < 45 THEN '30-44'
        WHEN age < 60 THEN '45-59'
        ELSE '60+'
    END                                               AS age_group,
    COUNT(*)                                          AS total_customers,
    ROUND(SUM(churn) * 100.0 / COUNT(*), 2)           AS churn_rate_pct,
    ROUND(AVG(tenure), 1)                             AS avg_tenure
FROM customers
GROUP BY age_group
ORDER BY MIN(age);


-- Query 8: Monthly revenue at risk from churned customers
SELECT
    contract_type,
    COUNT(*)                                          AS churned_count,
    ROUND(SUM(monthly_charges), 2)                    AS lost_monthly_revenue,
    ROUND(AVG(monthly_charges), 2)                    AS avg_monthly_charges
FROM customers
WHERE churn = 1
GROUP BY contract_type
ORDER BY lost_monthly_revenue DESC;


-- Query 9: Customer lifetime value (CLV) comparison
SELECT
    CASE WHEN churn = 1 THEN 'Churned' ELSE 'Retained' END AS status,
    ROUND(AVG(total_charges), 2)                      AS avg_clv,
    ROUND(MIN(total_charges), 2)                      AS min_clv,
    ROUND(MAX(total_charges), 2)                      AS max_clv,
    ROUND(STDDEV(total_charges), 2)                   AS stddev_clv
FROM customers
GROUP BY churn;


-- Query 10: Cohort summary - customers with tenure < 6 months and high charges
SELECT
    payment_method,
    contract_type,
    COUNT(*)                                          AS at_risk_customers,
    ROUND(AVG(monthly_charges), 2)                    AS avg_monthly_charges,
    ROUND(SUM(churn) * 100.0 / COUNT(*), 2)           AS churn_rate_pct
FROM customers
WHERE tenure < 6
  AND monthly_charges > 70
GROUP BY payment_method, contract_type
HAVING COUNT(*) >= 5
ORDER BY churn_rate_pct DESC, at_risk_customers DESC;
