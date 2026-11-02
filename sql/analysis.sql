USE pizza_sales;

-- 1. Overall Sales Performance
SELECT
    ROUND(SUM(od.quantity * p.price), 2) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(od.quantity) AS total_pizzas_sold,
    ROUND(SUM(od.quantity * p.price) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
JOIN pizzas p ON od.pizza_id = p.pizza_id;

-- 2. Monthly Revenue
SELECT
    MONTHNAME(o.order_date) AS month,
    ROUND(SUM(od.quantity * p.price), 2) AS revenue
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
JOIN pizzas p ON od.pizza_id = p.pizza_id
GROUP BY MONTH(o.order_date), MONTHNAME(o.order_date)
ORDER BY MONTH(o.order_date);

-- 3. Category-wise Sales
SELECT
    pt.category,
    SUM(od.quantity) AS pizzas_sold,
    ROUND(SUM(od.quantity * p.price), 2) AS revenue
FROM order_details od
JOIN pizzas p ON od.pizza_id = p.pizza_id
JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
GROUP BY pt.category
ORDER BY pizzas_sold DESC;

-- 4. Top 5 Best-Selling Pizzas
SELECT
    pt.name AS pizza_name,
    SUM(od.quantity) AS pizzas_sold,
    ROUND(SUM(od.quantity * p.price), 2) AS revenue
FROM order_details od
JOIN pizzas p ON od.pizza_id = p.pizza_id
JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
GROUP BY pt.name
ORDER BY pizzas_sold DESC
LIMIT 5;

-- 5. Peak Ordering Hours
SELECT
    HOUR(o.order_time) AS order_hour,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
GROUP BY HOUR(o.order_time)
ORDER BY total_orders DESC;