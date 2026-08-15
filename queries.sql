-- Business questions answered against the `spending` table.

-- 1. Average total monthly spending by major, ranked highest to lowest.
SELECT
    major,
    ROUND(AVG(housing + food + transportation + books_supplies + entertainment
              + personal_care + technology + health_wellness + miscellaneous), 2) AS avg_monthly_spending
FROM spending
GROUP BY major
ORDER BY avg_monthly_spending DESC;

-- 2. Does financial aid correlate with lower part-time income? (proxy check)
SELECT
    CASE WHEN financial_aid > 0 THEN 'Receives aid' ELSE 'No aid' END AS aid_status,
    ROUND(AVG(monthly_income), 2) AS avg_income,
    COUNT(*) AS n_students
FROM spending
GROUP BY aid_status;

-- 3. Spending category breakdown as % of total spend, across all students.
SELECT
    ROUND(100.0 * SUM(housing) / SUM(housing + food + transportation + books_supplies
        + entertainment + personal_care + technology + health_wellness + miscellaneous), 1) AS pct_housing,
    ROUND(100.0 * SUM(food) / SUM(housing + food + transportation + books_supplies
        + entertainment + personal_care + technology + health_wellness + miscellaneous), 1) AS pct_food,
    ROUND(100.0 * SUM(entertainment) / SUM(housing + food + transportation + books_supplies
        + entertainment + personal_care + technology + health_wellness + miscellaneous), 1) AS pct_entertainment
FROM spending;

-- 4. Students whose total spending exceeds income + aid (potential deficit risk).
SELECT
    student_id, major, year_in_school,
    ROUND(monthly_income + financial_aid, 2) AS total_inflow,
    ROUND(housing + food + transportation + books_supplies + entertainment
          + personal_care + technology + health_wellness + miscellaneous, 2) AS total_spending
FROM spending
WHERE (housing + food + transportation + books_supplies + entertainment
       + personal_care + technology + health_wellness + miscellaneous) > (monthly_income + financial_aid)
ORDER BY (total_spending - total_inflow) DESC
LIMIT 10;

-- 5. Preferred payment method distribution by year in school.
SELECT
    year_in_school,
    preferred_payment_method,
    COUNT(*) AS n_students
FROM spending
GROUP BY year_in_school, preferred_payment_method
ORDER BY year_in_school, n_students DESC;
