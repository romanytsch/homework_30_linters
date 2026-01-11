import sqlite3

get_vaccine = """
SELECT EXISTS(
    SELECT 1 
    FROM table_truck_with_vaccine 
    WHERE truck_number = ?
      AND temperature_in_celsius NOT BETWEEN -20 AND -16
)
"""

def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    cursor.execute(get_vaccine, (truck_number,))

    return cursor.fetchone()[0] == 1



if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect(r'C:\Users\ProBook\PycharmProjects\python_advanced\module_13_db2\homework\homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')

        conn.commit()
