"""Настройка админки для приложения books."""
from django.contrib import admin

from .models import Book, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для модели Genre."""

    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Админка для модели Book."""

    list_display = ('id', 'title', 'author', 'genre', 'year', 'owner', 'created_at')
    list_filter = ('genre', 'year')
    search_fields = ('title', 'author')
