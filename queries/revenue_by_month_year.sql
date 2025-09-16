-- TODO: Esta consulta devolverá una tabla con los ingresos por mes y año.
-- Tendrá varias columnas: month_no, con los números de mes del 01 al 12;
-- month, con las primeras 3 letras de cada mes (ej. Ene, Feb);
-- Year2016, con los ingresos por mes de 2016 (0.00 si no existe);
-- Year2017, con los ingresos por mes de 2017 (0.00 si no existe); y
-- Year2018, con los ingresos por mes de 2018 (0.00 si no existe).

WITH month_year_revenue AS (
    SELECT 
        STRFTIME('%m', o.order_delivered_customer_date) AS month_no,
        STRFTIME('%Y', o.order_delivered_customer_date) AS year,
        SUM(oi.price + oi.freight_value) AS revenue
    FROM olist_orders o
    INNER JOIN olist_order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered' 
        AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY STRFTIME('%m', o.order_delivered_customer_date), STRFTIME('%Y', o.order_delivered_customer_date)
),
months AS (
    SELECT '01' AS month_no, 'Jan' AS month
    UNION SELECT '02', 'Feb'
    UNION SELECT '03', 'Mar'
    UNION SELECT '04', 'Apr'
    UNION SELECT '05', 'May'
    UNION SELECT '06', 'Jun'
    UNION SELECT '07', 'Jul'
    UNION SELECT '08', 'Aug'
    UNION SELECT '09', 'Sep'
    UNION SELECT '10', 'Oct'
    UNION SELECT '11', 'Nov'
    UNION SELECT '12', 'Dec'
)
SELECT 
    m.month_no,
    m.month,
    COALESCE(SUM(CASE WHEN myr.year = '2016' THEN myr.revenue END), 0.0) AS Year2016,
    COALESCE(SUM(CASE WHEN myr.year = '2017' THEN myr.revenue END), 0.0) AS Year2017,
    COALESCE(SUM(CASE WHEN myr.year = '2018' THEN myr.revenue END), 0.0) AS Year2018
FROM months m
LEFT JOIN month_year_revenue myr ON m.month_no = myr.month_no
GROUP BY m.month_no, m.month
ORDER BY m.month_no;