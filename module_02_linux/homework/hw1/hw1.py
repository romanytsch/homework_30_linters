import os.path

base_dir = os.path.dirname(os.path.abspath(__file__))
path_file = os.path.join(base_dir, 'output_file.txt')

def size_format(size):
    """"
    Преобразует размер файла из байт в человеко-читаемый формат.

    Аргументы:
        size (int): размер файла в байтах.

    Возвращает:
        str: строка с размером и соответствующей единицей измерения,
             округленная до целого числа"""

    units = ['Б', 'кБ', 'МБ', 'ГБ']
    i = 0

    while size >= 1024 and i < len(units) - 1:
        size = size / 1024
        i += 1

    if i == 0:
        return f'{size} {units[i]}'
    else:
        return f'{round(size)} {units[i]}'


def get_summary_rss(path):
    with open(path, 'r', encoding='utf8') as file:
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


    return size_format(total_size)

def main():
    total_size = get_summary_rss(path_file)
    print(total_size)

if __name__ == "__main__":
    main()