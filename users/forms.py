"""Формы для приложения users."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

User = get_user_model()


class StyleFormMixin:
    """Миксин для добавления CSS-классов ко всем полям формы."""

    def __init__(self, *args, **kwargs):
        """Добавляет классы к виджетам."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault('class', 'form-checkbox')
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault('class', 'form-select')
            else:
                widget.attrs.setdefault('class', 'form-input')
                widget.attrs.setdefault(
                    'placeholder', field.label or field_name,
                )


class UserRegisterForm(StyleFormMixin, forms.ModelForm):
    """Форма регистрации нового пользователя."""

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        min_length=8,
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
    )

    class Meta:
        """Метаданные формы."""

        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone']

    def clean_email(self):
        """Проверяет уникальность email."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return email

    def clean(self):
        """Проверяет совпадение паролей."""
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned

    def save(self, commit=True):
        """Создаёт пользователя с зашифрованным паролем."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма входа в аккаунт."""

    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
    )


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    """Форма редактирования профиля."""

    class Meta:
        """Метаданные формы."""

        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']


class CustomPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    """Форма смены пароля со стилизацией."""
