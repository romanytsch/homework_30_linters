import json
from flask import Flask, request


app = Flask(__name__)

logs = []

@app.route('/log', methods=['POST'])
def log_save():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    data = request.get_json()
    if data:
        logs.append(data)
        print(f"Log received: {data}")
    return 'Log received', 200



@app.route('/logs', methods=['GET'])
def logs_view():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    try:
        logs_html = '<pre>' + '\n'.join(json.dumps(log, ensure_ascii=False, indent=2) for log in logs) + '</pre>'
        return logs_html
    except Exception as e:
        return f'Error: {str(e)}', 500

# TODO запустить сервер
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False, threaded=True)