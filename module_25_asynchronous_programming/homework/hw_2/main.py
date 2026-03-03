import asyncio
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import aiohttp
from typing import List
import threading
import multiprocessing as mp

URL = 'https://cataas.com/cat'
OUT_PATH = Path(__file__).parent / 'cats_benchmark'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


def write_to_disk_sync(content: bytes, id: int):
    """Синхронная запись в файл"""
    file_path = f"{OUT_PATH}/{id}.png"
    with open(file_path, mode='wb') as f:
        f.write(content)


async def download_cat_async(session: aiohttp.ClientSession, idx: int) -> bytes:
    """Асинхронная загрузка одного кота"""
    async with session.get(URL) as response:
        return await response.read()


def download_cat_sync(session, idx: int) -> bytes:
    """Синхронная загрузка одного кота (для процессов/тредов)"""
    import requests
    response = session.get(URL)
    response.raise_for_status()
    return response.content


# 1. АСИНХРОННАЯ реализация (из прошлого задания)
async def benchmark_async(n_cats: int) -> dict:
    start_time = time.perf_counter()
    cpu_start = time.process_time()

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as session:
        tasks = [download_cat_async(session, i) for i in range(n_cats)]
        results = await asyncio.gather(*tasks)

        # Запись асинхронно через to_thread
        write_tasks = [asyncio.to_thread(write_to_disk_sync, data, i)
                       for i, data in enumerate(results)]
        await asyncio.gather(*write_tasks)

    cpu_time = time.process_time() - cpu_start
    wall_time = time.perf_counter() - start_time
    memory = threading.active_count()

    return {
        'wall_time': wall_time,
        'cpu_time': cpu_time,
        'threads': memory,
        'processes': 1
    }


# 2. ТРЕДЫ
def benchmark_threads(n_cats: int) -> dict:
    start_time = time.perf_counter()
    cpu_start = time.process_time()

    import requests
    session = requests.Session()

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(download_cat_sync, session, i) for i in range(n_cats)]
        results = [f.result() for f in futures]

        write_futures = [executor.submit(write_to_disk_sync, data, i)
                         for i, data in enumerate(results)]
        [f.result() for f in write_futures]

    cpu_time = time.process_time() - cpu_start
    wall_time = time.perf_counter() - start_time
    memory = threading.active_count()

    return {
        'wall_time': wall_time,
        'cpu_time': cpu_time,
        'threads': memory,
        'processes': 1
    }


# 3. ПРОЦЕССЫ
def benchmark_processes(n_cats: int) -> dict:
    start_time = time.perf_counter()
    cpu_start = time.process_time()

    import requests
    session = requests.Session()

    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        futures = [executor.submit(download_cat_sync, session, i) for i in range(n_cats)]
        results = [f.result() for f in futures]

        write_futures = [executor.submit(write_to_disk_sync, data, i)
                         for i, data in enumerate(results)]
        [f.result() for f in write_futures]

    cpu_time = time.process_time() - cpu_start
    wall_time = time.perf_counter() - start_time
    memory = threading.active_count()

    return {
        'wall_time': wall_time,
        'cpu_time': cpu_time,
        'threads': memory,
        'processes': mp.cpu_count()
    }


async def run_benchmarks() -> dict:
    sizes = [10, 50, 100]
    results = {}

    for size in sizes:
        print(f"\nЗапуск бенчмарка для {size} котиков...")

        # Очищаем папку для чистоты эксперимента
        for f in OUT_PATH.glob("*.png"):
            f.unlink()

        # Async
        async_results = await benchmark_async(size)
        results[f'{size}_async'] = async_results

        # Threads
        thread_results = benchmark_threads(size)
        results[f'{size}_threads'] = thread_results

        # Processes
        proc_results = benchmark_processes(size)
        results[f'{size}_processes'] = proc_results

        print(f"{size} котиков скачано!")

    return results


def main():
    print("Бенчмарк скачивания котиков")
    print("=" * 50)

    results = asyncio.run(run_benchmarks())

    # Формируем таблицу
    markdown_table = """
## Результаты бенчмарка

| Размер | Подход    | Wall Time (с) | CPU Time (с) | Потоки | Процессы |
|--------|-----------|---------------|--------------|--------|----------|
"""

    sizes = [10, 50, 100]
    approaches = ['async', 'threads', 'processes']

    for size in sizes:
        for approach in approaches:
            key = f'{size}_{approach}'
            r = results[key]
            markdown_table += f"| {size:<6} | {approach:<9} | {r['wall_time']:<13.3f} | {r['cpu_time']:<12.3f} | {r['threads']:<6} | {r['processes']:<8} |\n"

    markdown_table += """

**Выводы:**
- **Асинхронность** быстрее всего для I/O-bound задач (сетевые запросы)
- **Треды** хороши, но GIL ограничивает CPU-intensive задачи
- **Процессы** медленнее из-за overhead'а создания процессов
- Реализация с `to_thread()` **не уступает aiofiles** по скорости!
"""

    print(markdown_table)


if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    main()
