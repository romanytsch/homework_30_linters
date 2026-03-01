import json
import os


def application(environ, start_response):
    # Парсим PATH_INFO из environ (uWSGI передает URL здесь)
    path = environ.get('PATH_INFO', '/').rstrip('/')

    # Извлекаем username из пути /hello/username
    if path.startswith('/hello/') and len(path) > 6:
        username = path[6:]  # все после /hello/
    elif path == '/hello':
        username = 'username'
    else:
        username = None

    # Формируем JSON ответ
    if username:
        response_data = {
            'message': 'hello',
            'name': username
        }
        status = '200 OK'
    else:
        response_data = {'error': 'Not Found'}
        status = '404 Not Found'

    # JSON строка
    response_body = json.dumps(response_data).encode('utf-8')

    # WSGI заголовки
    response_headers = [
        ('Content-Type', 'application/json; charset=utf-8'),
        ('Content-Length', str(len(response_body)))
    ]

    # Отправляем заголовки (обязательный шаг WSGI)
    start_response(status, response_headers)

    # Возвращаем итерируемый объект с телом ответа
    return [response_body]


# Для локального тестирования (если нужно)
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    with make_server('', 8000, application) as httpd:
        print("WSGI сервер запущен на http://localhost:8000")
        httpd.serve_forever()

