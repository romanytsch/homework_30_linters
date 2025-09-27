"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import shlex
import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    args = request.args.getlist('arg')
    safe_args = [shlex.quote(arg) for arg in args]
    command = ['ps'] + safe_args

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"Ошибка в выполнении команды: {e}"

    return f"<pre>{output}</pre>"


if __name__ == "__main__":
    app.run(debug=True)
