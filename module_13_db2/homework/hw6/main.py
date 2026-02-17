import sqlite3


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    # 1. Очищаем таблицу расписания
    cursor.execute("DELETE FROM table_friendship_schedule")

    # 2. Загружаем сотрудников
    cursor.execute("SELECT id, preferable_sport FROM table_friendship_employees")
    employees = cursor.fetchall()

    # 3. Спорт → день недели (0=пн, 1=вт, ..., 6=вс)
    sport_to_dow = {
        'футбол': 0,
        'хоккей': 1,
        'шахматы': 2,
        'SUP-сёрфинг': 3,
        'бокс': 4,
        'Dota2': 5,
        'шахбокс': 6
    }

    # 4. Заполняем 366 дней (високосный год 2024)
    for day_num in range(1, 367):
        # День недели
        day_of_week = (day_num - 1) % 7

        # Запрещённый спорт этого дня
        forbidden_sport = None
        for sport, dow in sport_to_dow.items():
            if dow == day_of_week:
                forbidden_sport = sport
                break

        # Доступные сотрудники
        available_workers = [
            emp_id for emp_id, sport in employees
            if sport != forbidden_sport
        ]
        selected_workers = available_workers[:10]

        # ✅ ФОРМАТИРУЕМ ДАТУ как '2024-01-01'
        date_str = f"2024-{day_num:02d}" if day_num <= 366 else "2024-12-31"

        # 5. Заполняем смену с правильным форматом даты
        for worker_id in selected_workers:
            cursor.execute("""
                INSERT INTO table_friendship_schedule (employee_id, date) 
                VALUES (?, ?)
            """, (worker_id, date_str))



if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
