SELECT t.full_name
FROM teachers t
JOIN assignments a ON t.teacher_id = a.teacher_id
JOIN assignments_grades g ON g.assisgnment_id = a.assisgnment_id
GROUP BY t.teacher_id, t.full_name
ORDER BY AVG(g.grade) ASC
LIMIT 3;