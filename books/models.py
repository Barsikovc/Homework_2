"""Модели приложения books."""
from django.conf import settings
from django.db import models


class Author(models.Model):
    """Автор книги (родословная)."""

    name = models.CharField(max_length=200, unique=True, verbose_name='Имя')
    bio = models.TextField(blank=True, verbose_name='Биография')
    photo = models.ImageField(
        upload_to='authors/', blank=True, null=True, verbose_name='Фото',
    )
    birth_date = models.DateField(
        blank=True, null=True, verbose_name='Дата рождения',
    )
    country = models.CharField(max_length=100, blank=True, verbose_name='Страна')

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']

    def __str__(self):
        """Возвращает имя автора."""
        return self.name


class Genre(models.Model):
    """Жанр книги."""

    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(
        upload_to='genres/', blank=True, null=True, verbose_name='Изображение',
    )

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        """Возвращает название жанра."""
        return self.name


class Book(models.Model):
    """Книга."""

    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Автор',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Жанр',
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    cover = models.ImageField(
        upload_to='covers/', blank=True, null=True, verbose_name='Обложка',
    )
    year = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Год издания',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name='Владелец',
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']

    def __str__(self):
        """Возвращает название книги."""
        return f'{self.title} — {self.author.name}'


class Review(models.Model):
    """Отзыв пользователя на книгу."""

    RATING_CHOICES = [
        (1, 'Ужасно'),
        (2, 'Плохо'),
        (3, 'Нормально'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Книга',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        verbose_name='Оценка',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'user'],
                name='unique_review_per_book',
            ),
        ]

    def __str__(self):
        """Возвращает описание отзыва."""
        return f'{self.user.username} — {self.book.title} ({self.rating}/5)'
