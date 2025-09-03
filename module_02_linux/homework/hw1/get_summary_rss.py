"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""

import os.path

base_dir = os.path.dirname(os.path.abspath(__file__))
path_file = os.path.join(base_dir, 'output_file.txt')

def get_summary_rss(ps_output_file_path: str) -> str:
    units = ['Б', 'кБ', 'МБ', 'ГБ']
    i = 0

    with open(ps_output_file_path, 'r', encoding='utf8') as file:
        total_size = 0
        read_rows = []

        for rows in file:
            read_rows = rows.split()
            value = read_rows[5]
            try:
                num_value = int(value)
                total_size += num_value
            except ValueError:
                pass



    while total_size >= 1024 and i < len(units) - 1:
        total_size = total_size / 1024
        i += 1

    if i == 0:
        human_size = f'{total_size} {units[i]}'
    else:
        human_size = f'{round(total_size)} {units[i]}'


    return human_size


if __name__ == '__main__':
    path: str = path_file
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
