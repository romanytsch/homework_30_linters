"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""
import os

# https://yandex.ru/support/mail/mail-clients/others.html

SMTP_USER = "romanytsch@yandex.ru"
SMTP_HOST = "smtp.yandex.com"
SMTP_PASSWORD = "mzdjkaovzopkjddd"
SMTP_PORT = 587

# Redis настройки (для Celery)
REDIS_URL = 'redis://localhost:6379/0'

# Celery Beat расписание (еженедельная рассылка)
WEEKLY_NEWSLETTER_TIME = 'mon 09:00'  # Понедельник в 9 утра