import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None


@dataclass
class Book:
    title: str
    author_id: Optional[int] = None
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def parse_author(author_str: str) -> tuple[str, str, Optional[str]]:
    parts = author_str.strip().rsplit(' ', 2)
    if len(parts) == 1:
        return parts[0], '', None
    elif len(parts) == 2:
        return parts[0], parts[1], None
    else:
        first_name = parts[0]
        last_name = f"{parts[1]} {parts[2]}"
        return first_name, last_name, None


def get_author_id(cursor: sqlite3.Cursor, author_str: str) -> Optional[int]:
    first_name, last_name, middle_name = parse_author(author_str)
    cursor.execute(
        'SELECT id FROM authors WHERE first_name=? AND last_name=? AND middle_name=?',
        (first_name, last_name, middle_name)
    )
    result = cursor.fetchone()
    return result[0] if result else None


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute('PRAGMA foreign_keys = ON;')
        cursor = conn.cursor()

        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';")
        authors_exists = cursor.fetchone()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{BOOKS_TABLE_NAME}';")
        books_exists = cursor.fetchone()

        if not authors_exists:
            cursor.execute(f"""
                CREATE TABLE `{AUTHORS_TABLE_NAME}` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    middle_name TEXT
                );
            """)

        if books_exists:
            cursor.execute(f'DROP TABLE `{BOOKS_TABLE_NAME}`;')

        cursor.execute(f"""
            CREATE TABLE `{BOOKS_TABLE_NAME}`(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES `{AUTHORS_TABLE_NAME}`(id) ON DELETE CASCADE
            );
        """)

        for item in initial_records:
            author_str = item['author']
            first, last, middle = parse_author(author_str)

            cursor.execute(
                'SELECT id FROM authors WHERE first_name=? AND last_name=? AND middle_name=?',
                (first, last, middle)
            )
            result = cursor.fetchone()

            if result:
                author_id = result[0]
            else:
                cursor.execute(
                    'INSERT INTO authors (first_name, last_name, middle_name) VALUES (?, ?, ?)',
                    (first, last, middle)
                )
                author_id = cursor.lastrowid

            cursor.execute(
                'INSERT INTO books (title, author_id) VALUES (?, ?)',
                (item['title'], author_id)
            )
        conn.commit()


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])

def get_all_books() -> List[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        return [_get_book_obj_from_row(row) for row in cursor.fetchall()]

def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO books (title, author_id) VALUES (?, ?)',
            (book.title, book.author_id)
        )
        book.id = cursor.lastrowid
        conn.commit()
        return book

def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        row = cursor.fetchone()
        return _get_book_obj_from_row(row) if row else None

def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE books SET title = ?, author_id = ? WHERE id = ?',
            (book.title, book.author_id, book.id)
        )
        conn.commit()

def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()

def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE title = ?', (book_title,))
        row = cursor.fetchone()
        return _get_book_obj_from_row(row) if row else None

def get_author_id_by_id(author_id: int) -> bool:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM authors WHERE id = ?', (author_id,))
        return cursor.fetchone() is not None

def add_author(author: Author) -> Author:
    """Создаёт нового автора"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO authors (first_name, last_name, middle_name) VALUES (?, ?, ?)',
            (author.first_name, author.last_name, author.middle_name)
        )
        author.id = cursor.lastrowid
        conn.commit()
        return author

def get_author_by_id(author_id: int) -> Optional[Author]:
    """Получает автора по ID"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
        row = cursor.fetchone()
        if row:
            return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])
        return None

def get_books_by_author(author_id: int) -> List[Book]:
    """Получает все книги автора"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE author_id = ?', (author_id,))
        return [_get_book_obj_from_row(row) for row in cursor.fetchall()]
