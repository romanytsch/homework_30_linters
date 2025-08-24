from datetime import datetime, timedelta
import random
import os
import re
from flask import Flask

app = Flask(__name__)

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada', 'Mercedes']
breeds = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

# Абсолютный путь к папке с проектом и к файлу книги
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

COUNTER = 0

# Функция для получения списка слов из текста (без знаков препинания)
def get_words(txt):
    words_txt = re.findall(r'\b[а-яА-ЯёЁ]+\b', txt)
    return words_txt

# Читаем файл и получаем слова один раз при запуске приложения
with open(BOOK_FILE, encoding='utf-8') as file:
    text = file.read()

words = get_words(text)

@app.route('/hello_world')
def hello():
    return "Привет, мир!"


@app.route('/cars')
def cars():
    global cars_list
    return ', '.join(cars_list)


@app.route('/cats')
def cats():
    global breeds
    return random.choice(breeds)


@app.route('/get_time/now')
def current_time_func():
    current_time = datetime.now().strftime("%H:%M:%S")
    return f'«Точное время: {current_time}»'


@app.route('/get_time/future')
def current_time_future():
    future_time = datetime.now() + timedelta(hours=1)
    formatted_time = future_time.strftime("%H:%M:%S")
    return f'«Точное время через час: {formatted_time}»'


@app.route('/get_random_word')
def random_word():
    word = random.choice(words)
    return word


@app.route('/counter')
def counter():
    global COUNTER
    COUNTER += 1
    return f'{str(COUNTER)}'


if __name__ == '__main__':
    app.run(debug=True)
