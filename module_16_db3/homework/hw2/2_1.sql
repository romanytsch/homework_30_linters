SELECT
    c.full_name AS "Имя покупателя",
    m.full_name AS "Имя продавца",
    o.purchase_amount AS "Сумма",
    o.date AS "Дата"
FROM "order" o
JOIN customer c ON o.customer_id = c.customer_id
JOIN manager m ON o.manager_id = m.manager_id
ORDER BY o.date