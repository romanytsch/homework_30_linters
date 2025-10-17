"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение
кода, истекло, то процесс завершается, после чего отправляется сообщение о том, что
исполнение кода не уложилось в данное время.
"""
from flask import Flask, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.csrf import CSRFProtect, generate_csrf
import subprocess
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

csrf = CSRFProtect(app)  # инициализируем CSRF защиту

class CodeForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    timeout = IntegerField('timeout', validators=[DataRequired(), NumberRange(min=1, max=30)])

def run_python_code_in_subprocess(code: str, timeout: int):
    try:
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True, text=True, timeout=timeout
        )
        return {'output': result.stdout, 'error': result.stderr, 'timeout': False}
    except subprocess.TimeoutExpired:
        return {'output': '', 'error': 'Execution timed out', 'timeout': True}

@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if not form.validate_on_submit():
        return jsonify({'error': 'Invalid input', 'messages': form.errors}), 400

    code = form.code.data
    timeout = form.timeout.data
    result = run_python_code_in_subprocess(code, timeout)

    if result['timeout']:
        return jsonify({'error': 'Execution timed out'}), 408
    return jsonify({'output': result['output'], 'error': result['error']})

@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    response = jsonify({'csrf_token': token})
    return response

if __name__ == '__main__':
    app.run(debug=True)