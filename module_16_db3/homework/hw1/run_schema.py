import sqlite3

with open('create_schema.sql', 'r') as sql_file:
    sql_script: str = sql_file.read()

def create_schema():
    with sqlite3.connect('database.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        print("Схема создана успешно.")

if __name__ == '__main__':
    create_schema()