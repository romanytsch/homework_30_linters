"""
Реализуйте endpoint, который показывает превью файла, принимая на вход два параметра: SIZE (int) и RELATIVE_PATH —
и возвращая первые SIZE символов файла по указанному в RELATIVE_PATH пути.

Endpoint должен вернуть страницу с двумя строками.
В первой строке будет содержаться информация о файле: его абсолютный путь и размер файла в символах,
а во второй строке — первые SIZE символов из файла:

<abs_path> <result_size><br>
<result_text>

где abs_path — написанный жирным абсолютный путь до файла;
result_text — первые SIZE символов файла;
result_size — длина result_text в символах.

Перенос строки осуществляется с помощью HTML-тега <br>.

Пример:

/head_file/8/docs/simple.txt
/home/user/module_2/docs/simple.txt 8
hello wo

/head_file/12/docs/simple.txt
/home/user/module_2/docs/simple.txt 12
hello world!
"""
import os
from flask import Flask, abort, request

app = Flask(__name__)


@app.route("/head_file/<int:size>")
def head_file(size: int):
    """
    Формат запроса: http://127.0.0.1:5000/head_file/15?path=/home/roma/PycharmProjects/python_advanced/module_02_linux/homework/hw6/README.md
    """
    relative_path = request.args.get("path")
    if not relative_path:
        abort(400, description="Missing path parameter")
    file_path = os.path.abspath(relative_path)

    if not os.path.isfile(file_path):
        abort(404, description="File not found")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(size)  # читаем только SIZE символов
    except Exception as e:
        abort(500, description=f"Error reading file: {str(e)}")

    result_size = len(content)
    abs_path_formatted = f"<b>{file_path}</b>"

    return f"{abs_path_formatted} {result_size}<br>{content}"


if __name__ == "__main__":
    app.run(debug=True)
