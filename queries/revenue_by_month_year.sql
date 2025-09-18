-- TODO: Esta consulta devolverá una tabla con los ingresos por mes y año.
-- Tendrá varias columnas: month_no, con los números de mes del 01 al 12;
-- month, con las primeras 3 letras de cada mes (ej. Ene, Feb);
-- Year2016, con los ingresos por mes de 2016 (0.00 si no existe);
-- Year2017, con los ingresos por mes de 2017 (0.00 si no existe); y
-- Year2018, con los ingresos por mes de 2018 (0.00 si no existe).

WITH price_per_order AS (
    SELECT 
        o.order_id, 
        MIN(op.payment_value) AS total_price,
        o.order_delivered_customer_date
    FROM olist_orders o
    INNER JOIN olist_order_payments op ON o.order_id = op.order_id
    WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY o.order_id, o.order_delivered_customer_date
),
freight_per_order AS (
    SELECT 
        order_id, 
        freight_value
    FROM olist_order_items
    WHERE order_item_id = 1
),
order_totals AS (
    SELECT 
        ppo.order_id,
        ppo.total_price AS total,
        ppo.order_delivered_customer_date
    FROM price_per_order ppo
),
month_year_revenue AS (
    SELECT 
        STRFTIME('%m', ot.order_delivered_customer_date) AS month_no,
        STRFTIME('%Y', ot.order_delivered_customer_date) AS year,
        SUM(ot.total) AS revenue
    FROM order_totals ot
    GROUP BY STRFTIME('%m', ot.order_delivered_customer_date), STRFTIME('%Y', ot.order_delivered_customer_date)
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
    COALESCE(myr2016.revenue, 0.0) AS Year2016,
    COALESCE(myr2017.revenue, 0.0) AS Year2017,
    COALESCE(myr2018.revenue, 0.0) AS Year2018
FROM months m
LEFT JOIN month_year_revenue myr2016 ON m.month_no = myr2016.month_no AND myr2016.year = '2016'
LEFT JOIN month_year_revenue myr2017 ON m.month_no = myr2017.month_no AND myr2017.year = '2017'
LEFT JOIN month_year_revenue myr2018 ON m.month_no = myr2018.month_no AND myr2018.year = '2018'
ORDER BY m.month_no;