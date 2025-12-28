import requests
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import multiprocessing


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
    init_db()
    conn = sqlite3.connect('starwars_characters.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters")
    conn.commit()
    conn.close()


# 1. Загрузка с ThreadPoolExecutor (пула потоков)
def load_characters_threadpool(n=20, max_workers=10):
    init_db()
    start_time = time.time()

    # Собираем данные параллельно с потоками
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_character, uid) for uid in range(1, n + 1)]
        characters = [future.result() for future in futures]

    # Записываем в БД одним транзакционным блоком
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
    print(f"ThreadPool (workers={max_workers}): {end_time - start_time:.2f} сек")
    return end_time - start_time


# 2. Загрузка с multiprocessing.Pool (пула процессов)
def load_characters_multiprocessing(n=20, processes=None):
    if processes is None:
        processes = multiprocessing.cpu_count()

    init_db()
    start_time = time.time()

    # Собираем данные параллельно с процессами
    with Pool(processes=processes) as pool:
        characters = pool.map(fetch_character, range(1, n + 1))

    # Записываем в БД одним транзакционным блоком
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
    print(f"ProcessPool (processes={processes}): {end_time - start_time:.2f} сек")
    return end_time - start_time


# Тестирование производительности
if __name__ == "__main__":
    print("=== Сравнение ThreadPoolExecutor vs multiprocessing.Pool ===")

    # Очищаем БД
    clear_db()

    # Тест 1: ThreadPool с 10 потоками
    time_threadpool = load_characters_threadpool(20, max_workers=10)

    # Очищаем БД
    clear_db()

    # Тест 2: ProcessPool с количеством CPU ядер
    time_processpool = load_characters_multiprocessing(20)

    print(f"\n{'=' * 50}")
    print(f"Ускорение ThreadPool/ProcessPool: {time_processpool / time_threadpool:.2f}x")
    print(f"ProcessPool быстрее ThreadPool в {time_threadpool / time_processpool:.2f}x")

    # Дополнительный тест с разным количеством процессов
    print("\n=== Эксперимент с разным количеством процессов ===")
    clear_db()
    for proc_count in [2, 4, multiprocessing.cpu_count(), multiprocessing.cpu_count() * 2]:
        clear_db()
        load_characters_multiprocessing(20, processes=proc_count)
