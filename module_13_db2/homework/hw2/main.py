import csv
import sqlite3

sql_delete = """
DELETE
    FROM table_fees
    WHERE truck_number = ? AND timestamp = ?
"""

def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(r'C:\Users\ProBook\PycharmProjects\python_advanced\module_13_db2\homework\wrong_fees.csv', 'r', newline='', encoding='windows-1251') as csv_file:
        wrong_fees_all = csv.reader(csv_file, delimiter=',')
        next(wrong_fees_all, None)

        for row in wrong_fees_all:
            if row:
                truck_number = row[0].strip()
                timestamp = row[1].strip()
                cursor.execute(sql_delete, (truck_number, timestamp))
                print(f"Удаляем: {truck_number} от {timestamp}")



if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
