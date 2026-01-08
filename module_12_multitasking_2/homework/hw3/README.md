from threading import Semaphore, Thread, Event
import time
import signal
import sys

sem: Semaphore = Semaphore()
stop_event = Event()

def signal_handler(sig, frame):
    print('\nПолучен сигнал прерывания, завершение потоков...')
    stop_event.set()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def fun1():
    while True:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)

def fun2():
    while True:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)

t1 = Thread(target=fun1, daemon=True)
t2 = Thread(target=fun2, daemon=True)

t1.start()
t2.start()

# Бесконечное ожидание с проверкой события
while not stop_event.is_set():
    time.sleep(0.1)
