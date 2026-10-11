"""Формы приложения books."""
from datetime import date

from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    """Форма для создания и редактирования книги."""

    class Meta:
        """Метаданные формы."""

        model = Book
        fields = ['title', 'author', 'genre', 'description', 'cover', 'year']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'author': forms.TextInput(attrs={'class': 'form-input'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }

    def clean_title(self):
        """Проверяет минимальную длину названия."""
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Название должно содержать минимум 3 символа.')
        return title

    def clean_year(self):
        """Проверяет, что год не в будущем."""
        year = self.cleaned_data.get('year')
        if year and year > date.today().year:
            raise forms.ValidationError('Год издания не может быть в будущем.')
        if year and year < 1000:
            raise forms.ValidationError('Год должен быть не меньше 1000.')
        return year
