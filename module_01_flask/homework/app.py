from datetime import datetime, timedelta
import random

from flask import Flask

app = Flask(__name__)

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada', 'Mercedes']
breeds = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

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


# @app.route('/get_random_word')
# def test_function():
#     pass
#
#
# @app.route('/counter')
# def test_function():
#     pass


if __name__ == '__main__':
    app.run(debug=True)
