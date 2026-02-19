SELECT pc.model, pc.price
FROM PC pc
JOIN Product p ON p.model = pc.model
WHERE p.maker = 'B'

UNION

SELECT l.model, l.price
FROM Laptop l
JOIN Product p ON p.model = l.model
WHERE p.maker = 'B'

UNION

SELECT pr.model, pr.price
FROM Printer pr
JOIN Product p ON p.model = pr.model
WHERE p.maker = 'B'
