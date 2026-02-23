SELECT
    group_id,
    AVG(overdue_count) as avg_overdue,
    MAX(overdue_count) as max_overdue,
    MIN(overdue_count) as min_overdue
FROM (
    SELECT
        a.group_id,
        COUNT(CASE WHEN ag.date > a.due_date THEN 1 END) as overdue_count
    FROM assignments a
    JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
    GROUP BY a.assisgnment_id, a.group_id
) overdue_per_assignment
GROUP BY group_id;
