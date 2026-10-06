-- =========================================================
-- CUSTOMER CHURN PREDICTION PROJECT
-- SQL DATA EXPLORATION AND ANALYSIS (EDA)
-- Objective:
-- Analyze customer behavior and identify patterns associated with churn.
-- =========================================================


-- =========================================================
-- 1. CREATE DATABASE
-- =========================================================

CREATE DATABASE IF NOT EXISTS customer_churn_project;


-- =========================================================
-- 2. SELECT PROJECT DATABASE
-- =========================================================

USE customer_churn_project;


-- =========================================================
-- 3. VIEW AVAILABLE TABLES
-- =========================================================

SHOW TABLES;


-- =========================================================
-- 4. CHECK TOTAL NUMBER OF CUSTOMERS
-- =========================================================

SELECT COUNT(*) AS total_rows
FROM customers;


-- =========================================================
-- 5. CHECK UNIQUE CUSTOMER IDs
-- =========================================================

SELECT COUNT(DISTINCT customerID) AS unique_customers
FROM customers;


-- =========================================================
-- 6. VIEW FIRST 5 RECORDS
-- =========================================================

SELECT *
FROM customers
LIMIT 5;


-- =========================================================
-- 7. CHECK TABLE STRUCTURE AND DATA TYPES
-- =========================================================

DESCRIBE customers;


-- =========================================================
-- 8. CHECK NULL VALUES IN ALL COLUMNS
-- =========================================================

SELECT
    SUM(customerID IS NULL) AS customerID_nulls,
    SUM(gender IS NULL) AS gender_nulls,
    SUM(SeniorCitizen IS NULL) AS SeniorCitizen_nulls,
    SUM(Partner IS NULL) AS Partner_nulls,
    SUM(Dependents IS NULL) AS Dependents_nulls,
    SUM(tenure IS NULL) AS tenure_nulls,
    SUM(PhoneService IS NULL) AS PhoneService_nulls,
    SUM(MultipleLines IS NULL) AS MultipleLines_nulls,
    SUM(InternetService IS NULL) AS InternetService_nulls,
    SUM(OnlineSecurity IS NULL) AS OnlineSecurity_nulls,
    SUM(OnlineBackup IS NULL) AS OnlineBackup_nulls,
    SUM(DeviceProtection IS NULL) AS DeviceProtection_nulls,
    SUM(TechSupport IS NULL) AS TechSupport_nulls,
    SUM(StreamingTV IS NULL) AS StreamingTV_nulls,
    SUM(StreamingMovies IS NULL) AS StreamingMovies_nulls,
    SUM(Contract IS NULL) AS Contract_nulls,
    SUM(PaperlessBilling IS NULL) AS PaperlessBilling_nulls,
    SUM(PaymentMethod IS NULL) AS PaymentMethod_nulls,
    SUM(MonthlyCharges IS NULL) AS MonthlyCharges_nulls,
    SUM(TotalCharges IS NULL) AS TotalCharges_nulls,
    SUM(Churn IS NULL) AS Churn_nulls
FROM customers;


-- =========================================================
-- 9. CHECK BLANK VALUES IN TotalCharges
-- =========================================================

SELECT COUNT(*) AS blank_totalcharges
FROM customers
WHERE TRIM(TotalCharges) = '';


-- =========================================================
-- 10. INVESTIGATE CUSTOMERS WITH BLANK TotalCharges
-- =========================================================

SELECT
    customerID,
    tenure,
    MonthlyCharges,
    TotalCharges,
    Churn
FROM customers
WHERE TRIM(TotalCharges) = '';


-- =========================================================
-- 11. CHECK DUPLICATE CUSTOMER IDs
-- =========================================================

SELECT
    customerID,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customerID
HAVING COUNT(*) > 1;


-- =========================================================
-- 12. CHECK CHURN DISTRIBUTION
-- =========================================================

SELECT
    Churn,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customers),
        2
    ) AS percentage
FROM customers
GROUP BY Churn;


-- Result:
-- Total customers = 7,043
-- Churned customers = 1,869 (26.54%)
-- Non-churned customers = 5,174 (73.46%)
--
-- The target variable is moderately imbalanced.


-- =========================================================
-- 13. NUMERICAL FEATURE SUMMARY
-- =========================================================

SELECT
    MIN(tenure) AS min_tenure,
    MAX(tenure) AS max_tenure,
    ROUND(AVG(tenure), 2) AS avg_tenure,

    MIN(MonthlyCharges) AS min_monthly_charges,
    MAX(MonthlyCharges) AS max_monthly_charges,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,

    MIN(SeniorCitizen) AS min_senior_citizen,
    MAX(SeniorCitizen) AS max_senior_citizen,
    ROUND(AVG(SeniorCitizen), 2) AS avg_senior_citizen

FROM customers;


-- Result:
-- Tenure ranges from 0 to 72 months.
-- Average tenure = 32.37 months.
-- Monthly charges range from 18.25 to 118.75.
-- Average monthly charges = 64.76.
-- Approximately 16% of customers are senior citizens.


-- =========================================================
-- 14. GENDER DISTRIBUTION
-- =========================================================

SELECT
    gender,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customers),
        2
    ) AS percentage
FROM customers
GROUP BY gender;


-- Result:
-- Female = 49.52%
-- Male = 50.48%
--
-- Gender distribution is approximately balanced.


-- =========================================================
-- 15. CONTRACT DISTRIBUTION
-- =========================================================

SELECT
    Contract,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customers),
        2
    ) AS percentage
FROM customers
GROUP BY Contract
ORDER BY customer_count DESC;


-- Result:
-- Month-to-month = 55.02%
-- Two year = 24.07%
-- One year = 20.91%


-- =========================================================
-- 16. CHURN RATE BY CONTRACT TYPE
-- =========================================================

SELECT
    Contract,
    COUNT(*) AS total_customers,
   SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY Contract
ORDER BY churn_rate DESC;


-- Result:
-- Month-to-month = 42.71%
-- One year = 11.27%
-- Two year = 2.83%
--
-- Month-to-month customers show a substantially higher
-- observed churn rate than customers on longer-term contracts.


-- =========================================================
-- 17. CHURN RATE BY PAYMENT METHOD
-- =========================================================

SELECT
    PaymentMethod,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate DESC;


-- Result:
-- Electronic check = 45.29%
-- Mailed check = 19.11%
-- Bank transfer (automatic) = 16.71%
-- Credit card (automatic) = 15.24%
--
-- Electronic-check customers show the highest observed
-- churn rate among the payment-method groups.


-- =========================================================
-- 18. CHURN RATE BY INTERNET SERVICE
-- =========================================================

SELECT
    InternetService,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY InternetService
ORDER BY churn_rate DESC;


-- Result:
-- Fiber optic = 41.89%
-- DSL = 18.96%
-- No internet service = 7.40%
--
-- Fiber-optic customers have the highest observed churn rate.


-- =========================================================
-- 19. CHURN RATE BY PARTNER STATUS
-- =========================================================

SELECT
    Partner,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY Partner
ORDER BY churn_rate DESC;


-- Result:
-- Partner = No  → 32.96%
-- Partner = Yes → 19.66%
--
-- Customers without a partner have a higher observed churn rate in this dataset.


-- =========================================================
-- 20. CHURN RATE BY DEPENDENTS STATUS
-- =========================================================

SELECT
    Dependents,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY Dependents
ORDER BY churn_rate DESC;


-- Result:
-- Dependents = No  → 31.28%
-- Dependents = Yes → 15.45%
--
-- Customers without dependents have a higher observed churn rate in this dataset.


-- =========================================================
-- 21. CHURN RATE BY TENURE GROUP
-- =========================================================

SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49-72 months'
    END AS tenure_group,

    COUNT(*) AS total_customers,

    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,

    ROUND(
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate

FROM customers

GROUP BY tenure_group

ORDER BY churn_rate DESC;


-- Result:
-- 0-12 months   = 47.44%
-- 13-24 months  = 28.71%
-- 25-48 months  = 20.39%
-- 49-72 months  = 9.51%
--
-- Customers with shorter tenure show higher observed churn rates than long-term customers.


-- =========================================================
-- 22. CHURN RATE BY MONTHLY CHARGES GROUP
-- =========================================================

SELECT
    CASE
        WHEN MonthlyCharges < 40 THEN 'Low'
        WHEN MonthlyCharges < 70 THEN 'Medium'
        ELSE 'High'
    END AS monthly_charges_group,

    COUNT(*) AS total_customers,

    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,

    ROUND(
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate

FROM customers

GROUP BY monthly_charges_group

ORDER BY churn_rate DESC;


-- Result:
-- High charges   = 35.48%
-- Medium charges = 23.65%
-- Low charges    = 11.59%
--
-- Customers in the high MonthlyCharges group have
-- the highest observed churn rate.


-- =========================================================
-- 23. CHURN RATE BY PAPERLESS BILLING
-- =========================================================

SELECT
    PaperlessBilling,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY PaperlessBilling
ORDER BY churn_rate DESC;


-- Result:
-- Paperless billing = Yes → 33.57%
-- Paperless billing = No  → 16.33%
--
-- Customers with paperless billing have a higher observed
-- churn rate in this dataset.


-- =========================================================
-- 24. CHURN RATE BY TECH SUPPORT
-- =========================================================

SELECT
    TechSupport,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY TechSupport
ORDER BY churn_rate DESC;


-- Result:
-- No tech support           = 41.64%
-- Tech support              = 15.17%
-- No internet service       = 7.40%
--
-- Customers without Tech Support have a higher observed
-- churn rate than customers with Tech Support.


-- =========================================================
-- 25. KEY SQL EDA FINDINGS
-- =========================================================

-- 1. Dataset contains 7,043 customers.
-- 2. There are 7,043 unique customer IDs.
-- 3. No duplicate customer IDs were found.
-- 4. No SQL NULL values were found.
-- 5. 11 customers have blank TotalCharges values.
-- 6. These 11 customers have tenure = 0.
-- 7. Overall churn rate = 26.54%.
-- 8. Month-to-month contract churn rate = 42.71%.
-- 9. Electronic-check churn rate = 45.29%.
-- 10. Fiber-optic churn rate = 41.89%.
-- 11. 0-12 month tenure group churn rate = 47.44%.
-- 12. High MonthlyCharges group churn rate = 35.48%.
-- 13. Customers without Tech Support churn rate = 41.64%.
-- 14. Customers with paperless billing churn rate = 33.57%.
-- 15. Customers without a partner churn rate = 32.96%.
-- 16. Customers without dependents churn rate = 31.28%.
--
-- These findings represent observed associations in the dataset.
-- They do not imply that these factors directly cause churn.


-- =========================================================
-- END OF SQL EDA
-- =========================================================