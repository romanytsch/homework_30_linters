"""
В этом файле будет ваше Flask-приложение
"""

from flask import Flask, request, jsonify
from celery import group
from celery_app import celery_app, process_single_image  # ← Правильный импорт!
import uuid, os, redis
from werkzeug.utils import secure_filename
from datetime import datetime
from image import blur_image
from mail import send_email

app_flask = Flask(__name__)
app_flask.config['UPLOAD_FOLDER'] = 'uploads'
app_flask.config['PROCESSED_FOLDER'] = 'processed'

os.makedirs(app_flask.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app_flask.config['PROCESSED_FOLDER'], exist_ok=True)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
SUBSCRIBERS_KEY = "subscribers"


@app_flask.route('/blur', methods=['POST'])
def blur_images():
    files = request.files.getlist('images')
    email = request.form.get('email')

    if not email or not files:
        return jsonify({'error': 'Email and images required'}), 400

    group_id = str(uuid.uuid4())
    task_info = {
        'email': email, 'total': len(files), 'processed': 0,
        'status': 'pending', 'created_at': datetime.now().isoformat()
    }
    r.hset(f"group:{group_id}", mapping=task_info)

    # Группа задач из celery_app
    job_tasks = group(process_single_image.s(group_id, secure_filename(f.filename), f.stream.read()) for f in files)
    job_tasks.apply_async()

    return jsonify({'group_id': group_id}), 202


@app_flask.route('/status/<group_id>')
def status(group_id):
    data = r.hgetall(f"group:{group_id}")
    return jsonify(data) if data else jsonify({'error': 'Not found'}), 404


@app_flask.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    r.sadd(SUBSCRIBERS_KEY, email)
    return jsonify({'message': 'Subscribed'})


@app_flask.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.json.get('email')
    r.srem(SUBSCRIBERS_KEY, email)
    return jsonify({'message': 'Unsubscribed'})


if __name__ == '__main__':
    app_flask.run(debug=True, port=5000)
