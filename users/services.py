"""Сервисы для приложения users."""
from django.conf import settings
from django.core.mail import send_mail


def send_welcome_email(user):
    """Отправляет приветственное письмо после регистрации.

    Args:
        user: Объект пользователя.
    """
    subject = 'Добро пожаловать!'
    message = (
        f'Здравствуйте, {user.username}!\n\n'
        f'Спасибо за регистрацию на нашем сайте.\n'
        f'Ваш аккаунт успешно создан.\n\n'
        f'С уважением,\nКоманда сайта.'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


def send_password_change_email(user):
    """Отправляет уведомление о смене пароля.

    Args:
        user: Объект пользователя.
    """
    subject = 'Пароль изменён'
    message = (
        f'Здравствуйте, {user.username}!\n\n'
        f'Ваш пароль был успешно изменён.\n'
        f'Если это были не вы — срочно свяжитесь с администрацией.\n\n'
        f'С уважением,\nКоманда сайта.'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )
