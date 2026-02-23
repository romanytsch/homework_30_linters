SELECT
    sg.group_id,
    COUNT(DISTINCT s.student_id) as total_students,
    AVG(ag.grade) as avg_grade,
    COUNT(DISTINCT CASE WHEN ag.grade < 60 THEN s.student_id END) as failed_students,
    COUNT(DISTINCT CASE WHEN ag.date > a.due_date THEN s.student_id END) as overdue_students,
    COUNT(ag.grade_id) - COUNT(DISTINCT CONCAT(s.student_id, '_', a.assisgnment_id)) as retry_attempts
FROM students_groups sg
JOIN students s ON sg.group_id = s.group_id
JOIN assignments a ON a.group_id = sg.group_id
JOIN assignments_grades ag ON ag.assisgnment_id = a.assisgnment_id
GROUP BY sg.group_id;
