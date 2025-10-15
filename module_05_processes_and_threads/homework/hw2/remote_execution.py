"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение
кода, истекло, то процесс завершается, после чего отправляется сообщение о том, что
исполнение кода не уложилось в данное время.
"""
import subprocess
import sys

from flask import Flask, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

app = Flask(__name__)

class CodeForm(FlaskForm):
    code = StringField()
    timeout = IntegerField()


def run_python_code_in_subproccess(code: str, timeout: int):
    try:
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True, text=True,
            timeout=timeout
        )
        return {'output': result.stdout, 'error': result.stderr, 'timeout': False}
    except subprocess.TimeoutExpired:
        return {'output': '', 'error': 'Execution timed out', 'timeout': True}



@app.route('/run_code', methods=['GET'])
def run_code():
    code = request.args.get('code')
    timeout = request.args.get('timeout', type=int)

    if not code or timeout is None:
        return "Параметры code и timeout обязательны", 400
    if timeout <= 0 or timeout > 30:
        return "Timeout должен быть от 1 до 30 секунд", 400

    try:
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        # Возвращаем stdout и stderr как простой текст
        return f"Output:\n{result.stdout}\nError:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Время выполнения истекло", 408


if __name__ == '__main__':
    app.run(debug=True)
