SELECT
    o.order_no,
    m.full_name,
    c.full_name
FROM "order" o
JOIN manager m ON o.manager_id = m.manager_id
JOIN customer c ON o.customer_id = c.customer_id
WHERE m.city != c.city;