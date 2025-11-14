# TODO переписать реализацию ini-файла в формате dict-конфигурации.

import configparser
import sys

def ini_to_dict_config(filename):
    config = configparser.ConfigParser(interpolation=None)  # отключаем интерполяцию
    config.read(filename)

    # Формируем dict-конфигурацию
    dict_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {},
        'handlers': {},
        'loggers': {},
        'root': {}
    }

    # Форматтеры
    for fmt_name in config['formatters']['keys'].split(','):
        fmt_name = fmt_name.strip()
        dict_config['formatters'][fmt_name] = {
            'format': config[f'formatter_{fmt_name}']['format']
        }
        if 'datefmt' in config[f'formatter_{fmt_name}']:
            dict_config['formatters'][fmt_name]['datefmt'] = config[f'formatter_{fmt_name}']['datefmt']

    # Хендлеры
    for handler_name in config['handlers']['keys'].split(','):
        handler_name = handler_name.strip()
        handler_section = f'handler_{handler_name}'
        handler_class = config[handler_section]['class']
        # Формируем полное имя класса с 'logging.' если надо
        if not handler_class.startswith('logging.'):
            handler_class = 'logging.' + handler_class
        # Аргументы парсим осторожно
        args_str = config[handler_section].get('args', '').strip()
        # Обработка 'args' из ini: берем первый аргумент (например, файл или sys.stdout)
        if args_str.startswith('(') and args_str.endswith(')'):
            args_content = args_str[1:-1].strip()
        else:
            args_content = ''

        handler_dict = {
            'class': handler_class,
            'level': config[handler_section]['level'],
            'formatter': config[handler_section]['formatter']
        }

        # Преобразуем args_content в параметры
        # Для StreamHandler с (sys.stdout,) ставим stream: ext://sys.stdout
        if args_content == 'sys.stdout':
            handler_dict['stream'] = 'ext://sys.stdout'
        elif args_content.startswith("'") and args_content.endswith("'"):
            # Для FileHandler аргумент - имя файла
            handler_dict['filename'] = args_content.strip("'")
        elif args_content:
            # Для более сложных случаев можно добавить парсер если надо
            pass

        dict_config['handlers'][handler_name] = handler_dict

    # Логгеры (кроме корневого)
    for logger_name in config['loggers']['keys'].split(','):
        logger_name = logger_name.strip()
        if logger_name == 'root':
            continue
        logger_section = f'logger_{logger_name}'
        logger_dict = {
            'level': config[logger_section]['level'],
            'handlers': [h.strip() for h in config[logger_section]['handlers'].split(',')],
            'propagate': config[logger_section].get('propagate', '1') in ['1', 'true', 'True']
        }
        # qualname можно учесть, но в dict-конфигурации имя ключа и так qualname
        dict_config['loggers'][logger_name] = logger_dict

    # Корневой логгер
    root_section = 'logger_root'
    if root_section in config:
        dict_config['root'] = {
            'level': config[root_section]['level'],
            'handlers': [h.strip() for h in config[root_section]['handlers'].split(',')]
        }

    return dict_config

# Пример использования
if __name__ == '__main__':
    import pprint
    dict_conf = ini_to_dict_config('logging_conf.ini')
    pprint.pprint(dict_conf)
