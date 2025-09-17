from flask import Flask

app = Flask(__name__)
storage = {}

@app.route('/add/<date>/<int:number>', methods=['GET'])
def add_expense(date, number):
    try:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
    except (ValueError, IndexError):
        return 'Неверный формат даты. Используйте YYYYMMDD.', 400

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
