"""Сервисы для приложения books."""
from django.conf import settings
from django.core.mail import send_mail


def send_new_book_email(book):
    """Отправляет письмо о создании новой книги.

    Args:
        book: Объект книги.
    """
    if not book.owner or not book.owner.email:
        return

    subject = f'Книга «{book.title}» добавлена'
    message = (
        f'Здравствуйте, {book.owner.username}!\n\n'
        f'Вы успешно добавили новую книгу:\n'
        f'Название: {book.title}\n'
        f'Автор: {book.author}\n'
        f'Жанр: {book.genre.name}\n\n'
        f'Спасибо за вклад в нашу библиотеку!'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[book.owner.email],
        fail_silently=True,
    )


def send_views_milestone_email(book):
    """Отправляет письмо владельцу при кратности просмотров 20.

    Args:
        book: Объект книги.
    """
    if not book.owner or not book.owner.email:
        return

    subject = f'Книгу «{book.title}» посмотрели {book.views} раз'
    message = (
        f'Здравствуйте, {book.owner.username}!\n\n'
        f'Вашу книгу «{book.title}» посмотрели {book.views} раз.\n'
        f'Продолжайте в том же духе!\n\n'
        f'С уважением,\nКоманда сайта.'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[book.owner.email],
        fail_silently=True,
    )
