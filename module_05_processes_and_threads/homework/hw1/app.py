"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы
используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё
является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт.
Напишите функцию, которая на вход принимает порт и запускает по нему сервер.
Если порт будет занят, она должна найти процесс по этому порту, завершить его и попытаться
запустить сервер ещё раз.
"""
import subprocess
from typing import List

from flask import Flask

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    if not isinstance(port, int):
        raise ValueError("Порт должен быть целым числом")

    pids: List[int] = []

    result = subprocess.run(['lsof', f'-i:{port}'], capture_output=True, text=True)

    if result.returncode != 0:
        return pids

    lines = result.stdout.splitlines()

    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 2:
            try:
                pid = int(parts[1])
                if pid not in pids:
                    pids.append(pid)
            except ValueError:
                continue

    return pids


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт
    @param port: порт
    """
    pids: List[int] = get_pids(port)

    for pid in pids:
        subprocess.run(['kill', '-9', str(pid)], check=True)


def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: порт
    """
    free_port(port)
    app.run(port=port)


if __name__ == '__main__':
    run(5000)
