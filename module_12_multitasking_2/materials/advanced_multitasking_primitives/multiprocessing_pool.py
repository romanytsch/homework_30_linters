import requests
import sqlite3
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Инициализация базы данных"""
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


def fetch_character(uid):
    """Получение данных персонажа из SWAPI"""
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
        logger.error(f"Ошибка при загрузке персонажа {uid}: {e}")
        return None


def save_to_db(characters):
    """Сохранение персонажей в базу данных"""
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


def clear_db():
    """Очистка базы данных"""
    init_db()
    conn = sqlite3.connect('starwars_characters.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters")
    conn.commit()
    conn.close()


def threadpool_map():
    """ThreadPoolExecutor с map-подходом"""
    init_db()
    start = time.time()
    input_values = list(range(1, 21))  # 20 персонажей

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_character, input_values))

    save_to_db(results)

    end = time.time()
    logger.info(f'ThreadPoolExecutor (10 workers): {end - start:.2f} сек')
    logger.info(f'Загружено персонажей: {len([r for r in results if r])}')


def processpool_map():
    """multiprocessing.Pool с map"""
    init_db()
    start = time.time()
    input_values = list(range(1, 21))  # 20 персонажей

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(fetch_character, input_values)

    save_to_db(results)

    end = time.time()
    logger.info(f'ProcessPool (processes={cpu_count()}): {end - start:.2f} сек')
    logger.info(f'Загружено персонажей: {len([r for r in results if r])}')


def processpool_apply_async():
    """multiprocessing.Pool с apply_async"""
    init_db()
    start = time.time()
    input_values = list(range(1, 21))  # 20 персонажей

    pool = Pool(processes=4)
    async_results = [pool.apply_async(fetch_character, [uid]) for uid in input_values]
    pool.close()
    pool.join()

    results = [ar.get(timeout=5) for ar in async_results]
    save_to_db(results)

    end = time.time()
    logger.info(f'ProcessPool apply_async (4 processes): {end - start:.2f} сек')
    logger.info(f'Загружено персонажей: {len([r for r in results if r])}')


def high_load_comparison():
    """Высокая нагрузка"""
    logger.info('=== Высокая нагрузка: 50 персонажей ===')
    n = 50
    input_values = list(range(1, n + 1))

    # ThreadPool
    init_db()
    start = time.time()
    with ThreadPoolExecutor(max_workers=20) as executor:
        results_tp = list(executor.map(fetch_character, input_values))
    save_to_db(results_tp)
    end = time.time()
    logger.info(f'ThreadPool (20 workers): {end - start:.2f} сек')

    # ProcessPool map
    clear_db()
    start = time.time()
    with Pool(processes=cpu_count()) as pool:
        results_pm = pool.map(fetch_character, input_values)
    save_to_db(results_pm)
    end = time.time()
    logger.info(f'ProcessPool map ({cpu_count()} processes): {end - start:.2f} сек')

    # ProcessPool apply_async
    clear_db()
    start = time.time()
    pool = Pool(processes=cpu_count())
    async_results = [pool.apply_async(fetch_character, [uid]) for uid in input_values]
    pool.close()
    pool.join()
    results_pa = [ar.get(timeout=5) for ar in async_results]
    save_to_db(results_pa)
    end = time.time()
    logger.info(f'ProcessPool apply_async ({cpu_count()} processes): {end - start:.2f} сек')


if __name__ == '__main__':
    # Базовое сравнение
    clear_db()
    threadpool_map()

    clear_db()
    processpool_map()

    clear_db()
    processpool_apply_async()

    logger.info('-' * 60)

    # Тест высокой нагрузки
    high_load_comparison()
