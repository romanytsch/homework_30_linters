SELECT DISTINCT p.maker, l.speed
FROM Product p
JOIN Laptop l ON p.model = l.model
WHERE p.type = 'Laptop' AND l.hd >= 10