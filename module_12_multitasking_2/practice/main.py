import time
from math import factorial
from multiprocessing import Pool, cpu_count
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def task(end):  # Принимает параметр - конец диапазона
    return sum(factorial(i) for i in range(end + 1))


def calculation():
    starts = [i * 1000 for i in range(10)]  # 10 чанков по 10000
    ends = [min(start + 9999, 10000) for start in starts]

    start_time = time.time()
    with Pool(processes=cpu_count()) as pool:
        partial_sums = pool.starmap(task, [(end,) for end in ends])  # Правильный вызов
        total_sum = sum(partial_sums[:1]) + sum(partial_sums[1:])  # Упрощённо

    end_time = time.time()
    logger.info(f'Сумма факториалов 0!..100000!: {total_sum}')
    logger.info(f'Время выполнения ({cpu_count()} процессов): {end_time - start_time:.2f} сек')


if __name__ == '__main__':
    calculation()