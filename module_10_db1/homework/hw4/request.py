import sqlite3

with sqlite3.connect('hw_4_database.db') as conn:
    cur = conn.cursor()

    # 1. Бедные
    poor = cur.execute("SELECT COUNT(*) FROM salaries WHERE salary < 5000").fetchone()[0]

    # 2. Средняя
    avg_salary = cur.execute("SELECT AVG(salary) FROM salaries").fetchone()[0]

    # 3. Медиана (упрощённо через PERCENTILE_CONT в новых SQLite)
    median = cur.execute("""
        SELECT AVG(salary) FROM (
            SELECT salary FROM salaries ORDER BY salary LIMIT 2 OFFSET (
                SELECT (COUNT(*) - 1) / 2 FROM salaries
            )
        )
    """).fetchone()[0]

    # 4. Коэффициент F
    salaries = [row[0] for row in cur.execute("SELECT salary FROM salaries ORDER BY salary DESC").fetchall()]
    n = len(salaries)
    top10_count = max(1, round(0.1 * n))
    top10_sum = sum(salaries[:top10_count])
    total_sum = sum(salaries)
    bottom90_sum = total_sum - top10_sum
    f = round(100.0 * top10_sum / bottom90_sum, 2) if bottom90_sum > 0 else 0.0

    print(f"Бедные: {poor}, Средняя: {avg_salary:.2f}, Медиана: {median:.2f}, F: {f}%")