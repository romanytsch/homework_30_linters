import sqlite3


def add_10_records_to_table_warehouse(cursor: sqlite3.Cursor) -> None:
    for item in range(10):
        cursor.execute("""
        INSERT INTO `table_warehouse` (name, description, amount)
        VALUES (?, ?, ?)
    """, ('Помидоры', 'Кучерявые', f'{item * 100 + 500}')
    )



if __name__ == "__main__":
    with sqlite3.connect(r"C:\Users\ProBook\PycharmProjects\python_advanced\module_13_db2\materials\db_1.db") as conn:
        cursor = conn.cursor()
        add_10_records_to_table_warehouse(cursor)
        conn.commit()
