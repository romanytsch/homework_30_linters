SELECT AVG(ag.grade) as avg_reading_homework
FROM assignments_grades ag
WHERE ag.assisgnment_id IN (
    SELECT assisgnment_id
    FROM assignments
    WHERE LOWER(assignment_text) LIKE '%прочитать%'
       OR LOWER(assignment_text) LIKE '%выучить%'
);
