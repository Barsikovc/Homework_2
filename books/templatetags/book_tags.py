"""Кастомные теги и фильтры для приложения books."""
from django import template

register = template.Library()


@register.filter(name='truncate_text')
def truncate_text(value, max_length=100):
    """Обрезает текст до max_length символов."""
    if not value:
        return ''
    text = str(value)
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + '...'


@register.simple_tag(name='genre_book_count')
def genre_book_count(genre):
    """Возвращает количество книг в жанре."""
    if not genre:
        return 0
    return genre.books.count()


@register.filter(name='is_owner')
def is_owner(obj, user):
    """Проверяет, владелец ли пользователь."""
    if not user or not user.is_authenticated:
        return False
    return getattr(obj, 'owner_id', None) == user.id


@register.filter(name='can_edit')
def can_edit(obj, user):
    """Проверяет, может ли пользователь редактировать объект.

    Разрешено: владелец, модератор, админ.
    """
    if not user or not user.is_authenticated:
        return False
    if user.is_moderator:
        return True
    return getattr(obj, 'owner_id', None) == user.id


@register.filter(name='can_create_book')
def can_create_book(user):
    """Проверяет, может ли пользователь создавать книги."""
    if not user or not user.is_authenticated:
        return False
    return user.is_author

@register.filter(name='can_toggle_active')
def can_toggle_active(user):
    """Может ли пользователь менять активность."""
    if not user or not user.is_authenticated:
        return False
    return user.is_moderator


@register.filter(name='is_moderator')
def is_moderator(user):
    """Проверяет, модератор ли пользователь."""
    if not user or not user.is_authenticated:
        return False
    return user.is_moderator
