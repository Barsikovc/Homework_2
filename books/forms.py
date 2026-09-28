"""Формы приложения books."""
from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    """Форма для создания и редактирования книги."""

    class Meta:
        """Метаданные формы."""

        model = Book
        fields = ['title', 'author', 'genre', 'description', 'cover', 'year']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
