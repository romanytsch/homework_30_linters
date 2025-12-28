from threading import Semaphore, Thread
import time
import sys

sem = Semaphore(1)  # Явно указано значение 1
stop_threads = False

def fun1():
    global stop_threads
    while True:
        sem.acquire()
        if stop_threads:
            sem.release()
            break
        print(1)
        sem.release()
        time.sleep(0.25)

def fun2():
    global stop_threads
    while True:
        sem.acquire()
        if stop_threads:
            sem.release()
            break
        print(2)
        sem.release()
        time.sleep(0.25)

t1 = Thread(target=fun1, daemon=True)
t2 = Thread(target=fun2, daemon=True)

t1.start()
t2.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\nCtrl+C!')
    stop_threads = True
    sys.exit(0)
