SELECT DISTINCT b.name
FROM Ships s
JOIN Outcomes o ON s.name = o.ship
JOIN Battles b ON o.battle = b.name
WHERE s.class = 'Kongo'