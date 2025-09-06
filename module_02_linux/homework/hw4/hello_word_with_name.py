"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>.
Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом,
на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)

day_names = {
    0: "Хорошего понедельника",
    1: "Хорошего вторника",
    2: "Хорошей среды",
    3: "Хорошего четверга",
    4: "Хорошей пятницы",
    5: "Хорошей субботы",
    6: "Хорошего воскресенья"
}


@app.route('/hello-world/<user_name>')
def hello_world(user_name):
    weekday = datetime.today().weekday()
    weekday_names = day_names[weekday]
    return f"Привет, {user_name}. {weekday_names}!"



if __name__ == '__main__':
    app.run(debug=True)