import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
MAX_SEATS: int = 40
PRINT_BATCH: int = 6

logging.basicConfig(level=logging.INFO, format='[%(threadName)s] %(message)s')
logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, stop_event: threading.Event) -> None:
        super().__init__()
        self.sem = semaphore
        self.stop_event = stop_event
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        while not self.stop_event.is_set():
            self.random_sleep()
            if self.stop_event.is_set():
                break
            with self.sem:
                if TOTAL_TICKETS <= 0 or self.stop_event.is_set():
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'sold one; {TOTAL_TICKETS} left')
        logger.info(f'Seller finished, sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, sellers_count: int, stop_event: threading.Event) -> None:
        super().__init__()
        self.sem = semaphore
        self.sellers_count = sellers_count
        self.stop_event = stop_event
        self.total_printed = TOTAL_TICKETS
        self.daemon = True  # Важно: демон-поток завершится автоматически

    def run(self) -> None:
        global TOTAL_TICKETS
        while not self.stop_event.is_set():
            time.sleep(0.1)
            if self.stop_event.is_set():
                break

            with self.sem:
                if self.stop_event.is_set():
                    break

                # Проверяем условия для печати
                if (0 < TOTAL_TICKETS <= self.sellers_count and
                        self.total_printed < MAX_SEATS):
                    can_print = MAX_SEATS - self.total_printed
                    to_print = min(PRINT_BATCH, can_print)
                    TOTAL_TICKETS += to_print
                    self.total_printed += to_print
                    logger.info(
                        f'Printed {to_print} tickets, now {TOTAL_TICKETS}, total {self.total_printed}/{MAX_SEATS}')

                # Если лимит достигнут И билетов нет — сигнализируем остановку
                if self.total_printed >= MAX_SEATS and TOTAL_TICKETS <= 0:
                    logger.info('Director: limit reached and no tickets left')
                    self.stop_event.set()
                    break


def main() -> None:
    semaphore = threading.Semaphore(1)  # Один за раз (либо продавец, либо директор)
    stop_event = threading.Event()

    sellers_count = 3
    sellers = []

    # Запускаем продавцов
    for _ in range(sellers_count):
        seller = Seller(semaphore, stop_event)
        seller.start()
        sellers.append(seller)

    # Запускаем директора
    director = Director(semaphore, sellers_count, stop_event)
    director.start()

    # Ждём продавцов (директор — завершится автоматически)
    for seller in sellers:
        seller.join()

    logger.info('All sellers finished. Cinema closed.')


if __name__ == '__main__':
    main()
