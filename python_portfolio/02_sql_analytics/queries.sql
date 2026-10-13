-- 1. Выручка по месяцам.
SELECT
    substr(o.order_date, 1, 7) AS month,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
GROUP BY substr(o.order_date, 1, 7)
ORDER BY month;

-- 2. Топ товаров по выручке.
SELECT
    p.product_name,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM products AS p
JOIN order_items AS oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC;

-- 3. Выручка по каждому заказу и накопительная выручка (оконная функция).
WITH order_revenue AS (
    SELECT
        o.order_id,
        o.order_date,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM orders AS o
    JOIN order_items AS oi ON oi.order_id = o.order_id
    GROUP BY o.order_id, o.order_date
)
SELECT
    order_id,
    order_date,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        SUM(revenue) OVER (
            ORDER BY order_date, order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ), 2
    ) AS cumulative_revenue
FROM order_revenue
ORDER BY order_date, order_id;

-- 4. Сравнение выручки месяца с предыдущим месяцем (LAG).
WITH monthly AS (
    SELECT
        substr(o.order_date, 1, 7) AS month,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM orders AS o
    JOIN order_items AS oi ON oi.order_id = o.order_id
    GROUP BY substr(o.order_date, 1, 7)
),
with_previous AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS previous_month_revenue
    FROM monthly
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(revenue - previous_month_revenue, 2) AS difference
FROM with_previous
ORDER BY month;

-- 5. Рейтинг заказов внутри каждого региона по сумме заказа.
WITH order_totals AS (
    SELECT
        o.order_id,
        o.order_date,
        c.region,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM orders AS o
    JOIN customers AS c ON c.customer_id = o.customer_id
    JOIN order_items AS oi ON oi.order_id = o.order_id
    GROUP BY o.order_id, o.order_date, c.region
)
SELECT
    region,
    order_id,
    ROUND(revenue, 2) AS revenue,
    DENSE_RANK() OVER (
        PARTITION BY region
        ORDER BY revenue DESC
    ) AS region_rank
FROM order_totals
ORDER BY region, region_rank;
