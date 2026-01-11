import sqlite3

sql_request = """
    SELECT *
        FROM `table_kotlin`
        WHERE wind >= '33'
"""

if __name__ == "__main__":
    with sqlite3.connect('practise.db') as conn:
        cursor = conn.cursor()
        cursor.execute(sql_request)
        days_wind_count = len(cursor.fetchall())

        print(f'Количество ветреных дней: {days_wind_count}')

