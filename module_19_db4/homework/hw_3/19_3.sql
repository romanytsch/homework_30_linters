SELECT s.full_name
FROM students s
JOIN assignments_grades ag ON s.student_id = ag.student_id
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
JOIN (
    SELECT a3.teacher_id
    FROM assignments a3
    JOIN assignments_grades ag3 ON a3.assisgnment_id = ag3.assisgnment_id
    GROUP BY a3.teacher_id
    ORDER BY AVG(ag3.grade) DESC
    LIMIT 1
) best_teacher ON a.teacher_id = best_teacher.teacher_id;