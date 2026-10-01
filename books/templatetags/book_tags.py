"""Кастомные теги и фильтры для приложения books."""
from django import template

register = template.Library()


@register.filter(name='truncate_text')
def truncate_text(value, max_length=100):
    """Обрезает текст до указанной длины в символах.

    Args:
        value: Исходный текст.
        max_length: Максимум символов.

    Returns:
        str: Обрезанный текст с многоточием.
    """
    if not value:
        return ''
    text = str(value)
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + '...'

@register.simple_tag(name='genre_book_count')
def genre_book_count(genre):
    """Возвращает количество книг в жанре.

    Args:
        genre: Объект Genre.

    Returns:
        int: Количество книг.
    """
    if not genre:
        return 0
    return genre.books.count()


@register.filter(name='is_owner')
def is_owner(obj, user):
    """Проверяет, является ли пользователь владельцем объекта.

    Args:
        obj: Объект с полем owner.
        user: Пользователь.

    Returns:
        bool: True, если пользователь — владелец.
    """
    if not user or not user.is_authenticated:
        return False
    return getattr(obj, 'owner_id', None) == user.id
