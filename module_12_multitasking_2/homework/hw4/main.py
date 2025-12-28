import threading
import queue
import time
import requests
from datetime import datetime

log_queue = queue.Queue()
log_file = 'logs.txt'
stop_event = threading.Event()


def writer():
    """Писатель ждет ВСЕ логи и только потом сортирует/пишет"""
    logs = []

    # Ждем все логи (200 штук = 10 потоков × 20 сек)
    while len(logs) < 200 or not stop_event.is_set():
        try:
            logs.append(log_queue.get(timeout=0.5))
        except queue.Empty:
            continue

    # Сортируем и пишем
    logs.sort(key=lambda x: x[0])
    with open(log_file, 'w') as f:
        for ts, date in logs:
            f.write(f"{ts} {date}\n")
    print(f"Записано {len(logs)} логов в {log_file}")


def worker(thread_id):
    """Рабочий поток"""
    start = time.time()
    while time.time() - start < 20:
        ts = time.time()

        try:
            date = requests.get(f"http://127.0.0.1:8080/timestamp/{ts}", timeout=1).text.strip()
        except:
            date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        log_queue.put((ts, date))
        time.sleep(1)


def main():
    print("Запуск потоков...")

    # Запускаем писателя
    writer_thread = threading.Thread(target=writer)
    writer_thread.start()

    # 10 потоков по 1 в секунду
    threads = []
    for i in range(10):
        print(f"Запуск потока {i + 1}")
        time.sleep(1)
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)

    # Ждем рабочие потоки
    for t in threads:
        t.join()

    # Сигнал писателю: все готово
    stop_event.set()
    writer_thread.join()

    print("Готово! Проверьте logs.txt")


if __name__ == '__main__':
    main()
