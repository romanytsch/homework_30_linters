import sqlite3


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:

    query = """
        SELECT EXISTS(
            SELECT 1 FROM table_truck_with_vaccine t1
            WHERE t1.truck_number = ?
              AND t1.temperature_in_celsius NOT BETWEEN -20 AND -16
              AND EXISTS(
                  SELECT 1 FROM table_truck_with_vaccine t2
                  WHERE t2.truck_number = t1.truck_number
                    AND t2.temperature_in_celsius NOT BETWEEN -20 AND -16
                    AND t2.timestamp >= datetime(t1.timestamp, '-2 hours')
                    AND t2.timestamp <= t1.timestamp
              )
        )
        """
    cursor.execute(query, (truck_number,))
    return cursor.fetchone()[0] == 1


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
