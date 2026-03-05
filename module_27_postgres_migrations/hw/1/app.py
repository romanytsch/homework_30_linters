from flask import Flask
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'pass')

@app.route('/')
def hello():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()
        return f"Flask + Gunicorn + PostgreSQL работает!<br>Версия PostgreSQL: {version['version']}"
    except Exception as e:
        return f"Ошибка подключения к БД: {str(e)}", 500

@app.route('/health')
def health():
    return {"status": "ok", "service": "flask-app"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
