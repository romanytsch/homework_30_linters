import requests
import sqlite3
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from functools import partial


# Создаем базу данных и таблицу
def init_db():
    conn = sqlite3.connect('starwars_characters.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT,
            birth_year TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Функция для получения данных персонажа
def fetch_character(uid):
    url = f"https://www.swapi.tech/api/people/{uid}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        properties = data['result']['properties']
        return {
            'uid': uid,
            'name': properties.get('name', ''),
            'birth_year': properties.get('birth_year', ''),
            'gender': properties.get('gender', '')
        }
    except Exception as e:
        print(f"Ошибка при загрузке персонажа {uid}: {e}")
        return None


# Безопасная очистка БД
def clear_db():
    init_db()  # Сначала создаем таблицу!
    conn = sqlite3.connect('starwars_characters.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters")
    conn.commit()
    conn.close()


# Последовательная загрузка (1 функция)
def load_characters_sequential(n=20):
    init_db()
    start_time = time.time()

    conn = sqlite3.connect('starwars_characters.db')
    cursor = conn.cursor()

    for uid in range(1, n + 1):
        char_data = fetch_character(uid)
        if char_data:
            cursor.execute('''
                INSERT OR REPLACE INTO characters (id, name, birth_year, gender)
                VALUES (?, ?, ?, ?)
            ''', (char_data['uid'], char_data['name'],
                  char_data['birth_year'], char_data['gender']))

    conn.commit()
    conn.close()

    end_time = time.time()
    print(f"Последовательная загрузка {n} персонажей: {end_time - start_time:.2f} сек")
    return end_time - start_time


# Параллельная загрузка с потоками (2 функция)
def load_characters_threaded(n=20):
    init_db()
    start_time = time.time()

    # Собираем все данные в потоке
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_character, uid) for uid in range(1, n + 1)]
        characters = [future.result() for future in futures]

    # Записываем в БД после получения всех данных
    conn = sqlite3.connect('starwars_characters.db')
    cursor = conn.cursor()

    for char_data in characters:
        if char_data:
            cursor.execute('''
                INSERT OR REPLACE INTO characters (id, name, birth_year, gender)
                VALUES (?, ?, ?, ?)
            ''', (char_data['uid'], char_data['name'],
                  char_data['birth_year'], char_data['gender']))

    conn.commit()
    conn.close()

    end_time = time.time()
    print(f"Параллельная загрузка {n} персонажей (потоки): {end_time - start_time:.2f} сек")
    return end_time - start_time


# Тестирование производительности
if __name__ == "__main__":
    print("=== Тестирование производительности ===")

    # Очищаем БД перед тестом (теперь безопасно!)
    clear_db()

    # Последовательная загрузка
    time_seq = load_characters_sequential(20)

    # Очищаем БД и тестируем потоки
    clear_db()

    # Параллельная загрузка
    time_threaded = load_characters_threaded(20)

    print(f"\nУскорение: {time_seq / time_threaded:.2f}x")
