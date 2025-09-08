"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было
потрачено за день, а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12),
DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""
from flask import Flask, jsonify

app = Flask(__name__)

storage = {}


@app.route('/add/<date>/<int:number>', methods=['GET'])
def add_expense(date, number):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])

    storage.setdefault(year, {}).setdefault(month, {}).setdefault(day, 0)
    storage[year][month][day] += number

    storage[year][month].setdefault('total', 0)
    storage[year][month]['total'] += number

    storage[year].setdefault('total', 0)
    storage[year]['total'] += number

    return f'Записано: {date}, траты: {number}'


@app.route('/calculate/<int:year>', methods=['GET'])
def calculate_year(year):
    total_year = storage.get(year, {}).get('total', 0)
    return f'Год: {year}, Траты: {total_year}'


@app.route('/calculate/<int:year>/<int:month>', methods=['GET'])
def calculate_year_month(year, month):
    total_month = storage.get(year, {}).get(month, {}).get('total', 0)
    return f'Год: {year}, месяц: {month} -> траты: {total_month}'


if __name__ == '__main__':
    app.run(debug=True)