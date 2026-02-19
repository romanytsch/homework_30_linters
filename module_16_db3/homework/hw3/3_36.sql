SELECT DISTINCT name
FROM (
    SELECT class AS name
    FROM Classes
    WHERE class NOT IN (SELECT class FROM Ships)

    UNION

    SELECT name
    FROM Ships
    WHERE name = class
) AS leads;