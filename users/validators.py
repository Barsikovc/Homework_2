"""Валидаторы для приложения users."""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomPasswordValidator:
    """Валидатор пароля.

    Требования:
    - минимум 8 символов;
    - хотя бы одна заглавная буква;
    - хотя бы одна строчная буква;
    - хотя бы одна цифра;
    - хотя бы один специальный символ.
    """

    def validate(self, password, user=None):
        """Проверяет пароль на соответствие правилам."""
        if len(password) < 8:
            raise ValidationError(
                _('Пароль должен содержать минимум 8 символов.'),
                code='password_too_short',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _('Пароль должен содержать хотя бы одну заглавную букву.'),
                code='password_no_upper',
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _('Пароль должен содержать хотя бы одну строчную букву.'),
                code='password_no_lower',
            )
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _('Пароль должен содержать хотя бы одну цифру.'),
                code='password_no_number',
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-]', password):
            raise ValidationError(
                _('Пароль должен содержать хотя бы один специальный символ.'),
                code='password_no_special',
            )

    def get_help_text(self):
        """Возвращает текст подсказки."""
        return _(
            'Пароль должен содержать минимум 8 символов, '
            'заглавную и строчную буквы, цифру и специальный символ.'
        )
