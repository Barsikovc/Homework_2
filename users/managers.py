"""Менеджеры для приложения users."""
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Менеджер для кастомной модели пользователя."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Создаёт обычного пользователя.

        Args:
            username: Логин пользователя.
            email: Email пользователя.
            password: Пароль.
            **extra_fields: Дополнительные поля.

        Returns:
            CustomUser: Созданный пользователь.

        Raises:
            ValueError: Если username или email пустые.
        """
        if not username:
            raise ValueError('Username обязателен.')
        if not email:
            raise ValueError('Email обязателен.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Создаёт суперпользователя.

        Args:
            username: Логин.
            email: Email.
            password: Пароль.
            **extra_fields: Дополнительные поля.

        Returns:
            CustomUser: Созданный суперпользователь.

        Raises:
            ValueError: Если is_staff или is_superuser не True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
