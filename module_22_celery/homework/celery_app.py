"""
В этом файле будут Celery-задачи
"""

from celery import Celery
from config import REDIS_URL
import os
from image import blur_image
from mail import send_email
import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

celery_app = Celery('blur_service', broker=REDIS_URL, backend=REDIS_URL)


@celery_app.task(bind=True)
def process_single_image(self, group_id, filename, image_data):
    try:
        print(f"Processing {filename} for {group_id}")

        # 1. Создаем папки
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('processed', exist_ok=True)

        # 2. Сохраняем оригинал
        orig_path = f"uploads/{filename}"
        with open(orig_path, 'wb') as f:
            f.write(image_data)

        # 3. Обрабатываем размытие
        processed_path = f"processed/blur_{filename}"
        blur_image(orig_path, processed_path)

        # 4. Отправляем почту
        email = r.hget(f"group:{group_id}", 'email')  # ← УБРАЛИ .decode()!
        print(f"Sending email to {email}")
        send_email(group_id, email, processed_path)

        # 5. Обновляем статус
        r.hincrby(f"group:{group_id}", 'processed', 1)
        total = int(r.hget(f"group:{group_id}", 'total'))
        processed = int(r.hget(f"group:{group_id}", 'processed'))

        if processed == total:
            r.hset(f"group:{group_id}", 'status', 'completed')

        # 6. Удаляем файлы
        os.remove(orig_path)
        os.remove(processed_path)

        print(f"✅ Completed {filename}")
        return {'status': 'success', 'filename': filename}

    except Exception as e:
        print(f"❌ Error: {e}")
        r.hset(f"group:{group_id}", 'status', 'failed')
        raise
