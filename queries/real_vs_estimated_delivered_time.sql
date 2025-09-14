-- TODO: Esta consulta devolverá una tabla con las diferencias entre los tiempos 
-- reales y estimados de entrega por mes y año. Tendrá varias columnas: 
-- month_no, con los números de mes del 01 al 12; month, con las primeras 3 letras 
-- de cada mes (ej. Ene, Feb); Year2016_real_time, con el tiempo promedio de 
-- entrega real por mes de 2016 (NaN si no existe); Year2017_real_time, con el 
-- tiempo promedio de entrega real por mes de 2017 (NaN si no existe); 
-- Year2018_real_time, con el tiempo promedio de entrega real por mes de 2018 
-- (NaN si no existe); Year2016_estimated_time, con el tiempo promedio estimado 
-- de entrega por mes de 2016 (NaN si no existe); Year2017_estimated_time, con 
-- el tiempo promedio estimado de entrega por mes de 2017 (NaN si no existe); y 
-- Year2018_estimated_time, con el tiempo promedio estimado de entrega por mes 
-- de 2018 (NaN si no existe).
-- PISTAS:
-- 1. Puedes usar la función julianday para convertir una fecha a un número.
-- 2. order_status == 'delivered' AND order_delivered_customer_date IS NOT NULL
-- 3. Considera tomar order_id distintos.

WITH delivery_times AS (
    SELECT DISTINCT
        o.order_id,
        STRFTIME('%m', o.order_purchase_timestamp) AS month_no,
        STRFTIME('%Y', o.order_purchase_timestamp) AS year,
        julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) AS real_time,
        julianday(o.order_estimated_delivery_date) - julianday(o.order_purchase_timestamp) AS estimated_time
    FROM olist_orders o
    WHERE o.order_status = 'delivered' 
        AND o.order_delivered_customer_date IS NOT NULL
),
monthly_averages AS (
    SELECT 
        month_no,
        year,
        AVG(real_time) AS avg_real_time,
        AVG(estimated_time) AS avg_estimated_time
    FROM delivery_times
    GROUP BY month_no, year
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
    AVG(CASE WHEN ma.year = '2016' THEN ma.avg_real_time END) AS Year2016_real_time,
    AVG(CASE WHEN ma.year = '2017' THEN ma.avg_real_time END) AS Year2017_real_time,
    AVG(CASE WHEN ma.year = '2018' THEN ma.avg_real_time END) AS Year2018_real_time,
    AVG(CASE WHEN ma.year = '2016' THEN ma.avg_estimated_time END) AS Year2016_estimated_time,
    AVG(CASE WHEN ma.year = '2017' THEN ma.avg_estimated_time END) AS Year2017_estimated_time,
    AVG(CASE WHEN ma.year = '2018' THEN ma.avg_estimated_time END) AS Year2018_estimated_time
FROM months m
LEFT JOIN monthly_averages ma ON m.month_no = ma.month_no
GROUP BY m.month_no, m.month
ORDER BY m.month_no;
