import operator
from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask("calculator")  # без точки в имени

# без enable_web_browsable_api=True
jsonrpc = JSONRPC(app, '/api')


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    Сложение двух чисел.

    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.add",
            "params": {"a": 7.8, "b": 5.3},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 13.1
    }
    """
    return operator.add(a, b)


@jsonrpc.method('calc.subtract')
def subtract(a: float, b: float) -> float:
    """
    Вычитание двух чисел.

    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.subtract",
            "params": {"a": 10.0, "b": 3.5},
            "id": "2"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
      "id": "2",
      "jsonrpc": "2.0",
      "result": 6.5
    }
    """
    return operator.sub(a, b)


@jsonrpc.method('calc.multiply')
def multiply(a: float, b: float) -> float:
    """
    Умножение двух чисел.

    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.multiply",
            "params": {"a": 4.2, "b": 3.0},
            "id": "3"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
      "id": "3",
      "jsonrpc": "2.0",
      "result": 12.6
    }
    """
    return operator.mul(a, b)


@jsonrpc.method('calc.divide')
def divide(a: float, b: float) -> float:
    """
    Деление двух чисел.

    При делении на ноль сервер вернёт ошибку JSON‑RPC.

    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.divide",
            "params": {"a": 10.0, "b": 2.0},
            "id": "4"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
      "id": "4",
      "jsonrpc": "2.0",
      "result": 5.0
    }

    Пример ошибки (деление на ноль):

    $ curl -i -X POST -H "Content-Type: application/json" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.divide",
            "params": {"a": 10.0, "b": 0.0},
            "id": "5"
        }' http://localhost:5000/api

    {
      "id": "5",
      "jsonrpc": "2.0",
      "error": {
        "code": -32603,
        "message": "Division by zero"
      }
    }
    """
    if b == 0:
        raise Exception("Division by zero")
    return operator.truediv(a, b)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
