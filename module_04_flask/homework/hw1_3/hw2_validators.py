"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import ValidationError



def number_length(min: int, max: int, message: Optional[str] = None):
    def _number_length(form, field):
        length = len(str(field.data))
        if length < min or length > max:
            msg = message or f"Длина должна быть от {min} до {max} символов."
            raise ValidationError(msg)
    return _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        length = len(str(field.data))
        if length < self.min or length > self.max:
            msg = self.message or f"Длина должна быть от {self.min} до {self.max} символов."
            raise ValidationError(msg)