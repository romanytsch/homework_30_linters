SELECT DISTINCT p.maker
FROM PC pc
JOIN Product p ON p.model = pc.model
WHERE speed >= 450;