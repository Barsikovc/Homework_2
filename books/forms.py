"""Формы приложения books."""
from datetime import date

from django import forms

from .models import Author, Book


class StyleFormMixin:
    """Миксин для CSS-классов."""

    def __init__(self, *args, **kwargs):
        """Добавляет классы к виджетам."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault('class', 'form-checkbox')
            elif isinstance(widget, (forms.Select, forms.SelectDateWidget)):
                widget.attrs.setdefault('class', 'form-select')
            else:
                widget.attrs.setdefault('class', 'form-input')
                widget.attrs.setdefault('placeholder', field.label or field_name)


class BookForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания и редактирования книги."""

    class Meta:
        """Метаданные формы."""

        model = Book
        fields = ['title', 'author', 'genre', 'description', 'cover', 'year']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_title(self):
        """Проверяет минимальную длину названия."""
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Название должно содержать минимум 3 символа.')
        return title

    def clean_year(self):
        """Проверяет год."""
        year = self.cleaned_data.get('year')
        if year and year > date.today().year:
            raise forms.ValidationError('Год издания не может быть в будущем.')
        if year and year < 1000:
            raise forms.ValidationError('Год должен быть не меньше 1000.')
        return year


class AuthorForm(StyleFormMixin, forms.ModelForm):
    """Форма для автора."""

    class Meta:
        """Метаданные формы."""

        model = Author
        fields = ['name', 'bio', 'photo', 'birth_date', 'country']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_name(self):
        """Проверяет длину имени."""
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Имя должно содержать минимум 2 символа.')
        return name


class GenreForm(StyleFormMixin, forms.ModelForm):
    """Форма для жанра."""

    class Meta:
        """Метаданные формы."""

        from .models import Genre
        model = Genre
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class BookUpdateForm(StyleFormMixin, forms.ModelForm):
    """Форма редактирования книги для владельца (без активности, владельца, просмотров)."""

    class Meta:
        """Метаданные формы."""

        model = Book
        fields = ['title', 'author', 'genre', 'description', 'cover', 'year']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_title(self):
        """Проверяет длину названия."""
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Название должно содержать минимум 3 символа.')
        return title

    def clean_year(self):
        """Проверяет год."""
        year = self.cleaned_data.get('year')
        if year and year > date.today().year:
            raise forms.ValidationError('Год издания не может быть в будущем.')
        if year and year < 1000:
            raise forms.ValidationError('Год должен быть не меньше 1000.')
        return year


class BookAdminUpdateForm(StyleFormMixin, forms.ModelForm):
    """Форма редактирования книги для админа/модератора (все поля)."""

    class Meta:
        """Метаданные формы."""

        model = Book
        fields = [
            'title', 'author', 'genre', 'description', 'cover', 'year',
            'is_active', 'owner', 'views',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_title(self):
        """Проверяет длину названия."""
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Название должно содержать минимум 3 символа.')
        return title

    def clean_year(self):
        """Проверяет год."""
        year = self.cleaned_data.get('year')
        if year and year > date.today().year:
            raise forms.ValidationError('Год издания не может быть в будущем.')
        if year and year < 1000:
            raise forms.ValidationError('Год должен быть не меньше 1000.')
        return year
