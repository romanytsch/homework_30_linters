"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import json
from typing import Dict
from collections import Counter
import re


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    msg_dict = {'ERROR': 0, 'WARNING': 0, 'INFO': 0, 'DEBUG': 0, 'CRITICAL': 0}

    with open('skillbox_json_messages.log', 'r') as file:
        for line in file:
            i_msg = json.loads(line)

            level = i_msg['level']
            if level in msg_dict:
                msg_dict[level] += 1

    return msg_dict

def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    hour_counts = {}

    with open('skillbox_json_messages.log', 'r') as file:
        for line in file:
            i_msg = json.loads(line)

            time_str = i_msg.get('time', '')
            if time_str:
                hour = int(time_str.split(':')[0])
                hour_counts[hour] = hour_counts.get(hour, 0) + 1

    max_hour = max(hour_counts, key=hour_counts.get)
    return max_hour



def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    count = 0
    start_time = "05:00:00"
    end_time = "05:20:00"

    with open('skillbox_json_messages.log', 'r') as file:
        for line in file:
            i_msg = json.loads(line)
            time_str = i_msg.get("time", "")
            level = i_msg.get("level", "")

            if level == "CRITICAL" and start_time <= time_str <= end_time:
                count += 1

    return count


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    count = 0

    with open('skillbox_json_messages.log', 'r') as file:
        for line in file:
            i_log = json.loads(line)
            msg = i_log['message']

            if 'dog' in msg.lower():
                count += 1

    return count


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    word_counter = Counter()

    with open('skillbox_json_messages.log', 'r') as file:
        for line in file:
            log_entry = json.loads(line)
            if log_entry.get('level') == 'WARNING':
                message = log_entry.get('message', '').lower()
                # Разбиваем сообщение на слова, игнорируя знаки пунктуации
                words = re.findall(r'\b\w+\b', message.lower())
                filtered_words = [w for w in words if len(w) > 1 and w != 's']
                word_counter.update(filtered_words)

    if word_counter:
        most_common_word, _ = word_counter.most_common(1)[0]
        return most_common_word
    else:
        return ''


if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
