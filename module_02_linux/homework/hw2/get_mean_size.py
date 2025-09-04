"""
Удобно направлять результат выполнения команды напрямую в программу с помощью
конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения
команды ls -l, а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: str) -> float:
    """На вход принимает результат выполнения команды `ls -l`,
    а возвращает средний размер файла в каталоге
    """
    count_files = 0
    size_files = 0

    lines = ls_output.strip().split('\n')

    for line in lines[1:]:
        line_list = line.split()
        if len(line_list) < 5:
            continue
        line_list = line.split()
        count_files += 1
        size_files += int(line_list[4])

    if count_files == 0:
        return 0.0

    average = size_files / count_files

    return round(average, 2)


if __name__ == '__main__':
    data: str = sys.stdin.read()
    mean_size: float = get_mean_size(data)
    print(mean_size)
