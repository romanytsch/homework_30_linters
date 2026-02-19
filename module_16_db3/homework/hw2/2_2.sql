SELECT c.full_name
FROM customer c
LEFT JOIN "order" o ON c.customer_id = o.customer_id
WHERE o.purchase_amount IS NULL;