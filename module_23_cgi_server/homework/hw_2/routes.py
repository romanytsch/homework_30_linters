import json
from pathlib import Path
import mimetypes


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    # STATIC FILES
    if path.startswith('/static/'):
        static_path = path[7:].lstrip('/')
        base_dir = Path(__file__).parent.absolute()
        static_dir = base_dir / 'static'
        file_path = static_dir / static_path

        if file_path.exists() and file_path.is_file():
            content_type, _ = mimetypes.guess_type(str(file_path))
            if not content_type:
                content_type = 'application/octet-stream'

            with open(file_path, 'rb') as f:
                response_body = f.read()

            status = '200 OK'
            headers = [
                ('Content-Type', content_type),
                ('Content-Length', str(len(response_body)))
            ]
            start_response(status, headers)
            return [response_body]

        status = '404 Not Found'
        start_response(status, [('Content-Type', 'application/json')])
        return [json.dumps({'error': 'Static file not found'}).encode()]

    # JSON API роуты
    path_clean = path.rstrip('/')
    if path_clean.startswith('/hello/') and len(path_clean) > 6:
        username = path_clean[6:]
    elif path_clean == '/hello':
        username = 'username'
    else:
        username = None

    if username:
        response_data = {'message': 'hello', 'name': username}
        status = '200 OK'
    else:
        response_data = {'error': 'Not Found'}
        status = '404 Not Found'

    response_body = json.dumps(response_data).encode('utf-8')
    headers = [
        ('Content-Type', 'application/json; charset=utf-8'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, headers)
    return [response_body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('127.0.0.1', 5000, application)
    print("=== WSGI dev server http://127.0.0.1:5000 ===")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        httpd.server_close()
