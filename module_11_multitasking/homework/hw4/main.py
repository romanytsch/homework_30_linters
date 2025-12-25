import threading
import time
import random
from queue import PriorityQueue
import sys


class Task:
    def __init__(self, priority, func, *args):
        self.priority = priority
        self.func = func
        self.args = args

    def __lt__(self, other):
        return self.priority < other.priority

    def run(self):
        return self.func(*self.args)


class Producer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Producer: Running")
        # Генерируем задачи с разными приоритетами (0-6)
        for priority in range(7):
            for _ in range(2):  # по 2 задачи на приоритет
                sleep_time = random.random()
                task = Task(priority, time.sleep, sleep_time)
                self.queue.put((priority, task))
        print("Producer: Done")


class Consumer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Consumer: Running")
        while True:
            try:
                priority, task = self.queue.get(timeout=1)
                print(f">running Task(priority={priority}).          sleep({task.args[0]})")
                task.run()
                self.queue.task_done()
            except:
                # Если очередь пуста, завершаем
                if self.queue.empty():
                    break
        print("Consumer: Done")


if __name__ == "__main__":
    queue = PriorityQueue()

    producer = Producer(queue)
    consumer = Consumer(queue)

    producer.start()
    producer.join()  # Ждем завершения producer

    consumer.start()
    consumer.join()
