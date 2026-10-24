"""Настройка админки для приложения books."""
from django.contrib import admin

from .models import Author, Book, Genre


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Админка для автора."""

    list_display = ('id', 'name', 'country', 'birth_date')
    search_fields = ('name', 'country')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для жанра."""

    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Админка для книги."""

    list_display = ('id', 'title', 'author', 'genre', 'year', 'owner', 'created_at')
    list_filter = ('genre', 'year', 'author')
    search_fields = ('title',)
