/* 
   Project: Bali Hotel Cluster Revenue Analysis
   Author: Rizky A.
   POV: Cluster Revenue Analyst
   System: PostgreSQL / Amadeus API Integration
*/

-- =========================================================
-- 1. DAILY PICKUP & PACE REPORT (Amadeus GDS Ingestion)
-- Goal: Calculate net room pickup vs. same time last year (STLY)
-- =========================================================

WITH current_pickup AS (
    SELECT 
        property_id,
        check_in_date,
        COUNT(confirmation_no) as rooms_sold,
        SUM(total_price) as revenue_captured
    FROM bookings
    WHERE booking_date = CURRENT_DATE - 1
    GROUP BY 1, 2
),
historical_pickup AS (
    SELECT 
        property_id,
        check_in_date,
        COUNT(confirmation_no) as rooms_sold_stly,
        SUM(total_price) as revenue_stly
    FROM bookings_archive
    WHERE booking_date = (CURRENT_DATE - 1 - INTERVAL '1 year')
    GROUP BY 1, 2
)
SELECT 
    c.property_id,
    c.check_in_date,
    c.rooms_sold AS pickup_yesterday,
    h.rooms_sold_stly AS pickup_stly,
    (c.revenue_captured - h.revenue_stly) AS revenue_variance
FROM current_pickup c
JOIN historical_pickup h 
    ON c.property_id = h.property_id 
    AND c.check_in_date = h.check_in_date
ORDER BY c.check_in_date DESC;


-- =========================================================
-- 2. COMPETITOR RATE SHOPPING (Market Spy)
-- Goal: Identify dates where our rate is > 15% above compset avg
-- =========================================================

SELECT 
    shop_date,
    check_in_date,
    my_property_rate,
    (comp_1_rate + comp_2_rate + comp_3_rate) / 3.0 AS compset_avg,
    ROUND(
        ((my_property_rate - ((comp_1_rate + comp_2_rate + comp_3_rate) / 3.0)) / 
        ((comp_1_rate + comp_2_rate + comp_3_rate) / 3.0)) * 100, 2
    ) AS price_premium_percent
FROM rate_shopper_log
WHERE 
    ((my_property_rate - ((comp_1_rate + comp_2_rate + comp_3_rate) / 3.0)) / 
    ((comp_1_rate + comp_2_rate + comp_3_rate) / 3.0)) > 0.15
ORDER BY check_in_date ASC;


-- =========================================================
-- 3. MARKET SEGMENTATION DRILL-DOWN (Budgeting)
-- Goal: Analyze high-value booking windows for 'Corporate' segment
-- =========================================================

SELECT 
    segment_code,
    CASE 
        WHEN lead_time_days BETWEEN 0 AND 3 THEN 'Last Minute'
        WHEN lead_time_days BETWEEN 4 AND 14 THEN 'Short Lead'
        WHEN lead_time_days BETWEEN 15 AND 30 THEN 'Standard'
        ELSE 'Long Lead'
    END AS booking_window_bucket,
    COUNT(*) as total_bookings,
    AVG(adr) as avg_daily_rate,
    SUM(total_revenue) as total_rev
FROM bookings
WHERE 
    segment_code = 'CORP' 
    AND status = 'CHECKED_OUT'
GROUP BY 1, 2
HAVING SUM(total_revenue) > 50000000
ORDER BY total_rev DESC;
