SELECT
    c.full_name,
    o.order_no
FROM "order" o
JOIN customer c ON o.customer_id = c.customer_id
LEFT JOIN manager m ON o.manager_id = m.manager_id
WHERE o.manager_id IS NULL;