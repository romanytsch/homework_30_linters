import sqlite3


def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    IVAN_SOVIN_SALARY = 100000

    cursor.execute("""
            SELECT id, salary 
                FROM table_effective_manager 
                WHERE name LIKE ? AND name != 'Иван Совин'
        """, (f'%{name}%',))
    row = cursor.fetchone()
    if row:
        emp_id, emp_salary = row
        new_salary = emp_salary * 1.1
        if new_salary > IVAN_SOVIN_SALARY:
            cursor.execute(
                "DELETE FROM table_effective_manager WHERE id = ?",
                (emp_id,)
            )
        else:
            cursor.execute(
                "UPDATE table_effective_manager SET salary = ? WHERE id = ?",
                (new_salary, emp_id)
            )



if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
