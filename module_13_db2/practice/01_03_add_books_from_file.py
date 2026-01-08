import sqlite3


def add_books_from_file(c: sqlite3.Cursor, file_name: str) -> None:
    with open(file_name, 'r', encoding='utf-8') as file:
        first_line = True
        for i_line in file:
            i_line = i_line.strip()

            if not i_line:  # пропускаем пустые строки
                continue

            data = i_line.split(',')

            if first_line:
                first_line = False
                continue

            if len(data) != 4:
                print(f"Пропуск некорректной строки: {i_line}")
                continue

            isbn = data[0].strip()
            book_name = data[1].strip()
            author = data[2].strip()
            publish_year = data[3].strip()

            c.execute("""
            INSERT INTO `table_books` (isbn, book_name, author, publish_year)
            VALUES (?, ?, ?, ?)
            """, (isbn, book_name, author, publish_year))


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_books_from_file(cursor, "book_list.csv")
        conn.commit()
